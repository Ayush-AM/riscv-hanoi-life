#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         TOWER OF HANOI — Recursive Demonstration             ║
║         RISC-V High Precision Code Base Challenge            ║
╚══════════════════════════════════════════════════════════════╝

Language : Python 3  (scripted / interpreted)
Algorithm: RECURSION — the solution naturally decomposes into
           three sub-problems of size (n-1), making it a
           textbook example of the divide-and-conquer paradigm.

Minimum moves to solve n disks = 2ⁿ − 1
  • 3 disks  →   7 moves
  • 5 disks  →  31 moves
  • 10 disks → 1023 moves

Run:  python3 hanoi.py
"""

import time
import os
import sys

# ── Configuration ────────────────────────────────────────────
NUM_DISKS = 5       # change this (try 3–7) to vary complexity
DELAY     = 0.35    # seconds between moves (0 = instant)
PEG_NAMES = ('A', 'B', 'C')

# ── State: three pegs stored as Python lists (stacks) ────────
# Index 0 = bottom of peg, last index = top of peg
pegs: dict[str, list[int]] = {
    'A': list(range(NUM_DISKS, 0, -1)),   # largest disk at bottom
    'B': [],
    'C': [],
}

move_count = 0   # global counter incremented on every disk move


# ── Rendering helpers ─────────────────────────────────────────

def clear():
    """Cross-platform screen clear."""
    os.system('cls' if os.name == 'nt' else 'clear')


def draw_towers(last_move: str = ""):
    """
    ASCII-art renderer for the current peg state.
    ITERATION: nested loops walk every (row, peg) position.
    """
    col_w  = NUM_DISKS * 2 + 5   # width of one peg column
    border = "═" * (col_w * 3 + 4)

    print(f"╔{border}╗")
    title = f"  Tower of Hanoi │ Disks: {NUM_DISKS} │ Move: {move_count:3d}/{2**NUM_DISKS - 1}  "
    print(f"║{title:<{len(border)}}║")
    if last_move:
        print(f"║  {last_move:<{len(border)-2}}║")
    print(f"╠{border}╣")

    # ── ITERATION: draw rows top-to-bottom ─────────────────
    for row in range(NUM_DISKS, 0, -1):
        line = "║"
        for peg_name in PEG_NAMES:
            peg = pegs[peg_name]
            if row <= len(peg):
                disk = peg[row - 1]                    # disk number
                bar  = "▓" * (disk * 2 - 1)           # visual width ∝ disk size
                line += f"{bar:^{col_w}}"
            else:
                line += f"{'│':^{col_w}}"              # empty pole
        line += " ║"
        print(line)
    # ── End of row iteration ────────────────────────────────

    base = "▔" * (col_w - 2)
    print(f"║{'':3}{base:^{col_w}}{base:^{col_w}}{base:^{col_w}}  ║")
    labels = "".join(f"{'Peg ' + p:^{col_w}}" for p in PEG_NAMES)
    print(f"║{labels}  ║")
    print(f"╚{border}╝")


# ════════════════════════════════════════════════════════════════
#  ★  RECURSIVE CORE — Tower of Hanoi solver
#
#  move_disk(n, src, dst, aux) moves the top n disks from
#  peg `src` to peg `dst` using `aux` as a temporary buffer.
#
#  Recursion structure:
#  ┌──────────────────────────────────────────────────────────┐
#  │  move_disk(n, src, dst, aux)                             │
#  │    ├─ BASE CASE:  n == 0  →  return immediately          │
#  │    ├─ RECURSIVE CALL 1:                                  │
#  │    │    move_disk(n-1, src, aux, dst)   ← clear the way  │
#  │    ├─ DIRECT MOVE:                                       │
#  │    │    physically move disk n: src → dst                │
#  │    └─ RECURSIVE CALL 2:                                  │
#  │         move_disk(n-1, aux, dst, src)   ← stack back     │
#  └──────────────────────────────────────────────────────────┘
#
#  Call-stack depth  = n      (linear space)
#  Total moves made  = 2ⁿ − 1 (exponential time — optimal)
# ════════════════════════════════════════════════════════════════

def move_disk(n: int, src: str, dst: str, aux: str) -> None:
    """
    Recursively transfer n disks from peg `src` to peg `dst`.

    Parameters
    ----------
    n   : number of disks currently to be moved
    src : source peg name ('A', 'B', or 'C')
    dst : destination peg name
    aux : auxiliary (helper) peg name
    """
    global move_count

    # ── BASE CASE ────────────────────────────────────────────
    # When n reaches 0 there is nothing left to move.
    # This terminates all recursive branches.
    if n == 0:
        return
    # ── End base case ────────────────────────────────────────

    # ── RECURSIVE CALL 1 ─────────────────────────────────────
    # Move the top (n-1) disks out of the way so we can access
    # the nth (largest remaining) disk underneath them.
    # Note how src and dst swap roles vs the parent call.
    move_disk(n - 1, src, aux, dst)
    # ── End recursive call 1 ─────────────────────────────────

    # ── DIRECT MOVE (the actual disk transfer) ────────────────
    # Now that disk n is exposed on src, move it to dst.
    disk = pegs[src].pop()
    pegs[dst].append(disk)
    move_count += 1
    msg = f"Disk {disk} : Peg {src}  →  Peg {dst}"
    clear()
    draw_towers(msg)
    time.sleep(DELAY)
    # ── End direct move ───────────────────────────────────────

    # ── RECURSIVE CALL 2 ─────────────────────────────────────
    # The (n-1) disks we parked on `aux` must now be moved on
    # top of disk n which sits on `dst`.
    move_disk(n - 1, aux, dst, src)
    # ── End recursive call 2 ─────────────────────────────────


# ── Entry point ───────────────────────────────────────────────

def main() -> None:
    clear()
    print("\n  🗼  Tower of Hanoi — Recursive Demonstration  🗼")
    print(f"      Moving {NUM_DISKS} disks from Peg A → Peg C")
    print(f"      Minimum moves required : {2**NUM_DISKS - 1}\n")
    draw_towers("Initial state — all disks stacked on Peg A")
    time.sleep(1.8)

    # Kick off the recursion: move all NUM_DISKS from A to C via B
    move_disk(NUM_DISKS, 'A', 'C', 'B')

    print(f"\n  ✅  Solved in {move_count} moves  "
          f"(optimal minimum = {2**NUM_DISKS - 1})\n")


if __name__ == "__main__":
    main()
