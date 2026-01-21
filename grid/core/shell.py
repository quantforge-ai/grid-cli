import os
import subprocess
import shlex
import sys
import ctypes
from rich.console import Console
from rich.prompt import Prompt
from grid.core import style

console = Console()

def set_window_title(title):
    """Forces the Windows/Linux terminal window title to change."""
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")

def launch():
    """
    The Main Event Loop.
    This makes 'grid.exe' behave like 'bash.exe' or 'cmd.exe'.
    """
    # 1. Initialize the Environment
    set_window_title("Grid Terminal // Neural Link Active")
    os.system('cls' if os.name == 'nt' else 'clear') # Start fresh
    
    # 2. Run the Boot Sequence (The "Movie" effect)
    style.boot_sequence()
    style.print_header()
    style.print_dashboard()
    
    console.print("\n[bold green]>> NEURAL LINK ESTABLISHED.[/] [dim](Ready for input)[/]\n")

    # 3. The Infinite Shell Loop
    while True:
        try:
            # --- THE PROMPT ---
            # Get current directory and shorten it if it's too long
            cwd = os.getcwd()
            home = os.path.expanduser("~")
            if cwd.startswith(home):
                cwd = "~" + cwd[len(home):] # Replace C:\Users\Tanishq with ~
            
            # The actual prompt line: "   ~/projects/grid-cli $ "
            user_input = Prompt.ask(f"[bold cyan]{cwd}[/] [bold green]$[/]")
            
            if not user_input.strip():
                continue

            # Parse command
            # shlex.split handles quotes correctly: git commit -m "my message"
            try:
                parts = shlex.split(user_input)
            except ValueError:
                console.print("[red]Error: Unclosed quote.[/]")
                continue

            cmd = parts[0].lower()

            # --- BUILT-IN SHELL COMMANDS ---
            if cmd == "exit" or cmd == "quit":
                console.print("[bold red]>> Terminating Neural Link...[/]")
                break
            
            elif cmd == "cls" or cmd == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                style.print_header()
                continue
            
            elif cmd == "cd":
                # Python needs to handle CD manually to persist state
                try:
                    target = parts[1] if len(parts) > 1 else home
                    os.chdir(target)
                except FileNotFoundError:
                    console.print(f"[red]Directory not found: {target}[/]")
                except Exception as e:
                    console.print(f"[red]Error: {e}[/]")
                continue

            # --- GRID COMMAND SHORTCUTS ---
            # Allows typing 'push' instead of 'grid push' inside this specific terminal
            grid_keywords = [
                "auth", "init", "dev", "status", "branch", "push", "home", 
                "purge", "roast", "rank", "blame", "docker", "tree", "recap"
            ]
            
            if cmd in grid_keywords:
                # We re-run the grid command as a subprocess
                # This ensures it uses the same logic as the CLI
                subprocess.run(["grid"] + parts, shell=True)
            
            # --- SYSTEM COMMAND PASSTHROUGH ---
            # Passes 'git status', 'npm start', 'dir' to the underlying OS
            else:
                # shell=True allows using pipes (|) and system aliases
                subprocess.run(user_input, shell=True)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully (don't crash the shell, just clear line)
            console.print("^C")
            continue
        except Exception as e:
            console.print(f"[bold red]System Error: {e}[/]")