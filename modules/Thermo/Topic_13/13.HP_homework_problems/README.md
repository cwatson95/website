# 13.HP — Homework Problems (Topic 13)

Support module for **Topic 13 (Compressible Flow & Gas Dynamics)**: 7 **compressible-flow
problems** from Moran 8e Ch.9, solved and code-checked. Parallels the other topics' `HP`
modules.

## Contents
- `problems.md` — the 7 problems (given → find → answer), grouped by type, each with its
  check call.
- `code/homework.py` — one function per problem, solved from the given data.
- `code/test_homework.py` — 37 checks: worked answers + consistency (choking test,
  mass-flow ordering by molecular weight, stagnation-T conserved across a shock).

## Note
Moran provides **no answer key** for these end-of-chapter problems; the answers are
*worked solutions* (checked-but-unofficial). Coverage: sonic velocity of several gases,
deriving and evaluating the critical (sonic) ratios, converging-nozzle choking (three
sub-problems incl. a gas mixture and an English-unit multi-gas set), the effect of
raising supply pressure, and two normal-shock problems (one with mass flow rate).

> Gas-specific `k`, `M` are the ideal-gas (Table A-20, room-temperature) values; each is
> stated in the corresponding `homework.py` function. English-unit mass flows carry
> `gc = 32.2 lb·ft/(lbf·s²)` and `R = 1545/M ft·lbf/(lb·°R)`.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 37 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
