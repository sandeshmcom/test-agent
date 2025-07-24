"""AI Provider interface for manual test case generation."""

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class TestPriority(Enum):
    """Test case priority levels."""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TestType(Enum):
    """Types of manual tests."""
    FUNCTIONAL = "Functional"
    UI_UX = "UI/UX"
    INTEGRATION = "Integration"
    PERFORMANCE = "Performance"
    SECURITY = "Security"
    USABILITY = "Usability"
    COMPATIBILITY = "Compatibility"
    REGRESSION = "Regression"


@dataclass
class TestStep:
    """Individual test step."""
    step_number: int
    action: str
    expected_result: str
    notes: Optional[str] = None


@dataclass
class ManualTestCase:
    """Manual test case structure."""
    test_id: str
    title: str
    description: str
    preconditions: List[str]
    test_steps: List[TestStep]
    expected_outcome: str
    test_type: TestType
    priority: TestPriority
    estimated_time: str  # e.g., "5 minutes"
    tags: List[str]
    requirements_covered: List[str]
    test_data_needed: Optional[str] = None
    environment: Optional[str] = None


@dataclass
class TestCaseGenerationRequest:
    """Request object for manual test case generation."""
    feature_description: str
    requirements: List[str]
    user_stories: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
    application_type: str = "web"  # web, mobile, desktop, api
    target_audience: Optional[str] = None
    business_context: Optional[str] = None
    existing_functionality: Optional[str] = None
    integration_points: Optional[List[str]] = None
    test_types_requested: Optional[List[TestType]] = None


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    async def generate_manual_tests(self, request: TestCaseGenerationRequest) -> List[ManualTestCase]:
        """Generate manual test cases for the given requirements."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is properly configured."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider for manual test case generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def generate_manual_tests(self, request: TestCaseGenerationRequest) -> List[ManualTestCase]:
        """Generate manual test cases using OpenAI API."""
        if not self.is_available():
            raise ValueError("OpenAI API key not configured")
        
        try:
            from openai import AsyncOpenAI
            if not self._client:
                self._client = AsyncOpenAI(api_key=self.api_key)
            
            prompt = self._build_prompt(request)
            
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            
            return self._parse_response(response.choices[0].message.content)
        
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        return """You are an expert QA Engineer and Test Case Designer. Your task is to create comprehensive manual test cases that ensure thorough testing coverage. Focus on:

1. **Functional Testing**: Core feature functionality, business logic validation
2. **UI/UX Testing**: User interface elements, user experience flows
3. **Edge Cases**: Boundary conditions, unusual scenarios
4. **Error Handling**: Invalid inputs, system failures, error messages
5. **Integration Testing**: Data flow between components/systems
6. **Usability Testing**: User-friendliness, accessibility
7. **Performance**: Response times, load handling (where applicable)
8. **Security**: Data protection, input validation, authorization

Create test cases that are:
- Clear and unambiguous with step-by-step instructions
- Executable by any QA tester without domain expertise
- Cover positive, negative, and edge case scenarios
- Include specific expected results
- Prioritized by business impact
- Traceable to requirements

Return your response in JSON format with this structure:
{
    "test_cases": [
        {
            "test_id": "TC_001",
            "title": "Clear, descriptive test case name",
            "description": "What this test validates",
            "preconditions": ["Setup requirement 1", "Setup requirement 2"],
            "test_steps": [
                {
                    "step_number": 1,
                    "action": "Detailed action to perform",
                    "expected_result": "Expected outcome",
                    "notes": "Optional additional info"
                }
            ],
            "expected_outcome": "Overall expected result",
            "test_type": "Functional|UI_UX|Integration|Performance|Security|Usability|Compatibility|Regression",
            "priority": "Critical|High|Medium|Low",
            "estimated_time": "X minutes",
            "tags": ["tag1", "tag2"],
            "requirements_covered": ["REQ-001"],
            "test_data_needed": "Description of test data",
            "environment": "Test environment requirements"
        }
    ]
}"""
    
    def _build_prompt(self, request: TestCaseGenerationRequest) -> str:
        prompt = f"""Create comprehensive manual test cases for the following feature:

**Feature Description:**
{request.feature_description}

**Requirements:**
{chr(10).join(f"- {req}" for req in request.requirements)}

**Application Type:** {request.application_type}
"""
        
        if request.user_stories:
            prompt += f"\n**User Stories:**\n{chr(10).join(f'- {story}' for story in request.user_stories)}\n"
        
        if request.acceptance_criteria:
            prompt += f"\n**Acceptance Criteria:**\n{chr(10).join(f'- {criteria}' for criteria in request.acceptance_criteria)}\n"
        
        if request.target_audience:
            prompt += f"\n**Target Audience:** {request.target_audience}\n"
        
        if request.business_context:
            prompt += f"\n**Business Context:** {request.business_context}\n"
        
        if request.existing_functionality:
            prompt += f"\n**Existing Functionality:** {request.existing_functionality}\n"
        
        if request.integration_points:
            prompt += f"\n**Integration Points:** {', '.join(request.integration_points)}\n"
        
        if request.test_types_requested:
            test_types = [t.value for t in request.test_types_requested]
            prompt += f"\n**Focus on these test types:** {', '.join(test_types)}\n"
        
        prompt += """
