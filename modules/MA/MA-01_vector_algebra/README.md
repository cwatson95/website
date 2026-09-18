# MA-01 — Vector Algebra

Root module of the **MATHEMATICS / METHODS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** none (this is a root).
- **Feeds into:** `~MA-02` (vector calculus), `~CM-01` (kinematics), `~CM-09`
  (angular momentum & torque, both cross products), `~CM-13` (inertia tensor),
  `~EM-02` (flux / Gauss's law).

## Scope
The dot, cross, scalar-triple and vector-triple products, their geometric
meaning, and the identities that follow (Lagrange, BAC–CAB, Jacobi, cyclic
symmetry of the box product).

Built so the operations also act on **vector-valued functions**: hand it a
trajectory `r(t)` and `cross(r, v)` returns the *function* `t ↦ r(t)×v(t)` — the
seed for kinematics and angular momentum in the CM trunk.

## Operations — `code/vector_algebra.py`

| call | meaning | formula |
|------|---------|---------|
| `dot(a, b)` | scalar product | a·b = Σ aᵢ bᵢ |
| `cross(a, b)` | vector product | (a×b)ᵢ = εᵢⱼₖ aⱼ bₖ |
| `scalar_triple(a, b, c)` (alias `triple`) | box product | a·(b×c) = det[a b c] |
| `vector_triple(a, b, c)` | BAC–CAB | a×(b×c) = b(a·c) − c(a·b) |

Plus `norm, unit, angle, projection, rejection, are_parallel,
are_perpendicular, are_coplanar, box_volume`.

**Three kinds of input, one set of functions.** Components may be
numbers, SymPy symbols, or *callables*. If any argument is a function the result
is a function — that lifting is a single decorator, `lift`, which downstream
modules can reuse for their own vector operations.

## Use
```python
from vector_algebra import dot, cross, scalar_triple, norm

dot((1, 2, 3), (4, 5, 6))                      # 32
cross((1, 0, 0), (0, 1, 0))                    # (0, 0, 1)
scalar_triple((1,0,0), (0,1,0), (0,0,1))       # 1  (unit-cube volume)

import math
r = lambda t: (math.cos(t),  math.sin(t), t)   # a helix
v = lambda t: (-math.sin(t), math.cos(t), 1.0) # r'(t)
L     = cross(r, v)        # FUNCTION: specific angular momentum  t ↦ r×v
speed = norm(v)            # FUNCTION: |v(t)|
L(0.0), speed(0.0)         # ((-1.0, 1.0, 1.0), 1.4142...)
```

## Run
```bash
cd code
python3 vector_algebra.py          # demo: numeric, functional, + symbolic if sympy present
python3 test_vector_algebra.py     # tests  ->  "All N tests passed."
```

## Files
- `notes.md` — definitions, geometry, identities, and product rules for `r(t)`
- `code/vector_algebra.py` — the library (`lift` + the operations)
- `code/test_vector_algebra.py` — numeric + functional + symbolic checks
- `problems/problems.md` — worked problems (Boas, Griffiths)
- `refs.md` — textbook sections
