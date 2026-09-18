# NE-21 — Neutron diffusion theory: Fick's law, the diffusion equation, criticality

Twenty-first module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), and the last of Chapter 10. Covers **§10.10**
(Addendum 1, printed pp. 356–362) of Shultis & Faw, 3rd ed.: the neutron balance,
Fick's law, the one-speed diffusion equation, fixed-source and criticality
problems, and Table 10.10's bare-core bucklings.

- **Prerequisites:** `~NE-19` (k_∞, L², and the bucklings it took on trust),
  `~NE-11` (macroscopic cross sections), `~MA-14` (the Helmholtz eigenproblem).
- **Cross-links:** `~NE-20` (point kinetics integrates this space away),
  `~NE-22` (power peaking as a design constraint).

## Scope
Where the buckling comes from. A balance sheet on a differential volume, plus the
assumption that neutrons flow down the flux gradient, gives a second-order PDE
that splits the subject in two: with a source it is a **fixed-source** problem and
L is the decay length; without one it is an **eigenvalue** problem, and
criticality is the single condition **B²_mat = B²_g** — material on the left,
geometry on the right. Two things `~NE-19` could only assert then follow: the
thermal non-leakage probability 1/(1+L²B²), and the fact that the flux shape, and
hence the power peaking, is pure geometry with no material in it.

## Operations — `code/diffusion.py`

| call | meaning | reference |
|------|---------|-----------|
| `fick_current(D, dφ/dx)` | J = −D dφ/dx | Eq. (10.58) |
| `diffusion_coefficient(Σ_tr)`, `transport_mfp` | D = λ_tr/3 | added |
| `diffusion_length(D, Σ_a)`, `diffusion_length_squared` | L = √(D/Σ_a) | Eq. (10.66) |
| `plane_source_flux(S₀, x, D, L)` | (S₀L/2D)e^{−|x|/L} | Eq. (10.72) |
| `point_source_flux(S, r, D, L)` | S e^{−r/L}/(4πDr) — **not** the uncollided form | added |
| `diffusion_valid(distance, Σ_tr)` | is Fick's law trustworthy here? | added |
| `material_buckling(k_∞, L²)` | (k_∞−1)/L² | Eq. (10.73) |
| `geometric_buckling(geom, **dims)` | slab, parallelepiped, sphere, cylinders | Table 10.10 |
| `critical_dimension(geom, k_∞, L²)` | solves B²_g = B²_mat; **refuses k_∞ ≤ 1** | Eq. (10.80) |
| `critical_flux_profile(geom, pos, **dims)` | Table 10.10's eigenfunctions | Table 10.10 |
| `peak_to_average(geom)` | π/2, 2.32, π²/3, 3.64, (π/2)³ | added |
| `extrapolation_distance`, `extrapolated_dimension` | d = 0.7104 λ_tr, which S&F drop | added |
| `k_effective_from_buckling(k_∞, L², B²)` | k_∞/(1+L²B²) — `~NE-19`'s Eq. (10.13) derived | added |
| `bessel_j0`, `bessel_j1` | for the cylindrical profiles, stdlib only | — |

## Use
```python
from diffusion import (plane_source_flux, point_source_flux, diffusion_valid,
                       material_buckling, geometric_buckling, critical_dimension,
                       peak_to_average, k_effective_from_buckling,
                       extrapolated_dimension)

plane_source_flux(1.0, 55.4, D=0.84, L=55.4)   # 1/e of the peak, by construction
diffusion_valid(5.0, sigma_tr=0.4)             # False -- within 3 transport mfp

material_buckling(1.6939, 570.1)               # 1.217e-3 /cm2
critical_dimension("sphere", 1.6939, 570.1)    # 90.0 cm (one-speed; ~NE-19's 127 cm
                                               #   includes fast leakage)
critical_dimension("sphere", 0.781, 570.1)     # raises: k_inf <= 1, no size works
peak_to_average("cylinder")                    # 3.639 -- the bare-core penalty

k_effective_from_buckling(1.6939, 570.1, geometric_buckling("sphere", R=120.0))
extrapolated_dimension(20.0, sigma_tr=0.4)     # 23.6 cm: an 18% correction
```

## Run
```bash
cd code
python3 diffusion.py        # demo: the plane source, criticality, peaking, the limits
python3 test_diffusion.py   # tests  ->  "All 11 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — Fick's law and its Fourier ancestry → the equation → what L means
  → criticality as an eigenvalue problem → the flux shape as pure geometry →
  the three places it stops working, with a "Where this goes" map and a note on
  the module's one correction.
- `code/diffusion.py`, `code/test_diffusion.py` (stdlib only, including its own
  Bessel J₀ and J₁). `critical_dimension` **refuses** k_∞ ≤ 1, because leakage
  only removes neutrons and no bare assembly of such a material is critical at
  any size; `diffusion_valid` exists so that Fick's law is not used where it is
  known to fail. The plane- and point-source solutions are checked against
  neutron conservation, not just against the book's algebra.
- `problems/problems.md` — 6 worked problems with numeric `*Check:*` lines.
- `figures/` — the plane-source solution against the uncollided beam with the
  invalid zone marked, the critical profiles beside their peaking factors,
  buckling as an intersection, and what the extrapolation distance and the
  one-speed approximation each cost.
- `refs.md` — page-verified citations; the printed **n** in Eq. (10.79) that
  should not be there; and the three approximations the module quantifies rather
  than inherits.
