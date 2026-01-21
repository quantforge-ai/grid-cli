import subprocess
from grid.core import utils, git_police

def run(clean):
    utils.print_header("RETURNING TO BASE")

    # 1. Identify "Home" (main or master)
    try:
        branches = subprocess.check_output(["git", "branch"], stderr=subprocess.DEVNULL).decode()
    except:
        utils.print_error("Not a git repository.")
        return

    target = "main" if "main" in branches else "master"
    current = git_police.get_current_branch()

    if current == target:
        utils.print_warning(f"You are already on {target}.")
        return

    # 2. Switch
    utils.spin_action(f"Switching to {target}...", 
        lambda: subprocess.run(["git", "checkout", target], check=True))
    
    # 3. Update
    utils.spin_action("Pulling latest updates...", 
        lambda: subprocess.run(["git", "pull"], check=True))

    utils.print_success(f"Welcome home. You are now on [bold]{target}[/].")

    # 4. Cleanup (Optional)
    if clean and current.startswith("cowboy/"):
        if utils.confirm(f"Delete the local branch '{current}'?"):
            subprocess.run(["git", "branch", "-D", current])
            utils.print_success("Cowboy evidence destroyed.")