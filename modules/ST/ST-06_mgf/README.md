# ST-06 — Moment-Generating Functions

Sixth module of the **PROBABILITY THEORY** trunk (see `modules/topic_network.txt`),
a module-by-module replica of Penn State's **STAT 414**. Covers **Lesson 9,
Moment Generating Functions**. This is the trunk's single most reusable tool: one
function $M(t)=E[e^{tX}]$ that encodes *all* the moments of $X$, turns sums of
independent variables into products, and (by uniqueness) pins down the
distribution itself.

- **Prerequisites:** `~ST-05` (discrete random variables, $E[X]$, variance,
  raw moments $E[X^k]$ — the quantities the mgf generates), `~ST-02` (counting,
  for the binomial coefficients), `~MA-08`/`~MA-13` (Taylor series & differentiation
  — the mgf *is* the exponential generating function of the moments).
- **Cross-links:** `~MA-10` (the mgf is the two-sided **Laplace transform** of the
  density read at $s=-t$; uniqueness = invertibility of that transform),
  `~SM-03` (the **partition function** $Z(\beta)$ is the mgf of the energy and
  $\ln Z$ generates its cumulants — exactly the $K(t)=\ln M(t)$ of §6),
  `~ST-17` (the **mgf technique**: identify the distribution of a sum/transform by
  recognizing its mgf — the payoff of uniqueness), and forward to `~ST-07`/`~ST-09`/
  `~ST-11`/`~ST-12` (binomial, Poisson, gamma, normal — each derived through its mgf)
  and `~ST-18` (the mgf proof of the **central limit theorem**).

## Scope
For a random variable $X$ the **moment-generating function** is
$M(t)=E[e^{tX}]$, a sum $\sum_x e^{tx}p(x)$ (discrete) or integral
$\int e^{tx}f(x)\,dx$ (continuous), defined on the open $t$-interval about $0$
where it converges. Three theorems do the work. (1) **Moments by
differentiation:** $M(t)=\sum_k E[X^k]\,t^k/k!$, so $M^{(k)}(0)=E[X^k]$; in
particular $\mu=M'(0)$ and $\sigma^2=M''(0)-[M'(0)]^2$. (2) **Sums multiply:**
for independent $X,Y$, $M_{X+Y}(t)=M_X(t)M_Y(t)$ — the mgf converts convolution
into a product. (3) **Uniqueness:** an mgf that exists near $0$ *determines* the
distribution. The **cumulant generating function** $K(t)=\ln M(t)$ gives
$K'(0)=\mu$, $K''(0)=\sigma^2$, and cumulants of an independent sum add — the same
object as the statistical-mechanics $\ln Z(\beta)$ (`~SM-03`). The code builds the
mgf by summation/quadrature, extracts moments and cumulants by accurate central
differences at $0$, and verifies the product rule and the closed-form mgfs of the
Bernoulli, binomial, Poisson, geometric, exponential, gamma and normal laws.

## Operations — `code/mgf.py`  (numpy + stdlib only)

| call | meaning | reference |
|------|---------|-----------|
| `mgf(t, values, probs)` | $M(t)=\sum_x e^{tx}p(x)$ | L9.1 |
| `cgf(t, values, probs)` | $K(t)=\ln M(t)$ (cumulant generator) | L9; `~SM-03` |
| `mean(values, probs)` / `variance(...)` | direct $E[X]=\sum x\,p(x)$, $\mathrm{Var}\,X$ — the `~ST-05` ground truth | L8 |
| `mean_from_mgf(values, probs)` | $\mu=M'(0)$ | L9.2 |
| `var_from_mgf(values, probs)` | $\sigma^2=M''(0)-[M'(0)]^2$ | L9.2 |
| `moment_from_mgf(k, values, probs)` | $E[X^k]=M^{(k)}(0)$ (central stencil) | L9.2 |
| `cumulant_from_mgf(k, values, probs)` | $\kappa_k=K^{(k)}(0)$; $\kappa_1=\mu,\ \kappa_2=\sigma^2$ | L9; `~SM-03` |
| `mgf_of_sum(t, dists)` | $M_{\sum X_i}(t)=\prod_i M_{X_i}(t)$ | L9.3 |
| `convolve_dists(d1, d2)` | distribution of $X+Y$ (independent); its mgf $=$ the product | L9.3; `~ST-16` |
| `mgf_continuous(t, pdf, a, b)` | $M(t)=\int_a^b e^{tx}f(x)\,dx$ by quadrature (Laplace view) | L9.1; `~MA-10` |
| `bernoulli_mgf(t,p)` | $(1-p)+pe^t$ | L9; `~ST-07` |
| `binomial_mgf(t,n,p)` | $((1-p)+pe^t)^n$ | L9; `~ST-07` |
| `poisson_mgf(t,\lambda)` | $\exp(\lambda(e^t-1))$ | L9; `~ST-09` |
| `geometric_mgf(t,p)` | $pe^t/(1-(1-p)e^t)$ | L9; `~ST-08` |
| `exponential_mgf(t,\lambda)` / `gamma_mgf(t,\alpha,\lambda)` | $\lambda/(\lambda-t)$, $(\lambda/(\lambda-t))^\alpha$ | L9; `~ST-11` |
| `normal_mgf(t,\mu,\sigma)` | $\exp(\mu t+\tfrac12\sigma^2t^2)$ | L9; `~ST-12` |
| `bernoulli_dist`/`binomial_dist`/`poisson_dist`/`geometric_dist` | `(values, probs)` builders for the numeric machinery | L10–L11 |

## Use
```python
import math
from mgf import (binomial_dist, mean_from_mgf, var_from_mgf, moment_from_mgf,
                 cumulant_from_mgf, poisson_dist, poisson_mgf,
                 mgf, mgf_of_sum, convolve_dists, bernoulli_dist, normal_mgf)

d = binomial_dist(10, 0.3)
mean_from_mgf(*d), var_from_mgf(*d)        # 3.0, 2.1   = np, np(1-p)   (M'(0), M''(0)-M'(0)^2)

dp = poisson_dist(2.0)
[cumulant_from_mgf(k, *dp) for k in (1, 2, 3)]   # ~[2,2,2]: every Poisson cumulant = lambda

# mgf of a sum of independents is the product (convolution theorem):
b = bernoulli_dist(0.4)
mgf_of_sum(0.5, [b, b]) == mgf(0.5, *convolve_dists(b, b))    # True

# closed-form additivity of the normal (uniqueness => the sum is normal):
normal_mgf(0.3, 1, 2)*normal_mgf(0.3, -0.5, 1.5) - normal_mgf(0.3, 0.5, math.sqrt(2**2+1.5**2))  # ~0
```

## Run
```bash
cd code
python3 mgf.py            # demo: M(0)=1, moments/cumulants by differentiation, convolution theorem, Laplace view
python3 test_mgf.py       # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — definition → Taylor/moment series → moments & variance by
  differentiation → product rule for sums → uniqueness → cumulants & the
  $\ln Z$ / Laplace-transform bridges; a catalogue of closed-form mgfs
- `code/mgf.py`, `code/test_mgf.py` (numpy + stdlib, self-contained)
- `problems/problems.md` — worked problems (STAT 414 L9; cross-checks to the code)
- `refs.md` — citation table (STAT 414 OER primary; Hogg–Tanis–Zimmerman, Wackerly,
  Ross at chapter level)
