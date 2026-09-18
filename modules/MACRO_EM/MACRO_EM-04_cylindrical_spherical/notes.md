# MACRO_EM-04 — Electrostatics in Cylindrical and Spherical Coordinates (notes)

Compact map of Wilcox & Thron 2e Ch. 4 (printed pp. 135–179; exercises §4.16,
pp. 180–202) — the results the 49 solutions in `problems/problems.md` lean
on. Page numbers are *printed* (PDF = printed + 23, verified; see `refs.md`).
**Gaussian units**: $\nabla^2G=-4\pi\delta^3$ (4.73). Ch. 3's toolbox
(reduced Green functions, image checks, §3.9 summation): `~MACRO_EM-03`;
Griffiths-level separation of variables: `~EM-04`; Bessel/Legendre
background: `~MA-11`/`~MA-14`.

**The chapter's program:** in cylindrical and spherical coordinates the
plane wave $e^{i\vec k\cdot\vec x}$ no longer factors into Laplacian
eigenfunctions — but it *sums* over them. That sum defines the special
functions (Bessel via the generating function, $Y_{\ell m}$ via Schwinger's
$(\vec a\cdot\vec r\,)^\ell$), and completeness of those families turns every
Green-function problem into a 1-D reduced problem solved by the Wronskian
recipe (4.128)–(4.130).

## §4.1 Cylindrical coordinates and Bessel functions (pp. 135–140)
Factor $e^{ik_\perp\rho\cos(\phi-\alpha)}=e^{\frac t2(u-1/u)}$ with
$t=k_\perp\rho$, $u=ie^{i(\phi-\alpha)}$ (4.5–4.6); the expansion
$e^{\frac t2(u-1/u)}=\sum_mu^mJ_m(t)$ (4.7) *defines* $J_m$ and yields the
Taylor series (4.8) (P1), $J_{-m}=(-1)^mJ_m$ (4.10), the integral
representations (4.13)/(4.15)/(4.16) (P1, P4), the sum rules of P2, and the
recursion ladder (4.24)–(4.28) — whose $\frac d{dt}[t^{m+1}J_{m+1}]=t^{m+1}J_m$
member gives P3's $\int_0^a\rho^{m+1}J_m$. Neumann function $N_\nu$ defined
p. 140. Code: `jm_taylor`, `jn_intrep_*`, `sumrule_*`, `int_rho_pow_jm`.

