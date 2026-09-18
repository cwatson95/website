# MACRO_EM-02 — Introduction to Electrostatics (notes)

Compact map of the Wilcox & Thron Ch. 2 results the problem solutions lean on.
**Gaussian units throughout** (the book's convention): $\vec E=-\vec\nabla\Phi$,
$\vec\nabla\!\cdot\!\vec E=4\pi\rho$, $\Phi=q/r$ for a point charge. Citation key:
**WT** = Wilcox & Thron 2e; page numbers are *printed* pages (PDF = printed + 23);
equation numbers are the book's. Full page table in `refs.md`.

## 1. Field, superposition, potential (§2.1, §2.4, pp.29–30, 41–42)

- Coulomb: $\vec E_{q'}(\vec x)=q'(\vec x-\vec x')/|\vec x-\vec x'|^3$ (2.2); a
  continuous distribution superposes, $\vec E=\int d^3x'\,\rho(\vec x')(\vec x-\vec x')/|\vec x-\vec x'|^3$ (2.5).
- $-\vec\nabla|\vec x-\vec x'|^{-1}=(\vec x-\vec x')/|\vec x-\vec x'|^3$ (2.48)
  pulls the gradient out: $\Phi(\vec x)=\int d^3x'\,\rho(\vec x')/|\vec x-\vec x'|$ (2.51),
  $\vec E=-\vec\nabla\Phi$ (2.52), $\vec\nabla\times\vec E=0$ (2.54).
- **Poisson**: $\nabla^2\Phi=-4\pi\rho$ (2.53); applied to a point source,
  $\nabla^2|\vec x-\vec x'|^{-1}=-4\pi\delta(\vec x-\vec x')$ (2.55).

## 2. Delta functions (§2.2–2.3, pp.31–38)

- $\delta(x)=\lim_{\epsilon\to0^+}\epsilon^{-1}f(x/\epsilon)$ for any nonnegative
  unit-integral $f$ (2.9)–(2.10); sampling $\int f\delta=f(0)$ (2.8); scaling
  $\delta(ax)=\delta(x)/|a|$ (2.13); composition
  $\delta(f(x))=\sum_i\delta(x-x_i)/|f'(x_i)|$ over simple roots (2.16).
- **Curvilinear coordinates** $u,v,w$: $\delta(\vec x-\vec x')=\delta(u-u')\delta(v-v')\delta(w-w')/|\det\partial(x,y,z)/\partial(u,v,w)|$
  (2.25); for *orthogonal* systems the Jacobian is the product of scale factors,
  $|\det|=UVW$ with $U=|\partial\vec x/\partial u|$ etc. (2.28)–(2.29).
- Fourier representation $\delta^{(n)}(\vec x)=(2\pi)^{-n}\int d^nk\,e^{i\vec k\cdot\vec x}$ (2.34).
- Line/surface deltas embed lower-dimensional charge in 3-D: $\lambda(z)\delta(x)\delta(y)$,
  $\sigma(x,y)\delta(z)$; recovered by integrating $\delta^{(3)}$ along the line/surface
  (2.35)–(2.36); directed ("membrane") versions (2.37)–(2.39) give $\pm1/0$ when a
  path crosses/misses a surface — used again in §6.5/§7.8.

## 3. Gauss law and solid angles (§2.4, pp.38–41)

- $da\,\hat n\cdot(\vec x-\vec x_j)/|\vec x-\vec x_j|^3=d\Omega_j$, the solid angle
  of the patch seen from the charge (2.42). Net solid angle: $4\pi$ from inside,
  $0$ from outside — hence $\oint_S da\,\hat n\cdot\vec E=4\pi\sum_{\rm in}q_j$ (2.44),
  continuous version (2.45), differential form $\vec\nabla\cdot\vec E=4\pi\rho$ (2.47).
