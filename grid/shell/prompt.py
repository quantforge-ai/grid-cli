"""
Grid CLI - Prompt Styling
"""

import os
import getpass
from prompt_toolkit.formatted_text import HTML

def get_prompt():
    """Generates the clean 'Grid Terminal' prompt in HTML."""
    cwd = os.getcwd()
    # Shorten home directory to ~
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd = cwd.replace(home, "~", 1)
    
    # Format: ➜ {cwd} $ 
    return HTML(
        f"<style fg='green' font='bold'>➜</style> "
        f"<style fg='magenta' font='italic'>{cwd}</style> "
        f"<style fg='white' font='bold'>$ </style>"
    )

def set_terminal_title():
    """Sets the OS terminal window title."""
    import platform
    if platform.system() == "Windows":
        os.system("title Grid Terminal // Neural Link Active")
