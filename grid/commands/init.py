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
        "banned_files": [".env", ".pem", "credentials.json", "secrets.json", ".key", "*.p12"]
    }
    
    config.save_project_config(template)
    
    # Update .gitignore to prevent accidental commits
    _update_gitignore()
    
    utils.print_success(f"✨ Created .grid configuration file")
    utils.print_info(f"Project ID: {project_id}")
    if repo_url:
        utils.print_info(f"Repository: {repo_url}")
    utils.print_success("✅ Updated .gitignore to protect sensitive files")
    utils.print_info("\n📝 Next steps:")
    utils.print_info("   1. Open .grid and configure your project settings")
    utils.print_info("   2. Add your team webhook URL (optional)")
    utils.print_info("   3. Run 'grid push' to register with Cloud Brain")
    utils.print_info("   4. Teammates can use 'grid dev' to sync config")

def _update_gitignore():
    """Adds .grid and common secret files to .gitignore"""
    gitignore_path = ".gitignore"
    
    # Files/patterns to protect
    protected_patterns = [
        "",  # Empty line for spacing
        "# Grid CLI - Sensitive Configuration",
        ".grid",
        ".grid_identity",
        "",
        "# Common Secret Files",
        ".env",
        ".env.*",
        "*.pem",
        "*.key",
        "*.p12",
        "credentials.json",
        "secrets.json",
        "config.json",
    ]
    
    # Read existing .gitignore if it exists
    existing_lines = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            existing_lines = [line.rstrip() for line in f.readlines()]
    
    # Add only missing patterns
    lines_to_add = []
    for pattern in protected_patterns:
        if pattern and pattern not in existing_lines and not pattern.startswith("#"):
            lines_to_add.append(pattern)
    
    if lines_to_add:
        # Add header if first time
        if ".grid" in lines_to_add and "# Grid CLI" not in "\n".join(existing_lines):
            existing_lines.extend(["", "# Grid CLI - Sensitive Configuration"])
        
        existing_lines.extend(lines_to_add)
        
        # Write back
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(existing_lines) + '\n')