## §4.2 Completeness of Bessel functions (pp. 141–142)
The $\alpha$-average of $e^{i\vec k_\perp\cdot(\vec x-\vec x')_\perp}$
evaluated two ways is the **addition theorem**
$J_0(kD)=\sum_mJ_m(k\rho)J_m(k\rho')e^{im\Delta\phi}$, and integrating over
$k$ gives the completeness relation (4.39)
$\int_0^\infty k\,dk\,J_m(k\rho)J_m(k\rho')=\delta(\rho-\rho')/\rho$ (per
$m$) — P5, tested through Weber's Gaussian-regulated closed form. Code:
`addition_j0_series`, `weber_gauss_*`, `delta2d_gauss_family`.

## §4.3 Zeros and orthogonality (pp. 142–145)
Dirichlet eigenfunctions on $[0,a]$: $J_m(k_{mn}\rho)$ with $k_{mn}=x_{mn}/a$,
$J_m(x_{mn})=0$ (4.46); normalization $\frac{a^2}2J_{m+1}(x_{mn})^2$ (4.58);
Neumann family at zeros $y_{mn}$ of $J_m'$ with norm
$\frac{a^2}2(1-m^2/y^2)J_m(y)^2$ (4.52, worked as P6). Normalized
$\mathcal J_{1m}(k_{mn}\rho)=\frac{\sqrt2}aJ_m/J_{m+1}(x_{mn})$ (4.67);
orthogonality/completeness (4.69)–(4.72) — the discrete twin of (4.39)
(P11 connects them via the zero asymptotics (4.98)). Code: `J1m_fn`,
`bessel_norm_deriv_zero`.

## §4.4 Reduced Green function for the conducting cylinder (pp. 146–148)
Template calculation: expand $\delta^3$ in the transverse complete set,
reduce $\nabla^2G=-4\pi\delta$ to $(k^2-\partial_z^2)g=\delta(z-z')$, solve
with wall conditions → the capped-cylinder kernel (4.78)/(4.79)
$g=\sinh(kz_<)\sinh(k(L-z_>))/(k\sinh kL)$, and the top-plate BVP solution
(4.80)–(4.82). The module's P7–P10 run this machinery on the grounded plane
(recovering Ch. 3's images), the half-plane sheet ($\sin m\phi$ modes), the
disk-driven Neumann capacitor, and the half-infinite capped cylinder. Code:
`g_halfspace`, `G_halfplane_series`, `phi_capacitor_disk`, `G_halfinf_cyl`,
`g_plates_z`.

## §4.5 Cylinder as a boundary value problem (pp. 148–149)
Same answer by separation of variables: $\Phi=P(\rho)Q(\phi)Z(z)$
(4.83–4.87), modes $\mathcal J_{1m}e^{im\phi}\sinh k_{mn}z$, coefficients by
orthogonality (4.90–4.91) $=$ (4.81)–(4.82). Quicker but less general than
§4.4. No exercises attach; P12 is the closest cousin.

## §4.6 Modified Bessel functions; asymptotics (pp. 149–151)
Choosing the oscillatory direction to be $z$ flips the radial equation to
(4.92) with solutions $I_\nu=i^{-\nu}J_\nu(i\cdot)$,
$K_\nu=\frac\pi2i^{\nu+1}H^{(1)}_\nu(i\cdot)$ (4.93–4.94). Asymptotics:
$J,N\sim\sqrt{2/\pi t}\times$oscillation (4.97/4.101), zeros
$x_{mn}\simeq(n+\frac m2-\frac14)\pi$ (4.98) (P11); $I\nearrow e^{t}$,
$K\searrow e^{-t}$; small-argument forms (4.102)–(4.107). P12: grounded
caps + side at $V$ → $I_0$ ratios. Code: `bessel_zero_asymptotic`,
`phi_cyl_side_V`, `solve_laplace_axisym` (FD cross-check).

## §4.7 Free-space Green function via Wronskians (pp. 151–155)
Two expansions of $1/|\vec x-\vec x'|$: oscillatory-$\rho$ (4.108–4.120,
$g_m(z,z')=e^{-k(z_>-z_<)}/2k$) giving
$$\frac1{|\vec x-\vec x'|}=\int_0^\infty dk\sum_me^{im\Delta\phi}J_mJ_m'e^{-k(z_>-z_<)}\quad(4.120),$$
and oscillatory-$z$ (4.121–4.125, $g_m(\rho,\rho')=I_m(k\rho_<)K_m(k\rho_>)$).
The general **Wronskian recipe** (4.128)–(4.130): $g=C\psi_1(x_<)\psi_2(x_>)$,
$C=D/W$; $W[I_m,K_m]=-1/t$, $W[J_\nu,J_{-\nu}]=-2\sin\nu\pi/\pi t$,
$W[J_m,N_m]=2/\pi t$ (P15). Applications: disk variational capacitance
(P13, book's $0.6213a$), Neumann patch (P14), interior/exterior cylinder
$g_m$ (P16), the rectangular-section toroid (P17), and the (4.120) identity
checks (P18). Code: `disk_C_var*`, `phi_patch_neumann`, `g_in_cyl`,
`g_out_cyl`, `g_free_cyl`, `G_cyl_reduced_rho`, `g_toroid`, `coulomb_cylJ`.

## §4.8 Conducting wedge (pp. 155–157)
Line source in the wedge $0<\phi<\beta$: sine expansion (4.132)–(4.133),
radial equation (4.134) with power-law solutions $\rho^{\pm\gamma}$,
$\gamma=n\pi/\beta$ (4.136) → $g_n$ (4.141), wedge-in-cylinder (4.142), open
wedge (4.143); near the tip $G\sim\rho^{\pi/\beta}$ — the §3.8 corner
exponent. P19 sums (4.143) to a closed log (quadrant = Ex. 3.1.3); P20 adds
the second arc; P21 is the full-azimuth cylinder (image closed form,
Ex. 3.3.5b); P22 the 3-D point-charge wedge (fractional-order $I,K$); P23
the concentric-cylinder annulus ($\ln$ modes at $m=0$). Code:
`wedge_series/closed`, `g_wedge_annulus`, `cyl2d_series/image`, `G_wedge3d`,
`g_concentric_2d`.

## §4.9 Schwinger's construction of spherical harmonics (pp. 157–165)
For null $\vec a$ ($\vec a\cdot\vec a=0$), $(\vec a\cdot\vec r\,)^\ell$ is
harmonic; parametrizing $\vec a$ by spinor-like $\xi_\pm$ and expanding in
$\xi_+/\xi_-$ generates the $Y_{\ell m}$ (4.167) with the identity (4.168)
$(\vec a\cdot\vec r)^\ell=\sum_m\xi_+^{\ell+m}\xi_-^{\ell-m}(\cdot)Y_{\ell m}$
— no ODE theory needed. Legendre polynomials via Rodrigues (4.179),
recursions (4.180)–(4.182), explicit $Y_{\ell m}$ (4.185), Tables 4.1–4.3.
P24 (explicit coefficients, $P_\ell(0)$, $P^{(m)}_\ell(0)$), P25 (parity
$(-1)^\ell$), P26 (orthogonality + norm $2/(2\ell+1)$ by induction). Code:
`legendre_explicit`, `legendre0(_seq)`, `dlegendre0`, `ylm`.

## §4.10 Orthogonality of spherical harmonics (p. 165)
$\int Y^*_{\ell m}Y_{\ell'm'}d\Omega=\delta_{\ell\ell'}\delta_{mm'}$ from the
associated-Legendre norms. No exercises; used everywhere from P29 on.

## §4.11 Coulomb expansion; completeness of $Y_{\ell m}$ (pp. 166–169)
Generating function (4.204/4.205) → the Coulomb/Legendre expansion (4.215)
$\frac1{|\vec r-\vec r'|}=\sum_\ell\frac{r_<^\ell}{r_>^{\ell+1}}P_\ell(\cos\gamma)$;
rotations mix only within fixed $\ell$ (4.288/4.289, Vandermonde argument —
P31), giving $P_\ell(\cos\gamma)=\sum_mA_{\ell m}Y_{\ell m}$ (4.219),
completeness (4.220–4.222), the **addition theorem** (4.223), and the fully
resolved Coulomb expansion (4.225). P27/P28 (generating-function and
Rodrigues recursions), P29 (the $\int P_\ell P_\ell$ projector), P30
(hemisphere-bowl variational $C>0.8052a$), P32 (spherical averages of
$1/R$). Code: `integral_PlPl`, `hemi_C_var*`, `ylm_rotation_*`,
`vandermonde_det`, `sphere_int_coulomb*`.

## §4.12 Green function for concentric spheres (pp. 170–172)
Expand in $Y_{\ell m}$: radial equation (4.230)
$-(r^2g_\ell')'+\ell(\ell+1)g_\ell=\delta(r-r')$; two-wall Dirichlet solution
(4.231)-(4.235); limits: interior of a sphere, and $a\to0,b\to\infty$
special cases; image resummations (4.236–4.245) — Kelvin image for Dirichlet,
image + **line image** for the exterior Neumann function (P34). P33
(hemispherical ±V caps: $C=\frac a2\sum[P_{2n}(0)-P_{2n+2}(0)]^2$,
log-divergent), P35 (Neumann shell: $g_0$ unique only up to a constant, §2.8;
surface-delta doubling), P36 (mode series ↔ Poisson kernel), P37 (hemisphere
basin), P38 (capacitance matrix $ab/(b-a)$, $+b$ on the outer shell). Code:
`caps_*`, `gN_ext_sphere_*`, `gN_shell(_g0)`, `sphere_poisson_kernel`,
`sphere_series_from_V`, `hemi_basin_phi`, `concentric_C`.

## §4.13 Conducting sphere in a uniform field; sphere problems (pp. 173–174)
Uniform-field problem redone with the sphere's Green function: radial
solutions $r^\ell,r^{-\ell-1}$ of (4.253), $\Phi=-E_0(r-a^3/r^2)\cos\theta$;
Legendre functions of the second kind $Q_\ell$ (4.255–4.256),
$Q_0=\frac12\ln\frac{1+x}{1-x}$. P39 (field at the center of a split
sphere), P40 (point electrostatics *on* the sphere: $G=Q_0(\cos\gamma)$ —
the book's series prefactor 2 is an erratum, see problems.md), P41/P42
(split-sphere capacitances; $C_{11}+C_{12}=a/2$ exactly), P43 (half-space
$G_D$ as an $\ell+m$-odd harmonic sum). Code: `E_center_split(_fd)`,
`Q0_legendre`, `sphereG_series`, `unequal_caps_*`, `halves_C11_C12`,
`gD_halfspace_sph_*`.

## §4.14 Method of last resort: eigenfunction expansions (pp. 175–179)
For a complete orthonormal eigenbasis $-\nabla^2\psi_n=k_n^2\psi_n$ with the
right BCs: $\delta(\vec x-\vec x')=\sum\psi^*_n(\vec x')\psi_n(\vec x)$
(4.267, P44) and $G_D=4\pi\sum\psi_n\psi^*_n/k_n^2$ (4.268) — always
available, rarely fastest ("last resort": one infinite sum per dimension).
Worked 2-D examples (4.273–4.283); the cylinder eigen-form (4.286–4.287).
P45 (plates: $J_0$ integral × sine sum = the Ch. 3 image ladder), P46
(cylinder reduced $g$ as a Fourier–Bessel resolvent), P47 (1-D triangle
kernel $x_<(L-x_>)/L$), P48 (the sine **sum rule**
$\sum_n\frac{\sin\sin}{k^2+k_n^2}=\frac L2\frac{\sinh(kz_<)\sinh(k(L-z_>))}{k\sinh kL}$,
tying the eigen-form to (4.79)), P49 ($j_\ell(kr)Y_{\ell m}$ modes of the
sphere, eigenvalues $j_\ell(ka)=0$). Code: `sine_delta_action`,
`G_plates_bessel/images`, `G_finite_cyl_79/eigen`, `sumrule_sine(_closed)`,
`g_in_eigen`, `g1d_eigen/closed`, `sph_jn_zeros`, `sph_radial_residual`.

## §4.15 Going Deeper (p. 179)
Pointers: special-function references (Watson for Bessel; the book's
footnote 7 licenses non-integer $\nu\ge-1$ orthogonality — used by P22) and
eigenfunction-expansion literature (Schwinger et al. Ch. 18 does P45's $k$
integral in closed form).

## Numerical craft the module encodes
- **Scaled Bessel products**: every $I,K$ reduced Green function is evaluated
  with `ive`/`kve` and explicit exponent bookkeeping (overflow-free at large
  $ka$), with the exact $m\gg kb$ power-law limit (the 2-D annulus modes) as
  the underflow fallback.
- **Ratio-stable power sums**: $r^\ell$-type two-wall kernels are grouped so
  every base is $\le1$ ($\ell\sim10^3$ safe): `g_wedge_annulus`,
  `g_concentric_2d`, `gN_shell`, `gN_ext_sphere_series`.
- **Conditionally convergent tails**: at $z=z'$ the plates' $k$ integrand
  decays like $J_0(kD)/2k$; split off the free part analytically
  ($\to1/|\vec x-\vec x'|$) and integrate the exponentially decaying rest
  (`G_plates_bessel`) — same trick as the Madelung regularization in
  `~MACRO_EM-03` P24.
- **Stable $P_{2n}(0)$**: the double-factorial form overflows past
  $\ell\sim300$; the recursion $q_n=-q_{n-1}(2n-1)/2n$ doesn't
  (`legendre0_seq`, used by P33/P37/P41/P42).

## Where this goes
- `~MACRO_EM-03` — the images/reduced-$g$/summation toolbox this chapter
  generalizes; its P1/P8 plate problem is re-derived twice here (P45, P48).
- `~MACRO_EM-05` (Ch. 5) — the $Y_{\ell m}$ machinery feeds multipoles and
  dielectric boundary problems.
- Ch. 10 (waveguides/cavities): $J_m$ zeros and $j_\ell$ zeros return as TE/TM
  cutoffs and cavity spectra (P49's eigenvalues).
- `~MA-11`/`~MA-08` (Sturm–Liouville, separation), `~MA-14` (Green
  functions), `~MA-06` (the $\ln$/conformal reading of the 2-D results).
