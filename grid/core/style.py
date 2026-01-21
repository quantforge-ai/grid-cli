"""
Grid CLI Visual Style Module
Handles boot sequences, headers, and dashboard displays
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import time

console = Console()

def boot_sequence():
    """Displays a cool boot sequence animation"""
    messages = [
        "[dim cyan]◆ Initializing Neural Core...[/]",
        "[dim cyan]◆ Loading Git Protocol...[/]",
        "[dim cyan]◆ Syncing Cloud Brain...[/]",
        "[bold green]◆ Systems Online[/]",
    ]
    
    for msg in messages:
        console.print(msg)
        time.sleep(0.15)
    
    console.print()

def print_header():
    """Prints the Grid CLI header"""
    header = Text()
    header.append("╔═══════════════════════════════════════╗\n", style="bold cyan")
    header.append("║                                       ║\n", style="bold cyan")
    header.append("║         ", style="bold cyan")
    header.append("G R I D   C L I", style="bold white")
    header.append("           ║\n", style="bold cyan")
    header.append("║    ", style="bold cyan")
    header.append("The Sentient Developer Companion", style="dim white")
    header.append("   ║\n", style="bold cyan")
    header.append("║                                       ║\n", style="bold cyan")
    header.append("╚═══════════════════════════════════════╝", style="bold cyan")
    
    console.print(header)

def print_dashboard():
    """Prints a status dashboard"""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="dim cyan", justify="right")
    table.add_column(style="bold white")
    
    table.add_row("Status:", "[bold green]ONLINE[/]")
    table.add_row("Mode:", "[bold yellow]INTERACTIVE TERMINAL[/]")
    table.add_row("Commands:", "[dim]Type 'exit' to quit, 'clear' to refresh[/]")
    
    console.print(table)
