# MACRO_EM-03 — Boundary Value Problems (Wilcox Ch. 3 problems)

Module of the **MACROSCOPIC ELECTRODYNAMICS** problems trunk (see
`../list_MACRO_EM.txt`). Unlike the concept trunks, this is a **problems
library**: `problems/problems.md` works **every exercise of Wilcox & Thron 2e
Chapter 3** — all 33 of §3.13 (printed pp. 120–133) — with full stepwise
solutions and machine checks. The book prints no solutions; every solution
here is module-authored.

- **Prerequisites:** `~MACRO_EM-02` (Ch. 2: Green identities, the (2.98)
  representation, uniqueness, capacitance matrix), `~MA-14` (Green functions),
  `~MA-08`/`~MA-11` (separation of variables, orthogonal eigenfunctions),
  `~MA-06` (complex analysis, for §3.11).
- **Same physics at Griffiths level:** `~EM-04` (images, separation,
  relaxation) — cross-linked throughout; this module is the Green-function
  upgrade (reduced Green functions, eigenfunction kernels, Robin conditions,
  image *densities*, variational bounds, conformal maps).
- **Feeds into:** `~MACRO_EM-04` (cylindrical/spherical eigenfunctions redo
  these geometries), `~MACRO_EM-05` (dielectrics/multipoles).

**Conventions:** the book's **Gaussian units**. $\Phi=q/r$ for a point
charge; $\nabla^2G=-4\pi\delta$; $\sigma=\frac1{4\pi}\partial_n\Phi$; 2-D
line charges use $G=-2\ln\rho$.

## Coverage (P → exercise)

| Section | Exercises | Problems |
|---|---|---|
| §3.1 plane & corner images | 3.1.1–3.1.5 | P1–P5 |
| §3.2 reduced Green functions | 3.2.1–3.2.4 | P6–P9 |
| §3.3 sphere/cylinder images | 3.3.1–3.3.8 | P10–P17 |
| §3.5 Cartesian separation | 3.5.1–3.5.6 | P18–P23 |
| §3.6 box eigenfunction kernel | 3.6.1 (Madelung) | P24 |
| §3.7–§3.9 polar problems | 3.7.1, 3.8.1, 3.9.1–3.9.5 | P25–P31 |
| §3.11 conformal mapping | 3.11.1–3.11.2 | P32–P33 |

(§3.4 and §3.10 have no exercises; §3.10's variational capacitance bound is
covered by a notes-level check, `test_variational_disk_bound`.)

## Operations — `code/bvp_greens.py` (highlights)

| call | meaning |
|------|---------|
| `green_plane`, `green_corner`, `green_perp_2d` | image Green functions: half-space, 3-D corner, 2-D corner |
| `green_plates_images` / `g_reduced_plates` / `green_plates_kspace` | parallel plates: image ladder vs reduced-$g$ $k$-integral (P1↔P8) |
| `g_reduced_halfspace(k,z,z',kind,h)` | reduced $g$: Dirichlet, Neumann, **Robin** $\beta=\frac{hk-1}{hk+1}$ (P7, P9) |
| `plate_induced_charge(_quad)` | $Q\vert_{z=0}=-(1-z'/a)$, $Q\vert_{z=a}=-z'/a$ (P8b) |
| `sphere_image`, `green_sphere`, `green_cylinder` | Eq. (3.46)/(3.48) and the cylindrical log twin (P10, P14) |
| `rho_star`, `image_cloud` | image charge *density* $-(a/r)^5\rho(a^2/r)$ (P12) |
| `two_sphere_C`, `two_sphere_C_system` | iterated-image capacitance matrix; $C_{ab}\to-ab/d$ (P13) |
| `force_sphere_V`, `force_sphere_neutral`, `V_zero_force` | forces from held-at-$V$ / neutral spheres (P17) |
| `box2d_phi`, `strip_phi`, `green_strip_D/N`, `green_2plates_2d_*` | §3.5 separation solutions and slot Green functions (P18–P23) |
| `solve_laplace_rect` | sparse FD Laplace solver — the uniqueness cross-check |
| `green_box3d`, `madelung_from_box_green`, `madelung_evjen` | Eq. (3.98) kernel; Madelung $-1.747564594$ from its regularized self-limit (P24) |
| `poisson_kernel`, `poisson_integral`, `cyl_delta_series` | 2-D Poisson integral and the delta-data series it sums (P25, P27, P31) |
| `wedge_coeffs`, `wedge_phi` | pie wedge with end data; $\rho^{\pi/\beta-1}$ corner field (P26) |
| `halves_series/closed/axis`, `halves_exterior_*` | split cylinder (3.130)/(3.131), exterior, on-axis $2\arctan(\rho/b)$ (P28–P30) |
| `disk_C_variational` | Thompson/(3.144) lower bound on $C$ (uniform trial $3\pi R/16<2R/\pi$) |
| `cauchy_riemann_residual`, `map_box_to_halfannulus`, `semicircle_phi`, `exterior_from_inversion` | conformal checks: CR residuals, boundary tracing, pullbacks (P32–P33) |

## Use
```python
from bvp_greens import (green_sphere, force_sphere_neutral, madelung_from_box_green,
                        halves_closed, halves_axis, two_sphere_C, disk_C_variational)
import numpy as np

green_sphere(np.array([0,0,1.0]), np.array([0,0,0.3]), a=1.0)   # 0.0 on the shell
force_sphere_neutral(q=1, a=1, d=3)     # -0.009838  (always attractive)
madelung_from_box_green()               # -1.7475635 (Ex. 3.6.1, vs -1.747564594)
two_sphere_C(1.0, 2.0, 30.0)[1]         # -0.06682   (~ -ab/d = -0.06667)
halves_closed(0.5, 0.0, 1.0, 1, -1) == halves_axis(0.5, 1.0, 1, -1)  # axis arctan
disk_C_variational(lambda r: np.ones_like(r), 1.0)   # 0.58928 = 3*pi/16 < 2/pi
```

## Run
```bash
cd code
python3 bvp_greens.py           # demo: corner work, Madelung, C_ab, disk bound
python3 test_bvp_greens.py      # tests  ->  "All 44 tests passed."  (~10 s)
```

## Files
- `notes.md` — compact map of Ch. 3 (§3.1–§3.12) with printed-page cites:
  images, reduced Green functions, the box eigenfunction kernel and its image
  lattice, polar/corner/halves results, Thompson's bound, conformal mapping
- `problems/problems.md` — **all 33 exercises**: statement (paraphrased, data
  intact), *Answer*, *Check* (code + test), **Solution** with every step
- `code/bvp_greens.py` — the library (numpy/scipy: image sums, reduced-$g$
  $k$-integrals, sparse FD Laplace, elliptic-kernel energies, series/closed
  forms, conformal maps)
- `code/test_bvp_greens.py` — 44 checks; every exercise that admits a numeric
  check has one (all 33 do, via 43 exercise-tests + 1 variational notes-test)
- `refs.md` — page-verified locations (PDF = printed + 23)
