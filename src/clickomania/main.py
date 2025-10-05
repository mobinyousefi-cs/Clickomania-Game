#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Click-o-Mania (Memory Match) – Tkinter Edition
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-05
Updated: 2025-10-05
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
High-level runner that wires the pure game core to the Tkinter UI.
"""

from __future__ import annotations

import tkinter as tk

from .ui import ClickOManiaApp


def main() -> None:
    """Launch the Click-o-Mania application."""
    root = tk.Tk()
    root.title("Click-o-Mania — Mobin Yousefi")
    # Optional: set a reasonable min size for cleaner layout across platforms
    root.minsize(480, 520)
    app = ClickOManiaApp(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
