; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Bentsch Business Tools"
#define MyAppVersion "1.0"
#define MyAppPublisher "GONC "
#define MyAppURL "https://www.gonc.co.zw/bentsch"
#define MyAppExeName "client.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{E70A10B7-807F-4915-BF06-D4DBFD4C2460}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\licence.rtf
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename=Bentsch Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\client.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\_decimal.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\_multiprocessing.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-console-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-datetime-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-debug-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-errorhandling-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-file-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-file-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-file-l2-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-handle-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-heap-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-interlocked-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-libraryloader-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-localization-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-memory-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-namedpipe-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-processenvironment-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-processthreads-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-processthreads-l1-1-1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-profile-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-rtlsupport-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-string-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-synch-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-synch-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-sysinfo-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-timezone-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-core-util-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-conio-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-convert-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-environment-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-filesystem-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-heap-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-locale-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-math-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-multibyte-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-process-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-runtime-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-stdio-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-string-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-time-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\api-ms-win-crt-utility-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\base_library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\cef.pak"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\cef_100_percent.pak"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\cef_200_percent.pak"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\cef_extensions.pak"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\chrome_elf.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\client.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\client.exe.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\clr.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\d3dcompiler_43.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\d3dcompiler_47.dll"; DestDir: "{app}"; Flags: ignoreversion

Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\devtools_resources.pak"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\icudtl.dat"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\libcef.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\libEGL.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\libGLESv2.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\License"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\msvcp100.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\MSVCP140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\msvcp90.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\natives_blob.bin"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\Python.Runtime.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\python36.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\pywintypes36.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\snapshot_blob.bin"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\subprocess.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\ucrtbase.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\v8_context_snapshot.bin"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\WebBrowserInterop.x86.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\widevinecdmadapter.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\win32console.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\win32gui.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\win32wnet.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\cefpython3\*"; DestDir: "{app}\cefpython3"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\client\dist\client\locales\*"; DestDir: "{app}\locales"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\temp\service\service\*"; DestDir: "{app}\service"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\temp\service\server\*"; DestDir: "{app}\server"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\temp\service\database\config.json"; DestDir: "{app}\database\config.json"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\temp\service\bin\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\temp\service\python\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\nakamura9a\Documents\code\git\umisoft\build-tools\installer\dist\installer.exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
Root: HKLM64; Subkey: "Software\umisoft-19"; Check: IsWin64;  Flags: uninsdeletekeyifempty
Root: HKLM64; Subkey: "SOFTWARE\umisoft-19"; Check: IsWin64; ValueType: string; ValueName: "SERVICE_PATH"; ValueData: "{app}\service"; Flags: uninsdeletekeyifempty
Root: HKLM32; Subkey: "Software\umisoft-19"; Flags: uninsdeletekeyifempty
Root: HKLM32; Subkey: "SOFTWARE\umisoft-19"; ValueType: string; ValueName: "SERVICE_PATH"; ValueData: "{app}\service"; Flags: uninsdeletekeyifempty


[Run]

Filename: "{app}\installer.exe"; Description: "Install Application Service"; Flags: skipifsilent waituntilterminated
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
