#!/bin/bash
echo "🚀 Building Grid CLI Standalone (Linux/Mac)..."

# Check for PyInstaller
if ! command -v pyinstaller &> /dev/null
then
    echo "[!] PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Build
pyinstaller --onefile --console \
    --name grid \
    --add-data "grid/assets:grid/assets" \
    grid/main.py

echo "✅ Build Complete: dist/grid"
