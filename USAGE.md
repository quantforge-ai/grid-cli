# Grid CLI - Usage Guide & Examples

This guide provides detailed workflows and explains how to configure Grid to match your team's style.

---

## Getting Started

### 1. Set Your Identity
Before you start, tell Grid who you are. This name is used for the Leaderboard and Multiplayer Roasts.

```bash
grid auth <your_username>

# Example:
grid auth neo
# ✅ Identity updated to: neo
```

### 2. Choose Your Path

**Are you the Team Lead?** → Run `grid init` to create the project configuration.

**Are you a Team Member?** → Run `grid dev <repo_url> <your_name>` to join an existing project.

---

## For Team Leads: Project Setup

### Step 1: Initialize Project (Lead Only)
Run this once in your project root to "install" Grid into the repo.

```bash
cd your-project
grid init
```

**What just happened?**
Grid created a file named `.grid` in your folder. This is your Project Configuration File.

**ACTION REQUIRED:**
1. Open `.grid` in your code editor
2. Add your Webhook URL (for Discord/Slack notifications)
3. Define Banned Files (to stop team members from leaking secrets)
4. Save the file

### Step 2: Sync to Cloud Brain (Lead Only)
Once you have edited the `.grid` file, upload it to the Grid Cloud so your team can access these rules.

```bash
grid cloud_sync
```

**Output:**
```
✅ Configuration synced to Cloud Brain.
📡 Project ID: 550e8400-e29b... registered.
```

Now, when other developers run `grid dev`, they will automatically fetch these rules.

---

## For Team Members: Joining a Project

### Use `grid dev` to Onboard

When you join a team using Grid, use this command instead of manually cloning the repo:

```bash
grid dev <repo_url> <your_name>

# Example:
grid dev https://github.com/your-org/your-repo alice
```

**What happens:**
1. Clones the repository
2. Sets your Grid identity to `alice`
3. Downloads the `.grid` config from Cloud Brain
4. Downloads team webhooks and banned file patterns

**Output:**
```
✅ Identity set to: alice
📥 Cloning backend...
🌥️ Syncing with Cloud Brain...
✅ Secrets & Webhooks downloaded.
✅ SETUP COMPLETE.
>> Run: cd backend
```

---

## The .grid Configuration File

This file controls how Grid behaves for your entire team.

### Full Example of a .grid file:

```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000", 
  "lead_dev": "neo",
  "banned_files": [
    ".env",
    ".env.local",
    "secrets.json",
    "*.key",
    "*.pem",
    "id_rsa"
  ],
  "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL",
  "services": {
    "db": {
      "image": "postgres:15-alpine",
      "ports": ["5432:5432"],
      "environment": {
        "POSTGRES_USER": "grid_user",
        "POSTGRES_PASSWORD": "secure_password",
        "POSTGRES_DB": "grid_db"
      }
    },
    "cache": {
      "image": "redis:alpine",
      "ports": ["6379:6379"]
    }
  }
}
```

### What do I put in here?

- **project_id**: DO NOT TOUCH. This connects your repo to the Cloud Database.
- **banned_files**: The "No-Fly List." Any file matching these patterns will be blocked from being pushed.
  - *Why?* To prevent leaking API keys.
- **webhook_url**: Your Discord Webhook URL.
  - *Why?* So `grid roast --share` can post directly to your team channel.
- **services** (Optional): Docker service definitions for your infrastructure.
  - *Why?* Team members can run `grid docker up` without creating docker-compose.yml
  - Grid auto-generates the Docker configuration from this JSON
  - Supports any Docker Compose service syntax (image, ports, environment, volumes, etc.)

---

## The Push Workflow

Grid separates developers into two categories: **Sane Professionals** and **Cowboys**.

### 1. The "Sane Developer" Push
For developers who actually remember to create a branch before writing code.

```bash
# You are already on 'feature/login'
grid push "implemented auth logic"

# Output:
# 🔍 Scanning for secrets... Clean.
# ✅ Changes staged and committed.
# 🚀 Pushed to origin/feature/login.
# "Suspiciously clean code. Good job."
```

### 2. The "Cowboy" Push
For developers who forget to create branches. You are on `main`, you made breaking changes, and you tried to push.

```bash
# You are on 'main' (The Mistake)
grid push "quick hotfix"

# Output:
# ⚠️  COWBOY DETECTED. "Did you forget you're on production?"
# 🔀 Taking the wheel...
#    Creating safety branch: cowboy/maverick/quick-hotfix/yolo-mode
# ✅ Branch switched. Files moved.
# 📤 Pushed to safety branch.
# 
# 👉 PR LINK PRE-GENERATED:
# https://github.com/org/repo/compare/main...cowboy/maverick/quick-hotfix
```

**Why?** Grid saved you from breaking the build. It automatically branched off, moved your changes, pushed them, and gave you a PR link. The branch name includes the identity of the developer (`maverick`) so everyone knows who messed up.

---

## Security & Secret Blocking

Grid acts as a firewall for your repo.

```bash
# Accidentally added a .env file containing keys
grid push "update config"

# Output:
# 🚫 PUSH BLOCKED. "Are you trying to give hackers a free lunch?"
# ⚠️  Restricted files detected: ['.env']
# → Files auto-unstaged.
```

**How did it know?**
It checked the `banned_files` list in your `.grid` file (which you configured earlier).

---

## Roasting & Collaboration

### Roast a Teammate
Want to see if your teammate has been writing bad code?

```bash
grid roast --dev <teammate_name>

# Example:
grid roast --dev alice

# Output:
# ╭─ Roasting alice ──────────────╮
# │ Last Commit: "typo fix"      │
# │                              │
# │ Grid says: "Took you 3       │
# │ commits to fix one word?     │
# │ Efficient."                  │
# ╰──────────────────────────────╯
```

