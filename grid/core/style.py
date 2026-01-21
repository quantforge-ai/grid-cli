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
    """Runs the package-style loading animation."""
    console.clear()
    
    # 1. Display Colorful ASCII Header
    console.print()
    console.print(Align.center(Text("   ██████╗ ██████╗ ██╗██████╗     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     ", style="bold cyan")))
    console.print(Align.center(Text("  ██╔════╝ ██╔══██╗██║██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ", style="bold blue")))
    console.print(Align.center(Text("  ██║  ███╗██████╔╝██║██║  ██║       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ", style="bold magenta")))
    console.print(Align.center(Text("  ██║   ██║██╔══██╗██║██║  ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ", style="bold red")))
    console.print(Align.center(Text("  ╚██████╔╝██║  ██║██║██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗", style="bold yellow")))
    console.print(Align.center(Text("   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝", style="bold green")))
    console.print()
    console.print(Align.center(Text("⚡ NEURAL LINK INITIALIZATION ⚡", style="bold yellow")))
    console.print(Align.center(Text("v1.0.0", style="dim cyan")))
    print()

    # 2. The Loading Bar with colorful steps
    steps = [
        ("Resolving dependencies...", "cyan"),
        ("Loading neural_core.pkg...", "blue"),
        ("Mounting git_filesystem...", "magenta"),
        ("Injecting sarcasm_module.dll...", "yellow"),
        ("Establishing uplink...", "green")
    ]

    with Progress(
        SpinnerColumn(spinner_name="dots12", style="bold magenta"),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=40, style="yellow", complete_style="bold cyan"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:
        
        main_task = progress.add_task("[white]System Boot", total=100)
        
        for i in range(100):
            sleep_time = 0.02 if i < 80 else 0.005
            time.sleep(sleep_time)
            
            step_index = min(len(steps)-1, int(i / 20))
            desc, color = steps[step_index]
            progress.update(main_task, advance=1, description=f"[{color}]{desc}[/{color}]")

    # 3. Final Flash
    console.print(Align.center(Text(">> SYSTEM READY <<", style="bold green")))
    console.print(Align.center(Text("━" * 50, style="cyan")))
    time.sleep(0.5)
    console.clear()

def print_header():
    """The Persistent Header with vibrant colors."""
    console.print()
    console.print(Text("   ██████╗ ██████╗ ██╗██████╗ ", style="bold cyan"), end="")
    console.print(Text("    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     ", style="bold magenta"))
    
    console.print(Text("  ██╔════╝ ██╔══██╗██║██╔══██╗", style="bold cyan"), end="")
    console.print(Text("    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ", style="bold magenta"))
    
    console.print(Text("  ██║  ███╗██████╔╝██║██║  ██║", style="bold cyan"), end="")
    console.print(Text("       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ", style="bold magenta"))
    
    console.print(Text("  ██║   ██║██╔══██╗██║██║  ██║", style="bold cyan"), end="")
    console.print(Text("       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ", style="bold magenta"))
    
    console.print(Text("  ╚██████╔╝██║  ██║██║██████╔╝", style="bold cyan"), end="")
    console.print(Text("       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗", style="bold magenta"))
    
    console.print(Text("   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ ", style="bold cyan"), end="")
    console.print(Text("       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝", style="bold magenta"))
    
    console.print()
    console.print(Text("        The Sentient Developer Companion", style="italic yellow"), justify="center")
    console.print(Text("        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", style="dim cyan"), justify="center")
    print()

def print_dashboard():
    """The Command Menu - Clean without borders."""
    # Create a simple table without any box borders
    table = Table(show_header=True, box=None, expand=False, padding=(0, 3), show_edge=False)
    
    table.add_column("⚡ COMMAND", style="bold cyan", no_wrap=True)
    table.add_column("DESCRIPTION", style="bold white")
    
    rows = [
        ("grid push", "[yellow]Safe Push / Cowboy Mode[/]"),
        ("grid roast", "[magenta]Audit Code Quality[/]"),
        ("grid rank", "[blue]View Leaderboard[/]"),
        ("grid status", "[green]System Diagnostics[/]"),
        ("exit", "[red]Disconnect[/]")
    ]
    
    for cmd, desc in rows:
        table.add_row(cmd, desc)
    
    # Print header manually with custom styling
    console.print()
    console.print(Text("  ⚡ AVAILABLE PROTOCOLS", style="bold yellow"))
    console.print(Text("  " + "─" * 60, style="dim cyan"))
    console.print(table)
    console.print(Text("  " + "─" * 60, style="dim cyan"))
    console.print()
