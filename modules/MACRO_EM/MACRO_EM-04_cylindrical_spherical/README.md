# MACRO_EM-04 — Cylindrical & Spherical Electrostatics (Wilcox Ch. 4 problems)

Module of the **MACROSCOPIC ELECTRODYNAMICS** problems trunk (see
`../list_MACRO_EM.txt`). Unlike the concept trunks, this is a **problems
library**: `problems/problems.md` works **every exercise of Wilcox & Thron 2e
Chapter 4** — all 49 of §4.16 (printed pp. 180–202) — with full stepwise
solutions and machine checks. The book prints no solutions; every solution
here is module-authored.

- **Prerequisites:** `~MACRO_EM-03` (Ch. 3: reduced Green functions, images,
  the §3.9 summation method, Thompson's variational bound), `~MA-11`
  (Sturm–Liouville orthogonality/completeness), `~MA-14` (Green functions),
  `~MA-08` (separation of variables).
- **Same physics at Griffiths level:** `~EM-04` (separation in cylindrical/
  spherical coordinates) — this module is the special-function upgrade:
  generating functions, Wronskian-built reduced kernels, Schwinger's
  $Y_{\ell m}$, eigenfunction expansions.
- **Feeds into:** `~MACRO_EM-05` (multipoles/dielectrics run on the
  $Y_{\ell m}$ machinery), Ch. 10 (the $J_m$ / $j_\ell$ zeros return as
  waveguide cutoffs and cavity spectra).

**Conventions:** the book's **Gaussian units**. $\nabla^2G=-4\pi\delta^3$
(4.73); 2-D reduced radial jump $-1/\rho'$; 1-D (2.124) has no $4\pi$;
$\mathcal J_{1m}(k_{mn}\rho)=\frac{\sqrt2}{a}J_m(x_{mn}\rho/a)/J_{m+1}(x_{mn})$
(4.67); spherical harmonics in the Condon–Shortley (= scipy) convention.

## Coverage (P → exercise)

| Section | Exercises | Problems |
|---|---|---|
| §4.1 Bessel via generating function | 4.1.1–4.1.4 | P1–P4 |
| §4.2 completeness / addition theorem | 4.2.1 | P5 |
| §4.3 zeros & orthogonality | 4.3.1 | P6 |
| §4.4 reduced $G$, flat/capped geometry | 4.4.1–4.4.4 | P7–P10 |
| §4.6 modified Bessel, asymptotics | 4.6.1–4.6.2 | P11–P12 |
| §4.7 Wronskian technique | 4.7.1–4.7.6 | P13–P18 |
| §4.8 conducting wedge family | 4.8.1–4.8.5 | P19–P23 |
| §4.9 Legendre / $Y_{\ell m}$ construction | 4.9.1–4.9.3 | P24–P26 |
| §4.11 Coulomb expansion, addition theorem | 4.11.1–4.11.6 | P27–P32 |
| §4.12 concentric spheres | 4.12.1–4.12.6 | P33–P38 |
| §4.13 split spheres, sphere point-electrostatics | 4.13.1–4.13.5 | P39–P43 |
| §4.14 eigenfunction expansions | 4.14.1–4.14.6 | P44–P49 |

(§4.5, §4.10 and §4.15 have no exercises.)

## Operations — `code/cylindrical_spherical.py` (highlights)

| call | meaning |
|------|---------|
| `jm_taylor`, `jn_intrep_413/415/416`, `sumrule_*` | §4.1: series, integral representations, sum rules (P1–P4) |
| `addition_j0_series`, `weber_gauss_closed/quad/lattice` | addition theorem; Gaussian-regulated completeness, Weber closed form (P5, P11) |
| `g_halfspace`, `G_axisym_from_g`, `G_halfplane_series` | wall / half-plane reduced kernels vs image answers (P7–P8) |
| `phi_capacitor_disk`, `Ez_capacitor_disk` | disk-driven Neumann/mixed parallel plates (P9) |
| `G_halfinf_cyl` | capped half-infinite cylinder $G_D$ (P10) |
| `phi_cyl_side_V`, `solve_laplace_axisym` | caps grounded + side at $V$; sparse-FD cross-check (P12) |
| `disk_C_var(_best)`, `hemi_C_var(_best)` | variational capacitances: disk 0.6213a, bowl 0.8052a (P13, P30) |
| `phi_patch_neumann(_axis_closed)` | Neumann patch potential, on-axis closed form (P14) |
| `wronskian_jnu_jmnu`, `wronskian_jm_nm`, `wronskian_fd` | $W[J_\nu,J_{-\nu}]$, $W[J_m,N_m]$ (P15) |
| `g_in_cyl`, `g_out_cyl`, `g_free_cyl`, `G_cyl_reduced_rho` | interior/exterior/free cylinder reduced $g$ (fractional order OK), assembler (P16, P22) |
| `g_toroid`, `G_toroid` | rectangular-section toroid kernel (P17) |
| `coulomb_cylJ`, `disk_free_potential_lhs/rhs` | (4.120) identity and the disk average (P18) |
| `wedge_series/closed`, `g_wedge_annulus`, `cyl2d_series/image`, `G_wedge3d`, `g_concentric_2d` | the §4.8 wedge family (P19–P23) |
| `legendre_explicit`, `legendre0(_seq)`, `dlegendre0`, `ylm` | explicit Legendre data; stable $P_{2n}(0)$; scipy-backed $Y_{\ell m}$ (P24–P25) |
| `integral_PlPl`, `ylm_rotation_coeffs`, `vandermonde_det` | projector integral; fixed-$\ell$ rotation closure (P29, P31) |
| `sphere_int_coulomb(_costh)` | spherical averages of the Coulomb kernel (P32) |
| `caps_terms/caps_C_partial/caps_sigma/caps_Q_top` | ±V hemispherical caps: the log-divergent $C$ series (P33) |
| `gN_ext_sphere_series/closed`, `gN_shell(_g0)` | Neumann sphere: image + line image; shell modes, §2.8 zero mode (P34–P35) |
| `sphere_poisson_kernel`, `sphere_series_from_V` | surface-data mode sum ↔ Poisson kernel (P36) |
| `hemi_basin_phi`, `concentric_C`, `E_center_split(_fd)` | hemisphere basin; $C_{ij}$ of concentric spheres; split-sphere field (P37–P39) |
| `Q0_legendre`, `sphereG_series` | point electrostatics on a sphere, $G=Q_0(\cos\gamma)$ (P40; book's factor-2 erratum flagged) |
| `unequal_caps_V2/_C_book/_C_simple`, `halves_C11_C12` | split-sphere potentials & capacitance matrices (P41–P42) |
| `gD_halfspace_sph_series/images` | half-space $G_D$ as $\ell{+}m$-odd harmonics (P43) |
| `sine_delta_action`, `g1d_eigen/closed`, `g_in_eigen` | completeness in action; 1-D and radial resolvents (P44, P46–P47) |
| `G_plates_bessel/images`, `G_finite_cyl_79/eigen`, `sumrule_sine(_closed)` | plates & finite cylinder: eigen-form ↔ (4.79) ↔ image ladder (P45, P48) |
| `sph_jn_zeros`, `sph_radial_residual` | $j_\ell(kr)Y_{\ell m}$ sphere eigenmodes (P49) |

## Use
```python
from cylindrical_spherical import (disk_C_var_best, hemi_C_var_best, caps_C_partial,
                                   g_in_cyl, wedge_closed, Q0_legendre, sphereG_series,
                                   concentric_C, E_center_split)
import numpy as np

disk_C_var_best()                  # (0.62126, 7.00)  book's 0.6213a bound
hemi_C_var_best()                  # (0.80515, -0.684) bowl bound, edge-weighted
caps_C_partial(4000)               # 6.27...  (log-divergent split-sphere C)
g_in_cyl(2, 1.3, 2.0, 1.1, 2.0)    # 0.0  (grounded wall)
wedge_closed(0.7, 0.6, 1.1, 0.9, np.pi/2)   # quadrant image answer
sphereG_series(0.5), Q0_legendre(0.5)       # 0.549306 both (P40 erratum check)
concentric_C(1.0, 2.5)             # (1.6667, -1.6667, 4.1667)
E_center_split(1.0, np.pi/3, 1.0)  # -1.125 = -(3V/2a) sin^2(60°)
```

## Run
```bash
cd code
python3 cylindrical_spherical.py           # demo: disk/bowl bounds, caps C, Q0
python3 test_cylindrical_spherical.py      # tests -> "All 52 tests passed."  (~50 s)
```

## Files
- `notes.md` — compact map of Ch. 4 (§4.1–§4.15) with printed-page cites:
  generating functions, completeness, the Wronskian recipe, wedge kernels,
  Schwinger's construction, Coulomb expansion, concentric spheres,
  eigenfunction expansions — plus the numerical-craft notes (scaled Bessel
  products, ratio-stable power sums, split-off free parts)
- `problems/problems.md` — **all 49 exercises**: statement (paraphrased, data
  intact), *Answer*, *Check* (code + test), **Solution** with every step
- `code/cylindrical_spherical.py` — the library (numpy/scipy.special)
- `code/test_cylindrical_spherical.py` — 52 checks; every exercise has a
  numeric check (none analytic-only)
- `refs.md` — page-verified locations (PDF = printed + 23), section map,
  exercise→problem table, errata notes (Ex. 4.13.2b factor 2; Ex. 4.2.1a
  $\rho'$ typo)
