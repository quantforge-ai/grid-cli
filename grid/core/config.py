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
            with open(PROJECT_CONFIG, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def save_project_config(data):
    """Saves project settings to .grid."""
    with open(PROJECT_CONFIG, "w") as f:
        json.dump(data, f, indent=4)

def set_global_identity(name):
    """Saves 'Tanishq' to ~/.grid_identity."""
    try:
        with open(GLOBAL_ID_FILE, "w") as f:
            json.dump({"name": name}, f)
    except Exception as e:
        print(f"Warning: Could not save identity: {e}")

def get_global_identity():
    """Returns 'Tanishq' or 'Stranger'."""
    if os.path.exists(GLOBAL_ID_FILE):
        try:
            with open(GLOBAL_ID_FILE, "r") as f:
                data = json.load(f)
                return data.get("name", "Stranger")
        except:
            pass
    return "Stranger"