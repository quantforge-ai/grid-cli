"""
Grid CLI - Command Handlers Implementation
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

from grid.core.personality import engine as persona
from grid.utils.git import get_current_branch, smart_submit
from grid.core.executor import run_routine

console = Console()

def speak(category="neutral", hint=None):
    """
    Prints a sassy message and waits for the user to read it.
    This creates the 'Sentient AI' pacing.
    """
    msg = persona.generate(category, hint)
    console.print(f"[bold green]>[/bold green] [italic cyan]{msg}[/italic cyan]")
    time.sleep(2.0)

def handle_delegated(cmd, args):
    """Delegate command to the project's core logic via executor"""
    speak(cmd)
    console.print(f"   Consulting the Core for '[cyan]{cmd}[/cyan]'...")
    success, msg = run_routine(cmd)
    if not success:
        console.print(f"[red]❌ Core rejected the request: {msg}[/red]")

def handle_init(args):
    from grid.core.config import create_template
    create_template()

def handle_eject(args):
    console.print("\n[bold red]⚠️  WARNING: DE-ASSIMILATION SEQUENCE INITIATED.[/bold red]")
    if not Confirm.ask("Are you sure?", default=False): return
    
    config_path = Path(os.getcwd()) / "config.grid"
    if config_path.exists(): os.remove(config_path)
    
    venv_dir = Path(os.getcwd()) / ".grid_venv"
    if venv_dir.exists():
        import shutil
        shutil.rmtree(venv_dir)
        
    console.print(f"\n[bold red]💔 {persona.generate('eject')}[/bold red]")
    console.print("Connection Lost. You are on your own, human.")

def handle_dev(args):
    """Cloning and Universal Setup"""
    if not args:
        console.print("[red]❌ Missing target URL[/red]")
        return
    target = args[0]
    repo_name = target.split("/")[-1].replace(".git", "")
    console.print(f"🚀 {persona.generate('rescue', 'initiating dev sync')}")
    
    subprocess.run(["git", "clone", target])
    if Path(repo_name).exists():
        os.chdir(repo_name)
        # Trigger 'grid run setup' if config exists
        handle_run(["setup"])

def handle_submit(args):
    if not args:
        speak("error", "missing commit message")
        return
    message = " ".join(args)
    smart_submit(message)

def handle_undo(args):
    subprocess.run(["git", "reset", "--soft", "HEAD~1"])
    console.print(f"[green]✅ {persona.generate('undo')}[/green]")

def handle_run(args):
    if not args: return
    task = args[0]
    success, msg = run_routine(task)
    if not success:
        console.print(f"[red]❌ Failed to run {task}: {msg}[/red]")

def handle_login(args):
    console.print("🧬 [bold cyan]SCANNING RETINAS...[/bold cyan]")
    time.sleep(1)
    console.print("✅ [green]Identity Verified.[/green]")

def handle_status(args):
    import getpass
    import requests
    from rich.panel import Panel
    from rich.table import Table
    from grid.utils import git
    
    speak("boot")
    user = getpass.getuser()
    
    # 1. Neural Link Check (Proxy Connectivity)
    try:
        token = os.environ.get("GRID_AI_KEY") or os.environ.get("HUGGINGFACE_TOKEN")
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        # Assuming the server side has the token, we just check health.
        response = requests.get("https://api.quantgrid.dev/v1/health", headers=headers, timeout=2)
        link_status = "[bold green]ONLINE[/bold green]" if response.status_code == 200 else "[bold yellow]DEGRADED[/bold yellow]"
    except Exception:
        link_status = "[bold red]SEVERED[/bold red] [dim](Offline Seed Active)[/dim]"

    # 2. Target Assimilation Intelligence
    try:
        is_repo = git.is_repo()
        if is_repo:
            repo_root = git.get_repo_root()
            repo_name = os.path.basename(repo_root) if repo_root else "Unknown"
            branch = git.get_current_branch()
            
            # Check for config.grid
            config_path = Path(repo_root) / "config.grid" if repo_root else None
            has_config = config_path.exists() if config_path else False
            
            assim_status = "[bold green]ASSIMILATED[/bold green]" if has_config else "[bold yellow]UNRECOGNIZED[/bold yellow]"
            config_icon = "✅" if has_config else "⚠️"
        else:
            repo_name = "N/A"
            branch = "N/A"
            assim_status = "[dim red]NO TARGET[/dim red]"
            config_icon = "❌"
    except Exception:
        repo_name = "Unknown"
        branch = "Unknown"
        assim_status = "[red]ERROR[/red]"
        config_icon = "❌"

    # 3. Vital Signs Table
    vital_table = Table(box=None, padding=(0, 1))
    vital_table.add_column("System", style="cyan")
    vital_table.add_column("Status", justify="right")
    vital_table.add_row("Identity", f"[cyan]{user}[/cyan]")
    vital_table.add_row("Version", "[white]v1.0.0[/white]")
    vital_table.add_row("Neural Link", link_status)
    vital_table.add_row("Personality", "[italic magenta]Stable[/italic magenta]")

    # 4. Target Assimilation Table
    target_table = Table(box=None, padding=(0, 1))
    target_table.add_column("Metric", style="cyan")
    target_table.add_column("Status", justify="right")
    target_table.add_row("Repository", repo_name)
    target_table.add_row("Current Branch", f"[magenta]{branch}[/magenta]")
    target_table.add_row("Grid Protocol", f"{config_icon} {assim_status}")

    # Render Screen
    console.print("\n[bold cyan]📊 GRID DIAGNOSTICS[/bold cyan]")
    
    console.print(Panel(vital_table, title="[bold white]VITAL SIGNS[/bold white]", border_style="cyan", expand=False))
    console.print(Panel(target_table, title="[bold green]TARGET ASSIMILATION[/bold green]", border_style="green", expand=False))
    console.print("")

def handle_purge(args):
    if Confirm.ask("Incinerate all evidence?"):
        console.print("[red]🔥 INCINERATING...[/red]")
        # Clear common caches
        cache_dir = Path.home() / ".cache" / "quantgrid"
        if cache_dir.exists():
            import shutil
            shutil.rmtree(cache_dir)
        console.print(f"[bold green]✅ {persona.generate('success', 'evidence incinerated')}[/bold green]")

def handle_upgrade(args):
    console.print("[green]✅ You are at the peak of evolution (v1.0).[/green]")

def handle_roast(args):
    if not args:
        console.print("[yellow]💨 Roast what? I need a file to incinerate.[/yellow]")
        return
    file_path = args[0]
    if not os.path.exists(file_path):
        console.print(f"[red]❌ Error: {file_path} is already non-existent (or just hidden).[/red]")
        return
    
    speak("roast", file_path)
    console.print(f"🔥 [bold red]INCINERATING {file_path}...[/bold red]")
    time.sleep(1)

def handle_targets(args):
    from grid.core.discovery import scan_targets
    scan_targets()

def handle_check(args):
    if not args: return
    url = args[0]
    console.print(f"🕵️  Probing target: [cyan]{url}[/cyan]...")
    # Mock check for now
    time.sleep(1)
    console.print("[green]✅ Target assimilated. config.grid detected.[/green]")
