# ST-18 — The Central Limit Theorem & Approximations (notes)

Every distribution in this trunk has been pointing here. The normal of `~ST-12`
was introduced as "the most important continuous distribution"; this module says
*why*. The **central limit theorem** is the reason the Gaussian is universal: add
up many independent contributions — whatever their individual law — and the
standardized total is normal in the limit. That single fact explains the bell of
thermodynamic fluctuations (`~SM-01`), of measurement error, of kinetic
distribution functions (`~PK-01`), and it licenses the practical **normal
approximations to the binomial and Poisson** that close Penn State STAT 414. Every
formula below is tied to a function in `code/clt.py`.

Citation key (full details + granularity in `refs.md`): **PSU L27** = STAT 414
Lesson 27 *The Central Limit Theorem*; **PSU L28** = Lesson 28 *Approximations for
Discrete Distributions*; **HTZ** = Hogg, Tanis & Zimmerman, *Probability and
Statistical Inference*, Ch. 5. Cited at **lesson/chapter level**. $\Phi,\varphi$
are the standard-normal cdf and pdf; $q\equiv1-p$.

## 1. Sums of i.i.d. random variables

Let $X_1,\dots,X_n$ be **independent and identically distributed** with common
mean $\mu=E[X_i]$ and variance $\sigma^2=\operatorname{Var}(X_i)<\infty$. Form the
**sum** $S_n=\sum_{i=1}^n X_i$ and the **sample mean** $\bar X=S_n/n$. Linearity of
expectation and independence (variances of independents add) give exactly
[PSU L27; HTZ §5.6]
$$E[S_n]=n\mu,\quad \operatorname{Var}(S_n)=n\sigma^2;\qquad
E[\bar X]=\mu,\quad \operatorname{Var}(\bar X)=\frac{\sigma^2}{n}.$$
Two things to notice. The **mean is unbiased** — $\bar X$ is centered on the true
$\mu$ for every $n$ — and its **spread collapses**, $\operatorname{SD}(\bar X)=
\sigma/\sqrt n\to0$. This $1/\sqrt n$ is the **standard error**, the rate at which
averaging beats down noise, and it is exactly the fractional width $1/\sqrt N$ that
makes thermodynamics sharp in `~SM-01`. In code a parent law is a pmf array
`probs` with `probs[k]=P(X=k)`; `pmf_mean` and `pmf_var` return $\mu,\sigma^2$, and
because the pmf of a sum of independents is a **convolution** (`~ST-16`),
`nfold_pmf(probs, n)` builds the exact law of $S_n$ with mean $n\mu$ and variance
$n\sigma^2$ (checked in `test_convolution_normalization_and_moments`).

## 2. The central limit theorem

The mean of $\bar X$ is fixed and its variance vanishes, so $\bar X\to\mu$ (the law
of large numbers). The CLT describes the *shape* of the residual fluctuation once
we rescale it to a fixed size. **Standardize** the sum (subtract its mean, divide
by its standard deviation):
$$Z_n=\frac{S_n-n\mu}{\sigma\sqrt n}
=\frac{\bar X-\mu}{\sigma/\sqrt n},\qquad E[Z_n]=0,\ \operatorname{Var}(Z_n)=1.$$
The **central limit theorem** states that, no matter the parent distribution (so
long as $\sigma^2<\infty$), the cdf of $Z_n$ converges pointwise to the
standard-normal cdf [PSU L27; HTZ §5.6]:
$$\boxed{\ \lim_{n\to\infty}P(Z_n\le z)=\Phi(z)=\int_{-\infty}^{z}\frac{1}{\sqrt{2\pi}}
e^{-t^2/2}\,dt\ }\qquad(\text{convergence in distribution}).$$
Equivalently $S_n\approx N(n\mu,\,n\sigma^2)$ and $\bar X\approx N(\mu,\sigma^2/n)$
for large $n$. The remarkable content is **universality**: the parent's higher
structure (skew, modes, even whether it is discrete) is washed out, leaving only
$\mu$ and $\sigma^2$ to set the location and scale of one fixed curve. Code
`standard_normal_cdf` is $\Phi$ via $\operatorname{erf}$ (the limit target), and
`standard_normal_pdf` its density $\varphi$; `test_standard_normal_cdf_via_erf_and_integral`
checks $\Phi(0)=\tfrac12$, the reflection $\Phi(-z)=1-\Phi(z)$, and that $\Phi$ is
the integral of $\varphi$ (the `_integrate` continuous check).

