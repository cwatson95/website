# 12.EQ — List of Equations (Topic 12)

Support module for **Topic 12 (Combustion & Reacting Mixtures)**: the topic's equations,
cited and **machine-verified**. Parallels the `EQ` modules of other topics.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a
  book-verified value, then imports the concept modules `12.1` and `12.2` (and the
  worked-examples module `12.EP`) and asserts they compute the same thing, so a formula
  change anywhere in the topic fails this test.

## Scope
The Moran Ch.13 combustion trunk — theoretical O₂/air and the air–fuel ratio (Eq. 13.2),
% theoretical/excess air and equivalence ratio, product dew point, `h = h°_f + Δh`
(Eq. 13.9), the steady-flow and closed-vessel energy balances (Eqs. 13.12b/13.15b,
13.17b), enthalpy of combustion and heating values (Eq. 13.18), and the adiabatic-flame
balance (Eq. 13.21b) — plus the Ch.14 equilibrium trunk — chemical potential (Eq. 14.17),
reaction equilibrium (Eq. 14.26), `ΔG°`/`ln K` (Eqs. 14.29b/14.31), the composition and
mole forms of K (Eqs. 14.32/14.35), inverse reactions (Eq. 14.34), and ionization
equilibrium (§14.4.3, Ex. 14.8) — plus the **Saha rows (~PK, NOT Moran)**: the quantum
concentration and the Saha equation that supply the ionization K Moran cites to
statistical thermodynamics but does not derive.

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 37 value + 30 cross-module checks -> "All 67 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
