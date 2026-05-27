#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║     CONWAY'S GAME OF LIFE — Iterative Demonstration         ║
║     RISC-V High Precision Code Base Challenge               ║
╚══════════════════════════════════════════════════════════════╝

Language : Python 3  (scripted / interpreted)
Algorithm: ITERATION — every generation, the program iterates
           over every cell in the grid and applies four simple
           rules.  No recursion; all state transitions are
           driven by loops.

Conway's Four Rules (applied simultaneously to all cells):
  1. Live cell, < 2 live neighbours  → dies  (underpopulation)
  2. Live cell, 2–3 live neighbours  → lives (survival)
  3. Live cell, > 3 live neighbours  → dies  (overpopulation)
  4. Dead cell, exactly 3 neighbours → born  (reproduction)

Included start patterns (selectable at runtime):
  • Random   – random 30 % fill
  • Glider   – small 5-cell ship that travels diagonally
  • Blinker  – period-2 oscillator
  • Gosper Glider Gun – infinite glider factory

Run:  python3 game_of_life.py
"""

import time
import os
import random
import sys

# ── Configuration ─────────────────────────────────────────────
WIDTH      = 60    # grid columns
HEIGHT     = 22    # grid rows
DELAY      = 0.08  # seconds between generations
MAX_GENS   = 500   # stop automatically after this many generations

# Cell characters
ALIVE = "█"
DEAD  = "·"


# ── Grid helpers ──────────────────────────────────────────────

def make_grid() -> list[list[bool]]:
    """Return a blank (all-dead) HEIGHT×WIDTH grid."""
    return [[False] * WIDTH for _ in range(HEIGHT)]


def clear():
    """Cross-platform terminal clear."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ── Start patterns ────────────────────────────────────────────
# Each pattern is a list of (row, col) offsets for live cells.

PATTERNS: dict[str, list[tuple[int, int]]] = {
    "glider": [
        (0, 1), (1, 2), (2, 0), (2, 1), (2, 2),
    ],
    "blinker": [
        (0, 0), (0, 1), (0, 2),
    ],
    "gosper_gun": [
        # Left square
        (5,1),(5,2),(6,1),(6,2),
        # Left part of gun
        (5,11),(6,11),(7,11),(4,12),(8,12),(3,13),(9,13),(3,14),(9,14),
        (6,15),(4,16),(8,16),(5,17),(6,17),(7,17),(6,18),
        # Right part of gun
        (3,21),(4,21),(5,21),(3,22),(4,22),(5,22),(2,23),(6,23),
        (1,25),(2,25),(6,25),(7,25),
        # Right square
        (3,35),(4,35),(3,36),(4,36),
    ],
}


def place_pattern(grid: list[list[bool]],
                  name: str,
                  origin_r: int = 2,
                  origin_c: int = 2) -> list[list[bool]]:
    """Stamp a named pattern onto the grid at (origin_r, origin_c)."""
    for (dr, dc) in PATTERNS[name]:
        r = (origin_r + dr) % HEIGHT
        c = (origin_c + dc) % WIDTH
        grid[r][c] = True
    return grid


def random_grid() -> list[list[bool]]:
    """
    Fill grid randomly with ≈30 % live cells.
    ITERATION: nested loops touch every cell exactly once.
    """
    grid = make_grid()
    # ── ITERATION over all rows ──────────────────────────────
    for r in range(HEIGHT):
        # ── ITERATION over all columns ───────────────────────
        for c in range(WIDTH):
            grid[r][c] = random.random() < 0.30
        # ── End column iteration ─────────────────────────────
    # ── End row iteration ────────────────────────────────────
    return grid


# ════════════════════════════════════════════════════════════════
#  ★  ITERATIVE CORE — neighbour counting
#
#  count_neighbours() examines the 8 cells surrounding (r, c).
#  The grid wraps (toroidal topology), so edges connect to the
#  opposite side — no special boundary handling needed.
#
#  ITERATION: a 3×3 loop over offsets {-1, 0, +1}² minus (0,0).
# ════════════════════════════════════════════════════════════════

def count_neighbours(grid: list[list[bool]], r: int, c: int) -> int:
    """
    Count live neighbours of cell (r, c) using 8-connectivity.

    ITERATION: loops over all 9 offsets and skips the cell itself.
    Wrap-around uses the modulo operator (%) — toroidal grid.
    """
    count = 0

    # ── ITERATION over 3×3 neighbourhood offsets ─────────────
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue                             # skip self
            nr = (r + dr) % HEIGHT                  # wrap row
            nc = (c + dc) % WIDTH                   # wrap column
            if grid[nr][nc]:
                count += 1
    # ── End neighbourhood iteration ──────────────────────────

    return count


