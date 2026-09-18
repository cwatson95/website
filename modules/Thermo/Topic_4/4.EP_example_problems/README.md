# 4.EP — Example Problems (Topic 4)

Support module for **Topic 4 (Properties & State Functions)**: six Moran 8e worked
**Examples** (Ch.3, 6, 7), transcribed and **code-verified**. Parallels `3.EP`.

## What it does
- `examples.md` — index of the examples (given → find → book answer → function).
- `code/examples.py` — each example solved from its given data.
- `code/test_examples.py` — regenerates each book answer and checks it (16 checks).

## Scope
Constant-pressure (enthalpy/work) and constant-volume (quality) heating; the
reversible/irreversible evaporation pair (entropy & production); and two exergy
evaluations — including the `6.1 → 6.2 → 7.2` thread on one process.

## Run
```bash
cd code
python3 examples.py
python3 test_examples.py     # -> "All 16 tests passed."
```

## Files
`examples.md`, `code/examples.py`, `code/test_examples.py`, `refs.md`.
