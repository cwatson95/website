# 9.HP — Homework Problems (Topic 9)

Support module for **Topic 9 (Power & Refrigeration Cycles)**: 12 problems across all
six cycles (Carnot, Otto, Diesel, dual, Brayton, Rankine), solved and code-checked.
Parallels `7.HP`.

## Contents
- `problems.md` — the 12 problems (given → find → answer), grouped by cycle, each with
  its check call.
- `code/homework.py` — one function per problem, solved from complete given data; the
  Rankine problems read their saturation states from `../../steam_tables/` at runtime.
- `code/test_homework.py` — 66 checks: worked answers + consistency closures (energy
  balance `q_in − q_out = w_net`; η below the Carnot ceiling at the same temperature
  extremes; bwr in the characteristic band — 40–80% gas turbine, <2% vapor plant;
  mep > 0; dual bracketed by Diesel/Otto; pressure-effect trends).

## Note
Moran provides **no answer key** for its end-of-chapter problems; these are *worked
solutions* (checked-but-unofficial) in the style of the Ch.8–9 sets. Coverage: Carnot
verdicts, Otto/Diesel/dual cold air-standard cycles, Brayton with irreversibilities and
regeneration, Rankine with boiler/condenser-pressure effects.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 66 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
