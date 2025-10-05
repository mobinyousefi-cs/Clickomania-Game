#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Click-o-Mania (Memory Match) – Tkinter Edition
File: ui.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-05
Updated: 2025-10-05
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Tkinter UI for Click-o-Mania. Binds button clicks to the core logic, handles resets,
and shows game status (turns, matches). Uses a 4x4 grid with gray hidden tiles.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple

from .core import GameConfig, GameState, new_game, flip_tile, try_resolve_turn


class ClickOManiaApp(tk.Frame):
    HIDDEN_COLOR = "#9CA3AF"  # gray-400
    TILE_SIZE = 90
    PAD = 8
    DELAY_MS = 450  # hide delay for non-matching pair

    def __init__(self, master: tk.Misc, *, cfg: Optional[GameConfig] = None):
        super().__init__(master, padx=12, pady=12)
        self.master = master
        self.cfg = cfg or GameConfig()
        self.grid(sticky="nsew")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Top panel: stats + reset
        self.header = tk.Frame(self)
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header.columnconfigure(0, weight=1)

        self.lbl_status = tk.Label(self.header, text="", font=("Segoe UI", 12, "bold"))
        self.lbl_status.grid(row=0, column=0, sticky="w")

        self.btn_reset = tk.Button(self.header, text="Reset", command=self.reset_game, width=10)
        self.btn_reset.grid(row=0, column=1, sticky="e")

        # Board
        self.board_frame = tk.Frame(self)
        self.board_frame.grid(row=1, column=0)

        # Footer
        self.footer = tk.Frame(self)
        self.footer.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.lbl_hint = tk.Label(
            self.footer,
            text="Rule: Reveal two tiles per turn. Match all pairs within 25 turns to win.",
        )
        self.lbl_hint.pack(anchor="w")

        self.buttons = []  # type: list[list[tk.Button]]
        self.state: GameState = new_game(self.cfg)
        self._pending_hide: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None

        self._build_grid()
        self._refresh_status()

    # --- UI building ---

    def _build_grid(self) -> None:
        for w in self.board_frame.winfo_children():
            w.destroy()
        self.buttons.clear()

        for r in range(self.cfg.rows):
            row_btns = []
            for c in range(self.cfg.cols):
                btn = tk.Button(
                    self.board_frame,
                    width=6,
                    height=3,
                    relief="raised",
                    bg=self.HIDDEN_COLOR,
                    activebackground=self.HIDDEN_COLOR,
                    command=lambda rr=r, cc=c: self.on_tile_click(rr, cc),
                )
                btn.grid(row=r, column=c, padx=self.PAD, pady=self.PAD)
                row_btns.append(btn)
            self.buttons.append(row_btns)

    # --- Interactions ---

    def on_tile_click(self, r: int, c: int) -> None:
        if self.state.won or self.state.lost:
            return

        if not flip_tile(self.state, r, c):
            return

        self._paint_tile(r, c)

        if self.state.first_pick is None:
            # First selection of the turn
            self.state.first_pick = (r, c)
        else:
            # Second selection: attempt to resolve
            r1, c1 = self.state.first_pick
            self.state.first_pick = None

            # Delay resolution visually so the player can see the second tile
            self.after(self.DELAY_MS, lambda: self._resolve_pair((r1, c1), (r, c)))

    def _resolve_pair(self, pick1: Tuple[int, int], pick2: Tuple[int, int]) -> None:
        (r1, c1), (r2, c2) = pick1, pick2
        is_match, game_over = try_resolve_turn(self.state, r2, c2)

        if not is_match:
            # hide colors back to gray
            self._paint_tile(r1, c1)
            self._paint_tile(r2, c2)

        self._refresh_status()

        if game_over:
            if self.state.won:
                messagebox.showinfo("You Win!", f"All pairs matched with {self.state.turns_left} turns left. 🎉")
            elif self.state.lost:
                messagebox.showwarning("Game Over", "No turns left. Try again!")

    def reset_game(self) -> None:
        self.state = new_game(self.cfg)
        self._build_grid()
        self._refresh_status()

    # --- Rendering helpers ---

    def _paint_tile(self, r: int, c: int) -> None:
        btn = self.buttons[r][c]
        if self.state.matched[r][c] or self.state.revealed[r][c]:
            btn.configure(bg=self.state.board[r][c], activebackground=self.state.board[r][c], relief="sunken")
        else:
            btn.configure(bg=self.HIDDEN_COLOR, activebackground=self.HIDDEN_COLOR, relief="raised")

    def _refresh_status(self) -> None:
        for r in range(self.cfg.rows):
            for c in range(self.cfg.cols):
                self._paint_tile(r, c)

        self.lbl_status.configure(
            text=(
                f"Turns Left: {self.state.turns_left}    "
                f"Matched: {self.state.matched_pairs}/{self.state.total_pairs}"
            )
        )
