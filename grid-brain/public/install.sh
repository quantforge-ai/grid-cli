#!/bin/bash

# --- COLORS ---
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- HEADER ---
clear
echo -e "${CYAN}"
echo "   ________  _______  ____     ______   ____"
echo "  / ____/  |/  / __ \/ __ \   / ____/  /  _/"
echo " / / __/ /|_/ / / / / / / /  / /       / /  "
echo "/ /_/ / /  / / /_/ / /_/ /  / /___   _/ /   "
echo "\____/_/  /_/\____/_____/   \____/  /___/   "
echo -e "${NC}"
echo -e "${CYAN}>> INITIALIZING NEURAL LINK...${NC}"
sleep 1

# --- CHECK PYTHON ---
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed.${NC}"
    echo "Please install Python 3 and try again."
    exit 1
fi

# --- INSTALLATION ---
echo -e "${GREEN}[1/2] Downloading Core Files...${NC}"

# We use pip3 to ensure it installs for Python 3
# --upgrade ensures they always get the latest version
if pip3 install --upgrade git+https://github.com/quantforge-ai/grid-cli.git; then
    echo -e "${GREEN}[2/2] Assimilation Complete.${NC}"
    echo ""
    echo -e "${CYAN}>> GRID ONLINE.${NC}"
    echo "Type 'grid' to launch the terminal."
else
    echo -e "${RED}[ERROR] Installation failed.${NC}"
    echo "Check your internet connection or git installation."
    exit 1
fi
