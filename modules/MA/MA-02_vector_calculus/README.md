# MA-02 — Vector Calculus

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-01`.
**Feeds:** `~EM-13` (Maxwell's equations), `~CM-22` (continuity equation),
`~QM-04` (probability current), `~MA-03` (operators in curvilinear coords).

## Scope
The differential operators on fields — gradient, divergence, curl, Laplacian —
and the integral theorems (fundamental theorem for gradients, the divergence /
Gauss theorem, Stokes' theorem). Fields are plain functions; the operators
return new fields by central finite differences, and the integral helpers let
you *check the theorems numerically*. Reuses MA-01's `dot`/`cross`.

## Operations — `code/vector_calculus.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `gradient(f)` | ∇f (scalar→vector field) | Boas §6 p.290; Griffiths §1.2.2 p.13 |
| `divergence(F)` | ∇·F | Boas §7 p.296; Griffiths §1.2.4 p.17 |
| `curl(F)` | ∇×F | Boas §7 p.296; Griffiths §1.2.5 p.18 |
| `laplacian(f)` | ∇²f = ∇·∇f | Boas §7 p.297; Griffiths §1.2.7 p.23 |
| `directional_derivative(f, u)` | ∇f·û | Boas §6 p.290 |
| `line_integral(F, path, a, b)` | ∫F·dl (work / circulation) | Boas §8 p.299; Griffiths §1.3.1 p.24 |
| `surface_flux(F, surf, …)` | ∬F·dS | Griffiths §1.3.1 p.24 |

A field is `f(x, y, z)->number` (scalar) or `F(x, y, z)->(Fx, Fy, Fz)` (vector).
Operators compose: `laplacian(f)` == `divergence(gradient(f))`, and the identities
`curl(grad f)=0`, `div(curl F)=0` hold (tested).

## Use
```python
from vector_calculus import gradient, divergence, curl, laplacian, line_integral
import math

f = lambda x, y, z: x**2 + y**2 + z**2     # r^2
gradient(f)(1, 2, 3)                        # ~ (2, 4, 6)
laplacian(f)(1, 2, 3)                       # ~ 6

F = lambda x, y, z: (-y, x, 0.0)           # rigid rotation
curl(F)(1, 1, 1)                           # ~ (0, 0, 2)
circle = lambda t: (math.cos(t), math.sin(t), 0.0)
line_integral(F, circle, 0, 2*math.pi)     # ~ 2*pi  (Stokes: = curl_z * area)
```

## Run
```bash
cd code
python3 vector_calculus.py          # demo (operators + Stokes/Gauss checks)
python3 test_vector_calculus.py     # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/vector_calculus.py` · `code/test_vector_calculus.py` · `problems/problems.md`
