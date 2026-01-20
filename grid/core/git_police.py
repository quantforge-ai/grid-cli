import os
import subprocess
import re
import time

# --- CONFIGURATION ---
PROTECTED_BRANCHES = ["main", "master", "dev", "production"]
SENSITIVE_FILES = [".env", ".pem", ".key", "id_rsa", "credentials.json"]
SECRET_PATTERNS = [
    r"sk_live_[0-9a-zA-Z]{24}",        # Stripe Keys
    r"ghp_[0-9a-zA-Z]{36}",             # GitHub Tokens
    r"xox[baprs]-([0-9a-zA-Z]{10,48})", # Slack Tokens
    r"AIza[0-9A-Za-z-_]{35}",           # Google API Keys
]

def get_current_branch():
    """Returns the active git branch name."""
    try:
        return subprocess.check_output(
            ["git", "branch", "--show-current"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except:
        return None

def get_git_user():
    """Fetches the configured git username."""
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        # Sanitize: "Tanishq Dasari" -> "tanishq"
        return name.split(" ")[0].lower() if name else "stranger"
    except:
        return "stranger"

def slugify(text):
    """Turns 'Fixing the Auth Bug!!' into 'fixing-the-auth-bug'."""
    # Remove special chars, keep spaces/alphanumeric
    clean = "".join(c if c.isalnum() or c.isspace() else "" for c in text).strip()
    # Join with dashes and limit to 4 words
    return "-".join(clean.split()[:4]).lower()

def is_clean():
    """Checks if there are uncommitted changes."""
    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], 
            stderr=subprocess.DEVNULL
        ).decode()
        return not status.strip()
    except:
        return False

def scan_for_secrets():
    """
    Scans STAGED files for secrets. 
    Returns a list of file paths that contain secrets.
    """
    try:
        files = subprocess.check_output(
            ["git", "diff", "--name-only", "--cached"],
            stderr=subprocess.DEVNULL
        ).decode().splitlines()
    except:
        return []

    leaking_files = []

    for file_path in files:
        if any(file_path.endswith(s) for s in SENSITIVE_FILES):
            leaking_files.append(file_path)
            continue
        
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

def cowboy_check(message=""):
    """
    Returns (is_risk, suggestion)
    Constructs a sassy branch name based on the commit message and user.
    """
    branch = get_current_branch()
    
    if branch in PROTECTED_BRANCHES:
        user = get_git_user()
        slug = slugify(message) if message else f"patch-{int(time.time())}"
        
        # New Format: cowboy/topic/who-saved
        # Example: cowboy/initial-commit/tanishq-saved
        safe_name = f"cowboy/{slug}/{user}-saved"
        return True, safe_name
        
    return False, None