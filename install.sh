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
    echo "Deployment Mode Selector:"
    echo "  1) Full Tactical Sync (Unique Quants - Heavy Storage ~15GB)"
    echo "  2) Standard Sync (Single Quant - Light Storage ~5GB) [Default]"
    read -p "Select mode [1 or 2]: " mode

    if [ "$mode" == "1" ]; then
        echo "Executing Full Tactical Sync..."
        ollama create melchior -f melchior.modelfile
        ollama create balthasar -f balthasar.modelfile
        ollama create casper -f casper.modelfile
    else
        echo "Executing Standard Sync (Using llama3 base)..."
        ollama pull llama3
        # Create personas using the standard llama3 to save space
        ollama create melchior -f - <<EOF
FROM llama3
SYSTEM "$(grep -A 10 'SYSTEM """' melchior.modelfile | sed '1d;$d')"
EOF
        ollama create balthasar -f - <<EOF
FROM llama3
SYSTEM "$(grep -A 10 'SYSTEM """' balthasar.modelfile | sed '1d;$d')"
EOF
        ollama create casper -f - <<EOF
FROM llama3
SYSTEM "$(grep -A 10 'SYSTEM """' casper.modelfile | sed '1d;$d')"
EOF
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
