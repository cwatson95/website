# ST-11 — Exponential, Gamma & Chi-Square Distributions

Eleventh module of the **PROBABILITY THEORY** trunk (Penn State STAT 414; see
`modules/ST/list_ST.txt`), covering **Lesson 15**. With the continuous-r.v.
machinery of `~ST-10` in hand (pdf, cdf, percentiles), this module builds the
**gamma family** — the continuous *waiting-time* and *sum-of-squares* laws — all
normalized by the **gamma function** $\Gamma(\alpha)=\int_0^\infty t^{\alpha-1}e^{-t}\,dt$
(`~MA-12`). The exponential is the continuous memoryless law (the limit of the
geometric `~ST-08`, the inter-arrival time of the Poisson process `~ST-09`); the
gamma is a sum of exponentials (the time to the $\alpha$-th arrival); and the
chi-square is the special gamma $(\alpha=r/2,\theta=2)$ that becomes the central
**sampling distribution** of `~ST-17`.

- **Prerequisites:** `~ST-10` (continuous random variables: pdf $f$, cdf
  $F(x)=\int_{-\infty}^x f$, $E[X]=\int x f\,dx$), `~ST-06` (moment-generating
  functions $M(t)=E[e^{tX}]$ — how we read off means/variances and prove the
  sum-of-exponentials identity), `~MA-12` (special functions — the gamma function
  $\Gamma$ and its recursion $\Gamma(\alpha+1)=\alpha\Gamma(\alpha)$).
- **Cross-links:** `~ST-09` (the Poisson process — exponential inter-arrivals,
  gamma/Erlang arrival times), `~ST-08` (geometric — the *discrete* memoryless
  waiting time the exponential mirrors), `~ST-17` (the MGF technique & normal
  sampling distributions — where $\chi^2_r=\sum_{i=1}^r Z_i^2$ feeds Student-$t$
  and $F$), `~ST-12` (the normal, whose squared standard form is $\chi^2_1$),
  `~SM-06` (kinetic theory — a molecule's energy $E=\tfrac12 m v^2$ has
  $2E/kT\sim\chi^2_3$, a gamma with shape $\tfrac32$).

## Scope
Three named distributions, one gamma function. The **gamma function**
$\Gamma(\alpha)=\int_0^\infty t^{\alpha-1}e^{-t}\,dt$ interpolates the factorial
($\Gamma(n)=(n-1)!$, $\Gamma(\tfrac12)=\sqrt\pi$) and obeys
$\Gamma(\alpha+1)=\alpha\Gamma(\alpha)$. The **exponential** pdf $f(x)=\lambda
e^{-\lambda x}$ has mean $1/\lambda$, variance $1/\lambda^2$, mgf
$\lambda/(\lambda-t)$, and is **memoryless**: $P(X>s+t\mid X>s)=P(X>t)$. The
**gamma** pdf $f(x)=x^{\alpha-1}e^{-x/\theta}/(\Gamma(\alpha)\theta^\alpha)$ adds a
shape $\alpha$ and scale $\theta$, with mean $\alpha\theta$, variance
$\alpha\theta^2$, mgf $(1-\theta t)^{-\alpha}$; setting $\alpha=1$ recovers the
exponential, and a **sum of $\alpha$ iid exponentials is gamma** (the Erlang
waiting time, proved by multiplying mgfs). The **chi-square** $\chi^2_r$ is the
gamma with $\alpha=r/2,\theta=2$, so its mean is $r$, variance $2r$, mgf
$(1-2t)^{-r/2}$; $r$ is the *degrees of freedom*, and $\chi^2_2$ is the exponential
of mean $2$. The code implements every pdf/cdf/mean/variance/mgf, a Lanczos
cross-check of $\Gamma$, a regularized incomplete-gamma cdf, the memorylessness
identity, and a numerical verification that summed exponentials are gamma.

## Operations — `code/exponential_gamma_chisquare.py`

