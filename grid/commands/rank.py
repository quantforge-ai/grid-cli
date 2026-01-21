import subprocess
from rich.table import Table
from grid.core import utils

def run():
    utils.print_header("GRID LEADERBOARD (HALL OF SHAME)")
    
    # 1. Fetch all remote branches
    try:
        # git ls-remote returns list of refs
        raw = subprocess.check_output(["git", "ls-remote", "--heads", "origin"], stderr=subprocess.DEVNULL).decode()
    except:
        utils.print_error("Could not fetch remote stats (Are you online?).")
        return

    # 2. Count Cowboy Incidents
    # Format of line: "hash\trefs/heads/cowboy/tanishq/fix-bug"
    scores = {}
    
    for line in raw.splitlines():
        if "cowboy/" in line:
            parts = line.split("/")
            # refs/heads/cowboy/{user}/{msg}/{slug}
            # Index: 0/1/2/3/4/5
            try:
                # part[3] is the user name (e.g., tanishq)
                user = parts[3].capitalize()
                scores[user] = scores.get(user, 0) + 1
            except:
                continue

    if not scores:
        utils.print_success("No cowboy branches detected. This team is... surprisingly professional.")
        return

    # 3. Display Table
    table = Table(title="Recklessness Ranking", show_lines=True)
    table.add_column("Rank", justify="center", style="bold")
    table.add_column("Developer", style="cyan")
    table.add_column("Cowboy Incidents", justify="right", style="red")
    table.add_column("Title", justify="center")

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    for i, (user, count) in enumerate(sorted_scores, 1):
        if i == 1:
            title = "🤠 Sheriff of Chaos"
        elif i == 2:
            title = "🐴 Deputy Danger"
        else:
            title = "Village Idiot"
            
        table.add_row(f"#{i}", user, str(count), title)

    utils.console.print(table)
    utils.print_warning("Stats are based on active 'cowboy/' branches on origin.")