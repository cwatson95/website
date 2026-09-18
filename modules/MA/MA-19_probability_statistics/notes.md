# MA-19 — Probability & Statistics (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. All in **Chapter 15, Probability and Statistics**.

## 1. Probability and random variables
A probability assigns numbers in [0,1] to events of a sample space, additive over
disjoint events with P(total)=1 [B §2 *Sample Space* p.724; §3 *Probability
Theorems* p.729]. A **random variable** X maps outcomes to numbers; its
distribution is summarized by **moments** [B §5 *Random Variables* p.744]:
$$\mu=E[X],\qquad \sigma^2=E[(X-\mu)^2]=E[X^2]-\mu^2,$$
plus skewness E[(X−μ)³]/σ³ and kurtosis. Code: `sample_moments`; `mean_var` gives
the closed forms.

## 2. The discrete distributions
- **Binomial** [B §7 *Binomial Distribution* p.756]: k successes in n independent
  trials, P(k)=C(n,k)pᵏ(1−p)ⁿ⁻ᵏ, with μ=np, σ²=np(1−p). Code: `binomial_pmf`.
- **Poisson** [B §9 *The Poisson Distribution* p.767]: the **rare-event limit** of
  the binomial (n→∞, p→0, np=λ), P(k)=λᵏe⁻λ/k!, with μ=σ²=λ. Code: `poisson_pmf`;
  the test shows binomial(n, λ/n) → Poisson(λ).

## 3. The continuous distributions
- **Normal / Gaussian** [B §8 *The Normal or Gaussian Distribution* p.761]:
  f(x)=1/(σ√2π)·exp(−(x−μ)²/2σ²); the CDF is ½(1+erf((x−μ)/σ√2)). The 1σ/2σ/3σ
  bands hold 68.3 / 95.4 / 99.7 %. Code: `normal_pdf`, `normal_cdf`.
- **Exponential** [B §6 *Continuous Distributions* p.750]: λe⁻λˣ, μ=1/λ, σ²=1/λ²
  — waiting times of a Poisson process. Code: `exponential_pdf`.

## 4. The Central Limit Theorem
The sum (or mean) of many independent random variables — *whatever* their
individual distribution — tends to a Gaussian [B §8 p.761, the normal as a limit].
A clean demonstrator: the sum of 12 uniform U(0,1) variables, minus 6, is already
an excellent N(0,1) (its mean is 0 and variance 12·(1/12)=1). Code:
`sample_uniform_sum`; the test confirms sample mean→0, variance→1, skew→0, and the
empirical CDF matches `normal_cdf` to ~1 %. The CLT is *why* measurement errors are
normally distributed and why §3's Gaussian dominates physics.

## 5. Statistics: getting numbers (and error bars) from data
[B §10 *Statistics and Experimental Measurements* p.770]
- **Error propagation**: for f(x₁,…,xₙ) with independent uncertainties σ_i,
  $$\sigma_f^2=\sum_i\Big(\frac{\partial f}{\partial x_i}\Big)^2\sigma_i^2.$$
  For a product f=xy this is the familiar (σ_f/f)²=(σ_x/x)²+(σ_y/y)²; for a sum,
  σ_f²=σ_x²+σ_y². Code: `error_propagation` (numerical partials).
- **Least squares**: the line y=a+bx minimizing Σ(y−a−bx)² has b=S_xy/S_xx,
  a=ȳ−bx̄, with uncertainties from the residual variance s²=SSE/(n−2). Code:
  `least_squares_line` (returns b, a, σ_b, σ_a); the test recovers a known slope to
  within its quoted σ.

## Where this goes
- `~SM-01`: a statistical ensemble is a probability distribution over microstates;
  the mean/variance machinery here is the thermodynamic average and fluctuation.
- `~SM-03`: the partition function is a normalizing constant (like Σpmf=1); ⟨E⟩ and
  Var(E)=k_BT²C_V are §1 moments of the Boltzmann distribution.
- `~PK-04`: rate coefficients fitted from swarm/EEDF data carry exactly the §5
  error bars; least-squares and propagation are the daily tools.
