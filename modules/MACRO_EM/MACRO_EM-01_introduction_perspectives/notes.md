# MACRO_EM-01 — Introduction & Perspectives (notes)

Compact map of the Ch. 1 results the P1–P9 solutions lean on. Citation key
(full printed→PDF table in `refs.md`): **WT** = Wilcox & Thron 2e; page numbers
are *printed* pages. The book is **Gaussian** throughout — every $4\pi$ and
$1/c$ below is real.

## 1. Maxwell's equations (WT §1.1, Table 1.1, p.2)

| name | Gaussian form | components |
|---|---|---|
| Coulomb | $\vec\nabla\cdot\vec E=4\pi\rho$ | 1 |
| Ampère–Maxwell | $\vec\nabla\times\vec B-\frac1c\frac{\partial\vec E}{\partial t}=\frac{4\pi}{c}\vec J$ | 3 |
| Faraday | $\vec\nabla\times\vec E+\frac1c\frac{\partial\vec B}{\partial t}=0$ | 3 |
| No-monopole | $\vec\nabla\cdot\vec B=0$ | 1 |

with $c\equiv 2.9979245800\times10^{10}\,$cm/s (Table 1.1 header). The two
*sourceless* equations act as constraints; the count of equations is exactly
right for a second-order formulation in a 4-potential $(\Phi,\vec A)$ — that
observation (p.3) **is** Exercise 1.1.2 / P2. Matter feels the fields through
the Lorentz force (WT Eq. 1.1, p.3):
$$\vec F=q\left(\vec E+\frac{\vec v}{c}\times\vec B\right).$$

## 2. Charge conservation is built in (WT pp.3–4)

Divergence of Ampère–Maxwell kills $\vec\nabla\cdot(\vec\nabla\times\vec B)$;
the time derivative of Coulomb supplies $\partial_t(\vec\nabla\cdot\vec E)=4\pi\,\partial_t\rho$.
Eliminating $\vec\nabla\cdot\partial_t\vec E$ between them gives the
**continuity equation** (WT Eq. 1.2, p.4):
$$\frac{\partial\rho}{\partial t}+\vec\nabla\cdot\vec J=0,$$
and integrating it over a volume (divergence theorem, WT Eq. 1.3) says the
charge lost inside $S$ is the charge that flowed out through $S$. P3 verifies
this for the rigidly-translating blob $\rho=ef(\vec r-\vec R(t))$,
$\vec J=e\dot{\vec R}f$ — the finite-width stand-in for a point charge
($f\to\delta^3$, `~MA-15`).

## 3. Macroscopic equations & constitutive relations (WT §1.3, pp.6–8)

Inside matter the atomic-scale fields are replaced by smooth averages
(idealization (c), p.6), and the sourced equations are rewritten with
$\vec D$ and $\vec H$ (Table 1.4, p.7): $\vec\nabla\cdot\vec D=4\pi\rho$,
$\vec\nabla\times\vec H-\frac1c\partial_t\vec D=\frac{4\pi}{c}\vec J$; the
sourceless pair is unchanged. Closure comes from **constitutive relations**
(WT Eq. 1.5, p.7): linear local media have $D_j=\sum_k\epsilon_{jk}E_k$,
$B_j=\sum_k\mu_{jk}H_k$ (isotropic: scalars $\epsilon,\mu$; homogeneous:
constants), nonlocal media convolve in space/time (Eqs. 1.6–1.7), and
conductors obey Ohm, $\vec J=\sigma\vec E$ (Eq. 1.8, p.8). In vacuum
$\vec D=\vec E$, $\vec H=\vec B$ — which is how the P7 (2-D point charge)
solution reads Table 1.5.

## 4. The §1.4 machinery: integral theorems → boundary conditions (pp.8–14)

