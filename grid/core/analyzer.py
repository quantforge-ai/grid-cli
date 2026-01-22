import ast
import os
import random

# Try importing tree-sitter for multi-language support
try:
    from tree_sitter import Parser
    import tree_sitter_languages
    TREE_SITTER_READY = True
except ImportError:
    TREE_SITTER_READY = False

# Mapping of file extensions to Tree-sitter language IDs
# Exhaustive mapping for Polyglot God Mode
LANG_MAP = {
    # Scripting & Web
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".php": "php",
    ".rb": "ruby",
    ".lua": "lua",
    
    # Systems & Compiled
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cc": "cpp",
    ".cs": "c_sharp",
    ".java": "java",
    ".kt": "kotlin",
    ".go": "go",
    ".rs": "rust",
    ".swift": "swift",
    ".zig": "zig",
    ".dart": "dart",
    ".scala": "scala",
    ".m": "objc",
    ".mm": "objc",
    
    # Functional & Logic
    ".hs": "haskell",
    ".ml": "ocaml",
    ".erl": "erlang",
    ".ex": "elixir",
    ".exs": "elixir",
    ".elm": "elm",
    ".scm": "scheme",
    ".rkt": "scheme",
    ".fs": "c_sharp", # F# often maps reasonably to C# structure in TS
    ".clj": "clojure",
    
    # Data & Math
    ".r": "r",
    ".jl": "julia",
    ".sql": "sql",
    ".f90": "fortran",
    ".f": "fortran",
    ".cob": "cobol",
    
    # Infrastructure & Config
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".fish": "fish",
    ".ps1": "bash", # Fallback
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".json": "json",
    ".dockerfile": "dockerfile",
    ".nix": "nix",
    ".hcl": "hcl",
    ".tf": "hcl",
    ".make": "make",
    "Makefile": "make",
    
    # Shaders & Low Level
    ".glsl": "glsl",
    ".hlsl": "glsl",
    ".sol": "solidity",
    ".v": "verilog",
    ".sv": "verilog",
}

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
        if (node.end_lineno - node.lineno) > 40:
            self.stats["long_functions"] += 1
        args = len(node.args.args)
        self.stats["max_args"] = max(self.stats["max_args"], args)
        self.generic_visit(node)

    def visit_Global(self, node):
        self.stats["globals"] += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id.lower()
                if any(x in name for x in ["api", "key", "secret", "token", "password", "aws", "database"]):
                    self.stats["secrets"] += 1
        self.generic_visit(node)

    def visit_Call(self, node):
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

# --- TREE-SITTER ANALYZER (Polyglot) ---
class TreeSitterSentinel:
    def __init__(self, language_name):
        self.lang_name = language_name
        self.stats = {
            "max_nesting": 0,
            "long_functions": 0,
            "max_args": 0,
            "globals": 0,
            "print_statements": 0,
            "secrets": 0
        }
        self.current_nesting = 0

    def analyze_node(self, node):
        node_type = node.type
        
        # 1. Nesting Level
        nesting_types = [
            'if_statement', 'for_statement', 'while_statement', 'switch_statement', 
            'do_statement', 'if_expression', 'for_expression', 'while_expression',
            'match_expression', 'case_statement'
        ]
        if node_type in nesting_types:
            self.current_nesting += 1
            self.stats["max_nesting"] = max(self.stats["max_nesting"], self.current_nesting)
            for child in node.children:
                self.analyze_node(child)
            self.current_nesting -= 1
            return

        # 2. Function Length & Args
        func_types = [
            'function_declaration', 'method_definition', 'arrow_function', 
            'function_definition', 'method_declaration', 'func_declaration'
        ]
        if node_type in func_types:
            # Length
            lines = node.end_point[0] - node.start_point[0]
            if lines > 40:
                self.stats["long_functions"] += 1
            
            # Args
            for child in node.children:
                if child.type in ['formal_parameters', 'parameter_list', 'parameters']:
                    params = [c for c in child.children if c.type not in ['(', ')', '{', '}', ',', ';', 'type']]
                    self.stats["max_args"] = max(self.stats["max_args"], len(params))
        
        # 3. Secret Detection
        if node_type in ['variable_declarator', 'assignment_expression', 'variable_declaration', 'assignment']:
            text = node.text.decode('utf-8', errors='ignore').lower()
            if any(x in text for x in ["api", "key", "secret", "token", "password", "aws", "database"]):
                self.stats["secrets"] += 1

        # 4. Print Statements
        if node_type in ['call_expression', 'function_call']:
            text = node.text.decode('utf-8', errors='ignore')
            print_patterns = [
                'console.log', 'console.error', 'print(', 'println(', 'fmt.Print', 
                'std::cout', 'printf(', 'System.out.print', 'cat(', 'Log.d'
            ]
            if any(p in text for p in print_patterns):
                self.stats["print_statements"] += 1

        # Recurse
        for child in node.children:
            self.analyze_node(child)

def analyze_python(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        sentinel = PythonSentinel()
        sentinel.visit(tree)
        return {"score": calculate_score(sentinel.stats), "metrics": sentinel.stats}
    except Exception as e:
        return {"score": 1, "error": str(e)}

def analyze_generic(file_path, lang_id):
    if not TREE_SITTER_READY:
        return {"score": 5, "info": "Tree-sitter not available"}
    
    try:
        lang = tree_sitter_languages.get_language(lang_id)
        parser = Parser()
        parser.set_language(lang)
        
        with open(file_path, "rb") as f:
            tree = parser.parse(f.read())
        
        sentinel = TreeSitterSentinel(lang_id)
        sentinel.analyze_node(tree.root_node)
        
        return {"score": calculate_score(sentinel.stats), "metrics": sentinel.stats}
    except Exception as e:
        return {"score": 1, "error": str(e)}

def analyze_file(file_path):
    if not os.path.exists(file_path):
        return {"score": 0, "error": "File not found"}

    ext = os.path.splitext(file_path)[1].lower()
    if not ext: # Handle files like 'Makefile'
        ext = os.path.basename(file_path)

    if ext == ".py":
        return analyze_python(file_path)
    
    lang_id = LANG_MAP.get(ext)
    if lang_id:
        return analyze_generic(file_path, lang_id)
    else:
        return {"score": 5, "info": f"Language {ext} not deeply supported"}