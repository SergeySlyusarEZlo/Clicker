#!/bin/bash

# POWERJET Auto-Clicker Test Runner
# © 2026 Sergii Sliusar <powerjet777@gmail.com>

set -e

echo "============================================================"
echo "    POWERJET Auto-Clicker - Test Suite"
echo "    © 2026 Sergii Sliusar"
echo "============================================================"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest is not installed."
    echo "Installing test dependencies..."
    pip3 install pytest pytest-cov pytest-mock
    echo ""
fi

# Run tests with coverage
echo "Running tests with coverage..."
echo ""

pytest -v --cov=. --cov-report=term-missing --cov-report=html \
    --tb=short \
    tests/

EXIT_CODE=$?

echo ""
echo "============================================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed!"
    echo ""
    echo "Coverage report generated:"
    echo "  - Terminal: See above"
    echo "  - HTML: Open htmlcov/index.html in browser"
else
    echo "❌ Some tests failed"
    echo ""
    echo "Check the output above for details"
fi

echo "============================================================"

exit $EXIT_CODE
