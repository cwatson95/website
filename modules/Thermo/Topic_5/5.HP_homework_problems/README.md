# 5.HP — Homework Problems (Topic 5)

Support module for **Topic 5 (Property Data: Tables & Diagrams)**: 6 **property-evaluation
problems** from Moran 8e Ch.3, solved with the Topic-5 steam-table tools (`5.1`–`5.3`) and
code-checked. Parallels `Topic_3/3.HP`.

## Contents
- `problems.md` — the 6 problems (given → find → answer), grouped by type, each with its
  check call.
- `code/homework.py` — one function per problem, solved from the given data using the
  embedded SI steam tables in `modules/Thermo/steam_tables/`.
- `code/test_homework.py` — 26 checks: worked answers + consistency (quality in [0,1],
  recovered phases, rigid-process v₂ = v₁).

## Note
Moran provides **no answer key** for end-of-chapter problems; the answers are *worked
solutions* (checked-but-unofficial). Coverage: phase determination from (p, T) and (T, v);
superheated-vapor interpolation; compressed-liquid specific volume (Table A-5 and the
saturated-liquid approximation); two-phase quality from a container volume; and a rigid-tank
cool-down into the two-phase region. All problems use **water**.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 26 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
