# 7.EQ — List of Equations (Topic 7)

Support module for **Topic 7 (Performance Metrics)**: the topic's equations, cited and
**machine-verified**. Parallels `3.EQ`, `4.EQ`.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a
  book-verified value, then imports the concept module `07.1` and asserts it computes
  the same thing.

## Scope
Thermal efficiency `η = W/Q_in = 1 − Q_out/Q_in`; refrigerator and heat-pump COPs
`β = Q_C/W`, `γ = Q_H/W` (`γ = β + 1`); the Carnot ceilings `η_max`, `β_max`, `γ_max`;
and the isentropic turbine/nozzle/compressor efficiencies.

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 10 value + 10 cross-module checks -> "All 20 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
