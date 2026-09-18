# ST-14 — References

| Source (edition) | Locator | Notes |
|---|---|---|
| Penn State **STAT 414**, *Introduction to Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414` → **Lesson 18** *The Correlation Coefficient*, **Lesson 19** *Conditional Distributions* | **primary**; this module is a faithful replica of L18–L19. Cited by **lesson number and title**. |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | Ch. 4 *Bivariate Distributions* | **the text STAT 414 follows**; cross-cited at **chapter level** (covariance, correlation, conditional distributions, regression). |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | Ch. 5 *Multivariate Probability Distributions* | optional cross-reference, **chapter level** (Cov, $\rho$, conditional expectation). |
| Ross, *A First Course in Probability* (10th ed.) | Ch. 7 *Properties of Expectation* (§§7.4 covariance, 7.5 conditional expectation) | optional cross-reference, **section level** (the Cauchy–Schwarz bound, conditioning). |

> **Granularity.** This trunk has **no textbook PDF on the shelf**, so the primary
> citation is the **STAT 414 OER at lesson level** (`.../lesson/18`, `.../lesson/19`);
> these lesson pages are stable and were used to fix definitions and notation. The
> book cross-references (HTZ, Wackerly, Ross) are given at **chapter/section level
> only** — chapter titles follow the standard editions, but **page offsets are not
> verified** (we do not hold the PDFs). Tighten to page level only against a copy in
> hand. Lesson↔book mapping follows STAT 414's stated correspondence to HTZ Ch. 4.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Covariance $\operatorname{Cov}(X,Y)=E[XY]-E[X]E[Y]$, bilinearity, $\operatorname{Cov}(X,X)=\operatorname{Var}X$ (`covariance`, `mean_xy`) | PSU | **L18** *The Correlation Coefficient* |
| Correlation $\rho=\operatorname{Cov}/(\sigma_X\sigma_Y)$, scale invariance (`correlation`) | PSU | **L18** |
| $\lvert\rho\rvert\le1$ by **Cauchy–Schwarz**; equality $\Leftrightarrow$ affine $Y=aX+b$ (`linear_dependence_example`) | PSU / HTZ | **L18** / Ch. 4; `~MA-04` |
| Covariance matrix $\Sigma$, PSD, $\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)$ (`covariance_matrix`) | HTZ | Ch. 4; `~MA-04` (the bilinear-form view) |
| Independence $\Rightarrow\rho=0$; converse false, $X\sim U\{-1,0,1\},Y=X^2$ (`product_joint`, `is_independent`, `uncorrelated_dependent_example`) | PSU / HTZ | **L18** / Ch. 4 |
| Conditional pmf/pdf $f(y\mid x)=f(x,y)/f_X(x)$ (`conditional_pmf`, `cont_marginal_x`) | PSU | **L19** *Conditional Distributions* |
| Conditional expectation $E[Y\mid X=x]$, the **regression function** (`conditional_expectation`, `regression_function`, `cont_conditional_expectation`) | PSU / HTZ | **L19** / Ch. 4 |
| Law of total expectation $E[E[Y\mid X]]=E[Y]$ (`law_of_total_expectation`, `cont_total_expectation`) | PSU / Ross | **L19** / Ch. 7.5 |
| Least-squares line, slope $\rho\,\sigma_Y/\sigma_X$, **regression to the mean** (`regression_line`, `best_linear_predictor`) | PSU / HTZ | **L18** / Ch. 4 |

## See also
- `~ST-13` (joint distributions, marginals, independence) — the joint law this
  module measures and conditions; the marginals $f_X,f_Y$ are reused as
  denominators here.
- `~MA-04` (linear algebra: inner products, Cauchy–Schwarz, positive-definite /
  covariance matrices) — the algebra behind $|\rho|\le1$ and $\det\Sigma\ge0$ (§2–3
  of `notes.md`).
- `~ST-15` (the **bivariate normal**) — the next module: the regression function
  becomes the §8 line and $\rho=0\Leftrightarrow$ independence; `~ST-12` (the normal
  marginal) feeds it.
- `~ST-05` (expectation, variance) and `~ST-06` (MGF) — the one-variable moments
  the cross moment $E[XY]$ and joint MGF generalize.
- `~MA-19` (probability & statistics) and `~SM-01` (ensembles) — the empirical
  sample correlation / least-squares estimator, and fluctuation correlations in
  statistical mechanics.
- STAT 414 L18–L19 (primary, with worked examples); HTZ Ch. 4 (the matching
  textbook treatment); Wackerly Ch. 5 and Ross Ch. 7 (alternative expositions of
  covariance, correlation, and conditional expectation).
