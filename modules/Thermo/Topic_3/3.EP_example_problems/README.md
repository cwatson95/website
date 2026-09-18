# 3.EP — Example Problems (Topic 3)

Support module for **Topic 3 (The Laws)**: Moran 8e Chapter-5 worked **Examples
5.1–5.3** (second law), transcribed and **code-verified**. Parallels `Topic_2/2.EP`,
but holds its own code because the second-law examples are new to Topic 3.

## What it does
- `examples.md` — index of the examples (given → find → book answer → function).
- `code/examples.py` — each example solved from its given data via Eqs. 5.9–5.11.
- `code/test_examples.py` — regenerates each book answer and checks it (15 checks).

## Scope
Power-cycle performance against the Carnot ceiling and corollary 1 (Ex. 5.1);
refrigerator and heat-pump COPs vs. their reversible maxima (Ex. 5.2, 5.3),
including an impossible-claim test and a cost estimate.

## Run
```bash
cd code
python3 examples.py
python3 test_examples.py     # -> "All 14 tests passed."
```

## Files
`examples.md`, `code/examples.py`, `code/test_examples.py`, `refs.md`.
