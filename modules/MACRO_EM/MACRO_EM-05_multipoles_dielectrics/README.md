# MACRO_EM-05 — Multipoles, Macroscopic Media, Dielectrics (Wilcox Ch. 5 problems)

Module of the **MACROSCOPIC ELECTRODYNAMICS** problems trunk (see
`../list_MACRO_EM.txt`). A **problems library**: `problems/problems.md` works
**every exercise of Wilcox & Thron 2e Chapter 5** — all 49 of §5.13 (printed
pp. 242–266) — with full stepwise solutions and machine checks. The book
prints no solutions; every solution here is module-authored.

- **Prerequisites:** `~MACRO_EM-04` (Bessel/Legendre reduced Green functions;
  Exs. 4.2.1, 4.9.1, 4.13.4 are direct inputs), `~MACRO_EM-03` (images,
  reduced $g$, uniqueness), `~MACRO_EM-02` (Green identities, energy),
  `~MA-11`/`~MA-14` (orthogonal expansions, Green functions).
- **Same physics at Griffiths level:** `~EM-05` (multipoles, polarization,
  D-field) — this module adds the systematic Cartesian/spherical expansions,
  dielectric Green functions, and the fixed-$Q$/fixed-$V$ force calculus.
- **Feeds into:** `~MACRO_EM-06` (magnetization/H mirrors polarization/D),
  `~MACRO_EM-09` ($\epsilon(\omega)$).

**Conventions:** the book's **Gaussian units**. $\vec D=\vec E+4\pi\vec P
=\epsilon\vec E$, $\epsilon=1+4\pi\chi$; bound charge
$\rho_b=-\vec\nabla\cdot\vec P$, $\sigma_b=\vec P\cdot\hat n$; dielectric
Green equation $\vec\nabla\cdot[\epsilon\vec\nabla G]=-4\pi\delta$; interface
conditions: $\Phi$ and $D_n$ continuous.

## Coverage (P → exercise)

| Section | Exercises | Problems |
|---|---|---|
| §5.1 multipole expansions | 5.1.1–5.1.6 | P1–P6 |
| §5.2 multipole energies | 5.2.1–5.2.3 | P7–P9 |
| §5.3 forces & torques | 5.3.1 | P10 |
| §5.4 polarization & D | 5.4.1–5.4.5 | P11–P15 |
| §5.6 slab Green functions | 5.6.1–5.6.6 | P16–P21 |
| §5.7 sphere/cylinder Green functions | 5.7.1–5.7.12 | P22–P33 |
| §5.8 field energy | 5.8.1 | P34 |
| §5.9 forces on dielectrics | 5.9.1–5.9.10 | P35–P44 |
| §5.10 leading-log model | 5.10.1 | P45 |
| §5.11 force examples | 5.11.1–5.11.4 | P46–P49 |

(§5.5 — dielectric Green-function theory — and §5.12 — Going Deeper — have no
exercises.) **Errata found:** Ex. 5.2.2's sign ($+9/16$, not $-9/16$) and
Ex. 5.7.12's power ($a^5$, not $a^3$) — both settled numerically; see
`refs.md`.

## Operations — `code/multipole_dielectrics.py` (highlights)

