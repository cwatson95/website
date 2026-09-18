# CM-16 — Coupled Oscillations & Normal Modes

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-15`,
**`~MA-04`** (the eigensolver). **Links:** `~MA-09` (each mode is a Fourier
component), `~QM-05`.

## Scope
The small-oscillation eigenvalue problem **K v = ω²M v** for a coupled system,
solved by reducing it to a symmetric eigenproblem and diagonalizing with MA-04.
Returns the **normal frequencies** and (mass-orthonormal) **normal modes**.

## Operations — `code/normal_modes.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `normal_modes(K, M)` | frequencies & modes of K v = ω²M v | Fowles §11.3 p.472 |
| `mode_inner_product(M, va, vb)` | mass-weighted inner product vᵀMv | Fowles §11.3 p.472 |

K is the (symmetric) stiffness matrix; M is the list of masses (diagonal mass matrix).

## Use
```python
from normal_modes import normal_modes
K = [[2,-1],[-1,2]]                  # two masses, three springs (k=1)
freqs, modes = normal_modes(K, [1,1])
# freqs = [1, sqrt(3)];  modes = in-phase (1,1) and out-of-phase (1,-1)
```

## Run
```bash
cd code
python3 normal_modes.py        # demo (two-mass normal frequencies and shapes)
python3 test_normal_modes.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/normal_modes.py` · `code/test_normal_modes.py` · `problems/problems.md`
