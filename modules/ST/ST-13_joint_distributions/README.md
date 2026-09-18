# ST-13 — Joint Distributions of Two Random Variables

Module ST-13 of the **PROBABILITY THEORY** trunk (a module-by-module replica of
Penn State's STAT 414; see `modules/topic_network.txt`). It opens **Section 4,
Bivariate Distributions**, lifting the single-variable machinery of `~ST-05`
(discrete) and `~ST-10`/`~ST-12` (continuous) to **two** random variables on the
same sample space, and it sets up `~ST-14` (covariance, correlation, conditional
distributions) and `~ST-15` (the bivariate normal).

- **Prerequisites:** `~ST-05` (a single discrete random variable — pmf $f(x)$,
  cdf $F(x)$, $E[X]$, variance; everything here is its two-variable lift),
  `~ST-10` (continuous random variables — pdf, integrating to find probabilities),
  `~ST-02` (counting / sums over a sample space), `~MA-15` (multiple integrals —
  the double integral that replaces the double sum).
- **Cross-links:** `~ST-14` (covariance, correlation, **conditional**
  distributions — the immediate sequel built on these marginals and on
  `expectation_joint`), `~ST-15` (bivariate normal — the headline continuous
  joint density), `~ST-06` (mgf — the joint mgf factors iff $X,Y$ are
  independent), `~ST-16` (transformations of two RVs — sums by convolution),
  `~SM-01` (multiplicity / independence of subsystems — the same product rule in
  statistical physics).

## Scope

A **joint distribution** specifies the probabilities of $X$ and $Y$ *together*.
The discrete (STAT 414 **L17**) and continuous (**L20**) theories run perfectly
parallel — **sum** $\leftrightarrow$ **integral**, everything else identical:

- **Joint pmf / pdf.** Discrete: $f(x,y)=P(X=x,Y=y)\ge0$ with
  $\sum_{x,y}f(x,y)=1$. Continuous: $f(x,y)\ge0$ with
  $\iint f(x,y)\,dx\,dy=1$. Code: `joint_pmf_is_valid`, `joint_pdf_is_valid`,
  `normalize_joint_pdf`.
- **Marginals.** Sum / integrate the *other* variable out:
  $f_X(x)=\sum_y f(x,y)$ or $\int f(x,y)\,dy$. Code: `marginal_x`,
  `marginal_y`, `marginal_pdf_x`, `marginal_pdf_y`.
- **Independence.** $X\perp Y$ iff the joint **factors** as
  $f(x,y)=f_X(x)\,f_Y(y)$ for *all* $(x,y)$. Code: `independent_rv_check`,
  `independent_pdf_check`.
- **Expectation (LOTUS).** $E[g(X,Y)]=\sum_{x,y}g\,f$ or $\iint g\,f$; with
  $g=x+y$ this gives linearity, $E[X+Y]=E[X]+E[Y]$, for *any* joint. Code:
  `expectation_joint`, `expectation_joint_continuous`.
- **Joint & marginal cdfs.** $F(x,y)=P(X\le x,Y\le y)$; $F_X(x)=F(x,\infty)$.
  Code: `joint_cdf`, `marginal_cdf_x`, `joint_cdf_continuous`.

A 1-D and a 2-D **midpoint integrator** (`_integrate`, `_integrate2d`) let every
continuous identity be checked numerically against its closed form.

## Operations — `code/joint_distributions.py`

Discrete: `P` is a 2-D array, `P[i,j]` $=f(x_i,y_j)$ (rows $\to X$, cols $\to Y$).
Continuous: `f` is a callable `f(x,y)` on a rectangle support.

| call | meaning | reference |
|------|---------|-----------|
| `joint_pmf_is_valid(P)` | $f\ge0$ and $\sum_{x,y}f(x,y)=1$ | PSU L17 |
| `marginal_x(P)` / `marginal_y(P)` | $f_X(x)=\sum_y f(x,y)$ / $f_Y(y)=\sum_x f(x,y)$ | PSU L17 |
| `independent_rv_check(P)` | $f(x,y)=f_X(x)\,f_Y(y)$ for all $(x,y)$ (outer product) | PSU L17 |
| `expectation_joint(g, xv, yv, P)` | $E[g(X,Y)]=\sum_{x,y}g(x,y)f(x,y)$ (LOTUS) | PSU L17 |
| `joint_cdf(P, xv, yv, x, y)` | $F(x,y)=\sum_{x_i\le x,\,y_j\le y}f(x_i,y_j)$ | PSU L17 |
| `marginal_cdf_x(P, xv, x)` | $F_X(x)=\sum_{x_i\le x}f_X(x_i)=F(x,\infty)$ | PSU L17 |
| `joint_pdf_is_valid(f, ax,bx,ay,by)` | $f\ge0$ and $\iint f\,dx\,dy=1$ | PSU L20 |
| `normalize_joint_pdf(shape, ...)` | $c=1/\iint \text{shape}\,dx\,dy$ | PSU L20 |
| `marginal_pdf_x(f, x, ay, by)` | $f_X(x)=\int f(x,y)\,dy$ | PSU L20 |
| `marginal_pdf_y(f, y, ax, bx)` | $f_Y(y)=\int f(x,y)\,dx$ | PSU L20 |
| `independent_pdf_check(f, ...)` | $f(x,y)=f_X(x)f_Y(y)$ on a grid | PSU L20 |
| `expectation_joint_continuous(g, f, ...)` | $E[g]=\iint g(x,y)f(x,y)\,dx\,dy$ | PSU L20 |
| `joint_cdf_continuous(f, ax, ay, x, y)` | $F(x,y)=\int_{a_x}^{x}\!\int_{a_y}^{y}f\,dv\,du$ | PSU L20 |
| `_integrate(f,a,b)` / `_integrate2d(f,...)` | midpoint $\int$ and $\iint$ (`~MA-15`) | — |

## Use

```python
import numpy as np
from joint_distributions import (joint_pmf_is_valid, marginal_x, marginal_y,
    independent_rv_check, expectation_joint, joint_cdf,
    marginal_pdf_x, independent_pdf_check, expectation_joint_continuous,
    joint_cdf_continuous)

# discrete  f(x,y) = (x+y)/32,  x in {1,2}, y in {1,2,3,4}   (STAT 414 L17)
xv, yv = [1, 2], [1, 2, 3, 4]
P = np.array([[x + y for y in yv] for x in xv], float) / 32.0
joint_pmf_is_valid(P)                                 # True
marginal_x(P)                                         # [0.4375 0.5625]
independent_rv_check(P)                               # False  (does not factor)
expectation_joint(lambda x, y: x*y, xv, yv, P)        # 4.375  = E[XY]
joint_cdf(P, xv, yv, 1, 2)                            # 0.15625 = P(X<=1, Y<=2)

# continuous  f = 4xy (independent) and f = x+y (dependent) on the unit square (L20)
f_ind, f_dep = (lambda x, y: 4*x*y), (lambda x, y: x + y)
independent_pdf_check(f_ind, 0, 1, 0, 1)              # True   (= 2x * 2y)
independent_pdf_check(f_dep, 0, 1, 0, 1)              # False
marginal_pdf_x(f_dep, 0.3, 0, 1)                      # 0.8    = x + 1/2
expectation_joint_continuous(lambda x, y: x, f_dep, 0, 1, 0, 1)  # 0.5833 = 7/12
joint_cdf_continuous(f_ind, 0, 0, 0.5, 0.5)          # 0.0625 = x^2 y^2
```

## Run

```bash
cd code
python3 joint_distributions.py        # demo: discrete (x+y)/32 and continuous 4xy, x+y
python3 test_joint_distributions.py   # tests  ->  "All 12 tests passed."
```

## Files
- `notes.md` — the discrete (L17) and continuous (L20) theories side by side:
  joint pmf/pdf, marginals, independence, LOTUS, joint/marginal cdfs; each result
  tied to a code symbol; a "Where this goes" map.
- `code/joint_distributions.py`, `code/test_joint_distributions.py` (numpy + stdlib
  `math` only, self-contained; a midpoint 1-D/2-D integrator for the continuous checks).
- `problems/problems.md` — worked problems (STAT 414 L17/L20; each ends with a
  numerical cross-check to the code).
- `refs.md` — citation table (STAT 414 OER primary, by lesson; Hogg–Tanis–Zimmerman
  at chapter level).
