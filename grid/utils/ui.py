"""
Grid CLI - UI Helpers
"""

import time
from rich.console import Console
from rich.status import Status

console = Console()

def sassy_spinner(text, duration=2):
    """Run a spinner with a sassy delay."""
    with Status(f"[bold cyan]{text}[/bold cyan]", spinner="dots"):
        time.sleep(duration)

def sassy_print(text, style="white"):
    """Standardized sassy output."""
    console.print(f" • [italic {style}]{text}[/italic {style}]")
