# ⚡ Grid CLI

**The Sentient Developer Companion**

Grid CLI is a next-generation developer tool that combines Git automation, code quality analysis, and team collaboration with a Matrix-style hacker terminal experience. It's Git meets AI-powered roasts, with zero tolerance for bad code.

---

## 🎯 Features

### 🚀 Smart Git Automation
- **Safe Push**: Auto-stages files, scans for secrets, and blocks pushes with sensitive data
- **Cowboy Protocol**: Automatically creates safety branches when pushing to `main`/`master`/`production`
- **Smart Branching**: Create or switch to branches in one command
- **Auto-Cleanup**: Remove merged branches automatically

### 🔥 Code Quality & Roasting
- **File Analysis**: Get complexity scores and brutally honest feedback on your code
- **Project Scanning**: Analyze entire codebases with detailed reports
- **Developer Roasts**: PvP mode - roast teammates based on their commit history
- **Leaderboard**: Track who's the biggest cowboy on your team

### 🎨 Interactive Terminal
- **Matrix Green Theme**: Hacker-style UI with vibrant green/cyan colors
- **Git Bash Prompt**: Clean `user@hostname GRID ~/.../path $` format
- **Smart Path Shortening**: Long paths auto-truncate to `~/.../lastdir`
- **Right-Click Integration**: "Open Grid Here ⚡" in Windows Explorer

### 🤝 Team Collaboration
- **Multiplayer Roasts**: Share code roasts with your team via Discord
- **Blame with Attitude**: Find who wrote that line and roast them
- **Daily Standups**: Auto-generate recap reports from commit history  
- **Cowboy Leaderboard**: See who's pushing to main the most

---

## 📦 Installation

### Windows Installer
1. Download `GridSetup.exe` from releases
2. Run the installer
3. Choose installation options:
   - ✅ Add to PATH (recommended)
   - ✅ Desktop shortcut
   - ✅ Right-click context menu "Open Grid Here ⚡"
4. Launch from Start Menu or Desktop

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/quantforge-ai/grid-cli.git
cd grid-cli

# Install dependencies
pip install -r requirements.txt

# Build executable (optional)
python -m PyInstaller grid.spec --clean
```

---

## 🎮 Quick Start

### First Time Setup
```bash
# Set your identity (used for cowboy commits and roasts)
grid auth YourName

# Initialize Grid in your project (creates .grid config)
grid init
```

### Launch Interactive Terminal
```bash
# Just type 'grid' to enter the Grid Terminal
grid

# Or double-click grid.exe
# Or right-click folder → "Open Grid Here ⚡"
```

---

## 📋 Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `grid` | Launch interactive Grid Terminal | `grid` |
| `grid auth <name>` | Set your developer identity | `grid auth tanishq` |
| `grid init` | Initialize .grid config in project | `grid init` |
| `grid push [message]` | Safe push with secret scanning & cowboy protection | `grid push "fix login"` |
| `grid roast [file]` | Analyze code quality (file or whole project) | `grid roast auth.py` |
| `grid roast --dev <name>` | Roast a teammate based on git history | `grid roast --dev alice` |
| `grid branch <name>` | Create/switch to branch | `grid branch feature/login` |
| `grid home [--clean]` | Return to main and pull latest | `grid home --clean` |
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
- `grid docker nuke` - Kill all running containers
- `grid docker ps` - Show container status

---

## 🎨 Interactive Terminal Features

When you run `grid` without arguments, you enter the **Grid Terminal**:

```bash
tan@obsidian GRID ~/.../grid-cli $
```

### Available Commands in Terminal
- All Grid commands (`push`, `roast`, `status`, etc.)
- Standard system commands (`git`, `npm`, `ls`, `dir`, etc.)
- Built-in shell commands (`cd`, `clear`, `exit`)

### Features
- ✨ **Boot Animation**: Matrix-style loading sequence
- 🎯 **Git Bash Prompt**: Shows user, hostname, and current directory
- 📁 **Smart Paths**: Long paths auto-shorten to save space
- 🌈 **Color Coded**: Green for commands, cyan for accents
- ⌨️ **Full Shell**: Works like bash/cmd with Grid superpowers

---

## ⚙️ Configuration

Grid creates a `.grid` file in your project root:

```json
{
  "project_id": "uuid-here",
  "lead_dev": "your-name",
  "banned_files": [".env", "secrets.json"],
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

## 🔒 Security Features

### Secret Scanning
Grid automatically scans for:
- Environment files (`.env`, `.env.local`)
- API keys and tokens
- Private keys
- Custom patterns defined in `.grid`

### Cowboy Protocol
Prevents accidental pushes to protected branches:
1. Detects push to `main`/`master`/ `dev`/`production`
2. Creates safety branch: `cowboy/yourname/message/roast-slug`
3. Pushes to safety branch instead
4. Generates pre-filled PR link

---

## 🎯 Use Cases

See [USAGE.md](USAGE.md) for detailed examples and workflows.

---

## 🤝 Contributing

Grid CLI is built for engineers, by engineers. Contributions welcome!

```bash
# Fork the repo, create a branch
grid branch feature/awesome-feature

# Make your changes
# Grid will roast your code automatically

# Push safely
grid push "Add awesome feature"
```

---

## 📝 License

MIT License - see LICENSE file

---

## 🔗 Links

- **GitHub**: [quantforge-ai/grid-cli](https://github.com/quantforge-ai/grid-cli)
- **Issues**: [Report bugs](https://github.com/quantforge-ai/grid-cli/issues)
- **Documentation**: [USAGE.md](USAGE.md)

---

**Built with ❤️ by the QuantForge AI Team**

*"The terminal you deserve, not the one you need."*
