from grid.core import utils, config, git_police, cloud

def run():
    utils.print_header("GRID SYSTEM DIAGNOSTICS")
    
    # Gather Info
    identity = config.get_global_identity()
    project_cfg = config.load_project_config()
    repo_id = cloud.get_git_remote()
    branch = git_police.get_current_branch()
    
    # Determine Status
    project_name = project_cfg.get("name", "Unknown (Run 'grid init')") if project_cfg else "No Config Found"
    webhook_status = "[green]Active[/]" if project_cfg and project_cfg.get("webhook") else "[red]Inactive[/]"
    
    # Build Dashboard Dictionary
    dashboard = {
        "Agent Identity": identity,
        "Project Name": project_name,
        "Repo Connection": repo_id or "Not a git repo",
        "Current Branch": branch,
        "Cloud Uplink": webhook_status
    }
    
    utils.print_dashboard(dashboard)