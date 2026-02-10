#!/usr/bin/env python3
"""Visual indicator showing target click position"""
import tkinter as tk
import sys

def create_indicator(x, y, size=30):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.6)

    window_size = size + 10
    root.geometry(f"{window_size}x{window_size}+{x - window_size//2}+{y - window_size//2}")

    canvas = tk.Canvas(root, width=window_size, height=window_size,
                      bg='black', highlightthickness=0)
    canvas.pack()

    # Draw white circle with red outline
    margin = 5
    canvas.create_oval(margin, margin, window_size-margin, window_size-margin,
                      fill='white', outline='red', width=2)

    # Add crosshair
    center = window_size // 2
    canvas.create_line(center, margin, center, window_size-margin, fill='red', width=1)
    canvas.create_line(margin, center, window_size-margin, center, fill='red', width=1)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    x = int(sys.argv[1])
    y = int(sys.argv[2])
    create_indicator(x, y)
