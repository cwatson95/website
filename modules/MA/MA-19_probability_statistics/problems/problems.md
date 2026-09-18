# MA-19 — Problems

Work by hand, then check with `code/probability.py`. Citations in `../refs.md`.

### P1.  Binomial moments  *(Boas 3e §7, p.756)*
For the binomial, derive μ=np and σ²=np(1−p) (e.g. from the generating function or
directly). Confirm by summing k·P(k) and (k−μ)²·P(k). *Check:*
`sum(k*binomial_pmf(k,12,0.4) for k in range(13))` → 4.8.

**Solution.** Write $q=1-p$ and use $k\binom{n}{k}=n\binom{n-1}{k-1}$:
$$\mu=\sum_{k=0}^n k\binom{n}{k}p^kq^{n-k}=np\sum_{k=1}^n\binom{n-1}{k-1}p^{k-1}q^{n-k}=np\,(p+q)^{n-1}=np.$$
Similarly $E[X(X-1)]=n(n-1)p^2$, so $E[X^2]=n(n-1)p^2+np$ and
$$\sigma^2=E[X^2]-\mu^2=np-np^2=np(1-p).$$
For $n=12,\ p=0.4$: $\mu=12(0.4)=4.8$ and $\sigma^2=12(0.4)(0.6)=2.88$, matching the direct sums
`sum(k*binomial_pmf(k,12,0.4) for k in range(13))` $=4.8$ and $\sum(k-\mu)^2P(k)=2.88$.

### P2.  Binomial → Poisson  *(Boas 3e §9, p.767)*
Take n→∞, p→0 with np=λ fixed and show C(n,k)pᵏ(1−p)ⁿ⁻ᵏ → λᵏe⁻λ/k!. Verify the
convergence numerically. *Check:* `binomial_pmf(3, 1000, 2/1000)` ≈ `poisson_pmf(3, 2)`.

**Solution.** Put $p=\lambda/n$:
$$\binom{n}{k}p^k(1-p)^{n-k}=\underbrace{\frac{n(n-1)\cdots(n-k+1)}{n^k}}_{\to\,1}\,\frac{\lambda^k}{k!}\,\underbrace{\Big(1-\frac{\lambda}{n}\Big)^{n}}_{\to\,e^{-\lambda}}\underbrace{\Big(1-\frac{\lambda}{n}\Big)^{-k}}_{\to\,1}.$$
As $n\to\infty$ each braced factor tends to its limit, leaving $P(k)\to\lambda^k e^{-\lambda}/k!$ —
the Poisson law. Numerically for $k=3,\ \lambda=2,\ n=1000$, the binomial gives $0.18063$ versus
$\lambda^3e^{-\lambda}/3!=0.18045$, agreeing to $\sim0.1\%$ — i.e.
`binomial_pmf(3, 1000, 2/1000)` $\approx$ `poisson_pmf(3, 2)`.

### P3.  Normal bands  *(Boas 3e §8, p.761)*
Using the CDF ½(1+erf(z/√2)), confirm the 1σ/2σ/3σ probabilities 0.683 / 0.954 /
0.997. *Check:* `normal_cdf(1)-normal_cdf(-1)` ≈ 0.6827.

**Solution.** For the standard normal $\Phi(z)=\tfrac12\big(1+\operatorname{erf}(z/\sqrt2)\big)$, the band
probability is
$$P(|Z|\le a)=\Phi(a)-\Phi(-a)=\tfrac12\operatorname{erf}\tfrac{a}{\sqrt2}-\tfrac12\operatorname{erf}\tfrac{-a}{\sqrt2}=\operatorname{erf}\!\Big(\frac{a}{\sqrt2}\Big),$$
since $\operatorname{erf}$ is odd. Evaluating: $\operatorname{erf}(1/\sqrt2)=0.6827$,
$\operatorname{erf}(2/\sqrt2)=0.9545$, $\operatorname{erf}(3/\sqrt2)=0.9973$ — the familiar
$68.3/95.4/99.7\%$. This matches `normal_cdf(1)-normal_cdf(-1)` $=0.6827$.

