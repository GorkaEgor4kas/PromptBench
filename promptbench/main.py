import typer 
from rich.console import Console

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
    # TODO
    # call runner 


@app.command()
def list():
    """List configured LLMs and prompts."""
    # TODO

if __name__ == "__main__":
    app()



