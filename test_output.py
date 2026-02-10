#!/usr/bin/env python3
"""Test script to check if carriage return works in terminal"""
import sys
import time

print("Testing carriage return...")
print("This line should update in place:")
print()

for i in range(10):
    msg = f"Counter: {i} | Progress: {'█' * i}{'░' * (10-i)}"
    sys.stdout.write(f"\r\033[K{msg}")
    sys.stdout.flush()
    time.sleep(0.5)

print("\n\nDone! If you saw counter updating on ONE line - it works!")
print("If you saw multiple lines - there's a terminal issue.")
