# Click-o-Mania (Memory Match) – Tkinter Edition

A polished Tkinter implementation of the classic 4×4 memory-matching mini-game.

- **Goal:** Match all pairs within **25 turns**.
- **Rules:** Each turn, flip exactly two tiles. A matched pair stays revealed; a mismatch flips back.
- **Reset:** Click **Reset** anytime to start a fresh game.

## Features
- 4×4 grid, **8 color pairs** randomized on each run
- **25-turn** limit with live counters (turns left & matched pairs)
- Minimal, responsive UI (buttons auto-update between hidden/matched states)
- Clean separation of **pure core logic** vs. **UI**
- Unit tests for the core logic

## Tech
- Python 3.10+ (standard library only: `tkinter`, `random`, etc.)
- No third-party dependencies

## Run

```bash
# Option A: module entry
python -m clickomania

# Option B: explicit
python src/clickomania/main.py
