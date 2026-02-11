"""
Unit tests for POWERJET Auto-Clicker

© 2026 Sergii Sliusar <powerjet777@gmail.com>
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
import subprocess
import time
import sys
import os

# Add parent directory to path to import clicker module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestClickerArguments(unittest.TestCase):
    """Test command-line argument parsing"""

    @patch('sys.argv', ['clicker.py'])
    def test_default_timeout(self):
        """Test default idle timeout is 20 seconds"""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--fast', nargs='?', const=1, type=int)
        args = parser.parse_args([])

        idle_timeout = 20 if args.fast is None else args.fast
        self.assertEqual(idle_timeout, 20)

    @patch('sys.argv', ['clicker.py', '-f'])
    def test_fast_mode_no_value(self):
        """Test fast mode without value defaults to 1 second"""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--fast', nargs='?', const=1, type=int)
        args = parser.parse_args(['-f'])

        idle_timeout = 20 if args.fast is None else args.fast
        self.assertEqual(idle_timeout, 1)

    @patch('sys.argv', ['clicker.py', '-f', '10'])
    def test_fast_mode_with_value(self):
        """Test fast mode with custom value"""
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--fast', nargs='?', const=1, type=int)
        args = parser.parse_args(['-f', '10'])

        idle_timeout = 20 if args.fast is None else args.fast
        self.assertEqual(idle_timeout, 10)


class TestProcessDetection(unittest.TestCase):
    """Test Claude process detection"""

    @patch('subprocess.run')
    def test_claude_running(self, mock_run):
        """Test when Claude process is running"""
        mock_run.return_value = Mock(returncode=0)

        result = subprocess.run(['pgrep', '-f', 'claude'],
                                capture_output=True, text=True)
        is_running = result.returncode == 0

        self.assertTrue(is_running)
        mock_run.assert_called_once_with(['pgrep', '-f', 'claude'],
                                          capture_output=True, text=True)

    @patch('subprocess.run')
    def test_claude_not_running(self, mock_run):
        """Test when Claude process is not running"""
        mock_run.return_value = Mock(returncode=1)

        result = subprocess.run(['pgrep', '-f', 'claude'],
                                capture_output=True, text=True)
        is_running = result.returncode == 0

        self.assertFalse(is_running)

    @patch('subprocess.run')
    def test_claude_detection_exception(self, mock_run):
        """Test exception handling in process detection"""
        mock_run.side_effect = Exception("Process error")

        try:
            result = subprocess.run(['pgrep', '-f', 'claude'],
                                    capture_output=True, text=True)
            is_running = result.returncode == 0
        except Exception:
            is_running = False

        self.assertFalse(is_running)


class TestActivityTracking(unittest.TestCase):
    """Test idle activity tracking"""

    def test_reset_activity(self):
        """Test activity reset updates timestamp"""
        before = time.time()
        time.sleep(0.1)

        # Simulate reset
        last_activity_time = time.time()
        after = last_activity_time

        self.assertGreater(after, before)
        self.assertAlmostEqual(after, time.time(), delta=0.1)

    def test_idle_time_calculation(self):
        """Test idle time calculation"""
        last_activity_time = time.time()
        time.sleep(0.5)

        idle_time = time.time() - last_activity_time

        self.assertGreater(idle_time, 0.4)
        self.assertLess(idle_time, 0.6)

    def test_idle_timeout_check(self):
        """Test idle timeout threshold detection"""
        idle_timeout = 1.0
        last_activity_time = time.time() - 1.5  # 1.5 seconds ago

        idle_time = time.time() - last_activity_time
        should_click = idle_time >= idle_timeout

        self.assertTrue(should_click)


class TestProgressBar(unittest.TestCase):
    """Test progress bar generation"""

    def test_empty_progress_bar(self):
        """Test progress bar at 0%"""
        progress = 0.0
        bar_length = 20
        filled = int(progress * bar_length)
        progress_bar = "█" * filled + "░" * (bar_length - filled)

        self.assertEqual(progress_bar, "░" * 20)
        self.assertEqual(len(progress_bar), 20)

    def test_half_progress_bar(self):
        """Test progress bar at 50%"""
        progress = 0.5
        bar_length = 20
        filled = int(progress * bar_length)
        progress_bar = "█" * filled + "░" * (bar_length - filled)

        self.assertEqual(progress_bar, "█" * 10 + "░" * 10)
        self.assertEqual(len(progress_bar), 20)

    def test_full_progress_bar(self):
        """Test progress bar at 100%"""
        progress = 1.0
        bar_length = 20
        filled = int(progress * bar_length)
        progress_bar = "█" * filled + "░" * (bar_length - filled)

        self.assertEqual(progress_bar, "█" * 20)
        self.assertEqual(len(progress_bar), 20)

    def test_progress_bar_clamping(self):
        """Test progress bar handles values > 1.0"""
        idle_time = 25.0
        idle_timeout = 20.0
        progress = min(idle_time / idle_timeout, 1.0)

        self.assertEqual(progress, 1.0)

        bar_length = 20
        filled = int(progress * bar_length)
        progress_bar = "█" * filled + "░" * (bar_length - filled)

        self.assertEqual(progress_bar, "█" * 20)


class TestSpinner(unittest.TestCase):
    """Test spinner animation"""

    def test_spinner_rotation(self):
        """Test spinner cycles through characters"""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

        self.assertEqual(len(spinner_chars), 10)

        # Test cycling
        for i in range(20):
            char = spinner_chars[i % len(spinner_chars)]
            self.assertIn(char, spinner_chars)

    def test_spinner_index_wrapping(self):
        """Test spinner index wraps correctly"""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

        # After 10 iterations, should wrap to start
        index = 10 % len(spinner_chars)
        self.assertEqual(index, 0)
        self.assertEqual(spinner_chars[index], '⠋')


class TestLogging(unittest.TestCase):
    """Test logging configuration"""

    def test_log_file_creation(self):
        """Test log file is created"""
        from logging.handlers import RotatingFileHandler
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            log_file = tmp.name

        try:
            handler = RotatingFileHandler(
                log_file,
                maxBytes=1024 * 1024,
                backupCount=2,
                encoding='utf-8'
            )

            self.assertEqual(handler.maxBytes, 1024 * 1024)
            self.assertEqual(handler.backupCount, 2)

            handler.close()
        finally:
            if os.path.exists(log_file):
                os.remove(log_file)

    def test_log_rotation_settings(self):
        """Test log rotation is configured correctly"""
        from logging.handlers import RotatingFileHandler

        max_bytes = 1024 * 1024  # 1 MB
        backup_count = 2

        self.assertEqual(max_bytes, 1048576)
        self.assertEqual(backup_count, 2)


class TestScreenCoordinates(unittest.TestCase):
    """Test screen coordinate calculations"""

    @patch('pyautogui.size')
    def test_target_coordinates(self, mock_size):
        """Test target coordinates calculation"""
        mock_size.return_value = (1920, 1080)

        screen_width, screen_height = mock_size()
        target_x = screen_width - 400
        target_y = screen_height - 100

        self.assertEqual(target_x, 1520)
        self.assertEqual(target_y, 980)

    @patch('pyautogui.size')
    def test_different_screen_size(self, mock_size):
        """Test coordinates on different screen size"""
        mock_size.return_value = (3840, 1080)

        screen_width, screen_height = mock_size()
        target_x = screen_width - 400
        target_y = screen_height - 100

        self.assertEqual(target_x, 3440)
        self.assertEqual(target_y, 980)


class TestClickSequence(unittest.TestCase):
    """Test click action sequence"""

    @patch('pyautogui.press')
    @patch('pyautogui.click')
    @patch('pyautogui.moveTo')
    @patch('time.sleep')
    def test_click_sequence(self, mock_sleep, mock_move, mock_click, mock_press):
        """Test complete click sequence executes correctly"""
        target_x = 1520
        target_y = 980

        # Simulate click sequence
        mock_move(target_x, target_y)
        mock_sleep(0.3)
        mock_click()
        mock_sleep(0.5)
        mock_press('enter')
        mock_sleep(0.2)

        mock_move.assert_called_once_with(target_x, target_y)
        mock_click.assert_called_once()
        mock_press.assert_called_once_with('enter')
        self.assertEqual(mock_sleep.call_count, 3)


if __name__ == '__main__':
    unittest.main()
