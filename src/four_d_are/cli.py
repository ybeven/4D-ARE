"""
4D-ARE Command Line Interface

Usage:
    four-d-are analyze "Why is retention declining?"
    four-d-are demo
    four-d-are mcp start --type mysql
"""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

app = typer.Typer(
    name="four-d-are",
    help="Attribution-Driven Agent Requirements Engineering for LLMs",
    no_args_is_help=True,
)
console = Console()


@app.command()
def analyze(
    query: str = typer.Argument(..., help="The question to analyze"),
    data_file: Optional[Path] = typer.Option(
        None, "--data", "-d", help="Path to JSON file with data context"
    ),
    template: str = typer.Option(
        "banking", "--template", "-t", help="Domain template: banking, healthcare, ecommerce"
    ),
):
    """
    Analyze a question using the 4D-ARE framework.

    Example:
        four-d-are analyze "Why is customer retention declining?"
    """
    from four_d_are import AttributionAgent, DataContext
    from four_d_are.prompts import BANKING_TEMPLATE, HEALTHCARE_TEMPLATE, ECOMMERCE_TEMPLATE

    # Load data context
    if data_file and data_file.exists():
        with open(data_file) as f:
            data = json.load(f)
        data_context = DataContext.from_dict(data)
    else:
        # Use demo data
        data_context = DataContext(
            results={"retention_rate": 0.56, "target": 0.80, "customer_satisfaction": 0.72},
            process={"visit_frequency": 2.1, "cross_sell_rate": 0.28, "quality_score": 0.82},
            support={"staffing_ratio": 0.68, "training_completion": 0.91},
            longterm={"market_trend": "declining", "competitor_entries": 3},
        )
        console.print("[dim]Using demo data context. Use --data to provide your own.[/dim]\n")

    # Select template
    templates = {
        "banking": BANKING_TEMPLATE,
        "healthcare": HEALTHCARE_TEMPLATE,
        "ecommerce": ECOMMERCE_TEMPLATE,
    }
    domain_template = templates.get(template.lower(), BANKING_TEMPLATE)

    # Run analysis
    console.print(Panel(f"[bold]Query:[/bold] {query}", title="4D-ARE Analysis"))
    console.print()

    with console.status("[bold blue]Analyzing with 4D-ARE framework..."):
        agent = AttributionAgent(template=domain_template)
        response = agent.analyze(query=query, data_context=data_context)

    console.print(Panel(Markdown(response), title="Analysis Result"))


@app.command()
def demo():
    """
    Run a quick demo of 4D-ARE with sample data.
    """
    console.print("\n[bold blue]4D-ARE Demo[/bold blue]\n")
    console.print("This demo shows how 4D-ARE traces causal chains through 4 dimensions.\n")

    # Demo data
    demo_data = {
        "results": {"retention_rate": 0.56, "target": 0.80},
        "process": {"visit_frequency": 2.1, "cross_sell_rate": 0.28},
        "support": {"staffing_ratio": 0.68},
        "longterm": {"market_trend": "declining", "competitor_entries": 3},
    }

    console.print("[bold]Demo Data Context:[/bold]")
    console.print_json(data=demo_data)
    console.print()

    query = "Why is customer retention rate only 56% when our target is 80%?"
    console.print(f"[bold]Query:[/bold] {query}\n")

    # Check if API key is configured
    try:
        from four_d_are.config import get_settings
        settings = get_settings()
        _ = settings.openai_api_key.get_secret_value()
    except Exception:
        console.print("[yellow]Note: Set OPENAI_API_KEY in .env to run actual analysis.[/yellow]")
        console.print("\nExample .env file:")
        console.print("  OPENAI_API_KEY=sk-your-key-here")
        console.print("\nTo run this demo with real analysis:")
        console.print('  four-d-are analyze "Why is retention declining?"')
        return

    # Run actual analysis
    from four_d_are import AttributionAgent, DataContext

    with console.status("[bold blue]Running 4D-ARE analysis..."):
        agent = AttributionAgent()
        data_context = DataContext.from_dict(demo_data)
        response = agent.analyze(query=query, data_context=data_context)

    console.print(Panel(Markdown(response), title="4D-ARE Analysis Result"))


@app.command()
def init(
    output_dir: Path = typer.Option(
        Path("."), "--output", "-o", help="Output directory for generated files"
    ),
):
    """
    Initialize a new 4D-ARE project with example files.
    """
    # Create directories
    (output_dir / "data").mkdir(parents=True, exist_ok=True)

    # Create example data file
    example_data = {
        "results": {
            "primary_metric": 0.62,
            "secondary_metric": 0.75,
        },
        "process": {
            "visit_frequency": 2.1,
            "cross_sell_rate": 0.28,
            "quality_score": 0.82,
        },
        "support": {
            "staffing_ratio": 0.68,
            "training_completion": 0.91,
        },
        "longterm": {
            "market_trend": "declining",
            "competitor_entries": 3,
        },
    }

    data_file = output_dir / "data" / "example_context.json"
    with open(data_file, "w") as f:
        json.dump(example_data, f, indent=2)

    # Create .env.example if it doesn't exist
    env_example = output_dir / ".env.example"
    if not env_example.exists():
        env_example.write_text("""# 4D-ARE Configuration
OPENAI_API_KEY=sk-your-key-here
# OPENAI_BASE_URL=https://api.openai.com/v1
# MODEL_AGENT=gpt-4o
""")

    console.print(f"[green]Initialized 4D-ARE project in {output_dir}[/green]")
    console.print(f"\nCreated files:")
    console.print(f"  - {data_file}")
    console.print(f"  - {env_example}")
    console.print("\nNext steps:")
    console.print("  1. Copy .env.example to .env and add your API key")
    console.print("  2. Edit data/example_context.json with your metrics")
    console.print('  3. Run: four-d-are analyze "Your question" --data data/example_context.json')


# MCP subcommand group
mcp_app = typer.Typer(help="MCP server management")
app.add_typer(mcp_app, name="mcp")


@mcp_app.command("start")
def mcp_start(
    server_type: str = typer.Option(
        "demo", "--type", "-t", help="Server type: demo, mysql, postgres, excel"
    ),
    port: int = typer.Option(8000, "--port", "-p", help="Port to run the server on"),
):
    """
    Start an MCP server for data access.
    """
    console.print(f"[bold blue]Starting {server_type} MCP server on port {port}...[/bold blue]")
    console.print("\n[yellow]MCP server implementation coming soon![/yellow]")
    console.print("\nFor now, use the analyze command with --data to provide data directly.")


@mcp_app.command("list")
def mcp_list():
    """
    List available MCP server types.
    """
    servers = [
        ("demo", "Static JSON data for quick demos", "Available"),
        ("mysql", "MySQL database connection", "Coming soon"),
        ("postgres", "PostgreSQL database connection", "Coming soon"),
        ("excel", "Excel/CSV file reader", "Coming soon"),
    ]

    console.print("\n[bold]Available MCP Servers:[/bold]\n")
    for name, desc, status in servers:
        status_color = "green" if status == "Available" else "yellow"
        console.print(f"  [{status_color}]{name}[/{status_color}]: {desc} ({status})")
    console.print()


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
