# 7.EP — Example Problems (Topic 7)

Support module for **Topic 7 (Performance Metrics)**: seven Moran 8e worked **Examples**
(Ch.5, 6), transcribed and **code-verified**. Parallels `3.EP`, `4.EP`.

## What it does
- `examples.md` — index of the examples (given → find → book answer → function).
- `code/examples.py` — each example solved from its given data.
- `code/test_examples.py` — regenerates each book answer and checks it (18 checks).

## Scope
Whole-cycle metrics against the Carnot ceiling — power-cycle classification (5.1),
refrigerator COP (5.2), heat-pump COP/min-work/cost (5.3) — and single-device isentropic
efficiencies — turbine both ways (6.11, 6.12), nozzle (6.13), compressor (6.14).

## Run
```bash
cd code
python3 examples.py
python3 test_examples.py     # -> "All 18 tests passed."
```

## Files
`examples.md`, `code/examples.py`, `code/test_examples.py`, `refs.md`.
