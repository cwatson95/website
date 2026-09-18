# ST-18 — The Central Limit Theorem & Approximations

Final module of the **PROBABILITY THEORY** trunk (see `modules/ST/list_ST.txt`),
a module-by-module replica of Penn State **STAT 414**. Covers **Lesson 27 — The
Central Limit Theorem** and **Lesson 28 — Approximations for Discrete
Distributions**. This is the capstone: it explains *why* the normal of `~ST-12`
is universal — sums of many independent pieces, whatever their own law, become
Gaussian — and turns that limit into the everyday normal approximations to the
binomial (`~ST-07`) and the Poisson (`~ST-09`).

- **Prerequisites:** `~ST-12` (the normal distribution — the limit law $N(0,1)$,
  its cdf $\Phi$ via $\operatorname{erf}$, the continuity-correction target),
  `~ST-16` (transformations & **sums by convolution** — the pmf of $S_n$ is the
  $n$-fold convolution of the parent), `~ST-06` (moment-generating functions —
  the mgf proof of the CLT and the uniqueness theorem), `~ST-05` (mean and
  variance of a distribution).
- **Cross-links:** `~SM-01` (why macroscopic averages are sharp — the
  de Moivre–Laplace Gaussian of the two-state system, fractional width
  $1/\sqrt N$ is the CLT in B11 form), `~PK-01` (distribution functions $f(\mathbf
  v)$ and their moments — the kinetic objects the CLT governs), `~MA-21`
  (asymptotic analysis — the $O(n^{-1/2})$ Berry–Esseen rate and Laplace's
  method behind the normal limit), `~ST-07` (binomial) and `~ST-09` (Poisson) —
  the two laws Lesson 28 approximates, `~MA-19` (the trunk's parent probability
  survey).

## Scope
Let $X_1,X_2,\dots$ be **independent and identically distributed** with mean
$\mu=E[X_i]$ and finite variance $\sigma^2=\operatorname{Var}(X_i)$, and write the
**sum** $S_n=\sum_{i=1}^n X_i$ and **sample mean** $\bar X=S_n/n$. The **central
limit theorem** says the *standardized* sample mean converges in distribution to
the standard normal:
$$Z_n=\frac{\bar X-\mu}{\sigma/\sqrt n}=\frac{S_n-n\mu}{\sigma\sqrt n}
\ \xrightarrow{\ d\ }\ N(0,1),\qquad
\lim_{n\to\infty}P(Z_n\le z)=\Phi(z).$$
The limit shape is the Gaussian (`~ST-12`) **regardless of the parent law** — the
universality that makes the normal the keystone of statistics. The module exhibits
the convergence by **convolution**: the pmf of $S_n$ is the $n$-fold convolution
of the parent pmf (`~ST-16`), and the maximum gap between its standardized cdf and
$\Phi$ shrinks like $1/\sqrt n$, the **Berry–Esseen** rate
$\sup_x|F_{S_n}(x)-\Phi|\le C\rho/(\sigma^3\sqrt n)$ (`~MA-21`). Lesson 28 cashes
the theorem out as the **normal approximations to discrete laws**: with mean and
variance matched, $\mathrm{Bin}(n,p)\approx N(np,np(1-p))$ and
$\mathrm{Poisson}(\lambda)\approx N(\lambda,\lambda)$. Because a continuous curve
is replacing integer bars, the **continuity correction** sharpens every
probability,
$$P(X\le k)\approx\Phi\!\Big(\frac{k+\tfrac12-\mu}{\sigma}\Big),\qquad
P(a\le X\le b)\approx\Phi\!\Big(\frac{b+\tfrac12-\mu}{\sigma}\Big)
-\Phi\!\Big(\frac{a-\tfrac12-\mu}{\sigma}\Big),$$
and the local **de Moivre–Laplace** limit $P(X=k)\approx\frac1\sigma\varphi\big(
(k-\mu)/\sigma\big)$ approximates a single bar. The error shrinks as $n$ (resp.
$\lambda$) grows; the usual rule of thumb is $np\ge5$ and $n(1-p)\ge5$.

## Operations — `code/clt.py`  (pure `numpy` + `math`; pmf = array with `probs[k]=P(X=k)`)

