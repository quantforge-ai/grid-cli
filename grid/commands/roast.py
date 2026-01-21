import os
from rich.table import Table
from rich import box
from grid.core import utils, analyzer, scraper, config, broadcaster, git_police

def roast_file(target):
    """Analyzes a single file and roasts it."""
    if not os.path.exists(target):
        utils.print_error(f"File not found: {target}")
        return

    utils.print_header(f"ANALYZING: {target}")
    
    # 1. Get Complexity Stats
    stats = analyzer.analyze_file(target)
    
    # 2. Determine Verdict
    if stats['score'] < 5:
        verdict = scraper.get_random_roast("roasts")
        color = "red"
    else:
        verdict = scraper.get_random_roast("compliments")
        color = "green"

    # 3. Print Report
    utils.print_panel(
        f"[bold]Complexity Score:[/ {color}] {stats['score']}/10\n"
        f"[bold]Verdict:[/ {color}] {verdict}",
        title=f"Roast Report: {target}"
    )

def roast_project():
    """Analyzes the entire directory and lists files in a table."""
    utils.print_header("SCANNING PROJECT SECTOR")
    utils.spin_action("Reading file structure...", lambda: None) # Fake spin for effect

    results = []
    total_score = 0
    file_count = 0

    # 1. Walk the directory
    for root, _, files in os.walk("."):
        # Skip garbage folders
        if any(x in root for x in [".git", "__pycache__", "venv", "node_modules", ".grid", "dist", "build"]):
            continue
            
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                
                # Analyze individual file
                try:
                    stats = analyzer.analyze_file(path)
                    score = stats['score']
                    
                    # Assign Status Icon based on score
                    if score < 5:
                        status = "[bold red]🔥 Toxic[/]"
                    elif score < 8:
                        status = "[yellow]⚠️  Messy[/]"
                    else:
                        status = "[bold green]✅ Clean[/]"
                    
                    results.append((path, score, status))
                    total_score += score
                    file_count += 1
                except:
                    # Skip unreadable files
                    continue

    if file_count == 0:
        utils.print_warning("No Python files found. Is this a real project?")
        return

    # 2. Sort by Score (Worst files at the top so they are visible)
    results.sort(key=lambda x: x[1])

    # 3. Create & Print Table
    table = Table(title="Artifact Analysis Report", box=box.ROUNDED, show_lines=True)
    table.add_column("File Name", style="cyan")
    table.add_column("Integrity", justify="right")
    table.add_column("Status", justify="center")

    for path, score, status in results:
        # Clean up path for display (remove ./ and win style slashes)
        clean_path = path.replace(".\\", "").replace("./", "")
        table.add_row(clean_path, f"{score}/10", status)

    utils.console.print(table)

    # 4. Final Verdict
    avg = total_score / file_count
    utils.print_header(f"AGGREGATE SCORE: {avg:.1f}/10")
    
    if avg < 5:
        verdict = scraper.get_random_roast("roasts")
        color = "red"
    else:
        verdict = scraper.get_random_roast("compliments")
        color = "green"

    utils.print_panel(f"[{color}]\"{verdict}\"[/]", title="Final Verdict")

def roast_developer(target_name, recent, share):
    """Roasts a specific person based on their git history."""
    utils.print_header(f"TARGET ACQUIRED: {target_name}")
    
    # 1. Identify User
    identity = config.get_global_identity()
    
    # 2. Analyze their last commit
    commit_msg = git_police.get_last_commit_message(target_name)
    if not commit_msg or commit_msg == "Unknown Commit":
        utils.print_error(f"No recent commits found for {target_name}.")
        return

    # 3. Generate Roast
    # If roasting yourself, be nicer (maybe). If roasting others, go hard.
    if target_name.lower() == identity.lower():
        roast = scraper.get_random_roast("roasts")
    else:
        roast = scraper.get_random_roast("roasts")

    # 4. Display
    utils.print_panel(
        f"[bold]Last Commit:[/bold] \"{commit_msg}\"\n\n"
        f"[bold red]Grid says:[/bold red] {roast}",
        title=f"Roasting {target_name}"
    )

    # 5. Share to Discord (PvP Mode)
    if share:
        utils.spin_action("Broadcasting to Team Channel...", 
            lambda: broadcaster.broadcast_roast(identity, target_name, commit_msg, roast, is_clean=False))
        utils.print_success("Roast sent to Discord.")