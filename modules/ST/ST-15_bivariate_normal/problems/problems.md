# ST-15 — Problems

Work each by hand, then check with `code/bivariate_normal.py`. Citations in
`../refs.md`; **PSU** = Penn State STAT 414 **Lesson 21**. Unless stated, the
running example is
$$\mu_X=1,\quad \mu_Y=2,\quad \sigma_X=1,\quad \sigma_Y=2,\quad \rho=0.6,$$
so $\Sigma=\left(\begin{smallmatrix}1&1.2\\1.2&4\end{smallmatrix}\right)$ and
$\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)=2.56$.

### P1.  The two forms of the pdf agree  *(PSU L21; `~MA-04`)*
Write the bivariate normal density at $(x,y)=(1.5,3.0)$ two ways: (i) the explicit
five-parameter form $f=\frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}}
e^{-z/2(1-\rho^2)}$ with $z=u^2-2\rho uv+v^2$, and (ii) the matrix form
$\frac{1}{2\pi\sqrt{\det\Sigma}}e^{-\frac12 w^\top\Sigma^{-1}w}$. Using
$u=v=0.5$, get $z=0.25-2(0.6)(0.25)+0.25=0.2$, exponent $-z/2(1-\rho^2)=
-0.2/1.28=-0.15625$, prefactor $1/(2\pi\cdot1\cdot2\cdot0.8)=0.099472$, so
$f=0.099472\,e^{-0.15625}$. Show the matrix form gives the same number because
$w^\top\Sigma^{-1}w=z/(1-\rho^2)=0.3125$ and $\det\Sigma=2.56$.
*Check:* `bivariate_normal_pdf(1.5,3.0,1,2,1,2,0.6)` $=0.08508277$ equals
`bivariate_normal_pdf_cov(1.5,3.0,(1,2),covariance_matrix(1,2,0.6))`; and
`mahalanobis_sq(1.5,3.0,1,2,1,2,0.6)` $=0.3125$.

**Solution.** With $u=(1.5-1)/1=0.5$ and $v=(3-2)/2=0.5$, the explicit form needs
$$z=u^2-2\rho uv+v^2=0.25-2(0.6)(0.25)+0.25=0.2,\qquad \frac{-z}{2(1-\rho^2)}=\frac{-0.2}{1.28}=-0.15625,$$
with prefactor $\tfrac{1}{2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}}=\tfrac{1}{2\pi(1)(2)(0.8)}=0.099472$,
so $f=0.099472\,e^{-0.15625}=0.08508$. The matrix form has the same exponent because
$w^\top\Sigma^{-1}w=z/(1-\rho^2)=0.2/0.64=0.3125$, and the same prefactor because
$2\pi\sqrt{\det\Sigma}=2\pi\sqrt{2.56}=3.2\pi$ equals
$2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}=3.2\pi$. Hence
`bivariate_normal_pdf(1.5,3.0,1,2,1,2,0.6)` $=$ `bivariate_normal_pdf_cov(...)` $=0.08508277$,
with `mahalanobis_sq(...)` $=0.3125$.

### P2.  When does $\Sigma$ define a distribution?  *(`~MA-04`)*
Show $\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)$ and that, by Sylvester's
criterion, $\Sigma$ is positive-definite iff its leading minors $\sigma_X^2$ and
$\det\Sigma$ are both positive — i.e. iff $|\rho|<1$. Conclude the density exists
exactly on $-1<\rho<1$, and that at $\rho=\pm1$ the matrix is singular and the
mass collapses onto a line (degenerate case). Verify you can read $\rho$ back off
$\Sigma$ as $\Sigma_{xy}/(\sigma_X\sigma_Y)$. *Check:* with `S=covariance_matrix(1,2,0.6)`,
`numpy.linalg.det(S)` $=2.56$, `correlation(S)` $=0.6$, `is_positive_definite(S)`
$=$ `True`; while `is_positive_definite(covariance_matrix(1,2,1.0))` $=$ `False`.

**Solution.** Expanding, $\det\Sigma=\sigma_X^2\sigma_Y^2-(\rho\sigma_X\sigma_Y)^2=\sigma_X^2\sigma_Y^2(1-\rho^2)$.
Sylvester's criterion makes $\Sigma$ positive-definite iff both leading minors are
positive:
$$\sigma_X^2>0\ (\text{automatic}),\qquad \det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)>0\iff|\rho|<1.$$
So the density — which needs $\Sigma^{-1}$ and $\sqrt{\det\Sigma}$ — exists exactly on
$-1<\rho<1$; at $\rho=\pm1$ the matrix is singular and the mass collapses onto the line
$v=\pm u$. The correlation is read back as $\Sigma_{xy}/(\sigma_X\sigma_Y)=\rho$. With
`S=covariance_matrix(1,2,0.6)`: `numpy.linalg.det(S)` $=2.56$, `correlation(S)` $=0.6$,
`is_positive_definite(S)` $=$ `True`, while
`is_positive_definite(covariance_matrix(1,2,1.0))` $=$ `False`.

