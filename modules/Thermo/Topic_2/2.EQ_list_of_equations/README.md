# 2.EQ — List of Equations (Topic 2)

Support module for **Topic 2 (Energy & Work)**: the topic's equations, cited and
**machine-verified**. Parallels `Topic_1/1.EQ`.

## What it does
- `equations.md` — the **list of equations** (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a
  known value, then imports the concept modules `2.1`–`2.6` and asserts they
  compute the same thing (so a formula change anywhere fails this test).

## Scope
Work definition & sign convention; the work modes (boundary `∫p dV`, shaft `τω`,
electric `−εi`, spring `½kx²`); power `F·V`; kinetic/potential energy; and the
total-energy decomposition `E = U + KE + PE`. The shared `∫p dV`, KE, PE forms
also appear in `1.EQ` (foundations); this module adds the work-mode/power/total-
energy content.

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 13 value + 14 cross-module checks -> "All 27 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