| call | meaning | reference |
|------|---------|-----------|
| `gamma_function(alpha)` | $\Gamma(\alpha)=\int_0^\infty t^{\alpha-1}e^{-t}\,dt$; $\Gamma(\alpha{+}1)=\alpha\Gamma(\alpha)$, $\Gamma(n)=(n{-}1)!$ | L15.1; `~MA-12` |
| `gamma_lanczos(z)` | Lanczos approximation of $\Gamma(z)$ — independent check of `gamma_function` | `~MA-12` |
| `exponential_pdf(x, lam)` | $f(x)=\lambda e^{-\lambda x},\ x\ge 0$ | L15.2 |
| `exponential_cdf(x, lam)` | $F(x)=1-e^{-\lambda x}$ | L15.2 |
| `exponential_survival(x, lam)` | $S(x)=P(X>x)=e^{-\lambda x}$ | L15.2 |
| `exponential_mean(lam)` / `exponential_var(lam)` | $E[X]=1/\lambda$; $\mathrm{Var}=1/\lambda^2$ | L15.2 |
| `exponential_mgf(t, lam)` | $M(t)=\lambda/(\lambda-t)=1/(1-\theta t),\ t<\lambda$ | L15.2; `~ST-06` |
| `exp_memoryless_check(s, t, lam)` | returns $\big(P(X{>}s{+}t\mid X{>}s),\,P(X{>}t)\big)$ — equal | L15.2 |
| `gamma_pdf(x, alpha, theta)` | $f(x)=x^{\alpha-1}e^{-x/\theta}/(\Gamma(\alpha)\theta^\alpha)$ | L15.3 |
| `gamma_cdf(x, alpha, theta)` | $F(x)=P(\alpha,\,x/\theta)$, regularized lower incomplete gamma | L15.3 |
| `gamma_mean(alpha, theta)` / `gamma_var(alpha, theta)` | $E[X]=\alpha\theta$; $\mathrm{Var}=\alpha\theta^2$ | L15.3 |
| `gamma_mgf(t, alpha, theta)` | $M(t)=(1-\theta t)^{-\alpha},\ t<1/\theta$ | L15.3; `~ST-06` |
| `convolve_two_exponentials_pdf(x, lam)` | $\int_0^x\!\lambda e^{-\lambda y}\lambda e^{-\lambda(x-y)}dy=\lambda^2 x e^{-\lambda x}$ = gamma$(2,1/\lambda)$ | L15.3 |
| `simulate_sum_of_exponentials(alpha, theta)` | Monte-Carlo: sum of $\alpha$ iid Exp$(\theta)$ is gamma$(\alpha,\theta)$ | L15.3 |
| `chi2_pdf(x, r)` / `chi2_cdf(x, r)` | gamma with $\alpha=r/2,\theta=2$ | L15.4 |
| `chi2_mean(r)` / `chi2_var(r)` | $E[X]=r$; $\mathrm{Var}=2r$ | L15.4 |
| `chi2_mgf(t, r)` | $M(t)=(1-2t)^{-r/2},\ t<\tfrac12$ | L15.4; `~ST-17` |
| `lower_incomplete_gamma_regularized(a, x)` | $P(a,x)=\tfrac1{\Gamma(a)}\int_0^x t^{a-1}e^{-t}dt$ | L15.3 |

## Use
```python
from exponential_gamma_chisquare import (
    gamma_function, exponential_mean, exp_memoryless_check,
    gamma_pdf, gamma_mean, gamma_var, chi2_pdf, chi2_mean, exponential_pdf)

gamma_function(5)                      # 24.0      = 4!  (Gamma(n) = (n-1)!)
gamma_function(0.5)                    # 1.7724538 = sqrt(pi)
exponential_mean(0.5)                  # 2.0       = 1/lambda
exp_memoryless_check(3.0, 2.0, 0.4)    # (0.449329, 0.449329)  P(X>5|X>3)=P(X>2)
gamma_mean(3.0, 2.0), gamma_var(3.0, 2.0)   # (6.0, 12.0)  alpha*theta, alpha*theta^2
chi2_mean(10)                          # 10.0      mean = r
chi2_pdf(3.0, 2) == exponential_pdf(3.0, 0.5)  # True   chi^2_2 is Exp(mean 2)
```

## Run
```bash
cd code
python3 exponential_gamma_chisquare.py        # demo: gamma function, exp/gamma/chi-square moments, memorylessness
python3 test_exponential_gamma_chisquare.py   # tests  ->  "All 21 tests passed."
```

## Files
- `notes.md` — the gamma function and its recursion; the exponential (pdf, cdf,
  moments, mgf, memorylessness); the gamma family (sum of exponentials = Erlang);
  the chi-square as gamma$(r/2,2)$ and its road to sampling theory
- `code/exponential_gamma_chisquare.py`, `code/test_exponential_gamma_chisquare.py`
  (numpy + stdlib `math` only; self-contained — no sibling imports)
- `problems/problems.md` — worked problems (STAT 414 L15; numeric cross-checks to the code)
- `refs.md` — citation table (STAT 414 OER primary; Hogg–Tanis–Zimmerman, Wackerly,
  Ross cross-cited at chapter level)
