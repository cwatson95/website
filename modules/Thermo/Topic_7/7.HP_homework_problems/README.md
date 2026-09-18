# 7.HP — Homework Problems (Topic 7)

Support module for **Topic 7 (Performance Metrics)**: 8 problems from Moran 8e Ch.2/5/6,
solved and code-checked. Parallels `3.HP`, `4.HP`.

## Contents
- `problems.md` — the 8 problems (given → find → answer), grouped by metric, each with
  its check call.
- `code/homework.py` — one function per problem, solved from complete given data.
- `code/test_homework.py` — 18 checks: worked answers + consistency (cycle balance
  Q_C + W = Q_H; isentropic work w = η_t·w_ideal).

## Note
Moran provides **no answer key**; these are *worked solutions* (checked-but-unofficial).
Problems 2–5 are Ch.5 *Checking Understanding* items (p.277) whose answers are fixed by the
physics. Coverage: power-cycle thermal efficiency and Carnot ceilings, refrigerator/heat-
pump COPs, and isentropic turbine/pump efficiencies.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 18 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
