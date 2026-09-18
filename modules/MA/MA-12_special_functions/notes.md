# MA-12 — Special Functions (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. All four families live in **Chapter 12** (series
solutions); spherical harmonics in **Chapter 13**.

## 1. Why these four functions
Separating a PDE in the standard coordinate systems (`~MA-03`, `~MA-08`) always
leaves the same handful of ODEs. Each is a **Sturm–Liouville problem** (`~MA-11`),
so each gives an orthogonal, complete set with its own weight w(x):

| family | ODE | interval | weight w | physics |
|---|---|---|---|---|
| Legendre P_n | (1−x²)y″−2xy′+n(n+1)y=0 | [−1,1] | 1 | polar angle, multipoles `~EM-05` |
| Bessel J_n | x²y″+xy′+(x²−n²)y=0 | [0,a] | x | cylinders, drums `~EM-16` |
| Hermite H_n | y″−2xy′+2ny=0 | (−∞,∞) | e^{−x²} | oscillator `~QM-09` |
| Laguerre L_n | xy″+(1−x)y′+ny=0 | [0,∞) | e^{−x} | hydrogen radial `~QM-12` |

Code: `ode_residual(family, n, x)` plugs each evaluated function back into its ODE
(y′,y″ by central differences) and returns ~0.

## 2. Legendre polynomials — the model case
Built from the recurrence [B §2 *Legendre's Equation* p.564]
$$(n+1)P_{n+1}(x)=(2n+1)\,x\,P_n(x)-n\,P_{n-1}(x),\qquad P_0=1,\ P_1=x,$$
so P₂=(3x²−1)/2, P₃=(5x³−3x)/2, … with P_n(1)=1 and parity P_n(−x)=(−1)ⁿP_n(x).
Three classic handles:
- **Rodrigues' formula** $P_n=\frac1{2^n n!}\frac{d^n}{dx^n}(x^2-1)^n$ [B §4 p.568].
- **Generating function** $\frac1{\sqrt{1-2xt+t^2}}=\sum_n P_n(x)\,t^n$ [B §5 p.569]
  — the source of the multipole expansion. Code: `legendre_generating`.
- **Orthogonality** $\int_{-1}^1 P_mP_n\,dx=\frac{2}{2n+1}\delta_{mn}$ [B §7 p.577].
Code: `legendre`, `legendre_deriv`, `orthogonality_legendre`.

## 3. Associated Legendre & spherical harmonics
The φ-dependence of a separated problem raises the index m, giving the **associated
Legendre functions** P_l^m [B §10 p.583], built from
$P_m^m=(-1)^m(2m-1)!!\,(1-x^2)^{m/2}$ and the l-recurrence. Together with e^{imφ}
they form the **spherical harmonics** [B Ch.13, p.651]
$$Y_l^m(\theta,\phi)\propto P_l^m(\cos\theta)\,e^{im\phi},$$
the eigenfunctions of angular momentum (`~QM-10`). Code: `assoc_legendre`
(verified to reduce to P_l for m=0 and to match P_1^1, P_2^1, P_2^2).

## 4. Hermite, Laguerre — the quantum pair
Hermite [B §22 p.607]: $H_{n+1}=2xH_n-2nH_n$… giving H₀=1, H₁=2x, H₂=4x²−2, with
$\int H_mH_n e^{-x^2}dx=2^n n!\sqrt\pi\,\delta_{mn}$ — the oscillator wavefunctions
are H_n(x)e^{−x²/2} (`~QM-09`). Laguerre [B §22 p.609]: $(n+1)L_{n+1}=(2n+1-x)L_n-nL_{n-1}$,
orthonormal under e^{−x} on [0,∞) — the hydrogen radial functions (`~QM-12`). Code:
`hermite`, `laguerre`, `orthogonality_hermite`, `orthogonality_laguerre`.

## 5. Bessel functions
J_n solves Bessel's equation [B §12 p.587]; rather than the Frobenius series the
code uses the **integral representation**
$$J_n(x)=\frac1\pi\int_0^\pi\cos(n\tau-x\sin\tau)\,d\tau,$$
which the test cross-checks against the power series $\sum_k\frac{(-1)^k}{k!(n+k)!}(x/2)^{2k+n}$.
J_n(x) oscillates with decaying amplitude; its zeros set the radial modes of a
drum/waveguide and obey $\int_0^a J_n(\alpha_{k}r/a)J_n(\alpha_{j}r/a)\,r\,dr\propto\delta_{kj}$
(weight w=r) [B §19 p.601]. Code: `bessel_j`.

## Where this goes
- `~QM-09`: H_n ↔ the harmonic oscillator; the ladder operators of §22 are the
  algebraic version (`~QM-09` does it with a,a†).
- `~QM-12`: L_n (radial) and Y_l^m (angular) are the hydrogen wavefunction; the
  1/r potential bridge B4.
- `~EM-05`: the Legendre generating function (§2) *is* the multipole expansion of
  1/|r−r′|.