### P3.  Both marginals are normal  *(PSU L21; `~ST-12`)*
By completing the square $z=(v-\rho u)^2+(1-\rho^2)u^2$ and integrating out $y$,
show $f_X(x)=\frac{1}{\sigma_X\sqrt{2\pi}}e^{-(x-\mu_X)^2/2\sigma_X^2}$, i.e.
$X\sim N(1,1)$. Evaluate at the mean $x=\mu_X=1$: $f_X(1)=1/\sqrt{2\pi}=0.398942$.
(The inner $y$-integral is a normal density and equals $1$.) *Check:*
`marginal_pdf_x(1,1,1)` $=0.398942$, and the numerical integral
`_integrate(lambda y: bivariate_normal_pdf(1,y,1,2,1,2,0.6), -14,18)` $\approx0.398942$
(this is exactly the assertion in `test_marginal_x_is_normal`).

**Solution.** Complete the square in $v$ inside the exponent,
$z=u^2-2\rho uv+v^2=(v-\rho u)^2+(1-\rho^2)u^2$. The $(1-\rho^2)u^2$ term cancels the
$1/(1-\rho^2)$ and leaves $e^{-u^2/2}$; what remains is a normal density in $y$ that
integrates to $1$:
$$f_X(x)=\int_{-\infty}^\infty f\,dy=\frac{e^{-u^2/2}}{\sigma_X\sqrt{2\pi}}\underbrace{\int_{-\infty}^\infty\frac{\exp\!\big(-(v-\rho u)^2/2(1-\rho^2)\big)}{\sigma_Y\sqrt{2\pi}\sqrt{1-\rho^2}}\,dy}_{=\,1}=\frac{1}{\sigma_X\sqrt{2\pi}}e^{-(x-\mu_X)^2/2\sigma_X^2},$$
so $X\sim N(\mu_X,\sigma_X^2)=N(1,1)$. At the mean, $f_X(1)=1/\sqrt{2\pi}=0.398942$. This
is `marginal_pdf_x(1,1,1)` $=0.398942$, equal to the direct numerical integral of the
joint over $y$.

### P4.  The conditional and the regression line  *(PSU L21; `~ST-14`)*
Divide the joint by $f_X$ to show $Y\mid X=x\sim N\!\big(\mu_Y+\rho\frac{\sigma_Y}
{\sigma_X}(x-\mu_X),\ \sigma_Y^2(1-\rho^2)\big)$. For our numbers the conditional
mean is $2+1.2\,(x-1)$ (slope $\rho\sigma_Y/\sigma_X=1.2$) and the conditional
variance is $4(1-0.36)=2.56$, **independent of $x$**. Evaluate at $x=1.5$ and at
$x=3.0$. *Check:* `conditional_params(1.5,1,2,1,2,0.6)` $=(2.6,\,2.56)$ and
`conditional_params(3.0,1,2,1,2,0.6)` $=(4.4,\,2.56)$ — same variance, mean on the
line.

**Solution.** Dividing the joint by $f_X$ removes the $e^{-u^2/2}$ factor found in P3
and leaves precisely the completed square as a normal density in $y$:
$$Y\mid X=x\ \sim\ N\!\Big(\mu_Y+\rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X),\ \sigma_Y^2(1-\rho^2)\Big).$$
For our numbers the mean is $2+0.6\cdot\tfrac21(x-1)=2+1.2(x-1)$ (slope
$\rho\sigma_Y/\sigma_X=1.2$) and the variance is $4(1-0.36)=2.56$, the *same for every*
$x$ (homoscedastic). Evaluating: at $x=1.5$, mean $=2+1.2(0.5)=2.6$; at $x=3.0$, mean
$=2+1.2(2)=4.4$. Hence `conditional_params(1.5,1,2,1,2,0.6)` $=(2.6,2.56)$ and
`conditional_params(3.0,1,2,1,2,0.6)` $=(4.4,2.56)$.