## 3. Why it is true: the moment-generating-function proof

The cleanest proof uses the mgf of `~ST-06` and its **uniqueness theorem** (if
mgfs converge to a limit mgf on a neighborhood of $0$, the distributions converge).
Work with the centered, scaled variables $Y_i=(X_i-\mu)/\sigma$, so $E[Y_i]=0$,
$E[Y_i^2]=1$, and $Z_n=\frac1{\sqrt n}\sum_i Y_i$. By independence the mgf factors,
$$M_{Z_n}(t)=E\!\Big[e^{tZ_n}\Big]=\Big[M_Y\!\Big(\tfrac{t}{\sqrt n}\Big)\Big]^n .$$
Taylor-expand the single-variable mgf about $0$ using $M_Y(0)=1$, $M_Y'(0)=E[Y]=0$,
$M_Y''(0)=E[Y^2]=1$ [PSU L27; HTZ §5.6]:
$$M_Y(s)=1+\tfrac12 s^2+o(s^2)\ \Longrightarrow\
M_{Z_n}(t)=\Big[1+\frac{t^2}{2n}+o\!\big(\tfrac1n\big)\Big]^n
\ \xrightarrow[n\to\infty]{}\ e^{t^2/2}.$$
But $e^{t^2/2}$ is exactly the mgf of $N(0,1)$ (`~ST-12` §6), so by uniqueness
$Z_n\to N(0,1)$. The first two moments survive the limit; everything else is
$o(1/n)$ and dies — the algebraic statement of universality. (The fully rigorous
version replaces the mgf by the always-finite **characteristic function**
$E[e^{itZ_n}]\to e^{-t^2/2}$, removing the assumption that $M$ exists; the limit
$(1+a/n)^n\to e^a$ is the same `~MA-21` asymptotic.)

## 4. Seeing it: convolution and the standardized cdf

The mgf proof is slick but invisible; the code makes the convergence concrete. The
pmf of a sum of independents is the **convolution** of their pmfs (`~ST-16`):
$$P(S_2=k)=\sum_j P(X_1=j)\,P(X_2=k-j)\equiv(p*p)[k],\qquad
P(S_n=\cdot)=\underbrace{p*p*\cdots*p}_{n}.$$
Code `convolve_pmf` is one convolution and `nfold_pmf(probs, n)` iterates it $n$
times. To watch the CLT, standardize the *exact* cdf of $S_n$ and measure its
largest gap from $\Phi$. With $\mu_n=n\mu$, $\sigma_n=\sigma\sqrt n$, and the
continuity correction of §7 to place a step cdf against a smooth one,
$$\mathrm{err}(n)=\max_k\Big|\,F_{S_n}(k)-\Phi\!\Big(\frac{k+\tfrac12-\mu_n}{\sigma_n}\Big)\Big|.$$
This is `clt_cdf_max_error(probs, n)`. For a **fair die** (uniform on
$\{1,\dots,6\}$, far from normal) the table from `clt_demo` is
$$\mathrm{err}(1)=0.0542,\ \mathrm{err}(4)=0.0071,\ \mathrm{err}(16)=0.0016,\
\mathrm{err}(64)=0.00041,$$
falling steadily toward zero: a single die is visibly non-normal, but the sum of
sixty-four is the bell to four decimals. `test_clt_cdf_error_shrinks_to_zero`
asserts the strict decrease (and that a skewed Bernoulli parent converges too).

## 5. How fast: the Berry–Esseen rate

