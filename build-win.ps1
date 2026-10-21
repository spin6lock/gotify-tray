$ErrorActionPreference = 'Stop'

Write-Output "Creating executable"
python -m PyInstaller --noconfirm gotify-tray.spec
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed: $LASTEXITCODE" }

Write-Output "Creating installer"
& "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" gotify-tray.iss
if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed: $LASTEXITCODE" }