### P5.  Regression to the mean and the shrink factor  *(PSU L21; `~ST-14`)*
Standardize: if $X$ sits $k$ standard deviations above its mean, show the
predicted $Y$ sits only $\rho k$ standard deviations above *its* mean, since
$\frac{E[Y\mid X=x]-\mu_Y}{\sigma_Y}=\rho\,\frac{x-\mu_X}{\sigma_X}$. Take
$x=\mu_X+2\sigma_X=3$ (a $+2\sigma$ outlier in $X$): the predicted $Y$ is only
$\rho\cdot2=1.2$ standard deviations above $\mu_Y$ — **regression to the mean**.
Also note the conditional variance is the marginal variance shrunk by $1-\rho^2$,
so $X$ explains a fraction $\rho^2=0.36$ of $Y$'s variance. *Check:*
`conditional_params(3.0,1,2,1,2,0.6)[0]` $=4.4$, and $(4.4-\mu_Y)/\sigma_Y=
(4.4-2)/2=1.2=\rho\cdot2$.

**Solution.** Subtract $\mu_Y$ and divide by $\sigma_Y$ in the P4 regression line:
$$\frac{E[Y\mid X=x]-\mu_Y}{\sigma_Y}=\rho\,\frac{x-\mu_X}{\sigma_X},$$
so an $x$ sitting $k$ standard deviations above $\mu_X$ predicts a $Y$ only $\rho k$
standard deviations above $\mu_Y$. Taking $x=\mu_X+2\sigma_X=3$ (a $+2\sigma$ outlier),
the predicted $Y$ is $\rho\cdot2=1.2$ standard deviations above $\mu_Y$ — pulled toward
the mean since $|\rho|<1$. Equivalently the conditional variance is the marginal
$\sigma_Y^2$ shrunk by $1-\rho^2=0.64$, so $X$ explains the fraction $\rho^2=0.36$ of
$Y$'s variance. Numerically `conditional_params(3.0,1,2,1,2,0.6)[0]` $=4.4$, and
$(4.4-2)/2=1.2=\rho\cdot2$.

### P6.  $\rho=0$ is independence (here)  *(PSU L21; contrast `~ST-14`)*
For a *general* joint distribution $\mathrm{Cov}=0$ does **not** imply
independence. Show that for the bivariate normal it does: setting $\rho=0$ kills
the cross term and $\sqrt{1-\rho^2}=1$, so $f(x,y)=f_X(x)f_Y(y)$. Verify at
$(x,y)=(0.5,3.0)$ that the $\rho=0$ joint equals the product of the marginals
$N(1,1)$ and $N(2,4)$. *Check:* `bivariate_normal_pdf(0.5,3.0,1,2,1,2,0.0)`
$=0.06197500$ equals `marginal_pdf_x(0.5,1,1)*marginal_pdf_y(3.0,2,2)`
$=0.06197500$; with $\rho=0.6$ the joint no longer equals that product.

**Solution.** Setting $\rho=0$ kills the cross term and makes $\sqrt{1-\rho^2}=1$, so the
quadratic separates, $z=u^2+v^2$, and the density splits into its marginals:
$$f(x,y)\big|_{\rho=0}=\frac{e^{-u^2/2}}{\sigma_X\sqrt{2\pi}}\cdot\frac{e^{-v^2/2}}{\sigma_Y\sqrt{2\pi}}=f_X(x)\,f_Y(y),$$
which is independence. This is special to the Gaussian: it is fixed by its first two
moments, so removing the only off-diagonal second moment removes *all* dependence
(unlike the `~ST-14` counterexample). At $(0.5,3.0)$ the $\rho=0$ joint equals
$f_X(0.5)f_Y(3.0)$ with $X\sim N(1,1),\,Y\sim N(2,4)$, so
`bivariate_normal_pdf(0.5,3.0,1,2,1,2,0.0)` $=$ `marginal_pdf_x(0.5,1,1)*marginal_pdf_y(3.0,2,2)`
$=0.06197500$, whereas with $\rho=0.6$ it no longer factors.

### P7.  The mgf delivers the moments  *(PSU L21; `~ST-06`)*
The joint mgf is $M(t_1,t_2)=\exp\!\big(\mu_X t_1+\mu_Y t_2+\tfrac12(\sigma_X^2 t_1^2
+2\rho\sigma_X\sigma_Y t_1t_2+\sigma_Y^2 t_2^2)\big)$. Confirm $M(0,0)=1$, then show
$\partial_{t_1}M|_0=\mu_X$, $\partial^2_{t_1}M|_0-\mu_X^2=\sigma_X^2$, and the mixed
partial $\partial_{t_1}\partial_{t_2}M|_0-\mu_X\mu_Y=\mathrm{Cov}(X,Y)=\rho\sigma_X
\sigma_Y=1.2$. As a numeric anchor evaluate the exponent at $t_1=t_2=0.1$:
$0.1+0.2+\tfrac12(0.01+0.024+0.04)=0.337$, so $M=e^{0.337}=1.40074$. *Check:*
`mgf(0,0,1,2,1,2,0.6)` $=1.0$ and `mgf(0.1,0.1,1,2,1,2,0.6)` $=1.400739$; the
finite-difference moment/covariance identities are asserted in
`test_mgf_derivatives_give_moments` and `test_mgf_mixed_partial_is_covariance`.

