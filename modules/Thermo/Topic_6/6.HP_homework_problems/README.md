# 6.HP — Homework Problems (Topic 6)

Support module for **Topic 6 (Processes & Idealizations)**: 8 **process** problems from
Moran 8e Ch.4 (steady-flow devices) and Ch.6 (entropy / reversibility / isentropic), solved
and code-checked. Parallels `Topic_3/3.HP`.

## Contents
- `problems.md` — the 8 problems (given → find → answer), grouped by type, each with its
  check call.
- `code/homework.py` — one function per problem, solved from the given data.
- `code/test_homework.py` — 28 checks: worked answers + consistency (energy- and
  entropy-balance closure; σ ≥ 0 for every real process).

## Note
Moran provides **no answer key** for these; the answers are *worked solutions*
(checked-but-unofficial). Coverage: steady nozzle (inlet area & heat), insulated turbine
power, ideal-gas entropy change → final volume, isothermal internally-reversible work,
paddle-stirred rigid-tank entropy production (SI and English), and an adiabatic-compression
minimum-work bound. Closed-system problems pair the energy balance with the entropy balance
`σ = ΔS − ∫δQ/T_b`.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 28 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
