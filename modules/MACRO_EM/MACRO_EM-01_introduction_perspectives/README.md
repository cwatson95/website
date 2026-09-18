# MACRO_EM-01 — Introduction & Perspectives (Wilcox Ch. 1 problems)

Module of the **MACROSCOPIC ELECTRODYNAMICS problems trunk** (see
`../list_MACRO_EM.txt`). Unlike the concept trunks (EM, QM, …), this trunk is a
**problems library**: one module per chapter of Wilcox & Thron, *Macroscopic
Electrodynamics: An Introduction* (2nd ed.), with **every exercise of the
chapter worked** — statement transcribed from the PDF, full stepwise solution,
and a machine check wherever the problem admits one. The book prints no
solutions; everything in `problems/problems.md` is module-authored and verified
by `code/test_intro_perspectives.py`.

- **Covers:** Ch. 1 *Introduction and Perspectives* (printed pp. 1–28) **plus**
  Appendix A *Appendix on Electromagnetic Units* (printed pp. 859–866), whose
  two exercises are folded in here because §1.6.2 is the units section.
- **Exercises worked (9):** 1.1.1, 1.1.2, 1.1.3, 1.4.1, 1.4.2, 1.4.3, 1.5.1
  (§1.7, printed pp. 21–22) and A.1.1, A.1.2 (§A.1, printed p. 862) → `P1…P9`.
- **Prerequisites:** `~MA-02` (grad/div/curl, Gauss & Stokes theorems);
  `~MA-15` helps for the δ-function reading of P3/P7.
- **Feeds into:** every later MACRO_EM module (the boundary-condition pillbox/
  loop technique, the §1.8 identity glossary, and the unit conventions are used
  chapter after chapter); concept-trunk siblings `~EM-01` and `~EM-13`.

**House rule:** the book works in **Gaussian units** — Maxwell's equations
carry their factors of $4\pi$ and $1/c$ explicitly
(e.g. $\vec\nabla\times\vec E+\frac1c\frac{\partial\vec B}{\partial t}=0$),
and the code keeps those conventions everywhere.

## Scope

1. **Vector-identity checks** (Ex 1.1.1) — the Jacobi identity, the Laplacian
   product rule, and the $\sum_i A_i\vec\nabla B_i$ expansion, verified on
   random vectors and on smooth fields via 4th-order finite differences
   (exact, to rounding, on low-degree polynomial fields).
2. **Potentials** (Ex 1.1.2) — $\vec E=-\vec\nabla\Phi-\frac1c\partial_t\vec A$,
   $\vec B=\vec\nabla\times\vec A$ make Faraday and no-monopole *identities*;
   Coulomb and Ampère–Maxwell become the coupled PDEs for $(\Phi,\vec A)$ —
   both facts checked numerically on concrete potentials.
3. **Charge conservation** (Ex 1.1.3) — $\partial_t\rho+\vec\nabla\cdot\vec J=0$
   for a rigidly moving blob $\rho=ef(\vec r-\vec R(t))$, checked by finite
   differences along a curved trajectory.
4. **Integral theorems** (Ex 1.4.1–1.4.3) — $\oint\vec v\cdot d\vec\ell=2A$ and
   the ellipse area; the gradient and curl forms of Gauss' theorem; the
   $\int da\,\hat n\times\vec\nabla\varphi=\oint d\vec\ell\,\varphi$ form of
   Stokes' theorem — all by quadrature (box faces, disc, hemisphere, contours).
5. **Two-dimensional electrodynamics** (Ex 1.5.1) — the 2-D point-charge field
   $\vec E=2q\hat\rho/\rho$ from $\oint\vec E\cdot\hat n\,d\ell=4\pi q$
   (Table 1.5 normalization), and the numerical demonstration that 2-D Gauss
   and 2-D Stokes are the *same* theorem under $\vec A\mapsto\vec A\times\hat z$.
6. **Electromagnetic units** (Ex A.1.1, A.1.2) — all 30 amount-conversion
   factors of Tables A.1–A.2 recomputed from
   $\alpha=10^2$, $\beta=10^7$, $4\pi\epsilon_0=10^7/c^2$, $\mu_0=4\pi\times10^{-7}$,
   plus the MKS-Gaussian unit sizes and the electron-charge round-trip
   $4.803\times10^{-10}\,\text{statC}\to1.602\times10^{-19}\,$C.

## Operations — `code/intro_perspectives.py`

