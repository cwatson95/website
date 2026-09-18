# ST-07 — The Binomial Distribution

Lesson 10 of the **PROBABILITY THEORY** trunk (a module-by-module replica of
Penn State's STAT 414; see `modules/ST/list_ST.txt`). This is the first *named*
discrete distribution: count the successes in $n$ independent **Bernoulli trials**
and you get the **binomial** $X\sim\mathrm{Bin}(n,p)$. It is the workhorse of
discrete probability and the source of two of the most important limits in the
subject — the Poisson "law of rare events" (`~ST-09`) and the normal
de Moivre–Laplace approximation (`~ST-18`).

- **Prerequisites:** `~ST-02` (counting — the binomial coefficient
  $\binom nk=\tfrac{n!}{k!(n-k)!}$ that weights each success pattern),
  `~ST-05` (discrete random variables — pmf/cdf, $E[X]$, $\mathrm{Var}(X)$),
  `~ST-06` (the moment-generating function $M(t)=E[e^{tX}]$ and moments by
  differentiation).
- **Cross-links:** `~ST-08` (geometric / negative binomial — the *waiting-time*
  duals of the same Bernoulli trials), `~ST-09` (Poisson — the $n\to\infty$,
  $np=\lambda$ limit of the binomial), `~ST-18` (the CLT and the normal
  approximation — the $n\to\infty$, $p$ fixed limit), `~SM-01` (the two-state
  paramagnet / coin system: the fair binomial $\mathrm{Bin}(N,\tfrac12)$ and its
  sharp peak), `~MA-19` (binomial & normal distributions in the maths trunk).

## Scope
A **Bernoulli($p$) trial** has two outcomes, success (prob. $p$) and failure
(prob. $q=1-p$), with indicator $X\in\{0,1\}$. Run $n$ of them, **independent and
identically distributed**, and let $X$ count the successes. Because any *one*
arrangement of $k$ successes and $n-k$ failures has probability $p^k q^{n-k}$ and
there are $\binom nk$ such arrangements (`~ST-02`), the **binomial pmf** is
$$P(X=k)=\binom nk p^k(1-p)^{n-k},\qquad k=0,1,\dots,n.$$
The **binomial theorem** $\sum_k\binom nk p^kq^{n-k}=(p+q)^n=1$ makes it a valid
pmf. Writing $X=\sum_{i=1}^n X_i$ as a sum of i.i.d. Bernoulli indicators gives,
by linearity and independence, the **mean** $np$ and **variance** $np(1-p)$, and
makes the **mgf** factor into $M(t)=(q+pe^t)^n$ — whose derivatives at $0$ return
the moments ($M'(0)=np$, $M''(0)-M'(0)^2=np(1-p)$). The same factorization shows
that **independent binomials with a common $p$ add**:
$\mathrm{Bin}(n_1,p)+\mathrm{Bin}(n_2,p)=\mathrm{Bin}(n_1+n_2,p)$. The module
closes by locating the **mode** $\lfloor(n+1)p\rfloor$ and by numerically
exhibiting the two limits the binomial seeds: $\mathrm{Bin}(n,\lambda/n)\to
\mathrm{Poisson}(\lambda)$ (`~ST-09`) and the de Moivre–Laplace
$P(X=k)\approx\frac{1}{\sqrt{2\pi npq}}e^{-(k-np)^2/2npq}$ (`~ST-18`).

## Operations — `code/binomial.py`  ($q\equiv 1-p$)

| call | meaning | reference |
|------|---------|-----------|
| `bernoulli_pmf(k, p)` | $P(X{=}k)=p^k q^{1-k}$, $k\in\{0,1\}$ (the $n{=}1$ atom) | L10; `~ST-05` |
| `bernoulli_mean(p)` / `bernoulli_var(p)` | $E[X]=p$, $\mathrm{Var}(X)=pq$ | L10 |
| `binom_pmf(k, n, p)` | $\binom nk p^k q^{n-k}$ (0 outside $0\le k\le n$) | L10; `~ST-02` |
| `binom_cdf(k, n, p)` | $F(k)=\sum_{j\le k}\binom nj p^j q^{n-j}$ | L10 |
| `binom_mean(n, p)` | $E[X]=np$ | L10 |
| `binom_var(n, p)` / `binom_std(n, p)` | $\mathrm{Var}(X)=npq$, $\sigma=\sqrt{npq}$ | L10 |
| `binom_skewness(n, p)` | $(1-2p)/\sqrt{npq}$ (0 at $p=\tfrac12$) | L10 |
| `binom_mgf(t, n, p)` | $M(t)=(q+pe^t)^n$ | L9–L10; `~ST-06` |
| `binom_pgf(s, n, p)` | $G(s)=E[s^X]=(q+ps)^n$ (factorial moments) | L9–L10 |
| `binom_mode(n, p)` | $\lfloor(n+1)p\rfloor$ (the most likely $k$) | L10 |
| `sum_two_binomials_pmf(k, n1, n2, p)` | convolution $\Rightarrow\mathrm{Bin}(n_1{+}n_2,p)$ | L10 |
| `_deriv1`, `_deriv2`, `_integrate` | numeric derivatives / midpoint integral for the identity checks | — |
| `_poisson_pmf`, `_normal_pdf` | self-contained reference pmf/pdf for the `~ST-09` / `~ST-18` limits | — |

## Use
```python
from binomial import (binom_pmf, binom_cdf, binom_mean, binom_var, binom_mgf,
                      binom_mode, sum_two_binomials_pmf, _deriv1)

binom_pmf(3, 10, 0.35)                         # 0.25222...  most likely value
sum(binom_pmf(k, 10, 0.35) for k in range(11)) # 1.0         pmf normalizes
binom_mean(10, 0.35), binom_var(10, 0.35)      # (3.5, 2.275)  np, np(1-p)
binom_mode(10, 0.35)                           # 3           floor((n+1)p)
_deriv1(lambda t: binom_mgf(t, 10, 0.35), 0.0) # 3.5 = np    M'(0) = mean
sum_two_binomials_pmf(5, 4, 6, 0.35) == binom_pmf(5, 10, 0.35)  # True (additivity)
```

## Run
```bash
cd code
python3 binomial.py        # demo: pmf bar chart, normalization, mean/var, mgf moments, Poisson & normal limits
python3 test_binomial.py   # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — Bernoulli trial → binomial pmf → normalization (binomial theorem)
  → mean/variance by indicator sums → mgf and additivity → mode → the Poisson and
  normal limits; each result tied to a code symbol.
- `code/binomial.py`, `code/test_binomial.py` (numpy + stdlib `math` only, self-contained).
- `problems/problems.md` — worked problems (STAT 414 L10; numerical cross-checks to the code).
- `refs.md` — citation table (STAT 414 OER primary, lesson level; Hogg–Tanis–Zimmerman,
  Wackerly, Ross cross-cited at chapter level).
