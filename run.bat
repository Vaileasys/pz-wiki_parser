@echo off
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in your PATH. Please install Python and try again.
    pause
    exit /B 1
)

python main.py

pause
