import os
import subprocess
import random
import click
from grid.core import utils, analyzer, scraper, broadcaster, git_police

# ... (Keep get_random_roast and get_last_commit_stats exactly as they were) ...
def get_random_roast(category="roasts"):
    try:
        db = scraper.load_db() 
        return random.choice(db.get(category, ["System offline. You got lucky."]))
    except:
        return "Database Error."

def get_last_commit_stats(developer):
    # (Same code as before - keeping it brief for the response)
    try:
        cmd = f'git log --author="{developer}" -n 1 --pretty=format:"%h|%s"'
        result = subprocess.check_output(cmd, shell=True).decode().strip()
        if not result: return None
        commit_hash, message = result.split("|", 1)
        stat_cmd = f"git show {commit_hash} --shortstat --oneline"
        stats = subprocess.check_output(stat_cmd, shell=True).decode().strip()
        files_cmd = f"git diff-tree --no-commit-id --name-only -r {commit_hash}"
        files = subprocess.check_output(files_cmd, shell=True).decode().splitlines()
        return {"hash": commit_hash, "message": message, "stats": stats, "files": files}
    except:
        return None

# --- COMMANDS ---

def roast_file(target):
    # (Same as before)
    pass 

def roast_project():
    # (Same as before)
    pass

def roast_developer(developer, recent, share):
    """
    The main logic handles --share now.
    """
    utils.print_header(f"Targeting developer identity: [bold red]{developer}[/]")
    
    data = get_last_commit_stats(developer)
    if not data:
        utils.print_error(f"User '{developer}' not found in git history.")
        return

    commit_msg = data['message']
    files = data['files']
    
    utils.print_dashboard({
        "Target": developer,
        "Last Commit": data['hash'],
        "Message": f"'{commit_msg}'",
        "Files Changed": f"{len(files)}"
    })

    # --- JUDGEMENT LOGIC (Same as before) ---
    is_good_commit = True
    critique = ""

    if len(commit_msg) < 10:
        is_good_commit = False
        critique = "Commit message is shorter than a tweet."
    elif len(commit_msg) < 20 and any(x in commit_msg.lower() for x in ["fix", "wip", "update"]):
        is_good_commit = False
        critique = "Using generic words without context?"

    if is_good_commit and files:
        target_code = next((f for f in files if f.endswith('.py')), None)
        if target_code and os.path.exists(target_code):
             code_verdict = analyzer.scan_file(target_code)
             if "adequate" not in code_verdict.lower():
                 is_good_commit = False
                 critique = f"Code Analysis Failed: {code_verdict}"

    # --- VERDICT ---
    flavor = ""
    if is_good_commit:
        flavor = get_random_roast("compliments")
        utils.print_success(f"Verdict: Solid work. \n>> Grid: {flavor}")
    else:
        flavor = get_random_roast("roasts")
        if not critique: critique = "Your git history is a cry for help."
        utils.print_warning(f"Verdict: {critique}\n>> Grid: {flavor}")

    # --- THE SHARE LOGIC ---
    if share:
        attacker = git_police.get_git_user() # We know who YOU are
        broadcaster.broadcast_roast(attacker, developer, critique or "Clean Commit", flavor, is_good_commit)