# Grid CLI

> **The Sentient Developer Companion**

**Grid CLI** is a next-generation developer tool that combines Git automation, code quality analysis, and team collaboration with a Matrix-style terminal experience. It's Git meets AI-powered roasts, with zero tolerance for bad code.

![Grid Terminal](grid/assets/variant_glitch.png)

---

## Features

### Smart Git Automation
- **Safe Push**: Auto-stages files, scans for secrets, and blocks pushes with sensitive data.
- **Cowboy Protocol**: Automatically creates safety branches when you try to push directly to `main`, `master`, or `production`. *(A "Cowboy" is someone who pushes to protected branches without using feature branches)*
- **Smart Branching**: Create or switch to branches in a single command (`grid branch feature/login`).
- **Branch Cleanup**: Remove merged branches with `grid purge` to keep your repo clean.

### Code Quality & Roasting
- **File Analysis**: Get complexity scores and brutally honest feedback on your code.
- **Project Scanning**: Analyze entire codebases with tables showing scores and status for each file.
- **Developer Roasts**: **PvP Mode** - roast teammates based on their commit history.
- **Leaderboard**: Track who is the biggest "Cowboy" on your team.

### Interactive Terminal
- **Matrix Green Theme**: Hacker-style UI with vibrant green/cyan colors.
- **Git Bash Prompt**: Clean `user@hostname GRID ~/.../path $` format.
- **Smart Path Shortening**: Long paths auto-truncate to `~/.../lastdir` to save screen space.
- **Right-Click Integration**: "Open Grid Here ⚡" context menu in Windows Explorer.

### Team Collaboration
- **Multiplayer Roasts**: Share code roasts with your team via Discord/Slack hooks.
- **Blame with Attitude**: Find who wrote a specific line and shame them.
- **Daily Standups**: Generate recap reports from git history with `grid recap`.

---

## Installation

### 🌐 Official Website

