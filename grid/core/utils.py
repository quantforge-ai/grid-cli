from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_header(text):
    console.print(f"[bold cyan]>> {text}[/]")

def print_success(text):
    console.print(f"[bold green]✔️ {text}[/]")

def print_info(text):
    console.print(f"[bold blue]ℹ️ {text}[/]")

def print_error(text):
    console.print(f"[bold red]❌ {text}[/]")

def print_warning(text):
    console.print(f"[bold yellow]⚠️ {text}[/]")

def print_dashboard(title, sections):
    """
    Renders a multi-section dashboard with headers.
    sections = {"VITAL SIGNS": {"Identity": "tanis", ...}, ...}
    """
    console.print(f"\n[bold magenta]📊 {title}[/]")
    
    for section_name, metrics in sections.items():
        content = ""
        for key, value in metrics.items():
            content += f"[bold blue]{key:<15}[/] {value}\n"
        
        console.print(Panel(content.strip(), title=f"[bold green] {section_name} [/]", border_style="cyan", padding=(0, 1)))

def spin_action(text, func):
    """
    Runs a function with a loading spinner.
    """
    with console.status(f"[bold green]{text}...[/]", spinner="dots"):
        return func()

