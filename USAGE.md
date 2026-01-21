# 📖 Grid CLI - Usage Guide & Examples

This guide provides detailed use cases, workflows, and best practices for Grid CLI commands.

---

## 🚀 Getting Started

### Initial Setup

```bash
# 1. Set your identity (required for multiplayer features)
grid auth tanishq

# Output:
# ✅ Identity updated to: tanishq
# ⚠️  This name will be used for Multiplayer Roasts and Cowboy commits.
```

```bash
# 2. Initialize Grid in your project (team lead only)
cd your-project
grid init

# This creates a .grid configuration file
```

---

## 💾 Safe Push Workflows

### Scenario 1: Normal Push
```bash
# Stage, scan, and push safely
grid push "Add user authentication"

#  → Auto-stages all changes
# 🔍 → Scans for secrets (.env, API keys)
# ✅ → Commits and pushes
# 🎉 → Success message or compliment
```

### Scenario 2: Cowboy Push (Blocked)
```bash
# Trying to push directly to main...
git checkout main
grid push "quick fix"

# Output:
# ⚠️  COWBOY DETECTED. "Did you forget what branches are for?"
# 🔀 Taking the wheel... Moving to: cowboy/tanishq/quick-fix/reckless-behavior
# ✅ Branch Switched.
# 📤 Code pushed to safety branch.
# 
# 👉 CLICK TO OPEN PR (Pre-filled):
# https://github.com/yourrepo/compare/main...cowboy/tanishq/quick-fix
```

### Scenario 3: Secret Detection
```bash
# Accidentally added .env file
grid push "update config"

# Output:
# 🚫 PUSH BLOCKED. "Are you trying to give hackers a free lunch?"
# ⚠️  Restricted files detected: ['.env']
# → Files auto-unstaged
```

---

## 🔥 Code Quality & Roasting

### Roast a Single File
```bash
grid roast src/auth.py

# Output:
# ╭─ Roast Report: src/auth.py ──╮
# │ Complexity Score: 3/10        │
# │ Verdict: "This code looks     │
# │ like it was written on a      │
# │ dare."                        │
# ╰───────────────────────────────╯
```

### Roast Entire Project
```bash
grid roast

# Output:
# ┌─ Artifact Analysis Report ────┐
# │ File Name        │ Score │ Status     │
# ├──────────────────┼───────┼────────────┤
# │ api/routes.py    │ 2/10  │ 🔥 Toxic   │
# │ utils/helpers.py │ 6/10  │ ⚠️  Messy  │
# │ core/auth.py     │ 9/10  │ ✅ Clean   │
# └──────────────────┴───────┴────────────┘
# 
# AGGREGATE SCORE: 5.7/10
# "Not bad, but I've seen better code from interns."
```

### Roast a Teammate (PvP Mode)
```bash
grid roast --dev alice

# Output:
# ╭─ Roasting alice ──────────────╮
# │ Last Commit: "fixed typo"    │
# │                              │
# │ Grid says: "Took you 3       │
# │ commits to fix a typo? Ever  │
# │ heard of spell check?"       │
# ╰──────────────────────────────╯
```

### Share Roast with Team
```bash
grid roast --dev bob --share

# → Posts roast to Discord webhook
# ✅ Roast sent to Discord.
```

---

## 🌿 Branch Management

### Smart Branch Switching
```bash
# Create new branch (if doesn't exist)
grid branch feature/login-ui

# Switch to existing branch
grid branch feature/login-ui

# Both commands work the same way!
```

### Return Home
```bash
# Go back to main and pull latest
grid home

# Output:
# 🏠 Switching to main...
# 📥 Pulling latest changes...
# ✅ Up to date with origin/main
```

### Clean Up After Yourself
```bash
# Return to main and delete your old branch
grid home --clean

# → Switches to main
# → Pulls changes
# → Deletes the branch you were on
```

### Purge Merged Branches
```bash
# Delete all  local branches that have been merged
grid purge

# Output:
# 🗑️  Deleting merged branches...
# ✅ Removed: feature/old-login
# ✅ Removed: bugfix/header-css
# 🎯 Cleaned up 2 branches
```

---

## 🔍 Git Blame with Attitude

### Find Who Broke It
```bash
grid blame src/payment.py 127

# Output:
# ╭─ Blame Detective ─────────────╮
# │ File: src/payment.py:127     │
# │ Author: alice                │
# │ Commit: "refactor payment"   │
# │ Date: 2 days ago             │
# │                              │
# │ Grid says: "Of course it     │
# │ was alice. She writes bugs   │
# │ like it's her job."          │
# ╰──────────────────────────────╯
```

### Share the Blame
```bash
grid blame auth.py 42 --share

# → Posts blame info + roast to team Discord
```

---

## 📊 System & Project Info

### Status Check
```bash
grid status

# Output:
# ╭─ SYSTEM DIAGNOSTICS ──────────╮
# │ Current Branch: feature/login │
# │ Git Status: Clean             │
# │ Identity: tanishq             │
# │ Project: quantforge-terminal  │
# │ Files Tracked: 127            │
# │ Last Commit: 2 hours ago      │
# ╰───────────────────────────────╯
```

