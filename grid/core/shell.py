import os
import subprocess
import shlex
import sys
import ctypes
import socket
from rich.console import Console
from rich.prompt import Prompt
from grid.core import style, config

console = Console()

def set_window_title(title):
    """Forces the Windows/Linux terminal window title to change."""
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")

def get_short_path(cwd):
    """
    Smartly shortens the path for the prompt.
    Full: C:/Users/Tanishq/AppData/Local/Programs/Grid CLI
    Short: ~/.../Grid CLI
    """
    home = os.path.expanduser("~")
    
    # 1. Replace Home with ~
    if cwd.startswith(home):
        path = "~" + cwd[len(home):]
    else:
        path = cwd

    # 2. Normalize Slashes
    path = path.replace("\\", "/")

    # 3. Truncate if too long (Visual noise reduction)
    # More aggressive shortening - show only last directory
    if len(path) > 25:
        parts = path.split("/")
        # Keep the first part (~ or Drive) and only the LAST part
        if len(parts) > 2:
            return f"{parts[0]}/.../{parts[-1]}"
    
    return path

def launch():
    """
    The Main Event Loop.
    Mimics Git Bash prompt style: user@host GRID ~/path $
    """
    # 1. Initialize the Environment
    set_window_title("Grid Terminal // Neural Link Active")
    os.system('cls' if os.name == 'nt' else 'clear') 
    
    # 2. Run the Boot Sequence (The "Package Loader" animation)
    style.boot_sequence()
    style.print_header()
    
    console.print("\n[bold green]>> NEURAL LINK ESTABLISHED.[/] [dim](Ready for input)[/]\n")

    # 3. The Infinite Shell Loop
    while True:
        try:
            # --- CONSTRUCT THE PROMPT ---
            
            # A. Get Identity (User)
            # If they haven't run 'grid auth' yet, default to system name or "Stranger"
            grid_user = config.get_global_identity()
            if grid_user == "Stranger":
                # Fallback to computer username if Grid auth isn't set
                try:
                    grid_user = os.getlogin().lower()
                except:
                    grid_user = "user"

            # B. Get Hostname (Computer Name)
            try:
                hostname = socket.gethostname().lower()
            except:
                hostname = "localhost"

            # C. Get Current Directory (Path) - SHORTENED VERSION
            current_path = get_short_path(os.getcwd())
            
            # D. Build the Git-Bash style string
            # Format: user@host (Green) GRID (Magenta) path (Yellow) $
            prompt_str = (
                f"[bold green]{grid_user}@{hostname}[/] "
                f"[bold magenta]GRID[/] "
                f"[bold yellow]{current_path}[/] "
                f"[bold white]$[/] "
            )

            # --- ASK FOR INPUT ---
            user_input = Prompt.ask(prompt_str)
            
            if not user_input.strip():
                continue

            # Parse command
            try:
                parts = shlex.split(user_input)
            except ValueError:
                console.print("[red]Error: Unclosed quote.[/]")
                continue

            cmd = parts[0].lower()

            # --- BUILT-IN COMMANDS ---
            if cmd == "exit" or cmd == "quit":
                console.print("[bold red]>> Terminating Neural Link...[/]")
                break
            
            elif cmd == "cls" or cmd == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                style.print_header()
                continue
            
            elif cmd == "cd":
                try:
                    target = parts[1] if len(parts) > 1 else home
                    os.chdir(target)
                except FileNotFoundError:
                    console.print(f"[red]Directory not found: {target}[/]")
                except Exception as e:
                    console.print(f"[red]Error: {e}[/]")
                continue

            # --- GRID SHORTCUTS ---
            grid_keywords = [
                "auth", "init", "dev", "status", "branch", "push", "home", 
                "purge", "roast", "rank", "blame", "docker", "tree", "recap"
            ]
            
            if cmd in grid_keywords:
                # Pass through to the installed grid command
                subprocess.run(["grid"] + parts, shell=True)
            
            # --- SYSTEM COMMANDS ---
            else:
                subprocess.run(user_input, shell=True)

        except KeyboardInterrupt:
            console.print("^C")
            continue
        except Exception as e:
            console.print(f"[bold red]System Error: {e}[/]")