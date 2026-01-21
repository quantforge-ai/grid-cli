import os
import subprocess
import click
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
    
    utils.print_header("Syncing with Cloud Brain...")
    project_config = cloud.fetch_project_config(repo_url)
    
    if project_config:
        config_path = os.path.join(target_path, ".grid")
        config.save_project_config(project_config)
        utils.print_success("Secrets & Webhooks downloaded.")
        utils.print_success(f"\n[bold green]SETUP COMPLETE.[/]\n>> Run: cd {folder_name}")
    else:
        utils.print_warning(f"No cloud config found for {repo_url}.\n(Ask your Lead to run 'grid init' inside the project).")