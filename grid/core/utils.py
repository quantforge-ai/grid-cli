from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_header(text):
    console.print(f"[bold cyan]>> {text}[/]")

def print_success(text):
    console.print(f"[bold green]✔️ {text}[/]")

def print_error(text):
    console.print(f"[bold red]❌ {text}[/]")

def print_warning(text):
    console.print(f"[bold yellow]⚠️ {text}[/]")

def print_dashboard(metrics):
    """
    Renders the 'grid status' table.
    metrics = {"Branch": "main", "Neural Link": "Online"}
    """
    content = ""
    for key, value in metrics.items():
        content += f"[bold blue]{key}:[/] {value}\n"
    
    console.print(Panel.fit(content.strip(), title="[bold magenta]GRID DIAGNOSTICS[/]", border_style="cyan"))

def spin_action(text, func):
    """
    Runs a function with a loading spinner.
    """
    with console.status(f"[bold green]{text}...[/]", spinner="dots"):
        return func()
        