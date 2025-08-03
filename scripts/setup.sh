#!/usr/bin/env bash

# Setup script for Metaphysical Scene Weaver

echo "=== Metaphysical Scene Weaver Setup ==="
echo

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "Installing Metaphysical Scene Weaver..."
pip install -e .

# Install additional dependencies
echo "Installing additional dependencies..."
pip install -e ".[dev,api]"

# Download spaCy language model
echo "Downloading spaCy English language model..."
python -m spacy download en_core_web_sm

# Create necessary directories
echo "Creating directories..."
mkdir -p examples/output
mkdir -p data

# Check for required data files
echo
echo "Checking for required data files..."
if [ ! -f "characters.json" ]; then
    echo "⚠️  Warning: characters.json not found. Please add your character data."
fi

if [ ! -f "places.json" ]; then
    echo "⚠️  Warning: places.json not found. Please add your location data."
fi

echo
echo "✓ Setup complete!"
echo
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo
echo "To run the CLI, use:"
echo "  python -m src --help"
echo
echo "To run the example:"
echo "  python examples/run_example.py"