# 13.EQ — List of Equations (Topic 13)

Support module for **Topic 13 (Compressible Flow & Gas Dynamics)**: the topic's
equations, cited and **machine-verified**. Parallels the `EQ` modules of other topics.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a known
  value, then imports the concept modules `13.1`–`13.5` and asserts they compute the
  same thing (so a formula change anywhere fails this test).

## Scope
The Moran Ch.9 compressible-flow trunk — speed of sound and Mach number (§9.12),
stagnation and isentropic flow functions, the area–velocity and area–Mach relations and
critical (sonic) ratios (§9.13–9.14.1), and the normal-shock functions (§9.14.2) — plus
the two cross-trunk pipe-flow leaves (~CM, **not Moran**): the Reynolds number and the
laminar/turbulent friction factors of `13.4`/`13.5`.

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 16 value + 17 cross-module checks -> "All 33 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
