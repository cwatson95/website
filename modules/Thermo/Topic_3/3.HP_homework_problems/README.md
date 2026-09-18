# 3.HP — Homework Problems (Topic 3)

Support module for **Topic 3 (The Laws)**: 7 **second-law problems** from Moran 8e
Ch.5, solved and code-checked. Parallels `Topic_2/2.HP`.

## Contents
- `problems.md` — the 7 problems (given → find → answer), grouped by type, each with
  its check call.
- `code/homework.py` — one function per problem, solved from the given data.
- `code/test_homework.py` — 22 checks: worked answers + consistency (energy balances
  close, COP claims classified against the reversible bound).

## Note
Moran provides **no answer key** for these; the answers are *worked solutions*
(checked-but-unofficial). Coverage: impossible-cycle detection, reversible power-cycle
sizing, actual-vs-reversible efficiency, minimum heat rejection, COP from efficiency,
evaluating performance claims, and Carnot-efficiency sensitivity.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 23 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
