# 2.HP — Homework Problems (Topic 2)

Support module for **Topic 2 (Energy & Work)**: 17 quantitative end-of-chapter
**work/energy problems** from Moran 8e Ch.2, solved and code-checked. Chosen to be
**disjoint** from `Topic_1/1.HP` (which already holds 12 other Ch.2 problems), so
together the two modules give broad Ch.2 coverage without duplication.

## Contents
- `problems.md` — the 17 problems (given → find → answer), grouped by type, each
  with its check call.
- `code/homework.py` — one function per problem, solved from the given data.
- `code/test_homework.py` — 30 checks: worked answers + consistency (recovered
  endpoints, energy balances close).

## Note
Moran provides **no answer key** for these; the answers are *worked solutions*
(checked-but-unofficial). Coverage: KE/PE, work from a resultant force, power,
expansion/compression & general `∫p dV` work, spring/shaft/electrical work,
closed-system and transient energy balances.

## Run
```bash
cd code
python3 homework.py          # sample
python3 test_homework.py     # -> "All 30 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
