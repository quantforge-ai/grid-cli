; Script generated for Grid CLI v1.0
; TARGET: The "Git Bash" Experience

#define MyAppName "Grid Terminal"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "QuantGrid"
#define MyAppURL "https://quantgrid.io"
#define MyAppExeName "grid.exe"

[Setup]
AppId={{C8B35038-7E55-4C3D-A320-GRIDCLI100}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
; Install for current user only (no admin needed = lower friction)
PrivilegesRequired=lowest
OutputBaseFilename=Grid_Terminal_Setup_v1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=grid\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; IMPORTANT: Ensure 'dist\grid.exe' exists before compiling!
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; 1. Start Menu Shortcut
Name: "{group}\Grid Terminal"; Filename: "{app}\{#MyAppExeName}"
; 2. Desktop Shortcut
Name: "{autodesktop}\Grid Terminal"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &Desktop icon"; GroupDescription: "Additional icons"
Name: "contextmenu"; Description: "Add 'Open Grid Here' to Right-Click Menu"; GroupDescription: "Integrations"

[Registry]
; 1. Add to PATH (So they can type 'grid' in PowerShell too)
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Flags: preservestringtype

; 2. The Right-Click Logic (Background of Folder)
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\Grid"; ValueType: string; ValueName: ""; ValueData: "⚡ Open Grid Here"; Tasks: contextmenu; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\Grid"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\grid.exe"; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\Grid\command"; ValueType: string; ValueName: ""; ValueData: """{app}\grid.exe"""; Tasks: contextmenu

; 3. The Right-Click Logic (On a Folder Icon)
Root: HKCU; Subkey: "Software\Classes\Directory\shell\Grid"; ValueType: string; ValueName: ""; ValueData: "⚡ Open Grid Here"; Tasks: contextmenu; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Directory\shell\Grid"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\grid.exe"; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\Grid\command"; ValueType: string; ValueName: ""; ValueData: """{app}\grid.exe"""; Tasks: contextmenu
