"""
Grid CLI - The Matrix REPL
"""

import os
import sys
import shlex
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML

from grid.shell.prompt import get_prompt
from grid.shell.help import show_help
from grid.shell.boot import boot_sequence
from grid.core.personality import engine as persona

console = Console()

class GridREPL:
    def __init__(self):
        self.session = PromptSession(
            history=FileHistory(os.path.expanduser("~/.grid_history")),
            auto_suggest=AutoSuggestFromHistory()
        )
        # Import handlers inside loop to avoid circular imports
        from grid.shell.handlers import get_handler
        self.get_handler = get_handler

    def start(self):
        from grid.shell.prompt import set_terminal_title
        from grid.shell.handlers_logic import speak
        set_terminal_title()
        boot_sequence()
        speak("boot")
        
        while True:
            try:
                # 1. The Prompt
                prompt_html = get_prompt()
                user_input = self.session.prompt(prompt_html)
                
                cmd_str = user_input.strip()
                if not cmd_str:
                    continue
                
                # 2. Shell Built-ins (No prefix needed)
                if cmd_str.lower() in ["exit", "quit", "disconnect", "eject"]:
                    console.print(f"\n[bold red]💔 {persona.generate('eject')}[/bold red]")
                    time.sleep(5.0)  # Dramatic farewell pause
                    break
                
                if cmd_str.lower() in ["clear", "cls"]:
                    import platform
                    os.system("cls" if platform.system() == "Windows" else "clear")
                    continue

                # Handle "cd" (Must change process dir)
                if cmd_str.startswith("cd "):
                    try:
                        target = cmd_str[3:].strip()
                        if target == "~":
                            target = os.path.expanduser("~")
                        os.chdir(target)
                    except FileNotFoundError:
                        console.print(f"[red]❌ Directory not found: {target}[/red]")
                    except Exception as e:
                        console.print(f"[red]❌ Error: {e}[/red]")
                    continue

                # 3. The "grid" Command Logic (Prefix Mode)
                if cmd_str.startswith("grid ") or cmd_str == "grid":
                    payload = cmd_str[5:].strip()
                    if not payload:
                        payload = "help"
                    
                    # Parse internal grid command
                    parts = shlex.split(payload)
                    grid_cmd = parts[0]
                    grid_args = parts[1:]
                    
                    if grid_cmd == "help":
                        show_help()
                        continue
                        
                    handler = self.get_handler(grid_cmd)
                    if handler:
                        handler(grid_args)
                        continue
                    else:
                        console.print(f"[yellow]❓ Unknown Grid protocol: [bold]{grid_cmd}[/bold]. Type 'grid help' for guidance.[/yellow]")
                        continue

                # 4. System Passthrough (Terminal Mode)
                try:
                    import subprocess
                    subprocess.run(cmd_str, shell=True)
                except Exception as e:
                    console.print(f"[red]❌ System execution failed: {e}[/red]")
                
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Critical Error: {e}[/red]")

def start_repl():
    repl = GridREPL()
    repl.start()
