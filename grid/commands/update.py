import sys
import subprocess
import webbrowser
import requests
from grid.core import utils

# Your Repo URL
REPO_URL = "https://github.com/quantforge-ai/grid-cli.git"
VERSION_URL = "https://raw.githubusercontent.com/quantforge-ai/grid-cli/main/setup.py"
RELEASES_URL = "https://github.com/quantforge-ai/grid-cli/releases/latest"

CURRENT_VERSION = "1.0.0"  # Update this when releasing new versions

def check_remote_version():
    """Scrapes setup.py from GitHub to find the latest version string."""
    try:
        r = requests.get(VERSION_URL, timeout=5)
        if r.status_code == 200:
            for line in r.text.splitlines():
                if "version=" in line:
                    # Extract '1.0.1' from version='1.0.1',
                    version = line.split('=')[1].strip().strip("',\"")
                    return version
    except:
        return None
    return None

def run():
    """The Update Logic."""
    utils.print_header("INITIATING SELF-UPDATE SEQUENCE")
    
    # 1. Check for new version
    utils.print_info(f"Current Version: {CURRENT_VERSION}")
    
    latest_ver = check_remote_version()
    if latest_ver:
        utils.print_info(f"Latest Version:  {latest_ver}")
        
        if latest_ver == CURRENT_VERSION:
            utils.print_success("You are running the latest version. No update needed.")
            return
    else:
        utils.print_warning("Could not check remote version. Proceeding with update anyway...")
    
    # 2. Update Logic
    # CHECK: Is this running as a Python script (pip) or Frozen Exe?
    if getattr(sys, 'frozen', False):
        # --- EXE USER ---
        # We cannot auto-update a running .exe file easily (Windows locks it).
        # Best practice: Notify and open download link.
        utils.print_warning("Binary detected. Cannot self-patch.")
        utils.print_success("Opening download portal...")
        webbrowser.open(RELEASES_URL)
        utils.print_info("\n>> Download the latest installer and run it.")
        utils.print_info(">> The new version will overwrite this one automatically.")
        
    else:
        # --- PIP/DEV USER ---
        # We can just run the pip command again!
        utils.print_warning("Downloading latest neural patterns from Cloud...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--upgrade", f"git+{REPO_URL}"
            ])
            utils.print_success("✅ ASSIMILATION COMPLETE.")
            utils.print_success(">> Restart your terminal to use the new version.")
        except subprocess.CalledProcessError:
            utils.print_error("Update failed. Try manually:")
            utils.print_info(f"pip install --upgrade git+{REPO_URL}")
