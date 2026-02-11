# Changelog

All notable changes to POWERJET Auto-Clicker will be documented in this file.

© 2026 Sergii Sliusar <powerjet777@gmail.com>

## [1.2.0] - 2026-02-11

### Added
- Comprehensive test suite with pytest
  - Unit tests for all major components
  - Test coverage for argument parsing
  - Process detection tests with mocking
  - Activity tracking and idle detection tests
  - Progress bar and spinner tests
  - Logging configuration tests
  - Screen coordinate calculation tests
  - Click sequence execution tests
- Test infrastructure
  - pytest configuration (pytest.ini)
  - Test fixtures (conftest.py)
  - Automated test runner script (run_tests.sh)
- Testing documentation (docs/TESTING.md)
  - Complete testing guide
  - Coverage instructions
  - Best practices for writing tests
- Test dependencies in requirements.txt
  - pytest >= 7.4.0
  - pytest-cov >= 4.1.0
  - pytest-mock >= 3.11.1

### Changed
- Updated .gitignore to exclude test artifacts
- Updated README with Testing section
- Updated project structure documentation

## [1.1.1] - 2026-02-11

### Added
- Log rotation with automatic file size management
  - Maximum ~10,000 lines per log file (~1 MB)
  - Keeps 2 backup files (clicker.log.1, clicker.log.2)
  - Prevents unlimited log growth

### Changed
- Replaced basic logging with RotatingFileHandler
- Logger now properly manages log file size

## [1.1.0] - 2026-02-11

### Added
- Comprehensive documentation in `docs/` folder
  - INSTALL.md - Detailed installation guide
  - USAGE.md - Complete usage documentation
- Installation automation script (`install.sh`)
- Python dependencies file (`requirements.txt`)
- Visual progress bar showing idle time
- Clean screen refresh after each click
- Animated spinner for waiting status

### Changed
- Improved UI with compact header
- Status line updates in place during waiting
- Screen clears and redraws after clicks
- Increased Enter key press delay to 0.5s
- Updated README with quick install instructions

### Fixed
- Status line no longer proliferates downward
- Better timing for Enter key press
- Cleaner visual output

## [1.0.0] - 2026-02-10

### Added
- Initial release
- Auto-click functionality on idle detection
- Claude process detection
- Configurable idle timeout via command-line arguments
- Visual indicator for click position (indicator.py)
- Comprehensive logging to clicker.log
- Spinner animation during waiting
- Mouse and keyboard activity monitoring
- POWERJET branding and logo

### Features
- Default 20-second idle timeout
- Fast mode with customizable timeout (-f flag)
- Automatic process detection for Claude
- Real-time status display
- Log file with timestamps
- Graceful shutdown with Ctrl+C
