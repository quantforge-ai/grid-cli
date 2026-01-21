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
    """Fetches the git username (e.g., 'tanishq')"""
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return name.split(" ")[0].lower() if name else "stranger"
    except:
        return "stranger"

def slugify(text):
    """Turns 'Fixing the Auth!!' into 'fixing-the-auth'."""
    clean = "".join(c if c.isalnum() or c.isspace() else "" for c in text).strip()
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

def scan_for_secrets(custom_patterns=None):
    """
    Scans STAGED files for secrets. 
    Accepts custom banned filenames from .grid config.
    Returns a list of file paths that contain secrets.
    """
    # Merge default sensitive files with project-specific bans
    banned_files = SENSITIVE_FILES + (custom_patterns or [])
    
    try:
        files = subprocess.check_output(
            ["git", "diff", "--name-only", "--cached"],
            stderr=subprocess.DEVNULL
        ).decode().splitlines()
    except:
        return []

    leaking_files = []

    for file_path in files:
        # Check against banned filenames (e.g. .env, secrets.json)
        if any(file_path.endswith(s) for s in banned_files):
            leaking_files.append(file_path)
            continue
        
        # Check file content for regex patterns (API keys)
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

# --- CONTEXT AWARENESS LOGIC ---
def detect_context_switch(message):
    """
    Decides if we should start a FRESH branch from main.
    Returns: (should_switch, new_branch_name)
    """
    current = get_current_branch()
    slug = slugify(message)
    user = get_git_user()
    
    # Format: cowboy/topic/user
    new_branch_name = f"cowboy/{slug}/{user}"

    # CASE 1: On Main/Master (The original Cowboy check)
    if current in PROTECTED_BRANCHES:
        return True, new_branch_name

    # CASE 2: Already on a Cowboy Branch?
    if current.startswith("cowboy/"):
        try:
            # Current: cowboy/auth-fix/tanishq
            # Message: "adding stripe payment" -> slug: "adding-stripe-payment"
            
            parts = current.split('/')
            if len(parts) > 1:
                old_topic = parts[1] # "auth-fix"
                
                # Tokenize to check for overlap
                old_tokens = set(old_topic.split('-'))
                new_tokens = set(slug.split('-'))
                
                # If they share NO words, it's a context switch
                # (e.g. "auth" vs "payment" = No match)
                if not old_tokens.intersection(new_tokens):
                    return True, new_branch_name
        except:
            pass 

    return False, None