# ST-14 — Correlation & Conditional Distributions

Fourteenth module of the **PROBABILITY THEORY** trunk (`modules/ST/list_ST.txt`),
a module-by-module replica of Penn State's **STAT 414**. It covers **L18 The
Correlation Coefficient** and **L19 Conditional Distributions**: how a *single
number* — the correlation $\rho$ — summarizes the linear tie between two random
variables, and how *conditioning* turns the joint law of `~ST-13` into a family
of one-variable laws whose means trace the **regression function**.

- **Prerequisites:** `~ST-13` (joint pmf/pdf $f(x,y)$, marginals
  $f_X,f_Y$, and independence $f(x,y)=f_X(x)f_Y(y)$ — the object this module
  measures and slices), `~ST-05` (expectation, variance, $E[g(X)]$),
  `~MA-04` (the **covariance matrix** and the **Cauchy–Schwarz inequality** —
  exactly the algebra behind $|\rho|\le 1$).
- **Cross-links:** `~ST-12` (the normal distribution — the marginal of the
  bivariate Gaussian), `~ST-15` (the **bivariate normal**, where the regression
  function *is* the straight line built here and the conditionals are Gaussian),
  `~ST-06` (the MGF, which the joint MGF generalizes), `~SM-01` (correlations and
  fluctuations in statistical ensembles), `~MA-19` (sample correlation /
  least-squares — the empirical estimator of $\rho$).

## Scope
For two random variables on one probability space the **covariance**
$\operatorname{Cov}(X,Y)=E[XY]-E[X]E[Y]$ measures their joint variation; dividing
by the two standard deviations gives the dimensionless **correlation
coefficient** $\rho=\operatorname{Cov}(X,Y)/(\sigma_X\sigma_Y)$, which the
**Cauchy–Schwarz inequality** confines to $|\rho|\le 1$ — with equality **iff**
$Y$ is an affine function of $X$. **Independence forces $\rho=0$**, but the
converse is false: $\rho$ sees only the *linear* part of a dependence, and the
module ships the standing counterexample ($X$ uniform on $\{-1,0,1\}$, $Y=X^2$:
$\rho=0$ yet $Y$ is a deterministic function of $X$). Conditioning replaces a
marginal by a slice, the **conditional pmf/pdf** $f(y\mid x)=f(x,y)/f_X(x)$,
itself a legitimate distribution; its mean $E[Y\mid X=x]$ is the **regression
function**, and averaging it over $X$ recovers the marginal mean — the **law of
total expectation** $E\!\left[E[Y\mid X]\right]=E[Y]$. The best straight-line
predictor has slope $\rho\,\sigma_Y/\sigma_X$ and, because $|\rho|\le1$, pulls
predictions toward the mean: **regression to the mean**. The covariance matrix
$\Sigma=\bigl[\begin{smallmatrix}\operatorname{Var}X&\operatorname{Cov}\\\operatorname{Cov}&\operatorname{Var}Y\end{smallmatrix}\bigr]$
ties it all to `~MA-04`: $\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)\ge0$ **is**
the statement $|\rho|\le1$.

## Operations — `code/correlation_conditional.py`

A discrete joint law is the small `Joint(xs, ys, P)` object with
$P_{ij}=P(X=x_i,Y=y_j)$; continuous laws use a density callable $f(x,y)$ on a
rectangle plus the midpoint integrators `_integrate` / `_integrate2`.

