from grid.core import utils, config

def run(name):
    utils.print_header("IDENTITY CONFIGURATION")
    
    # Save to ~/.grid_identity
    config.set_global_identity(name)
    
    utils.print_success(f"Identity updated to: [bold cyan]{name}[/]")
    utils.print_warning("This name will be used for Multiplayer Roasts and Cowboy commits.")