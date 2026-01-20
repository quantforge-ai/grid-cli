"""
Grid CLI - Project Discovery
"""

import os
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def scan_targets():
    """Scan the local filesystem (or external registry) for assimilated projects."""
    console.print("[bold magenta]📡 SCANNING SURVEILLANCE FEED...[/bold magenta]\n")
    
    targets = []
    # Simple parent dir scan for demo purposes
    parent = Path(os.getcwd()).parent
    for d in parent.iterdir():
        if d.is_dir() and (d / "config.grid").exists():
            targets.append(d.name)
            
    if not targets:
        console.print(" • [cyan]No active targets in this sector.[/cyan]")
    else:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Assimilated Project")
        for t in targets:
            table.add_row(t)
        console.print(table)