The two workhorses (p.9), for well-behaved fields:
$$\int_Vd^3x\,\vec\nabla\cdot\vec A=\oint_Sda\,\vec A\cdot\hat n\quad\text{(Gauss, Eq. 1.9)},\qquad
\int_{S'}da\,(\vec\nabla\times\vec A)\cdot\hat n=\oint_Cd\vec\ell\cdot\vec A\quad\text{(Stokes, Eq. 1.10)},$$
with $\hat n$ the outward normal of the closed $S$, and $(\hat n,d\vec\ell)$
right-hand related on the open $S'$. Shrinking the region gives the geometric
meanings (p.9): divergence = flux per unit volume ("sourcedness", Eq. 1.11),
curl·$\hat n$ = circulation per unit area (Eq. 1.12). P5/P6 (Ex 1.4.2/1.4.3)
prove the *gradient*, *curl-volume*, and *surface-gradient* siblings of these
theorems by the constant-vector trick; the numerics integrate both sides.

**Boundary conditions** follow by straddling an interface with infinitesimal
regions (pp.10–13). A **pillbox** (Fig. 1.4) applied to the integral Coulomb /
no-monopole equations — lateral wall contributes nothing by continuity, flat
faces give $(\vec F_2-\vec F_1)\cdot\hat n_{21}\Delta a$ — yields the normal
conditions (Eqs. 1.20–1.21, p.12); a **loop** (Fig. 1.5) applied to
Ampère–Maxwell / Faraday — short sides vanish, the bounded $\partial_t\vec D$,
$\partial_t\vec B$ fluxes die with the loop area — yields the tangential ones,
recast with the triple product (Eq. 1.27) as Eqs. 1.30–1.31 (p.13):
$$(\vec D_2-\vec D_1)\cdot\hat n_{21}=4\pi\sigma,\qquad(\vec B_2-\vec B_1)\cdot\hat n_{21}=0,$$
$$\hat n_{21}\times(\vec H_2-\vec H_1)=\frac{4\pi}{c}\vec K,\qquad\hat n_{21}\times(\vec E_2-\vec E_1)=0.$$
With $\sigma=0$, $\vec K=0$: $E_t,D_n,B_n,H_t$ continuous (Eq. 1.32, p.14).
Limits $\epsilon\to\infty$ / $\epsilon\to0$ give homogeneous Dirichlet /
Neumann conditions (p.14) — the conductor-boundary language of later chapters.

## 5. Two-dimensional electrodynamics (WT §1.5, pp.14–19)

2-D electrodynamics = 3-D electrodynamics with **sources restricted** to
$z$-independent line charges moving $\perp\hat z$ (not a Flatland slice,
pp.14–15). The Lorentz force then forces $E_z=D_z=0$,
$H_x=H_y=B_x=B_y=0$, $J_z=0$ (Eqs. 1.33–1.35), so only
$(E_x,E_y;B_z)$ survive and the no-monopole equation drops out. Table 1.5
(p.15) keeps three equations: $\vec\nabla\cdot\vec D=4\pi\sigma$,
$\vec\nabla\times\vec H-\frac1c\partial_t\vec D=\frac{4\pi}{c}\vec K$ (2
components), $\vec\nabla\times\vec E+\frac1c\partial_t\vec B=0$ (1 component),
with $\sigma,\vec K$ the renamed 2-D densities. The 2-D integral theorems
(p.16) are
$$\int_Sdx\,dy\,(\vec\nabla\cdot\vec A)=\oint_Cd\ell\,\hat n\cdot\vec A\quad\text{(1.37)},\qquad
\int_Sdx\,dy\,(\vec\nabla\times\vec A)\cdot\hat z=\oint_Cd\vec\ell\cdot\vec A\quad\text{(1.38)},$$
i.e. *both* live on a region bounded by one curve — which is why P7b can rotate
one into the other ($\vec A\mapsto\vec A\times\hat z$) and prove them
equivalent. Boundary conditions (Table 1.6, p.18): $(\vec D_2-\vec D_1)\cdot\hat n_{21}=4\pi\xi$,
$H_{z,1}-H_{z,2}=\frac{4\pi}{c}L$, $(\vec E_2-\vec E_1)\cdot\hat\ell=0$, with
line densities $\xi, L$; the $B_n$ condition has no 2-D counterpart. Footnote
10 (p.19): the $4\pi\xi$ normalization treats the 2-D charge as an infinite
3-D line charge; a "geometrical" 2-D world would carry $2\pi\xi$ — P7a states
its answer $E=2q/\rho$ under the book's $4\pi$ convention (Ex 1.5.1 is cited
by that footnote).

## 6. Units: Gaussian ↔ SI (WT Table 1.2 p.2; §1.6.2 p.20; Appendix A pp.859–866)

