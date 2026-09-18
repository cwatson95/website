# ST-15 — References

| Source (edition) | Locator | Notes |
|---|---|---|
| Penn State **STAT 414**, *Introduction to Probability Theory* (OER, CC BY-NC 4.0) | **Lesson 21, Bivariate Normal Distributions** — `https://online.stat.psu.edu/stat414/lesson/21` | **primary**; this module is a faithful replica of L21. Cited by **lesson number and title**. |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (the text STAT 414 follows) | **Ch. 5** (*Multivariate Distributions* — bivariate normal section) | cross-cited at **chapter level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* | **Ch. 5** (*Multivariate Probability Distributions* — bivariate normal) | cross-cited at **chapter level** |
| Ross, *A First Course in Probability* | **Ch. 6** (*Jointly Distributed Random Variables*) | cross-cited at **chapter level** |

> **Granularity.** This trunk has **no textbook PDF on the shelf**, so the primary
> citation is the **STAT 414 OER lesson** (by number and title), and the textbook
> cross-references are given at **chapter level only** — *no page numbers* (page
> offsets are **not** verified; cf. `~QF-01/refs.md`, which cites a PDF at section
> level). The bivariate normal pdf, marginals, conditional, $\rho=0\Leftrightarrow$
> independence, mgf, and contour ellipses are standard and appear in every source
> above; tighten to section/page level if a PDF is later added to the shelf. STAT
> 414 lesson titles follow the live OER and may be confirmed at the URL above.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Bivariate normal pdf, explicit $(\mu_X,\mu_Y,\sigma_X,\sigma_Y,\rho)$ form (`bivariate_normal_pdf`, `normal_pdf`) | PSU | L21 *Bivariate Normal Distributions* |
| Covariance-matrix form $\frac{1}{2\pi\sqrt{\det\Sigma}}e^{-\frac12 w^\top\Sigma^{-1}w}$; $\det\Sigma$, $\Sigma^{-1}$ (`covariance_matrix`, `bivariate_normal_pdf_cov`, `mahalanobis_sq`) | PSU; `~MA-04` | L21; linear-algebra layer |
| Positive-definite $\Sigma$ (Sylvester), $|\rho|<1$; correlation off $\Sigma$ (`is_positive_definite`, `correlation`) | `~MA-04`; PSU | L18 *Correlation Coefficient* / L21 |
| Both marginals normal $X\sim N(\mu_X,\sigma_X^2)$, $Y\sim N(\mu_Y,\sigma_Y^2)$ (`marginal_pdf_x`, `marginal_pdf_y`) | PSU | L21 (uses L19/L20 marginal/conditional machinery) |
| Conditional $Y\mid X=x\sim N(\mu_Y+\rho\tfrac{\sigma_Y}{\sigma_X}(x-\mu_X),\ \sigma_Y^2(1-\rho^2))$; regression line, regression to the mean (`conditional_params`, `conditional_pdf_y_given_x`) | PSU; `~ST-14` | L19 *Conditional Distributions* / L21 |
| $\rho=0\Leftrightarrow$ independence (joint Gaussian only) | PSU | L21 (contrast L18) |
| Joint mgf $M(t_1,t_2)=\exp(\mu^\top t+\tfrac12 t^\top\Sigma t)$; moments by differentiation (`mgf`) | PSU; `~ST-06` | L21; L9 *Moment-Generating Functions* |
| Contour ellipses $w^\top\Sigma^{-1}w=c^2$; principal axes / eigen-decomposition (`ellipse_axes`, `ellipse_points`) | PSU; `~MA-04` | L21; spectral theorem |

## See also
- `~ST-14` (covariance, correlation $\rho$, conditional mean / regression — STAT
  414 L18–L19) — the layer this module specializes; `~ST-13` (joint, marginal and
  conditional distributions, independence — L17/L20) — the operations used in §3–§5.
- `~ST-12` (the univariate normal — L16) — what every marginal and conditional
  here is; `~MA-19` (probability & sample moments) — the elementary substrate this
  trunk deepens.
- `~MA-04` (positive-definite matrices, $\Sigma^{-1}$, $\det\Sigma$, eigen-decomposition)
  — the linear-algebra engine of the matrix form and the contour ellipses.
- Forward: `~ST-16` (transformations / Jacobians — analytic marginals & sums),
  `~ST-17` (mgf technique & normal sampling distributions $\chi^2$, $t$, $F$),
  `~ST-18` (central limit theorem — why pairs of sums become bivariate normal).
- `~SM-01` (the Gaussian as the maximum-entropy density for fixed mean and
  covariance — the multivariate normal of statistical mechanics).
- STAT 414 OER L21 (primary, computational); Hogg–Tanis–Zimmerman Ch. 5 (the
  course text); Wackerly Ch. 5 and Ross Ch. 6 (parallel treatments).
