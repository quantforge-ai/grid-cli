import json
import os
from pathlib import Path

# Project-level config (lives in repo root)
PROJECT_CONFIG = ".grid"

# Global identity (lives in user's home folder)
GLOBAL_ID_FILE = os.path.join(str(Path.home()), ".grid_identity")

def load_project_config():
    """Loads the .grid file from the current directory."""
    if os.path.exists(PROJECT_CONFIG):
        try:
            if os.path.getsize(PROJECT_CONFIG) == 0:
                return None
            with open(PROJECT_CONFIG, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError, Exception):
            return None
    return None

def save_project_config(data):
    """Saves project settings to .grid."""
    with open(PROJECT_CONFIG, "w") as f:
        json.dump(data, f, indent=4)

def set_global_identity(name):
    """Saves identity to ~/.grid_identity."""
    try:
        with open(GLOBAL_ID_FILE, "w") as f:
            json.dump({"name": name}, f)
    except Exception as e:
        print(f"Warning: Could not save identity: {e}")

def get_global_identity():
    """Returns the registered name or 'Stranger'."""
    if os.path.exists(GLOBAL_ID_FILE):
        try:
            if os.path.getsize(GLOBAL_ID_FILE) == 0:
                return "Stranger"
            with open(GLOBAL_ID_FILE, "r") as f:
                data = json.load(f)
                return data.get("name", "Stranger")
        except (json.JSONDecodeError, ValueError, Exception):
            return "Stranger"
    return "Stranger"