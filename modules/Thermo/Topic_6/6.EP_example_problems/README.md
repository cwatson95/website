# 6.EP — Example Problems (Topic 6)

Support module for **Topic 6 (Processes & Idealizations)**: Moran 8e worked **Examples**
4.1, 4.2, 4.4 (steady-state control volumes) and 6.1–6.12 (entropy, reversibility,
isentropic processes), transcribed and **code-verified**. Parallels `Topic_3/3.EP`,
`Topic_13/13.EP`.

## What it does
- `examples.md` — index of the examples (given → find → book answer → function).
- `code/examples.py` — each example solved from its given data; book table values (h, u,
  s, v, p_r) are quoted as given.
- `code/test_examples.py` — regenerates each book answer and checks it (22 checks).

## Scope
Steady-state mass and energy balances (Ex 4.1, 4.2, 4.4); internally-reversible heat as the
T–s area (Ex 6.1); entropy production in irreversible processes (Ex 6.2, 6.4, 6.5); minimum
theoretical work from σ ≥ 0 (Ex 6.3); isentropic ideal-gas processes via `p_r`/constant-`k`
(Ex 6.9, 6.10); isentropic turbine efficiency (Ex 6.11, 6.12).

## Run
```bash
cd code
python3 examples.py
python3 test_examples.py     # -> "All 22 tests passed."
```

## Files
`examples.md`, `code/examples.py`, `code/test_examples.py`, `refs.md`.
