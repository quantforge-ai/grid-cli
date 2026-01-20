"""
Grid CLI - Git Guardian
"""

import subprocess
import random
from rich.console import Console
from grid.core.personality import engine as persona

console = Console()

def get_current_branch():
    """Get the name of the current active branch."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"

def is_repo():
    """Check if the current directory is inside a git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def get_repo_root():
    """Get the absolute path to the root of the git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return None

def generate_rescue_branch_name(msg_hint: str):
    """Generate a mischievous branch name for auto-rescue."""
    prefixes = ["grid-auto/rescue-", "grid-auto/oops-", "grid-auto/human-fix-"]
    clean_hint = "".join(e for e in msg_hint if e.isalnum())[:15].lower()
    return f"{random.choice(prefixes)}{clean_hint}"

def smart_submit(message):
    """Safe commit with auto-branching rescue."""
    from grid.core.firewall import check_contamination
    
    # 1. Firewall check
    if not check_contamination():
        console.print(f"[red]❌ Submission aborted. {persona.generate('firewall')}[/red]")
        return False
        
    branch = get_current_branch()
    if branch in ['main', 'master']:
        rescue_branch = generate_rescue_branch_name(message)
        console.print(f"[green]🛡️  RESCUE PROTOCOL:[/green] Moving to [cyan]{rescue_branch}[/cyan]")
        subprocess.run(["git", "checkout", "-b", rescue_branch])
    
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])
    console.print(f"[green]✅ {persona.generate('success', 'code injected')}[/green]")
    return True
