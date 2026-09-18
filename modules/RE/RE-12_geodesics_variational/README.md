# RE-12 — Geodesics & the variational principle

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The
worldlines of free fall: the geodesic equation, its derivation as the
Euler–Lagrange equation of the action, maximal aging, and conserved quantities
from symmetry.

- **Prerequisites:** `RE-11` (curvature — Christoffel/Riemann); **`~MA-13`**
  (calculus of variations — Euler–Lagrange) and **`~MA-17`** (differential
  geometry — `christoffel`). This module *imports both MA-13 and MA-17*.
- **Feeds into:** `~RE-14` (Schwarzschild orbits — the geodesic equation + the two
  Killing constants `E`, `L` built here are its entire input); `~CM-21`
  (Hamilton–Jacobi/eikonal — *not yet built*, forward reference). It is the
  relativity terminus of **bridge B1**, the variational thread
  `MA-13 → CM-17 → CM-21 → RE-12`.

## The one idea
A geodesic is a straight line in curved spacetime, and "straight" has two faces
that **coincide for the Levi-Civita connection**: the *straightest* path
(parallel-transports its tangent, `u^ν∇_ν u^μ = 0`) and the *extremal* path
(`δ∫ds = 0`). Extremizing the action `S = ∫ ½ g_{μν}ẋ^μẋ^ν dλ` via Euler–Lagrange
(MA-13) **reproduces the Christoffel symbols** — the slick way to compute `Γ`.
Timelike geodesics are the worldlines of **maximal proper time** (free fall =
maximal aging); null geodesics are light rays.

## Scope
The geodesic equation `ẍ^μ + Γ^μ_{νρ}ẋ^νẋ^ρ = 0` in an affine parameter; its
variational derivation; maximal aging (RE-05's reversed triangle inequality); and
**Killing symmetries ⇒ conserved quantities** (`∂_t → energy`, `∂_φ → angular
momentum`) — the constants that reduce Schwarzschild orbits (RE-14) to a 1-D
problem.

## Operations — `code/geodesics.py` (G = c = 1; metric is a callable `x→g`)
| call | meaning |
|------|---------|
| `geodesic_rhs(metric,x,xdot)` | `ẍ^k = −Γ^k_{ij}ẋ^iẋ^j` (via MA-17 `christoffel`) |
| `integrate_geodesic(metric,x0,xdot0,dtau,steps)` | RK4-integrate the worldline → list of `(x,xdot)` |
| `lagrangian(metric,x,xdot)` | `L = ½ g_{μν}ẋ^μẋ^ν` (affine geodesic Lagrangian) |
| `action_length(metric,path)` | `Σ√|g_{μν}Δx^μΔx^ν|` — arc length / proper time |
| `euler_lagrange_gives_christoffel(metric,x,xdot)` | E–L of `lagrangian` (MA-13) `==` `geodesic_rhs` |
| `is_geodesic(metric,path,dtau)` | does a sampled path satisfy `ẍ+Γẋẋ≈0`? |
| `killing_conserved(metric,ξ,x,xdot)` | `g_{μν}ξ^μẋ^ν`, conserved along geodesics |
| `minkowski_metric()`, `schwarzschild_metric(M)`, `sphere_metric(a)` | reference metrics |

## Use
```python
import math
from geodesics import (integrate_geodesic, is_geodesic, killing_conserved,
                       sphere_metric, schwarzschild_metric)

s = sphere_metric(1.0)
is_geodesic(s, [[math.pi/2, 0.2*k] for k in range(8)], dtau=0.2)   # True: equator
is_geodesic(s, [[1.0, 0.2*k] for k in range(8)], dtau=0.2)         # False: a latitude

sch = schwarzschild_metric(1.0)                                    # an orbit, r=10
orb = integrate_geodesic(sch, [0,10,math.pi/2,0], [1.2,0.2,0,0.04], dtau=0.2, steps=60)
E = killing_conserved(sch, [1,0,0,0], *orb[0])                     # energy (∂_t), conserved
```

## Run
```bash
cd code
python3 geodesics.py          # demo: straight lines, great circles, variational⇔Γ, aging, conservation
python3 test_geodesics.py     # 10 tests -> "All 10 tests passed."
```
*(Adds `../../../MA/MA-17_differential_geometry/code` and
`../../../MA/MA-13_calculus_of_variations/code` to `sys.path`; run in place.)*

## Files
- `notes.md` — straightest⇔extremal, the geodesic equation, the variational derivation, maximal aging, Killing conservation
- `code/geodesics.py` — the toolkit (imports MA-17 and MA-13)
- `code/test_geodesics.py` — flat=straight, sphere great circle, variational⇔Γ, maximal aging, Killing conservation
- `problems/problems.md` — worked problems (Zee, cpope)
- `refs.md` — verified citations
