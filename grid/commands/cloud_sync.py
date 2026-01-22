from grid.core import utils, config, cloud

def run():
    utils.print_header("SYNCING TO CLOUD BRAIN")
    
    # Load local .grid config
    project_config = config.load_project_config()
    
    if not project_config:
        utils.print_error("No .grid file found. Run 'grid init' first.")
        return
    
    project_id = project_config.get("id")
    if not project_id:
        utils.print_error("Invalid .grid file: missing project ID.")
        return
    
    utils.print_info(f"Project ID: {project_id}")
    utils.print_info(f"Uploading configuration...")
    
    # Upload to cloud
    if cloud.register_project(project_config):
        utils.print_success("✅ Configuration synced to Cloud Brain!")
        utils.print_info("\nℹ️  Teammates can now run:")
        utils.print_info(f"   grid dev {project_config.get('repo_url', 'REPO_URL')}")
    else:
        utils.print_error("❌ Cloud sync failed. Check your connection.")
