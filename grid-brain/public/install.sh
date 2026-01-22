#!/bin/bash

# Grid CLI Install Script for Mac/Linux
# Auto-installs Grid from the GitHub repository

echo "╔═══════════════════════════════════╗"
echo "║   GRID CLI INSTALLATION WIZARD    ║"
echo "╚═══════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip and try again."
    exit 1
fi

echo "✅ Python 3 detected"
echo "✅ pip3 detected"
echo ""
echo "Installing Grid CLI..."
echo ""

# Install Grid CLI from GitHub
pip3 install --upgrade git+https://github.com/quantforge-ai/grid-cli.git

if [ $? -eq 0 ]; then
    echo ""
    echo "✨ Grid CLI installed successfully!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Run 'grid' to launch the interactive terminal"
    echo "   2. Run 'grid init' in your project to get started"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check the error above."
    exit 1
fi
