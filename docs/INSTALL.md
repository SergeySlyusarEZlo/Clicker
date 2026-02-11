# Installation Guide

Complete installation guide for POWERJET Auto-Clicker.

© 2026 Sergii Sliusar <powerjet777@gmail.com>

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Manual Installation](#manual-installation)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Operating System
- Linux (Ubuntu, Debian, Fedora, etc.)
- Python 3.6 or higher

### Dependencies
- Python 3.6+
- pip3
- pyautogui >= 0.9.54
- pynput >= 1.7.6

### System Permissions
- X11 display server (for GUI automation)
- Permission to simulate mouse and keyboard events

## Quick Installation

The easiest way to install is using the automated installation script:

```bash
# Clone the repository
git clone https://github.com/SergeySlyusarEZlo/Clicker.git
cd Clicker

# Run installation script
chmod +x install.sh
./install.sh
```

The script will:
1. Check for Python 3 and pip3
2. Install required Python packages
3. Make scripts executable
4. Display usage instructions

## Manual Installation

If you prefer to install manually or the automatic script fails:

### Step 1: Clone Repository

```bash
git clone https://github.com/SergeySlyusarEZlo/Clicker.git
cd Clicker
```

### Step 2: Install Python Dependencies

Using pip:
```bash
pip3 install -r requirements.txt
```

Or install packages individually:
```bash
pip3 install pyautogui>=0.9.54
pip3 install pynput>=1.7.6
```

### Step 3: Make Scripts Executable

```bash
chmod +x clicker.py
chmod +x indicator.py
```

### Step 4: Verify Installation

```bash
python3 clicker.py --help
```

You should see the help message with available options.

## Platform-Specific Notes

### Ubuntu/Debian

You may need to install additional system packages:

```bash
sudo apt-get update
sudo apt-get install python3-tk python3-dev
sudo apt-get install python3-xlib
```

### Fedora/RHEL

```bash
sudo dnf install python3-tkinter
sudo dnf install python3-devel
```

### Arch Linux

```bash
sudo pacman -S python-pyautogui python-pynput
```

## Virtual Environment (Recommended)

To avoid conflicts with system packages:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
./clicker.py
```

## Troubleshooting

### Permission Denied Error

If you get "Permission denied" when running scripts:
```bash
chmod +x clicker.py indicator.py
```

### ModuleNotFoundError

If Python can't find required modules:
```bash
pip3 install --user -r requirements.txt
```

### X11 Display Error

If you get display errors, ensure X11 is running:
```bash
echo $DISPLAY
# Should output something like :0 or :1
```

For remote systems, enable X11 forwarding:
```bash
ssh -X user@hostname
```

### pyautogui Fails to Initialize

On some systems, you may need:
```bash
sudo apt-get install scrot
sudo apt-get install python3-tk python3-dev
```

### Claude Process Not Detected

Make sure Claude is running and its process name contains "claude":
```bash
pgrep -f claude
# Should return a process ID
```

## Uninstallation

To remove the application:

```bash
# Remove the directory
rm -rf Clicker

# Optionally remove Python packages
pip3 uninstall pyautogui pynput
```

## Next Steps

After successful installation:
- Read [USAGE.md](USAGE.md) for detailed usage instructions
- Check out the main [README.md](../README.md) for quick start guide
- Review configuration options in the script

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review `clicker.log` for error messages
3. Open an issue on [GitHub](https://github.com/SergeySlyusarEZlo/Clicker/issues)
4. Contact: powerjet777@gmail.com
