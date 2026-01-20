import os
import threading
from grid.core import git_police, scraper, utils

def run():
    # 1. Wrapper Data
    branch = git_police.get_current_branch()
    clean = git_police.is_clean()
    
    # 2. Logic Data
    danger = "LOW"
    if branch in ["main", "master"] and not clean:
        danger = "[bold red]CRITICAL (Cowboy Risk)[/]"
    
    # 3. Render
    utils.print_dashboard({
        "System": "Grid CLI v1.0",
        "Identity": os.environ.get("USERNAME", "Unknown"),
        "Branch": branch,
        "Status": "Clean" if clean else "Dirty",
        "Risk Level": danger
    })

    # 4. Background Update
    # Checks if DB needs update without blocking user
    t = threading.Thread(target=scraper.update_wit)
    t.daemon = True
    t.start()