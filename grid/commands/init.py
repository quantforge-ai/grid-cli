import os
from datetime import datetime
from grid.core import utils, config, cloud

def run():
    utils.print_header("INITIALIZING GRID PROJECT")
    
    # Check if .grid already exists
    if os.path.exists(".grid"):
        utils.print_error(".grid file already exists. Delete it first if you want to reinitialize.")
        return
    
    # Generate unique project ID: QG/DDMMMYYYY/project-name
    project_name = os.path.basename(os.getcwd())
    date_stamp = datetime.now().strftime("%d%b%Y")  # e.g., 22Jan2026
    project_id = f"QG/{date_stamp}/{project_name}"
    
    # Get GitHub URL from git remote
    repo_url = cloud.get_git_remote() or ""
    
    # Create template .grid file
    template = {
        "id": project_id,
        "name": project_name,
        "repo_url": repo_url,
        "webhook": "",  # Lead will fill this in manually
        "banned_files": [".env", ".pem", "credentials.json"]
    }
    
    config.save_project_config(template)
    
    utils.print_success(f"✨ Created .grid configuration file")
    utils.print_info(f"Project ID: {project_id}")
    if repo_url:
        utils.print_info(f"Repository: {repo_url}")
    utils.print_info("\n📝 Next steps:")
    utils.print_info("   1. Open .grid and configure your project settings")
    utils.print_info("   2. Add your team webhook URL (optional)")
    utils.print_info("   3. Run 'grid push' to register with Cloud Brain")
    utils.print_info("   4. Teammates can use 'grid dev' to sync config")