### View Project Tree
```bash
grid tree

# Output:
# 📂 quantforge-terminal/
# ├─📁 src/
# │  ├─📄 auth.py
# │  ├─📄 api.py
# │  └─📁 utils/
# │     └─📄 helpers.py
# ├─📁 tests/
# └─📄 README.md
```

---

## 🏆 Leaderboard & Analytics

### Cowboy Leaderboard
```bash
grid rank

# Output:
# ╭─ COWBOY LEADERBOARD ──────────╮
# │ Rank │ Name      │ Direct Pushes │
# ├──────┼───────────┼───────────────┤
# │ 🤠 1 │ alice     │ 23            │
# │ 🤦 2 │ bob       │ 17            │
# │ ✅ 3 │ tanishq   │ 2             │
# ╰───────────────────────────────────╯
# 
# "alice, you're the reason we can't have nice things."
```

### Daily Standup Report
```bash
grid recap

# Output:
# ╭─ Daily Recap - 2026-01-21 ────╮
# │ Commits Today: 8              │
# │ Files Changed: 14             │
# │ Lines Added: +237             │
# │ Lines Removed: -89            │
# │                               │
# │ Top Commits:                  │
# │ • "Add OAuth integration"     │
# │ • "Fix login redirect"        │
# │ • "Update dependencies"       │
# ╰───────────────────────────────╯
```

---

## 🐳 Docker Management

### Start Containers
```bash
# Start in foreground
grid docker up

# Start in background (detached)
grid docker up -d
```

### Stop Containers
```bash
grid docker down
```

### Nuclear Option
```bash
# Kill ALL Docker containers
grid docker nuke

# ⚠️  WARNING: Kills everything, not just this project!
```

### Check Status
```bash
grid docker ps

# Shows running containers
```

---

## 🎮 Interactive Terminal Usage

### Launch Grid Terminal
```bash
# Method 1: Type 'grid'
grid

# Method 2: Double-click grid.exe

# Method 3: Right-click folder → "Open Grid Here ⚡"
```

### Inside the Terminal
```bash
# Your prompt looks like this:
tan@obsidian GRID ~/.../project $

# Run Grid commands (no 'grid' prefix needed)
push "my changes"
roast app.py
status

# Run system commands
git log -n 5
npm install
ls -la

# Built-in commands
cd ../other-project
clear
exit
```

---

## 🔄 Common Workflows

### Daily Workflow
```bash
# 1. Start your day
grid home              # Get latest from main

# 2. Create feature branch
grid branch feature/new-thing

# 3. Make changes, then push
grid push "implement new thing"

# 4. Check code quality
grid roast

# 5. End of day
grid recap             # Generate standup report
```

### Team Lead Workflow
```bash
# Initialize project
grid init

# Set up webhooks in .grid file
# (Add Discord webhook URL)

# Monitor team
grid rank              # See who's cowboys
grid blame problem.py 50  # Find issues

# Share roasts
grid roast --dev <teammate> --share
```

### Code Review Workflow
```bash
# Before opening PR
grid roast             # Check your own code first
grid push "feature complete"

# Review teammate's code
git checkout their-branch
grid roast src/their-file.py
```

---

## ⚙️ Advanced Configuration

### Custom Secret Patterns
Edit `.grid` file:
```json
{
  "banned_files": [
    ".env",
    ".env.local",
    "secrets.json",
    "*.key",
    "*.pem"
  ]
}
```

### Discord  Integration
Add webhook to `.grid`:
```json
{
  "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK"
}
```

Now roasts with `--share` flag will post to Discord!

---

## 💡 Pro Tips

1. **Use `grid` instead of `git push`** - Save yourself from secrets leaks
2. **Roast your code before PRs** - Fix issues before teammates find them
3. **Enable Discord integration** - Make code reviews fun
4. **Use `grid home --clean`** - Keep your branches tidy
5. **Set identity first** - `grid auth yourname` for multiplayer features
6. **Right-click integration** - Open Grid Terminal in any folder instantly

---

## 🐛 Troubleshooting

### "No .grid file found"
```bash
# Solution: Initialize Grid in your project
grid init
```

### "Identity not set"
```bash
# Solution: Set your name
grid auth yourname
```

### "Push blocked - secrets detected"
```bash
# Grid found sensitive files
# Check what was blocked, remove from staging:
git reset .env
grid push "safe changes"
```

### Path too long in terminal
```bash
# Grid automatically shortens paths over 25 chars
# ~/.../really/deep/nested/path becomes ~/.../path
```

---

## 📚 Further Reading

- [README.md](README.md) - Project overview and installation
- [GitHub Issues](https://github.com/quantforge-ai/grid-cli/issues) - Report bugs
- [GitHub Repo](https://github.com/quantforge-ai/grid-cli) - Source code

---

**Happy Coding! 🚀**

*Remember: Grid is watching. Write good code.*
