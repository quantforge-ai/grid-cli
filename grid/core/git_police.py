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

def get_last_commit_message(author_name):
    """Fetches the last commit message for a specific author."""
    try:
        cmd = ["git", "log", f"--author={author_name}", "-n", "1", "--pretty=format:%s"]
        msg = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
        return msg if msg else "No recent activity."
    except:
        return "Unknown Commit"

def get_last_commit_files(author_name):
    """Fetches files changed in the last commit by a specific author."""
    try:
        # 1. Get the hash of the last commit by this author
        hash_cmd = ["git", "log", f"--author={author_name}", "-n", "1", "--pretty=format:%H"]
        commit_hash = subprocess.check_output(hash_cmd, stderr=subprocess.DEVNULL).decode().strip()
        
        if not commit_hash:
            return []
            
        # 2. Get files in that commit
        files_cmd = ["git", "show", "--name-only", "--pretty=format:", commit_hash]
        files = subprocess.check_output(files_cmd, stderr=subprocess.DEVNULL).decode().strip().splitlines()
        return [f.strip() for f in files if f.strip()]
    except:
        return []