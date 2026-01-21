import subprocess
import os
from grid.core import utils, config, scraper, broadcaster

def run(target, line, share):
    if not os.path.exists(target):
        utils.print_error(f"File {target} not found.")
        return

    # 1. Run Git Blame
    # -L 5,5 means "only line 5"
    try:
        cmd = ["git", "blame", "-L", f"{line},{line}", "--porcelain", target]
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().splitlines()
    except:
        utils.print_error("Could not blame this line. (Is it committed?)")
        return

    # 2. Parse Result
    # Porcelain format gives "author Tanishq" on one line
    author_line = next((l for l in result if l.startswith("author ")), "author Unknown")
    author = author_line.split(" ", 1)[1]

    # 3. The Verdict
    identity = config.get_global_identity()
    
    utils.print_header(f"BLAME INVESTIGATION: {target}:{line}")
    
    if author.lower() == identity.lower():
        # It was YOU
        utils.print_warning(f"Author: [bold yellow]YOU ({author})[/]")
        roast = "You wrote this garbage. Don't look at me."
        utils.print_error(f">> Grid: {roast}")
    else:
        # It was SOMEONE ELSE
        utils.print_error(f"Author: [bold red]{author}[/]")
        roast = scraper.get_random_roast("roasts")
        utils.print_success(f">> Grid: {roast}")

    # 4. Public Shame
    if share:
        broadcaster.broadcast_roast(identity, author, f"Suspect Line {line} in {target}", roast, False)
        utils.print_success("Shame broadcasted to team.")