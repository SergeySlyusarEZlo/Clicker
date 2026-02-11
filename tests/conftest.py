"""
Pytest configuration and fixtures for POWERJET Auto-Clicker

© 2026 Sergii Sliusar <powerjet777@gmail.com>
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def mock_screen_size():
    """Fixture for mocking screen size"""
    return (1920, 1080)


@pytest.fixture
def mock_large_screen_size():
    """Fixture for mocking large screen size"""
    return (3840, 1080)


@pytest.fixture
def idle_timeout_default():
    """Default idle timeout value"""
    return 20


@pytest.fixture
def idle_timeout_fast():
    """Fast mode idle timeout value"""
    return 1


@pytest.fixture
def spinner_characters():
    """Spinner animation characters"""
    return ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']


@pytest.fixture
def progress_bar_length():
    """Progress bar length"""
    return 20
