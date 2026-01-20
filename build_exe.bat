@echo off
echo 🚀 Building Grid CLI Standalone (Windows)...

:: Check for PyInstaller
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] PyInstaller not found. Installing...
    pip install pyinstaller
)

:: Build
pyinstaller --onefile --console ^
    --name grid ^
    --add-data "grid/assets;grid/assets" ^
    --icon "grid/assets/icon.ico" ^
    grid/main.py

echo ✅ Build Complete: dist/grid.exe
