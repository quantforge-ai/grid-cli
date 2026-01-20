import subprocess
from grid.core import utils, scraper

def run():
    utils.print_header("Initiating Uplink...")

    # 1. Check for Blunder Logs (Did we catch a secret earlier?)
    # If the secret sniffer ran, it might have unstaged files.
    # We assume 'grid submit' handled the commit.
    
    # 2. Push
    try:
        utils.spin_action("Pushing to Origin", lambda: subprocess.run(["git", "push"], check=True))
        utils.print_success("Code deployed.")
        
        # 3. TRIGGER THE SCRAPER (The Cycle continues)
        # Every push updates the wit database for the NEXT roast
        utils.print_header("Syncing Wit Database...")
        scraper.update_wit() 
        
    except subprocess.CalledProcessError:
        utils.print_error("Push failed. Resolve your conflicts manually.")