- The same construction in **2-D** gives $\oint d\ell\,\hat n\cdot\vec E=2\pi q_{\rm enc}$
  and $\nabla^2\ln(|\vec x-\vec x'|/K)=2\pi\delta^{(2)}$ (Exercise 2.4.1) — the 2-D
  Coulomb "$4\pi$" is $2\pi$, which is where the extra 2 of the 3-D line-charge
  potential $-2\lambda\ln(\rho/K)$ comes from.

## 4. Cavendish test of the inverse square (§2.5, pp.42–45)

- Hypothesize $F\propto|\vec x-\vec x'|^{-(2+\epsilon)}$ (2.56); a potential still
  exists: $\Phi=(1+\epsilon)^{-1}\int d^3x'\rho/|\vec x-\vec x'|^{1+\epsilon}$ (2.59).
- Uniform shell radius $a$, charge $q_a$, field point $r$ (both signs of $r-a$):
  $$\Phi_{\rm shell}(r)=\frac{q_a}{1-\epsilon^2}\,\frac{(r+a)^{1-\epsilon}-|r-a|^{1-\epsilon}}{2ar},$$
  specializing to $\Phi_{\rm out}$ (2.62) and $\Phi_{\rm in}$ (2.63).
- Two concentric conducting shells wired together force $\Phi(a)=\Phi(b)$ (2.64);
  to first order in $\epsilon$ the inner-shell charge is (2.65)
  $q_a\approx\dfrac{q_b\,\epsilon}{2(a-b)}\bigl[b\ln\frac{b-a}{a+b}+a\ln\frac{4b^2}{b^2-a^2}\bigr]$
  — zero iff $\epsilon=0$. Cavendish (1772): exponent $=2\pm.02$; Williams–Faller–Hill
  (1971): $\epsilon=(2.7\pm3.1)\times10^{-16}$, i.e. a photon-mass limit
  (Yukawa $R=\hbar/m_\gamma c$, Exercise 2.5.2).

## 5. Surface charge and dipole layers (§2.6, pp.45–49)

- Jumps across a charged sheet: $(\vec E_2-\vec E_1)\cdot\hat n_{21}=4\pi\sigma$ (2.68),
  tangential $\vec E$ continuous (2.67). Infinitesimal-disk split: the disk alone
  contributes $\pm2\pi\sigma$ on the two sides (2.74)–(2.75), the remainder is continuous.
- **Dipole layer**: $D=\sigma d$ finite as $d\to0$, $\sigma\to\infty$ (2.76). Potential
  $$\Phi(\vec x)=\int_S da'\,D(\vec x')\,\hat n_{21}\cdot\vec\nabla'\frac1{|\vec x-\vec x'|}
    = -\int_S D\,d\Omega' \quad(2.77\text{–}2.78),$$
  the solid-angle form making $\Phi$ constant for closed layers. Potential jump
  $\Delta\Phi=4\pi D$ crossing the layer (2.80)–(2.81); a *uniform* closed dipole
  shell therefore has $\vec E=0$ everywhere (Exercise 2.6.4c).

## 6. Boundary conditions and uniqueness (§2.7, pp.49–51)

- **Green's first identity** $\int_V(\phi\nabla^2\psi+\vec\nabla\phi\cdot\vec\nabla\psi)\,d^3x=\oint_S\phi\,\partial_n\psi\,da$ (2.83).
- Set $\phi=\psi=U\equiv\Phi_1-\Phi_2$: Dirichlet data $\Phi|_S$ (2.84), Neumann data
  $\partial_n\Phi|_S$ (2.88), or mixed (2.89) each force $\int|\vec\nabla U|^2=0$, so
  $\vec E$ is unique (Φ unique up to a constant in the pure Neumann case).
- Conductors: equipotential surfaces with $\sigma=\frac1{4\pi}\partial_n\Phi|_S$ (2.92)
  ($\hat n$ out of the *vacuum* volume). Homogeneous Neumann objects ($E_n=0$) are
  realized by dipole layers, not charges.

## 7. Dirichlet and Neumann Green functions (§2.8, pp.51–58)

- Definition: $\nabla^2G(\vec x,\vec x')=-4\pi\delta(\vec x-\vec x')$ (2.93) plus
  boundary data. Green's second identity (2.95) with $\psi=G,\ \phi=\Phi$ gives the
  master representation (2.97).
