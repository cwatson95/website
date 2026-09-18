# 4.EQ — List of Equations (Topic 4)

Support module for **Topic 4 (Properties & State Functions)**: the topic's equations,
cited and **machine-verified**. Parallels `1.EQ`, `2.EQ`, `3.EQ`.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a
  known value, then imports the concept modules `4.1`–`4.5` and asserts they compute
  the same thing.

## Scope
Enthalpy `h=u+pv`; quality and the `x`-weighted mixture relations; entropy change
(incompressible / ideal gas) and the entropy balance; exergy, exergy transfer, and
destruction `E_d=T₀σ`; the Gibbs phase rule `F=2+N−P`.

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 11 value + 9 cross-module checks -> "All 20 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
