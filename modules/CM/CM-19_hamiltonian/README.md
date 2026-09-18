# CM-19 — Hamiltonian Mechanics

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-17`
(Legendre transform), `~MA-07`. **Feeds:** `~CM-20` (Poisson brackets), `~QM-05`.

## Scope
The Hamiltonian H(q, p) from the Legendre transform of L, **Hamilton's equations**
q̇ = ∂H/∂p, ṗ = −∂H/∂q, and the phase-space flow (integrated with MA-07).

## Operations — `code/hamiltonian.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `hamilton_rhs(H)` | RHS [∂H/∂p, −∂H/∂q] | Fowles §10.9 p.455; Goldstein §8.1 p.334 |
| `integrate_hamilton(H, q0, p0, …)` | phase-space flow | Fowles §10.9 p.455 |
| `hamiltonian_from_potential(m, V)` | H = p²/2m + V(q) | Goldstein §8.1 p.334 |

## Use
```python
import math
from hamiltonian import hamiltonian_from_potential, integrate_hamilton
H = hamiltonian_from_potential(1.0, lambda q: 0.5*4*q*q)   # SHO, omega=2
ts, ys = integrate_hamilton(H, 1.0, 0.0, 0, 2*math.pi, 8000)
# orbit is a closed ellipse p^2 + omega^2 q^2 = const; H is conserved
```

## Run
```bash
cd code
python3 hamiltonian.py        # demo (Hamilton's equations, energy, phase ellipse)
python3 test_hamiltonian.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/hamiltonian.py` · `code/test_hamiltonian.py` · `problems/problems.md`
