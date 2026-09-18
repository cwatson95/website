# MACRO_EM-02 — Introduction to Electrostatics (Wilcox Ch. 2 problems)

Module of the **MACROSCOPIC ELECTRODYNAMICS problems trunk** (see
`../list_MACRO_EM.txt`): one module per chapter of Wilcox & Thron,
*Macroscopic Electrodynamics* 2e, working **every exercise** of the chapter.

- **Source:** Ch. 2 *Introduction to Electrostatics*, exercises §2.14
  (printed pp.69–86, PDF pp.92–109; PDF = printed + 23). The book prints **no
  solutions** — every solution here is module-authored and machine-checked.
- **Prerequisites:** `~MACRO_EM-01` (units/appendix conventions); Griffiths-level
  `~EM-01/02/03` for the physics, `~MA-14` (Green functions), `~MA-15` (delta
  functions) for the math.
- **Feeds into:** `~MACRO_EM-03` (boundary-value problems — images and reduced
  Green functions build directly on §2.8), `~MACRO_EM-05` (multipoles — the
  dipole-layer far fields reappear as Eq. 5.15).
- **Units:** Gaussian, as in the book: $\vec E=-\vec\nabla\Phi$,
  $\vec\nabla\cdot\vec E=4\pi\rho$, $\Phi=q/r$.

## Scope

All **41 exercises** (2.1.1 – 2.12.11), numbered `P1..P41` in book order with the
book's C.S.N labels kept in each heading:

| Block | Exercises | Topics |
|---|---|---|
| P1 | 2.1.1 | dipole field as gradient *and* curl |
| P2–P5 | 2.2.1–2.2.4 | Jacobians, delta sequences, curvilinear deltas (spherical, oblate spheroidal) |
| P6–P9 | 2.4.1–2.4.4 | 2-D Gauss law & log potential, crossed line charges, cylinder/ring/cone axial fields |
| P10–P11 | 2.5.1–2.5.2 | Cavendish null test: $1/r^{1+\epsilon}$ and Yukawa (photon mass) |
| P12–P15 | 2.6.1–2.6.4 | charged disk ($C=2R/\pi$), dipole-layer construction, tilted layers, dipole shells |
| P16–P18 | 2.7.1–2.7.3 | Green's first identity, reciprocation theorem, mean value theorem |
| P19–P21 | 2.8.1–2.8.3 | $G_N\leftrightarrow G_D$ relation, symmetrization, polyhedron center average |
| P22–P25 | 2.9.1–2.9.4 | 1-D Dirichlet/Neumann Green functions, mixed-data solve, Helmholtz GF |
| P26–P29 | 2.10.1–2.10.4 | energy theorems, string/sheet/ball self-energies, classical electron radius |
| P30 | 2.11.1 | surface force (averaged-field prescription) |
| P31–P41 | 2.12.1–2.12.11 | capacitance matrix: inequalities, symmetry, shells, disks, distant conductors, variational bound, three wires |

Every problem carries a numeric check; the only fully analytic items are proofs
verified on closed-form instances (P16, P19–P21, P31–P32 style), and even those
run a quantitative instance in the tests.

## Operations — `code/intro_electrostatics.py`

