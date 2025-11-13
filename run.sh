#!/bin/bash
# Run script for AI-Textpad - sets up venv and launches application

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
CODE_DIR="$SCRIPT_DIR/code"

echo "AI-Textpad Launcher"
echo "==================="
echo ""

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created at $VENV_DIR"
    echo ""
fi

# Activate venv
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Check if dependencies are installed
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r "$CODE_DIR/requirements.txt"
    echo "Dependencies installed."
    echo ""
fi

# Change to code directory and run application
cd "$CODE_DIR"
echo "Starting AI-Textpad..."
echo ""
python3 -m ai_textpad.main

# Deactivate on exit
deactivate
