# ST-05 — Discrete Random Variables & Expectation

Fifth module of the **PROBABILITY THEORY** trunk (Penn State STAT 414 replica;
see `modules/ST/list_ST.txt`). Covers **STAT 414 Lesson 7** (Discrete Random
Variables) and **Lesson 8** (Mathematical Expectation): the pmf and cdf of a
discrete random variable, and the expectation operator $E[\cdot]$ that turns a
distribution into its mean, variance, and moments.

- **Prerequisites:** `~ST-01` (sample spaces & the probability axioms — $P$ is
  the law $X$ pushes forward to its pmf), `~ST-03` (conditional probability &
  independence — used implicitly when atoms are combined), `~MA-19` (binomial /
  normal distributions and sample moments — the empirical analogues of the
  population $\mu,\sigma^2$ defined here).
- **Cross-links:** `~QM-06` (the quantum expectation value
  $\langle A\rangle=\sum_a a\,|c_a|^2$ and variance
  $\sigma_A^2=\langle A^2\rangle-\langle A\rangle^2$ — *literally* the formulas of
  this module with $f(x)=|c_a|^2$), `~SM-01` (the statistical-mechanics ensemble
  average $\langle\cdot\rangle=\sum_i(\cdot)P_i$ — Boltzmann weights are a pmf),
  `~ST-06` (the moment-generating function $M(t)=E[e^{tX}]$, previewed here and
  developed there), `~ST-07`/`~ST-08`/`~ST-09` (the named discrete distributions
  whose $\mu,\sigma^2$ this machinery computes).

## Scope
A **discrete random variable** $X$ assigns a real number to each outcome of a
sample space and takes values in a countable **support** $S_X$. Its law is the
**probability mass function** $f(x)=P(X=x)$, a valid pmf iff $f(x)\ge 0$ and
$\sum_x f(x)=1$. The **cumulative distribution function**
$F(x)=P(X\le x)=\sum_{x_i\le x}f(x_i)$ is a right-continuous **step function** that
jumps by $f(x)$ at each support point and climbs from $0$ to $1$. The **law of the
unconscious statistician (LOTUS)** computes the expectation of *any* function
without first finding its law: $E[g(X)]=\sum_x g(x)\,f(x)$. Specializing $g$ gives
the **mean** $\mu=E[X]$, the **variance** $\sigma^2=E[(X-\mu)^2]=E[X^2]-\mu^2$, the
**standard deviation** $\sigma$, and the **raw / central moments**
$\mu'_k=E[X^k]$, $\mu_k=E[(X-\mu)^k]$. Expectation is a **linear operator**:
$E[aX+b]=aE[X]+b$ and $\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$. The same weighted
sum is the quantum expectation value $\langle A\rangle=\sum_a a|c_a|^2$ (`~QM-06`)
and the thermodynamic ensemble average (`~SM-01`); the module closes with a
one-line preview of the moment-generating function (`~ST-06`).

## Operations — `code/discrete_rv_expectation.py`

| call | meaning | reference |
|------|---------|-----------|
| `pmf_is_valid(values, probs)` | check $f(x)\ge 0$, $\sum_x f(x)=1$, atoms distinct | PSU L7 |
| `support(values, probs)` | $S_X=\{x:f(x)>0\}$ (drop zero-mass atoms) | PSU L7 |
| `cdf_from_pmf(values, probs)` | step cdf $F(x)=P(X\le x)=\sum_{x_i\le x}f(x_i)$ | PSU L7 |
| `cdf_table(values, probs)` | sorted atoms and cumulative $F(x_i)$ after each jump | PSU L7 |
| `expectation(values, probs)` / `mean` | $\mu=E[X]=\sum_x x\,f(x)$ | PSU L8; `~QM-06` |
| `expectation_of(g, values, probs)` / `lotus` | LOTUS $E[g(X)]=\sum_x g(x)\,f(x)$ | PSU L8 |
| `raw_moment(values, probs, k)` | $\mu'_k=E[X^k]$ ($\mu'_0=1$, $\mu'_1=\mu$) | PSU L8 |
| `central_moment(values, probs, k)` | $\mu_k=E[(X-\mu)^k]$ ($\mu_1=0$, $\mu_2=\sigma^2$) | PSU L8 |
| `variance(values, probs)` | $\sigma^2=E[X^2]-\mu^2$ (computational formula) | PSU L8; `~QM-06` |
| `std(values, probs)` | $\sigma=\sqrt{\mathrm{Var}(X)}$ | PSU L8 |
| `standardize(values, probs)` | $Z=(X-\mu)/\sigma$; $E[Z]=0,\ \mathrm{Var}(Z)=1$ | PSU L8 |
| `skewness(values, probs)` | $\gamma_1=\mu_3/\sigma^3$ ($=0$ if symmetric) | PSU L8 |
| `excess_kurtosis(values, probs)` | $\gamma_2=\mu_4/\sigma^4-3$ | PSU L8 |
| `linear_transform(a, b, values, probs)` | the affine image $Y=aX+b$ | PSU L8 |
| `survival(values, probs)` / `mean_via_survival` | $S(x)=1-F(x)$; $E[X]=\sum_{k\ge0}S(k)$ | PSU L8 |
| `mgf(values, probs, t)` | $M(t)=E[e^{tX}]$ (preview of `~ST-06`) | PSU L9 |

## Use
```python
import numpy as np
from discrete_rv_expectation import (expectation, variance, std, expectation_of,
                                     linear_transform, cdf_from_pmf, mgf)

x = np.arange(1, 7); p = np.full(6, 1/6)      # a fair six-sided die
expectation(x, p)                              # 3.5          mu = 7/2
variance(x, p)                                 # 2.9166...    sigma^2 = 35/12
std(x, p)                                      # 1.7078       sigma
expectation_of(lambda t: (t-3.5)**2, x, p)     # 2.9166...    LOTUS == variance
cdf_from_pmf(x, p)(3.0)                         # 0.5          P(X <= 3) = 3/6

cx = np.array([-1., 0., 2.]); cp = np.array([.2, .5, .3])
yx, yp = linear_transform(3.0, -4.0, cx, cp)   # Y = 3X - 4
expectation(yx, yp)                            # -2.8 = 3*E[X] - 4   (linearity)
variance(yx, yp)                               # 11.16 = 9*Var(X)    (a^2 scaling)
```

## Run
```bash
cd code
python3 discrete_rv_expectation.py        # demo: die mean/var, LOTUS, linearity, mgf
python3 test_discrete_rv_expectation.py   # tests  ->  "All 10 tests passed."
```

## Files
- `notes.md` — pmf → cdf step function → LOTUS → mean → variance (computational
  formula) → raw/central moments & skewness → linearity → mgf preview; the
  `~QM-06` / `~SM-01` bridge
- `code/discrete_rv_expectation.py`, `code/test_discrete_rv_expectation.py`
  (numpy + stdlib only, self-contained)
- `problems/problems.md` — worked problems (STAT 414 L7–L8; numerical checks to the code)
- `refs.md` — citation table (STAT 414 OER primary, by lesson; Hogg–Tanis–Zimmerman
  cross-cited at chapter level)
