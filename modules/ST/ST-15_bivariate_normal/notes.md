# ST-15 — The Bivariate Normal Distribution (notes)

Up to now the bivariate-distributions lessons kept marginals, conditionals,
covariance and correlation as separate machinery you bolt onto an arbitrary joint
pmf or pdf (`~ST-13`, `~ST-14`). The **bivariate normal** is the distribution in
which all of that machinery has *one* closed form. Specify five numbers — two
means, two standard deviations, and a correlation — and you have fixed the joint
density, both marginals, every conditional, the regression line, and the entire
covariance structure simultaneously. It is the joint distribution that the central
limit theorem (`~ST-18`) drives sums of independent pairs toward, and the
maximum-entropy density for a fixed mean and covariance (`~SM-01`); this is why it
is *the* default model whenever two quantities are jointly random and roughly
Gaussian.

Citation key (full table + granularity in `refs.md`): **PSU** = Penn State STAT
414 OER, **Lesson 21, Bivariate Normal Distributions** (primary); **HTZ** = Hogg,
Tanis & Zimmerman, *Probability and Statistical Inference* (the text STAT 414
follows), Ch. 5; **WMS** = Wackerly–Mendenhall–Scheaffer, Ch. 5; **Ross**, Ch. 6.
Cited at **lesson / chapter level** (no page numbers — this trunk has no PDF on
the shelf). Each result names the code symbol that realizes it.

## 1. The explicit five-parameter density

A pair $(X,Y)$ is **bivariate normal** if its joint density is, for parameters
$\mu_X,\mu_Y\in\mathbb R$, $\sigma_X,\sigma_Y>0$ and $\rho\in(-1,1)$ [PSU L21]
$$f(x,y)=\frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}}\,
\exp\!\left(-\frac{z}{2(1-\rho^2)}\right),$$
$$z=\Big(\frac{x-\mu_X}{\sigma_X}\Big)^{\!2}
-2\rho\Big(\frac{x-\mu_X}{\sigma_X}\Big)\Big(\frac{y-\mu_Y}{\sigma_Y}\Big)
+\Big(\frac{y-\mu_Y}{\sigma_Y}\Big)^{\!2}.$$
The standardized coordinates $u=(x-\mu_X)/\sigma_X$, $v=(y-\mu_Y)/\sigma_Y$ make
$z=u^2-2\rho uv+v^2$ a positive-definite quadratic whenever $|\rho|<1$, so $f>0$
everywhere and decays like a Gaussian in every direction. Code:
`bivariate_normal_pdf(x, y, mux, muy, sx, sy, rho)`. The prefactor is fixed by
demanding $\iint f\,dx\,dy=1$ (verified numerically below and in
`test_joint_pdf_normalizes`).

## 2. The covariance-matrix form and the Mahalanobis exponent

Collect the means into $\boldsymbol\mu=(\mu_X,\mu_Y)^\top$ and the second moments
into the **covariance matrix** (`~MA-04`)
$$\Sigma=\begin{pmatrix}\sigma_X^2 & \rho\sigma_X\sigma_Y\\[2pt]
\rho\sigma_X\sigma_Y & \sigma_Y^2\end{pmatrix},\qquad
\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2),\qquad
\Sigma^{-1}=\frac{1}{\det\Sigma}\begin{pmatrix}\sigma_Y^2 & -\rho\sigma_X\sigma_Y\\[2pt]
-\rho\sigma_X\sigma_Y & \sigma_X^2\end{pmatrix}.$$
Code: `covariance_matrix(sx, sy, rho)`. With $\mathbf w=(x,y)^\top-\boldsymbol\mu$
the quadratic in the exponent is exactly the **Mahalanobis distance squared**
$$\mathbf w^\top\Sigma^{-1}\mathbf w
=\frac{1}{\det\Sigma}\big(\sigma_Y^2 u^2\sigma_X^2-2\rho\sigma_X\sigma_Y\,u\sigma_X v\sigma_Y+\sigma_X^2 v^2\sigma_Y^2\big)
=\frac{u^2-2\rho uv+v^2}{1-\rho^2}=\frac{z}{1-\rho^2},$$
so the density is the manifestly coordinate-free Gaussian [PSU L21; `~MA-04`]
$$\boxed{\,f(\mathbf x)=\frac{1}{2\pi\sqrt{\det\Sigma}}\,
\exp\!\Big(-\tfrac12(\mathbf x-\boldsymbol\mu)^\top\Sigma^{-1}(\mathbf x-\boldsymbol\mu)\Big).}$$
Code `bivariate_normal_pdf_cov(x, y, mu, Sigma)` evaluates this with numpy
linear algebra and equals the explicit §1 form to machine precision
(`test_explicit_equals_covariance_form`); `mahalanobis_sq` returns
$\mathbf w^\top\Sigma^{-1}\mathbf w$ directly. The matrix form is what
generalizes verbatim to $d$ dimensions: replace $2\pi\to(2\pi)^{d/2}$.

