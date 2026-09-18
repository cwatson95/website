# 13.EP — Example Problems (Topic 13)

Support module for **Topic 13 (Compressible Flow & Gas Dynamics)**: Moran 8e Chapter-9
worked **Examples 9.14–9.15** (nozzle/diffuser flow), transcribed and **code-verified**.
Holds its own code because the compressible-flow examples are specific to Topic 13.

## What it does
- `examples.md` — index of the examples (given → find → book answer → function).
- `code/examples.py` — each example solved from its given data via Eqs. 9.50–9.56.
- `code/test_examples.py` — regenerates each book answer and checks it (39 checks).

## Scope
The effect of back pressure on a **converging nozzle** (choked vs subsonic exit, mass
flow rate, exit Mach — Ex. 9.14), and the five-case analysis of a **converging–diverging
nozzle** (subsonic/supersonic exits, choking, and a normal shock at the exit and inside
the diverging section — Ex. 9.15).

## Run
```bash
cd code
python3 examples.py
python3 test_examples.py     # -> "All 39 tests passed."
```

## Files
`examples.md`, `code/examples.py`, `code/test_examples.py`, `refs.md`.
