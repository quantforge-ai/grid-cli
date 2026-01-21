import requests
import json
from grid.core import utils

# Replace with your actual Vercel URL
BRAIN_URL = "https://your-grid-brain.vercel.app/api" 

def register_project(repo_url, config_data):
    """
    Lead: Uploads the .grid config to the cloud.
    """
    payload = {
        "project_id": repo_url, # Unqiue ID
        "config": config_data   # Contains Webhook, Secret Patterns, etc.
    }
    try:
        resp = requests.post(f"{BRAIN_URL}/register", json=payload)
        return resp.status_code == 200
    except:
        return False

def fetch_project_config(repo_url):
    """
    Dev: Downloads config. No password needed.
    """
    try:
        resp = requests.get(f"{BRAIN_URL}/connect", params={"project_id": repo_url})
        if resp.status_code == 200:
            return resp.json() # Returns the .grid content
        return None
    except:
        return None