### P4.  Central Limit Theorem  *(Boas 3e §8, p.761)*
Explain why (Σ of 12 U(0,1)) − 6 is ≈ N(0,1) (match its mean and variance). Sample
it and compare the empirical CDF to the normal. *Check:* `sample_uniform_sum(12, N, rng)`;
`sample_moments` → (0, 1, 0, 0).

**Solution.** Each $U_i\sim U(0,1)$ has $E[U_i]=\tfrac12$ and $\operatorname{Var}(U_i)=\tfrac1{12}$. For
$S=\sum_{i=1}^{12}U_i$,
$$E[S]=12\cdot\tfrac12=6,\qquad \operatorname{Var}(S)=12\cdot\tfrac1{12}=1,$$
so $S-6$ has mean $0$ and variance $1$. The Central Limit Theorem makes a sum of 12 i.i.d.
terms already nearly Gaussian, and symmetry forces skewness $\to0$ and excess kurtosis $\to0$;
hence $S-6\approx N(0,1)$. Sampling $40000$ draws gives `sample_moments`
$\approx(0.003,\,0.999,\,-0.015,\,-0.084)\to(0,1,0,0)$, and the empirical CDF tracks `normal_cdf`
to $\sim1\%$.

### P5.  Error propagation  *(Boas 3e §10, p.770)*
Derive σ_f²=Σ(∂f/∂xᵢ)²σᵢ². Apply to f=xy (relative errors add in quadrature) and
f=x+y (absolute errors add in quadrature). *Check:* `error_propagation(lambda v: v[0]*v[1],
[4,5], [0.1,0.2])`.

**Solution.** Linearize $f$ about the mean values:
$f\approx f(\bar{\mathbf x})+\sum_i\frac{\partial f}{\partial x_i}(x_i-\bar x_i)$. For independent $x_i$
the cross-terms average to zero, so
$$\sigma_f^2=\sum_i\Big(\frac{\partial f}{\partial x_i}\Big)^2\sigma_i^2.$$
For $f=xy$: $\partial_x f=y,\ \partial_y f=x$, giving $\sigma_f^2=y^2\sigma_x^2+x^2\sigma_y^2$, i.e.
$(\sigma_f/f)^2=(\sigma_x/x)^2+(\sigma_y/y)^2$ — relative errors in quadrature. For $f=x+y$:
$\sigma_f^2=\sigma_x^2+\sigma_y^2$. With $x=4\pm0.1,\ y=5\pm0.2$: $f=20$ and
$\sigma_f=\sqrt{5^2(0.1)^2+4^2(0.2)^2}=\sqrt{0.89}=0.943$, a relative $0.0472$ — exactly what
`error_propagation(lambda v: v[0]*v[1], [4,5], [0.1,0.2])` returns.

### P6.  Least-squares fit  *(Boas 3e §10, p.770)*
Derive b=S_xy/S_xx, a=ȳ−bx̄ by minimizing Σ(y−a−bx)². Fit noisy data from y=2+3x and
check the recovered slope sits within its quoted uncertainty of 3. *Check:*
`least_squares_line(xd, yd)`.

**Solution.** Minimize $\chi^2=\sum_i(y_i-a-bx_i)^2$. The normal equations are
$$\frac{\partial\chi^2}{\partial a}=-2\sum_i(y_i-a-bx_i)=0\ \Rightarrow\ a=\bar y-b\bar x,\qquad
\frac{\partial\chi^2}{\partial b}=-2\sum_i x_i(y_i-a-bx_i)=0.$$
Substituting $a=\bar y-b\bar x$ into the second gives $\sum_i(x_i-\bar x)(y_i-\bar y)=b\sum_i(x_i-\bar x)^2$,
hence
$$b=\frac{S_{xy}}{S_{xx}},\qquad a=\bar y-b\bar x.$$
Fitting noisy $y=2+3x$ yields `least_squares_line(xd, yd)` $=(b,a,\sigma_b,\sigma_a)=(2.988,\,1.992,\,0.032,\,0.177)$;
the slope sits $|3-2.988|=0.012<\sigma_b$ from the true $3$ — within its quoted uncertainty.
