@echo off
chcp 65001 > nul
echo ============================================================
echo  ⚡ NewsPulse - LA Chargers Weekly Intelligence Generator
echo ============================================================
cd /d "%~dp0\.."

python -m newspulse.cli generate --all --format all --output-dir .\reports

echo ============================================================
echo  ✨ Weekly Report Completed at %date% %time%
echo ============================================================
