# MA-15 — The Dirac Delta & Distributions (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. The delta lives in **Chapter 8 §11** (Boas amplified its
treatment in the 3rd edition — see her preface); the Fourier representation ties to
Ch.7.

## 1. What δ is (and is not)
The Dirac delta is **not a function** — it is a *distribution*, defined by how it
acts under an integral [B §11 *The Dirac Delta Function* p.449]:
$$\int_{-\infty}^{\infty}\delta(x)\,\phi(x)\,dx=\phi(0),\qquad
\int\delta(x-x_0)\,\phi(x)\,dx=\phi(x_0).$$
This **sifting property** is the whole definition; "δ(0)=∞" is only shorthand.
Operationally δ is the limit of a **nascent sequence** δ_a → δ as a→0, each with
∫δ_a=1 [B §11 p.449]:
$$\frac{1}{a\sqrt\pi}e^{-(x/a)^2},\quad \frac{1}{\pi}\frac{a}{x^2+a^2},\quad
\tfrac1a\mathbf 1_{|x|<a/2},\quad \frac{\sin(x/a)}{\pi x}.$$
Code: the four nascent functions and `sift`; the test confirms ∫δ_a=1 and
sift→φ(x0). (The Lorentzian has no finite second moment, so it sifts only
*decaying/bounded* test functions — a clean reminder that the test function class
matters.)

## 2. The derivative δ′
Differentiate the functional by parts (boundary terms vanish):
$$\int\delta'(x)\,\phi(x)\,dx=-\int\delta(x)\,\phi'(x)\,dx=-\phi'(0).$$
δ′ measures *minus the slope* of the test function at 0. Code:
`gaussian_delta_prime` (the derivative of the Gaussian nascent), `delta_prime_sift`;
the test checks ⟨δ′,φ⟩=−φ′(0) for several φ.

## 3. Composition δ(g(x))
For g with simple zeros x_i (g′(x_i)≠0), change variables near each root [B §11
eq.(11.19), p.456 — Boas lists δ(ax)=δ(x)/|a| as (c), the product δ[(x−a)(x−b)] as
(d), and the general rule as (e)]:
$$\delta\big(g(x)\big)=\sum_i\frac{\delta(x-x_i)}{\lvert g'(x_i)\rvert}\quad\Rightarrow\quad
\int\delta(g(x))\phi(x)\,dx=\sum_i\frac{\phi(x_i)}{\lvert g'(x_i)\rvert}.$$
Special case δ(ax)=δ(x)/|a|. Example δ(x²−c²)=δ[(x−c)(x+c)]: roots ±c, |g′|=2c,
giving [φ(c)+φ(−c)]/(2c). Code: `delta_compose_rhs` (the closed form) and
`delta_compose_integral` (the nascent-δ witness), shown to agree as a→0.
(In 2-D/3-D the same picks out a point: δ(x−x₀)δ(y−y₀)… — the point-charge
density ρ=q δ³(r−r₀) of `~EM-01` [B eqs (11.20)–(11.21), p.456].)

## 4. The Heaviside step and δ
The unit step H(x) (0 for x<0, 1 for x>0) has distributional derivative
$$H'(x)=\delta(x),$$
because ⟨H′,φ⟩=−⟨H,φ′⟩=−∫₀^∞φ′=φ(0)=⟨δ,φ⟩ [B §11 p.449]. So δ is the "density
of a jump"; the point-charge density ρ=q δ(r−r₀) of `~EM-01` is the same idea in 3-D.
Code: `heaviside`; the test verifies the integration-by-parts identity numerically.

## 5. The Fourier representation
Completeness of the Fourier modes gives the most-used identity of mathematical
physics:
$$\delta(x)=\frac{1}{2\pi}\int_{-\infty}^{\infty}e^{ikx}\,dk,
\qquad \frac{1}{2\pi}\int_{-K}^{K}e^{ikx}\,dk=\frac{\sin(Kx)}{\pi x}\xrightarrow{K\to\infty}\delta(x).$$
The truncated integral is the **Dirichlet/sinc kernel**, a nascent delta [B §11
eqs.(11.12)–(11.16), p.454; the Fourier-transform machinery is Ch.7 §12 p.378].
This is exactly the statement that the Fourier transform and its inverse undo each
other (`~MA-09`), and that ⟨x|x′⟩=δ(x−x′) in QM (`~QM-05`). Code:
`fourier_delta_kernel`; the test sifts a decaying φ as K→∞.

## Where this goes
- `~MA-14`: δ is the **source** in L_x G(x,ξ)=δ(x−ξ); the slope-jump of the Green's
  function is exactly ∫δ across the source point.
- `~MA-09`: §5 is Fourier completeness; δ(x)=∫e^{ikx}dk/2π is the kernel that makes
  transform-then-inverse the identity.
- `~QM-05`: continuous spectra need δ-normalization ⟨x|x′⟩=δ(x−x′); the sifting
  property is how position eigenstates resolve the identity.
