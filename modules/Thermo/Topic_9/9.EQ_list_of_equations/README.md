# 9.EQ — List of Equations (Topic 9)

Support module for **Topic 9 (Power & Refrigeration Cycles)**: the topic's equations,
cited and **machine-verified**. Parallels `7.EQ`, `13.EQ`.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a
  book-verified value, then imports **all six** concept modules (`09.1`–`09.6`) and
  asserts each computes the same thing.

## Scope
Carnot ceiling `η_max = 1 − T_C/T_H`; mean effective pressure (Eq. 9.1); Otto
(Eqs. 9.3, 9.6–9.8), Diesel (9.11, 9.13), and dual (9.14 + closed form) piston cycles;
Brayton component works/heats, η, bwr, cold-air temperatures, `η = 1 − 1/r_p^((k−1)/k)`,
regenerator effectiveness (9.15–9.20, 9.23–9.25, 9.27); Rankine component balances,
η, bwr, and the pump-work approximation (8.1–8.6, 8.7b).

## Run
```bash
cd code
python3 equations.py          # print the cited registry (27 equations)
python3 test_equations.py     # 27 value + 33 cross-module checks -> "All 60 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
