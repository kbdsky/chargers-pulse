$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$PythonExe = "C:\Users\master\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe"
$WorkingDir = "C:\Users\master\Documents\antigravity\cool-rutherford"

$WshShell = New-Object -ComObject WScript.Shell

# 1. Main Launcher Shortcut (HTML Report)
$Shortcut1 = Join-Path $DesktopPath "LA Chargers News Briefing.lnk"
$S1 = $WshShell.CreateShortcut($Shortcut1)
$S1.TargetPath = $PythonExe
$S1.Arguments = "-m newspulse.launcher"
$S1.WorkingDirectory = $WorkingDir
$S1.Description = "LA Chargers News Briefing Launcher"
$S1.IconLocation = "shell32.dll,238"
$S1.Save()

# 2. Web Dashboard Shortcut (Streamlit)
$Shortcut2 = Join-Path $DesktopPath "LA Chargers Web Dashboard.lnk"
$S2 = $WshShell.CreateShortcut($Shortcut2)
$S2.TargetPath = $PythonExe
$S2.Arguments = "-m streamlit run newspulse/ui/app.py"
$S2.WorkingDirectory = $WorkingDir
$S2.Description = "LA Chargers Streamlit Web Dashboard"
$S2.IconLocation = "shell32.dll,14"
$S2.Save()

# 3. Mobile PWA App Server Shortcut (QR Code & Phone App)
$Shortcut3 = Join-Path $DesktopPath "LA Chargers Mobile App.lnk"
$S3 = $WshShell.CreateShortcut($Shortcut3)
$S3.TargetPath = $PythonExe
$S3.Arguments = "-m newspulse.mobile_launcher"
$S3.WorkingDirectory = $WorkingDir
$S3.Description = "LA Chargers Mobile App Server (QR Code for Phone)"
$S3.IconLocation = "shell32.dll,18"
$S3.Save()

Write-Output "SUCCESS: Created 3 shortcuts on Desktop"
