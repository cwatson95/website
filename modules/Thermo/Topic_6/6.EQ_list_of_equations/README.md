# 6.EQ — List of Equations (Topic 6)

Support module for **Topic 6 (Processes & Idealizations)**: the topic's equations, cited
and **machine-verified**. Parallels `Topic_3/3.EQ` and `Topic_13/13.EQ`.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a known
  value, then imports the concept modules `6.1`–`6.5` and asserts they compute the same
  thing (so a formula change anywhere fails this test).

## Scope
Reversible heat `Q = ∫T dS` and `dS = δQ/T` (6.1); the entropy balance, the increase-of-
entropy principle, and incompressible `Δs` (6.2); the isentropic ideal-gas relations
`T₂/T₁=(p₂/p₁)^((k−1)/k)`, `pv^k=const`, and the isentropic turbine efficiency (6.3); the
steady-state energy rate balance (6.4); the mass flow rate and steady mass balance (6.5).

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 13 value + 13 cross-module checks -> "All 26 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