| call | meaning |
|------|---------|
| `moments_point_charges`, `moments_translate` | $q,\vec p,Q_{ij}$ and the P2 translation law |
| `octopole_R`, `octopole_independent_count` | $R_{ijk}$ (15/−3 form), rank = 7 (P4) |
| `dipole_above_plane_phi`, `sigma_dipole_plane` | image dipole $(-p_x,-p_y,p_z)$; $\sigma\propto(2d^2-\rho^2)$ (P6) |
| `quad_energy_in_potential`, `quad_force_axial` | $W=\frac14Q_{33}\Phi_{zz}$, $\vec F=\frac14Q_{33}\partial_z^2\vec E$ (P7) |
| `W_quad_quad_perp/axial` + `W_charges_pair` | $+\frac9{16},+\frac32\;Q_1Q_2/r^5$ and the microscopic erratum check (P8) |
| `sphere_image_W_sum/closed` | (5.37) geometric series → image energy (P9) |
| `force_multipole`, `torque_multipole` | (5.53)-form force; $N=p\times E+\frac13\epsilon QdE$ (P10) |
| `quad_density_check` | $\rho^Q_{\rm eff},\sigma^Q_{\rm eff},\mathcal P^Q_{\rm eff}$ quadrature identity (P11) |
| `cylinder_in_field_phi` | $E_{\rm in}=\frac2{\epsilon+1}E_0$ transverse cylinder (P13) |
| `polarized_sphere_surface_E`, `solid_angle_square_from_center` | Lorentz cavity $\frac{4\pi}3P_0$: sphere and cube (P14–P15) |
| `clausius_mossotti_alpha` | $\alpha=\frac1N\chi/(1+\frac{4\pi}3\chi)$ (P15c) |
| `corner_dielectric_G(_region)`, `corner_interface_residuals` | $\beta,\beta,\beta^2$ corner images; exact iff factorizable medium (P16) |
| `g_slab_conductor_book/solve`, `g_slab_swapped_solve` | conductor+slab kernel; $\epsilon\to1/\epsilon$ swap rule (P17–P18) |
| `oneD_G_dielectric(_fd)` | two-wall 1-D kernel, $d/\epsilon$ reduced thickness (P19) |
| `two_halfspace_phi` | $q'=q\frac{\epsilon_2-\epsilon_1}{\epsilon_2+\epsilon_1}$, $q''=\frac{2q\epsilon_1}{\epsilon_1+\epsilon_2}$ (P20) |
| `slab_finite_solve` | finite slab: 6 coefficients, all limits (P21) |
| `gm_cyl2d`, `G_cyl2d` | 2-D dielectric-cylinder modes; $-2\ln\vert x-x'\vert$ at $\epsilon=1$ (P22) |
| `cyl3d_gm_solve`, `G_cyl3d` | $I_m/K_m$ reduced modes; $1/\vert x-x'\vert$ check (P23) |
| `sphere_G_in/out(_induced)`, `sphere_uniform_field_phi` | (5.140)/(5.141) kernels; uniform-field sphere (P24) |
| `sphere_source_inside_coeffs/solve` | interior-source kernel; $p_{\rm eff}=3r'/(\epsilon+2)$, $\oint\sigma_b=\frac{\epsilon-1}\epsilon$ (P25) |
| `bubble_G_out`, `bubble_gl_solve` | bubble $=\frac1\epsilon$sphere$(1/\epsilon)$ (P26) |
| `sphere_dipole_p_eff/E_in` | dipole near sphere: far moment, interior screening (P27) |
| `sphere_in_conductor_solve` | dielectric core in grounded shell (P28) |
| `plane_moment_integral`, `plane_sigma_phi_in` | charged plane: only $\ell=1$ survives (P29) |
| `ring_sphere_phi_in(_points)` | ring source: $(-1)^n\frac{(2n-1)!!}{(2n)!!}$ series (P30) |
| `split_sphere_C`, `split_sphere_Q1_quad` | $C_{11}(\varepsilon),C_{12}(\varepsilon)$ hemisphere sums (P31) |
| `coaxial_cyl_solve`, `G_coaxial` | dielectric core in conducting cylinder (P32) |
| `induced_quadrupole_sphere(_from_sigma)` | $Q_{ij}=\frac{2a^5(\epsilon-1)}{3+2\epsilon}(-\partial E'_j/\partial x'_i)$, $a^5$ erratum (P33) |
| `polarized_sphere_ED_integral/Wint` | $\int E\cdot D=0$; $-\frac12\int P\cdot E=\frac1{8\pi}\int E^2$ (P34) |
| `surface_force_from_fields/sigma_b/free_bound` | $\frac1{8\pi}(E_{2n}^2-E_{1n}^2)$ family (P35) |
| `halfspace_force_image/deltaW/stress` | half-space force three ways (P36) |
| `rod_force_perp/par`, `prolate_depolarization_nz` | rod forces; needle limit $n_z\to0$ (P37–P38) |
| `capacitor_force_fixed_V/Q` | slab-in-capacitor, both protocols (P39) |
| `slab_force_integral/weak`, `slab_deltaW` | exact slab force; weak-dielectric 3-image form (P40–P41) |
| `plate_sigma_kspace/images`, `plate_force_kspace/images` | $\epsilon\to\infty$ second plate; $-z'/d$ charge division (P42) |
| `layered_capacitor_force_V/Q` | battery attached vs disconnected (P43) |
| `line_cylinder_deltaW/force` | $\Delta W=-\beta\ln(1-a^2/\rho'^2)$ resummation (P44) |
| `leading_log_*` | perfect differential + $\delta^2W>0$ (P45) |
| `bubble_charge_*`, `sphere_deltaW_from_P` | bubble repulsion; (5.173) route to (5.202) (P46–P47) |
| `droplet_inside_force_series`, `droplet_deltaW` | charge in a droplet: central trap (P48) |
| `sphere_dipole_W(_exact)`, `sphere_dipole_force` | dipole–sphere $d^{-7}$ force (P49) |

## Use
```python
from multipole_dielectrics import (moments_translate, sphere_G_out,
    two_halfspace_phi, sphere_charge_force_far, droplet_inside_force_series,
    line_cylinder_force, split_sphere_C)
import numpy as np

moments_translate(1.0, np.array([0,0,1.0]), np.zeros((3,3)), np.array([0,0,1.0]))[1]
                                        # p' = p - qR = 0 (P1)
sphere_G_out(2.0, 3.0, 1.0, 1.0, 4.0)   # (5.141) kernel on-axis
sphere_charge_force_far(4.0, 1.0, 3.0)  # -7.8e-4 (Eq. 5.202, attraction)
line_cylinder_force(1.7, 1.0, 2.5)      # -0.318 (P44, attraction)
droplet_inside_force_series(0.3, 1.0, 2.0)   # -0.088 (P48, toward center)
split_sphere_C(4.5, 1.0)                # (C11, C12) with dielectric filling
```

## Run
```bash
cd code
python3 multipole_dielectrics.py         # demo: quadrupole erratum, forces
python3 test_multipole_dielectrics.py    # tests -> "All 49 tests passed." (~9 s)
```

## Files
- `notes.md` — compact map of Ch. 5 (§5.1–§5.12) with printed-page cites:
  multipole expansions and energies, polarization/D, dielectric Green
  functions (slab, sphere, cylinder), energy and force calculus, the
  leading-log confinement model, and the errata list
- `problems/problems.md` — **all 49 exercises**: statement (paraphrased, data
  intact), *Answer*, *Check* (code + test), **Solution** with every step
- `code/multipole_dielectrics.py` — the library (numpy/scipy: moment algebra,
  batched radial solves, Bessel/Legendre kernels, quadrature checks,
  virtual-work force machinery)
- `code/test_multipole_dielectrics.py` — 49 checks (one per exercise; several
  asserts each); every exercise admits and gets a numeric check
- `refs.md` — page-verified locations (PDF = printed + 23) and the errata