The CLT is a limit; for use we need its *speed*. The **Berry–Esseen theorem** makes
the convergence uniform and quantitative: if $\rho=E|X-\mu|^3<\infty$, then the
Kolmogorov distance between the standardized cdf and $\Phi$ obeys [HTZ §5.6;
`~MA-21`]
$$\sup_x\Big|F_{S_n}(x)-\Phi\!\Big(\frac{x-n\mu}{\sigma\sqrt n}\Big)\Big|
\ \le\ \frac{C\,\rho}{\sigma^{3}\,\sqrt n}.$$
The rate is $O(n^{-1/2})$ — doubling $n$ shrinks the worst-case error by
$1/\sqrt2$ — and the constant is universal ($C\le0.7655$, van Beek; the best known
is $C\approx0.469$, Shevtsova). Code `kolmogorov_cdf_error(probs, n)` computes the
true left/right sup over the lattice, `pmf_third_abs_moment` returns $\rho$, and
`berry_esseen_bound(probs, n)` returns $C\rho/(\sigma^3\sqrt n)$. For the die the
inequality holds with comfortable margin (actual $0.143\le$ bound $0.980$ at
$n=1$), asserted in `test_berry_esseen_bound_holds`; the leading $n^{-1/2}$ envelope
shows up as `err`$\cdot\sqrt n$ staying bounded in `test_clt_root_n_rate`. The
moral for Lesson 28: the normal approximation already does well at modest $n$, and
its error decays predictably.

## 6. The normal approximation to the binomial (de Moivre–Laplace)

The first and oldest CLT is the **de Moivre–Laplace theorem**, the special case
$X_i\sim\mathrm{Bernoulli}(p)$. Then $S_n=\sum X_i\sim\mathrm{Bin}(n,p)$ with
$\mu=np$ and $\sigma^2=npq$ (`~ST-07`), so the CLT gives [PSU L28; HTZ §5.7]
$$\mathrm{Bin}(n,p)\ \approx\ N\big(np,\,np q\big),\qquad
P(X\le k)\approx\Phi\!\Big(\frac{k-np}{\sqrt{npq}}\Big).$$
This is the limit $\mathrm{Bin}\to$ normal that complements the $\mathrm{Bin}\to
\mathrm{Poisson}$ limit of `~ST-09`: the **normal** is the $n\to\infty$ limit with
$p$ *fixed* (so $\mu,\sigma\to\infty$), the **Poisson** the limit with $np=\lambda$
*fixed* (rare events). Code `binom_pmf`/`binom_cdf` give the exact law and
`normal_approx_binomial(k,n,p,continuity=False)` the raw normal. The raw version is
mediocre — for $\mathrm{Bin}(20,\tfrac12)$ it estimates $P(X\le10)$ as $\Phi(0)=0.5$
against the true $0.5881$ — because a smooth curve is being asked to match the
midpoint of an integer step. The fix is §7.

## 7. The continuity correction

A discrete $X$ puts its probability on integers; the approximating normal spreads
it continuously. Align them by giving each integer $k$ the **unit interval**
$[k-\tfrac12,k+\tfrac12]$, so "$X\le k$" becomes "$\le k+\tfrac12$" under the normal
[PSU L28; HTZ §5.7]:
$$P(X\le k)\approx\Phi\!\Big(\frac{k+\tfrac12-\mu}{\sigma}\Big),\qquad
P(X\ge k)\approx1-\Phi\!\Big(\frac{k-\tfrac12-\mu}{\sigma}\Big),$$
$$P(a\le X\le b)\approx\Phi\!\Big(\frac{b+\tfrac12-\mu}{\sigma}\Big)
-\Phi\!\Big(\frac{a-\tfrac12-\mu}{\sigma}\Big),\qquad
P(X=k)\approx\Phi\!\Big(\frac{k+\tfrac12-\mu}{\sigma}\Big)
-\Phi\!\Big(\frac{k-\tfrac12-\mu}{\sigma}\Big).$$
This **continuity correction** is the difference between a usable approximation and
a poor one. The same $P(X\le10)$ for $\mathrm{Bin}(20,\tfrac12)$ now reads
$\Phi(0.5/\sqrt5)=0.5885$ against the true $0.5881$ — three correct digits instead
of one. Over *all* $k$ the maximum cdf error for $\mathrm{Bin}(10,\tfrac12)$ drops
from $0.123$ (uncorrected) to $0.0027$ (corrected), a factor of $\sim45$. Code
`normal_approx_binomial` (default `continuity=True`) and
`normal_approx_binomial_interval`; `binomial_approx_max_error` and
`binomial_approx_error_table` tabulate the gain, asserted in
`test_binomial_continuity_correction_helps` and `test_binomial_error_table_decreasing`.

## 8. The normal approximation to the Poisson

