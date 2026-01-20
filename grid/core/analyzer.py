import ast
import os
import random

# Try importing tree-sitter for C++ support (Graceful degradation if missing)
try:
    from tree_sitter import Language, Parser
    TREE_SITTER_READY = True
except ImportError:
    TREE_SITTER_READY = False

# --- THE DIAGNOSIS ENGINE ---
def diagnose(stats):
    """
    Takes raw code metrics and returns a roasting verdict.
    """
    verdicts = []

    # 1. Complexity Roast
    if stats.get("max_nesting", 0) > 4:
        verdicts.append("Your nesting is 5 levels deep. You are mining for Bitcoins, not logic.")
    
    # 2. Length Roast
    if stats.get("long_functions", 0) > 0:
        verdicts.append("You have functions longer than a CVS receipt. Break them down.")

    # 3. Argument Roast
    if stats.get("max_args", 0) > 5:
        verdicts.append("One function takes 6+ arguments. Just pass an object, you monster.")

    # 4. Global Roast
    if stats.get("globals", 0) > 2:
        verdicts.append("Global variables? What is this, 1999?")

    # 5. Bad Practice Roast (Print statements)
    if stats.get("print_statements", 0) > 0:
        verdicts.append("Leftover print statements? Use a debugger.")

    # If code is actually clean
    if not verdicts:
        return "Code structure appears... adequate. I'm watching you."
    
    return random.choice(verdicts)

# --- PYTHON ANALYZER (Built-in AST) ---
class PythonSentinel(ast.NodeVisitor):
    def __init__(self):
        self.stats = {
            "max_nesting": 0,
            "long_functions": 0,
            "max_args": 0,
            "globals": 0,
            "print_statements": 0
        }

    def visit_FunctionDef(self, node):
        # Check Length
        if (node.end_lineno - node.lineno) > 40:
            self.stats["long_functions"] += 1
        
        # Check Args
        if len(node.args.args) > 5:
            self.stats["max_args"] = max(self.stats["max_args"], len(node.args.args))
            
        self.generic_visit(node)

    def visit_Global(self, node):
        self.stats["globals"] += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check for print()
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.stats["print_statements"] += 1
        self.generic_visit(node)

    def visit_For(self, node):
        # Simple nesting check (approximate)
        self.stats["max_nesting"] += 1
        self.generic_visit(node)

def analyze_python(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        sentinel = PythonSentinel()
        sentinel.visit(tree)
        return diagnose(sentinel.stats)
    except Exception as e:
        return f"Syntax Error: {str(e)}. Fix your code before I roast it."

# --- C++ ANALYZER (Tree-sitter Placeholder) ---
def analyze_cpp(file_path):
    if not TREE_SITTER_READY:
        return "C++ detected, but 'tree-sitter' is missing. I can't analyze this yet."
    
    # (Full Tree-sitter logic goes here later if needed)
    return "C++ Analysis: Structurally valid, but manually managing memory is risky."

# --- MAIN ENTRY POINT ---
def scan_file(file_path):
    """
    Determines language and runs the appropriate sentinel.
    """
    if not os.path.exists(file_path):
        return "Ghost File: Target does not exist."

    ext = os.path.splitext(file_path)[1]

    if ext == ".py":
        return analyze_python(file_path)
    elif ext in [".cpp", ".c", ".h", ".hpp"]:
        return analyze_cpp(file_path)
    elif ext in [".js", ".ts", ".jsx"]:
        return "JavaScript detected. I assume it's broken by default."
    else:
        return "Unknown language. I can't roast what I can't read."