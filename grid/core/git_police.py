import subprocess
import re
import os

# Default Banned Files
SENSITIVE_FILES = [".env", ".pem", ".key", "id_rsa", "credentials.json", ".grid"]

# Regex Patterns for Keys
SECRET_PATTERNS = [
    r"sk_live_[0-9a-zA-Z]{24}",        # Stripe
    r"ghp_[0-9a-zA-Z]{36}",             # GitHub
    r"xox[baprs]-([0-9a-zA-Z]{10,48})", # Slack
    r"AIza[0-9A-Za-z-_]{35}",           # Google
]

def get_git_root():
    """Returns the absolute path to the git root."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except:
        return os.getcwd()

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
    _, msg, _ = get_last_commit_info(author_name)
    return msg

def get_last_commit_info(author_name):
    """Fetches the last commit hash, message, and files for a specific author."""
    try:
        root = get_git_root()
        # 1. Get the hash and message of the last commit by this author
        # Use -i for case-insensitive search and --all to search all branches
        cmd = ["git", "log", "-i", "--all", f"--author={author_name}", "-n", "1", "--pretty=format:%H%n%s"]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip().split("\n")
        
        if not output or len(output) < 2 or not output[0]:
            return None, "No recent activity.", []
            
        commit_hash = output[0]
        commit_msg = output[1]
            
        # 2. Get files in that commit
        files_cmd = ["git", "show", "--name-only", "--pretty=format:", commit_hash]
        files = subprocess.check_output(files_cmd, stderr=subprocess.DEVNULL).decode().strip().splitlines()
        
        abs_files = []
        for f in files:
            f = f.strip()
            if not f: continue
            abs_files.append(os.path.join(root, f))
            
        return commit_hash, commit_msg, abs_files
    except:
        return None, "Unknown Commit", []

def get_commit_diff(commit_hash):
    """
    Fetches the actual code changes for a specific commit.
    """
    try:
        # Get the diff of the changes in this commit
        # -U0 = zero context lines (we just want the changes)
        diff = subprocess.check_output(
            ["git", "show", commit_hash, "-U0", "--pretty=format:"], 
            stderr=subprocess.STDOUT
        ).decode('utf-8', errors='ignore').strip()
        
        # If the diff is too large (safety), truncate it
        if len(diff) > 5000:
            return diff[:5000] + "\n...[Truncated]..."
            
        return diff if diff else ""
    except Exception:
        return ""