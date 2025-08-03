; QuickQR Enhanced Installer

[Setup]
AppName=QuickQR
AppVersion=1.0
DefaultDirName={autopf}\QuickQR
DefaultGroupName=QuickQR
UninstallDisplayIcon={app}\quickqr.exe
OutputDir=.
OutputBaseFilename=QuickQR_Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=icon.ico
LicenseFile=LICENSE.txt

[Files]
Source: "dist\quickqr.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\QuickQR"; Filename: "{app}\quickqr.exe"; IconFilename: "{app}\icon.ico"
Name: "{commondesktop}\QuickQR"; Filename: "{app}\quickqr.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\README.txt"; Description: "View README file"; Flags: postinstall skipifsilent

; Optional: Auto-update hint (manual implementation)
; Future releases should update a version file like:
; https://yourdomain.com/quickqr/version.txt
; The app can check the version against its own.