| call | meaning | exercise |
|------|---------|----------|
| `jacobi_residual(a,b,c)` / `bac_cab_residual(a,b,c)` | $\vec A\times(\vec B\times\vec C)+\text{cyc.}$ ($=0$); BAC-CAB slack | 1.1.1a |
| `laplacian_product_residual(phi,psi,p,h)` | $\nabla^2(\phi\psi)-\phi\nabla^2\psi-\psi\nabla^2\phi-2\vec\nabla\phi\cdot\vec\nabla\psi$ | 1.1.1b |
| `grad_dot_expansion_residual(A,B,p,h)` | $\sum_iA_i\vec\nabla B_i-[\vec\nabla(\vec A\cdot\vec B)-(\vec B\cdot\vec\nabla)\vec A-\vec B\times(\vec\nabla\times\vec A)]$ | 1.1.1c |
| `e_from_potentials` / `b_from_potentials` | $\vec E=-\vec\nabla\Phi-\frac1c\partial_t\vec A$, $\vec B=\vec\nabla\times\vec A$ | 1.1.2 |
| `div_b_residual` / `faraday_residual` | the two identically-satisfied Maxwell equations | 1.1.2 |
| `coulomb_sides` / `ampere_sides` | LHS/RHS of the coupled $(\Phi,\vec A)$ PDEs | 1.1.2 |
| `continuity_residual(f,R,e,p,t,h)` | $\partial_t\rho+\vec\nabla\cdot\vec J$ for the moving blob | 1.1.3 |
| `circulation2d(F,curve,dcurve,n)` / `area_by_circulation(...)` | $\oint\vec v\cdot d\vec\ell$; $A=\frac12\oint(-y\,dx+x\,dy)$ | 1.4.1 |
| `gradient_theorem_sides(phi,box,n,h)` | $\int_Vd^3x\,\vec\nabla\varphi$ vs $\oint_Sda\,\hat n\varphi$ | 1.4.2a |
| `curl_volume_theorem_sides(A,box,n,h)` | $\int_Vd^3x\,\vec\nabla\times\vec A$ vs $\oint_Sda\,\hat n\times\vec A$ | 1.4.2b |
| `stokes_gradient_sides_disc/_hemisphere(phi,grad_phi,...)` | $\int_Sda\,\hat n\times\vec\nabla\varphi$ vs $\oint_Cd\vec\ell\,\varphi$ | 1.4.3 |
| `e2d_point_charge(q,r0)` / `flux2d(F,curve,dcurve,n)` | $\vec E=2q\hat\rho/\rho$; $\oint\vec E\cdot\hat n\,d\ell$ ($=4\pi q$) | 1.5.1a |
| `powerlaw_flux2d(s,r)` | circle flux of $\rho^s\hat\rho$ ($r$-independent only for $s=-1$) | 1.5.1a |
| `cross_z_2d(F)` / `gauss2d_sides` / `stokes2d_sides` | the $\vec A\mapsto\vec A\times\hat z$ map that swaps 2-D Gauss ↔ Stokes | 1.5.1b |
| `amount_factor(name)` / `book_value(name)` | Table A.1–A.2 column-4 factor, recomputed vs quoted | A.1.1 |
| `statcoulomb_in_C()`, `gauss_in_tesla()`, … | physical spot checks of the table | A.1.1 |
| `mksg_charge_unit_in_statC/_in_C()`, `mksg_bfield_unit_in_gauss/_in_tesla()` | MKS-Gaussian unit sizes | A.1.2 |
| `electron_charge_via_mksg()` | $e$: statC → MKS-Gaussian → C round-trip | A.1.2 |

Also exported: `fd_grad/fd_div/fd_curl/fd_lap/fd_dt` (5-point 4th-order
stencils), quadrature helpers (`box_volume_integral`, `box_surface_integral`,
`disc_integral_vec`, `hemisphere_integral_vec`, `line_integral_scalar_dl`),
2-D helpers (`fd_div2d`, `fd_curlz2d`, `disc2d_integral`, `circulation2d_field`),
and the constants `C_GAUSS_CM_S`, `C_NUM`, `ALPHA`, `BETA`, `EPS0_SI`, `MU0_SI`,
`E_STATC`.

## Use
```python
from intro_perspectives import (area_by_circulation, ellipse_curve,
                                e2d_point_charge, flux2d, circle_curve,
                                amount_factor, book_value,
                                electron_charge_via_mksg)

area_by_circulation(*ellipse_curve(3.0, 1.5))     # 14.137...  (= pi*3*1.5)

E = e2d_point_charge(1.0, (0.2, -0.1))            # 2-D field, 2q/rho
flux2d(E, *circle_curve(1.0))                     # 12.566...  (= 4 pi q)

amount_factor('charge'), book_value('charge')     # both 3.3356e-10 (statC -> C)
electron_charge_via_mksg()                        # 1.6022e-19  (C)
```

## Run
```bash
cd code
python3 intro_perspectives.py          # demo: headline numbers per exercise
python3 test_intro_perspectives.py     # tests -> "All N tests passed."
```

## Files
- `notes.md` — compact map of the chapter results the solutions lean on
  (Maxwell tables, continuity, boundary conditions, 2-D electrodynamics,
  units, the §1.8 identity glossary), with printed-page cites
- `refs.md` — page-verified locations (PDF = printed + 23)
- `problems/problems.md` — **all 9 exercises** with faithful statements, full
  stepwise solutions, and the code check for each
- `code/intro_perspectives.py` — the library (numpy; FD stencils + quadrature)
- `code/test_intro_perspectives.py` — the checks (plain python3, no pytest)
