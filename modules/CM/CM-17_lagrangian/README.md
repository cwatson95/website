# CM-17 — Lagrangian Mechanics

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:**
**`~MA-13`** (calculus of variations), `~MA-07`. **Feeds:** `~CM-18` (Noether),
`~CM-19` (Hamiltonian).

## Scope
Generalized coordinates and the **Euler–Lagrange equation**
d/dt(∂L/∂q̇) − ∂L/∂q = 0, the conjugate momentum p = ∂L/∂q̇, and the Jacobi
energy. The variational machinery is reused directly from MA-13 (t, q, q̇ play the
role of MA-13's x, y, y′).

## Operations — `code/lagrangian.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `el_residual(L, ts, qs)` | Euler–Lagrange residual along a path (MA-13) | Fowles §10.4 p.430; Goldstein §2.3 p.44 |
| `generalized_momentum(L, t, q, qdot)` | p = ∂L/∂q̇ | Fowles §10.4 p.430 |
| `jacobi_energy(L, t, q, qdot)` | h = q̇ p − L (= T+V) | Goldstein §2.7 |
| `integrate_eom(qddot, …)` | integrate a 1-DOF EOM (MA-07) | Fowles §10.4 p.430 |

L is a mechanics Lagrangian `L(t, q, qdot)`.

## Use
```python
import math
from lagrangian import el_residual, generalized_momentum, integrate_eom
L = lambda t,q,p: 0.5*p*p - 0.5*4*q*q                # SHO, omega=2
ts = [i*math.pi/200 for i in range(201)]
max(abs(r) for r in el_residual(L, ts, [math.cos(2*t) for t in ts]))   # ~0 on the true path
```

## Run
```bash
cd code
python3 lagrangian.py        # demo (EL residual, conjugate momentum, pendulum)
python3 test_lagrangian.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/lagrangian.py` · `code/test_lagrangian.py` · `problems/problems.md`
