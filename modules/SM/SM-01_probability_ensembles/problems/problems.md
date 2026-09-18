# SM-01 — Problems

Work by hand, then check with `code/probability_ensembles.py`. Citations in
`../refs.md`; **Pa** = Pathria 3e, **Sch** = Schroeder (image-only).

### P1.  Multiplicity of a two-state paramagnet  *(Pa §1.2, p.3)*
For N spins in a field, the macrostate with n up has multiplicity Ω = C(N,n). Show
Ω is maximal at n = N/2 and that Ω(N, N/2) ≈ 2ᴺ√(2/πN) (use Stirling). *Check:*
`multiplicity_two_state(100,50)` ≈ 1.01×10²⁹, larger than any other `n`.

**Solution.** $\Omega(N,n)=\binom{N}{n}=\dfrac{N!}{n!\,(N-n)!}$. Comparing neighbours,
$$\frac{\Omega(N,n+1)}{\Omega(N,n)}=\frac{N-n}{n+1},$$
which is $>1$ for $n<(N-1)/2$ and $<1$ beyond it, so $\Omega$ climbs to a single maximum at $n=N/2$. Stirling
($\ln m!\approx m\ln m-m+\tfrac12\ln 2\pi m$) applied to $\ln\binom{N}{N/2}=\ln N!-2\ln(N/2)!$ gives
$\ln\Omega(N,\tfrac N2)\approx N\ln 2-\tfrac12\ln(\pi N/2)$, i.e.
$$\Omega\!\left(N,\tfrac N2\right)\approx 2^N\sqrt{\frac{2}{\pi N}}.$$
For $N=100$: $2^{100}\sqrt{2/100\pi}=1.27\times10^{30}\times0.0798\approx1.01\times10^{29}$, matching
`multiplicity_two_state(100,50)`$\approx1.01\times10^{29}$ — the largest over all $n$.

### P2.  Entropy is additive  *(Pa §1.2, p.3)*
Two isolated systems have multiplicities Ω₁, Ω₂. Show the combined system has
Ω = Ω₁Ω₂, hence S = k ln Ω = S₁ + S₂. *Check:* `boltzmann_entropy(o1*o2, 1) ==
boltzmann_entropy(o1,1) + boltzmann_entropy(o2,1)`.

**Solution.** Independence means each microstate of the compound system is a pair — one microstate of system 1 together
with one of system 2 — so counting the pairs multiplies the counts:
$$\Omega=\Omega_1\,\Omega_2.$$
Boltzmann's $S=k\ln\Omega$ then turns the product into a sum:
$$S=k\ln(\Omega_1\Omega_2)=k\ln\Omega_1+k\ln\Omega_2=S_1+S_2.$$
The logarithm is exactly what makes entropy extensive — additive over independent subsystems, where the multiplicity is
multiplicative. Numerically `boltzmann_entropy(o1*o2, 1)` returns $\ln(\Omega_1\Omega_2)$, equal to
`boltzmann_entropy(o1,1) + boltzmann_entropy(o2,1)` (the demo's $79.84453=79.84453$).

### P3.  Stirling's approximation  *(Pa §1.4, p.10; Sch Ch.2)*
Derive ln n! ≈ n ln n − n by approximating the sum Σ ln k as an integral, and find
the next correction ½ln(2πn). Compare both to the exact value for n = 100. *Check:*
`stirling_ln_factorial(100)` vs `math.lgamma(101)` (refined within 1e-4; leading
term off by ~3).

**Solution.** Write $\ln n!=\sum_{k=1}^{n}\ln k$ and approximate the sum by an integral:
$$\ln n!\approx\int_1^n\ln x\,dx=\big[x\ln x-x\big]_1^n=n\ln n-n+1\approx n\ln n-n.$$
The Euler–Maclaurin correction (half the top endpoint, plus a constant) restores the subleading terms,
$$\ln n!\approx n\ln n-n+\tfrac12\ln(2\pi n).$$
At $n=100$ the exact value is $\ln 100!=363.7394$ (`math.lgamma(101)`); the refined formula gives $363.7385$
(relative error $2.5\times10^{-6}<10^{-4}$), while the bare leading term $n\ln n-n=360.52$ is low by $\approx3.2$. Hence
`stirling_ln_factorial(100)` agrees with `math.lgamma(101)` to within $10^{-4}$, the leading-only form off by $\sim3$.

### P4.  Sharpness of the peak  *(Pa §1.2, p.3)*
For the fair two-state distribution P(N,n) = C(N,n)/2ᴺ, show the standard deviation
is √N/2 and the **fractional** width σ/⟨n⟩ = 1/√N. How large is it at N = 10²³?
*Check:* `fractional_width(100)/fractional_width(400) == 2`; `fractional_width(1e6)
== 1e-3`.

**Solution.** $P(N,n)=\binom{N}{n}2^{-N}$ is the distribution of $N$ fair coins ($p=\tfrac12$) — a sum of $N$ independent
Bernoulli$(\tfrac12)$ variables. Therefore
$$\langle n\rangle=Np=\frac N2,\qquad \sigma^2=Np(1-p)=\frac N4,\qquad \sigma=\frac{\sqrt N}{2}.$$
The fractional width follows:
$$\frac{\sigma}{\langle n\rangle}=\frac{\sqrt N/2}{N/2}=\frac{1}{\sqrt N},$$
which vanishes as $N\to\infty$: at $N=10^{23}$ it is $1/\sqrt{10^{23}}\approx3\times10^{-12}$, so the magnetization is pinned to
a part in $10^{12}$ and thermodynamics looks deterministic. This gives
`fractional_width(100)/fractional_width(400)`$=\sqrt{400/100}=2$ and `fractional_width(1e6)`$=10^{-3}$.

### P5.  Gaussian limit of the binomial  *(Pa §1.2, p.3; de Moivre–Laplace)*
Show that near the peak the binomial P(N,n) tends to a Gaussian of mean N/2 and
variance N/4. Verify it for N = 200 at n = 90, 100, 110. *Check:*
`gaussian_approx_two_state(200,n)` matches `two_state_probability(200,n)` within 2%.

**Solution.** Expand $\ln P(N,n)$ about the peak $n_0=N/2$. The first derivative $\dfrac{d}{dn}\ln\binom{N}{n}=\ln\dfrac{N-n}{n}$
vanishes at $n_0$, and the second derivative there is $\dfrac{d^2}{dn^2}\ln\binom{N}{n}=-\dfrac1n-\dfrac1{N-n}=-\dfrac4N$,
while the peak height is $P(n_0)\approx\sqrt{2/\pi N}$ (P1). A second-order Taylor expansion then exponentiates to
$$P(n)\approx\sqrt{\frac{2}{\pi N}}\;e^{-(n-N/2)^2/(2\cdot N/4)}=\frac{1}{\sqrt{2\pi\,(N/4)}}\;e^{-(n-N/2)^2/2(N/4)},$$
a Gaussian of mean $N/2$ and variance $N/4$ — the de Moivre–Laplace theorem. For $N=200$ ($\sigma=\sqrt{50}=7.07$): at $n=100$,
binomial $0.05635$ vs Gaussian $0.05642$ ($0.13\%$); at $n=90,110$, $0.02080$ vs $0.02076$ ($0.21\%$) — all within $2\%$, so
`gaussian_approx_two_state(200,n)` matches `two_state_probability(200,n)`.