- **Dirichlet**: $G_D|_{S}=0$ (2.100); then
  $\Phi(\vec x)=\int d^3x'\,G_D(\vec x',\vec x)\rho(\vec x')-\frac1{4\pi}\oint da'\,\Phi(\vec x')\,\partial_{n'}G_D(\vec x',\vec x)$ (2.98).
- **Neumann**: $\partial_nG_N|_S=0$ is impossible since $\oint\partial_nG_N\,da=-4\pi$
  (2.102); the consistent choice is $\partial_nG_N|_S=-4\pi/S$ (2.106), giving
  $\Phi(\vec x)=\int G_N(\vec x',\vec x)\rho\,d^3x'+\frac1{4\pi}\oint da'\,G_N\,\partial_{n'}\Phi+\langle\Phi\rangle_S$ (2.103)–(2.104).
- **Symmetry**: $G_D(\vec x,\vec x')=G_D(\vec x',\vec x)$ always (2.107)–(2.108);
  any interior $G_N$ can be symmetrized by subtracting a function of the source
  point, $G_N^{\rm symm}(\vec x',\vec x'')=G_N(\vec x',\vec x'')-\langle G_N(\vec x,\vec x'')\rangle_{S(\vec x)}$ (2.111).
  Physical reading (p.62): $G$ = interaction energy of two unit charges, so symmetry
  is charge-exchange symmetry.
- Source-on-boundary limits produce surface deltas:
  $\lim_{\vec x\to S}\partial_nG_N=-4\pi/S+4\pi\delta^{(S)}$ (2.115) and
  $\lim_{\vec x'\to S}\partial_nG_D=-4\pi\delta^{(S)}$ (2.123).

## 8. One-dimensional Green functions (§2.9, pp.58–60)

1-D conventions: $\partial_x^2G=-\delta(x-x')$ (2.124), $\Phi''=-\lambda$ (2.126), and
the representation (2.127) mirrors (2.98) with endpoint evaluations replacing $\oint$.
Construction recipe: linear branches (2.128), continuity at $x'$ (2.129), slope jump
$\partial_xG|^{x'^+}_{x'^-}=-1$ (2.131), plus the boundary data. Results:

- Dirichlet box $[0,L]$: $G_D(x,x')=x_<\,(1-x_>/L)$ (2.136).
- Neumann box: endpoint fields $\partial_xG_N(0)=\tfrac12$, $\partial_xG_N(L)=-\tfrac12$
  (2.137) (the 1-D analog of $-4\pi/S$); representation (2.138); symmetrized
  $G_N^{\rm symm}(x,x')=-\tfrac12|x-x'|+C$ (2.139), with $C=L/4$ from the (2.111) recipe.

## 9. Electrostatic energy (§2.10, pp.60–63)

- Assembly work: $W=\frac12\sum_{i\ne j}q_iq_j/|\vec x_i-\vec x_j|$ (2.143) →
  $W=\frac12\int\rho\,\Phi\,d^3x$ (2.145) → field form
  $W=\int w\,d^3x$, $w=E^2/8\pi$ (2.147). The field form *includes* self-energies:
  a point charge diverges linearly (2.149); a 1-D string logarithmically
  (Exercise 2.10.2); a surface is finite.
- **Thompson's theorem** (p.62): fixed total charge on a fixed closed surface has
  minimum field energy when the surface is an equipotential — proof by
  $W'=W+\frac1{8\pi}\int|\vec\nabla\Delta\Phi|^2$ with vanishing cross term (2.153)–(2.155).
  Corollary flavor: introducing an uncharged insulated conductor *lowers* $W$
  (Exercise 2.10.1); adding a grounded neighbor *raises* a conductor's $C_{AA}$
  (Exercise 2.12.6).

## 10. Normal force on a charged surface (§2.11, pp.63–64)

The element $\sigma\,da$ feels the *average* of the fields on the two sides — the
disk/remainder split removes the self-field:
$\hat n\cdot\vec F=\tfrac12\sigma(\vec E_1+\vec E_2)\cdot\hat n$ (2.158)–(2.159);
for a conductor ($\vec E_1=0$, $E_{2n}=4\pi\sigma$): $\hat n\cdot\vec F=2\pi\sigma^2$
(2.161), always outward.

## 11. Capacitance (§2.12, pp.65–68)

- $N$ conductors, charge-free interior: $Q_i=\sum_jC_{ij}V_j$ with $C_{ij}$ a double
  normal derivative of $G_D$ over $S_i\times S_j$ (2.162)–(2.166); $C_{ij}=C_{ji}$
  from $G_D$ symmetry (2.167). Diagonal $C_{ii}$ = charge at unit potential, others
  grounded; off-diagonal = "induction coefficients".
- Energy: $W=\frac12\sum_iQ_iV_i=\frac12\sum_{ij}C_{ij}V_iV_j$ (2.169)–(2.170) —
  positivity of this quadratic form is the source of the inequalities
  $C_{ii}>0$, $C_{AB}^2<C_{AA}C_{BB}$ (Exercises 2.12.1–2.12.2).
- Closed systems: $\sum_iC_{ij}=0$ (2.171) (Gauss over all boundaries, (2.172)–(2.173)),
  so only potential *differences* matter (2.175). Isolated conductor: $Q=CV$ (2.177);
  with conductors nested inside the outermost surface, $C_{\infty\infty}=\sum_iC_{i1}$
  (2.178).
- Parallel plates: $C_{11}=C_{22}=-C_{12}=C$, $Q=C\Delta V$, $W=\frac12C\Delta V^2$
  (2.179)–(2.181), $C=A/4\pi a$ (2.182). Thin isolated disk: $C=2R/\pi$
  (Exercise 2.6.1). Variational principle: Dirichlet trial functions give *upper*
  bounds, $C\le C[\Psi]=\frac1{4\pi}\int|\vec\nabla\Psi|^2d^3x$ (Exercise 2.12.10;
  general version §3.10).

## Where the exercises sit

§2.14, printed pp.69–86: 41 exercises, keyed to sections —
2.1.1 (fields), 2.2.1–2.2.4 (deltas/Jacobians), 2.4.1–2.4.4 (Gauss/2-D/axial fields),
2.5.1–2.5.2 (Cavendish/Yukawa), 2.6.1–2.6.4 (disk, dipole layers),
2.7.1–2.7.3 (identities, reciprocation, MVT), 2.8.1–2.8.3 (G_D/G_N relations),
2.9.1–2.9.4 (1-D G's incl. Helmholtz), 2.10.1–2.10.4 (energy), 2.11.1 (surface force),
2.12.1–2.12.11 (capacitance matrix). All worked in `problems/problems.md`.
