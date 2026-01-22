from grid.core import utils, config, git_police, cloud
import os

def run():
    utils.print_header("GRID SYSTEM DIAGNOSTICS")
    
    # 1. Vital Signs
    identity = config.get_global_identity()
    
    # Check Cloud Connection (Safe)
    project_cfg = config.load_project_config()
    project_id = project_cfg.get("id") if project_cfg else None
    neural_link = "[bold green]ONLINE[/]" if project_id and cloud.fetch_project_config(project_id) else "[bold red]SEVERED[/] [dim](Offline Seed Active)[/]"
    
    
    # 2. Target Assimilation
    branch = git_police.get_current_branch()
    project_name = project_cfg.get("name", os.path.basename(os.getcwd())) if project_cfg else "Unknown"
    
    # Construct Sections
    sections = {
        "VITAL SIGNS": {
            "Identity": identity.lower(),
            "Version": "v1.0.0",
            "Neural Link": neural_link,
            "Personality": "[magenta]Stable[/]"
        },
        "TARGET ASSIMILATION": {
            "Repository": project_name,
            "Current Branch": f"[magenta]{branch}[/]",
            "Grid Protocol": "✅ [bold green]ASSIMILATED[/]" if project_cfg else "[yellow]NOT ASSIMILATED[/] [dim](Run 'grid init')[/]"
        }
    }
    
    utils.print_dashboard("GRID DIAGNOSTICS", sections)