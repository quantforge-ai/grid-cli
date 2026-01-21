import subprocess
from grid.core import utils, git_police, scraper

def run(name):
    utils.print_header("BRANCH MANAGER")
    
    # 1. Get List of Branches
    try:
        raw = subprocess.check_output(["git", "branch"], stderr=subprocess.DEVNULL).decode()
        # Clean up output (remove * and spaces)
        branches = [b.strip().replace("* ", "") for b in raw.splitlines()]
    except:
        utils.print_error("Not a git repository.")
        return

    current = git_police.get_current_branch()

    # 2. NAMING POLICE (Sassy Check)
    # If creating a new branch, judge the name
    if name not in branches:
        if "/" not in name and "-" not in name:
             # e.g., user typed "login" instead of "feature/login"
            roast = "Vague branch name detected. Consider 'feature/name' or 'fix/issue'."
            utils.print_warning(f"{roast}")
    
    # 3. SWITCH OR CREATE
    if name in branches:
        if name == current:
            utils.print_warning(f"You are already on [bold cyan]{name}[/].")
            return
        
        utils.spin_action(f"Switching to existing branch '{name}'...", 
            lambda: subprocess.run(["git", "checkout", name], check=True))
        utils.print_success(f"Active Branch: [bold green]{name}[/]")
        
    else:
        utils.spin_action(f"Creating new branch '{name}'...", 
            lambda: subprocess.run(["git", "checkout", "-b", name], check=True))
        utils.print_success(f"Branch Initialized: [bold green]{name}[/]")