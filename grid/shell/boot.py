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

    # Technical loading sequence
    steps = [
        "Mounting File System...",
        "Verifying CUDA Cores...",
        "Synchronizing Synapses...",
        "Handshaking with Grid Node...",
        "Allocating Memory Buffers...",
        "Decrypting Personality Core..."
    ]
    
    for step in steps:
        console.print(f"[dim green]/// {step}[/dim green]")
        time.sleep(random.uniform(0.2, 0.4))
    
    time.sleep(2.0)
    console.print("[bold green]/// ACCESS GRANTED[/bold green]\n")
    console.clear()
    console.print("[dim]Grid CLI v1.0 | Universal Interface[/dim]\n")
