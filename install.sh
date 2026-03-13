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

# Detect Ubuntu version and display server
UBUNTU_VERSION=$(lsb_release -rs 2>/dev/null || echo "unknown")
SESSION_TYPE="${XDG_SESSION_TYPE:-unknown}"
echo "  Ubuntu version: $UBUNTU_VERSION"
echo "  Session type:   $SESSION_TYPE"
echo ""

# Install system dependencies
echo "Installing system dependencies..."
if ! command -v xdotool &> /dev/null; then
    echo "  Installing xdotool (mouse/keyboard automation)..."
    sudo apt-get install -y xdotool
    echo "✓ xdotool installed"
else
    echo "✓ xdotool already installed"
fi

# On Ubuntu 22.04+ (Wayland), install ydotool as fallback
if [ "$SESSION_TYPE" = "wayland" ] || dpkg --compare-versions "$UBUNTU_VERSION" ge "22.04" 2>/dev/null; then
    if ! command -v ydotool &> /dev/null; then
        echo "  Installing ydotool (Wayland fallback)..."
        sudo apt-get install -y ydotool 2>/dev/null || echo "  ⚠ ydotool not available in repos (optional fallback)"
        if command -v ydotool &> /dev/null; then
            echo "✓ ydotool installed"
        fi
    else
        echo "✓ ydotool already installed"
    fi
fi
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

# Set up /dev/uinput permissions for Wayland support (Ubuntu 22.04+)
echo "Setting up uinput permissions for Wayland support..."

# Ensure uinput kernel module is loaded
if ! lsmod | grep -q uinput; then
    echo "  Loading uinput kernel module..."
    sudo modprobe uinput
    echo "✓ uinput module loaded"
else
    echo "✓ uinput module already loaded"
fi

# Ensure uinput module loads on boot
if ! grep -q '^uinput$' /etc/modules-load.d/*.conf 2>/dev/null; then
    echo "  Configuring uinput to load on boot..."
    echo 'uinput' | sudo tee /etc/modules-load.d/uinput.conf > /dev/null
    echo "✓ uinput will load on boot"
else
    echo "✓ uinput already configured to load on boot"
fi

# Create udev rule for /dev/uinput
UINPUT_RULE='KERNEL=="uinput", GROUP="input", MODE="0660"'
UINPUT_RULE_FILE="/etc/udev/rules.d/99-uinput.rules"

if [ -f "$UINPUT_RULE_FILE" ] && grep -q 'uinput' "$UINPUT_RULE_FILE"; then
    echo "✓ uinput udev rule already exists"
else
    echo "  Creating udev rule for /dev/uinput (requires sudo)..."
    sudo bash -c "echo '$UINPUT_RULE' > $UINPUT_RULE_FILE"
    echo "✓ udev rule created: $UINPUT_RULE_FILE"
fi

# Reload udev rules and apply
sudo udevadm control --reload-rules && sudo udevadm trigger /dev/uinput 2>/dev/null || sudo udevadm trigger

# Set permissions immediately for current session (before reboot/re-login)
if [ -e /dev/uinput ]; then
    sudo chmod 0666 /dev/uinput
    echo "✓ /dev/uinput permissions set for current session"
fi

# Add user to input group
if id -nG "$USER" | grep -qw input; then
    echo "✓ User '$USER' is already in the 'input' group"
else
    echo "  Adding user '$USER' to the 'input' group (requires sudo)..."
    sudo usermod -aG input "$USER"
    echo "✓ User added to 'input' group"
    echo "  ⚠ You must log out and back in for the group change to take effect!"
    echo "  (The script has set temporary permissions so it works immediately)"
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
