# RISC-V High Precision Code Base — Scripted Algorithm Demos

> **Coding Challenge**: Broadening the RISC-V High Precision Code Base and Reach
>
> Two classic algorithm demonstrations in **pure Python 3** — no external dependencies.
> Each script runs in any terminal and renders live ASCII graphics.

---

## 📁 Repository Contents

| File | Algorithm | Key Concept |
|------|-----------|-------------|
| [`hanoi.py`](hanoi.py) | Tower of Hanoi | **Recursion** |
| [`game_of_life.py`](game_of_life.py) | Conway's Game of Life | **Iteration** |

---

## 🗼 Tower of Hanoi (`hanoi.py`)

### What it demonstrates — **RECURSION**

The Tower of Hanoi is the canonical teaching example of **divide-and-conquer recursion**.  
Moving `n` disks reduces to three sub-problems:

```
move_disk(n, src, dst, aux):
    ├─ BASE CASE  : n == 0  → return          (stops infinite regression)
    ├─ RECURSIVE 1: move_disk(n-1, src, aux, dst)   ← clear the way
    ├─ DIRECT MOVE: physically transfer disk n from src to dst
    └─ RECURSIVE 2: move_disk(n-1, aux, dst, src)   ← stack back
```

| Property | Value |
|----------|-------|
| Call-stack depth | O(n) — linear |
| Total moves | 2ⁿ − 1 — optimal, exponential |
| Disks in demo | 5 (31 moves) |

### Running

```bash
python3 hanoi.py
```

### Sample output

```
╔══════════════════════════════════════════════╗
║  Tower of Hanoi │ Disks: 5 │ Move:   7/31   ║
║  Disk 3 : Peg A  →  Peg C                   ║
╠══════════════════════════════════════════════╣
       │             │             │
       │             │             │
      ▓▓▓            │             │
    ▓▓▓▓▓▓▓          │             │
  ▓▓▓▓▓▓▓▓▓▓▓        │          ▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      │        ▓▓▓▓▓▓▓▓▓
▔▔▔▔▔▔▔▔▔▔▔   ▔▔▔▔▔▔▔▔▔▔▔   ▔▔▔▔▔▔▔▔▔▔▔
    Peg A         Peg B         Peg C
```

---

## 🌱 Conway's Game of Life (`game_of_life.py`)

### What it demonstrates — **ITERATION**

The simulation advances generation by generation.  
Every generation **iterates** over every cell and applies four deterministic rules:

| Rule | Condition | Outcome |
|------|-----------|--------|
| 1 | Live cell, < 2 live neighbours | Dies (underpopulation) |
| 2 | Live cell, 2–3 live neighbours | Survives |
| 3 | Live cell, > 3 live neighbours | Dies (overpopulation) |
| 4 | Dead cell, exactly 3 neighbours | Born (reproduction) |

```
next_gen():
    for row in range(HEIGHT):          ← OUTER ITERATION
        for col in range(WIDTH):       ← INNER ITERATION
            n = count_neighbours(...)
            apply rules 1–4
```

| Property | Value |
|----------|-------|
| Grid size | 60 × 22 cells |
| Per-generation cost | O(WIDTH × HEIGHT) |
| Topology | Toroidal (wrap-around edges) |

### Included start patterns

| Choice | Pattern | Behaviour |
|--------|---------|----------|
| 1 | Random (30 % fill) | Chaotic, self-organising |
| 2 | Glider | 5-cell spaceship, travels diagonally |
| 3 | Blinker | Period-2 oscillator |
| 4 | Gosper Glider Gun | Emits an infinite stream of gliders |

### Running

```bash
python3 game_of_life.py
```

---

## ⚙️ Requirements

- **Python 3.8+** — standard library only (`os`, `time`, `random`, `sys`)
- Any terminal that supports UTF-8 block characters
- Works on Linux, macOS, and Windows (cmd / PowerShell / Windows Terminal)

---

## 🔑 Key Concepts Highlighted in Code

Both scripts use **extensive inline comments** to flag every recursive call,
every base case, every iteration, and every loop boundary.

```python
# ── RECURSIVE CALL 1 ─────────────────────────────────────────
# Move the top (n-1) disks out of the way …
move_disk(n - 1, src, aux, dst)

# ── OUTER ITERATION: row by row ──────────────────────────────
for r in range(HEIGHT):
    # ── INNER ITERATION: column by column ────────────────────
    for c in range(WIDTH):
        …
```

---

## 🔗 Related

This repository is part of the **RISC-V High Precision Code Base** challenge series,
exploring how fundamental algorithms (recursion, iteration, divide-and-conquer)
translate across different execution environments — from scripted Python down
to bare-metal RISC-V assembly.

---

*License: MIT*
