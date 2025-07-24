#!/usr/bin/env python3
"""
Demo script showing how to use the AI Test Agent programmatically.

This example demonstrates:
1. Initializing the test agent
2. Generating test cases
3. Exporting to different formats
4. Getting summary statistics
"""

import asyncio
import os
import sys

# Add the src directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.test_agent import TestAgent
from src.core.ai_provider import TestType


async def main():
    """Main demo function."""
    
    print("🤖 AI Test Agent Demo")
    print("=" * 50)
    
    try:
        # Initialize the test agent
        print("Initializing test agent...")
        agent = TestAgent(provider_name="auto")
        print(f"✓ Using {agent.provider_name} provider")
        
        # Example 1: Simple login feature
        print("\n📝 Generating test cases for user login feature...")
        
        test_cases = await agent.generate_test_cases(
            feature_description="User authentication system with email and password",
            requirements=[
                "Users must be able to log in with valid email and password",
                "System should validate credentials against user database",
                "Failed login attempts should be logged for security",
                "Users should be redirected to dashboard after successful login",
                "Account should be locked after 5 failed attempts"
            ],
            user_stories=[
                "As a registered user, I want to log in to access my account",
                "As a security admin, I want failed attempts logged for monitoring"
            ],
            acceptance_criteria=[
                "Given valid credentials, when user logs in, then they access dashboard",
                "Given invalid credentials, when user tries to log in, then error message is shown",
                "Given 5 failed attempts, when user tries again, then account is locked"
            ],
            application_type="web",
            target_audience="End users and administrators",
            business_context="E-commerce platform requiring secure user authentication",
            test_types_requested=["Functional", "Security", "Usability"]
        )
        
        print(f"✓ Generated {len(test_cases)} test cases")
        
        # Display summary
        print("\n📊 Test Case Summary:")
        summary = agent.get_test_summary(test_cases)
        print(f"  Total test cases: {summary['total']}")
        print(f"  Estimated time: {summary['estimated_total_time']}")
        
        print("\n  By type:")
        for test_type, count in summary['by_type'].items():
            print(f"    - {test_type}: {count}")
        
        print("\n  By priority:")
        for priority, count in summary['by_priority'].items():
            print(f"    - {priority}: {count}")
        
        # Export to different formats
        print("\n📤 Exporting test cases...")
        
        # Export to Markdown
        markdown_output = agent.export_test_cases(test_cases, "markdown", "demo_test_cases.md")
        print("✓ Exported to demo_test_cases.md")
        
        # Export to HTML
        html_output = agent.export_test_cases(test_cases, "html", "demo_test_cases.html")
        print("✓ Exported to demo_test_cases.html")
        
        # Export to JSON
        json_output = agent.export_test_cases(test_cases, "json", "demo_test_cases.json")
        print("✓ Exported to demo_test_cases.json")
        
        # Export to CSV
        csv_output = agent.export_test_cases(test_cases, "csv", "demo_test_cases.csv")
        print("✓ Exported to demo_test_cases.csv")
        
        # Display a sample test case
        if test_cases:
            print("\n📋 Sample Test Case:")
            print("-" * 30)
            tc = test_cases[0]
            print(f"ID: {tc.test_id}")
            print(f"Title: {tc.title}")
            print(f"Description: {tc.description}")
            print(f"Type: {tc.test_type.value}")
            print(f"Priority: {tc.priority.value}")
            print(f"Steps: {len(tc.test_steps)} steps")
            print(f"Estimated time: {tc.estimated_time}")
        
        print("\n🎉 Demo completed successfully!")
        print("Check the generated files in the current directory.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure you have set up your API keys:")
        print("  export OPENAI_API_KEY='your-key'")
        print("  or")
        print("  export ANTHROPIC_API_KEY='your-key'")


if __name__ == "__main__":
    asyncio.run(main())