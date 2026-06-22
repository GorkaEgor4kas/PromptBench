import typer 
import asyncio
from rich.console import Console

from promptbench.runner import run_all
from promptbench.display import show
from promptbench.config import load_llm_config, create_clients
from promptbench.prompts import PROMPTS

app = typer.Typer()
console = Console()

@app.command()
def run(
    query: str = typer.Argument(..., help="Query to send to LLMs"),
    prompt: str = typer.Option("default", "--prompt", "-p", help="Prompt name from prompts.py"),
    llm: str = typer.Option("all", "--llm", "-l", help="LLM names to use (comma-separated)"),
    times: int = typer.Option(1, "--times", "-t", help="Number of calls per LLM"),
    output: str = typer.Option(None, "--output", "-o", help="Save results to JSON file"),
    clean: bool = typer.Option(False, "--clean", "-c", help="Clean output without logs"),
):
    """Run a query through configured LLMs and compare results."""
    console.print(f"[bold]Query:[/bold] {query}")
    console.print(f"[bold]Prompt:[/bold] {prompt}")
    console.print(f"[bold]LLMs:[/bold] {llm}")
    console.print(f"[bold]Times:[/bold] {times}")

    #load and create clients
    configs = load_llm_config() 
    if not configs:
        console.print("[red]No LLMs configured. Check your .env file.[/red]")
        return

    all_clients = create_clients(configs=configs)

    if llm.lower() != "all":
        selected = [name.strip() for name in llm.split(",")]
        clients = {name: all_clients[name] for name in selected if name in all_clients}
        if not clients:
            console.print(f"[red]None of the specified LLMs found: {llm}[/red]")
            return
        
    else:
        clients = all_clients

    if prompt not in PROMPTS:
        console.print(f"[red]Prompt '{prompt}' not found. Available: {list(PROMPTS.keys())}[/red]")
        return
    prompt_text = PROMPTS[prompt]

    console.print(f"[bold]Query:[/bold] {query}")
    console.print(f"[bold]Prompt:[/bold] {prompt}")
    console.print(f"[bold]LLMs:[/bold] {', '.join(clients.keys())}")

    #runner start
    results = asyncio.run(run_all(
        clients=clients,
        prompt=prompt_text,
        query=query,
        times=times,
        ))
    
    #output
    show(results, clean=clean)

    if output:
        import json
        with open(output, "w") as f:
            json.dump(results, f, indent=2)
        console.print(f"[green]Results saved to {output}[/green]")

@app.command()
def list():
    """List configured LLMs and prompts."""
    configs = load_llm_config()
    
    console.print("[bold]Configured LLMs:[/bold]")
    if not configs:
        console.print("  [dim]No LLMs configured. Add LLM_1_NAME, LLM_1_KEY, etc. to .env[/dim]")
    for cfg in configs:
        console.print(f"  - {cfg.name} ({cfg.model})")
    
    console.print("\n[bold]Available prompts:[/bold]")
    for name in PROMPTS:
        console.print(f"  - {name}")

if __name__ == "__main__":
    app()



