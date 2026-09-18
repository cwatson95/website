# 5.EP — Example Problems (Topic 5)

Support module for **Topic 5 (Property Data: Tables & Diagrams)**: Moran 8e worked
**Examples 3.2, 3.4, 6.1** (water property evaluation), transcribed and **code-verified**.
Holds its own code, which reuses the concept modules' steam-table tools (5.1–5.5).

## What it does
- `examples.md` — index of the examples (given → find → book answer → function).
- `code/examples.py` — each example solved from its given data via the steam tables.
- `code/test_examples.py` — regenerates each book answer and checks it (29 checks).

## Scope
Two-phase quality and the saturation tables (Ex 3.2); a multi-process problem mixing
superheated, saturated, and two-phase states with the boundary-work term (Ex 3.4); and the
p–v / T–s **area** interpretation of work and heat for a reversible vaporization (Ex 6.1).
Two published in-text illustrations (superheated `h=u+pv` at p.112; the Mollier isentropic
expansion at p.296) round out coverage of A-2/A-3/A-4 and the entropy data.

## Note
All examples use **water** and the project SI steam tables in
`../../../steam_tables/`. The answers are Moran's *published* numbers; where the book rounds
an intermediate (Ex 3.4 quality), `examples.py` replicates the rounding so the answer
reproduces exactly. The Mollier values are chart reads the book labels approximate.

## Run
```bash
cd code
python3 examples.py
python3 test_examples.py     # -> "All 29 tests passed."
```

## Files
`examples.md`, `code/examples.py`, `code/test_examples.py`, `refs.md`.
