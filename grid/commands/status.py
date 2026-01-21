from grid.core import utils, config, git_police, cloud

def run():
    utils.print_header("GRID SYSTEM DIAGNOSTICS")
    
    identity = config.get_global_identity()
    project_cfg = config.load_project_config()
    repo_id = cloud.get_git_remote()
    branch = git_police.get_current_branch()
    
    project_name = project_cfg.get("name", "Unknown (Run 'grid init')") if project_cfg else "No Config Found"
    webhook_status = "Active" if project_cfg and project_cfg.get("webhook") else "Inactive"
    
    dashboard = {
        "Identity": identity,
        "Project": project_name,
        "Repo ID": repo_id or "Not a git repo",
        "Branch": branch,
        "Multiplayer": webhook_status
    }
    
    utils.print_dashboard(dashboard)