**Positive-definiteness.** The density exists iff $\Sigma$ is positive-definite.
By Sylvester's criterion (`~MA-04`) the leading principal minors must be positive:
$\sigma_X^2>0$ and $\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)>0$, i.e. exactly
$|\rho|<1$. At $\rho=\pm1$ the mass collapses onto the line $v=\pm u$ and $\Sigma$
is singular (the *degenerate* bivariate normal). Code: `is_positive_definite(Sigma)`,
`correlation(Sigma)` (which reads $\rho=\Sigma_{xy}/(\sigma_X\sigma_Y)$ back off).

## 3. Both marginals are normal

Integrate $Y$ out. Complete the square in $v$ inside $z$:
$z=(v-\rho u)^2+(1-\rho^2)u^2$, so
$$f_X(x)=\int_{-\infty}^{\infty}\!f(x,y)\,dy
=\frac{e^{-u^2/2}}{\sigma_X\sqrt{2\pi}}
\underbrace{\int_{-\infty}^{\infty}\frac{1}{\sigma_Y\sqrt{2\pi}\sqrt{1-\rho^2}}
\exp\!\Big(\!-\frac{(v-\rho u)^2}{2(1-\rho^2)}\Big)dy}_{=\,1}
=\frac{1}{\sigma_X\sqrt{2\pi}}e^{-(x-\mu_X)^2/2\sigma_X^2}.$$
The inner integral is a normal density in $y$ (mean $\mu_Y+\rho\sigma_Y u$,
variance $\sigma_Y^2(1-\rho^2)$) and integrates to $1$. Hence [PSU L21]
$$X\sim N(\mu_X,\sigma_X^2),\qquad Y\sim N(\mu_Y,\sigma_Y^2),$$
the marginals are univariate normal (`~ST-12`) with the named means and variances
— the diagonal of $\Sigma$. Code: `marginal_pdf_x`, `marginal_pdf_y`; verified by
direct numerical integration of the joint in `test_marginal_x_is_normal` /
`test_marginal_y_is_normal`. **The converse fails:** normal marginals do *not*
imply a bivariate normal joint, so "bivariate normal" is a statement about the
joint law, not just about $X$ and $Y$ separately.

## 4. The conditional $Y\mid X=x$ is normal — the regression line

Divide the joint by the marginal. The square completed in §3 *is* the conditional:
$$f(y\mid x)=\frac{f(x,y)}{f_X(x)}
=\frac{1}{\sigma_Y\sqrt{2\pi}\sqrt{1-\rho^2}}
\exp\!\left(-\frac{\big(y-[\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X)]\big)^2}
{2\sigma_Y^2(1-\rho^2)}\right),$$
which is a normal density. Therefore [PSU L21; `~ST-14`]
$$\boxed{\,Y\mid X=x\ \sim\ N\!\Big(\,\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X),\
\ \sigma_Y^2(1-\rho^2)\Big).}$$
Code: `conditional_params(x, ...)` returns the pair, `conditional_pdf_y_given_x`
the density. Three things to read off:

