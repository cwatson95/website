# 10.EQ — List of Equations (Topic 10)

Support module for **Topic 10 (Engines)**: the topic's equations, cited and
**machine-verified**. Parallels `3.EQ`, `7.EQ`.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a
  book-verified value, then imports BOTH concept modules (`10.1` Carnot engine,
  `10.2` Stirling engine) and asserts they compute the same thing.

## Scope
The Carnot ceilings `η_max = 1 − T_C/T_H`, `β_max`, `γ_max` (Eqs. 5.9–5.11); the
Kelvin-scale ratio `(Q_C/Q_H)_rev = T_C/T_H` (Eq. 5.7); the isothermal ideal-gas
heat/work `Q = W = RT ln(V₂/V₁)` (Eq. 2.17 form); the ideal Stirling efficiency
(**= Carnot**, §9.8.4); the regenerator duty `c_v(T_H−T_C)` and effectiveness
(Eq. 9.27). Eqs. 5.9–5.11 also live in `3.EQ`/`7.EQ` — same citations, each topic
cross-checking its own concept modules.

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 14 value + 14 cross-module checks -> "All 28 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
