# 1.EQ — List of Equations (Topic 1)

A support module for **Topic 1 (Foundations)**: the canonical equations of the
topic, gathered in one place, **cited**, and **machine-verified**. Part of the
`1.EQ / 1.EP / 1.HP` support set described in `modules/Thermo/plan.txt`.

## What it does
- `equations.md` — the human-readable **list of equations** (form + Moran
  §/Eq/page + the function that implements each).
- `code/equations.py` — each equation as one documented, canonical function,
  plus a `REGISTRY` table.
- `code/test_equations.py` — a **verification hub**: it (1) checks every equation
  against a known value, and (2) imports the concept modules `1.1`, `1.2`, `1.4`,
  `1.5` and asserts they compute the **same** thing. This is how the topic keeps
  its equations consistent — change a formula in one module and this test fails.

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 16 value checks + 10 cross-module checks -> "All 26 tests passed."
```

## Scope
Covers the equations behind modules 1.1–1.5: specific volume/density, temperature
& pressure relations (Ch.1); kinetic/potential energy, the closed-system energy
balance, `∫p dV` and polytropic work (Ch.2); the mass rate balance, mass flow
rate, enthalpy, and the control-volume energy balance (Ch.4). Substance gas
constants `R` are in the cross-cutting **Constants** module.

## Files
`equations.md` (the list), `code/equations.py`, `code/test_equations.py`, `refs.md`.
