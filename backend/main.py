"""FastAPI backend for AI Test Agent Web UI."""

import asyncio
import os
import sys
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# Add the parent directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.test_agent import TestAgent
from src.core.ai_provider import TestType, TestPriority, get_available_providers


app = FastAPI(
    title="AI Test Agent API",
    description="AI-powered manual test case generation API",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class TestGenerationRequest(BaseModel):
    feature_description: str
    requirements: List[str]
    user_stories: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
    application_type: str = "web"
    target_audience: Optional[str] = None
    business_context: Optional[str] = None
    existing_functionality: Optional[str] = None
    integration_points: Optional[List[str]] = None
    test_types_requested: Optional[List[str]] = None
    provider: str = "auto"


class TestCaseResponse(BaseModel):
    test_id: str
    title: str
    description: str
    preconditions: List[str]
    test_steps: List[Dict[str, Any]]
    expected_outcome: str
    test_type: str
    priority: str
    estimated_time: str
    tags: List[str]
    requirements_covered: List[str]
    test_data_needed: Optional[str] = None
    environment: Optional[str] = None


class GenerationResponse(BaseModel):
    success: bool
    test_cases: List[TestCaseResponse]
    summary: Dict[str, Any]
    generation_time: float
    provider_used: str
    error: Optional[str] = None


class ProviderStatus(BaseModel):
    name: str
    available: bool
    description: str


class ExportRequest(BaseModel):
    test_cases: List[TestCaseResponse]
    format: str  # json, csv, markdown, html
    filename: Optional[str] = None


# Global variables for session management
current_test_cases = []
generation_tasks = {}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Test Agent API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/providers", response_model=List[ProviderStatus])
async def get_providers():
    """Get available AI providers."""
    try:
        providers = get_available_providers()
        
        provider_list = []
        
        # Check OpenAI
        openai_available = "openai" in providers
        provider_list.append(ProviderStatus(
            name="openai",
            available=openai_available,
            description="OpenAI GPT-4 - Recommended for comprehensive test cases"
        ))
        
        # Check Anthropic
        anthropic_available = "anthropic" in providers
        provider_list.append(ProviderStatus(
            name="anthropic",
            available=anthropic_available,
            description="Anthropic Claude - Alternative AI provider"
        ))
        
        return provider_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking providers: {str(e)}")


@app.post("/generate", response_model=GenerationResponse)
async def generate_test_cases(request: TestGenerationRequest):
    """Generate manual test cases."""
    start_time = datetime.now()
    
    try:
        # Initialize test agent
        agent = TestAgent(provider_name=request.provider)
        
        # Generate test cases
        test_cases = await agent.generate_test_cases(
            feature_description=request.feature_description,
            requirements=request.requirements,
            user_stories=request.user_stories,
            acceptance_criteria=request.acceptance_criteria,
            application_type=request.application_type,
            target_audience=request.target_audience,
            business_context=request.business_context,
            existing_functionality=request.existing_functionality,
            integration_points=request.integration_points,
            test_types_requested=request.test_types_requested
        )
        
        # Convert to response format
        response_test_cases = []
        for tc in test_cases:
            test_steps = [
                {
                    "step_number": step.step_number,
                    "action": step.action,
                    "expected_result": step.expected_result,
                    "notes": step.notes
                }
                for step in tc.test_steps
            ]
            
            response_test_cases.append(TestCaseResponse(
                test_id=tc.test_id,
                title=tc.title,
                description=tc.description,
                preconditions=tc.preconditions,
                test_steps=test_steps,
                expected_outcome=tc.expected_outcome,
                test_type=tc.test_type.value,
                priority=tc.priority.value,
                estimated_time=tc.estimated_time,
                tags=tc.tags,
                requirements_covered=tc.requirements_covered,
                test_data_needed=tc.test_data_needed,
                environment=tc.environment
            ))
        
        # Get summary
        summary = agent.get_test_summary(test_cases)
        
        # Calculate generation time
        generation_time = (datetime.now() - start_time).total_seconds()
        
        # Store test cases for export
        global current_test_cases
        current_test_cases = test_cases
        
        return GenerationResponse(
            success=True,
            test_cases=response_test_cases,
            summary=summary,
            generation_time=generation_time,
            provider_used=agent.provider_name
        )
    
    except Exception as e:
        generation_time = (datetime.now() - start_time).total_seconds()
        return GenerationResponse(
            success=False,
            test_cases=[],
            summary={},
            generation_time=generation_time,
            provider_used="",
            error=str(e)
        )


@app.post("/export/{format}")
async def export_test_cases(format: str, export_request: ExportRequest):
    """Export test cases to specified format."""
    try:
        if not current_test_cases:
            raise HTTPException(status_code=400, detail="No test cases available for export")
        
        # Initialize agent for export functionality
        agent = TestAgent(provider_name="auto")
        
        # Export test cases
        filename = export_request.filename or f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        output_path = os.path.join("exports", filename)
        
        # Create exports directory if it doesn't exist
        os.makedirs("exports", exist_ok=True)
        
        agent.export_test_cases(current_test_cases, format, output_path)
        
        return FileResponse(
            path=output_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@app.get("/export/{format}")
async def export_current_test_cases(format: str):
    """Export currently stored test cases."""
    try:
        if not current_test_cases:
            raise HTTPException(status_code=400, detail="No test cases available for export")
        
        # Initialize agent for export functionality
        agent = TestAgent(provider_name="auto")
        
        # Export test cases
        filename = f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        output_path = os.path.join("exports", filename)
        
        # Create exports directory if it doesn't exist
        os.makedirs("exports", exist_ok=True)
        
        agent.export_test_cases(current_test_cases, format, output_path)
        
        return FileResponse(
            path=output_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@app.get("/test-types")
async def get_test_types():
    """Get available test types."""
    return [
        {"value": "Functional", "label": "Functional", "description": "Core feature functionality testing"},
        {"value": "UI/UX", "label": "UI/UX", "description": "User interface and experience testing"},
        {"value": "Integration", "label": "Integration", "description": "System integration testing"},
        {"value": "Performance", "label": "Performance", "description": "Performance and load testing"},
        {"value": "Security", "label": "Security", "description": "Security and vulnerability testing"},
        {"value": "Usability", "label": "Usability", "description": "User-friendliness and accessibility testing"},
        {"value": "Compatibility", "label": "Compatibility", "description": "Cross-browser and device compatibility"},
        {"value": "Regression", "label": "Regression", "description": "Regression testing for existing features"}
    ]


@app.get("/application-types")
async def get_application_types():
    """Get available application types."""
    return [
        {"value": "web", "label": "Web Application", "description": "Browser-based web applications"},
        {"value": "mobile", "label": "Mobile Application", "description": "iOS/Android mobile apps"},
        {"value": "desktop", "label": "Desktop Application", "description": "Desktop software applications"},
        {"value": "api", "label": "API/Backend", "description": "REST APIs and backend services"}
    ]


@app.delete("/clear")
async def clear_test_cases():
    """Clear currently stored test cases."""
    global current_test_cases
    current_test_cases = []
    return {"message": "Test cases cleared successfully"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )