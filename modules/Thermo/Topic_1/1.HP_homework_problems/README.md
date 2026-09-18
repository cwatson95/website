# 1.HP — Homework Problems (Topic 1)

A support module for **Topic 1 (Foundations)**: a large set of quantitative
**end-of-chapter problems** from Moran 8e Ch.1–2, each solved and **code-checked**.
Part of the `1.EQ / 1.EP / 1.HP` support set (`modules/Thermo/plan.txt`).

## Contents
- `problems.md` — 25 problems (13 from Ch.1, 12 from Ch.2): given → find → answer,
  grouped by chapter, each with its check call.
- `code/homework.py` — one function per problem, solving it from the given data
  via the Topic-1 equations (imported from module `1.EQ`).
- `code/test_homework.py` — 39 checks: the worked answers plus independent
  consistency checks (energy balances close, weight recomputes, etc.).

## Note on "verification"
Moran provides **no answer key** for these problems, so the answers are *my worked
solutions*. The module's guarantee is that each solution is encoded, reproducible,
and — where a governing balance allows — internally consistent. Treat the numbers
as checked-but-unofficial.

## Coverage
Weight & local gravity; specific volume / density / moles / molecules; manometers
& barometers, absolute vs gauge pressure; temperature-scale conversions
(Ch.1); kinetic/potential energy changes; polytropic `∫p dV` work; closed-system
energy balances; steady & rate balances (heater, motor); refrigerator COP (Ch.2).

## Run
```bash
cd code
python3 homework.py          # sample of worked answers
python3 test_homework.py     # -> "All 39 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
