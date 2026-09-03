@echo off
setlocal
cd /d "%~dp0\.."
python -m newspulse.launcher
if errorlevel 1 (
    echo.
    echo [Error] Execution failed.
    pause
)
endlocal
