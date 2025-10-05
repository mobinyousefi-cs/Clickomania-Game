#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Click-o-Mania (Memory Match) – Tkinter Edition
File: core.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-05
Updated: 2025-10-05
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Pure game logic (no GUI). Generates a 4x4 board of matched color pairs, tracks turns,
checks matches, and determines win/lose states. Designed to be unit-testable.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


Board = List[List[str]]  # 4x4 grid of color names


DEFAULT_COLORS = [
    "#EF4444",  # red
    "#F59E0B",  # amber
    "#10B981",  # emerald
    "#3B82F6",  # blue
    "#8B5CF6",  # violet
    "#EC4899",  # pink
    "#14B8A6",  # teal
    "#F97316",  # orange
]


@dataclass
class GameConfig:
    rows: int = 4
    cols: int = 4
    turns: int = 25
    colors: Tuple[str, ...] = tuple(DEFAULT_COLORS)


@dataclass
class GameState:
    board: Board
    revealed: List[List[bool]]
    matched: List[List[bool]]
    turns_left: int
    first_pick: Optional[Tuple[int, int]] = None
    matched_pairs: int = 0
    total_pairs: int = 8
    won: bool = False
    lost: bool = False


def generate_board(cfg: GameConfig, *, rng: Optional[random.Random] = None) -> Board:
    """Create a rows x cols grid with randomly placed color pairs."""
    rng = rng or random.Random()
    assert cfg.rows * cfg.cols % 2 == 0, "Board must contain an even number of tiles."

    # Select pairs: 8 unique colors for a 4x4.
    needed_pairs = (cfg.rows * cfg.cols) // 2
    if needed_pairs > len(cfg.colors):
        raise ValueError("Not enough unique colors to cover the board pairs.")

    chosen = list(cfg.colors[:needed_pairs])
    pairs = chosen * 2
    rng.shuffle(pairs)

    board: Board = []
    k = 0
    for _ in range(cfg.rows):
        row = []
        for _ in range(cfg.cols):
            row.append(pairs[k])
            k += 1
        board.append(row)
    return board


def new_game(cfg: GameConfig, *, rng: Optional[random.Random] = None) -> GameState:
    """Initialize a new game state."""
    board = generate_board(cfg, rng=rng)
    revealed = [[False for _ in range(cfg.cols)] for _ in range(cfg.rows)]
    matched = [[False for _ in range(cfg.cols)] for _ in range(cfg.rows)]
    return GameState(
        board=board,
        revealed=revealed,
        matched=matched,
        turns_left=cfg.turns,
        matched_pairs=0,
        total_pairs=(cfg.rows * cfg.cols) // 2,
        won=False,
        lost=False,
        first_pick=None,
    )


def within_bounds(state: GameState, r: int, c: int) -> bool:
    return 0 <= r < len(state.board) and 0 <= c < len(state.board[0])


def can_flip(state: GameState, r: int, c: int) -> bool:
    """Tile can be flipped if it's within bounds, not already matched, and not already revealed."""
    if not within_bounds(state, r, c):
        return False
    return not state.matched[r][c] and not state.revealed[r][c] and not state.won and not state.lost


def flip_tile(state: GameState, r: int, c: int) -> bool:
    """Reveal a tile if allowed; returns True if flip succeeded."""
    if not can_flip(state, r, c):
        return False
    state.revealed[r][c] = True
    return True


def try_resolve_turn(state: GameState, r2: int, c2: int) -> Tuple[bool, bool]:
    """
    Called after the second tile of a turn is revealed.
    Decrements turns, checks for a match, updates state.
    Returns (is_match, game_over_flag).
    """
    if state.first_pick is None:
        raise RuntimeError("Second flip called without a first_pick set.")

    r1, c1 = state.first_pick
    state.turns_left = max(0, state.turns_left - 1)
    is_match = state.board[r1][c1] == state.board[r2][c2]

    if is_match:
        state.matched[r1][c1] = True
        state.matched[r2][c2] = True
        state.matched_pairs += 1
        if state.matched_pairs == state.total_pairs:
            state.won = True
            return True, True
    else:
        # Hide both (UI should schedule the hide after a brief delay)
        state.revealed[r1][c1] = False
        state.revealed[r2][c2] = False

    if state.turns_left == 0 and not state.won:
        state.lost = True
        return is_match, True

    return is_match, False
