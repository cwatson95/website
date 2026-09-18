# 8.HP — Homework Problems (Topic 8)

Support module for **Topic 8 (Components & Devices)**: 8 problems spanning the
compressor, condenser, heat exchanger, and heat pump, solved and code-checked.
Parallels `7.HP`.

## Contents
- `problems.md` — the 8 problems (given → find → answer), grouped by device, each with
  its check call.
- `code/homework.py` — one function per problem, solved from complete given data.
- `code/test_homework.py` — 34 checks: worked answers + consistency (energy balances
  close; isentropic work is the minimum; `Q̇_C + Ẇ = Q̇_H`; COPs below the Carnot
  ceiling).

## Note
Moran provides **no answer key**; these are *worked solutions* (checked-but-unofficial).
Property values re-use the book-verified numbers of the Topic-8 worked Examples
(Ex 4.5, 4.7, 6.14, 10.3, 10.4 — see `8.EP`), so every embedded table value is
verified against the PDF. Coverage: mass flow two ways, compressor power with/without
heat loss, isentropic efficiency and the real exit state it fixes, condenser duty,
heat-exchanger flow ratio and exit state, heat-pump COP vs the Carnot ceiling.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 34 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
