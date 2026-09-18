# 12.HP — Homework Problems (Topic 12)

Support module for **Topic 12 (Combustion & Reacting Mixtures)**: 9 problems from Moran
8e Ch.13/14 (plus one ~PK Saha leaf), solved and code-checked. Parallels `7.HP`, `13.HP`.

## Contents
- `problems.md` — the 9 problems (given → find → answer), grouped by theme, each with
  its check call.
- `code/homework.py` — one function per problem, solved from complete given data with
  the book's Table A-2/A-23/A-25/A-27 entries embedded (page-verified).
- `code/test_homework.py` — 64 checks: worked answers + consistency (element balances
  close, mole fractions sum to 1, K round-trips through Eq. 14.35, dew points inside
  their steam-table bracket, HHV−LHV equals the condensed-water term, Saha ↔ Moran
  Eq.-14.35 identity) + cross-imports of `12.1` and `12.2`.

## Note
Moran provides **no answer key**; these are *worked solutions* (checked-but-unofficial).
Coverage: fuel stoichiometry (AF ratio, % excess air, equivalence ratio), dry-product-
analysis back-out, product dew points, HHV/LHV from formation enthalpies, adiabatic
flame temperature (theoretical & 300% air), equilibrium composition and pressure from
K_p in a closed vessel, Moran §14.4.3 ionization equilibrium, and — **flagged ~PK,
beyond Moran** — the Saha ionization fraction of hydrogen, bridged exactly to Moran's
Eq.-14.35 form.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 64 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
