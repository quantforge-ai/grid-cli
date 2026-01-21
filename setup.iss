; Script generated for Grid CLI
#define MyAppName "Grid CLI"
#define MyAppVersion "1.0"
#define MyAppPublisher "QuantForge AI"
#define MyAppExeName "grid.exe"

[Setup]
AppId={{A3D86659-3D4F-4C46-8659-3D4F4C468659}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=GridSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=grid\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &Desktop Shortcut"; GroupDescription: "Additional icons:"; Flags: checkedonce
Name: "addtopath"; Description: "Add 'grid' command to PATH (Recommended)"; GroupDescription: "System Integration:"; Flags: checkedonce

[Files]
; The main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Copy the icon file so shortcuts can reference it
Source: "grid\assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Force the shortcut to use the deployed icon.ico
; We name the shortcut "Grid Terminal" so users feel it's a dedicated app
Name: "{autodesktop}\Grid Terminal"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"
Name: "{autoprograms}\Grid Terminal"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"

[Registry]
; Add to PATH environment variable
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: addtopath; Check: NeedsAddPath(ExpandConstant('{app}'))

; Context menu: Right-click on folder
Root: HKCR; Subkey: "Directory\shell\OpenGridHere"; ValueType: string; ValueName: ""; ValueData: "Open Grid Here ⚡"; Flags: uninsdeletekey
Root: HKCR; Subkey: "Directory\shell\OpenGridHere"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"
Root: HKCR; Subkey: "Directory\shell\OpenGridHere\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%V"""

; Context menu: Right-click on folder background (inside folder)
Root: HKCR; Subkey: "Directory\Background\shell\OpenGridHere"; ValueType: string; ValueName: ""; ValueData: "Open Grid Here ⚡"; Flags: uninsdeletekey
Root: HKCR; Subkey: "Directory\Background\shell\OpenGridHere"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"
Root: HKCR; Subkey: "Directory\Background\shell\OpenGridHere\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%V"""

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;