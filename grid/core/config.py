"""
Grid CLI - config.grid Parser
"""

import os
import yaml
from pathlib import Path
from rich.console import Console
from grid.core.personality import engine as persona

console = Console()

def load_config():
    """Load and parse config.grid from CWD."""
    config_path = Path(os.getcwd()) / "config.grid"
    if not config_path.exists():
        return None
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Neural Link Corruption: {e}[/red]")
        return None

def create_template():
    """Create a default config.grid template."""
    target_file = Path(os.getcwd()) / "config.grid"
    if target_file.exists():
        console.print("[yellow]⚠️  Directory already assimilated.[/yellow]")
        return
    
    template = """# ⚡ GRID PROTOCOL v1.0
project:
  name: "{name}"
  type: "python"

firewall:
  block:
    - ".env"
    - "secrets.json"
    - "*.key"

commands:
  setup: "pip install -e ."
  train: "python -m quantgrid.ml.trainer"
  push: "python -m quantgrid.hub.submit"
  status: "python -m quantgrid.hub.status"
  test: "pytest"
"""
    name = os.path.basename(os.getcwd())
    try:
        with open(target_file, 'w', encoding="utf-8") as f:
            f.write(template.format(name=name))
        console.print(f"[green]✅ {persona.generate('success', 'repo assimilated')}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to assimilate: {e}[/red]")
