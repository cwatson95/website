# 3.EQ — List of Equations (Topic 3)

Support module for **Topic 3 (The Laws)**: the topic's equations, cited and
**machine-verified**. Parallels `Topic_1/1.EQ` and `Topic_2/2.EQ`.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a
  known value, then imports the concept modules `3.1`–`3.4` and asserts they compute
  the same thing (so a formula change anywhere fails this test).

## Scope
Temperature scales (zeroth law); the closed-system & cycle energy balance (first
law); Carnot efficiency, the Kelvin ratio, and the max COPs (second law); and the
absolute-entropy datum (third law).

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 13 value + 12 cross-module checks -> "All 25 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
