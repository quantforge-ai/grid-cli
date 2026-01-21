import os
import json
import subprocess
from grid.core import utils, config, scraper

TEMP_COMPOSE_FILE = ".grid_docker_compose.yml"

def check_docker():
    """Checks if Docker is running."""
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, check=True)
        return True
    except:
        utils.print_error("Docker is not installed or not running.")
        return False

def generate_compose_from_grid():
    """Reads .grid and creates a temporary docker-compose.yml"""
    cfg = config.load_project_config()
    
    if not cfg or "services" not in cfg:
        return False

    try:
        import yaml
    except ImportError:
        utils.print_error("PyYAML not installed. Run: pip install pyyaml")
        return False

    # Convert Grid JSON to Docker Compose YAML format
    compose_data = {
        "version": "3.8",
        "services": cfg["services"]
    }

    try:
        with open(TEMP_COMPOSE_FILE, "w") as f:
            yaml.dump(compose_data, f, default_flow_style=False)
        utils.print_success(f"Generated {TEMP_COMPOSE_FILE} from .grid config")
        return True
    except Exception as e:
        utils.print_error(f"Failed to generate docker config: {e}")
        return False

def run_docker_cmd(args):
    """Runs docker-compose with the correct file."""
    # Priority 1: standard docker-compose.yml
    if os.path.exists("docker-compose.yml"):
        file_arg = []
        utils.print_warning("Using existing docker-compose.yml")
    # Priority 2: Grid-generated config
    elif os.path.exists(TEMP_COMPOSE_FILE):
        file_arg = ["-f", TEMP_COMPOSE_FILE]
    # Priority 3: Try generating it now
    elif generate_compose_from_grid():
        file_arg = ["-f", TEMP_COMPOSE_FILE]
    else:
        utils.print_error("No docker-compose.yml found and no 'services' in .grid file.")
        return False

    try:
        subprocess.run(["docker-compose"] + file_arg + args, check=True)
        return True
    except subprocess.CalledProcessError:
        utils.print_error("Docker command failed.")
        return False
    except FileNotFoundError:
        utils.print_error("docker-compose is not installed or not in PATH.")
        return False

def up(detach):
    if not check_docker(): return
    utils.print_header("SPINNING UP GRID INFRASTRUCTURE")
    
    args = ["up"]
    if detach: args.append("-d")

    if run_docker_cmd(args):
        if detach:
            utils.print_success("Services are running in the background (Silent Mode).")
    else:
        utils.print_error("Failed to start services.")

def down():
    if not check_docker(): return
    utils.print_header("SHUTTING DOWN GRID INFRASTRUCTURE")
    
    run_docker_cmd(["down"])
    
    # Cleanup the temp file to keep folder clean
    if os.path.exists(TEMP_COMPOSE_FILE):
        os.remove(TEMP_COMPOSE_FILE)
        utils.print_success("Cleaned up temporary docker config.")
    
    utils.print_success("Infrastructure offline.")

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
    utils.print_header("CONTAINER STATUS")
    subprocess.run(["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"])