import click
from rich.console import Console
from rich.panel import Panel
from grid.commands import roast as cmd_roast
from grid.commands import submit as cmd_submit
from grid.commands import push as cmd_push
from grid.commands import status as cmd_status
from grid.core import utils

console = Console()

# --- THE FIX: We name this function 'main' to match the error's expectation ---
@click.group()
def main():
    """
    GRID CLI v1.0 | The Sentient Developer Companion.
    """
    pass

@main.command()
@click.argument('target', required=False)
@click.option('-dev', '--developer', help='Target a specific colleague (PvP Mode)')
@click.option('--recent', is_flag=True, help='Roast their most recent commit')
def roast(target, developer, recent):
    if developer:
        cmd_roast.roast_developer(developer, recent)
    elif target:
        cmd_roast.roast_file(target)
    else:
        cmd_roast.roast_project()

@main.command()
@click.argument('message')
def submit(message):
    cmd_submit.run(message)

@main.command()
def push():
    cmd_push.run()

@main.command()
def status():
    cmd_status.run()

@main.command()
def init():
    console.print(Panel.fit("[bold green]Assimilation Complete.[/]\nGrid is now watching this repository.", title="GRID v1.0"))

if __name__ == '__main__':
    main()