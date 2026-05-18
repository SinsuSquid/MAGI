#!/bin/bash
# ======================================
#   MAGI Python Project Installer
#   Platform: Linux / macOS
#   Repository: https://github.com/SinsuSquid/MAGI
# ======================================

set -e

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed." >&2
    exit 1
fi

# Optionally create a virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating a virtual environment in .venv..."
    python3 -m venv .venv
fi

# Activate the virtual environment
. .venv/bin/activate

echo "Installing dependencies..."
if [ -f requirements.txt ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

echo "Initializing MAGI Neural Cores in Ollama..."
if command -v ollama &> /dev/null; then
    echo "--------------------------------------------------"
    echo "DEPLOYMENT MODE SELECTOR"
    echo "--------------------------------------------------"
    echo "1) NERV Elite (Full Tactical Sync)"
    echo "   - Melchior (q8_0), Balthasar (q4_K_M), Casper (q3_K_L)"
    echo "   - Best experience, highest persona differentiation."
    echo "   - Storage Required: ~15.0 GB"
    echo ""
    echo "2) NERV Standard (Single-Model Sync) [RECOMMENDED]"
    echo "   - All cores share a single base 'llama3' model."
    echo "   - High performance, unique persona logic, minimal footprint."
    echo "   - Storage Required: ~5.0 GB"
    echo "--------------------------------------------------"
    read -p "Select tactical mode [1 or 2, default 2]: " mode

    if [ "$mode" == "1" ]; then
        echo "Executing NERV Elite Deployment..."
        ollama create melchior -f melchior.modelfile
        ollama create balthasar -f balthasar.modelfile
        ollama create casper -f casper.modelfile
    else
        echo "Executing NERV Standard Deployment (Using llama3 base)..."
        ollama pull llama3
        
        echo "Creating Melchior core..."
        sed 's/FROM .*/FROM llama3/' melchior.modelfile | ollama create melchior -f -
        
        echo "Creating Balthasar core..."
        sed 's/FROM .*/FROM llama3/' balthasar.modelfile | ollama create balthasar -f -
        
        echo "Creating Casper core..."
        sed 's/FROM .*/FROM llama3/' casper.modelfile | ollama create casper -f -
    fi
    echo "Neural Cores synchronized!"
else
    echo "⚠️  Warning: Ollama not found. Please install Ollama and run:"
    echo "  ollama create melchior -f melchior.modelfile"
    echo "  ollama create balthasar -f balthasar.modelfile"
    echo "  ollama create casper -f casper.modelfile"
fi

echo "Done! To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