- **The conditional mean is linear in $x$** — the population **regression line**
  $E[Y\mid X=x]=\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X)$, slope
  $\beta=\rho\,\sigma_Y/\sigma_X$ (the `~ST-14` least-squares slope, now exact
  rather than a best linear approximation). This is **regression to the mean**: a
  $k$-standard-deviation $x$ predicts only a $\rho k$-standard-deviation $y$.
- **The conditional variance $\sigma_Y^2(1-\rho^2)$ does not depend on $x$**
  (homoscedastic) and is *smaller* than the marginal variance $\sigma_Y^2$ by the
  factor $1-\rho^2$ — the fraction of $Y$'s variance *not* explained by $X$. The
  **coefficient of determination** $\rho^2$ is the fraction that is.
- At $\rho=0$ the conditional collapses to the marginal $N(\mu_Y,\sigma_Y^2)$;
  at $\rho\to\pm1$ the conditional variance $\to 0$ and $Y$ becomes a deterministic
  linear function of $X$.

The factorization $f(x,y)=f_X(x)\,f(y\mid x)$ holds identically (any $\rho$),
checked in `test_conditional_pdf_normalizes_and_factorizes`; the conditional
mean and variance are recovered by integrating $y\,f(y\mid x)$ and
$(y-\text{mean})^2 f(y\mid x)$ in `test_conditional_mean_and_var_by_integration`.

## 5. For the bivariate normal, $\rho=0\iff$ independence

In general **zero correlation does not imply independence** — that is the central
warning of `~ST-14`. The bivariate normal is the famous exception. Set $\rho=0$ in
§1: the cross term $-2\rho uv$ vanishes, $\sqrt{1-\rho^2}=1$, and the density
**factors**,
$$f(x,y)\big|_{\rho=0}=\frac{e^{-u^2/2}}{\sigma_X\sqrt{2\pi}}\cdot
\frac{e^{-v^2/2}}{\sigma_Y\sqrt{2\pi}}=f_X(x)\,f_Y(y),$$
so $X\perp Y$. Conversely independence forces $\mathrm{Cov}(X,Y)=0$, hence
$\rho=0$. Therefore, *within the bivariate normal family*,
$$\boxed{\ \rho=0\iff X\text{ and }Y\text{ independent}.\ }$$
Equivalently, $\Sigma$ is diagonal iff the components are independent. Code
`bivariate_normal_pdf(..., rho=0)` equals `marginal_pdf_x * marginal_pdf_y`
exactly (`test_rho_zero_is_independence`), while for $\rho\neq0$ it provably does
*not* factor. The matrix view also explains *why* it works here and not in
general: a Gaussian is fully determined by its first two moments, so killing the
only off-diagonal second moment kills all dependence.

## 6. The moment-generating function

The joint mgf (`~ST-06`) of the bivariate normal is [PSU L21; HTZ Ch. 5]
$$M(t_1,t_2)=E\big[e^{t_1X+t_2Y}\big]
=\exp\!\Big(\boldsymbol\mu^\top\mathbf t+\tfrac12\mathbf t^\top\Sigma\,\mathbf t\Big)
=\exp\!\Big(\mu_X t_1+\mu_Y t_2
+\tfrac12\big(\sigma_X^2 t_1^2+2\rho\sigma_X\sigma_Y t_1t_2+\sigma_Y^2 t_2^2\big)\Big).$$
Code: `mgf(t1, t2, ...)`, with $M(0,0)=1$. Differentiating at the origin
delivers every moment, tying $\Sigma$ to the moments operationally:
$$\frac{\partial M}{\partial t_1}\Big|_0=\mu_X,\qquad
\frac{\partial^2 M}{\partial t_1^2}\Big|_0-\mu_X^2=\sigma_X^2,\qquad
\frac{\partial^2 M}{\partial t_1\partial t_2}\Big|_0-\mu_X\mu_Y
=\mathrm{Cov}(X,Y)=\rho\,\sigma_X\sigma_Y.$$
These are checked by finite-difference differentiation in
`test_mgf_derivatives_give_moments` and `test_mgf_mixed_partial_is_covariance`;
the covariance is independently confirmed by 2-D integration in
`test_covariance_by_integration`. Setting $t_2=0$ recovers the univariate normal
mgf $e^{\mu_X t_1+\frac12\sigma_X^2 t_1^2}$ — another proof the marginal is
normal, and the route by which the mgf technique (`~ST-17`) propagates normality
through linear combinations.

