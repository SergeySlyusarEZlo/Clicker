# Testing Guide

Comprehensive testing guide for POWERJET Auto-Clicker.

© 2026 Sergii Sliusar <powerjet777@gmail.com>

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [Test Structure](#test-structure)

## Overview

The project uses `pytest` for testing with the following coverage:

- Command-line argument parsing
- Process detection (Claude process)
- Activity tracking and idle detection
- Progress bar generation
- Spinner animation
- Logging configuration
- Screen coordinate calculations
- Click sequence execution

## Installation

Install testing dependencies:

```bash
# Install all dependencies including test tools
pip3 install -r requirements.txt

# Or install only test dependencies
pip3 install pytest pytest-cov pytest-mock
```

## Running Tests

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_clicker.py

# Run specific test class
pytest tests/test_clicker.py::TestClickerArguments

# Run specific test
pytest tests/test_clicker.py::TestClickerArguments::test_default_timeout
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

### Run with Output

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

## Test Coverage

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser

# Terminal coverage report
pytest --cov=. --cov-report=term

# Coverage with missing lines
pytest --cov=. --cov-report=term-missing
```

### Coverage Targets

Current test coverage:
- Argument parsing: 100%
- Process detection: 100%
- Activity tracking: 100%
- Progress bar: 100%
- Spinner: 100%
- Logging: 90%
- Coordinates: 100%
- Click sequence: 100%

Overall target: >85% coverage

## Writing Tests

### Test Structure

```python
import unittest
from unittest.mock import patch, Mock

class TestNewFeature(unittest.TestCase):
    """Test description"""

    def test_basic_functionality(self):
        """Test basic case"""
        # Arrange
        expected = "value"

        # Act
        result = function_to_test()

        # Assert
        self.assertEqual(result, expected)

    @patch('module.function')
    def test_with_mock(self, mock_func):
        """Test with mocked dependency"""
        mock_func.return_value = "mocked"

        result = function_that_calls_mocked()

        self.assertEqual(result, "mocked")
        mock_func.assert_called_once()
```

### Using Fixtures

```python
def test_with_fixture(self, mock_screen_size):
    """Test using pytest fixture"""
    width, height = mock_screen_size
    self.assertEqual(width, 1920)
```

### Best Practices

1. **One assertion per test** (when possible)
2. **Clear test names** describing what is tested
3. **Use mocks** for external dependencies
4. **Test edge cases** and error conditions
5. **Keep tests independent** - no shared state
6. **Use fixtures** for common test data

## Test Structure

```
tests/
├── __init__.py           # Test package initialization
├── conftest.py           # Pytest fixtures and configuration
└── test_clicker.py       # Main test file
    ├── TestClickerArguments    # Argument parsing tests
    ├── TestProcessDetection    # Process detection tests
    ├── TestActivityTracking    # Activity tracking tests
    ├── TestProgressBar         # Progress bar tests
    ├── TestSpinner            # Spinner animation tests
    ├── TestLogging            # Logging configuration tests
    ├── TestScreenCoordinates  # Screen coordinate tests
    └── TestClickSequence      # Click sequence tests
```

## Test Categories

### Unit Tests

Test individual functions and components in isolation:
- Argument parsing
- Progress bar generation
- Spinner rotation
- Coordinate calculation

### Integration Tests

Test interaction between components:
- Complete click workflow
- Event handlers with activity tracking
- Logging with file system

### Mock Tests

Tests using mocks for external dependencies:
- Process detection (subprocess)
- GUI automation (pyautogui)
- Time-based operations

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Add current directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### Display Issues

Tests run in headless mode. If GUI tests fail:
```bash
# Use Xvfb for headless testing
xvfb-run pytest
```

### Permission Errors

Some tests may need special permissions:
```bash
# Run with proper permissions
sudo -E pytest
```

## Examples

### Running Quick Tests

```bash
# Fast feedback during development
pytest -x --tb=short
```

### Full Test Suite

```bash
# Complete test run with coverage
pytest -v --cov=. --cov-report=html --cov-report=term
```

### Debug Failing Test

```bash
# Run with debugger
pytest --pdb tests/test_clicker.py::TestName::test_method

# Show more context
pytest -vv --tb=long
```

## Test Metrics

Track these metrics:
- **Coverage**: Percentage of code tested
- **Pass rate**: Percentage of tests passing
- **Execution time**: Time to run full suite
- **Flakiness**: Tests that fail intermittently

## Support

For testing issues:
- Check [USAGE.md](USAGE.md) for setup
- Review [INSTALL.md](INSTALL.md) for dependencies
- Contact: powerjet777@gmail.com
- GitHub: https://github.com/SergeySlyusarEZlo/Clicker/issues
