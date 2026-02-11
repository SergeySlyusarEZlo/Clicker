#!/bin/bash

# POWERJET Auto-Clicker Installation Script
# © 2026 Sergii Sliusar <powerjet777@gmail.com>

set -e

echo "============================================================"
echo "    POWERJET Auto-Clicker Installation"
echo "    © 2026 Sergii Sliusar"
echo "============================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3.6 or higher and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python 3 found: $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x clicker.py
if [ -f "indicator.py" ]; then
    chmod +x indicator.py
    echo "✓ clicker.py and indicator.py are now executable"
else
    echo "✓ clicker.py is now executable"
fi

echo ""
echo "============================================================"
echo "    Installation Complete!"
echo "============================================================"
echo ""
echo "You can now run the auto-clicker with:"
echo "  ./clicker.py          # Default mode (20s timeout)"
echo "  ./clicker.py -f       # Fast mode (1s timeout)"
echo "  ./clicker.py -f 10    # Custom timeout (10s)"
echo ""
echo "For more information, see README.md"
echo "============================================================"