# ════════════════════════════════════════════════════════════════
#  ★  ITERATIVE CORE — generation step
#
#  next_gen() computes the entire next generation in one pass.
#  It ITERATES over every cell, applies the four Conway rules,
#  and writes results into a fresh grid (avoids in-place mutation
#  which would corrupt neighbour counts mid-sweep).
#
#  Time  complexity: O(HEIGHT × WIDTH) per generation
#  Space complexity: O(HEIGHT × WIDTH) for the two grids
# ════════════════════════════════════════════════════════════════

def next_gen(grid: list[list[bool]]) -> list[list[bool]]:
    """
    Apply Conway's four rules to produce the next generation.

    ITERATION: two nested loops cover every cell in the universe.
    """
    new = make_grid()   # blank canvas for the next state

    # ── OUTER ITERATION: row by row ──────────────────────────
    for r in range(HEIGHT):

        # ── INNER ITERATION: column by column (cell by cell) ─
        for c in range(WIDTH):
            alive = grid[r][c]
            n     = count_neighbours(grid, r, c)

            # Apply Conway's rules
            if alive:
                # Rule 1: underpopulation
                # Rule 2: survival
                # Rule 3: overpopulation
                new[r][c] = (n == 2 or n == 3)
            else:
                # Rule 4: reproduction
                new[r][c] = (n == 3)
        # ── End inner iteration ──────────────────────────────

    # ── End outer iteration ──────────────────────────────────
    return new


# ── Statistics helper ─────────────────────────────────────────

def count_alive(grid: list[list[bool]]) -> int:
    """Count live cells — single-expression generator iteration."""
    # ITERATION: generator expression walks all cells
    return sum(grid[r][c] for r in range(HEIGHT) for c in range(WIDTH))


# ── Renderer ──────────────────────────────────────────────────

def render(grid: list[list[bool]], generation: int, alive: int) -> None:
    """
    Print the grid as ASCII art with a status header.
    ITERATION: nested loops stringify every cell.
    """
    border = "═" * (WIDTH + 2)
    print(f"╔{border}╗")
    status = f" Conway's Game of Life │ Gen: {generation:4d} │ Alive: {alive:4d} "
    print(f"║{status:^{WIDTH + 2}}║")
    print(f"╠{border}╣")

    # ── ITERATION: draw each row ─────────────────────────────
    for r in range(HEIGHT):
        row_str = "║"
        # ── ITERATION: draw each cell in the row ─────────────
        for c in range(WIDTH):
            row_str += ALIVE if grid[r][c] else DEAD
        # ── End cell iteration ───────────────────────────────
        row_str += "║"
        print(row_str)
    # ── End row iteration ────────────────────────────────────

    print(f"╚{border}╝")
    print("  Ctrl-C to quit  │  toroidal (wrap-around) grid")


# ── Entry point ───────────────────────────────────────────────

def choose_pattern() -> list[list[bool]]:
    """Interactive pattern selector."""
    menu = {
        "1": ("Random (30 % fill)",   lambda: random_grid()),
        "2": ("Glider",               lambda: place_pattern(make_grid(), "glider",
                                                            HEIGHT // 2 - 1, 5)),
        "3": ("Blinker (oscillator)", lambda: place_pattern(make_grid(), "blinker",
                                                            HEIGHT // 2, WIDTH // 2)),
        "4": ("Gosper Glider Gun",    lambda: place_pattern(make_grid(), "gosper_gun",
                                                            1, 1)),
    }
    print("\n  Conway's Game of Life — Pattern Menu")
    print("  " + "─" * 38)
    for key, (label, _) in menu.items():
        print(f"    {key}. {label}")
    print("  " + "─" * 38)

    try:
        choice = input("  Select [1-4, default=1]: ").strip() or "1"
    except (EOFError, KeyboardInterrupt):
        choice = "1"

    if choice not in menu:
        choice = "1"
    label, factory = menu[choice]
    print(f"\n  Starting with: {label}\n")
    time.sleep(0.6)
    return factory()


def main() -> None:
    grid       = choose_pattern()
    generation = 0

    try:
        # ── MAIN LOOP: iterate through generations ────────────
        # ITERATION: each loop body is one full generation step
        while generation < MAX_GENS:
            alive = count_alive(grid)

            clear()
            render(grid, generation, alive)

            # Extinction check
            if alive == 0:
                print("\n  💀  All cells died — simulation ended.")
                break

            # Advance one generation (the iterative core)
            grid       = next_gen(grid)
            generation += 1

            time.sleep(DELAY)
        # ── End generation loop ───────────────────────────────

        if generation >= MAX_GENS:
            print(f"\n  ⏹  Reached generation limit ({MAX_GENS}).")

    except KeyboardInterrupt:
        pass

    alive = count_alive(grid)
    print(f"\n  Stopped at generation {generation}  │  "
          f"Final alive count: {alive}\n")


if __name__ == "__main__":
    main()
