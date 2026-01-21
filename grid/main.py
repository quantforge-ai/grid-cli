import click
from rich.console import Console
from grid.commands import dev as cmd_dev
from grid.commands import push as cmd_push
from grid.commands import roast as cmd_roast
from grid.commands import status as cmd_status
from grid.commands import init as cmd_init
from grid.commands import auth as cmd_auth
from grid.commands import blame as cmd_blame
from grid.commands import purge as cmd_purge
from grid.commands import recap as cmd_recap
from grid.commands import home as cmd_home
from grid.commands import docker as cmd_docker
from grid.commands import branch as cmd_branch
from grid.commands import tree as cmd_tree
from grid.commands import rank as cmd_rank
from grid.core import config, cloud, utils

console = Console()

@click.group()
def main():
    """GRID CLI | The Sentient Developer Companion"""
    pass

@main.command()
@click.argument('repo_url')
@click.argument('dev_name')
def dev(repo_url, dev_name):
    """Onboards a developer. Usage: grid dev <url> <name>"""
    cmd_dev.run(repo_url, dev_name)

@main.command()
@click.argument('message', required=False)
def push(message):
    """Safe Push. Auto-stages, Checks Secrets, Handles Cowboy Mode."""
    cmd_push.run(message)

@main.command()
@click.argument('target', required=False)
@click.option('--share', '-s', is_flag=True, help='Broadcast to Team')
@click.option('-dev', '--developer', help='Roast a colleague')
def roast(target, share, developer):
    """Analyzes code or roasts a colleague."""
    if developer:
        cmd_roast.roast_developer(developer, recent=True, share=share)
    elif target:
        cmd_roast.roast_file(target)
    else:
        cmd_roast.roast_project()

@main.command()
def init():
    """(Lead) Initializes the .grid config."""
    cmd_init.run()

@main.command()
def cloud_sync():
    """(Lead) Manually syncs local .grid to Cloud Brain."""
    cfg = config.load_project_config()
    if cfg:
        if cloud.register_project(cfg):
            utils.print_success("Config synced to Cloud.")
        else:
            utils.print_error("Sync failed.")
    else:
        utils.print_error("No .grid file found.")

@main.command()
@click.argument('name')
def auth(name):
    """Sets your local identity."""
    cmd_auth.run(name)

@main.command()
def status():
    """System Diagnostics."""
    cmd_status.run()

@main.command()
@click.argument('target')
@click.argument('line')
@click.option('--share', '-s', is_flag=True)
def blame(target, line, share):
    """Finds out who wrote a specific line."""
    cmd_blame.run(target, line, share)

@main.command()
def purge():
    """Deletes merged local branches."""
    cmd_purge.run()

@main.command()
def recap():
    """Generates daily standup report."""
    cmd_recap.run()

@main.command()
@click.option('--clean', is_flag=True, help='Delete the branch you just left')
def home(clean):
    """
    Returns to main/master and pulls latest changes.
    Usage: grid home --clean
    """
    cmd_home.run(clean)

@main.command()
@click.argument('action', type=click.Choice(['up', 'down', 'nuke', 'ps']))
@click.option('-d', '--detach', is_flag=True, help='Run in background')
def docker(action, detach):
    """
    Manages Docker containers with extreme prejudice.
    Actions: up, down, nuke (kill all), ps (status)
    """
    if action == 'up':
        cmd_docker.up(detach)
    elif action == 'down':
        cmd_docker.down()
    elif action == 'nuke':
        cmd_docker.nuke()
    elif action == 'ps':
        cmd_docker.status()

@main.command()
def tree():
    """Visualizes project structure."""
    cmd_tree.run()

@main.command()
def rank():
    """Shows the Cowboy Leaderboard."""
    cmd_rank.run()

@main.command()
@click.argument('name')
def branch(name):
    """
    Smart Switch. Creates a branch if it doesn't exist, switches if it does.
    Usage: grid branch feature/login
    """
    cmd_branch.run(name)

if __name__ == '__main__':
    main()