Generate a comprehensive set of manual test cases covering:
1. Happy path scenarios
2. Error/exception scenarios  
3. Edge cases and boundary conditions
4. Different user roles/permissions (if applicable)
5. Cross-browser/device compatibility (if applicable)
6. Integration scenarios
7. Performance considerations
8. Security aspects

Ensure test cases are practical, executable, and provide clear pass/fail criteria.
"""
        
        return prompt
    
    def _parse_response(self, response: str) -> List[ManualTestCase]:
        """Parse AI response into ManualTestCase objects."""
        import json
        import re
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON found in response")
            
            data = json.loads(json_match.group())
            test_cases = []
            
            for idx, tc_data in enumerate(data.get("test_cases", [])):
                # Parse test steps
                test_steps = []
                for step_data in tc_data.get("test_steps", []):
                    test_steps.append(TestStep(
                        step_number=step_data.get("step_number", 1),
                        action=step_data.get("action", ""),
                        expected_result=step_data.get("expected_result", ""),
                        notes=step_data.get("notes")
                    ))
                
                # Parse enums
                test_type = TestType.FUNCTIONAL
                try:
                    test_type = TestType(tc_data.get("test_type", "Functional"))
                except ValueError:
                    pass  # Default to FUNCTIONAL
                
                priority = TestPriority.MEDIUM
                try:
                    priority = TestPriority(tc_data.get("priority", "Medium"))
                except ValueError:
                    pass  # Default to MEDIUM
                
                test_cases.append(ManualTestCase(
                    test_id=tc_data.get("test_id", f"TC_{idx+1:03d}"),
                    title=tc_data.get("title", ""),
                    description=tc_data.get("description", ""),
                    preconditions=tc_data.get("preconditions", []),
                    test_steps=test_steps,
                    expected_outcome=tc_data.get("expected_outcome", ""),
                    test_type=test_type,
                    priority=priority,
                    estimated_time=tc_data.get("estimated_time", "5 minutes"),
                    tags=tc_data.get("tags", []),
                    requirements_covered=tc_data.get("requirements_covered", []),
                    test_data_needed=tc_data.get("test_data_needed"),
                    environment=tc_data.get("environment")
                ))
            
            return test_cases
        
        except Exception as e:
            raise RuntimeError(f"Failed to parse AI response: {str(e)}")


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider for manual test case generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self._client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def generate_manual_tests(self, request: TestCaseGenerationRequest) -> List[ManualTestCase]:
        """Generate manual test cases using Anthropic API."""
        if not self.is_available():
            raise ValueError("Anthropic API key not configured")
        
        try:
            import anthropic
            if not self._client:
                self._client = anthropic.AsyncAnthropic(api_key=self.api_key)
            
            prompt = self._build_prompt(request)
            
            response = await self._client.messages.create(
                model=self.model,
                max_tokens=3000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return self._parse_response(response.content[0].text)
        
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}")
    
    def _build_prompt(self, request: TestCaseGenerationRequest) -> str:
        system_context = """You are an expert QA Engineer specializing in manual test case design. Create comprehensive test cases covering functional, UI/UX, edge cases, error handling, and integration scenarios."""
        
        prompt = f"""{system_context}

Create manual test cases for this feature:

Feature: {request.feature_description}

Requirements:
{chr(10).join(f"- {req}" for req in request.requirements)}

Application Type: {request.application_type}
"""
        
        if request.user_stories:
            prompt += f"\nUser Stories: {', '.join(request.user_stories)}"
        
        if request.acceptance_criteria:
            prompt += f"\nAcceptance Criteria: {', '.join(request.acceptance_criteria)}"
        
        if request.business_context:
            prompt += f"\nBusiness Context: {request.business_context}"
        
        prompt += """

Return JSON format with comprehensive manual test cases:
{
    "test_cases": [
        {
            "test_id": "TC_001",
            "title": "Test case name",
            "description": "What this validates",
            "preconditions": ["setup requirements"],
            "test_steps": [
                {
                    "step_number": 1,
                    "action": "Step to perform",
                    "expected_result": "Expected outcome",
                    "notes": "Optional notes"
                }
            ],
            "expected_outcome": "Overall expected result",
            "test_type": "Functional|UI_UX|Integration|Performance|Security|Usability|Compatibility|Regression",
            "priority": "Critical|High|Medium|Low",
            "estimated_time": "X minutes",
            "tags": ["relevant", "tags"],
            "requirements_covered": ["REQ-001"],
            "test_data_needed": "Test data description",
            "environment": "Environment requirements"
        }
    ]
}

Cover positive flows, negative scenarios, edge cases, error handling, and integration points."""
        
        return prompt
    
    def _parse_response(self, response: str) -> List[ManualTestCase]:
        """Parse AI response into ManualTestCase objects."""
        # Reuse the same parsing logic as OpenAI
        return OpenAIProvider._parse_response(self, response)


def get_available_providers() -> Dict[str, AIProvider]:
    """Get all available AI providers."""
    providers = {}
    
    openai_provider = OpenAIProvider()
    if openai_provider.is_available():
        providers["openai"] = openai_provider
    
    anthropic_provider = AnthropicProvider()
    if anthropic_provider.is_available():
        providers["anthropic"] = anthropic_provider
    
    return providers