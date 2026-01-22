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
def calculate_score(stats):
    """
    Calculates a complexity score from 1-10.
    10 is perfect, 1 is total garbage.
    """
    score = 10
    
    # Penalties
    score -= stats.get("max_nesting", 0) * 1.5
    score -= stats.get("long_functions", 0) * 2
    score -= (stats.get("max_args", 0) - 3) * 1.5 if stats.get("max_args", 0) > 3 else 0
    score -= stats.get("globals", 0) * 3
    score -= stats.get("print_statements", 0) * 1
    score -= stats.get("secrets", 0) * 10 # Heavy penalty for secrets
    
    return max(1, min(10, int(score)))

# --- PYTHON ANALYZER (Built-in AST) ---
class PythonSentinel(ast.NodeVisitor):
    def __init__(self):
        self.stats = {
            "max_nesting": 0,
            "long_functions": 0,
            "max_args": 0,
            "globals": 0,
            "print_statements": 0,
            "secrets": 0
        }
        self.current_nesting = 0

    def visit_FunctionDef(self, node):
        # Check Length
        if (node.end_lineno - node.lineno) > 40:
            self.stats["long_functions"] += 1
        
        # Check Args
        args = len(node.args.args)
        self.stats["max_args"] = max(self.stats["max_args"], args)
            
        self.generic_visit(node)

    def visit_Global(self, node):
        self.stats["globals"] += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Look for hardcoded secrets in variable names
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id.lower()
                if any(x in name for x in ["api", "key", "secret", "token", "password", "aws", "database"]):
                    self.stats["secrets"] += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check for print()
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.stats["print_statements"] += 1
        self.generic_visit(node)

    def _visit_nesting(self, node):
        self.current_nesting += 1
        self.stats["max_nesting"] = max(self.stats["max_nesting"], self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1

    def visit_If(self, node): self._visit_nesting(node)
    def visit_While(self, node): self._visit_nesting(node)
    def visit_For(self, node): self._visit_nesting(node)

def analyze_python(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        sentinel = PythonSentinel()
        sentinel.visit(tree)
        
        score = calculate_score(sentinel.stats)
        return {
            "score": score,
            "metrics": sentinel.stats
        }
    except Exception as e:
        return {
            "score": 1,
            "error": str(e)
        }

# --- C++ ANALYZER (Tree-sitter Placeholder) ---
def analyze_cpp(file_path):
    if not TREE_SITTER_READY:
        return "C++ detected, but 'tree-sitter' is missing. I can't analyze this yet."
    return "C++ Analysis: Structurally valid, but manually managing memory is risky."

# --- MAIN ENTRY POINT ---
def analyze_file(file_path):
    """
    Determines language and runs the appropriate sentinel.
    """
    if not os.path.exists(file_path):
        return {"score": 0, "error": "File not found"}

    ext = os.path.splitext(file_path)[1]

    if ext == ".py":
        return analyze_python(file_path)
    elif ext in [".cpp", ".c", ".h", ".hpp"]:
        # Placeholder for C++
        return {"score": 7, "info": "C++ analysis limited"}
    else:
        # Default for unknown
        return {"score": 5, "info": "Language not supported for full analysis"}