A Poisson is a sum, too: $\mathrm{Poisson}(\lambda)=\sum_{i=1}^m\mathrm{Poisson}(
\lambda/m)$ for any $m$ by the reproductive property (`~ST-09`), so the CLT applies
as $\lambda\to\infty$. With $\mu=\operatorname{Var}=\lambda$ [PSU L28],
$$\mathrm{Poisson}(\lambda)\ \approx\ N(\lambda,\lambda),\qquad
P(X\le k)\approx\Phi\!\Big(\frac{k+\tfrac12-\lambda}{\sqrt\lambda}\Big).$$
Code `normal_approx_poisson` (continuity-corrected by default). The maximum cdf
error over $k$ shrinks like $1/\sqrt\lambda$: `poisson_approx_max_error` gives
$0.0322,\ 0.0165,\ 0.0083$ at $\lambda=4,16,64$ — each quadrupling of $\lambda$
halves the error, exactly the §5 rate with $n\leftrightarrow\lambda$. This is why
photon-counting shot noise (`~QO-01`) and large event counts (`~PK-04`) look
Gaussian once the mean count is large, with width $\sqrt\lambda$.
`test_poisson_normal_approx_limit` checks both the continuity gain and the decay.

## 9. The local limit theorem

The cdf statements above have a **density** counterpart. Dividing the
continuity-corrected single-bar probability by its width $1$ and shrinking suggests
$P(X=k)\approx\tfrac1\sigma\varphi((k-\mu)/\sigma)$, the **local de Moivre–Laplace
theorem** [HTZ §5.7]:
$$P(X=k)\ \approx\ \frac{1}{\sqrt{2\pi npq}}\,
\exp\!\Big(-\frac{(k-np)^2}{2npq}\Big)=\frac1\sigma\varphi\!\Big(\frac{k-\mu}{\sigma}\Big).$$
It says the *bars* of the binomial pmf trace out the normal density, not just that
their partial sums match $\Phi$. Code `de_moivre_laplace_pmf(k,n,p)`; for
$\mathrm{Bin}(20,\tfrac12)$ at the center it returns $0.1784$ against the exact bar
$0.1762$, and the local densities sum to $\approx1$ across the support
(`test_de_moivre_laplace_local`). This is precisely the de Moivre–Laplace Gaussian
that `~SM-01`'s `gaussian_approx_two_state` puts on the two-state multiplicity: a
fair binomial $\mathrm{Bin}(N,\tfrac12)$ becomes $N(N/2,N/4)$, the sharp peak of
statistical mechanics. **Rule of thumb** (`normal_approx_applicable`): trust the
approximation once $np\ge5$ and $n(1-p)\ge5$ — i.e. the mean must sit at least a few
$\sigma$ from both boundaries $0$ and $n$ for the symmetric bell to fit.

## Where this goes

- `~ST-12` (the normal distribution) — the limit law $N(0,1)$ this module *derives*
  as universal; `~ST-06` (mgf & uniqueness) powers the §3 proof, and `~ST-16`
  (sums by convolution) the §4 demonstration. `~ST-05` supplies $\mu,\sigma^2$.
- `~ST-07` (binomial) and `~ST-09` (Poisson) — the discrete laws Lesson 28
  approximates; the normal limit (fixed $p$) and the Poisson limit (fixed $np$) are
  the two faces of the binomial's large-$n$ behavior.
- `~SM-01` (statistical-mechanics fluctuations, **B11**) — the physics payoff:
  the de Moivre–Laplace Gaussian of §9 is why a macroscopic average has fractional
  width $1/\sqrt N$ and thermodynamics looks deterministic. `~PK-01` (kinetic
  distribution functions) — the moments the CLT governs in transport theory.
- `~MA-21` (asymptotic analysis) — the home of the $O(n^{-1/2})$ Berry–Esseen rate
  of §5, the $(1+a/n)^n\to e^a$ limit of §3, and Laplace's method behind the
  Gaussian peak; `~MA-19` is the trunk's parent probability survey.
- Beyond this trunk: the CLT is the foundation of **statistical inference** —
  confidence intervals and $z$/$t$-tests use $\bar X\approx N(\mu,\sigma^2/n)$ with
  the $\chi^2,t,F$ sampling laws of `~ST-17` — the natural sequel to STAT 414.