| call | meaning | reference |
|------|---------|-----------|
| `Joint(xs, ys, P)` | discrete joint pmf $P_{ij}=P(X{=}x_i,Y{=}y_j)$ (rows $x$, cols $y$) | L17–18; `~ST-13` |
| `marginal_x(j)` / `marginal_y(j)` | $f_X(x_i)=\sum_jP_{ij}$, $f_Y(y_j)=\sum_iP_{ij}$ | L17 |
| `mean_x` / `mean_y` / `mean_xy(j)` | $E[X]$, $E[Y]$, the cross moment $E[XY]=\sum_{ij}x_iy_jP_{ij}$ | L18 |
| `var_x` / `var_y` / `std_x` / `std_y` | $\operatorname{Var}=E[\cdot^2]-E[\cdot]^2$, $\sigma=\sqrt{\operatorname{Var}}$ | `~ST-05` |
| `covariance(j)` | $\operatorname{Cov}(X,Y)=E[XY]-E[X]E[Y]$ | L18 |
| `correlation(j)` | $\rho=\operatorname{Cov}/(\sigma_X\sigma_Y)$; raises if $|\rho|>1$ | L18 |
| `covariance_matrix(j)` | $\Sigma=[[\operatorname{Var}X,\operatorname{Cov}],[\operatorname{Cov},\operatorname{Var}Y]]$ (PSD) | L18; `~MA-04` |
| `conditional_pmf(j, x)` | $f(y\mid x)=f(x,y)/f_X(x)$ → `(ys, probs)` | L19 |
| `conditional_expectation(j, x)` | $E[Y\mid X{=}x]=\sum_jy_jf(y_j\mid x)$ | L19 |
| `regression_function(j)` | $x\mapsto E[Y\mid X{=}x]$ over the support | L19 |
| `law_of_total_expectation(j)` | $E[E[Y\mid X]]=\sum_iE[Y\mid X{=}x_i]f_X(x_i)=E[Y]$ | L19 |
| `regression_line(j)` | least-squares line: slope $b=\operatorname{Cov}/\operatorname{Var}X$, intercept $a=\mu_Y-b\mu_X$ | L18 |
| `best_linear_predictor(j, x)` | $\mu_Y+\rho\,(\sigma_Y/\sigma_X)(x-\mu_X)$ | L18 |
| `product_joint(xs,px,ys,py)` | independent joint $P_{ij}=f_X(x_i)f_Y(y_j)$ | L17; `~ST-13` |
| `is_independent(j)` | factorization test $P_{ij}=f_X(x_i)f_Y(y_j)$? | L17 |
| `uncorrelated_dependent_example()` | $X\sim U\{-1,0,1\}$, $Y=X^2$: $\rho=0$ yet dependent | L18 |
| `linear_dependence_example(a,b)` | $Y=aX+b$: $\rho=\operatorname{sgn}a$ (Cauchy–Schwarz equality) | L18 |
| `cont_covariance` / `cont_correlation(f, bounds)` | continuous $\operatorname{Cov}$, $\rho$ via `_integrate2` | L19 |
| `cont_conditional_expectation(f, x, bounds)` | $E[Y\mid X{=}x]=\int y\,f(x,y)\,dy/f_X(x)$ | L19 |

## Use
```python
import numpy as np
from correlation_conditional import (demo_joint, covariance, correlation,
    conditional_expectation, law_of_total_expectation, regression_line,
    uncorrelated_dependent_example, is_independent)

j = demo_joint()                       # f(x,y)=(x+y)/32, x in {1,2}, y in {1,2,3,4}
covariance(j)                          # -0.01953125  = -5/256
correlation(j)                         # -0.036677    |rho| <= 1
conditional_expectation(j, 1)          # 2.857142...  = 20/7  (E[Y|X=1])
law_of_total_expectation(j), j         # 2.8125 = E[Y]        (tower property)
regression_line(j)                     # (2.93651, -0.07937)  a, b=slope

u = uncorrelated_dependent_example()   # X~U{-1,0,1}, Y=X^2
correlation(u), is_independent(u)      # 0.0, False   -> rho=0 but DEPENDENT
```

## Run
```bash
cd code
python3 correlation_conditional.py        # demo: covariance, rho, regression, tower, counterexample
python3 test_correlation_conditional.py   # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — covariance and its bilinearity; Cauchy–Schwarz → $|\rho|\le1$ and
  the equality case; independence ⇒ $\rho=0$ and the $Y=X^2$ counterexample;
  conditional pmf/pdf, the regression function, the law of total expectation, and
  regression to the mean; the covariance-matrix (`~MA-04`) view.
- `code/correlation_conditional.py`, `code/test_correlation_conditional.py`
  (numpy + stdlib only, self-contained).
- `problems/problems.md` — worked problems (STAT 414 L18–L19) with numerical
  `*Check:*`s against the code.
- `refs.md` — citation table (STAT 414 OER primary; Hogg–Tanis–Zimmerman,
  Wackerly, Ross cross-cited at chapter level).
