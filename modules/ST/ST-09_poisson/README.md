# ST-09 — The Poisson Distribution

Ninth module of the **PROBABILITY THEORY** trunk (see `modules/list_ST.txt`), a
faithful module-by-module replica of Penn State's **STAT 414**. Covers
**Lesson 12, "The Poisson Distribution."** The Poisson is the distribution of a
*count* — how many independent, rare events fall in a fixed window of time or
space — and it arises two ways at once: as the $n\to\infty,\,p\to0,\,np\to\lambda$
limit of the binomial (`~ST-07`) and as the increment law of the **Poisson
process**.

- **Prerequisites:** `~ST-07` (the binomial distribution — the Poisson is its
  *law of rare events* limit), `~ST-05` (discrete random variables, $E[X]$ and
  $\mathrm{Var}(X)$ from a pmf), `~ST-06` (moment-generating functions — $M(t)$
  and the uniqueness theorem that powers the additivity proof). Helpful: `~ST-02`
  (the $\binom{n}{k}$ and $e^x$ series the derivations lean on).
- **Cross-links:** `~ST-08` (geometric / negative binomial — the other discrete
  count/waiting-time laws), `~ST-11` (exponential & gamma — the *interarrival*
  and *arrival-time* side of the same Poisson process), `~ST-18` (the central
  limit theorem — Poisson$(\lambda)\to$ normal as $\lambda\to\infty$),
  `~QO-01` (photon counting: a coherent beam has **Poissonian** photon
  statistics, $\mathrm{Var}(n)=\langle n\rangle$), `~PK-04` (collision / reaction
  event counts in plasma kinetics), `~SM-01` (counting and the rare-event limit).

## Scope
A **Poisson random variable** $X\sim\mathrm{Poisson}(\lambda)$ has pmf
$$P(X=k)=\frac{e^{-\lambda}\lambda^{k}}{k!},\qquad k=0,1,2,\dots,\ \ \lambda>0.$$
The series $\sum_k \lambda^k/k!=e^{\lambda}$ makes it sum to one. Its single
parameter is simultaneously the **mean and the variance**,
$E[X]=\mathrm{Var}(X)=\lambda$ — the Poisson signature, and the source of the
photon-shot-noise rule $\sigma_n=\sqrt{\langle n\rangle}$ in `~QO-01`. The
**moment-generating function** $M(t)=\exp\!\big(\lambda(e^{t}-1)\big)$ delivers
every moment by differentiation (`~ST-06`) and, through the uniqueness theorem,
two structural facts in one stroke: the **law of rare events** — the binomial
$\mathrm{Bin}(n,p)$ with $np=\lambda$ held fixed converges to $\mathrm{Poisson}(\lambda)$
as $n\to\infty$ (`~ST-07`) — and the **reproductive property** — a sum of
independent Poissons is Poisson, $\sum_i X_i\sim\mathrm{Poisson}(\sum_i\lambda_i)$.
The same $\lambda$ counts events of a **Poisson process** over an interval of
length $t$ (rate $\lambda=\nu t$); its waiting times are exponential/gamma
(`~ST-11`), a link the code checks numerically via the
$P(X\le k-1)=\int_\lambda^\infty t^{k-1}e^{-t}/(k-1)!\,dt$ identity.

## Operations — `code/poisson.py`

| call | meaning | reference |
|------|---------|-----------|
| `poisson_pmf(k, lam)` | $P(X=k)=e^{-\lambda}\lambda^{k}/k!$ (log-form, stable) | L12.1 |
| `poisson_cdf(k, lam)` | $F(k)=\sum_{j=0}^{\lfloor k\rfloor}e^{-\lambda}\lambda^{j}/j!$ | L12.1 |
| `poisson_normalization(lam, kmax)` | $\sum_{k=0}^{k_{\max}}P(X=k)\to1$ | L12.1 |
| `poisson_mean(lam)` | $E[X]=\lambda$ | L12.2 |
| `poisson_var(lam)` | $\mathrm{Var}(X)=\lambda$ ($=$ mean) | L12.2 |
| `poisson_std(lam)` | $\sigma=\sqrt{\lambda}$ | L12.2 |
| `poisson_skewness(lam)` | $\mu_3/\sigma^{3}=1/\sqrt{\lambda}$ | L12.2 |
| `poisson_excess_kurtosis(lam)` | $\mu_4/\sigma^{4}-3=1/\lambda$ | L12.2 |
| `poisson_mode(lam)` | $\lfloor\lambda\rfloor$ (argmax of the pmf) | L12.1 |
| `poisson_mgf(t, lam)` | $M(t)=\exp\!\big(\lambda(e^{t}-1)\big)$ | L12.2; `~ST-06` |
| `poisson_pgf(s, lam)` | $G(s)=\exp\!\big(\lambda(s-1)\big)$, $G^{(r)}(1)=\lambda^{r}$ | L12.2 |
| `poisson_factorial_moment(r, lam)` | $E[X(X-1)\cdots(X-r+1)]=\lambda^{r}$ | L12.2 |
| `binomial_pmf(k, n, p)` | $\binom{n}{k}p^{k}(1-p)^{n-k}$ (`~ST-07`) | L12.1 |
| `poisson_limit_of_binomial(n, p)` | $\max_k\lvert\mathrm{Bin}(n,p)-\mathrm{Poisson}(np)\rvert$ (law of rare events) | L12.1; `~ST-07` |
| `sum_of_poissons(lams)` | $\lambda_{\text{tot}}=\sum_i\lambda_i$ (additivity) | L12.2 |
| `poisson_convolution_pmf(k, l1, l2)` | $\sum_j P(X_1{=}j)P(X_2{=}k{-}j)=\mathrm{Poisson}(l_1{+}l_2)$ | L12.2 |

## Use
```python
from poisson import (poisson_pmf, poisson_mean, poisson_var, poisson_mgf,
                     poisson_limit_of_binomial, poisson_convolution_pmf)

poisson_pmf(0, 3.0)                      # 0.049787  = e^-3
poisson_pmf(2, 3.0)                      # 0.224042  = e^-3 * 3^2/2!
poisson_mean(4.0), poisson_var(4.0)      # (4.0, 4.0)   mean = variance = lambda
poisson_mgf(0.0, 5.0)                    # 1.0          M(0) = 1 always
poisson_limit_of_binomial(100, 0.02)     # 0.002743     Bin(100,0.02) ~ Poisson(2)
poisson_convolution_pmf(4, 3.0, 4.0)     # 0.091226  == poisson_pmf(4, 7.0)
```

## Run
```bash
cd code
python3 poisson.py          # demo: pmf bar chart, mean=var, mgf moments, rare-events limit, additivity
python3 test_poisson.py     # tests  ->  "All 13 tests passed."
```

## Files
- `notes.md` — pmf & normalization → mean/variance from the series → mgf and its
  moments → law of rare events (binomial limit) → the Poisson process →
  additivity; each result tied to a code symbol, with a "Where this goes" map.
- `code/poisson.py`, `code/test_poisson.py` (numpy + stdlib only, self-contained).
- `problems/problems.md` — 8 worked problems (STAT 414 L12; numeric `*Check:*`
  against the code).
- `refs.md` — STAT 414 OER (primary, lesson-level) + Hogg–Tanis–Zimmerman,
  Wackerly, and Ross at chapter level.
