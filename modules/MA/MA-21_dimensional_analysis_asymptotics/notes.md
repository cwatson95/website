# MA-21 — Dimensional Analysis & Asymptotics (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. The asymptotics are **Chapter 11 §10–11**; dimensional
analysis is a standard technique not given its own section in the shelf texts
(see `refs.md`).

## 1. Dimensional analysis — the Buckingham Pi theorem
Any physical law relating n quantities built from k independent base dimensions
(mass M, length L, time T, …) can be rewritten as a relation among **n − k
dimensionless groups** Π. Concretely: write the **dimension matrix** D (one row per
base dimension, one column per quantity, entries = exponents). A product of
quantities ∏ q_iᵖⁱ is dimensionless iff **D p = 0**, so the Pi groups are a basis
of the **null space** of D, and there are n − rank(D) of them. Code: `nullspace`,
`buckingham_pi`, `is_dimensionless`.

*Worked example — the pendulum.* Quantities {period T, length L, gravity g, mass
m} over (M,L,T):
$$D=\begin{pmatrix}0&0&0&1\\0&1&1&0\\1&0&-2&0\end{pmatrix},\quad \operatorname{rank}=3,\ \Rightarrow\ 4-3=1\ \text{group}.$$
The null vector is (2,−1,1,0): Π = g T²/L. With only one group the law must be
Π = const, i.e. **T ∝ √(L/g)** — the pendulum period, derived without solving any
equation of motion (and note the mass drops out). This is the engine behind the
Reynolds number, the Mach number, and every similarity argument (`~CM-23`).

## 2. Asymptotic series
An **asymptotic series** Σ aₙ/xⁿ may *diverge* for every x yet still approximate a
function f(x) for large x, in the precise sense that the error after N terms is
smaller than the first omitted term [B §10 *Asymptotic Series* p.549]:
$$f(x)-\sum_{n=0}^{N}\frac{a_n}{x^n}=O\!\left(\frac{1}{x^{N+1}}\right).$$
The canonical example is the scaled exponential integral g(x)=x eˣ E₁(x), with
$$g(x)\sim\sum_{k=0}^{\infty}(-1)^k\frac{k!}{x^k}=1-\frac1x+\frac{2}{x^2}-\cdots$$
The terms k!/xᵏ eventually **grow**, so the series diverges. Code:
`exp_integral_scaled_asymptotic` (the series) vs `exp_integral_scaled_true` (a
convergent quadrature benchmark).

## 3. Optimal truncation
Because the terms shrink then grow, the best you can do is **stop at the smallest
term**, near N ≈ x; the residual error is of order that smallest term,
~√(2πx) e⁻ˣ [B §10 p.549–551]. Code: `optimal_truncation` returns the best N and
its error; the test confirms (i) best N ≈ x, (ii) the minimal error is ~the
smallest term, and (iii) adding more terms makes it *worse* — the hallmark of an
asymptotic (as opposed to convergent) series. This "diverge but still useful" idea
is exactly how WKB and high-order perturbation theory behave in `~QM-15`.

## 4. Stirling's approximation
The most-used asymptotic series is **Stirling's** [B §11 *Stirling's Formula* p.552]:
$$\ln n!=n\ln n-n+\tfrac12\ln(2\pi n)+\frac{1}{12n}-\frac{1}{360n^3}+\cdots$$
Each correction shrinks the error; with the 1/(12n) term it is already < 1 ppm for
n ≳ 10. Code: `ln_factorial_stirling(n, terms)` checked against `math.lgamma`.
Stirling underlies the entropy of large systems (`~SM-02`, S = k ln Ω) and the
saddle-point method.

## 5. Regular perturbation
When a problem differs from a solvable one by a small parameter ε, expand the
answer as a power series in ε. For the root of x²+εx−1=0 near x=1, write
x = 1 + a₁ε + a₂ε² + … and match orders: a₁=−½, a₂=⅛, so
$$x\approx 1-\tfrac{\varepsilon}{2}+\tfrac{\varepsilon^2}{8}.$$
Code: `perturbed_root`; the test shows the order-k truncation has O(ε^{k+1}) error.
This is the baby version of Rayleigh–Schrödinger perturbation theory (`~QM-15`).
(When the small parameter multiplies the highest derivative the expansion becomes
*singular* — boundary layers, WKB — beyond this module.)

## Where this goes
- `~QM-15`: time-independent perturbation theory is §5 with ε = the perturbing
  Hamiltonian; WKB and large-order behavior are §2–3 (asymptotic, divergent).
- `~CM-23`/`~PK-03`: the Reynolds and Knudsen numbers are §1 Pi groups that decide
  which terms in Navier–Stokes/Boltzmann dominate.
- `~SM-02`: Stirling (§4) turns ln Ω for ~10²³ particles into the entropy.
