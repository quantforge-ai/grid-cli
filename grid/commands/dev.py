import os
import subprocess
import click
import sys
from grid.core import utils, cloud, config

def run(repo_url, dev_name):
    utils.print_header(f"ONBOARDING AGENT: {dev_name}")

    config.set_global_identity(dev_name)
    utils.print_success(f"Identity set to: [bold cyan]{dev_name}[/]")

    folder_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    
    if os.path.exists(folder_name):
        utils.print_warning(f"Folder '{folder_name}' exists. Skipping clone.")
    else:
        utils.spin_action(f"Cloning {folder_name}...", 
            lambda: subprocess.run(["git", "clone", repo_url], check=True))
        utils.print_success("Repository cloned.")

    target_path = os.path.abspath(folder_name)
    
    # Change into the cloned directory for environment setup
    os.chdir(target_path)

    # --- ENVIRONMENT SETUP ---
    utils.print_header("Initializing Development Environment...")
    
    # 1. Create Venv
    if not os.path.exists("venv"):
        utils.spin_action("Creating virtual environment...", 
            lambda: subprocess.run([sys.executable, "-m", "venv", "venv"], check=True))
        utils.print_success("Virtual environment created.")
    else:
        utils.print_info("Venv already exists. Skipping creation.")

    # 2. Install Dependencies
    if os.path.exists("requirements.txt"):
        utils.print_info("Found requirements.txt. Installing dependencies...")
        
        # Dynamic path to venv python/pip
        if os.name == 'nt':
            pip_path = os.path.join("venv", "Scripts", "pip")
        else:
            pip_path = os.path.join("venv", "bin", "pip")
        
        try:
            utils.spin_action("Upgrading pip & installing dependencies...", 
                lambda: subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True) or 
                        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True))
            utils.print_success("All dependencies installed successfully.")
        except Exception as e:
            utils.print_error(f"Failed to install dependencies: {e}")
    else:
        utils.print_warning("No requirements.txt found. Skipping dependency installation.")

    # --- CLOUD SYNC ---
    utils.print_header("Syncing with Cloud Brain...")
    # Refresh repo_url in case it was modified during chdir (it shouldn't be, but good practice)
    project_config = cloud.fetch_project_config(repo_url)
    
    if project_config:
        config.save_project_config(project_config)
        utils.print_success("Secrets & Webhooks downloaded.")
        utils.print_success(f"\n[bold green]ONBOARDING COMPLETE.[/]\n>> Run: cd {folder_name} && source venv/bin/activate (or venv\\Scripts\\activate on Windows)")
    else:
        utils.print_warning(f"No cloud config found for {repo_url}.\n(Ask your Lead to run 'grid init' inside the project).")