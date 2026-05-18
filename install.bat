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
    echo --------------------------------------------------
    echo DEPLOYMENT MODE SELECTOR
    echo --------------------------------------------------
    echo 1] NERV Elite [Full Tactical Sync]
    echo    - Melchior [q8_0], Balthasar [q4_K_M], Casper [q3_K_L]
    echo    - Best experience, highest persona differentiation.
    echo    - Storage Required: ~15.0 GB
    echo.
    echo 2] NERV Standard [Single-Model Sync] - RECOMMENDED
    echo    - All cores share a single base 'llama3' model.
    echo    - High performance, unique persona logic, minimal footprint.
    echo    - Storage Required: ~5.0 GB
    echo --------------------------------------------------
    set /p mode="Select tactical mode [1 or 2, default 2]: "

    if "%mode%"=="1" (
        echo Executing NERV Elite Deployment...
        ollama create melchior -f melchior.modelfile
        ollama create balthasar -f balthasar.modelfile
        ollama create casper -f casper.modelfile
    ) else (
        echo Executing NERV Standard Deployment [Using llama3 base]...
        ollama pull llama3
        
        echo Creating Melchior core...
        powershell -Command "(Get-Content melchior.modelfile) -replace '^FROM .*', 'FROM llama3' | Set-Content temp_m.modelfile"
        ollama create melchior -f temp_m.modelfile
        del temp_m.modelfile
        
        echo Creating Balthasar core...
        powershell -Command "(Get-Content balthasar.modelfile) -replace '^FROM .*', 'FROM llama3' | Set-Content temp_b.modelfile"
        ollama create balthasar -f temp_b.modelfile
        del temp_b.modelfile
        
        echo Creating Casper core...
        powershell -Command "(Get-Content casper.modelfile) -replace '^FROM .*', 'FROM llama3' | Set-Content temp_c.modelfile"
        ollama create casper -f temp_c.modelfile
        del temp_c.modelfile
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
