"""
Grid CLI - Venv Isolation Utility
"""

import os
import subprocess
import sys
from pathlib import Path
from rich.console import Console

console = Console()

def get_venv_python():
    """Get the path to the python executable in the local .grid_venv."""
    venv_dir = Path(os.getcwd()) / ".grid_venv"
    if not venv_dir.exists():
        _create_venv(venv_dir)
    
    if os.name == "nt": # Windows
        return venv_dir / "Scripts" / "python.exe"
    else: # Linux/Mac
        return venv_dir / "bin" / "python"

def _create_venv(venv_dir):
    """Create a hidden .grid_venv."""
    console.print(f"🛠️  Initializing isolated environment in [cyan]{venv_dir.name}[/cyan]...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    console.print("✅ Environment isolated.")
