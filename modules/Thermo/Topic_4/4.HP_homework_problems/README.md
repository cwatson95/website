# 4.HP — Homework Problems (Topic 4)

Support module for **Topic 4 (Properties & State Functions)**: 8 problems from Moran
8e Ch.3/6/7, solved and code-checked. Parallels `2.HP`, `3.HP`.

## Contents
- `problems.md` — the 8 problems (given → find → answer), grouped by property, each
  with its check call.
- `code/homework.py` — one function per problem, solved from given (table-sourced) data.
- `code/test_homework.py` — 19 checks: worked answers + consistency (rigid ⇒ Q=ΔU,
  const-p ⇒ Q=ΔH, energy/entropy/exergy balances close).

## Note
Moran provides **no answer key**; these are *worked solutions* (checked-but-unofficial).
Coverage: rigid vs constant-pressure heating (enthalpy & quality), ideal-gas and
incompressible entropy change, entropy production by stirring and by mixing, and exergy
change/destruction.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 18 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
