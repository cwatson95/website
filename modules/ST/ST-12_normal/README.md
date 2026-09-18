# ST-12 — The Normal Distribution

Twelfth module of the **PROBABILITY THEORY** trunk (see `modules/ST/list_ST.txt`),
a module-by-module replica of Penn State **STAT 414**. Covers **Lesson 16 — Normal
Distributions**. The normal (Gaussian) is the single most important continuous
distribution: the limit shape of sums (`~ST-18`), the law of thermodynamic
fluctuations (`~SM-01`), and the minimum-uncertainty wavepacket of quantum
mechanics (`~QM-07`).

- **Prerequisites:** `~ST-10` (continuous random variables — pdf, cdf, percentiles;
  the normal is one of them), `~ST-06` (moment-generating functions — we read the
  mean and variance off $M(t)$), `~ST-11` (the gamma family, where the normalizing
  $\Gamma(\tfrac12)=\sqrt\pi$ lives), `~MA-19` (the trunk's parent probability survey).
- **Cross-links:** `~SM-01` (statistical-mechanics fluctuations are Gaussian — the
  de Moivre–Laplace limit of the two-state system), `~QM-07` (the
  minimum-uncertainty Gaussian wavepacket saturating $\Delta x\,\Delta p=\hbar/2$),
  `~ST-18` (the **central limit theorem** — why the normal is universal), `~ST-07`
  (the binomial it approximates), `~ST-15` (the bivariate normal), `~MA-10`
  (the Laplace/Fourier transforms behind the mgf and characteristic function).

## Scope
A continuous random variable is **normal**, $X\sim N(\mu,\sigma^2)$, when its
density is the **Gaussian bell**
$$f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\!\Big(-\frac{(x-\mu)^2}{2\sigma^2}\Big).$$
The $\sqrt{2\pi}$ is the **Gaussian integral** $\int_{-\infty}^\infty e^{-x^2/2}\,dx
=\sqrt{2\pi}$, which makes $f$ integrate to one. **Standardizing**
$Z=(X-\mu)/\sigma$ collapses every normal onto the one **standard normal**
$N(0,1)$, whose cdf is written through the error function,
$\Phi(z)=\tfrac12\big[1+\operatorname{erf}(z/\sqrt2)\big]$. The first two moments
are $E[X]=\mu$ and $\operatorname{Var}[X]=\sigma^2$; the
**moment-generating function** is $M(t)=\exp(\mu t+\tfrac12\sigma^2t^2)$, from which
both moments fall out by differentiation at $t=0$. The symmetric tail areas give
the **68–95–99.7 rule** $P(|Z|\le k)=2\Phi(k)-1$, and inverting $\Phi$ by
bisection yields the **probit / quantile** $x_p=\mu+\sigma\,\Phi^{-1}(p)$. The
module closes by tying the Gaussian to its three big appearances: the CLT
(`~ST-18`), thermodynamic fluctuations (`~SM-01`), and the quantum wavepacket
(`~QM-07`).

## Operations — `code/normal.py`  (pure `numpy` + `math`)

| call | meaning | reference |
|------|---------|-----------|
| `normal_pdf(x, mu, sigma)` | $f(x)=\dfrac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}$ | L16.1 |
| `standard_normal_pdf(z)` | $\varphi(z)=\dfrac{1}{\sqrt{2\pi}}e^{-z^2/2}$ | L16.1 |
| `standardize(x, mu, sigma)` | $z=(x-\mu)/\sigma$ (the $Z$-score) | L16.2 |
| `standard_normal_cdf(z)` | $\Phi(z)=\tfrac12\big[1+\operatorname{erf}(z/\sqrt2)\big]$ | L16.3 |
| `normal_cdf(x, mu, sigma)` | $F(x)=\Phi\big((x-\mu)/\sigma\big)$ | L16.3 |
| `normal_interval_prob(a, b, mu, sigma)` | $P(a<X\le b)=F(b)-F(a)$ | L16.3 |
| `gaussian_integral_check()` | numeric $\int e^{-x^2/2}dx\to\sqrt{2\pi}$ | L16.1 |
| `normal_mean_by_integration(mu, sigma)` | $E[X]=\int x\,f\,dx\to\mu$ | L16.1 |
| `normal_variance_by_integration(mu, sigma)` | $\operatorname{Var}=\int(x-\mu)^2 f\,dx\to\sigma^2$ | L16.1 |
| `normal_mgf(t, mu, sigma)` | $M(t)=e^{\mu t+\sigma^2 t^2/2}$ | L16.1 |
| `mgf_moment(k, mu, sigma)` | $E[X^k]=M^{(k)}(0)$ by finite difference | L16.1; `~ST-06` |
| `probit(p)` | $\Phi^{-1}(p)$ by bisection | L16.3 |
| `normal_quantile(p, mu, sigma)` | $x_p=\mu+\sigma\,\Phi^{-1}(p)$ | L16.3 |
| `empirical_rule(k)` | $P(|Z|\le k)=2\Phi(k)-1$ (68–95–99.7) | L16.2 |

## Use
```python
import numpy as np
from normal import (normal_pdf, standard_normal_cdf, normal_cdf, normal_mgf,
                    mgf_moment, probit, normal_quantile, empirical_rule)

float(normal_pdf(0.0, 0.0, 1.0))          # 0.3989422804  = 1/sqrt(2 pi), the peak
float(standard_normal_cdf(1.96))          # 0.9750021049  -> 1.96 is the 97.5% point
1 - float(normal_cdf(130, 100, 15))       # 0.0227501319  P(IQ > 130) for N(100,15^2)
float(normal_mgf(0.0, 3.0, 2.0))          # 1.0           M(0)=1 always
mgf_moment(2, 3.0, 2.0)                    # 13.0000...    E[X^2]=mu^2+sigma^2
probit(0.975)                             # 1.9599639845  Phi^{-1}(0.975)
normal_quantile(0.90, 500, 100)           # 628.155...    90th percentile of N(500,100^2)
[round(empirical_rule(k), 4) for k in (1,2,3)]   # [0.6827, 0.9545, 0.9973]
```

## Run
```bash
cd code
python3 normal.py          # demo: Gaussian integral, Phi, mean/var, mgf, 68-95-99.7, probit
python3 test_normal.py     # tests  ->  "All 11 tests passed."
```

## Files
- `notes.md` — Gaussian integral → normalized pdf → standardization → $\Phi$ via
  $\operatorname{erf}$ → mean, variance, mgf → 68–95–99.7 → probit; the bridges to
  `~SM-01`, `~QM-07`, `~ST-18`.
- `code/normal.py`, `code/test_normal.py` (`numpy` + `math` only, self-contained).
- `problems/problems.md` — worked problems (STAT 414 L16; each with a numeric check
  against the code).
- `refs.md` — citation table (STAT 414 L16 primary; Hogg–Tanis–Zimmerman Ch. 5
  cross-cited at chapter level).
