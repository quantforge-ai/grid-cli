import os
import subprocess
import random
import click
from grid.core import utils, analyzer, scraper

# --- HELPER: PVP LOGIC ---
def get_last_commit_stats(developer):
    """
    Digs up dirt on a specific developer's last commit.
    """
    try:
        # Get the hash and message of the last commit by this author
        cmd = f'git log --author="{developer}" -n 1 --pretty=format:"%h|%s"'
        result = subprocess.check_output(cmd, shell=True).decode().strip()
        
        if not result:
            return None
            
        commit_hash, message = result.split("|", 1)
        
        # Get the stats (insertions/deletions)
        stat_cmd = f"git show {commit_hash} --shortstat --oneline"
        stats = subprocess.check_output(stat_cmd, shell=True).decode().strip()
        
        return {"hash": commit_hash, "message": message, "stats": stats}
    except:
        return None

# --- COMMAND LOGIC ---

def roast_file(target):
    """
    Roasts a specific file using AST analysis.
    """
    utils.print_header(f"Scanning sector for '{target}'...")
    
    if not os.path.exists(target):
        utils.print_error(f"Target '{target}' not found. Are you hallucinating files?")
        return

    # 1. Run the Sentinel (Offline Intelligence)
    verdict = analyzer.scan_file(target)
    
    # 2. Print the Result
    utils.print_warning(f"Analysis Complete: {verdict}")

def roast_project():
    """
    Scans the current directory for the 'worst' file.
    """
    utils.print_header("Initiating full system scan...")
    
    # Find all python/js files
    files = []
    for root, _, filenames in os.walk("."):
        for f in filenames:
            if f.endswith((".py", ".js", ".cpp")):
                files.append(os.path.join(root, f))
    
    if not files:
        utils.print_error("No code found. Is this a ghost project?")
        return

    # Pick a random victim (for MVP speed) OR scan all and pick the worst stats
    # Let's pick a random one to roast for now to keep it fast
    victim = random.choice(files)
    roast_file(victim)

def roast_developer(developer, recent):
    """
    PvP Mode: Roasts a colleague based on git history.
    """
    utils.print_header(f"Targeting developer identity: [bold red]{developer}[/]")
    
    data = get_last_commit_stats(developer)
    
    if not data:
        utils.print_error(f"User '{developer}' not found in git history. Are they even working?")
        return

    # THE ROAST GENERATOR
    # We generate a roast based on the raw git stats
    
    commit_msg = data['message']
    stats = data['stats']
    
    utils.print_dashboard({
        "Target": developer,
        "Last Commit": data['hash'],
        "Message": f"'{commit_msg}'"
    })

    # Rule-based Roasts (Offline)
    roasts = []
    
    # Rule 1: Lazy Messages
    if len(commit_msg) < 10 or "fix" in commit_msg.lower():
        roasts.append(f"Commit message '{commit_msg}'? A literary masterpiece.")
        
    # Rule 2: Massive Changes
    if "changed" in stats:
        # Extract numbers roughly
        import re
        nums = [int(s) for s in re.findall(r'\d+', stats)]
        if nums and max(nums) > 100:
            roasts.append(f"{max(nums)} lines changed? Reviewing this will be painful.")
            
    # Rule 3: Deletions > Insertions
    if "deletion" in stats and "insertion" not in stats:
         roasts.append("Deleting code? Finally contributing something of value.")

    # Default Roast
    if not roasts:
        roasts.append("Their logic is holding on by a thread, but it compiles.")

    final_roast = random.choice(roasts)
    utils.print_warning(f"Verdict: {final_roast}")