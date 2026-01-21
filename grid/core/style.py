import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align
from rich import box

console = Console()

def boot_sequence():
    """Runs the loading animation with hacker green theme."""
    console.clear()
    
    # Matrix-style green ASCII header
    console.print()
    console.print(Align.center(Text("   ██████╗ ██████╗ ██╗██████╗     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     ", style="bold green")))
    console.print(Align.center(Text("  ██╔════╝ ██╔══██╗██║██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ", style="bold green")))
    console.print(Align.center(Text("  ██║  ███╗██████╔╝██║██║  ██║       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ", style="bold green")))
    console.print(Align.center(Text("  ██║   ██║██╔══██╗██║██║  ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ", style="bold green")))
    console.print(Align.center(Text("  ╚██████╔╝██║  ██║██║██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗", style="bold green")))
    console.print(Align.center(Text("   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝", style="bold green")))
    console.print()
    console.print(Align.center(Text("⚡ NEURAL LINK INITIALIZATION ⚡", style="bold cyan")))
    console.print(Align.center(Text("v1.0.0", style="dim green")))
    print()

    # Loading bar - all green theme
    steps = [
        "Resolving dependencies...",
        "Loading neural_core.pkg...",
        "Mounting git_filesystem...",
        "Injecting sarcasm_module.dll...",
        "Establishing uplink..."
    ]

    with Progress(
        SpinnerColumn(spinner_name="dots12", style="bold green"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bold cyan"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:
        
        main_task = progress.add_task("[green]System Boot", total=100)
        
        for i in range(100):
            sleep_time = 0.02 if i < 80 else 0.005
            time.sleep(sleep_time)
            
            step_index = min(len(steps)-1, int(i / 20))
            progress.update(main_task, advance=1, description=f"[green]{steps[step_index]}[/green]")

    # Final Flash
    console.print(Align.center(Text(">> SYSTEM READY <<", style="bold green")))
    console.print(Align.center(Text("━" * 50, style="cyan")))
    time.sleep(0.5)
    console.clear()

def print_header():
    """The Persistent Header - all green hacker theme."""
    console.print()
    console.print(Text("   ██████╗ ██████╗ ██╗██████╗     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     ", style="bold green"))
    console.print(Text("  ██╔════╝ ██╔══██╗██║██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ", style="bold green"))
    console.print(Text("  ██║  ███╗██████╔╝██║██║  ██║       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ", style="bold green"))
    console.print(Text("  ██║   ██║██╔══██╗██║██║  ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ", style="bold green"))
    console.print(Text("  ╚██████╔╝██║  ██║██║██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗", style="bold green"))
    console.print(Text("   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝", style="bold green"))
    
    console.print()
    console.print(Text("        The Sentient Developer Companion", style="dim cyan"))
    console.print(Text("        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", style="dim green"))
    print()

def print_dashboard():
    """The Command Menu - Simple list, hacker theme."""
    console.print()
    console.print(Text("  ⚡ AVAILABLE PROTOCOLS", style="bold cyan"))
    console.print(Text("  " + "━" * 60, style="dim green"))
    console.print()
    
    # Simple commands list - green theme
    commands = [
        ("grid push", "Safe Push / Cowboy Mode"),
        ("grid roast", "Audit Code Quality"),
        ("grid rank", "View Leaderboard"),
        ("grid status", "System Diagnostics"),
        ("exit", "Disconnect")
    ]
    
    for cmd, desc in commands:
        console.print(f"    [bold green]{cmd:<15}[/] [dim white]{desc}[/]")
    
    console.print()
    console.print(Text("  " + "━" * 60, style="dim green"))
    console.print()
