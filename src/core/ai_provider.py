"""AI Provider interface for different LLM services."""

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class TestGenerationRequest:
    """Request object for test generation."""
    source_code: str
    language: str
    test_framework: str
    function_name: Optional[str] = None
    class_name: Optional[str] = None
    additional_context: Optional[str] = None
    coverage_requirements: List[str] = None


@dataclass
class GeneratedTest:
    """Generated test case result."""
    test_code: str
    test_name: str
    description: str
    coverage_areas: List[str]
    confidence_score: float


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    async def generate_tests(self, request: TestGenerationRequest) -> List[GeneratedTest]:
        """Generate test cases for the given source code."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is properly configured."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider for test generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def generate_tests(self, request: TestGenerationRequest) -> List[GeneratedTest]:
        """Generate tests using OpenAI API."""
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
                max_tokens=2000
            )
            
            return self._parse_response(response.choices[0].message.content, request)
        
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        return """You are an expert software testing engineer. Your task is to generate comprehensive, 
        high-quality test cases for the given source code. Focus on:
        
        1. Edge cases and boundary conditions
        2. Error handling and exception scenarios
        3. Normal operation flows
        4. Integration points
        5. Performance considerations where relevant
        
        Generate tests that are:
        - Well-documented with clear descriptions
        - Follow testing best practices
        - Use appropriate assertions
        - Cover different code paths
        - Are maintainable and readable
        
        Return your response in JSON format with the following structure:
        {
            "tests": [
                {
                    "test_name": "test_function_name",
                    "description": "What this test verifies",
                    "test_code": "Complete test function code",
                    "coverage_areas": ["area1", "area2"],
                    "confidence_score": 0.9
                }
            ]
        }"""
    
    def _build_prompt(self, request: TestGenerationRequest) -> str:
        prompt = f"""Generate comprehensive test cases for the following {request.language} code:

```{request.language}
{request.source_code}
```

Target testing framework: {request.test_framework}
"""
        
        if request.function_name:
            prompt += f"Focus on testing function: {request.function_name}\n"
        
        if request.class_name:
            prompt += f"Focus on testing class: {request.class_name}\n"
        
        if request.additional_context:
            prompt += f"Additional context: {request.additional_context}\n"
        
        if request.coverage_requirements:
            prompt += f"Required coverage areas: {', '.join(request.coverage_requirements)}\n"
        
        return prompt
    
    def _parse_response(self, response: str, request: TestGenerationRequest) -> List[GeneratedTest]:
        """Parse AI response into GeneratedTest objects."""
        import json
        import re
        
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                tests = []
                
                for test_data in data.get("tests", []):
                    tests.append(GeneratedTest(
                        test_code=test_data.get("test_code", ""),
                        test_name=test_data.get("test_name", ""),
                        description=test_data.get("description", ""),
                        coverage_areas=test_data.get("coverage_areas", []),
                        confidence_score=test_data.get("confidence_score", 0.5)
                    ))
                
                return tests
            else:
                # Fallback: treat entire response as test code
                return [GeneratedTest(
                    test_code=response,
                    test_name="generated_test",
                    description="Generated test case",
                    coverage_areas=["general"],
                    confidence_score=0.6
                )]
        
        except Exception as e:
            raise RuntimeError(f"Failed to parse AI response: {str(e)}")


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider for test generation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self._client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def generate_tests(self, request: TestGenerationRequest) -> List[GeneratedTest]:
        """Generate tests using Anthropic API."""
        if not self.is_available():
            raise ValueError("Anthropic API key not configured")
        
        try:
            import anthropic
            if not self._client:
                self._client = anthropic.AsyncAnthropic(api_key=self.api_key)
            
            prompt = self._build_prompt(request)
            
            response = await self._client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return self._parse_response(response.content[0].text, request)
        
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}")
    
    def _build_prompt(self, request: TestGenerationRequest) -> str:
        system_context = """You are an expert software testing engineer. Generate comprehensive, 
        high-quality test cases that cover edge cases, error handling, and normal operations."""
        
        prompt = f"""{system_context}

Generate test cases for this {request.language} code using {request.test_framework}:

```{request.language}
{request.source_code}
```
"""
        
        if request.function_name:
            prompt += f"Focus on function: {request.function_name}\n"
        
        if request.class_name:
            prompt += f"Focus on class: {request.class_name}\n"
        
        if request.additional_context:
            prompt += f"Context: {request.additional_context}\n"
        
        prompt += """
Return JSON format:
{
    "tests": [
        {
            "test_name": "test_name",
            "description": "test description",
            "test_code": "complete test code",
            "coverage_areas": ["area1", "area2"],
            "confidence_score": 0.9
        }
    ]
}"""
        
        return prompt
    
    def _parse_response(self, response: str, request: TestGenerationRequest) -> List[GeneratedTest]:
        """Parse AI response into GeneratedTest objects."""
        # Reuse the same parsing logic as OpenAI
        return OpenAIProvider._parse_response(self, response, request)


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