# MACRO_EM-06 — Magnetostatics (Wilcox Ch. 6 problems)

Module of the **MACROSCOPIC ELECTRODYNAMICS** problems trunk (see
`../list_MACRO_EM.txt`). Unlike the concept trunks, this is a **problems
library**: `problems/problems.md` works **every exercise of Wilcox & Thron
2e Chapter 6** — all 38 of §6.15 (printed pp. 316–336) — with full stepwise
solutions and machine checks. The book prints no solutions; every solution
here is module-authored.

- **Prerequisites:** `~MACRO_EM-04` (cylindrical/spherical Green expansions
  (4.120)/(4.225), modified Bessels §4.6, Legendre identities),
  `~MACRO_EM-05` (dielectric images (5.106)–(5.107), sphere in a field
  Ex. 5.7.3 — transcribed by §§6.11–6.12), `~MACRO_EM-03` (image method;
  Ex. 3.3.3 is P31's electrostatic twin), `~MA-08`/`~MA-11`
  (Bessel/Legendre machinery).
- **Same physics at Griffiths level:** `~EM-05` (Biot–Savart, Ampère,
  vector potential, magnetized matter) — this module is the
  solid-angle/Bessel-kernel/image-current upgrade.
- **Feeds into:** `~MACRO_EM-07` (time-varying fields; §7.8 reuses the
  multivalued $\Omega$ for monopoles).

**Conventions:** the book's **Gaussian units**. Biot–Savart
$\vec B=\frac Ic\oint d\vec x'\times(\vec x-\vec x')/|\vec x-\vec x'|^3$;
$\vec\nabla\times\vec B=\frac{4\pi}{c}\vec J$; solid angle per (6.67)–(6.69)
(negative above a $+\hat z$-oriented sheet); $\vec m=\frac1{2c}\int\vec
x\times\vec J$; $\vec H=\vec B-4\pi\vec M$; code sets $c=1$ (constant `C`)
with every $1/c$ kept explicit.

## Coverage (P → exercise)

| Section | Exercises | Problems |
|---|---|---|
| §6.1 analogy / circuit force | 6.1.1 | P1 |
| §6.3 Ampère & pinch | 6.3.1–6.3.2 | P2–P3 |
| §6.4 current sheet | 6.4.1 | P4 |
| §6.5 Stokes transform | 6.5.1 | P5 |
| §6.6 loop/solenoid Bessel kernels | 6.6.1–6.6.5 | P6–P10 |
| §6.7 solid-angle series, rotating spheres | 6.7.1–6.7.5 | P11–P15 |
| §6.8 moments, dipole delta, quadrupoles | 6.8.1–6.8.6 | P16–P21 |
| §6.9 forces & torques on dipoles | 6.9.1–6.9.2 | P22–P23 |
| §6.10 magnetization, H, cavity | 6.10.1–6.10.2 | P24–P25 |
| §6.11 permeable sphere | 6.11.1 | P26 |
| §6.12 image method | 6.12.1–6.12.6 | P27–P32 |
| §6.13 intrinsic magnetization | 6.13.1–6.13.6 | P33–P38 |

(§6.2 and §6.14 have no exercises; the §6.15 numbering runs 6.1.1 then
6.3.1 onward.)

## Operations — `code/magnetostatics.py` (highlights)

