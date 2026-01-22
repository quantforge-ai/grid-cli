import subprocess
from grid.core import utils, config

def corporate_translator(message):
    """Translates dev-speak to manager-speak."""
    msg = message.lower()
    if "fix" in msg or "bug" in msg:
        return "Resolved critical stability issues in core logic."
    if "feat" in msg or "add" in msg:
        return "Implemented new user-facing functionality."
    if "refactor" in msg or "clean" in msg:
        return "Optimized technical debt to improve maintainability."
    if "wip" in msg:
        return "Conducted ongoing research and development."
    return f"Progressed on task: {message}"

def run():
    utils.print_header("GENERATING DAILY REPORT")
    
    identity = config.get_global_identity()
    
    # Get commits from last 24h by this author
    # We try to match git config name roughly if identity fails
    cmd = [
        "git", "log", 
        f"--author={identity}", 
        "--since=24.hours", 
        "--pretty=format:%s"
    ]
    
    try:
        logs = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().splitlines()
    except:
        logs = []

    if not logs:
        utils.print_warning(f"No activity detected for '{identity}' in the last 24 hours.")
        utils.print_warning("(Try 'grid auth <git_name>' if the name doesn't match)")
        return

    utils.console.print(f"\n[bold underline]Daily Standup for {identity}:[/]\n")
    
    for log in logs:
        translated = corporate_translator(log)
        utils.console.print(f"• {translated} (Ref: '{log}')")
        
    utils.print_success("\nCopy-paste this to your manager.")