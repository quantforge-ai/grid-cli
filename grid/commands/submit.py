import subprocess
import sys
from grid.core import git_police, utils

def run(message):
    utils.print_header("Analyzing Trajectory...")

    # --- PHASE 0: AUTO-STAGE EVERYTHING (Frictionless) ---
    # We add ALL files (new and modified) immediately so we can scan them.
    # This fixes the "untracked files" error you saw.
    subprocess.run(["git", "add", "."])

    # --- PHASE 1: THE SECRET SNIFFER ---
    # Now that files are staged, we check them for secrets.
    leaks = git_police.scan_for_secrets()
    if leaks:
        utils.print_warning(f"SECRET LEAK DETECTED in: {', '.join(leaks)}")
        utils.print_header("🚑 Initiating Emergency Unstage...")
        
        # We unstage the dangerous files so they are NOT committed
        subprocess.run(["git", "restore", "--staged"] + leaks)
        
        utils.print_success("Secrets neutralized. Continuing with safe files.")

    # --- PHASE 2: THE COWBOY PROTOCOL ---
    # Check branch safety using the new dynamic naming logic
    is_risk, safe_branch = git_police.cowboy_check(message)
    
    if is_risk:
        utils.print_warning(f"COWBOY DETECTED! You are pushing directly to '{git_police.get_current_branch()}'.")
        utils.print_header(f"🤠 I am taking the wheel.")
        
        try:
            # We carry the staged files over to the new branch
            subprocess.run(["git", "checkout", "-b", safe_branch], check=True)
            utils.print_success(f"Switched to safety branch: '[bold cyan]{safe_branch}[/]'")
            utils.print_header("You can thank me later.")
        except subprocess.CalledProcessError:
            utils.print_error("Failed to auto-branch. You are on your own, Cowboy.")
            return

    # --- PHASE 3: THE COMMIT ---
    if len(message) < 5:
        utils.print_warning(f"Commit message '{message}' is pathetic. I'm adding context.")
        message = f"{message} (Grid: User refused to elaborate)"

    # We don't need 'git add' here anymore because we did it in Phase 0
    result = subprocess.run(["git", "commit", "-m", message])

    if result.returncode == 0:
        utils.print_success("Code submitted successfully.")
    else:
        # If commit fails (e.g., empty commit after unstaging secrets), we warn the user
        utils.print_error("Git commit failed. (Did I unstage everything?)")