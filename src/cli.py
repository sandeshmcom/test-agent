"""Command-line interface for the AI Test Agent."""

import asyncio
import click
import json
import os
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax

from .core.test_agent import TestAgent
from .core.ai_provider import TestType, TestPriority


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AI Test Agent - Generate comprehensive manual test cases from requirements."""
    pass


@cli.command()
@click.option('--feature', '-f', required=True, help='Feature description')
@click.option('--requirements', '-r', multiple=True, required=True, help='Requirements (can be specified multiple times)')
@click.option('--user-stories', '-u', multiple=True, help='User stories (can be specified multiple times)')
@click.option('--acceptance-criteria', '-a', multiple=True, help='Acceptance criteria (can be specified multiple times)')
@click.option('--app-type', default='web', type=click.Choice(['web', 'mobile', 'desktop', 'api']), help='Application type')
@click.option('--target-audience', help='Target audience description')
@click.option('--business-context', help='Business context')
@click.option('--existing-functionality', help='Description of existing functionality')
@click.option('--integration-points', multiple=True, help='Integration points (can be specified multiple times)')
@click.option('--test-types', multiple=True, 
              type=click.Choice(['Functional', 'UI/UX', 'Integration', 'Performance', 'Security', 'Usability', 'Compatibility', 'Regression']),
              help='Specific test types to focus on')
@click.option('--provider', default='auto', type=click.Choice(['auto', 'openai', 'anthropic']), help='AI provider to use')
@click.option('--output-format', '-o', default='markdown', type=click.Choice(['json', 'csv', 'markdown', 'html']), help='Output format')
@click.option('--output-file', help='Output file path')
@click.option('--show-summary/--no-summary', default=True, help='Show test case summary')
def generate(feature, requirements, user_stories, acceptance_criteria, app_type, 
            target_audience, business_context, existing_functionality, 
            integration_points, test_types, provider, output_format, output_file, show_summary):
    """Generate manual test cases from feature requirements."""
    
    asyncio.run(_generate_async(
        feature, requirements, user_stories, acceptance_criteria, app_type,
        target_audience, business_context, existing_functionality,
        integration_points, test_types, provider, output_format, output_file, show_summary
    ))


async def _generate_async(feature, requirements, user_stories, acceptance_criteria, app_type,
                         target_audience, business_context, existing_functionality,
                         integration_points, test_types, provider, output_format, output_file, show_summary):
    """Async implementation of test case generation."""
    
    try:
        # Initialize the test agent
        console.print(f"[blue]Initializing AI Test Agent with provider: {provider}[/blue]")
        agent = TestAgent(provider_name=provider)
        console.print(f"[green]✓ Using {agent.provider_name} provider[/green]")
        
        # Prepare parameters
        requirements_list = list(requirements) if requirements else []
        user_stories_list = list(user_stories) if user_stories else None
        acceptance_criteria_list = list(acceptance_criteria) if acceptance_criteria else None
        integration_points_list = list(integration_points) if integration_points else None
        test_types_list = list(test_types) if test_types else None
        
        # Generate test cases with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating test cases...", total=None)
            
            test_cases = await agent.generate_test_cases(
                feature_description=feature,
                requirements=requirements_list,
                user_stories=user_stories_list,
                acceptance_criteria=acceptance_criteria_list,
                application_type=app_type,
                target_audience=target_audience,
                business_context=business_context,
                existing_functionality=existing_functionality,
                integration_points=integration_points_list,
                test_types_requested=test_types_list
            )
            
            progress.update(task, completed=100)
        
        console.print(f"[green]✓ Generated {len(test_cases)} test cases[/green]")
        
        # Show summary if requested
        if show_summary:
            _display_summary(agent, test_cases)
        
        # Export test cases
        if output_file or output_format != 'markdown':
            output = agent.export_test_cases(test_cases, output_format, output_file)
            if not output_file:
                console.print(Panel(output, title=f"Test Cases ({output_format.upper()})"))
        else:
            # Display in console for markdown
            _display_test_cases(test_cases)
    
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()


def _display_summary(agent: TestAgent, test_cases):
    """Display test case summary in a nice table."""
    summary = agent.get_test_summary(test_cases)
    
    if summary["total"] == 0:
        console.print("[yellow]No test cases generated[/yellow]")
        return
    
    # Create summary table
    table = Table(title="Test Case Summary", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Test Cases", str(summary["total"]))
    table.add_row("Estimated Time", summary["estimated_total_time"])
    
    # Add type breakdown
    if "by_type" in summary:
        table.add_row("", "")  # Spacer
        table.add_row("By Type", "Count", style="bold")
        for test_type, count in summary["by_type"].items():
            table.add_row(f"  {test_type}", str(count))
    
    # Add priority breakdown
    if "by_priority" in summary:
        table.add_row("", "")  # Spacer
        table.add_row("By Priority", "Count", style="bold")
        for priority, count in summary["by_priority"].items():
            table.add_row(f"  {priority}", str(count))
    
    console.print(table)
    console.print()


def _display_test_cases(test_cases):
    """Display test cases in a formatted way."""
    for tc in test_cases:
        # Create test case panel
        content = []
        content.append(f"[bold]Description:[/bold] {tc.description}")
        content.append(f"[bold]Type:[/bold] {tc.test_type.value} | [bold]Priority:[/bold] {tc.priority.value} | [bold]Time:[/bold] {tc.estimated_time}")
        
        if tc.preconditions:
            content.append(f"\n[bold]Preconditions:[/bold]")
            for precond in tc.preconditions:
                content.append(f"  • {precond}")
        
        content.append(f"\n[bold]Test Steps:[/bold]")
        for step in tc.test_steps:
            content.append(f"  {step.step_number}. [blue]{step.action}[/blue]")
            content.append(f"     [green]Expected: {step.expected_result}[/green]")
            if step.notes:
                content.append(f"     [italic]Notes: {step.notes}[/italic]")
        
        content.append(f"\n[bold]Expected Outcome:[/bold] {tc.expected_outcome}")
        
        if tc.tags:
            content.append(f"[bold]Tags:[/bold] {', '.join(tc.tags)}")
        
        if tc.requirements_covered:
            content.append(f"[bold]Requirements:[/bold] {', '.join(tc.requirements_covered)}")
        
        panel_content = "\n".join(content)
        
        # Color-code by priority
        border_style = {
            "Critical": "red",
            "High": "yellow", 
            "Medium": "blue",
            "Low": "green"
        }.get(tc.priority.value, "white")
        
        console.print(Panel(
            panel_content,
            title=f"{tc.test_id}: {tc.title}",
            border_style=border_style
        ))
        console.print()


@cli.command()
@click.option('--input-file', '-i', required=True, help='Input requirements file (JSON or YAML)')
@click.option('--provider', default='auto', type=click.Choice(['auto', 'openai', 'anthropic']), help='AI provider to use')
@click.option('--output-format', '-o', default='markdown', type=click.Choice(['json', 'csv', 'markdown', 'html']), help='Output format')
@click.option('--output-file', help='Output file path')
def generate_from_file(input_file, provider, output_format, output_file):
    """Generate test cases from a requirements file."""
    
    asyncio.run(_generate_from_file_async(input_file, provider, output_format, output_file))


async def _generate_from_file_async(input_file, provider, output_format, output_file):
    """Async implementation of file-based generation."""
    
    try:
        # Read requirements file
        console.print(f"[blue]Reading requirements from {input_file}[/blue]")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            if input_file.endswith('.json'):
                data = json.load(f)
            elif input_file.endswith('.yaml') or input_file.endswith('.yml'):
                import yaml
                data = yaml.safe_load(f)
            else:
                raise click.ClickException("Input file must be JSON or YAML")
        
        # Validate required fields
        if 'feature_description' not in data:
            raise click.ClickException("Input file must contain 'feature_description'")
        if 'requirements' not in data:
            raise click.ClickException("Input file must contain 'requirements'")
        
        # Initialize the test agent
        agent = TestAgent(provider_name=provider)
        console.print(f"[green]✓ Using {agent.provider_name} provider[/green]")
        
        # Generate test cases
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating test cases...", total=None)
            
            test_cases = await agent.generate_test_cases(
                feature_description=data['feature_description'],
                requirements=data['requirements'],
                user_stories=data.get('user_stories'),
                acceptance_criteria=data.get('acceptance_criteria'),
                application_type=data.get('application_type', 'web'),
                target_audience=data.get('target_audience'),
                business_context=data.get('business_context'),
                existing_functionality=data.get('existing_functionality'),
                integration_points=data.get('integration_points'),
                test_types_requested=data.get('test_types_requested')
            )
            
            progress.update(task, completed=100)
        
        console.print(f"[green]✓ Generated {len(test_cases)} test cases[/green]")
        
        # Display summary
        _display_summary(agent, test_cases)
        
        # Export test cases
        if output_file or output_format != 'markdown':
            output = agent.export_test_cases(test_cases, output_format, output_file)
            if not output_file:
                console.print(Panel(output, title=f"Test Cases ({output_format.upper()})"))
        else:
            _display_test_cases(test_cases)
    
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()


@cli.command()
def list_providers():
    """List available AI providers and their status."""
    
    from .core.ai_provider import get_available_providers
    
    providers = get_available_providers()
    
    table = Table(title="Available AI Providers", show_header=True, header_style="bold magenta")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Configuration", style="yellow")
    
    # Check OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if "openai" in providers:
        table.add_row("OpenAI", "✓ Available", "OPENAI_API_KEY configured")
    else:
        table.add_row("OpenAI", "✗ Not available", "OPENAI_API_KEY not set")
    
    # Check Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if "anthropic" in providers:
        table.add_row("Anthropic", "✓ Available", "ANTHROPIC_API_KEY configured")
    else:
        table.add_row("Anthropic", "✗ Not available", "ANTHROPIC_API_KEY not set")
    
    console.print(table)
    
    if not providers:
        console.print("\n[red]No providers available. Please configure at least one AI provider:[/red]")
        console.print("  • Set OPENAI_API_KEY environment variable for OpenAI")
        console.print("  • Set ANTHROPIC_API_KEY environment variable for Anthropic")


@cli.command()
def create_template():
    """Create a template requirements file."""
    
    template = {
        "feature_description": "Description of the feature to test",
        "requirements": [
            "REQ-001: Functional requirement 1",
            "REQ-002: Functional requirement 2"
        ],
        "user_stories": [
            "As a user, I want to...",
            "As an admin, I need to..."
        ],
        "acceptance_criteria": [
            "Given... When... Then...",
            "The system should..."
        ],
        "application_type": "web",
        "target_audience": "End users, administrators",
        "business_context": "Context about the business domain",
        "existing_functionality": "Description of related existing features",
        "integration_points": [
            "External API X",
            "Database Y"
        ],
        "test_types_requested": [
            "Functional",
            "UI/UX",
            "Integration"
        ]
    }
    
    filename = "requirements_template.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2)
    
    console.print(f"[green]✓ Created template file: {filename}[/green]")
    console.print("Edit this file with your requirements and use:")
    console.print(f"[cyan]test-agent generate-from-file -i {filename}[/cyan]")


if __name__ == '__main__':
    cli()