## 7. Contour ellipses

The level sets of $f$ are the level sets of the Mahalanobis form,
$$(\mathbf x-\boldsymbol\mu)^\top\Sigma^{-1}(\mathbf x-\boldsymbol\mu)=c^2,$$
a family of **concentric ellipses** centered at $\boldsymbol\mu$ [PSU L21]. By the
spectral theorem (`~MA-04`) $\Sigma=V\Lambda V^\top$ with orthonormal eigenvectors
$V=[v_1\,v_2]$ and eigenvalues $\lambda_1,\lambda_2>0$; the ellipse has principal
axes along $v_1,v_2$ with **semi-axes $c\sqrt{\lambda_1}$, $c\sqrt{\lambda_2}$**.
Code `ellipse_axes(Sigma, c)` returns the two semi-axes and the tilt
$\theta=\operatorname{atan2}(V_{2j},V_{1j})$ of the major axis; for the $2\times2$
case the tilt also satisfies $\tan 2\theta=2\rho\sigma_X\sigma_Y/(\sigma_X^2-\sigma_Y^2)$.
Their product obeys $\big(c\sqrt{\lambda_1}\big)\big(c\sqrt{\lambda_2}\big)
=c^2\sqrt{\det\Sigma}$, so the ellipse area $\pi\,c^2\sqrt{\det\Sigma}$ grows with
$\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)$ — strong correlation ($|\rho|\to1$)
squeezes the ellipse toward its major axis (the regression line). When $\rho=0$
and $\sigma_X=\sigma_Y$ the ellipses are circles; otherwise they are axis-aligned
ellipses when $\rho=0$ and tilted when $\rho\neq0$. Code `ellipse_points` traces
$w^\top\Sigma^{-1}w=c^2$; every returned point has `mahalanobis_sq` $=c^2$
(`test_contour_ellipse_level_set`).

## Where this goes

- `~ST-14` (covariance, correlation, conditional means / regression) — this module
  is its joint-Gaussian special case: there the regression line is the *best linear
  predictor*; here it is the *exact* conditional mean, and zero correlation finally
  *does* mean independence (§5).
- `~ST-12` (the univariate normal) and `~ST-13` (joint/marginal/conditional pdfs,
  independence) — every marginal (§3) and conditional (§4) here is a `~ST-12`
  normal, assembled by the `~ST-13` operations.
- `~MA-04` (positive-definite matrices, inverse, determinant, eigen-decomposition)
  — the engine behind the matrix form (§2), the existence condition, and the
  contour ellipses (§7).
- `~ST-06` / `~ST-17` (mgf and the mgf technique) — §6's $M(t_1,t_2)$ shows linear
  combinations $aX+bY$ are again normal, the gateway to the normal sampling
  distributions ($\chi^2$, $t$, $F$).
- `~ST-16` (transformations / Jacobians) — the analytic route to §3–§4: the
  bivariate-normal marginals and conditionals also follow from a change of
  variables, and $aX+bY$ from the Jacobian/convolution method.
- `~ST-18` (central limit theorem) and `~SM-01` (Gaussian as maximum-entropy /
  the multivariate Gaussian of statistical mechanics) — *why* this surface is
  ubiquitous: sums of many small independent contributions land on it, and it is
  the least-committal distribution with a given mean and covariance.
