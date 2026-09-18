# 11.EQ — List of Equations (Topic 11)

Support module for **Topic 11 (Psychrometrics — Moist Air)**: the topic's equations,
cited and **machine-verified**. Parallels the `EQ` modules of other topics.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a known
  value, then imports the concept modules `11.1` (dry-bulb) and `11.2` (wet-bulb) and
  asserts they compute the same thing (so a formula change anywhere fails this test).

## Scope
The Moran Ch.12 moist-air set: humidity ratio and relative humidity (§12.5.2), mixture
enthalpy per unit dry air (§12.5.2), the adiabatic-saturation / wet-bulb humidity-ratio
relations and the chart dry-air enthalpy datum (§12.5.5, §12.7), and the steady-flow
water mass balance for air-conditioning processes (§12.8.1).

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 15 value + 16 cross-module checks -> "All 31 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
