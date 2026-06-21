from rich.table import Table
from rich.console import Console

console = Console()


def show(results: list[dict], clean: bool = False):
    """Return results table."""
    table = Table(title="PromptBench Results")
    
    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("Status", style="white")
    table.add_column("Latency", style="yellow")
    table.add_column("Tokens", style="magenta")
    table.add_column("Valid JSON", style="white")
    table.add_column("Tool", style="green")

    for r in results:
        status_style = "green" if r["status"] == "ok" else "red"
        json_style = "green" if r["valid_json"] == "YES" else "red"
        
        table.add_row(
            r["model"],
            f"[{status_style}]{r['status'].upper()}[/{status_style}]",
            r["latency"],
            str(r["tokens"]),
            f"[{json_style}]{r['valid_json']}[/{json_style}]",
            r.get("tool", "N/A")
        )

    console.print(table)
    
    # if errors
    if not clean:
        for r in results:
            if r["status"] == "error":
                console.print(f"[red]Error ({r['model']}):[/red] {r.get('error', 'unknown')}")