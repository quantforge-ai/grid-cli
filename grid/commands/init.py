import click
from grid.core import utils, config, cloud

def run():
    utils.print_header("INITIALIZING GRID PROJECT")
    
    # Check if git exists
    repo_id = cloud.get_git_remote()
    if not repo_id:
        utils.print_error("This folder is not a git repository. Run 'git init' first.")
        return

    # Gather Data
    project_name = click.prompt(">> Project Name", default=repo_id.split("/")[-1])
    webhook = click.prompt(">> Team Webhook URL (Discord/Slack)")
    
    click.echo(">> Enter filenames to BAN (comma separated). E.g. .env, secrets.json")
    secrets = click.prompt(">> Banned Files", default=".env, .pem, credentials.json")
    secret_list = [s.strip() for s in secrets.split(",")]

    # Create Data Structure
    data = {
        "id": repo_id,
        "name": project_name,
        "webhook": webhook,
        "banned_files": secret_list
    }

    # Save Locally
    config.save_project_config(data)
    utils.print_success(f"Generated .grid file for '{project_name}'.")
    
    # Prompt to Cloud Sync
    if click.confirm("Do you want to push this config to the Cloud Brain now?"):
        if cloud.register_project(data):
            utils.print_success("Project registered in Cloud. Teammates can now use 'grid dev'.")
        else:
            utils.print_error("Cloud upload failed (Server offline?). You can try 'grid cloud' later.")