### Multiplayer Roast (Discord)
Broadcast the shame to your entire team.

```bash
grid roast --dev bob --share
```

**How does it know where to post?**
It uses the `webhook_url` you added to the `.grid` file.

---

## The Interactive Terminal

Tired of typing `grid` before every command? Enter the Grid Shell.

```bash
# Launch the shell
grid
```

Inside the shell, you don't need prefixes. It behaves like a normal terminal but supercharged.

```bash
# Your prompt:
neo@matrix GRID ~/projects/backend $

# Just type commands directly:
push "refactor api"       # Runs: grid push ...
roast app.py              # Runs: grid roast ...
status                    # Runs: grid status

# System commands still work:
npm install
git status
ls -la
```

---

## Additional Useful Commands

### Branch Cleanup: `grid purge`
Remove all local branches that have been merged into main.

```bash
grid purge

# Output:
# 🗑️ Deleting merged branches...
# ✅ Removed: feature/old-login
# ✅ Removed: bugfix/header-fix
# 🎯 Cleaned up 2 branches
```

### Daily Standup: `grid recap`
Generate a summary of your day's work from git history.

```bash
grid recap

# Output:
# ╭─ Daily Recap - 2026-01-22 ───╮
# │ Commits Today: 8             │
# │ Files Changed: 14            │
# │ Lines Added: +237            │
# │ Lines Removed: -89           │
# │                              │
# │ Top Commits:                 │
# │ • "Add OAuth integration"    │
# │ • "Fix login redirect"       │
# │ • "Update dependencies"      │
# ╰──────────────────────────────╯
```

### System Status: `grid status`
View diagnostics and project information.

```bash
grid status

# Output:
# ╭─ SYSTEM DIAGNOSTICS ─────────╮
# │ Current Branch: feature/auth │
# │ Git Status: Clean            │
# │ Identity: neo                │
# │ Project: backend-api         │
# │ Last Commit: 2 hours ago     │
# ╰──────────────────────────────╯
```

### Git Blame with Attitude: `grid blame`
Find who wrote a specific line and get a roast.

```bash
grid blame src/auth.py 42

# Output:
# ╭─ Blame Detective ─────────────╮
# │ File: src/auth.py:42         │
# │ Author: alice                │
# │ Commit: "quick fix"          │
# │ Date: 3 days ago             │
# │                              │
# │ Grid says: "This line looks  │
# │ like it was written at 3am." │
# ╰──────────────────────────────╯

# Share to team Discord
grid blame src/auth.py 42 --share
```

### Cowboy Leaderboard: `grid rank`
See who's been pushing to protected branches the most.

```bash
grid rank

# Output:
# ╭─ Recklessness Ranking ───────╮
# │ Rank │ Developer │ Cowboy     │
# │      │           │ Incidents  │
# ├──────┼───────────┼────────────┤
# │  #1  │ Alice     │     23     │
# │      │           │ 🤠 Sheriff │
# │      │           │ of Chaos   │
# ├──────┼───────────┼────────────┤
# │  #2  │ Bob       │     17     │
# │      │           │ 🐴 Deputy  │
# │      │           │ Danger     │
# ├──────┼───────────┼────────────┤
# │  #3  │ Neo       │      2     │
# │      │           │ Village    │
# │      │           │ Idiot      │
# ╰───────────────────────────────╯
# 
# "Alice, you're the reason we can't have nice things."
```

**How it works:** Grid scans remote cowboy branches to count violations per developer.

### Project Structure: `grid tree`
Visualize your project's file structure.

```bash
grid tree

# Output:
# 📂 backend-api/
# ├─📁 src/
# │  ├─📄 auth.py
# │  ├─📄 api.py
# │  └─📁 utils/
# │     └─📄 helpers.py
# ├─📁 tests/
# └─📄 README.md
```

---

## Keeping Grid Updated

### Self-Update: `grid update`
Grid can update itself! Run this command to check for and install the latest version.

```bash
grid update

# For pip/dev users:
# Downloads and installs latest version from GitHub
# Output: ✅ ASSIMILATION COMPLETE. RESTART GRID.

# For .exe users:
# Opens browser to download latest installer
# Output: Opening download portal...
```

**Manual update methods:**
- **Developers**: `pip install --upgrade git+https://github.com/quantforge-ai/grid-cli.git`
- **Windows users**: Download latest `GridSetup.exe` and run it

---

## Summary of Commands

| Command | Action |
|---------|--------|
| `grid auth <name>` | Sets your identity |
| `grid init` | (Lead Only) Creates local configuration |
| `grid cloud_sync` | (Lead Only) Uploads config to Cloud Brain |
| `grid dev <url> <name>` | (Team Member) Clone repo and download config |
| `grid update` | Check for updates and upgrade Grid |
| `grid push "<msg>"` | Smart push (handles secrets & cowboy mode) |
| `grid branch <name>` | Creates or switches to a branch |
| `grid home [--clean]` | Returns to main and pulls updates |
| `grid status` | Shows system diagnostics and project info |
| `grid roast [file]` | Analyzes code quality (file or whole project) |
| `grid roast --dev <name> [--share]` | Roasts a teammate (optionally share to Discord) |
| `grid blame <file> <line> [--share]` | Find who wrote a line (with roast) |
| `grid purge` | Deletes all merged local branches |
| `grid recap` | Generates daily standup report from git history |
| `grid rank` | Shows the Cowboy Leaderboard |
| `grid tree` | Visualizes project structure |
| `grid docker up [-d]` | Starts Docker containers (detached mode optional) |
| `grid docker down` | Stops Docker containers |
| `grid docker nuke` | Kills all running containers |
| `grid docker ps` | Shows container status |

---

**Happy Coding!**

*Grid is watching.*
