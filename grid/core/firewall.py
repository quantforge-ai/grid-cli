"""
Grid CLI - Digital Jail (Firewall)
"""

import os
import shutil
from pathlib import Path
from rich.console import Console
from grid.core.config import load_config
from grid.core.personality import engine as persona

console = Console()

def check_contamination():
    """Scan staged files for firewall violations."""
    config = load_config()
    if not config or "firewall" not in config:
        return True
    
    blocked = config["firewall"].get("block", [])
    violations = []
    
    # Simple check: if a blocked file exists in CWD, we count it as contamination 
    # (Real implementation would check 'git status')
    for pattern in blocked:
        # Basic glob matching logic simplified for this phase
        if pattern.startswith("*"):
            ext = pattern[1:]
            for f in os.listdir():
                if f.endswith(ext):
                    violations.append(f)
        elif os.path.exists(pattern):
            violations.append(pattern)
            
    if violations:
        console.print(f"[bold red]🛑 CONTAMINANT DETECTED:[/bold red] {', '.join(violations)}")
        for v in violations:
            _quarantine(v)
        return False
    
    return True

def _quarantine(file_path):
    """Move a file to 'Digital Jail' (Stash)."""
    jail_dir = Path(os.getcwd()) / ".grid_quarantine"
    jail_dir.mkdir(exist_ok=True)
    
    try:
        shutil.move(file_path, jail_dir / Path(file_path).name)
        console.print(f"[dim]File [white]{file_path}[/white] is now serving a life sentence in 'Digital Jail'.[/dim]")
    except Exception as e:
        console.print(f"[red]Failed to seize contaminant: {e}[/red]")
