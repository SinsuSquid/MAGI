@echo off
REM ======================================
REM   MAGI Python Project Installer
REM   Platform: Windows
REM   Repository: https://github.com/SinsuSquid/MAGI
REM ======================================

REM Check for Python
where python >nul 2>nul
if errorlevel 1 (
    echo Error: Python is not installed.
    exit /b 1
)

REM Create virtual environment if not exists
if not exist .venv (
    echo Creating virtual environment in .venv...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo No requirements.txt found. Skipping dependency installation.
)

echo Done! To activate the virtual environment later, run:
echo   .venv\Scripts\activate.bat
