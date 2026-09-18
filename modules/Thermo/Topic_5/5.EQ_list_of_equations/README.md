# 5.EQ — List of Equations (Topic 5)

Support module for **Topic 5 (Property Data: Tables & Diagrams)**: the topic's equations,
cited and **machine-verified**. Parallels the `EQ` modules of other topics.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a known
  value, then imports the concept modules `5.1`–`5.5` and asserts they compute the same
  thing (so a formula change anywhere fails this test).

## Scope
The Moran Ch.3 property-evaluation set — quality and the two-phase mixture rule
(§3.3, §3.5.2, §3.6.2), enthalpy and linear interpolation (§3.5.1, §3.6.1), the
saturated-liquid approximations for compressed liquid (§3.10.1) — plus the two "area"
relations that turn property diagrams into work and heat: `W = ∫p dV` on the p–v diagram
(§2.2.5) and `Q = ∫T dS` on the T–s diagram (§6.6), with the Carnot efficiency (§6.6.2,
Eq. 5.9). Entropy uses §6.2.2/§6.2.3 (Eqs. 6.4, 6.5).

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 19 value + 17 cross-module checks -> "All 36 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
