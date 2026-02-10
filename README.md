# POWERJET Auto-Clicker

Auto-clicker for Claude that automatically clicks on a specified screen area when user inactivity is detected.

© 2026 Sergii Sliusar <powerjet777@gmail.com>

## Description

The program monitors mouse and keyboard activity. When the system is idle for a specified time and the Claude process is running, the program automatically clicks on a designated screen area and presses Enter.

## Features

- 🎯 Automatic click on idle detection
- 📊 Visual progress bar showing wait time
- 🔄 Animated status spinner
- 📝 Logging of all actions to file
- 🎨 Visual click position indicator (indicator.py)
- ⚙️ Flexible timeout configuration via command-line arguments

## Requirements

- Python 3.6+
- pyautogui
- pynput

## Installation

```bash
# Install dependencies
pip install pyautogui pynput

# Or via requirements.txt (if available)
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Run with default timeout (20 seconds)
python3 clicker.py

# Or make executable
chmod +x clicker.py
./clicker.py
```

### Fast Mode

```bash
# Fast mode with 1 second timeout
./clicker.py -f

# Or using --fast
./clicker.py --fast
```

### Custom Timeout

```bash
# 10 seconds timeout
./clicker.py -f 10

# 30 seconds timeout
./clicker.py -f 30
```

## Command-Line Arguments

- `-f, --fast [SECONDS]` - Fast mode
  - Without value: 1 second timeout
  - With value: specified number of seconds

## Configuration

You can modify the following parameters in the code:

- `target_x` - Click X coordinate (default: screen_width - 400)
- `target_y` - Click Y coordinate (default: screen_height - 100)
- `idle_timeout` - Idle time before click (configurable via arguments)

## Logging

All program actions are logged to `clicker.log`:
- Program startup
- Screen parameters and click position
- Each click with timestamps
- Errors and exceptions

## Stopping the Program

Press `Ctrl+C` to stop the program gracefully.

## Visual Indicator

If `indicator.py` is present in the same directory, the program will automatically launch a visual indicator showing the future click location on the screen.

## Project Structure

```
clicker/
├── clicker.py      # Main script
├── indicator.py    # Visual indicator (optional)
├── clicker.log     # Log file (created automatically)
└── README.md       # This file
```

## Output Example

```
============================================================

    ╔═══════════════════════════════╗
               Auto-Clicker
    ╚═══════════════════════════════╝
  © 2026 Sergii Sliusar <powerjet777@gmail.com>
  Auto-clicker for Claude
  Idle timeout: 20 seconds
  Screen size: 1920x1080
  Target: (1820, 980) | Log: clicker.log
  Press Ctrl+C to stop
============================================================

⠋ Waiting... Idle: 5.2/20s | Claude: running [█████░░░░░░░░░░░░░░░]
✓ CLICKED! Idle: 20.1s | Claude: running [████████████████████]
```

## Security

- Program only works when Claude process is detected
- All actions are logged
- Can be stopped at any time with Ctrl+C

## License

© 2026 Sergii Sliusar. All rights reserved.

## Contact

Email: powerjet777@gmail.com
