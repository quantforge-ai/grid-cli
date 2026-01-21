import subprocess
from grid.core import utils, scraper

def check_docker():
    """Checks if Docker is running."""
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, check=True)
        return True
    except:
        utils.print_error("Docker is not installed or not running.")
        return False

def up(detach):
    if not check_docker(): return
    utils.print_header("STARTING ENGINES")
    
    cmd = ["docker-compose", "up"]
    if detach: cmd.append("-d")

    try:
        subprocess.run(cmd)
        if detach:
            utils.print_success("Containers are running in the background (Silent Mode).")
    except:
        utils.print_error("Failed to start. Is docker-compose.yml present?")

def down():
    if not check_docker(): return
    utils.print_header("SHUTTING DOWN")
    subprocess.run(["docker-compose", "down"])
    utils.print_success("Systems offline.")

def nuke():
    """The Nuclear Option: Kills ALL running containers."""
    if not check_docker(): return
    utils.print_header("☢️  INITIATING NUCLEAR CLEANUP ☢️")
    
    # Get all container IDs
    try:
        ids = subprocess.check_output(["docker", "ps", "-q"]).decode().split()
    except:
        ids = []

    if not ids:
        utils.print_warning("No targets found. The battlefield is empty.")
        return

    # KILL THEM ALL
    utils.print_warning(f"Targeting {len(ids)} containers...")
    subprocess.run(["docker", "kill"] + ids)
    subprocess.run(["docker", "rm"] + ids)
    
    roast = scraper.get_random_roast("roasts")
    utils.print_success(f"Tango down. All containers destroyed.\n>> Grid: {roast}")

def status():
    if not check_docker(): return
    subprocess.run(["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"])