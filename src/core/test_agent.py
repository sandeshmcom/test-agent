"""Main Test Agent for generating manual test cases."""

import asyncio
from typing import List, Optional, Dict, Any
from dataclasses import asdict
import json
import os
from datetime import datetime

from .ai_provider import (
    AIProvider, TestCaseGenerationRequest, ManualTestCase, 
    TestType, TestPriority, get_available_providers
)


class TestAgent:
    """AI-powered manual test case generation agent."""
    
    def __init__(self, provider_name: str = "auto"):
        """Initialize the test agent with specified AI provider."""
        self.providers = get_available_providers()
        
        if provider_name == "auto":
            # Use first available provider
            if not self.providers:
                raise RuntimeError("No AI providers configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")
            self.provider = next(iter(self.providers.values()))
            self.provider_name = next(iter(self.providers.keys()))
        else:
            if provider_name not in self.providers:
                available = list(self.providers.keys())
                raise ValueError(f"Provider '{provider_name}' not available. Available: {available}")
            self.provider = self.providers[provider_name]
            self.provider_name = provider_name
    
    async def generate_test_cases(
        self,
        feature_description: str,
        requirements: List[str],
        user_stories: Optional[List[str]] = None,
        acceptance_criteria: Optional[List[str]] = None,
        application_type: str = "web",
        target_audience: Optional[str] = None,
        business_context: Optional[str] = None,
        existing_functionality: Optional[str] = None,
        integration_points: Optional[List[str]] = None,
        test_types_requested: Optional[List[str]] = None
    ) -> List[ManualTestCase]:
        """Generate manual test cases based on provided requirements."""
        
        # Convert string test types to enums
        test_type_enums = None
        if test_types_requested:
            test_type_enums = []
            for test_type_str in test_types_requested:
                try:
                    test_type_enums.append(TestType(test_type_str))
                except ValueError:
                    print(f"Warning: Unknown test type '{test_type_str}', ignoring")
        
        request = TestCaseGenerationRequest(
            feature_description=feature_description,
            requirements=requirements,
            user_stories=user_stories,
            acceptance_criteria=acceptance_criteria,
            application_type=application_type,
            target_audience=target_audience,
            business_context=business_context,
            existing_functionality=existing_functionality,
            integration_points=integration_points,
            test_types_requested=test_type_enums
        )
        
        test_cases = await self.provider.generate_manual_tests(request)
        return test_cases
    
    def export_test_cases(
        self, 
        test_cases: List[ManualTestCase], 
        output_format: str = "json",
        output_file: Optional[str] = None
    ) -> str:
        """Export test cases to various formats."""
        
        if output_format.lower() == "json":
            output = self._export_to_json(test_cases)
        elif output_format.lower() == "csv":
            output = self._export_to_csv(test_cases)
        elif output_format.lower() == "markdown":
            output = self._export_to_markdown(test_cases)
        elif output_format.lower() == "html":
            output = self._export_to_html(test_cases)
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Test cases exported to {output_file}")
        
        return output
    
    def _export_to_json(self, test_cases: List[ManualTestCase]) -> str:
        """Export test cases to JSON format."""
        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "provider": self.provider_name,
                "total_test_cases": len(test_cases)
            },
            "test_cases": [self._test_case_to_dict(tc) for tc in test_cases]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _export_to_csv(self, test_cases: List[ManualTestCase]) -> str:
        """Export test cases to CSV format."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'Test ID', 'Title', 'Description', 'Type', 'Priority', 
            'Estimated Time', 'Preconditions', 'Test Steps', 
            'Expected Outcome', 'Tags', 'Requirements Covered'
        ])
        
        # Data rows
        for tc in test_cases:
            preconditions = '; '.join(tc.preconditions)
            test_steps = '; '.join([f"{step.step_number}. {step.action} -> {step.expected_result}" 
                                  for step in tc.test_steps])
            tags = ', '.join(tc.tags)
            requirements = ', '.join(tc.requirements_covered)
            
            writer.writerow([
                tc.test_id, tc.title, tc.description, tc.test_type.value,
                tc.priority.value, tc.estimated_time, preconditions,
                test_steps, tc.expected_outcome, tags, requirements
            ])
        
        return output.getvalue()
    
    def _export_to_markdown(self, test_cases: List[ManualTestCase]) -> str:
        """Export test cases to Markdown format."""
        output = ["# Manual Test Cases", ""]
        output.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"**Provider:** {self.provider_name}")
        output.append(f"**Total Test Cases:** {len(test_cases)}")
        output.append("")
        
        for tc in test_cases:
            output.append(f"## {tc.test_id}: {tc.title}")
            output.append("")
            output.append(f"**Description:** {tc.description}")
            output.append(f"**Type:** {tc.test_type.value}")
            output.append(f"**Priority:** {tc.priority.value}")
            output.append(f"**Estimated Time:** {tc.estimated_time}")
            
            if tc.preconditions:
                output.append("**Preconditions:**")
                for precond in tc.preconditions:
                    output.append(f"- {precond}")
            
            output.append("**Test Steps:**")
            for step in tc.test_steps:
                output.append(f"{step.step_number}. **Action:** {step.action}")
                output.append(f"   **Expected Result:** {step.expected_result}")
                if step.notes:
                    output.append(f"   **Notes:** {step.notes}")
            
            output.append(f"**Expected Outcome:** {tc.expected_outcome}")
            
            if tc.tags:
                output.append(f"**Tags:** {', '.join(tc.tags)}")
            
            if tc.requirements_covered:
                output.append(f"**Requirements Covered:** {', '.join(tc.requirements_covered)}")
            
            output.append("---")
            output.append("")
        
        return "\n".join(output)
    
    def _export_to_html(self, test_cases: List[ManualTestCase]) -> str:
        """Export test cases to HTML format."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Manual Test Cases</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .test-case {{ border: 1px solid #ddd; margin: 20px 0; padding: 20px; border-radius: 5px; }}
        .test-header {{ background-color: #f5f5f5; padding: 10px; margin: -20px -20px 20px -20px; border-radius: 5px 5px 0 0; }}
        .priority-critical {{ border-left: 5px solid #dc3545; }}
        .priority-high {{ border-left: 5px solid #fd7e14; }}
        .priority-medium {{ border-left: 5px solid #ffc107; }}
        .priority-low {{ border-left: 5px solid #28a745; }}
        .test-steps {{ margin: 15px 0; }}
        .test-step {{ margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-radius: 3px; }}
        .tags {{ margin: 10px 0; }}
        .tag {{ display: inline-block; background-color: #007bff; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin: 2px; }}
    </style>
</head>
<body>
    <h1>Manual Test Cases</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Provider:</strong> {self.provider_name}</p>
    <p><strong>Total Test Cases:</strong> {len(test_cases)}</p>
"""
        
        for tc in test_cases:
            priority_class = f"priority-{tc.priority.value.lower()}"
            html += f"""
    <div class="test-case {priority_class}">
        <div class="test-header">
            <h2>{tc.test_id}: {tc.title}</h2>
            <p><strong>Type:</strong> {tc.test_type.value} | <strong>Priority:</strong> {tc.priority.value} | <strong>Time:</strong> {tc.estimated_time}</p>
        </div>
        
        <p><strong>Description:</strong> {tc.description}</p>
        
        {f'<p><strong>Preconditions:</strong></p><ul>{"".join([f"<li>{p}</li>" for p in tc.preconditions])}</ul>' if tc.preconditions else ''}
        
        <div class="test-steps">
            <p><strong>Test Steps:</strong></p>
            {"".join([f'<div class="test-step"><strong>Step {step.step_number}:</strong> {step.action}<br><strong>Expected:</strong> {step.expected_result}{f"<br><strong>Notes:</strong> {step.notes}" if step.notes else ""}</div>' for step in tc.test_steps])}
        </div>
        
        <p><strong>Expected Outcome:</strong> {tc.expected_outcome}</p>
        
        {f'<div class="tags">{"".join([f\'<span class="tag">{tag}</span>\' for tag in tc.tags])}</div>' if tc.tags else ''}
        
        {f'<p><strong>Requirements:</strong> {", ".join(tc.requirements_covered)}</p>' if tc.requirements_covered else ''}
    </div>
"""
        
        html += """
</body>
</html>"""
        return html
    
    def _test_case_to_dict(self, test_case: ManualTestCase) -> Dict[str, Any]:
        """Convert ManualTestCase to dictionary for JSON serialization."""
        data = asdict(test_case)
        # Convert enums to their values
        data['test_type'] = test_case.test_type.value
        data['priority'] = test_case.priority.value
        return data
    
    def get_test_summary(self, test_cases: List[ManualTestCase]) -> Dict[str, Any]:
        """Get summary statistics of generated test cases."""
        if not test_cases:
            return {"total": 0}
        
        # Count by type
        type_counts = {}
        for tc in test_cases:
            type_counts[tc.test_type.value] = type_counts.get(tc.test_type.value, 0) + 1
        
        # Count by priority
        priority_counts = {}
        for tc in test_cases:
            priority_counts[tc.priority.value] = priority_counts.get(tc.priority.value, 0) + 1
        
        # Estimate total time
        total_minutes = 0
        for tc in test_cases:
            time_str = tc.estimated_time.lower()
            if 'minute' in time_str:
                try:
                    minutes = int(time_str.split()[0])
                    total_minutes += minutes
                except (ValueError, IndexError):
                    total_minutes += 5  # Default estimate
        
        return {
            "total": len(test_cases),
            "by_type": type_counts,
            "by_priority": priority_counts,
            "estimated_total_time": f"{total_minutes} minutes ({total_minutes/60:.1f} hours)"
        }