**[Download Grid CLI →](https://grid-cli.vercel.app/)**

Visit our official website for the latest installers and documentation.

---

### Quick Install (Alternative)

Or download directly from GitHub Releases:

| Platform | Download Link |
|----------|---------------|
| **Windows** | [GridSetup.exe](https://github.com/quantforge-ai/grid-cli/releases/latest/download/GridSetup.exe) |
| **macOS** | [Grid-macOS.dmg](https://github.com/quantforge-ai/grid-cli/releases/latest/download/Grid-macOS.dmg) |
| **Linux** | [Grid-Linux.AppImage](https://github.com/quantforge-ai/grid-cli/releases/latest/download/Grid-Linux.AppImage) |

#### Windows Installation
1. Download `GridSetup.exe`
2. Run the installer
3. Choose installation options:
   - **Add to PATH** (Required for global access)
   - **Desktop Shortcut**
   - **Right-Click Context Menu** ("Open Grid Here ⚡")
4. Launch "Grid Terminal" from Start Menu or Desktop

#### macOS Installation
```bash
# Download and install
curl -L https://github.com/quantforge-ai/grid-cli/releases/latest/download/Grid-macOS.dmg -o Grid.dmg
open Grid.dmg

# Or install via Homebrew (coming soon)
brew install quantforge-ai/tap/grid
```

#### Linux Installation
```bash
# Download AppImage
curl -L https://github.com/quantforge-ai/grid-cli/releases/latest/download/Grid-Linux.AppImage -o grid
chmod +x grid
sudo mv grid /usr/local/bin/

# Or via package manager (Ubuntu/Debian)
sudo add-apt-repository ppa:quantforge-ai/grid
sudo apt update
sudo apt install grid-cli
```

### Manual Installation (For Developers)
```bash
# Clone the repository
git clone https://github.com/quantforge-ai/grid-cli.git
cd grid-cli

# Install dependencies
pip install -r requirements.txt
pip install --editable .

# (Optional) Build executable
pyinstaller --noconfirm --onefile --console --name "grid" --icon "grid/assets/icon.ico" grid/main.py
```

---

## Quick Start

### 1. First Time Setup
```bash
# Set your identity (used for cowboy commits and roasts)
grid auth YourName

# Initialize Grid in your project (creates .grid config)
grid init
# To understand .grid configuration, see USAGE.md
```

### 2. Launch Interactive Terminal
You can run grid commands in your normal terminal, or enter the **Grid Shell**:

```bash
# Just type 'grid' to enter the Grid Terminal
grid

# Or double-click the "Grid Terminal" icon on your desktop
```

---

## Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `grid` | Launch interactive Grid Terminal | `grid` |
| `grid auth <name>` | Set your developer identity | `grid auth tanishq` |
| `grid init` | (Lead) Initialize .grid config in project | `grid init` |
| `grid cloud_sync` | (Lead) Sync .grid config to Cloud Brain | `grid cloud_sync` |
| `grid dev <url> <name>` | (Team) Clone repo and download config from Cloud | `grid dev https://github.com/org/repo alice` |
| `grid update` | Check for updates and upgrade Grid | `grid update` |
| `grid push [message]` | Safe push with secret scanning & cowboy protection | `grid push "fix login"` |
| `grid roast [file]` | Analyze code quality (file or whole project) | `grid roast auth.py` |
| `grid roast --dev <name>` | Roast a teammate based on git history | `grid roast --dev alice` |
| `grid branch <name>` | Create/switch to branch | `grid branch feature/login` |
| `grid home [--clean]` | Return to main and pull latest changes | `grid home --clean` |
| `grid status` | System diagnostics & project info | `grid status` |
| `grid blame <file> <line>` | Find who wrote a line (with roast) | `grid blame app.py 42` |
| `grid purge` | Delete merged local branches | `grid purge` |
| `grid rank` | View cowboy leaderboard | `grid rank` |
| `grid recap` | Generate daily standup report | `grid recap` |
| `grid tree` | Visualize project structure | `grid tree` |
| `grid docker <action>` | Manage Docker containers | `grid docker up` |

### Docker Actions
- `grid docker up [-d]` - Start containers (detached mode)
- `grid docker down` - Stop containers
- `grid docker nuke` - Kill all running containers instantly
- `grid docker ps` - Show container status

---

## Interactive Terminal Features

When you run `grid` without arguments, you enter the **Grid Terminal**:

```bash
tan@obsidian GRID ~/.../grid-cli $
```

### Features
- **Boot Animation**: Matrix-style package loading sequence.
- **Git Bash Prompt**: Shows user, hostname, and current directory.
- **Smart Paths**: Long paths auto-shorten (`~/.../folder`) to keep the prompt clean.
- **Color Coded**: Green for commands, Cyan for accents, Red for errors.
- **Full Shell**: Works like bash/cmd. You can run `git`, `npm`, `cd`, `ls` inside it.

---

## Configuration

Grid creates a `.grid` file in your project root:

```json
{
  "project_id": "uuid-here",
  "lead_dev": "your-name",
  "banned_files": [".env", "secrets.json", "*.key"],
  "webhook_url": "https://discord.com/webhook/..."
}
```

### Global Identity
Stored in `~/.grid_identity`:

```json
{
  "name": "tanishq"
}
```

---

## Security Features

### Secret Scanning
Grid automatically scans for:
- Environment files (`.env`, `.env.local`)
- API keys, AWS tokens, and Private Keys
- Custom patterns defined in `.grid`

### Cowboy Protocol
Prevents accidental pushes to protected branches. If you try to push to `main`:
1. Intercepts the push.
2. Creates a safety branch: `cowboy/yourname/message/roast-slug`.
3. Pushes to that branch instead.
4. Generates a pre-filled Pull Request link.

---

## Contributing

Grid CLI is built for engineers, by engineers. Contributions welcome!

```bash
# Fork the repo, create a branch
grid branch feature/awesome-feature

# Make your changes
# Grid will roast your code automatically if you write bad code

# Push safely
grid push "feat: add awesome feature"
```

---

## License

MIT License - see LICENSE file.

---

**Built with ❤️ (and sarcasm) by the QuantForge AI Team**

*"The terminal you deserve, not the one you need."*
