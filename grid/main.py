"""
Grid CLI - Main Entry Point
"""

import sys
from grid.shell.loop import start_repl
from grid.shell.handlers import get_handler

def main():
    # If no args, start the interactive shell
    if len(sys.argv) == 1:
        start_repl()
        return

    # Handle one-off commands
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    handler = get_handler(cmd)
    if handler:
        handler(args)
    else:
        # Fallback to system help if unknown command
        print(f"Unknown Grid command: {cmd}")
        print("Type 'grid' for the interactive shell or 'grid help' for a list of commands.")

if __name__ == "__main__":
    main()