Gaussian units need no $\epsilon_0,\mu_0$; all EM units are powers of
(g, cm, s), at the cost of explicit $4\pi$'s and $c$'s (pp.859–860). The
Appendix's four-part table gives, per quantity: a **symbol conversion**
(rewrite a Gaussian equation as an SI one, e.g. $q\to q/\sqrt{4\pi\epsilon_0}$,
$\vec E\to\sqrt{4\pi\epsilon_0}\,\vec E$, $\vec B\to\sqrt{4\pi/\mu_0}\,\vec B$)
and an **amount conversion** (Factor & Value: multiply the Gaussian numerical
value to get the SI numerical value). The Values are generated by (p.860)
$$\alpha=10^2\ \text{cm/m},\qquad\beta=10^7\ \text{erg/J},\qquad
4\pi\epsilon_0=\frac{10^7}{c^2},\qquad\mu_0=4\pi\times10^{-7},$$
with $c=299{,}792{,}458$ used as a pure number — P8 (Ex A.1.1) derives the
recipe and the code recomputes all 30 rows. Heaviside–Lorentz (p.862) drops
the $4\pi$'s instead (rationalized Gaussian); natural units add $c=\hbar=1$.
P9 (Ex A.1.2) plays the same game with MKS mechanical units under Gaussian
conventions.

## 7. The §1.8 identity glossary (pp.22–25) — what the solutions actually use

Notation: $\delta_{ij}$, $\epsilon_{ijk}$ (p.23), summation convention written
out. Key entries, cited constantly in `problems/problems.md`:

- **BAC-CAB** $\vec A\times(\vec B\times\vec C)=\vec B(\vec A\cdot\vec C)-\vec C(\vec A\cdot\vec B)$;
  **triple product** $\vec A\cdot(\vec B\times\vec C)=\vec B\cdot(\vec C\times\vec A)=\vec C\cdot(\vec A\times\vec B)$;
  **Jacobi** (the P1a target) — all p.23.
- **ε–δ contraction** $\sum_i\epsilon_{ijk}\epsilon_{imn}=\delta_{jm}\delta_{kn}-\delta_{jn}\delta_{km}$ (p.24)
  — the engine behind every index proof below.
- **First-order identities** (p.24): $\vec\nabla\cdot(\phi\vec A)$,
  $\vec\nabla\times(\phi\vec A)=\vec\nabla\phi\times\vec A+\phi\vec\nabla\times\vec A$,
  $\vec\nabla(\vec A\cdot\vec B)$, $\vec\nabla\cdot(\vec A\times\vec B)=\vec B\cdot(\vec\nabla\times\vec A)-\vec A\cdot(\vec\nabla\times\vec B)$,
  $\vec\nabla\times(\vec A\times\vec B)$ — P5/P6/P7b run on these.
- **Second-order identities** (p.24): $\vec\nabla\times\vec\nabla\phi=0$,
  $\vec\nabla\cdot(\vec\nabla\times\vec A)=0$ (the two that make P2's Maxwell
  equations identities),
  $\vec\nabla\times(\vec\nabla\times\vec A)=\vec\nabla(\vec\nabla\cdot\vec A)-\nabla^2\vec A$
  (the simplification step of P2's Ampère PDE), and $\nabla^2(\phi\psi)$ (the
  P1b target).
- **Integral identities** (p.25): Gauss, Stokes, Green's first & second — P5/P6
  generate three more members of this family.
- Vector operators in rectangular/cylindrical/spherical coordinates
  (pp.25–26) and the coordinate figures (pp.27–28).

## Where this goes

- `~MA-02` owns the general vector-calculus theory; this module's P4–P6 are
  the exercise-level proofs of its integral theorems.
- `~EM-13` states the same Maxwell equations in SI; the unit dictionary of §6
  (P8/P9) is the translation layer.
- MACRO_EM-02 (electrostatics) starts from Coulomb + the P2 potentials;
  the pillbox/loop boundary conditions of §4 return in every boundary-value
  module (MACRO_EM-03/04); 2-D electrodynamics (§5) returns as line charges
  and conformal methods (MACRO_EM-03/04) and in waveguide cross-sections
  (MACRO_EM-10).
