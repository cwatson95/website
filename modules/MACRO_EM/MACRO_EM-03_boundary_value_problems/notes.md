# MACRO_EM-03 — Boundary Value Problems in Electrostatics (notes)

Compact map of Wilcox & Thron 2e Ch. 3 (printed pp. 87–119; exercises §3.13,
pp. 120–133) — the results the 33 solutions in `problems/problems.md` lean on.
Page numbers are *printed* pages (PDF = printed + 23, verified; see `refs.md`).
**Gaussian units throughout**: a unit charge has $\Phi=1/r$, and every Green
function obeys $\nabla^2G=-4\pi\delta$ (3.14). Griffiths-level treatment of
the same physics (images, separation, relaxation): `~EM-04`. This chapter is
the Green-function upgrade: the *same* boundary problems, solved as kernels.

**The working equations from Ch. 2** (cited constantly): Dirichlet
representation (2.98) $\Phi=\int\rho\,G_D-\frac1{4\pi}\oint\Phi\,\partial_{n'}G_D\,da'$;
Neumann representation (2.103) with $+\frac1{4\pi}\oint G_N\,\partial_{n'}\Phi$
and the surface average $\langle\Phi\rangle_S$; conductor charge
$\sigma=\frac1{4\pi}\partial_n\Phi$ (2.92); Neumann BC
$\partial_nG_N|_S=-4\pi/S$ (2.106), whose source-on-boundary refinement
carries a surface delta (2.115) — verified in this chapter's Ex. 3.2.2.

## §3.1 Conducting plane: images (pp. 87–89)
Free Green function $G_f=1/|\vec x-\vec x'|$ (3.1). Grounded plane $z=0$:
image $-1$ at the mirror point gives
$G_D=1/|\vec x-\vec x'|-1/|\vec x-\vec x''|$ (3.2–3.4); flipping the image
sign gives the Neumann function $G_N$ (3.5) with $\partial_zG_N|_{z=0}=0$.
2-D electrostatics (line charges): $G_f=-2\ln(|\vec x_\perp-\vec x'_\perp|/L)$
(3.9–3.11), with image forms (3.12)–(3.13). Code: `green_plane`,
`green_corner` (P2), `green_perp_2d` (P3), `plate_images` (P1 — two plates,
infinite image ladder).

## §3.2 Reduced Green functions for flat conductors (pp. 90–94)
The chapter's central technique. Fourier-transform the Green equation in the
translation-invariant directions: $\bigl(k^2-\partial_z^2\bigr)g(z,z',k)=\delta(z-z')$
(3.22), with $G=4\pi\int\frac{d^2k}{(2\pi)^2}e^{i\vec k\cdot(\vec x-\vec x')_\perp}g$
(3.23, 3.31). Solve the 1-D ODE with the wall conditions, continuity at
$z'$, and the unit jump in $-\partial_zg$; for the half-space
$g_D=\frac1{2k}\bigl(e^{-k|z-z'|}-e^{-k(z+z')}\bigr)$ (3.30), whose Bessel
inversion (3.32–3.34) lands back on the image answer (3.35–3.36) — the two
methods certify each other. Surface delta function verified both from the
image form (3.37–3.39) and in $k$-space (3.41–3.42); physically,
$\partial_nG_D|_S=4\pi\sigma_{\rm surface}$ (3.40). Free-space warm-up by
3-D Fourier transform: (3.16)–(3.21). Code: `g_reduced_halfspace`
(D/N/Robin), `g_reduced_plates`, `green_halfspace_kspace`,
`green_plates_kspace`, `gf_regulated` (P6–P9).

## §3.3 Conducting sphere by images (pp. 94–98)
Demanding $\Phi=0$ on $r=a$ for a charge $q$ at $\vec r\,'$ forces (3.45–3.46)
$$q'=-\frac{a}{r'}\,q,\qquad
\vec r\,''=\frac{a^2}{r'^2}\,\vec r\,',$$
giving the sphere Green function (3.48) with
$\cos\gamma=\hat n\cdot\hat n'$ (3.49) — valid inside and outside (P10).
Surface gradient (3.50); its integral $\to-4\pi$ as $r'\to a$ (3.52) — the
sphere's surface delta (3.51). Sphere held at $V$: add $Va/r$ (3.53); total
charge $Q=-qa/r'+Va$ (3.54); isolated sphere with given $Q$: (3.55) — the
engine behind P17's forces. Distant-charge limit builds the uniform-field
solution $\Phi=-E_0(r-a^3/r^2)\cos\theta$ (3.56–3.61). Cylindrical twin
(unit line density, image at $a^2/\rho'$, strength $-1$): Ex. 3.3.5 → P14,
closed log form used by P27's Poisson kernel. Code: `sphere_image`,
`green_sphere`, `green_cylinder`, `two_sphere_C` (P13 iterated images),
`rho_star` (P12's image density $-(a/r)^5\rho(a^2/r)$).

## §3.4 Force example: hemispheres in a field (pp. 98–99)
For the grounded sphere in a uniform field, $\sigma=\frac3{4\pi}E_0\cos\theta$
(3.62); the electrostatic pressure integrated over the upper hemisphere gives
$F_z=\frac9{16}E_0^2a^2$ (3.63); with net charge $Q$ added,
$F^{u,\ell}_z=\pm\frac9{16}E_0^2a^2+\frac12E_0Q\pm\frac{Q^2}{8a^2}$
(3.66–3.67), total $E_0Q$, and the hold-together force (3.68). No exercises
attach here; the surface-charge and image machinery is exercised by P16–P17
instead.

## §3.5 Separation of variables: box (pp. 100–101)
$\Phi=X(x)Y(y)Z(z)$ in Laplace's equation (3.69–3.71) forces constant ratios
(3.72): oscillatory in the grounded directions, $\sinh$ in the matched one
(3.73–3.76). Box with data $V(x,y)$ on $z=c$: modes (3.77–3.81), coefficient
projection by sine orthogonality (3.83):
$A_{mn}=\frac{4}{ab\sinh(\gamma_{mn}c)}\int\!\!\int V\sin\alpha_nx\sin\beta_my$
(3.84). The module's 2-D versions: P18 (constant top), P23 (linear top,
$-Ex$), P19/P20 (semi-infinite slot and its Green function), P21 (Neumann
slot), P22 (two plates, closed form). Code: `box2d_phi`, `box2d_phi_Ex`,
`strip_phi`, `green_strip_D/N`, `green_2plates_2d_*`, checked against a
sparse FD Laplace solver (`solve_laplace_rect`) — uniqueness run numerically,
as in `~EM-04` §6.

## §3.6 Eigenfunction expansion of the box Green function (pp. 101–106)
The strategy used all over the book: expand $G$ *and* the delta function in
Laplacian eigenfunctions adapted to the boundary (Fourier sine series,
(3.86)–(3.89)), reducing $\nabla^2G=-4\pi\delta^3$ to the 1-D reduced problem
(3.92): $g_{nm}=\frac{\sinh(\gamma_{nm}z_<)\sinh[\gamma_{nm}(c-z_>)]}{\gamma_{nm}\sinh(\gamma_{nm}c)}$
(3.97), assembling to the full box kernel (3.98). Feeding (3.98) into the
surface term of (2.98) reproduces §3.5's series (3.99–3.101) — kernel and
mode expansion are the same object. The sine-series delta extends periodically
to an *image lattice* (3.102–3.107): alternating-sign unit charges at
$(2na+(-1)^kx',\,2mb+(-1)^\ell y')$ — the box Green function *is* an infinite
image array ("house of mirrors", Fig. 3.10). At the cube center that array is
the NaCl lattice, hence the Madelung constant
$M=\sum'(-1)^{i+j+k}/\sqrt{i^2+j^2+k^2}=-1.747564594$ (3.108), conditionally
convergent — P24 extracts it from (3.98) as the *regularized* self-limit
$a\,[G_D-1/|\vec x-\vec x'|]$, Richardson-extrapolated; Evjen summation as
cross-check. Code: `green_box3d`, `madelung_from_box_green`, `madelung_evjen`.

## §3.7 Polar separation (p. 107)
$\Phi=R(\rho)F(\phi)$ in the polar Laplacian (3.109) gives (3.112–3.113):
$R=a_\nu\rho^\nu+b_\nu\rho^{-\nu}$, $F=\cos/\sin(\nu\phi)$ for $\nu\ne0$;
$R=a_0+b_0\ln\rho$, $F=A_0+B_0\phi$ for $\nu=0$ (3.114–3.115). Full azimuth
forces integer $\nu$ and kills $B_0$ (3.116–3.118). P25 (delta surface data)
is the cleanest instance; its sum is the Poisson kernel (P31). Code:
`cyl_delta_series`, `poisson_kernel`.

## §3.8 Corner problems (pp. 108–109)
Wedge of opening $\beta$, sides at $V$: regularity at the tip and the side
conditions leave $\Phi=V+\sum_ma_m\rho^{m\pi/\beta}\sin(m\pi\phi/\beta)$
(3.119). Near the tip the $m=1$ term rules (3.120), with fields
(3.121–3.122) of magnitude $\frac{\pi|a_1|}{\beta}\rho^{\pi/\beta-1}$ (3.123):
field concentration for reentrant corners ($\beta>\pi$), shielding for
$\beta<\pi$ — the lightning-rod exponent. P26 turns this into the full pie
BVP with end data at $\rho=b$; P2(c) is the two-sided-wedge special case
$\Phi=V(1-2\phi/\beta)$, cf. (3.152). Code: `wedge_coeffs`, `wedge_phi`.

## §3.9 Cylindrical halves at different potentials (pp. 109–110)
Split cylinder ($V_1$ right half, $V_2$ left): the average fixes $a_0$
(3.125); odd symmetry about $\phi=\pi/2$ kills the cosines (3.126–3.127);
orthogonality gives $c'_n\propto(V_2-V_1)/nb^n$, odd $n$ only (3.129) —
series (3.130), summed exactly (Ex. 3.9.3, hint $Z=(\rho/b)e^{i(\phi-\pi/2)}$)
to
$$\Phi=\frac{V_1+V_2}2+\frac{V_1-V_2}\pi
\arctan\frac{2(\rho/b)\cos\phi}{1-(\rho/b)^2}\qquad(3.131),$$
with surface charge $\sigma=\frac{V_1-V_2}{4\pi^2\,b\cos\phi}$ (3.132),
diverging at the gaps $\phi=\pm\pi/2$. P27–P31 orbit this result: Poisson integral
(P27, from P14's Green function), rederivation (P28), the series sum (P29,
including the on-axis collapse to $2\arctan(\rho/b)$), the exterior solution
(P30), the delta-data kernel (P31). Code: `halves_series/closed/axis`,
`halves_exterior_*`, `poisson_integral`, `arctan_series*`.

## §3.10 Variational methods (pp. 111–113)
Thompson's theorem, general form: *among all placements of a fixed total
charge on a fixed open surface, the equipotential (conductor) arrangement
minimizes the field energy* — proof via
$W[\sigma]=\frac12\int\!\!\int\sigma\sigma'/|\vec x-\vec x'|$ (3.136–3.137),
$\frac1{8\pi}\int E^2=W>0$ (3.138–3.140), and $W[\sigma_1+\delta\sigma]=W_1+W'$
with $W'>0$ (3.141–3.143). Consequence (3.144): $C^{-1}[\sigma]=2W[\sigma]/Q^2$
is an upper bound on $1/C$, so every trial density gives a **lower bound on
the capacitance**. No exercise attaches (the book defers examples to Ch. 4's
machinery), so the module carries a notes-level check: for the unit disk,
the uniform trial gives $C_{\rm var}=3\pi R/16\approx0.589R$, strictly below
the exact $C=2R/\pi\approx0.637R$, and the edge density
$\sigma\propto(R^2-\rho^2)^{-1/2}$ saturates the bound. Code: `disk_energy`,
`disk_C_variational` (elliptic-kernel quadrature), `test_variational_disk_bound`.

## §3.11 Conformal mapping (pp. 113–118)
Analytic $f(z)=u+iv$ obeys Cauchy–Riemann (3.145), so $u$ and $v$ are both
harmonic (3.146–3.147) with mutually orthogonal gradients (3.148): $v$-levels
are the field lines of $u$. Mapping theorem (p. 113): through a conformal map,
constant-Dirichlet and homogeneous-Neumann boundary data pull back intact
(constant *Neumann* data does not). Worked examples: $z=e^w$ maps the strip
to the half-plane, giving the two-half-plane wedge potential
$\Phi=V(1-\frac2\pi\phi)$ (3.149–3.151), generalized to opening $\beta$ as
$\Phi=V(1-\frac2\beta\phi)$ (3.152) — P2(c)'s answer; the same result is
re-derived through the half-space Green function (3.154–3.160). Edge of a
parallel-plate capacitor via $z=e^w+w$ (3.161–3.167): fringing field
$E_y\to V/\pi x$ off the edge, constant inside (3.168–3.169). P32 maps P18's
box to a half-annulus by $w=e^{\pi z/b}$; P33 gets the split-cylinder
exterior from the interior by $w=b^2/z$. Deeper refs listed in §3.12
(pp. 118–119): Brown–Churchill for the mapping dictionary (`~MA-06`),
Morse–Feshbach, Smythe. Code: `cauchy_riemann_residual`,
`map_box_to_halfannulus`, `semicircle_phi`, `exterior_from_inversion`.

## Where this goes
- `~EM-04` — the same toolbox one level down (Griffiths): uniqueness proofs,
  the classic plane image, the arctan slot; this module's slot problems
  (P19–P22) are that module's §5 with the Green function made explicit.
- `~MA-08` (PDE separation), `~MA-11` (Sturm–Liouville orthogonality — every
  coefficient projection here), `~MA-14` (Green functions in general),
  `~MA-06` (analytic functions/conformal maps — §3.11's engine).
- Within the trunk: Ch. 4 (MACRO_EM-04) redoes these geometries in cylindrical
  and spherical eigenfunctions (Bessel/Legendre reduced Green functions) and
  supplies the variational examples §3.10 promises; Ch. 5 (MACRO_EM-05) sends
  the sphere images into dielectrics and multipoles.
