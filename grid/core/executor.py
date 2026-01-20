"""
Grid CLI - Universal Executor (The Bridge)
"""

import os
import subprocess
from rich.console import Console
from grid.core.config import load_config
from grid.utils.venv import get_venv_python

console = Console()

def run_routine(command_key):
    """
    Executes a command defined in config.grid using the isolated venv.
    Maps: 'train' -> 'python -m quantgrid.ml.trainer'
    """
    config = load_config()
    if not config:
        return False, "Target not assimilated (no config.grid found)."
    
    commands = config.get("commands", {})
    if command_key not in commands:
        return False, f"Command '{command_key}' not documented in this project's archive."
    
    full_cmd = commands[command_key]
    venv_python = get_venv_python()
    
    # If the command starts with 'python', replace it with the venv python
    if full_cmd.startswith("python "):
        full_cmd = str(venv_python) + full_cmd[6:]
        
    console.print(f"📡 [dim]Executing:[/dim] [italic]{full_cmd}[/italic]")
    
    try:
        # Run the command
        subprocess.run(full_cmd, shell=True, check=True)
        return True, "Execution complete."
    except subprocess.CalledProcessError as e:
        return False, f"Process exited with error code {e.returncode}"
    except Exception as e:
        return False, str(e)
