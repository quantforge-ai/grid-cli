"""
Grid CLI - Help & Menu System
"""

from rich.console import Console
from rich.table import Table

console = Console()

def show_help():
    table = Table(title="[bold cyan]GRID BASH COMMANDS[/bold cyan]", show_header=True, header_style="bold magenta", border_style="dim")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    # Universal Commands
    table.add_row("dev <url>", "Neural Link: Clones repository and creates isolated .venv")
    table.add_row("init", "Assimilate: Generate config.grid and inject Grid protocols")
    table.add_row("eject", "Sever: Remove Grid configuration and decoupling from core")
    table.add_row("submit <msg>", "Inject: Safe commit with auto-branching rescue protocols")
    table.add_row("roast <file>", "Incinerate: AI-powered ruthless code analysis")
    table.add_row("undo", "Rewrite History: Soft reset the last commit (Time Jump)")
    table.add_row("targets", "Surveillance: List available Grid-compatible repositories")
    table.add_row("check <url>", "Probe: Scan remote repo for config.grid")
    table.add_row("run <task>", "Execute: Run a specialized task defined in config.grid")
    
    # Intelligence Commands (Delegated)
    table.add_row("train", "Synapse: Initiate local model training sequence")
    table.add_row("push", "Collate: Upload intelligence packet to the Hub")
    table.add_row("pull <id>", "Ingest: Download model artifacts from Collective")
    
    # Developer Utilities
    table.add_row("coin", "Binary Decision Protocol: Flip for PROCEED or ABORT")
    table.add_row("zen", "Void State: Clear terminal and enter focus mode")
    table.add_row("blame <file>", "Identify: Execute git blame with cyberpunk flair")
    
    # System Commands
    table.add_row("login", "Authenticate: Verify identity on the Community Hub")
    table.add_row("status", "Vital Signs: Show system diagnostics and memory usage")
    table.add_row("purge", "Sanitize: Incinerate cache, temp files, and dead data")
    table.add_row("exit", "Disconnect: Power down the interface")

    console.print("\n", table, "\n")
    console.print("[dim]Powered by QuantGrid Personality Engine v1.0[/dim]")
