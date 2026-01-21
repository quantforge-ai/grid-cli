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

[Icons]
; THIS IS THE MAGIC PART
; We name the shortcut "Grid Terminal" so users feel it's a dedicated app
Name: "{autodesktop}\Grid Terminal"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\Grid Terminal"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: addtopath; Check: NeedsAddPath(ExpandConstant('{app}'))

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