# ST-08 — Geometric & Negative Binomial Distributions

Eighth module of the **PROBABILITY THEORY** trunk (Penn State STAT 414; see
`modules/ST/list_ST.txt`). It covers **Lesson 11** (Geometric and Negative
Binomial Distributions). Where `~ST-07` fixes the number of Bernoulli$(p)$ trials
$n$ and counts the **successes**, this module fixes the number of successes and
counts the **trials** — the two *discrete waiting-time* distributions.

- **Prerequisites:** `~ST-07` (Bernoulli trials and the binomial distribution —
  the same independent $p$-coin, here read "the other way round"), `~ST-05`
  (discrete random variables: pmf/cdf, $E[X]$, $\operatorname{Var}(X)$), `~ST-06`
  (moment-generating functions — $M(t)=E[e^{tX}]$, moments by differentiation,
  uniqueness).
- **Cross-links:** `~ST-09` (Poisson — the *next* waiting-count distribution, and
  the limit of the negative binomial), `~ST-11` (exponential & gamma — the
  **continuous** analogues: the exponential is memoryless like the geometric, the
  gamma is a sum of exponentials like the negative binomial is a sum of
  geometrics), `~ST-02` (counting — the $\binom{x-1}{r-1}$ in the negative-binomial
  pmf), `~MA-19` (probability foundations the whole trunk deep-dives).

## Scope
A sequence of independent **Bernoulli$(p)$** trials. The **geometric** random
variable $X$ is the number of trials up to and including the **first success**,
with pmf $f(x)=(1-p)^{x-1}p$ on $x=1,2,3,\dots$ (the geometric series guarantees
$\sum f=1$). Its mean is $E[X]=1/p$ and variance $\operatorname{Var}(X)=(1-p)/p^2$,
and its survival function is the clean $P(X>x)=(1-p)^x$, which gives the
**memoryless property** $P(X>m+n\mid X>m)=P(X>n)$ — the geometric is the *unique*
discrete distribution with no memory of past failures. The **negative binomial**
random variable counts the trials to the **$r$-th success**, pmf
$f(x)=\binom{x-1}{r-1}(1-p)^{x-r}p^r$ on $x=r,r+1,\dots$, with mean $r/p$ and
variance $r(1-p)/p^2$. Two structural facts tie them together: the geometric is
exactly the negative binomial with **$r=1$**, and a **sum of $r$ i.i.d.
geometrics** is negative binomial$(r,p)$ — its mgf is the geometric mgf raised to
the $r$. The module closes on the continuous limit: as $p\to0$ the geometric
becomes the **exponential** ($\sim$`~ST-11`), the only memoryless continuous law.

## Operations — `code/geometric_negbinomial.py`  (trials convention, support $\ge 1$)

| call | meaning | reference |
|------|---------|-----------|
| `geometric_pmf(x, p)` | $f(x)=(1-p)^{x-1}p$, trials to first success ($x=1,2,\dots$) | STAT 414 L11 |
| `geometric_cdf(x, p)` | $P(X\le x)=1-(1-p)^{\lfloor x\rfloor}$ | STAT 414 L11 |
| `geometric_sf(x, p)` | survival $P(X>x)=(1-p)^{\lfloor x\rfloor}$ (the memoryless tail) | STAT 414 L11 |
| `geometric_mean(p)` | $E[X]=1/p$ | STAT 414 L11 |
| `geometric_var(p)` | $\operatorname{Var}(X)=(1-p)/p^2$ | STAT 414 L11 |
| `geometric_mgf(t, p)` | $M(t)=\dfrac{pe^t}{1-(1-p)e^t}$, $t<-\ln(1-p)$ | STAT 414 L9, L11; `~ST-06` |
| `memoryless_check(m, n, p)` | $\big(P(X>m+n\mid X>m),\,P(X>n)\big)$ — equal | STAT 414 L11 |
| `negbinom_pmf(x, r, p)` | $f(x)=\binom{x-1}{r-1}(1-p)^{x-r}p^r$, trials to $r$-th success | STAT 414 L11; `~ST-02` |
| `negbinom_mean(r, p)` | $E[X]=r/p$ ($=r\times$ geometric mean) | STAT 414 L11 |
| `negbinom_var(r, p)` | $\operatorname{Var}(X)=r(1-p)/p^2$ ($=r\times$ geometric var) | STAT 414 L11 |
| `negbinom_mgf(t, r, p)` | $M(t)=\Big(\dfrac{pe^t}{1-(1-p)e^t}\Big)^r$ = geometric mgf$^{\,r}$ | STAT 414 L11; `~ST-06` |

## Use
```python
from geometric_negbinomial import (geometric_pmf, geometric_mean, geometric_var,
    geometric_sf, memoryless_check, negbinom_pmf, negbinom_mean, negbinom_mgf,
    geometric_mgf)

geometric_pmf(1, 0.5), geometric_pmf(3, 0.5)   # 0.5, 0.125     (1-p)^{x-1} p
geometric_mean(0.25), geometric_var(0.25)      # 4.0, 12.0       1/p, (1-p)/p^2
geometric_sf(5, 0.25)                          # 0.2373...       P(X>5)=(1-p)^5
memoryless_check(10, 4, 0.25)                  # (0.3164, 0.3164) equal -> no memory
negbinom_pmf(5, 3, 0.25)                       # 0.0527          C(4,2)(.75)^2(.25)^3
negbinom_mean(3, 0.25), negbinom_pmf(7, 1, 0.25) == geometric_pmf(7, 0.25)  # 12.0, True
negbinom_mgf(0.1, 3, 0.25) == geometric_mgf(0.1, 0.25)**3                    # True
```

## Run
```bash
cd code
python3 geometric_negbinomial.py        # demo: pmf, mean/var, memoryless, r=1 and sum relations
python3 test_geometric_negbinomial.py   # tests  ->  "All 14 tests passed."
```

## Files
- `notes.md` — geometric series → pmf/cdf; mean & variance from the series and
  from the mgf; the memoryless property and its uniqueness; negative-binomial pmf
  by counting; mean/variance; geometric $=$ negbinom$(r{=}1)$; sum-of-geometrics;
  the exponential continuous limit; a "Where this goes" map.
- `code/geometric_negbinomial.py`, `code/test_geometric_negbinomial.py`
  (stdlib `math` only; numpy used solely for the convolution test).
- `problems/problems.md` — worked problems (STAT 414 L11; each with a numerical
  `*Check:*` against the code).
- `refs.md` — citation table (STAT 414 OER **primary** by lesson; Hogg, Tanis &
  Zimmerman cross-cited at chapter level).
