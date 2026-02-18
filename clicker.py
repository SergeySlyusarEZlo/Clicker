#!/usr/bin/env python3
import pyautogui
import time
import logging
from logging.handlers import RotatingFileHandler
import subprocess
import argparse
import os
from pynput import mouse, keyboard

# Configure rotating log handler (max ~10000 lines, ~1MB per file)
log_handler = RotatingFileHandler(
    'clicker.log',
    maxBytes=1024 * 1024,  # 1 MB (~10000 lines)
    backupCount=2,          # Keep 2 backup files
    encoding='utf-8'
)
log_handler.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Auto-clicker for Claude on idle',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''
Usage examples:
  %(prog)s          - run with idle time = 20 seconds (default)
  %(prog)s -f       - run with idle time = 1 second (fast mode)
  %(prog)s -f 10    - run with idle time = 10 seconds (custom value)
    ''')

parser.add_argument('-f', '--fast', nargs='?', const=1, type=int, metavar='SECONDS',
                    help='Fast mode. Without value = 1 sec, with value = specified time')

args = parser.parse_args()

# Determine idle timeout
if args.fast is not None:
    idle_timeout = args.fast
else:
    idle_timeout = 20

last_activity_time = time.time()
spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
spinner_index = 0
suppress_activity = False

def reset_activity():
    global last_activity_time
    if not suppress_activity:
        last_activity_time = time.time()

def on_move(x, y):
    reset_activity()

def on_click(x, y, button, pressed):
    reset_activity()

def on_scroll(x, y, dx, dy):
    reset_activity()

def on_press(key):
    reset_activity()

def is_claude_running():
    try:
        result = subprocess.run(['pgrep', '-f', 'claude'],
                                capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def stop_indicator(indicator_process):
    """Stop visual indicator process"""
    if indicator_process and indicator_process.poll() is None:
        try:
            indicator_process.terminate()
            indicator_process.wait(timeout=1)
            logger.debug("Visual indicator stopped")
        except Exception as e:
            logger.warning(f"Could not stop indicator: {e}")

def start_indicator(target_x, target_y, indicator_script):
    """Start visual indicator process"""
    if os.path.exists(indicator_script):
        try:
            process = subprocess.Popen(
                ['python3', indicator_script, str(target_x), str(target_y)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logger.debug("Visual indicator started")
            return process
        except Exception as e:
            logger.warning(f"Could not start indicator: {e}")
            return None
    return None

try:
    # Clear screen before starting
    os.system('clear')

    screen_width, screen_height = pyautogui.size()
    target_x = screen_width - 400
    target_y = screen_height - 100

    # Display startup information with Powerjet logo
    print("\n" + "=" * 60)
    print("    ╔═══════════════════════════════╗")
    print("               Auto-Clicker          ")
    print("    ╚═══════════════════════════════╝")
    print(f"  © 2026 Sergii Sliusar <powerjet777@gmail.com>")
    print(f"  Auto-clicker for Claude")
    print(f"  Idle timeout: {idle_timeout} seconds")
    print(f"  Screen size: {screen_width}x{screen_height}")
    print(f"  Target: ({target_x}, {target_y}) | Log: clicker.log")
    print(f"  Press Ctrl+C to stop")
    print("=" * 60 + "\n")

    logger.info(f"Screen size: {screen_width}x{screen_height}")
    logger.info(f"Target position: {target_x}, {target_y}")
    logger.info(f"Idle timeout: {idle_timeout} seconds")

    # Start visual indicator in background
    indicator_script = os.path.join(os.path.dirname(__file__), 'indicator.py')
    indicator_process = start_indicator(target_x, target_y, indicator_script)
    if indicator_process:
        logger.info("Visual indicator started")

    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener.start()
    keyboard_listener.start()

    while True:
        idle_time = time.time() - last_activity_time
        claude_running = is_claude_running()

        if idle_time >= idle_timeout and claude_running:
            # Stop visual indicator before clicking
            stop_indicator(indicator_process)

            try:
                prev_x, prev_y = pyautogui.position()
                pyautogui.moveTo(target_x, target_y)
                time.sleep(0.3)
                pyautogui.click()
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(0.2)
                suppress_activity = True
                pyautogui.moveTo(prev_x, prev_y)
                suppress_activity = False
            except pyautogui.FailSafeException:
                logger.warning("Fail-safe triggered: mouse was at a screen corner. Skipping click.")
                print(f"\r{'⚠ Fail-safe: move mouse away from corner and wait...':<80}", end='', flush=True)
                indicator_process = start_indicator(target_x, target_y, indicator_script)
                reset_activity()
                continue

            # Restart visual indicator after clicking
            indicator_process = start_indicator(target_x, target_y, indicator_script)

            # Clear screen and redraw header after click
            os.system('clear')
            print("\n" + "=" * 60)
            print("    ╔═══════════════════════════════╗")
            print("               Auto-Clicker          ")
            print("    ╚═══════════════════════════════╝")
            print(f"  © 2026 Sergii Sliusar <powerjet777@gmail.com>")
            print(f"  Auto-clicker for Claude")
            print(f"  Idle timeout: {idle_timeout} seconds")
            print(f"  Screen size: {screen_width}x{screen_height}")
            print(f"  Target: ({target_x}, {target_y}) | Log: clicker.log")
            print(f"  Press Ctrl+C to stop")
            print("=" * 60 + "\n")

            progress_bar = "█" * 20
            status_msg = f"✓ CLICKED! Idle: {idle_time:.1f}s | Claude: running [{progress_bar}]"
            print(f"\r\033[2K{status_msg}", end='', flush=True)
            logger.debug(f"Clicked! Idle: {idle_time:.0f}s, Claude: running")

            reset_activity()
        else:
            spinner = spinner_chars[spinner_index % len(spinner_chars)]
            spinner_index = (spinner_index + 1) % len(spinner_chars)

            # Calculate progress bar
            progress = min(idle_time / idle_timeout, 1.0)
            bar_length = 20
            filled = int(progress * bar_length)
            progress_bar = "█" * filled + "░" * (bar_length - filled)

            claude_status = "running" if claude_running else "not found"
            status_msg = f"{spinner} Waiting... Idle: {idle_time:.1f}/{idle_timeout}s | Claude: {claude_status} [{progress_bar}]"
            print(f"\r\033[2K{status_msg}", end='', flush=True)
            logger.debug(f"Waiting. Idle: {idle_time:.0f}s, Claude: {claude_running}")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by user (Ctrl+C)")
    logger.info("Stopped by user (Ctrl+C)")
except Exception as e:
    print(f"\nError: {e}")
    logger.error("Exception: %s", e, exc_info=True)
finally:
    # Stop visual indicator
    if 'indicator_process' in locals():
        stop_indicator(indicator_process)
