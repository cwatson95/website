# ST-15 — The Bivariate Normal Distribution

Module of the **PROBABILITY THEORY** trunk (see `modules/ST/list_ST.txt`), a
module-by-module replica of Penn State's **STAT 414**. Covers **Lesson 21,
Bivariate Normal Distributions** — the joint Gaussian on a pair $(X,Y)$, the
high point of the bivariate-distributions section where every separate idea of
the previous lessons (marginals, conditionals, covariance, correlation) collapses
into one closed-form object.

- **Prerequisites:** `~ST-14` (covariance, correlation $\rho$, and the conditional
  mean / regression line — this module is their joint-Gaussian special case),
  `~ST-12` (the univariate normal $N(\mu,\sigma^2)$ — every marginal and every
  conditional here *is* one), `~ST-13` (joint/marginal/conditional densities and
  independence for two random variables), `~MA-04` (the **positive-definite**
  covariance matrix $\Sigma$, its inverse, determinant, and eigen-decomposition).
- **Cross-links:** `~SM-01` (the multivariate Gaussian is the maximum-entropy
  density for fixed mean and covariance — the statistical-mechanics workhorse),
  `~ST-06` (the moment-generating function $M(t_1,t_2)$ that pins the moments),
  `~MA-19` (probability & sample moments — the elementary layer this trunk
  deepens), `~ST-18` (the central limit theorem — why sums land on this surface),
  `~ST-16` (transformations / Jacobians — how to derive the marginals and
  conditionals analytically).

## Scope
The **bivariate normal** density in the five parameters $(\mu_X,\mu_Y,\sigma_X,
\sigma_Y,\rho)$ is
$$f(x,y)=\frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}}
\exp\!\left(-\frac{z}{2(1-\rho^2)}\right),\qquad
z=\frac{(x-\mu_X)^2}{\sigma_X^2}-\frac{2\rho(x-\mu_X)(y-\mu_Y)}{\sigma_X\sigma_Y}
+\frac{(y-\mu_Y)^2}{\sigma_Y^2}.$$
Packing the means into $\boldsymbol\mu=(\mu_X,\mu_Y)$ and the second moments into
the **covariance matrix** $\Sigma=\left(\begin{smallmatrix}\sigma_X^2&\rho\sigma_X\sigma_Y\\
\rho\sigma_X\sigma_Y&\sigma_Y^2\end{smallmatrix}\right)$ rewrites it as the clean
quadratic form $f(\mathbf x)=\frac{1}{2\pi\sqrt{\det\Sigma}}\exp\!\big(-\tfrac12
(\mathbf x-\boldsymbol\mu)^{\!\top}\Sigma^{-1}(\mathbf x-\boldsymbol\mu)\big)$,
which requires $\Sigma$ **positive-definite** ($\sigma_X,\sigma_Y>0$, $|\rho|<1$;
`~MA-04`). From this one object the whole lesson follows: **both marginals are
normal** ($X\sim N(\mu_X,\sigma_X^2)$, $Y\sim N(\mu_Y,\sigma_Y^2)$); the
**conditional $Y\mid X=x$ is normal** with mean $\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}
(x-\mu_X)$ (the regression line of `~ST-14`) and variance $\sigma_Y^2(1-\rho^2)$
(*independent of $x$* — homoscedastic, and shrunk by the information $X$ carries);
and — uniquely for the joint Gaussian — **$\rho=0\iff$ independence**. The
constant-density **contour ellipses** $(\mathbf x-\boldsymbol\mu)^{\!\top}
\Sigma^{-1}(\mathbf x-\boldsymbol\mu)=c^2$ have principal axes along the
eigenvectors of $\Sigma$ with semi-axes $c\sqrt{\lambda_i}$. The code builds the
density both ways and **verifies they agree**, integrates out a variable to
confirm the normal marginal, checks the conditional mean/variance by integration,
confirms the $\rho=0$ factorization, and recovers the moments from the
mgf $M(t_1,t_2)=\exp\!\big(\boldsymbol\mu^{\!\top}\mathbf t+\tfrac12\mathbf t^{\!\top}
\Sigma\,\mathbf t\big)$.

## Operations — `code/bivariate_normal.py`

