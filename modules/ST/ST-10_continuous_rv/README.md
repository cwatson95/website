# ST-10 — Continuous Random Variables

Tenth module of the **PROBABILITY THEORY** trunk (a module-by-module replica of
Penn State's STAT 414; see `modules/ST/list_ST.txt`). Covers **Lesson 13**
(Exploring Continuous Data) and **Lesson 14** (Continuous Random Variables): the
move from probability *mass* on a countable set (`~ST-05`) to probability
*density* on an interval. A continuous random variable spreads a total
probability of $1$ as **area** under a density curve $f(x)$, and every question —
intervals, means, variances, percentiles — becomes an integral.

- **Prerequisites:** `~ST-05` (discrete random variables, expectation $E[X]=\sum x\,p(x)$
  and variance — every formula here is the integral version of one there),
  `~MA-15` (the **Dirac delta** as the density of a point mass — the bridge that
  makes a discrete jump look like a continuous density), basic single-variable
  integration (`~MA-02`).
- **Cross-links:** `~ST-06` (moment-generating functions, $M(t)=E[e^{tX}]$ as an
  integral), `~ST-11`/`~ST-12` (the exponential, gamma, and normal laws — the
  named continuous distributions this machinery is built to handle), `~SM-01`
  (continuous probability densities in statistical mechanics), `~SM-06` (the
  Maxwell–Boltzmann *speed density*, the same $\int f=1$, $E[g(v)]=\int g f$).

## Scope
A **continuous** random variable $X$ has a **probability density function (pdf)**
$f(x)\ge0$ with $\int_{-\infty}^{\infty}f=1$. Its **cumulative distribution
function (cdf)** is $F(x)=P(X\le x)=\int_{-\infty}^{x}f$, so by the fundamental
theorem of calculus $f=F'$. Because probability is *area*, a single point has
$P(X=x)=0$, and intervals obey $P(a<X<b)=F(b)-F(a)=\int_a^b f$ (open vs. closed
endpoints do not matter). **Expectation** and **variance** are integrals,
$E[X]=\int x f$, $\operatorname{Var}[X]=E[X^2]-(E[X])^2$, the continuous echo of
the sums in `~ST-05`. **Percentiles / quantiles** invert the cdf, $F(\pi_p)=p$ (the
code does this by bisection). The headline example is the **continuous uniform**
$U(a,b)$: $f=\tfrac1{b-a}$, $F=\tfrac{x-a}{b-a}$, mean $\tfrac{a+b}2$, variance
$\tfrac{(b-a)^2}{12}$. The module closes with the **discrete→continuous bridge**: a
point mass is the $\varepsilon\to0$ limit of a narrow box density, i.e. a **Dirac
delta** $\delta(x-c)$ (`~MA-15`), with mean $\to c$ and variance $\to0$.

## Operations — `code/continuous_rv.py`

| call | meaning | reference |
|------|---------|-----------|
| `_integrate(f, a, b, n)` | composite midpoint $\int_a^b f$ (continuous-check helper) | L14.1 |
| `pdf_is_normalized(f, a, b)` | total-probability axiom $\int_a^b f=1$ | L14.1 |
| `cdf_from_pdf(f, x, a)` | $F(x)=\int_{a}^{x}f(t)\,dt$ (the cdf as accumulated area) | L14.2 |
| `prob_between(f, lo, hi)` | $P(lo<X<hi)=\int_{lo}^{hi}f=F(hi)-F(lo)$; $P(X{=}c)=0$ | L14.2 |
| `expectation_continuous(f, a, b)` | $E[X]=\int_a^b x\,f(x)\,dx$ | L14.3 |
| `expectation_of(g, f, a, b)` | LOTUS $E[g(X)]=\int g(x)f(x)\,dx$ | L14.3 |
| `moment_continuous(f, a, b, k)` | $E[X^k]=\int x^k f\,dx$ | L14.3 |
| `variance_continuous(f, a, b)` | $\operatorname{Var}[X]=E[X^2]-(E[X])^2$ | L14.3 |
| `quantile(F, p, lo, hi)` | $100p$-th percentile: solve $F(\pi_p)=p$ (bisection) | L13; L14.4 |
| `median_continuous(F, lo, hi)` | median $=$ $0.5$-quantile, $F=\tfrac12$ | L13 |
| `uniform_pdf/uniform_cdf(x, a, b)` | $U(a,b)$: $f=\tfrac1{b-a}$, $F=\tfrac{x-a}{b-a}$ | L14.6 |
| `uniform_mean/uniform_var(a, b)` | $\tfrac{a+b}2$, $\tfrac{(b-a)^2}{12}$ | L14.6 |
| `uniform_quantile(p, a, b)` | $a+p(b-a)$ (closed-form cdf inverse) | L14.6 |
| `point_mass_pdf(x, c, eps)` | box density $\to\delta(x-c)$ as $\varepsilon\to0$ (`~MA-15`) | L14.1; `~MA-15` |

## Use
```python
from continuous_rv import (uniform_pdf, uniform_cdf, uniform_mean, uniform_var,
                           expectation_continuous, variance_continuous,
                           prob_between, quantile, cdf_from_pdf)

a, b = 2.0, 8.0
f = lambda x: uniform_pdf(x, a, b)
F = lambda x: uniform_cdf(x, a, b)

uniform_mean(a, b), uniform_var(a, b)        # 5.0, 3.0   = (a+b)/2, (b-a)^2/12
expectation_continuous(f, a, b)              # 5.0        E[X] = int x f
variance_continuous(f, a, b)                 # 3.0        int x^2 f - mean^2
prob_between(f, 3.0, 5.0)                     # 0.333...   = F(5)-F(3)
prob_between(f, 5.0, 5.0)                     # 0.0        P(X=c)=0
quantile(F, 0.25, a, b)                       # 3.5        25th percentile
cdf_from_pdf(lambda x: 2*x, 0.5, 0.0)         # 0.25       F(x)=x^2 at x=1/2
```

## Run
```bash
cd code
python3 continuous_rv.py        # demo: uniform mean/var/percentiles, f=2x, the delta limit
python3 test_continuous_rv.py   # tests  ->  "All 10 tests passed."
```

## Files
- `notes.md` — pdf/cdf axioms → $f=F'$ and $P(X{=}x)=0$ → expectation/variance as
  integrals → percentiles by inverting $F$ → the uniform $U(a,b)$ → the
  discrete→continuous (point-mass / Dirac-delta) bridge; each result tied to a code symbol
- `code/continuous_rv.py`, `code/test_continuous_rv.py` (stdlib `math` only, self-contained)
- `problems/problems.md` — worked problems (STAT 414 L13–L14; numerical cross-checks to the code)
- `refs.md` — citation table (STAT 414 OER primary; Hogg–Tanis–Zimmerman, Wackerly, Ross cross-cited)
