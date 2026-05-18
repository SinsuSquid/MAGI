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

echo "Done! To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
