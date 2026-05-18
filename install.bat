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

echo Initializing MAGI Neural Cores in Ollama...
where ollama >nul 2>nul
if %errorlevel% equ 0 (
    echo Deployment Mode Selector:
    echo   1] Full Tactical Sync [Unique Quants - Heavy Storage ~15GB]
    echo   2] Standard Sync [Single Quant - Light Storage ~5GB]
    set /p mode="Select mode [1 or 2, default 2]: "

    if "%mode%"=="1" (
        echo Executing Full Tactical Sync...
        ollama create melchior -f melchior.modelfile
        ollama create balthasar -f balthasar.modelfile
        ollama create casper -f casper.modelfile
    ) else (
        echo Executing Standard Sync [Using llama3 base]...
        ollama pull llama3
        REM We use simple FROM llama3 to save space, keeping the personas unique
        ollama create melchior -f melchior.modelfile
        ollama create balthasar -f balthasar.modelfile
        ollama create casper -f casper.modelfile
        echo NOTE: Windows install uses modelfiles which might trigger pulls if not edited. 
        echo For true space saving, Melchior/Balthasar/Casper should be manually edited to FROM llama3.
    )
    echo Neural Cores synchronized!
) else (
    echo [33mWarning: Ollama not found. Please install Ollama and run:[0m
    echo   ollama create melchior -f melchior.modelfile
    echo   ollama create balthasar -f balthasar.modelfile
    echo   ollama create casper -f casper.modelfile
)

echo Done! To activate the virtual environment later, run:
echo   .venv\Scripts\activate.bat
