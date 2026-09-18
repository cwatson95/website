# EM-04 — Boundary-Value Problems

Fourth module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (the field, `coulomb_field`) and `~EM-03` (the
  potential `potential_point_charges`, and Laplace's equation ∇²V = 0) — both
  imported directly; `~MA-08` (the Laplace PDE and separation of variables).
- **Feeds into:** `~EM-05` (multipole expansion — the spherical-separation
  Legendre series, §3.3.2), `~EM-06` (conductors & capacitance reuse the
  boundary conditions and the second uniqueness theorem).

## Scope
One equation, **Laplace's equation ∇²V = 0** (Gr §3.1, the source-free case of
`~EM-03`'s Poisson equation), with the potential pinned by **boundary data**.
The whole subject is *how to solve it*, and the **uniqueness theorems** (§3.1.5–3.1.6)
are the licence: any potential that obeys ∇²V = 0 in the region and matches the
boundary **is** the solution, however you found it. Three ways to find it:

1. **Method of images** (§3.2) — replace a grounded conductor by fictitious
   *image* charges that reproduce its boundary condition. The classic case: a
   point charge *q* a height *d* above a grounded plane → image −*q* at −*d*.
2. **Separation of variables / Fourier series** (§3.3) — the semi-infinite slot,
   solved as a Fourier sine series (Eq. 3.34) and **summed in closed form**
   (Eq. 3.36); the code carries both so the series can be checked against the
   closed form. The orthogonality behind the Fourier step is `~MA-11`.
3. **Relaxation** (§3.1.5) — iterate the discrete Laplace equation (each node →
   the average of its neighbours) to the one potential the boundary allows: a
   numerical **demonstration of the uniqueness theorem**.

SI units throughout; potentials are returned as functions `V(x, y, z)` (images)
or `V(x, y)` (slot), the same convention as `~EM-03`.

## Operations — `code/boundary_value.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `image_potential_plane(q, d)` | V for z>0 of *q* at height *d* + image −*q* at −*d*; V = 0 on the plane | Gr §3.2.1 Eq.3.9 p.124 |
| `image_field_plane(q, d)` | the matching field **E** = −∇V (real + image), z>0 | Gr §3.2.1 p.124 |
| `induced_surface_charge(q, d)` | σ(x,y) = −*qd* / 2π(x²+y²+d²)^(3/2) | Gr §3.2.2 Eq.3.10 p.125 |
| `total_induced_charge(q, d)` | ∫σ da over the plane = −*q* | Gr §3.2.2 Eq.3.10 p.125 |
| `image_force(q, d)` | F = −(1/4πε₀) q²/(2d)² (attractive, toward the plane) | Gr §3.2.3 Eq.3.12 p.126 |
| `slot_potential_series(V0, a)` | Fourier sine series for the slot (odd *n*) | Gr §3.3.1 Eq.3.34 p.131 |
| `slot_potential_closed(V0, a)` | V = (2V₀/π) arctan(sin(πy/a) / sinh(πx/a)) | Gr §3.3.1 Eq.3.36 p.131 |
| `solve_laplace_2d(bc, …)` | Gauss–Seidel relaxation → the unique V fixed by Dirichlet `bc` | Gr §3.1.5 p.119 |

Constants `EPS0` (ε₀) and `K_E` = 1/4πε₀ ≈ 8.99×10⁹ are imported from `~EM-01`;
the image construction reuses `coulomb_field` (`~EM-01`) and
`potential_point_charges` (`~EM-03`), so the boundary-value layer adds no new
field machinery.

## Use
```python
from boundary_value import (image_potential_plane, total_induced_charge, image_force,
                            slot_potential_series, slot_potential_closed, solve_laplace_2d)

q, d = 1e-9, 0.1                       # 1 nC, 0.1 m above a grounded plane z=0
V = image_potential_plane(q, d)        # real q at (0,0,d) + image -q at (0,0,-d)
V(0.05, 0.03, 0.0)                     # 0.0 V — exactly the grounded boundary
total_induced_charge(q, d)             # ~ -1e-9 C = -q  (all the image charge is real σ)
image_force(q, d)                      # ~ -2.25e-7 N: attractive, toward the conductor

Vs = slot_potential_series(10.0, 1.0)  # truncated Fourier sum, V0=10 V, slot width a=1
Vc = slot_potential_closed(10.0, 1.0)  # arctan closed form (Eq. 3.36)
Vs(0.3, 0.5), Vc(0.3, 0.5)             # agree to ~1e-4: the series collapses to the arctan

grid, xs, ys = solve_laplace_2d(lambda x, y: 10.0 * x)  # relax to the unique V = 10x
```

## Run
```bash
cd code
python3 boundary_value.py          # demo: image charge, the slot (series vs closed form), relaxation
python3 test_boundary_value.py     # tests  ->  "All 8 tests passed."
```
(`boundary_value.py` puts the `~EM-01`/`~EM-03` `code/` directories on `sys.path`;
this becomes `from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/boundary_value.py`, `code/test_boundary_value.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 3)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