| call | meaning | checked against |
|------|---------|-----------------|
| `dipole_phi/E/A` | $\vec d\cdot\vec x/r^3$ family | numeric grad/curl (P1) |
| `parallelepiped_volume`, `jacobian_matrix`, `scale_factors` | $\lvert\det M\rvert=UVW$ | `spherical_map` ($r^2$), `oblate_map` ($R^3(\xi^2+\mu^2)$) (P2, P4, P5) |
| `lorentzian_delta`, `delta2d_seq`, `smear_1d/2d` | delta sequences | unit mass, $f(0)$ sampling (P3) |
| `E2d_point`, `flux2d`, `laplacian2d_log` | 2-D Gauss law | $2\pi q_{\rm enc}$, harmonicity of $\ln r$ (P6) |
| `phi_segment(_quad)`, `phi_plus(_asym)`, `phi_halflines(_asym)` | finite-line potentials | quadrature + asymptotes (P7) |
| `Ez_disk`, `Ez_cylinder(_quad)`, `cylinder_center_slope` | axial cylinder field | disk-stack quadrature, slab limit (P8) |
| `Ez_ring(_quad)`, `Ez_cone_tip(_quad)` | ring & truncated cone | quadrature, $\sin2\alpha$ extremum (P9) |
| `phi_shell_eps(_quad)`, `qa_eps_exact/approx` | Cavendish $\epsilon$-shells | linear solve vs (2.65) (P10) |
| `phi_shell_yukawa(_quad)`, `qa_yukawa(_solve/_approx)` | Yukawa shells | ratio formula, $ab/6R^2$ limit (P11) |
| `phi_disk(_oblate)`, `sigma_disk`, `disk_capacitance` | charged disk | $A=2V/\pi$, $Q=2RV/\pi$, far field (P12) |
| `phi_dipole_disk_axis`, `phi_two_disks_axis`, `phi_pair_offset`, `phi_cap_dipole_axis_quad`, `Ez_dipole_cap_axis`, `phi_dipole_sphere` | dipole layers | $d\to0$ limits, $4\pi D$ jumps, hemisphere=disk axis field, sphere $\vec E=0$ (P13–P15) |
| `green_identity_sides` | Green's first identity | $16\pi R^7$ instance (P16) |
| `induced_charges_shells(_gauss)` | reciprocation | independent Gauss/continuity solve (P17) |
| `sphere_average` | mean value theorem | harmonic vs $x^2$ control (P18) |
| `gd1`, `gn1_unsym/symm`, `gn_gd_identity_rhs`, `phi_dirichlet_rep`, `phi_neumann_rep`, `phi_293` | 1-D Green functions | exact identities, BVP solves (P19–P24) |
| `cube_center_potential` | polyhedron average | Jacobi relaxation $\to1/6$ (P21) |
| `g_helmholtz`, `phi_helmholtz_direct/gf` | Helmholtz GF | jump, symmetry, $k_0\to0$, full solve (P25) |
| `energy_sphere_*`, `energy_field_quad`, `string_self_energy(_quad)`, `square_sheet_coeff_exact/quad`, `ball_self_energy(_quad)`, `classical_radius_uniform_cm` | energies | Thompson instance, log divergence, $1.4866048$, $(3{+}\alpha)/(5{+}2\alpha)$, $1.69\times10^{-13}$ cm (P26–P29) |
| `E_sphere_rho_sigma`, `surface_force_per_area` | surface force | $4\pi\sigma$ jump, $2\pi\sigma^2$ limit (P30) |
| `elastance_shells`, `cap_matrix_shells`, `cap_two_spheres`, `system_capacitance`, `energy_from_caps/at_charges` | capacitance matrix | inversion, Schwarz, sum rules, $\det/\Sigma$ (P31–P36) |
| `plates_C_small_d/large_d`, `distant_pair_cap_matrix`, `C12_approx`, `C22_approx` | disk pair, distant conductors | monopole model, $(R/\pi)(1+2R/\pi d)$ (P37–P39) |
| `cyl_trial_capacitance`, `cyl_exact_capacitance`, `cyl_functional_quad` | variational bound | $0.750L\ge0.7213L$ (P40) |
| `wire_potentials`, `three_wire_CL`, `three_wire_energy` | three-wire system | $N=12$, $w=\lambda^2/2C_L$ (P41) |

## Run

```bash
cd code
python3 intro_electrostatics.py         # demo: dipole, 2-D Gauss, disk C, cube 1/6, sheet 1.48660, shells, N=12
python3 test_intro_electrostatics.py    # tests  ->  "All 48 tests passed."   (~4 s)
```

## Files
- `problems/problems.md` — all 41 exercises: condensed statements, *Answer*,
  *Check* (function/test names), and **full stepwise solutions**
- `notes.md` — compact map of the chapter results the solutions lean on
  (printed-page + equation-number cites)
- `refs.md` — page-verified locations (PDF = printed + 23), exercise-block page
  table, cross-trunk pointers
- `code/intro_electrostatics.py` — the check library (numpy/scipy, Gaussian units)
- `code/test_intro_electrostatics.py` — 48 checks, at least one per exercise
