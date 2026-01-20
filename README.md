# Grid CLI v1.0.0

The Universal Sentient Developer Toolkit. 

This repository contains the "Face" of the QuantGrid ecosystem. It provides the high-performance terminal UI, the LLM-powered personality engine, and the universal project orchestration logic.

## Installation
```bash
pip install -e .
```

## Features
- **Matrix Boot Sequence**: Stylized startup animation.
- **Sassy LLM Personality**: Unique remarks powered by Mistral-7B.
- **Universal Dev Loop**: `grid dev <url>` clones and sets up ANY project (Python, Node, Rust).
- **Core Orchestration**: Delegated commands to project-specific virtual environments.

## Standalone Architecture
**Grid CLI is a zero-dependency, standalone application.** 
It does not require `quantgrid-core` to be installed for its own operation. It acts as a universal orchestrator that:
1. Detects any project type (React, Python, C++, etc.)
2. Manages local Git automation and "Rescue" protocols.
3. Only interacts with backends like `quantgrid-core` if a `config.grid` file is present in the target repository.

This allows web developers, cloud engineers, and data scientists to use Grid CLI for project management without the overhead of heavy AI libraries.

## 🛰️ Installation: Grid Bash

To experience the full sentient terminal (Windows), run:
```powershell
.\install.bat
```

### This will:
1. **Materialize**: Create a `Grid Bash` shortcut on your desktop.
2. **Synchronize**: Add `grid` to your system PATH for universal access.
3. **Assimilate**: Add a **"Grid Bash Here"** option to your Windows Right-Click menu.

---

## 🦾 Commands
| Command | Action |
| :--- | :--- |
| `grid` | Enter the interactive Matrix REPL |
| `grid init` | Assimilate the current directory (creates `config.grid`) |
| `grid dev <url>` | Clone a project and establish a neural link |
| `grid status` | Perform a system diagnostic scan |
| `grid roast <file>` | AI-powered ruthless code analysis |
| `grid submit` | Safe-inject code via the Rescue Protocol |
| `grid undo` | "Rewrite History" (Soft reset last commit) |
| `grid exit` | Disconnect the neural link |