| call | meaning |
|------|---------|
| `loop_B_elliptic`, `loop_B_bessel`, `loop_B_3d`, `loop_Bz_axis` | circular-loop field: elliptic closed form, (6.83)–(6.84) kernels, 3-D Biot–Savart polygon, on-axis (6.62) |
| `loop_A_bessel`, `loop_A_IK`, `loop_A_3d` | loop potential: (6.227), the $I_1K_1$ form (P9), direct line integral |
| `chord_force`, `circuit_force_partial` | P1: $\vec F=\frac Ic\vec L\times\vec B$ vs segment sum |
| `pinch_pressure(_quad)`, `wire_B_phi` | P2: $P=\frac{I^2}{\pi c^2a^2}(1-\rho^2/a^2)$, Ampère field |
| `spinning_cylinder_B(_quad)`, `sheet_B(_wires)` | P3/P4 closed forms vs Biot–Savart superpositions |
| `stokes_transform_lhs/rhs` | P5: $\oint d\vec\ell\times\vec A=\int(d\vec s\times\vec\nabla)\times\vec A$ |
| `solenoid_B_inside_bessel`, `solenoid_Bz_outside_bessel`, `solenoid_corr_axis(_asym)`, `solenoid_B_loops` | P6/P16: finite solenoid kernels, $1/d^2$ end correction, loop-stack benchmark |
| `spinning_disk_B_bessel(_rings)`, `spinning_disk_moment` | P7: $J_2(kR)$ kernels, $m=\pi\sigma\omega R^4/4c$ |
| `spinning_cylinder_solid_Bz_bessel(_disks)`, `weber_schafheitlin` | P8: rotating solid cylinder, step-term integral |
| `cone_Bz_tip(_quad)` | P10: $\frac{2\pi\sigma\omega}{c}(L_2{-}L_1)\sin^3\alpha/\cos\alpha$ |
| `solid_angle_disk_series(_split)`, `solid_angle_disk_bessel/_quad/_axis`, `solid_angle_rect` | P11: all four representations of the disk solid angle |
| `loop_Br_series`, `loop_Bth_series`, `loop_B_spherical` | P12: (6.119)/(6.121) vs elliptic benchmark |
| `rotating_shell_B`, `rotating_solid_sphere_B`, `costheta_shell_B` (+`_quad`) | P13–P15: rotating spheres (uniform, solid, $\cos\theta$) |
| `slab_equiv_current`, `slab_B_charges` | P17: shaved magnet $\equiv$ rim current $I=cM_0d$ |
| `circuit_moment`, `saddle_circuit/moment`, `bent_loop_circuit/moment` | P18: $\frac1{2c}\oint\vec x\times d\vec\ell$ vs closed forms |
| `gradgrad_1r_box`, `dipole_ball_integral`, `jm_moment_smeared` | P19: (6.139) delta weights, $\frac{8\pi}3\vec m$, $\vec J_m$ moment |
| `make_divfree_J`, `moment_vector`, `quad_moment_mij`, `cyclic_integral`, `A_quadrupole`, `B_quadrupole`, `costheta_shell_sij(_quad)` | P20–P21: magnetic quadrupole machinery |
| `wire_dipole_force/torque`, `small_loop_force/torque`, `force_grad_mB` | P22–P23: dipole near a wire; $\vec F=\vec\nabla(\vec m\cdot\vec B)$ |
| `hemisphere_torque(_quad)` | P24: surface torque $=\vec m\times\vec B_0$ |
| `cavity_C1C2`, `sphere_C1C2`, `cavity_fields`, `cavity_Kb_coefficient` | P25: dipole in cavity / permeable sphere |
| `perm_sphere_phim/B/M` | P26: sphere in uniform field, $\vec M=\frac3{4\pi}\frac{\mu-1}{\mu+2}\vec B_0$ |
| `image_coeffs_vacuum_source/embedded_source`, `interface_BC_residual_*`, `loop_image_force` | P27–P28: plane-interface image currents |
| `solid_angle_B`, `greens_phim` | P29–P30: solid-angle answer and general Green representation |
| `sphere_image_ring` | P31: superconducting sphere, $I^*=-(r_0/a)I$ at $a^2/r_0$ |
| `dipole_slab_force(_quad)` | P32: $F_z=-\frac{3m^2(1+\cos^2\theta)}{16d^4}\frac{\mu-1}{\mu+1}$ |
| `A_magnetized_sphere`, `A_magnetization_surface`, `A_direct_dipole_sum`, `A_curl_plus_surface` | P33: magnetization potential volume+surface split |
| `split_sphere_Cn/phim_exterior/phim_interior/phim_quad` | P34: split-sphere magnet (book $C_n$ outside; corrected interior) |
| `bar_H_exact/monopoles`, `cube_Hz(_direct)`, `square_face_omega` | P35–P36: monopole ends; $H_z=-M_0\Omega$, cube center $-\frac{4\pi}3M_0$ |
| `rod_H_bessel/disks` | P37: rod magnet $\vec H$, solenoid harmonization |
| `closed_shell_phim_sphere/cube` | P38: normal-magnetized shell, $-4\pi M_A$ inside |

## Use
```python
from magnetostatics import (loop_B_elliptic, loop_Bz_axis, cavity_C1C2,
                            dipole_slab_force, split_sphere_Cn, cube_Hz_direct,
                            rotating_shell_B, image_coeffs_vacuum_source)
import numpy as np

loop_Bz_axis(0.0, 1.0, 1.0)          # 2*pi (on-axis loop, a=I=1, z=0)
loop_B_elliptic(0.6, 0.4, 1.0, 1.0)  # (B_rho, B_z) = (2.274098, 5.069283)
cavity_C1C2(2.6)                     # (0.258065, 1.258065)  [(mu-1)/(2mu+1), 3mu/(2mu+1)]
image_coeffs_vacuum_source(3.0)      # (0.5, -0.5, 1.5)      [a, b, c']
dipole_slab_force(1, 1, 3, 0.0)      # -0.1875 = -3*(1+1)/(16*2)
split_sphere_Cn(1)                   # 0.25 (exterior quadrupole coefficient)
cube_Hz_direct(np.zeros(3), 1.0, 1.0)  # -4.18879 = -4*pi/3 (cube center)
rotating_shell_B([0.2, 0.1, 0.3], 1.0, 0.7, 1.2)  # uniform 8*pi*a*sigma*omega/(3c) zhat
```

## Run
```bash
cd code
python3 magnetostatics.py           # demo: loop forms, cone, moments, cavity, slab force
python3 test_magnetostatics.py      # tests  ->  "All 42 tests passed."  (~30 s)
```

## Files
- `notes.md` — compact map of Ch. 6 (§6.1–§6.14) with printed-page cites:
  Biot–Savart & Ampère, vector potential & gauge, the solid-angle formula,
  the loop both ways, moments & quadrupoles, forces/torques, magnetization &
  H, boundary conditions, image method, intrinsic magnetization
- `problems/problems.md` — **all 38 exercises**: statement (paraphrased,
  data intact), *Answer*, *Check* (code + test), **Solution** with every
  step
- `code/magnetostatics.py` — the library (numpy/scipy: elliptic/Bessel loop
  kernels, solid angles, Biot–Savart quadratures, multipole integrals, image
  systems, magnetic-charge potentials)
- `code/test_magnetostatics.py` — 42 checks; every exercise has a numeric
  check (P1–P38 all covered, plus global div/curl/Ampère Maxwell checks)
- `refs.md` — page-verified locations (PDF = printed + 23) and the four
  book-text caveats found while transcribing (Ex. 6.6.2 limit variables,
  Ex. 6.6.3 step notation, Ex. 6.8.5(c) prefactor, Ex. 6.13.2 interior
  branch)