| call | meaning | reference |
|------|---------|-----------|
| `standard_normal_pdf(z)` | $\varphi(z)=e^{-z^2/2}/\sqrt{2\pi}$ (the limit density) | L27; `~ST-12` |
| `standard_normal_cdf(z)` | $\Phi(z)=\tfrac12[1+\operatorname{erf}(z/\sqrt2)]$ | L27; `~ST-12` |
| `convolve_pmf(p, q)` | pmf of $X+Y$: $(p*q)[k]=\sum_j p_j\,q_{k-j}$ | L27; `~ST-16` |
| `nfold_pmf(probs, n)` | pmf of $S_n=\sum_1^n X_i$ ($n$-fold self-convolution) | L27 |
| `pmf_mean(probs)` / `pmf_var(probs)` | $\mu=\sum_k kP_k$, $\sigma^2=\sum_k k^2P_k-\mu^2$ | L27; `~ST-05` |
| `pmf_third_abs_moment(probs)` | $\rho=E\lvert X-\mu\rvert^3$ (Berry–Esseen input) | L27; `~MA-21` |
| `clt_cdf_max_error(probs, n)` | $\max_k\lvert F_{S_n}(k)-\Phi(\tfrac{k+0.5-\mu_n}{\sigma_n})\rvert$ | L27 |
| `clt_demo(probs, ns)` | table $[(n,\text{error})]$ — the gap $\to 0$ | L27 |
| `kolmogorov_cdf_error(probs, n)` | $\sup_x\lvert F_{S_n}(x)-\Phi(\tfrac{x-\mu_n}{\sigma_n})\rvert$ | L27; `~MA-21` |
| `berry_esseen_bound(probs, n)` | $C\rho/(\sigma^3\sqrt n)$, $C=0.7655$ | L27; `~MA-21` |
| `binom_pmf(k,n,p)` / `binom_cdf(k,n,p)` | exact $\mathrm{Bin}(n,p)$ (`~ST-07`) | L28 |
| `poisson_pmf(k,lam)` / `poisson_cdf(k,lam)` | exact $\mathrm{Poisson}(\lambda)$ (`~ST-09`) | L28 |
| `normal_approx_binomial(k,n,p,continuity=True)` | $P(X\le k)\approx\Phi(\tfrac{k+0.5-np}{\sqrt{npq}})$ | L28 |
| `normal_approx_binomial_interval(a,b,n,p)` | $P(a\le X\le b)$, two-sided continuity correction | L28 |
| `de_moivre_laplace_pmf(k,n,p)` | $P(X{=}k)\approx\tfrac1\sigma\varphi(\tfrac{k-np}{\sigma})$ (local limit) | L28 |
| `normal_approx_poisson(k,lam,continuity=True)` | $P(X\le k)\approx\Phi(\tfrac{k+0.5-\lambda}{\sqrt\lambda})$ | L28 |
| `binomial_approx_max_error(n,p,continuity=True)` | $\max_k\lvert\text{Bin cdf}-\text{approx}\rvert$ | L28 |
| `poisson_approx_max_error(lam,continuity=True)` | $\max_k\lvert\text{Poisson cdf}-\text{approx}\rvert$ | L28 |
| `binomial_approx_error_table(p, ns)` | error vs $n$ at fixed $p$ ($\to 0$) | L28 |
| `normal_approx_applicable(n, p, thresh=5)` | rule of thumb $np\ge5$ and $n(1-p)\ge5$ | L28 |

## Use
```python
import numpy as np
from clt import (standard_normal_cdf, die_pmf, clt_cdf_max_error, binom_cdf,
                 normal_approx_binomial, normal_approx_binomial_interval,
                 poisson_approx_max_error, normal_approx_applicable)

float(standard_normal_cdf(1.96))                  # 0.975002   the limit law N(0,1)
clt_cdf_max_error(die_pmf(), 1)                   # 0.05424    one die: not yet normal
clt_cdf_max_error(die_pmf(), 64)                  # 0.00041    sum of 64: essentially Phi
binom_cdf(10, 20, 0.5)                            # 0.588099   exact P(X<=10), Bin(20,1/2)
normal_approx_binomial(10, 20, 0.5)               # 0.588468   cont.-corrected: Phi(0.5/sqrt5)
normal_approx_binomial(10, 20, 0.5, False)        # 0.5        no correction: much worse
normal_approx_binomial_interval(8, 12, 20, 0.5)   # 0.736448   vs exact 0.736824
poisson_approx_max_error(4.0), poisson_approx_max_error(64.0)  # 0.0322, 0.0083  (~1/sqrt(lam))
normal_approx_applicable(20, 0.5)                 # True       np=n(1-p)=10 >= 5
```

## Run
```bash
cd code
python3 clt.py          # demo: Phi, CLT-by-convolution, Berry-Esseen, binomial/Poisson approx
python3 test_clt.py     # tests  ->  "All 12 tests passed."
```

## Files
- `notes.md` — i.i.d. sums → the CLT statement (sum & sample-mean forms) → the
  mgf proof → convergence by convolution and the Berry–Esseen rate → the normal
  approximations to the binomial & Poisson → the continuity correction and the
  de Moivre–Laplace local limit; each result tied to a code symbol, with a
  "Where this goes" map.
- `code/clt.py`, `code/test_clt.py` (`numpy` + stdlib `math` only, self-contained).
- `problems/problems.md` — worked problems (STAT 414 L27–L28; each with a numeric
  `*Check:*` against the code).
- `refs.md` — citation table (STAT 414 OER primary, lesson level; Hogg–Tanis–
  Zimmerman, Wackerly, Ross cross-cited at chapter level).
