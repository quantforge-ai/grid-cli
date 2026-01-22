import requests
import subprocess
from grid.core import utils

# YOUR LIVE BRAIN
BRAIN_URL = "https://grid-cli.vercel.app/api" 

def get_git_remote():
    """Extracts the unique GitHub URL to use as Project ID."""
    try:
        url = subprocess.check_output(["git", "remote", "get-url", "origin"], stderr=subprocess.DEVNULL).decode().strip()
        # Clean URL: git@github.com:User/Repo.git -> https://github.com/User/Repo
        if url.startswith("git@"):
            url = url.replace(":", "/").replace("git@", "https://")
        if url.endswith(".git"):
            url = url[:-4]
        return url
    except:
        return None

def register_project(config_data):
    """Lead: Pushes .grid config to Cloud Brain."""
    project_id = config_data.get("id")
    if not project_id:
        utils.print_error("Invalid config: missing project ID.")
        return False

    payload = {
        "project_id": project_id, 
        "config": config_data
    }
    
    try:
        resp = requests.post(f"{BRAIN_URL}/register", json=payload, timeout=10)
        # Handle non-200 or non-JSON responses
        if resp.status_code != 200:
            return False
        return True
    except (requests.exceptions.RequestException, ValueError):
        utils.print_error("Brain Link Severed: Cloud is unresponsive.")
        return False
    except Exception as e:
        utils.print_error(f"Neural Glitch: {e}")
        return False

def fetch_project_config(project_id):
    """Dev: Downloads config using Project ID as key."""
    try:
        resp = requests.get(f"{BRAIN_URL}/connect", params={"project_id": project_id}, timeout=10)
        
        # Guard against HTML error pages or down server
        if resp.status_code != 200:
            return None
            
        return resp.json()
    except (requests.exceptions.RequestException, ValueError):
        # ValueError catches the "Expecting value..." JSON error
        return None
    except Exception:
        return None