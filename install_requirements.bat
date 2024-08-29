@echo off
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /B 1
)

IF NOT EXIST "requirements.txt" (
    echo requirements.txt not found. Please ensure it is in the same directory as this script.
    pause
    exit /B 1
)

echo Installing packages from requirements.txt...
pip install -r requirements.txt

IF %ERRORLEVEL% EQU 0 (
    echo All packages installed successfully.
) ELSE (
    echo An error occurred while installing the packages.
)

pause
