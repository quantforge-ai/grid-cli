import subprocess
import re

# Default Banned Files
SENSITIVE_FILES = [".env", ".pem", ".key", "id_rsa", "credentials.json", ".grid"]

# Regex Patterns for Keys
SECRET_PATTERNS = [
    r"sk_live_[0-9a-zA-Z]{24}",        # Stripe
    r"ghp_[0-9a-zA-Z]{36}",             # GitHub
    r"xox[baprs]-([0-9a-zA-Z]{10,48})", # Slack
    r"AIza[0-9A-Za-z-_]{35}",           # Google
]

def get_current_branch():
    """Returns the active git branch name."""
    try:
        return subprocess.check_output(
            ["git", "branch", "--show-current"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except:
        return "unknown"

def scan_for_secrets(custom_patterns=None):
    """
    Scans staged files for banned filenames or regex patterns.
    """
    # Combine default bans with project-specific bans
    banned_files = SENSITIVE_FILES + (custom_patterns or [])
    
    try:
        # Get list of staged files
        files = subprocess.check_output(
            ["git", "diff", "--name-only", "--cached"], 
            stderr=subprocess.DEVNULL
        ).decode().splitlines()
    except:
        return []

def get_last_commit_message(author_name):
    """Fetches the last commit message for a specific author."""
    try:
        # Tries to find last commit by author
        cmd = ["git", "log", f"--author={author_name}", "-n", "1", "--pretty=format:%s"]
        msg = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
        return msg if msg else "No recent activity."
    except:
        return "Unknown Commit"

    leaking_files = []

    for file_path in files:
        # 1. Check Filenames
        if any(file_path.endswith(s) for s in banned_files):
            leaking_files.append(file_path)
            continue
        
        # 2. Check Content (Regex)
        try:
            content = subprocess.check_output(
                ["git", "show", f":{file_path}"], 
                stderr=subprocess.DEVNULL
            ).decode(errors='ignore')
            
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, content):
                    leaking_files.append(file_path)
                    break
        except:
            continue

    return leaking_files