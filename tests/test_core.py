#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Click-o-Mania (Memory Match) – Tkinter Edition
File: test_core.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-05
Updated: 2025-10-05
License: MIT License (see LICENSE file for details)
=========================================================================================================

Description:
Unit tests for the pure game core (no GUI).
"""

from __future__ import annotations

import random
from collections import Counter

from clickomania.core import GameConfig, generate_board, new_game, flip_tile, try_resolve_turn


def test_generate_board_pairs():
    rng = random.Random(1337)
    cfg = GameConfig()
    board = generate_board(cfg, rng=rng)
    flat = [c for row in board for c in row]
    counts = Counter(flat)
    # In 4x4 we should have 8 colors, each exactly twice
    assert len(counts) == 8
    assert all(v == 2 for v in counts.values())


def test_basic_flip_and_match_flow():
    rng = random.Random(42)
    cfg = GameConfig(turns=3)
    state = new_game(cfg, rng=rng)

    # Search for a known pair to test deterministic flow
    pos = {}
    for r, row in enumerate(state.board):
        for c, color in enumerate(row):
            pos.setdefault(color, []).append((r, c))

    # take the first color with two positions
    color, (a, b) = next((k, v) for k, v in pos.items() if len(v) == 2)

    # Flip first
    assert flip_tile(state, *a)
    state.first_pick = a
    # Flip second -> resolve
    assert flip_tile(state, *b)
    is_match, over = try_resolve_turn(state, *b)
    assert is_match is True
    assert over is False
    assert state.matched_pairs == 1
    assert state.turns_left == 2  # one turn consumed


def test_lose_when_turns_exhausted():
    rng = random.Random(123)
    cfg = GameConfig(turns=1)
    state = new_game(cfg, rng=rng)

    # Flip two different tiles with different colors (force mismatch)
    # Find two different colors
    coords = []
    colors = set()
    for r, row in enumerate(state.board):
        for c, col in enumerate(row):
            if len(colors) < 2 and col not in colors:
                colors.add(col)
                coords.append((r, c))
            if len(coords) == 2:
                break
        if len(coords) == 2:
            break

    a, b = coords
    assert flip_tile(state, *a)
    state.first_pick = a
    assert flip_tile(state, *b)
    is_match, over = try_resolve_turn(state, *b)
    assert is_match is False
    assert over is True
    assert state.lost is True
