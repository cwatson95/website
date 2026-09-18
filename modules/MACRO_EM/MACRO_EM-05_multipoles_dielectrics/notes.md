# MACRO_EM-05 — Multipoles, Macroscopic Media, Dielectrics (notes)

Compact map of Wilcox & Thron 2e Ch. 5 (printed pp. 203–241; exercises §5.13,
pp. 242–266) — the results the 49 solutions in `problems/problems.md` lean on.
Page numbers are *printed* (PDF = printed + 23, verified; see `refs.md`).
**Gaussian units**: $\Phi=q/r$, $\vec D=\vec E+4\pi\vec P$, and the dielectric
Green equation is $\vec\nabla\cdot[\epsilon(\vec x)\vec\nabla G]=-4\pi\delta$
(5.72). Griffiths-level treatment of the same physics: `~EM-05` (multipoles,
polarization), `~EM-07`-adjacent energy/force arguments; this chapter is the
Green-function/systematics upgrade.

## §5.1 Cartesian and spherical multipole expansions (pp. 203–207)
Taylor expansion of $1/|\vec x-\vec x'|$ (5.2)–(5.9) organizes the far
potential (5.12):
$$\Phi=\frac qr+\frac{\vec x\cdot\vec p}{r^3}
+\frac12\sum_{ij}Q_{ij}\frac{x_ix_j}{r^5}+\dots,\qquad
Q_{ij}=\int(3x_i'x_j'-\delta_{ij}r'^2)\rho\,d^3x',$$
$Q$ symmetric-traceless (5.13): 1, 3, 5 independent components
($\to2\ell+1$). Ideal fields (5.14)–(5.16): $r^{-2},r^{-3},r^{-4}$; prolate
vs oblate $Q_{33}\gtrless0$ (Fig. 5.3). Spherical version via the Coulomb
expansion (5.17): moments $\rho_{\ell m}$ (5.19) and
$\Phi=\sum\rho_{\ell m}\sqrt{4\pi/(2\ell+1)}\,Y_{\ell m}/r^{\ell+1}$ (5.20).
Code: `moments_point_charges`, `moments_translate` (P2's translation law),
`octopole_R` (P4: $R_{ijk}$, 7 components), `rho_lm`. P1–P6; the
lowest nonvanishing moment is origin-independent (P1/P2).

## §5.2 Multipole energy expansions (pp. 207–211)
Charge–multipole energy (5.21)–(5.25):
$W=q_1q/r-\vec p\cdot\vec E^{(0)}+\frac16\sum Q_{ij}\partial E_j^{(0)}/\partial x_i+\dots$;
pair energies: dipole–charge (5.26), dipole–dipole (5.27),
dipole–quadrupole (5.28) with the $\pm$ orientation subtlety (5.29). For the
axisymmetric quadrupole this collapses to $W=\frac14Q_{33}\partial_z^2\Phi$
(P7; force $\frac14Q_{33}\partial_z^2\vec E$). Quadrupole–quadrupole (P8):
$+\frac9{16}Q_{33}^{(1)}Q_{33}^{(2)}/r^5$ broadside (book's $-$ sign is an
erratum — microscopic check), $+\frac32$ collinear. Separable configurations:
spherical harvest (5.30)–(5.37), $W=\sum(\rho_<)^*_{\ell m}(\rho_>)_{\ell m}$;
dipole components vs $(\rho)_{1m}$ (5.38)–(5.39). P9 sums the geometric
$\ell$-series for the charge-and-grounded-sphere image system. Code:
`quad_energy_in_potential`, `W_quad_quad_*`, `sphere_image_W_*`.

## §5.3 External fields and forces on multipole distributions (pp. 211–214)
$\vec F=\int\rho\vec E^{(0)}$ (5.41) Taylor-expanded (5.42)–(5.51) with the
$\vec\nabla(\vec a\cdot\vec b)$ identity (5.43) and $\nabla\cdot\vec E^{(0)}=0$
insertions (5.49) gives the gradient form (5.52)
$\vec F=q\vec E^{(0)}+\vec\nabla(\vec p\cdot\vec E^{(0)})
+\vec\nabla\frac16\sum Q_{ij}\partial_jE_i^{(0)}+\dots$ and the alternate
(5.53) $(\vec p\cdot\vec\nabla)\vec E^{(0)}+\frac16Q_{ij}\partial_i\partial_j\vec E^{(0)}$
— P10 spells out the assumptions (curl- **and** divergence-free external
field across the body) and adds the torque
$N_i=(\vec p\times\vec E^{(0)})_i+\frac13\epsilon_{ijk}Q_{jm}\partial_mE_k^{(0)}$.
Code: `force_multipole`, `torque_multipole` vs exact sums.

## §5.4 Electric polarization and the displacement field (pp. 214–217)
Summing (5.53) over atoms: bulk force $\int(\vec P\cdot\vec\nabla)\vec E^{(0)}$
(5.55) with $\vec P=n\vec p$ (5.56); integration by parts (5.57) identifies
$\rho^d_{\rm eff}=-\vec\nabla\cdot\vec P$ (5.58), $\sigma^d_{\rm eff}=\vec P\cdot\hat n$
(5.59); quadrupole-density generalization (5.60)/P11 (adds a surface dipole
layer $(\mathcal P^Q)_j=\frac16\hat n_iq_{ij}$). Bound charge closes Maxwell:
$\vec\nabla\cdot\vec D=4\pi\rho_f$ with $\vec D=\vec E+4\pi\vec P$
(5.61)–(5.65); linear media $\vec P=\chi\vec E$ (5.66),
$\epsilon=1+4\pi\chi$ (5.67), $\vec\nabla\cdot\vec E=4\pi\rho_f/\epsilon$
(5.70) — P12's $\rho_b=\frac{1-\epsilon}\epsilon\rho_f$ and the
$\frac{\epsilon-1}\epsilon Q_f$ surface total. Worked BVPs: cylinder in a
uniform field (P13: $E_{\rm in}=\frac2{\epsilon+1}E_0$), polarized-body
potential as surface+volume bound charge (P14), the Lorentz cavity field
$\frac{4\pi}3\vec P$ (sphere P14b, cube P15ab) and Clausius–Mossotti
$\alpha=\frac1N\chi/(1+\frac{4\pi}3\chi)$ (P15c). Code: `cylinder_in_field_phi`,
`polarized_sphere_surface_E`, `solid_angle_square_from_center`,
`clausius_mossotti_alpha`, `quad_density_check`.

## §5.5 Green functions in the presence of linear dielectrics (pp. 217–218)
$\vec\nabla\cdot[\epsilon\vec\nabla\Phi]=-4\pi\rho_f$ (5.71) and the Green
function (5.72); Green's-identity derivation (5.73)–(5.75) gives the
representation (5.77)
$\Phi=\int G_D\rho-\frac1{4\pi}\oint\epsilon\,\Phi\,\partial_{n'}G_D$ — the
Dirichlet surface is a **conductor** surface, not a dielectric one;
$G_D$ symmetric (5.78). No exercises attach; every §5.6–§5.7 problem runs on
this machinery.

## §5.6 Green function for the dielectric slab (pp. 218–222)
Transverse Fourier transform (5.81)–(5.85) with matching conditions:
$g$ continuous ($E_\parallel$), $\epsilon\,\partial_zg$ continuous ($D_n$)
(5.86)–(5.87). Half-space solution (5.88)–(5.104); Bessel inversion
(5.105)–(5.107): images
$$G_{z>0}=\frac1{|\vec x-\vec x'|}-\frac{\epsilon-1}{\epsilon+1}\frac1{|\vec x-\vec x''|},
\qquad G_{z<0}=\frac1\epsilon\frac{2\epsilon}{\epsilon+1}\frac1{|\vec x-\vec x'|},$$
bound surface charge (5.108)–(5.111) with its $z'\to0$ surface-delta limit
(5.112)–(5.113); limits $\epsilon\to\infty$ (conductor), $\epsilon\to0$
(Neumann), $\epsilon\to1$ (free). Exercises: the dielectric corner and its
image-composition caveat (P16 — exact only for factorizable
$\epsilon(x,y)=e(x)e(y)$; the module proves no finite image set solves the
uniform corner), conductor+slab reduced kernel (P17), the
$\epsilon\to1/\epsilon$ swap rule $G_{\rm swap}=\frac1\epsilon G(1/\epsilon)$
(P18, reused by P26/P32), the 1-D two-wall slab kernel (P19: dielectric
thickness counts as $d/\epsilon$), the two-half-space image pair
$q'=q\frac{\epsilon_2-\epsilon_1}{\epsilon_2+\epsilon_1}$,
$q''=\frac{2q\epsilon_1}{\epsilon_1+\epsilon_2}$ (P20), and the finite slab's
6-coefficient count (P21). Code: `g_slab_conductor_book/solve`,
`g_slab_swapped_solve`, `oneD_G_dielectric(_fd)`, `two_halfspace_phi`,
`slab_finite_solve`, `corner_dielectric_G(_region)`.

## §5.7 Green function for the dielectric sphere (pp. 223–226)
Spherical harmonics ansatz (5.116); radial problems (5.117)–(5.118) with
conditions (5.119)–(5.120); coefficients (5.121)–(5.135); assembled kernels
(5.136)–(5.138), Legendre form (5.139)–(5.141):
$$G_{r<a}=\sum_\ell\frac{2\ell+1}{\ell(1+\epsilon)+1}\frac{r^\ell}{r'^{\ell+1}}P_\ell,\qquad
G_{r>a}=\frac1{|\vec x-\vec x'|}-\sum_{\ell\ge1}
\frac{(\epsilon-1)\ell}{\ell(1+\epsilon)+1}\frac{a^{2\ell+1}}{(rr')^{\ell+1}}P_\ell .$$
No image-charge reading except $\epsilon\to\infty$ (→(4.240) minus the
$\ell=0$ term). Far-source limits: induced dipole
$\vec p=\frac{\epsilon-1}{\epsilon+2}a^3\vec E$ (5.142)–(5.144); interior
screening $\vec E_{\rm in}=\frac3{\epsilon+2}\vec E$ (5.145)–(5.146).
Exercise fan-out: 2-D dielectric cylinder modes (P22: image weight
$\beta=\frac{1-\epsilon}{1+\epsilon}$ per $m$; $\epsilon$-blind $m=0$),
3-D cylinder via $I_m/K_m$ (P23), uniform-field sphere by distant charge
(P24), source-inside kernel + $\frac{\epsilon-1}\epsilon$ surface charge
(P25), bubble $=\frac1\epsilon\times$sphere$(1/\epsilon)$ (P26), dipole near
sphere (P27), sphere-in-grounded-shell counting (P28), charged plane =
exactly uniform field (P29: all $\ell\ge2$ plane moments vanish), ring source
via $P_{2n}(0)$ (P30), dielectric-filled split-sphere capacitances (P31),
conducting cylinder with dielectric core (P32), induced quadrupole
$Q_{ij}=\frac{2a^5(\epsilon-1)}{3+2\epsilon}(-\partial E'_j/\partial x'_i)$
(P33 — book prints $a^3$, dimensional erratum). Code: `sphere_G_in/out`,
`sphere_source_inside_coeffs`, `bubble_G_out`, `gm_cyl2d`, `cyl3d_gm_solve`,
`ring_sphere_phi_in`, `split_sphere_C`, `coaxial_cyl_solve`,
`induced_quadrupole_sphere`.

## §5.8 Field energy and dielectrics (pp. 226–229)
From work on charge carriers: $\delta W=\int\delta\rho\,\Phi$ (5.155)
$\to\frac1{4\pi}\int\vec E\cdot\delta\vec D$ (5.157)–(5.159) — always true;
integrable to $W=\frac1{8\pi}\int\vec E\cdot\vec D$ (5.164) only for
symmetric linear response $\epsilon_{ij}=\epsilon_{ji}$ (5.160)–(5.163);
excludes $\epsilon(E^2)$ (→§5.10). Green-function forms:
$W=\frac12\int\rho\Phi=\frac12\int\!\!\int\rho G_D\rho$ (5.165)–(5.167).
Introducing a dielectric at fixed charges (5.169)–(5.172):
$$\Delta W=\frac12\int\!\!\int\rho\,[G_D-G_D^0]\,\rho
=\frac1{8\pi}\int(\epsilon_0-\epsilon)\vec E\cdot\vec E_0
\;\;\overset{\epsilon_0=1}{=}\;-\frac12\int\vec P\cdot\vec E_0\ \ (5.173).$$
P34: permanent-$\vec P$ identities $\int\vec E\cdot\vec D=0$ and
$W^{\rm int}=-\frac12\int\vec P\cdot\vec E=\frac1{8\pi}\int E^2$
(uniformly polarized sphere as the worked instance: $\vec E_{\rm in}$
anti-parallel to $\vec D_{\rm in}$). Code: `polarized_sphere_ED_integral`,
`polarized_sphere_Wint`, `slab_deltaW`, `sphere_charge_deltaW_series`.

## §5.9 Bulk forces on dielectrics: theory (pp. 230–232)
Fixed charge: $\vec F=-\partial W/\partial\vec x|_Q$ (5.174); fixed voltage
(idealized batteries): the battery ledger (5.176)–(5.178) flips the sign,
$\vec F=+\partial W/\partial\vec x|_V$ (5.179) — same instantaneous force
(P39/P43 exercise both). Where the force acts: $\vec F_{\rm bulk}
=\oint(\vec P\cdot\hat n)\vec E^{(0)}da$ (5.180) when $\vec\nabla\cdot\vec P=0$
(no interior free charge, (5.181)); the self-field drops by Newton's third
law, leaving the **average field rule** (5.183)–(5.185):
force/area $=\sigma_{\rm eff}\,\frac12(\vec E_1+\vec E_2)$ — P35's
$\frac1{8\pi}(E_{2n}^2-E_{1n}^2)=2\pi\sigma_b^2\frac{\epsilon+1}{\epsilon-1}$
family. Applications: half-space three ways (P36), thin rods broadside/
lengthwise ($\alpha_\perp$ vs $\alpha_\parallel$, ratio $\frac{\epsilon+1}2$;
P37–P38), partially inserted capacitor slab (P39), the exact slab force
integral (P40), its weak-dielectric three-image form (P41), the
$\epsilon\to\infty$ second-plate limit with
$\sigma=-\frac1{2\pi}\int k\,dk\frac{\sinh kz'}{\sinh kd}J_0(k\rho)$ and
$F=-\int k[\frac{\sinh kz'}{\sinh kd}]^2dk$ (P42), the layered capacitor at
fixed $V$ vs disconnected (P43), and the line-charge/cylinder force with the
exact log resummation $\Delta W=-\beta\ln(1-a^2/\rho'^2)$ (P44). Code:
`halfspace_*`, `rod_force_*`, `capacitor_*`, `slab_force_integral/weak`,
`plate_*`, `line_cylinder_*`.

## §5.10 Nonlinear dielectric example: leading logarithm model (pp. 232–235)
QCD-inspired phenomenology (Adler–Piran): $\vec D=\epsilon\vec E$ with
$\epsilon=2\alpha\ln(E^2/K^2)$, $\vec D=0$ where $E^2<K^2$ — a dynamical
confinement boundary with $\vec D\cdot\hat n=0$ (homogeneous Neumann) on the
flux-tube wall (Fig. 5.16). The correct energy functional is
$W=\frac1{4\pi}\int[\frac12\vec E\cdot\vec D+\alpha E^2]$ (5.190)–(5.194):
its first variation is $\frac1{4\pi}\int\vec E\cdot\delta\vec D$ exactly.
Bound (5.195)–(5.197): $W>\frac K{8\pi}\int|\vec D|\ge\frac12K|Q|(R-2r)$ —
energy linear in separation ⇒ confinement. P45 proves the extremum
($\delta W^{(1)}=0$ at fixed free charge) and its stability
($\delta W^{(2)}>0$ for $E^2>K^2$). Code: `leading_log_*`.

## §5.11 Bulk forces on dielectrics: examples (pp. 235–240)
Sphere–charge force three ways: (i) energy difference (5.198)–(5.201),
$\Delta W=-\frac{\epsilon-1}{2r_0}\sum_{\ell\ge1}\frac{\ell}{\ell(1+\epsilon)+1}(a/r_0)^{2\ell+1}$,
leading (5.202) $F_r=-\frac{\epsilon-1}{\epsilon+2}\frac{2a^3}{r_0^5}$
(attractive; contrast the grounded sphere's $r^{-3}$ — no $\ell=0$ image);
(ii) surface-stress integral (5.203)–(5.216); (iii) external-field form
(5.217)–(5.221) — all agree. Fluid-rise capacitor (5.222)–(5.229):
$\epsilon-1\approx\frac{2\pi}{V^2}(b^2-a^2)\rho g\,\Delta z\ln(b/a)$ — the
energy method vs the hopeless local-force route. Exercises: bubble–charge
repulsion (P46), (5.173)-route rederivation of (5.202) (P47), charge inside
a droplet — harmonic trap toward the center (P48), sphere–dipole $d^{-7}$
force (P49). Code: `bubble_charge_*`, `sphere_deltaW_from_P`,
`droplet_inside_force_series`, `sphere_dipole_force`.

## §5.12 Going Deeper (p. 241)
Dielectric-materials reading list: Gallot-Lavallée; Kittel Ch. 16 (the
microscopic $\alpha$); Landau–Pitaevskii–Lifshitz *ECM* Ch. II (the
thermodynamic force treatment); Martínez-Vega; Scaife; von Hippel.

## Errata caught by the module's checks
- **Ex. 5.2.2**: printed $W_{QQ}=-\frac9{16}Q^{(1)}_{33}Q^{(2)}_{33}/r^5$;
  microscopic sums give $+\frac9{16}$ (P8).
- **Ex. 5.7.12**: printed $Q_{ij}\propto a^3$; dimensions and the
  bound-charge quadrature require $a^5$ (P33).
- Fig. 5.24's caption says "magnetic field" (electric intended); Fig. 5.32's
  caption says "Exercise 5.9.10" (belongs to 5.7.1); Ex. 5.9.9's text cites
  "Figure 5.39" (the drawing is Fig. 5.43).

## Where this goes
- `~EM-05`/`~EM-07` — Griffiths-level multipoles, polarization, and D-field;
  this module adds the systematic expansions, dielectric Green functions,
  and the fixed-$Q$/fixed-$V$ force calculus.
- Within the trunk: builds directly on `~MACRO_EM-04` (Bessel/Legendre
  reduced Green functions — Exs. 4.2.1, 4.9.1, 4.13.4 are inputs here) and
  `~MACRO_EM-03` (images, reduced $g$, uniqueness); feeds `~MACRO_EM-06`
  (magnetization mirrors §5.4's polarization, $\vec H$ mirrors $\vec D$) and
  `~MACRO_EM-09` ($\epsilon(\omega)$: the frequency dependence promised in
  §5.4).
- `~MA-11`/`~MA-14` — orthogonal expansions and Green-function formalism
  behind every kernel here.
