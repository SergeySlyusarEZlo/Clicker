# Usage Guide

Comprehensive usage guide for POWERJET Auto-Clicker.

© 2026 Sergii Sliusar <powerjet777@gmail.com>

## Table of Contents

- [Basic Usage](#basic-usage)
- [Command-Line Options](#command-line-options)
- [Configuration](#configuration)
- [Understanding the Interface](#understanding-the-interface)
- [Advanced Usage](#advanced-usage)
- [Tips and Best Practices](#tips-and-best-practices)

## Basic Usage

### Starting the Application

Default mode (20-second idle timeout):
```bash
./clicker.py
```

Fast mode (1-second timeout):
```bash
./clicker.py -f
```

Custom timeout:
```bash
./clicker.py -f 10
```

### Stopping the Application

Press `Ctrl+C` to stop the program gracefully.

## Command-Line Options

### `-f, --fast [SECONDS]`

Fast mode with configurable timeout.

**Examples:**

```bash
# 1-second timeout
./clicker.py -f
./clicker.py --fast

# 5-second timeout
./clicker.py -f 5
./clicker.py --fast 5

# 30-second timeout
./clicker.py -f 30
```

### Getting Help

```bash
./clicker.py -h
./clicker.py --help
```

## Configuration

### Modifying Click Position

Edit `clicker.py` and modify these variables:

```python
target_x = screen_width - 400  # X coordinate
target_y = screen_height - 100  # Y coordinate
```

### Changing Process Detection

By default, the program looks for "claude" process. To change:

```python
def is_claude_running():
    result = subprocess.run(['pgrep', '-f', 'your_process'],
                            capture_output=True, text=True)
    return result.returncode == 0
```

### Adjusting Click Delays

Modify timing in the click sequence:

```python
time.sleep(0.3)  # Before click
pyautogui.click()
time.sleep(0.5)  # After click, before Enter
pyautogui.press('enter')
time.sleep(0.2)  # After Enter
```

## Understanding the Interface

### Startup Screen

```
============================================================
    ╔═══════════════════════════════╗
               Auto-Clicker
    ╚═══════════════════════════════╝
  © 2026 Sergii Sliusar <powerjet777@gmail.com>
  Auto-clicker for Claude
  Idle timeout: 20 seconds
  Screen size: 1920x1080
  Target: (1520, 980) | Log: clicker.log
  Press Ctrl+C to stop
============================================================
```

**Information displayed:**
- Copyright and branding
- Current idle timeout setting
- Screen resolution
- Target click coordinates
- Log file location

### Status Line

During operation, you'll see a dynamic status line:

**Waiting State:**
```
⠋ Waiting... Idle: 5.2/20s | Claude: running [█████░░░░░░░░░░░░░░░]
```

**Click Event:**
```
✓ CLICKED! Idle: 20.1s | Claude: running [████████████████████]
```

**Components:**
- Spinner (⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏) - Shows program is active
- Idle time - Current/Maximum idle time
- Claude status - Process detection status
- Progress bar - Visual representation of idle progress

### Progress Bar

The progress bar shows how close the system is to triggering a click:

```
[░░░░░░░░░░░░░░░░░░░░]  0% - Just started counting
[█████░░░░░░░░░░░░░░░]  25% - Quarter way there
[██████████░░░░░░░░░░]  50% - Halfway to click
[███████████████░░░░░]  75% - Almost there
[████████████████████]  100% - Click triggered!
```

## Advanced Usage

### Running in Background

To run as a background process:

```bash
nohup ./clicker.py &
```

To check the output:
```bash
tail -f clicker.log
```

To stop:
```bash
pkill -f clicker.py
```

### Running on Startup

Add to your startup applications or create a systemd service:

Create `/etc/systemd/system/powerjet-clicker.service`:
```ini
[Unit]
Description=POWERJET Auto-Clicker
After=graphical.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/Clicker
ExecStart=/path/to/Clicker/clicker.py
Restart=on-failure

[Install]
WantedBy=graphical.target
```

Enable and start:
```bash
sudo systemctl enable powerjet-clicker
sudo systemctl start powerjet-clicker
```

### Visual Indicator

If `indicator.py` is present, a visual indicator will show the click location:

```bash
# indicator.py runs automatically with clicker.py
# To run manually for testing:
python3 indicator.py 1520 980
```

### Multiple Instances

To run multiple instances with different settings:

```bash
# Terminal 1 - Fast mode
./clicker.py -f 1

# Terminal 2 - Normal mode
./clicker.py -f 20

# Terminal 3 - Slow mode
./clicker.py -f 60
```

## Tips and Best Practices

### 1. Finding the Right Timeout

Start with a longer timeout and adjust:
- Development work: 30-60 seconds
- General use: 20 seconds (default)
- Frequent updates: 5-10 seconds
- Testing: 1-2 seconds

### 2. Verifying Click Position

Before running continuously:
1. Run with `-f 1` (fast mode)
2. Watch where it clicks
3. Adjust coordinates if needed
4. Stop with Ctrl+C

### 3. Monitoring Logs

Regularly check logs for issues:
```bash
tail -f clicker.log
```

View rotated logs:
```bash
cat clicker.log.1  # Previous log
cat clicker.log.2  # Oldest backup
```

Note: Logs are automatically rotated when they reach ~1 MB (~10,000 lines).

### 4. Process Detection

Ensure Claude is running and detectable:
```bash
pgrep -f claude
ps aux | grep claude
```

### 5. Avoiding Conflicts

- Don't move the mouse during click countdown
- Avoid keyboard input near timeout
- Keep Claude window accessible
- Don't minimize the target application

### 6. Performance Optimization

For lower CPU usage:
- Use longer timeout intervals
- Disable visual indicator if not needed
- Reduce logging verbosity

## Logging

### Log File Location

Logs are written to `clicker.log` in the application directory.

### Log Rotation

The application uses automatic log rotation to prevent unlimited log growth:
- Maximum file size: ~1 MB (~10,000 lines)
- Backup files: 2 rotated copies kept (clicker.log.1, clicker.log.2)
- When clicker.log reaches 1 MB:
  - clicker.log.1 → clicker.log.2
  - clicker.log → clicker.log.1
  - New clicker.log is created

This ensures logs don't consume excessive disk space while maintaining recent history.

### Log Levels

The application logs:
- INFO: Startup, configuration
- DEBUG: Each wait cycle, each click
- WARNING: Minor issues (e.g., indicator failed to start)
- ERROR: Critical errors

### Reading Logs

View recent activity:
```bash
tail -n 50 clicker.log
```

Filter by level:
```bash
grep "ERROR" clicker.log
grep "CLICKED" clicker.log
```

Watch in real-time:
```bash
tail -f clicker.log
```

## Troubleshooting Common Issues

### Clicks Not Happening

1. Check Claude is running: `pgrep -f claude`
2. Verify idle timeout is reached
3. Check logs for errors
4. Ensure mouse/keyboard activity detection works

### Clicks in Wrong Location

1. Check screen resolution matches
2. Update target coordinates in code
3. Use indicator.py to verify position

### High CPU Usage

1. Increase timeout interval
2. Check for errors in logs
3. Ensure no infinite loops

### Application Crashes

1. Check `clicker.log` for error messages
2. Verify all dependencies installed
3. Test with `python3 clicker.py -f 10`

## Examples

### Example 1: Testing Setup

```bash
# Quick test with 2-second timeout
./clicker.py -f 2

# Watch for clicks, verify position
# Stop with Ctrl+C when satisfied
```

### Example 2: Daily Work

```bash
# Start with 20-second timeout
./clicker.py

# Let it run in background
# Check logs periodically: tail -f clicker.log
```

### Example 3: Debugging

```bash
# Enable verbose output
./clicker.py -f 1 2>&1 | tee debug.log

# Or check the log file
tail -f clicker.log | grep -E "ERROR|WARNING"
```

## Security Considerations

- The application simulates mouse and keyboard input
- Only runs when Claude process is detected
- All actions are logged for accountability
- Can be stopped immediately with Ctrl+C
- Does not collect or transmit any data

## Support

For questions or issues:
- Email: powerjet777@gmail.com
- GitHub: https://github.com/SergeySlyusarEZlo/Clicker
- Documentation: See docs/ folder