| call | meaning | reference |
|------|---------|-----------|
| `normal_pdf(x, mu, sigma)` | univariate $N(\mu,\sigma^2)$ pdf — the marginal building block | L16/L21; `~ST-12` |
| `bivariate_normal_pdf(x, y, mux, muy, sx, sy, rho)` | explicit five-parameter pdf $f(x,y)$ | L21 |
| `covariance_matrix(sx, sy, rho)` | $\Sigma=\left(\begin{smallmatrix}\sigma_X^2&\rho\sigma_X\sigma_Y\\\rho\sigma_X\sigma_Y&\sigma_Y^2\end{smallmatrix}\right)$ | L21; `~MA-04` |
| `bivariate_normal_pdf_cov(x, y, mu, Sigma)` | matrix form $\frac{1}{2\pi\sqrt{\det\Sigma}}e^{-\frac12 w^\top\Sigma^{-1}w}$ (numpy) | L21; `~MA-04` |
| `mahalanobis_sq(x, y, ...)` | quadratic form $w^\top\Sigma^{-1}w=z/(1-\rho^2)$ — the ellipse level | L21 |
| `marginal_pdf_x(x, mux, sx)` / `marginal_pdf_y(y, muy, sy)` | the marginals $N(\mu_X,\sigma_X^2)$, $N(\mu_Y,\sigma_Y^2)$ | L21 |
| `conditional_params(x, ...)` | $(\,\mu_Y+\rho\tfrac{\sigma_Y}{\sigma_X}(x-\mu_X),\ \sigma_Y^2(1-\rho^2)\,)$ | L21; `~ST-14` |
| `conditional_pdf_y_given_x(y, x, ...)` | $f(y\mid x)$: normal with those parameters | L21 |
| `correlation(Sigma)` | $\rho=\Sigma_{xy}/(\sigma_X\sigma_Y)$ read off $\Sigma$ | L18; `~ST-14` |
| `is_positive_definite(Sigma)` | Sylvester test: every leading minor $>0$ ($|\rho|<1$) | `~MA-04` |
| `mgf(t1, t2, ...)` | $M(t_1,t_2)=\exp(\boldsymbol\mu^\top\mathbf t+\tfrac12\mathbf t^\top\Sigma\mathbf t)$ | L21; `~ST-06` |
| `ellipse_axes(Sigma, c)` | semi-axes $c\sqrt{\lambda_i}$ and tilt from $\Sigma=V\Lambda V^\top$ | `~MA-04` |
| `ellipse_points(mux, muy, sx, sy, rho, c)` | points on the contour $w^\top\Sigma^{-1}w=c^2$ | L21 |

## Use
```python
import numpy as np
from bivariate_normal import (bivariate_normal_pdf, covariance_matrix,
    bivariate_normal_pdf_cov, conditional_params, marginal_pdf_x,
    conditional_pdf_y_given_x, correlation, is_positive_definite, mgf)

mux, muy, sx, sy, rho = 1.0, 2.0, 1.0, 2.0, 0.6
Sigma = covariance_matrix(sx, sy, rho)            # [[1,1.2],[1.2,4]]
np.linalg.det(Sigma)                               # 2.56 = sx^2 sy^2 (1-rho^2)
is_positive_definite(Sigma), correlation(Sigma)    # (True, 0.6)

# explicit pdf == covariance-matrix pdf
bivariate_normal_pdf(1.5, 3.0, mux, muy, sx, sy, rho)        # 0.08508277
bivariate_normal_pdf_cov(1.5, 3.0, (mux, muy), Sigma)        # 0.08508277

# conditional Y | X=1.5 is N(2.6, 2.56): regression line + (1-rho^2) variance
conditional_params(1.5, mux, muy, sx, sy, rho)               # (2.6, 2.56)

# joint factors as marginal_X * conditional (always) ...
mux_pdf = marginal_pdf_x(1.5, mux, sx)
mux_pdf * conditional_pdf_y_given_x(3.0, 1.5, mux, muy, sx, sy, rho)  # 0.08508277

# ... and as marginal_X * marginal_Y exactly when rho=0 (independence)
mgf(0.0, 0.0, mux, muy, sx, sy, rho)                         # 1.0  (always)
```

## Run
```bash
cd code
python3 bivariate_normal.py        # demo: Sigma, pdf two ways, conditional, ellipse
python3 test_bivariate_normal.py   # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — the derivations: explicit pdf ↔ covariance-matrix form, the
  Mahalanobis exponent, marginals by integrating out, the conditional regression
  line and shrunk variance, $\rho=0\iff$ independence, the mgf, contour ellipses.
- `code/bivariate_normal.py`, `code/test_bivariate_normal.py` (numpy + stdlib `math`, self-contained).
- `problems/problems.md` — worked problems (STAT 414 L21; each ends in a code check).
- `refs.md` — citation table (STAT 414 OER primary; Hogg–Tanis–Zimmerman,
  Wackerly, Ross cross-cited at chapter level).
