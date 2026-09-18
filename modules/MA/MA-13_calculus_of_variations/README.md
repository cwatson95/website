# MA-13 — Calculus of Variations

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-07` (ODEs),
`~MA-02` (functionals of paths). **Feeds:** `~CM-17` (Lagrangian mechanics —
action ∫L dt), `~CM-19` (the Beltrami integral → Hamiltonian), `~RE-12`
(geodesics). This module is **bridge B1** of the network: one principle, four
trunks.

## Scope
Extremizing a **functional** J[y]=∫L(x,y,y′)dx: the **Euler–Lagrange equation**
∂L/∂y − d/dx(∂L/∂y′)=0, the **Beltrami first integral** (when L has no explicit
x, L − y′L_{y′} is conserved), and the classic problems — shortest path
(geodesic), **brachistochrone** (cycloid), and minimal surface of revolution
(catenary). The functional is discretized segment-by-segment with L's partials by
finite differences, so any L works; a coordinate-Newton minimizer recovers
extremals numerically.

## Operations — `code/variational.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `functional(L, xs, ys)` | J[y]=∫L dx on a sampled path | Boas §1 p.472 |
| `euler_lagrange_residual(L, xs, ys)` | ∂L/∂y − d/dx(∂L/∂y′), ~0 on extremals | Boas §2 p.474 |
| `beltrami(L, x, y, p)` | first integral L − y′L_{y′} (∂L/∂x=0) | Boas §3–4 p.478 |
| `minimize_path(L, xa, ya, xb, yb, N)` | recover the extremal by Newton sweeps | Boas §3 p.478 |
| `cycloid_brachistochrone(a, thetas)` | the brachistochrone solution | Boas §4 p.482 |
| `catenary(c, xs)` | minimal surface of revolution | Boas §3 p.478 |

## Use
```python
import math
from variational import minimize_path, functional, beltrami, catenary

# shortest path: starts bent, relaxes to the straight line, J -> sqrt(2)
xs, ys = minimize_path(lambda x, y, p: math.sqrt(1 + p*p), 0, 0, 1, 1, N=15)
functional(lambda x, y, p: math.sqrt(1 + p*p), xs, ys)     # ~ 1.41421

# Beltrami constant along the catenary y = c cosh(x/c):  B = c
L = lambda x, y, p: y*math.sqrt(1 + p*p)
beltrami(L, 0.5, catenary(1.3, [0.5])[0], math.sinh(0.5/1.3))   # ~ 1.3
```

## Run
```bash
cd code
python3 variational.py        # demo (geodesic recovery, Beltrami on cycloid & catenary)
python3 test_variational.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/variational.py` · `code/test_variational.py` · `problems/problems.md`
