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
    if stats['score'] < 7:
        verdict = scraper.get_random_roast("roasts")
        color = "red"
    else:
        verdict = scraper.get_random_roast("compliments")
        color = "green"

    # 3. Print Report
    report_text = f"[bold]Complexity Score:[/][{color}] {stats['score']}/10[/]\n"
    report_text += f"[bold]Verdict:[/][{color}] {verdict}[/]"
    
    # 4. Secret Warning
    if stats['metrics'].get("secrets", 0) > 0:
        report_text += f"\n\n[bold red blink]⚠️  CONTAMINANT ALERT: {stats['metrics']['secrets']} Hardcoded Secrets Detected![/]"
    
    utils.print_panel(
        report_text,
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
    
    if avg < 7:
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
    touched_files = git_police.get_last_commit_files(target_name)
    
    if not commit_msg or commit_msg == "Unknown Commit":
        utils.print_error(f"No recent commits found for {target_name}.")
        return

    # 3. Aggregate Score for Touched Files
    commit_scores = []
    for f in touched_files:
        if os.path.exists(f) and f.endswith(".py"):
            try:
                stats = analyzer.analyze_file(f)
                commit_scores.append(stats['score'])
            except:
                continue
    
    avg_score = sum(commit_scores) / len(commit_scores) if commit_scores else 0
    
    # 4. Generate Roast
    roast = scraper.get_random_roast("roasts")

    # 5. Format display elements
    if touched_files:
        files_str = "\n[bold]Files Touched:[/bold]\n" + "\n".join([f" • {f}" for f in touched_files[:3]])
        if len(touched_files) > 3:
            files_str += f"\n ... and {len(touched_files)-3} more"
    else:
        files_str = ""

    score_str = f"\n[bold]Commit Integrity:[/bold] [red]{avg_score:.1f}/10[/]" if commit_scores else "\n[bold]Commit Integrity:[/bold] [dim]N/A (No Code Found)[/]"

    # 6. Display
    utils.print_panel(
        f"[bold]Last Commit:[/bold] \"{commit_msg}\""
        f"{files_str}"
        f"{score_str}\n\n"
        f"[bold red]Grid says:[/bold red] {roast}",
        title=f"Roasting {target_name}"
    )

    # 7. Share to Discord (PvP Mode)
    if share:
        utils.spin_action("Broadcasting to Team Channel...", 
            lambda: broadcaster.broadcast_roast(identity, target_name, commit_msg, roast, is_clean=False))
        utils.print_success("Roast sent to Discord.")