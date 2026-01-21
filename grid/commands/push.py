import subprocess
import random
from grid.core import utils, git_police, scraper, config

def get_dynamic_slug():
    """Fetches a short 2-4 word roast for branch names."""
    try:
        # We grab a full roast but truncate it to 4 words for the branch name
        full_roast = scraper.get_random_roast("roasts")
        words = full_roast.split()
        # Take 3-4 random words from the middle to make it sound chaotic
        slug_words = words[:4] if len(words) >= 4 else words
        return "-".join(slug_words).lower().replace(".", "").replace("!", "")
    except:
        return "clown-behavior"

def run(message):
    utils.print_header("INITIATING PUSH SEQUENCE")

    # 1. AUTO-STAGE
    subprocess.run(["git", "add", "."])

    # 2. SECRET SCAN (The "Guard Dog" Phase)
    cfg = config.load_project_config()
    banned_files = cfg.get("banned_files", []) if cfg else [".env"]
    
    leaks = git_police.scan_for_secrets(custom_patterns=banned_files)
    
    if leaks:
        # SASSY ERROR: Private roast for being careless
        roast = scraper.get_random_roast("secrets")
        utils.print_error(f"PUSH BLOCKED. {roast}")
        utils.print_warning(f"Restricted files detected: {leaks}")
        
        # Unstage them to save the dev
        subprocess.run(["git", "restore", "--staged"] + leaks)
        return

    # 3. COWBOY PROTOCOL (The "Safety Net" Phase)
    current_branch = git_police.get_current_branch()
    dev_name = config.get_global_identity()
    
    if current_branch in ["main", "master", "dev", "production"]:
        # SASSY WARNING: Private roast for being reckless
        roast = scraper.get_random_roast("cowboy_shame")
        utils.print_warning(f"COWBOY DETECTED. {roast}")
        
        # Dynamic Branch Naming
        slug = get_dynamic_slug() # <--- NOW DYNAMIC
        clean_msg = "".join(c if c.isalnum() else "-" for c in (message or "update")[:15]).lower()
        safe_branch = f"cowboy/{dev_name}/{clean_msg}/{slug}"
        
        utils.print_header(f"Taking the wheel... Moving to safety.")
        
        try:
            subprocess.run(["git", "checkout", "-b", safe_branch], check=True)
            utils.print_success(f"Created Branch: {safe_branch}")
        except:
            utils.print_error("Emergency branching failed. You are on your own.")
            return

    # 4. COMMIT & PUSH
    if not message: message = "grid auto-push"
    subprocess.run(["git", "commit", "-m", message])
    
    utils.spin_action("Pushing to Origin...", 
        lambda: subprocess.run(["git", "push", "--set-upstream", "origin", git_police.get_current_branch()]))

    # 5. THE REWARD (Compliment if successful)
    # If we made it here without errors or cowboy mode, give a compliment
    if current_branch not in ["main", "master"]:
        compliment = scraper.get_random_roast("compliments")
        utils.print_success(f"Code is live. {compliment}")

    # 6. TRIGGER WIT ENGINE
    scraper.trigger_background_update()