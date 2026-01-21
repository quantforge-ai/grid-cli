import click
from rich.console import Console
from grid.commands import dev as cmd_dev
from grid.commands import push as cmd_push
from grid.commands import roast as cmd_roast
from grid.commands import status as cmd_status
from grid.commands import init as cmd_init
from grid.commands import blame as cmd_blame
from grid.commands import purge as cmd_purge
from grid.commands import recap as cmd_recap
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
    """
    Onboards a developer. Clones repo & syncs config.
    Usage: grid dev https://github.com/user/repo Tanishq
    """
    cmd_dev.run(repo_url, dev_name)

@main.command()
@click.argument('message', required=False)
def push(message):
    """
    Safe Push. Auto-stages, Checks Secrets, Handles Cowboy Mode.
    Usage: grid push "fixing bug"
    """
    cmd_push.run(message)

@main.command()
@click.argument('target', required=False)
@click.option('--share', '-s', is_flag=True, help='Broadcast to Team')
@click.option('-dev', '--developer', help='Roast a colleague')
def roast(target, share, developer):
    """
    Analyzes code or roasts a colleague.
    """
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
def cloud():
    """(Lead) Manually syncs local .grid to Cloud Brain."""
    cfg = config.load_project_config()
    if cfg:
        if cloud.register_project(cfg):
            utils.print_success("Config synced to Cloud.")
        else:
            utils.print_error("Sync failed.")
    else:
        utils.print_error("No .grid file found. Run 'grid init' first.")

@main.command()
@click.argument('name')
def auth(name):
    """Sets your local identity."""
    config.set_global_identity(name)
    utils.print_success(f"Identity updated: {name}")

@main.command()
def status():
    """System Diagnostics."""
    cmd_status.run()

@main.command()
@click.argument('target')
@click.argument('line')
@click.option('--share', '-s', is_flag=True, help='Broadcast shame to team')
def blame(target, line, share):
    """
    Finds out who wrote a specific line of code.
    Usage: grid blame main.py 42
    """
    cmd_blame.run(target, line, share)

@main.command()
def purge():
    """
    Deletes local branches that have been merged.
    """
    cmd_purge.run()

@main.command()
def recap():
    """
    Generates a corporate-speak summary of yesterday's work.
    """
    cmd_recap.run()

if __name__ == '__main__':
    main()