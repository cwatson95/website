# 10.HP — Homework Problems (Topic 10)

Support module for **Topic 10 (Engines)**: 8 problems from Moran 8e Ch.5/9, solved and
code-checked. Parallels `7.HP`.

## Contents
- `problems.md` — the 8 problems (given → find → answer), grouped Carnot vs Stirling,
  each with its check call.
- `code/homework.py` — one function per problem, solved from complete given data.
- `code/test_homework.py` — 45 checks: worked answers + consistency (cycle balance
  Q_C + W = Q_H; η = W/Q_in; regenerator legs cancel; mep) + cross-checks against
  the concept modules `10.1` and `10.2` (shared Carnot ceiling).

## Note
Moran provides **no answer key**; these are *worked solutions* (checked-but-unofficial).
P1–P3 are Ch.5 *Checking Understanding* items (p.277) whose answers are fixed by the
physics (different items from `7.HP`); P6–P8 work the Ch.9 Stirling problems 9.102–9.103
(p.601). Coverage: inventor-claim verdicts against the Carnot ceiling, max-work /
min-heat extrema for given reservoirs, minimum refrigerator power, Stirling per-cycle
heats with and without regeneration (the efficiency collapse), and the
Stirling-vs-Carnot ceiling comparison.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 45 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
