# 2.1 — Work

First module of **Topic 2 (Energy & Work)**; see `modules/Thermo/list.txt`.

- **Builds on:** `1.5` quasiequilibrium (`∫p dV`), `1.2` closed systems.
- **Feeds into:** `2.2`/`2.3` expansion/compression work, `2.4` power, the laws
  (`3`), and every device/cycle that exchanges work.

## Scope
Work is an energy transfer that could in principle raise a weight, `W = ∫F·ds`
(Moran §2.2). This module is the **catalog of work modes** under one sign
convention — **`W > 0` when done BY the system** — and the reminder that work is
a **path function** (`δW`, not a property; see `1.5`):

| mode | expression | `code/work.py` |
|------|-----------|----------------|
| moving boundary | `∫p dV` | `boundary_work` |
| general force | `∫F·ds` | `work_force_displacement` |
| rotating shaft | `τ ω · dt` | `shaft_work` |
| electrical | `V I · dt` (`−` into system) | `electric_work` |
| spring (linear) | `½k(x₂²−x₁²)` | `spring_work` |

Moran's §2.2.8 gathers them as `δW = p dV + σ d(Ax) + τ dA − ε dZ + …` (Eq. 2.26).

## Run
```bash
cd code && python3 work.py          # one example of each mode
python3 test_work.py                # "All 7 tests passed."
```

## Files
`notes.md`, `code/work.py`, `code/test_work.py`, `problems/problems.md`, `refs.md`.
