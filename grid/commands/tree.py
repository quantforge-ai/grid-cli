import os
from rich.tree import Tree
from grid.core import utils

def run():
    utils.print_header("PROJECT TOPOGRAPHY")
    
    root_name = os.path.basename(os.getcwd())
    tree = Tree(f"[bold cyan]📂 {root_name}[/]")
    
    def add_to_tree(path, tree_node):
        try:
            # Sort: Directories first, then files
            items = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x))
            
            for item in items:
                # Ignore hidden/system files
                if item.startswith(".") or item in ["__pycache__", "venv", "node_modules", "dist", "build", "grid.egg-info"]:
                    continue
                    
                full_path = os.path.join(path, item)
                
                if os.path.isdir(full_path):
                    branch = tree_node.add(f"[bold blue]📂 {item}[/]")
                    add_to_tree(full_path, branch)
                else:
                    # Icons based on file type
                    if item.endswith(".py"):
                        icon = "🐍"
                        style = "green"
                    elif item.endswith(".json") or item.endswith(".yaml") or item.endswith(".grid"):
                        icon = "⚙️ "
                        style = "yellow"
                    elif item.endswith(".md") or item.endswith(".txt"):
                        icon = "📄"
                        style = "white"
                    else:
                        icon = "💾"
                        style = "dim"
                        
                    tree_node.add(f"[{style}]{icon} {item}[/]")
        except PermissionError:
            pass

    add_to_tree(".", tree)
    utils.console.print(tree)