# CM-21 — Hamilton–Jacobi Theory & Action-Angle Variables

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-19`,
`~MA-07`. **Links:** `~QM-15` (WKB: S/ℏ is the phase), `~RE-12` (action as length).

## Scope
Hamilton's characteristic function W(q) = ∫p dq, the **action variable**
J = ∮p dq, and the exact oscillation **period** T = dJ/dE — isochronous for the
harmonic oscillator, amplitude-dependent for an anharmonic well.

## Operations — `code/hamilton_jacobi.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `turning_points(V, E, …)` | where V(q) = E | Goldstein §10.6 p.452 |
| `characteristic_function(V, m, E, q, …)` | W(q) = ∫√(2m(E−V)) dq | Goldstein §10.3 p.440 |
| `action_variable(V, m, E, …)` | J = ∮ p dq | Goldstein §10.6 p.452 |
| `period(V, m, E, …)` | T = dJ/dE (singularity-cancelling) | Goldstein §10.6 p.452 |
| `frequency(V, m, E, …)` | ω = 2π/T | Goldstein §10.6 p.452 |

## Use
```python
import math
from hamilton_jacobi import action_variable, period
V = lambda q: 0.5*4*q*q                       # SHO, omega=2
action_variable(V, 1.0, 2.0, -10, 10)         # J = 2 pi E/omega = 2 pi
period(V, 1.0, 2.0, -10, 10)                   # 2 pi/omega = pi (independent of E)
```

## Run
```bash
cd code
python3 hamilton_jacobi.py        # demo (SHO isochronous, pendulum anharmonic)
python3 test_hamilton_jacobi.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/hamilton_jacobi.py` · `code/test_hamilton_jacobi.py` · `problems/problems.md`