**Solution.** At the origin every term in the exponent vanishes, so $M(0,0)=e^0=1$.
Differentiating
$M=\exp(\mu_Xt_1+\mu_Yt_2+\tfrac12(\sigma_X^2t_1^2+2\rho\sigma_X\sigma_Yt_1t_2+\sigma_Y^2t_2^2))$
brings down the bracketed factor; evaluated at $0$,
$$\partial_{t_1}M|_0=\mu_X,\qquad \partial^2_{t_1}M|_0-\mu_X^2=\sigma_X^2,\qquad \partial_{t_1}\partial_{t_2}M|_0-\mu_X\mu_Y=\rho\sigma_X\sigma_Y=1.2,$$
the last because the mixed partial produces $\mu_X\mu_Y+\rho\sigma_X\sigma_Y$. As a
numeric anchor, at $t_1=t_2=0.1$ the exponent is
$0.1+0.2+\tfrac12(0.01+0.024+0.04)=0.337$, so $M=e^{0.337}=1.40074$. These give
`mgf(0,0,1,2,1,2,0.6)` $=1.0$ and `mgf(0.1,0.1,1,2,1,2,0.6)` $=1.400739$, with the
derivative identities confirmed by finite differences.

### P8.  Contour ellipses and their area  *(PSU L21; `~MA-04`)*
The constant-density curves solve $w^\top\Sigma^{-1}w=c^2$. Diagonalize
$\Sigma=V\Lambda V^\top$; the ellipse has semi-axes $c\sqrt{\lambda_1},
c\sqrt{\lambda_2}$ along the eigenvectors, so its area is $\pi c^2\sqrt{\lambda_1
\lambda_2}=\pi c^2\sqrt{\det\Sigma}$. For our $\Sigma$ the eigenvalues are
$\lambda\approx\{0.579,4.421\}$; the $c=1$ ellipse has semi-axes
$\approx\{0.761,2.103\}$ tilted $\approx70.7^\circ$ from the $x$-axis, with
$a\,b=\sqrt{\det\Sigma}=\sqrt{2.56}=1.6$. Confirm every point on it has
Mahalanobis distance squared equal to $1$. *Check:* `ellipse_axes(covariance_matrix(1,2,0.6),1.0)`
$\approx(2.1026,\,0.7610,\,1.2334\,\text{rad})$ with product $2.1026\times0.7610=1.6$;
and for points from `ellipse_points(1,2,1,2,0.6,c=1)`, `mahalanobis_sq(...)` $=1.0$
at each (`test_contour_ellipse_level_set`).

**Solution.** A constant-density curve is a level set $w^\top\Sigma^{-1}w=c^2$.
Diagonalizing $\Sigma=V\Lambda V^\top$ aligns it with the eigenvectors, where it reads
$(w_1')^2/\lambda_1+(w_2')^2/\lambda_2=c^2$ — an ellipse with semi-axes
$c\sqrt{\lambda_1},c\sqrt{\lambda_2}$, hence area
$$\pi(c\sqrt{\lambda_1})(c\sqrt{\lambda_2})=\pi c^2\sqrt{\lambda_1\lambda_2}=\pi c^2\sqrt{\det\Sigma}.$$
For $\Sigma=\left(\begin{smallmatrix}1&1.2\\1.2&4\end{smallmatrix}\right)$ the eigenvalues
are $\lambda=2.5\pm\sqrt{1.5^2+1.2^2}=\{4.421,0.579\}$, so the $c=1$ ellipse has
semi-axes $\{2.1026,0.7610\}$ with product
$2.1026\times0.7610=1.6=\sqrt{2.56}=\sqrt{\det\Sigma}$, tilted $\approx70.7^\circ$ along
the major eigenvector; every point on it has $w^\top\Sigma^{-1}w=1$ by definition. This
is `ellipse_axes(covariance_matrix(1,2,0.6),1.0)` $\approx(2.1026,0.7610,1.2334)$ with
axis product $1.6$, and `mahalanobis_sq(...)` $=1.0$ at each `ellipse_points`.
