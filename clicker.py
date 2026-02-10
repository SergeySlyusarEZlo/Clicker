#!/usr/bin/env python3
import pyautogui
import time
import logging
import subprocess
import argparse
import os
from pynput import mouse, keyboard

logging.basicConfig(filename='clicker.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

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

def reset_activity():
    global last_activity_time
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

    logging.info(f"Screen size: {screen_width}x{screen_height}")
    logging.info(f"Target position: {target_x}, {target_y}")
    logging.info(f"Idle timeout: {idle_timeout} seconds")

    # Start visual indicator in background
    indicator_process = None
    indicator_script = os.path.join(os.path.dirname(__file__), 'indicator.py')
    if os.path.exists(indicator_script):
        try:
            indicator_process = subprocess.Popen(
                ['python3', indicator_script, str(target_x), str(target_y)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logging.info("Visual indicator started")
        except Exception as e:
            logging.warning(f"Could not start visual indicator: {e}")

    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener.start()
    keyboard_listener.start()

    while True:
        idle_time = time.time() - last_activity_time
        claude_running = is_claude_running()

        if idle_time >= idle_timeout and claude_running:
            pyautogui.moveTo(target_x, target_y)
            time.sleep(0.3)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.2)

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
            print(f"\r{status_msg:<80}", end='', flush=True)
            logging.debug(f"Clicked! Idle: {idle_time:.0f}s, Claude: running")

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
            print(f"\r{status_msg:<80}", end='', flush=True)
            logging.debug(f"Waiting. Idle: {idle_time:.0f}s, Claude: {claude_running}")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by user (Ctrl+C)")
    logging.info("Stopped by user (Ctrl+C)")
except Exception as e:
    print(f"\nError: {e}")
    logging.error("Exception: %s", e, exc_info=True)
finally:
    # Stop visual indicator
    if 'indicator_process' in locals() and indicator_process:
        try:
            indicator_process.terminate()
            indicator_process.wait(timeout=2)
        except:
            pass
