"""
Grid CLI - Boot Sequence Animation
"""

import time
import random
from rich.console import Console
from rich.progress import track

console = Console()

LOGO = r"""
   ______     _     __   ____             __  
  / ____/____(_)___/ /  / __ )____ ______/ /_ 
 / / __/ ___/ / __  /  / __  / __ `/ ___/ __ \
/ /_/ / /  / / /_/ /  / /_/ / /_/ (__  ) / / /
\____/_/  /_/\__,_/  /_____/\__,_/____/_/ /_/ 
"""

from grid.core.personality import engine as persona

def get_random_flavor_text():
    return persona.generate("boot")

def boot_sequence():
    console.clear()
    lines = LOGO.strip().split("\n")
    
    for i, line in enumerate(lines):
        blue_val = min(255, 100 + (i * 40))
        color = f"rgb(0,{blue_val},255)"
        console.print(line, style=color, justify="center")
        time.sleep(random.uniform(0.01, 0.05))

    console.print(
        "\n[bold italic white]   /// ESTABLISHING NEURAL LINK... ///   [/bold italic white]",
        justify="center"
    )
    console.print("\n")

    steps = [
        "Mounting File System...",
        "Verifying CUDA Cores...",
        get_random_flavor_text(),
        "Handshaking with Grid Node...",
        "Allocating Memory Buffers...",
        "ACCESS GRANTED"
    ]
    
    for step in track(
        steps,
        description="[cyan]Synchronizing Synapses...[/cyan]",
        transient=True
    ):
        time.sleep(random.uniform(0.1, 0.4))

    console.clear()
    console.print("[dim]Grid CLI v1.0 | Universal Interface[/dim]\n")
