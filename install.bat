@echo off
setlocal enabledelayedexpansion

echo.
echo [bold cyan]🌐 QUANTGRID: ASSIMILATION PROTOCOL v1.0[/bold cyan]
echo.

:: 1. Define Paths
set "INSTALL_DIR=%USERPROFILE%\.quantgrid\bin"
set "EXE_SOURCE=%~dp0dist\grid.exe"

:: 2. Create Directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: 3. Copy Executable
if exist "%EXE_SOURCE%" (
    echo [ ] Moving Grid to local bin...
    copy /Y "%EXE_SOURCE%" "%INSTALL_DIR%\grid.exe" >nul
) else (
    echo [!] dist\grid.exe not found. Build it first.
    exit /b 1
)

:: 4. Add to User PATH (via registry to be permanent)
echo [ ] Synchronizing Environment Variables...
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path') do set "OLD_PATH=%%B"
echo !OLD_PATH! | find /i "%INSTALL_DIR%" >nul
if %errorlevel% neq 0 (
    setx Path "%OLD_PATH%;%INSTALL_DIR%" >nul
)

:: 5. Create "Grid Bash Here" Context Menu
echo [ ] Injecting Context Menu (Registry)...
set "KEY=HKEY_CLASSES_ROOT\Directory\Background\shell\GridBash"
reg add "%KEY%" /ve /t REG_SZ /d "Grid Bash Here" /f >nul
reg add "%KEY%" /v "Icon" /t REG_SZ /d "%INSTALL_DIR%\grid.exe" /f >nul
reg add "%KEY%\command" /ve /t REG_SZ /d "cmd.exe /K \"cd /d %%V && grid\"" /f >nul

:: 6. Create Desktop Shortcut
echo [ ] Materializing Launcher...
powershell -Command "$s = (New-Object -ComObject WScript.Shell).CreateShortcut('%USERPROFILE%\Desktop\Grid Bash.lnk'); $s.TargetPath = '%INSTALL_DIR%\grid.exe'; $s.IconLocation = '%INSTALL_DIR%\grid.exe'; $s.Save()"

echo.
echo [bold green]✅ ASSIMILATION COMPLETE.[/bold green]
echo.
echo You can now:
echo  1. Type 'grid' in any terminal.
echo  2. Right-click any folder and select 'Grid Bash Here'.
echo  3. Launch 'Grid Bash' from your desktop.
echo.
pause
