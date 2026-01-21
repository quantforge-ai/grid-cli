import subprocess
from grid.core import utils, git_police

def run():
    utils.print_header("INITIATING GARBAGE COLLECTION")
    
    # 1. Get Merged Branches
    try:
        raw = subprocess.check_output(["git", "branch", "--merged"], stderr=subprocess.DEVNULL).decode()
    except:
        utils.print_error("Git error.")
        return

    branches = [b.strip().replace("* ", "") for b in raw.splitlines()]
    
    # 2. Filter Protected
    protected = ["main", "master", "dev", "production", git_police.get_current_branch()]
    to_delete = [b for b in branches if b not in protected]
    
    if not to_delete:
        utils.print_success("System is clean. No trash detected.")
        return

    # 3. The Purge
    utils.print_warning(f"Deleting {len(to_delete)} dead branches...")
    
    for branch in to_delete:
        try:
            subprocess.run(["git", "branch", "-d", branch], check=True, stderr=subprocess.DEVNULL)
            print(f"   [x] Deleted '{branch}'")
        except:
            print(f"   [!] Failed to delete '{branch}' (Unmerged changes?)")
            
    utils.print_success("Recycle Bin Emptied.")
