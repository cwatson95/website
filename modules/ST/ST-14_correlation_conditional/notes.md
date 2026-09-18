# ST-14 — Correlation & Conditional Distributions (notes)

A joint distribution (`~ST-13`) carries *everything* about a pair $(X,Y)$, but it
is a high-dimensional object. Two questions reduce it to something usable. First,
**how tightly do $X$ and $Y$ move together?** — answered by one number, the
correlation coefficient $\rho$, built from the **covariance** and bounded by the
**Cauchy–Schwarz inequality** (the linear-algebra fact of `~MA-04`). Second,
**given that $X$ took the value $x$, what is the law of $Y$?** — answered by the
**conditional distribution** $f(y\mid x)$, whose mean $E[Y\mid X=x]$ is the
**regression function**. These two threads meet in the least-squares line, whose
slope is $\rho\,\sigma_Y/\sigma_X$, and in the **law of total expectation**.

Citation key (full details + granularity in `refs.md`): **PSU** = Penn State
STAT 414 OER, lessons **L18** (correlation) and **L19** (conditional
distributions); **HTZ** = Hogg, Tanis & Zimmerman, *Probability and Statistical
Inference* (the text STAT 414 follows), cited at **chapter level**. Every result
is tied to a symbol in `code/correlation_conditional.py`.

## 1. Covariance: the mean product of deviations

Let $\mu_X=E[X]$, $\mu_Y=E[Y]$. The **covariance** is the expected product of the
two deviations from the mean [PSU L18]:
$$\operatorname{Cov}(X,Y)\;=\;E\!\big[(X-\mu_X)(Y-\mu_Y)\big].$$
Expanding the product and using linearity of expectation (`~ST-05`) gives the
**shortcut formula**, the one the code evaluates:
$$\operatorname{Cov}(X,Y)=E[XY]-\mu_X\mu_Y,\qquad
E[XY]=\sum_{i,j}x_i\,y_j\,P_{ij}\ \ \text{or}\ \ \iint xy\,f(x,y)\,dx\,dy .$$
Code: `mean_xy` returns $E[XY]=\texttt{xs @ P @ ys}$ and `covariance(j)` returns
$E[XY]-\mu_X\mu_Y$; `test_covariance_two_formulas_agree` checks the shortcut
against the direct grid sum $\sum_{ij}(x_i-\mu_X)(y_j-\mu_Y)P_{ij}$. Covariance is
**symmetric** and **bilinear**,
$$\operatorname{Cov}(X,Y)=\operatorname{Cov}(Y,X),\qquad
\operatorname{Cov}(aX+b,\,cY+d)=ac\,\operatorname{Cov}(X,Y),$$
and reduces to the variance on the diagonal: $\operatorname{Cov}(X,X)=
E[X^2]-\mu_X^2=\operatorname{Var}(X)$ (code: `test_covariance_of_X_with_itself_is_variance`).
Its sign tells the *direction* of the linear tie — positive if $Y$ tends to be
above its mean when $X$ is, negative otherwise — but its magnitude is in the units
of $X$ times $Y$, so it cannot be compared across problems. That is what $\rho$
fixes.

## 2. The correlation coefficient and $|\rho|\le1$ (Cauchy–Schwarz)

Standardize each variable, $Z_X=(X-\mu_X)/\sigma_X$, $Z_Y=(Y-\mu_Y)/\sigma_Y$, and
define the **correlation coefficient** as the covariance of the standardized
variables [PSU L18]:
$$\boxed{\;\rho \;=\; \operatorname{Cov}(Z_X,Z_Y)\;=\;
\frac{\operatorname{Cov}(X,Y)}{\sigma_X\,\sigma_Y}\;}\qquad(\text{code: }\texttt{correlation(j)}).$$
It is **dimensionless** and **scale/shift invariant**: $\rho(aX+b,cY+d)=
\operatorname{sgn}(ac)\,\rho(X,Y)$, by the bilinearity of §1. The bound $|\rho|\le1$
is the **Cauchy–Schwarz inequality** of `~MA-04` applied to the inner product
$\langle U,V\rangle=E[UV]$ on mean-zero random variables. With $U=X-\mu_X$,
$V=Y-\mu_Y$,
$$\big(E[UV]\big)^2\le E[U^2]\,E[V^2]
\;\Longrightarrow\;\operatorname{Cov}(X,Y)^2\le\operatorname{Var}(X)\operatorname{Var}(Y)
\;\Longrightarrow\;\rho^2\le1 .$$
A clean self-contained proof: for any $t$ the variance of $U-tV$ is nonnegative,
$$0\le E\big[(U-tV)^2\big]=E[U^2]-2t\,E[UV]+t^2E[V^2],$$
a quadratic in $t$ with no two distinct real roots, so its discriminant is
$\le0$: $\big(E[UV]\big)^2\le E[U^2]E[V^2]$. **Equality** holds iff the quadratic
has a (double) root $t_\*$, i.e. $E[(U-t_\*V)^2]=0$, meaning $X-\mu_X=t_\*(Y-\mu_Y)$
almost surely — **$X$ and $Y$ are exactly affinely related**. Then $|\rho|=1$,
with $\rho=+1$ for an increasing line and $\rho=-1$ for a decreasing one. Code:
`linear_dependence_example(a,b)` builds $Y=aX+b$ and `correlation` returns
$\operatorname{sgn}(a)$ exactly (`test_correlation_definition_and_cauchy_schwarz`).

## 3. The covariance matrix view (`~MA-04`)

Collect the second moments into the $2\times2$ **covariance matrix**
$$\Sigma=\begin{pmatrix}\operatorname{Var}(X)&\operatorname{Cov}(X,Y)\\[2pt]
\operatorname{Cov}(X,Y)&\operatorname{Var}(Y)\end{pmatrix}
=\begin{pmatrix}\sigma_X^2&\rho\,\sigma_X\sigma_Y\\[2pt]\rho\,\sigma_X\sigma_Y&\sigma_Y^2\end{pmatrix}.$$
For any real $\mathbf a=(a_1,a_2)$, $\mathbf a^{\!\top}\Sigma\,\mathbf a=
\operatorname{Var}(a_1X+a_2Y)\ge0$, so **$\Sigma$ is positive semidefinite** — the
matrix incarnation of Cauchy–Schwarz. Its determinant is
$$\det\Sigma=\sigma_X^2\sigma_Y^2-\operatorname{Cov}(X,Y)^2
=\sigma_X^2\sigma_Y^2\,(1-\rho^2)\;\ge\;0,$$
and $\det\Sigma\ge0$ **is exactly** the statement $|\rho|\le1$; the degenerate case
$\det\Sigma=0$ ($\rho=\pm1$) is the affine-dependence case of §2, where the
distribution collapses onto a line. Code: `covariance_matrix(j)`; the identity
$\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)$ and PSD-ness are checked in
`test_covariance_matrix_psd_iff_rho_bound`. This $\Sigma$ is the kernel of the
**bivariate normal** density of `~ST-15`.

## 4. Independence $\Rightarrow\rho=0$ — and why the converse fails

If $X$ and $Y$ are **independent** then $f(x,y)=f_X(x)f_Y(y)$ (`~ST-13`), so the
cross moment factors,
$$E[XY]=\sum_{i,j}x_iy_j\,f_X(x_i)f_Y(y_j)=\Big(\sum_i x_if_X(x_i)\Big)\Big(\sum_j y_jf_Y(y_j)\Big)=E[X]\,E[Y],$$
hence $\operatorname{Cov}(X,Y)=0$ and $\rho=0$: independent variables are
**uncorrelated** (code: `product_joint`, `test_independence_implies_zero_correlation`).
The **converse is false** — $\rho$ measures only *linear* association. The standing
counterexample (code: `uncorrelated_dependent_example`): let $X$ be uniform on
$\{-1,0,1\}$ and $Y=X^2$. Then $E[X]=0$ and $E[XY]=E[X^3]=0$, so
$$\operatorname{Cov}(X,Y)=E[X^3]-E[X]\,E[X^2]=0,\qquad \rho=0,$$
yet $Y$ is a *deterministic function* of $X$ — as dependent as two variables can
be. The factorization test `is_independent` returns `False`, and the conditional
means $E[Y\mid X=-1]=E[Y\mid X=1]=1\ne0=E[Y\mid X=0]$ vary with $x$
(`test_uncorrelated_but_dependent_counterexample`). Moral: $\rho=0$ rules out a
*linear* trend, nothing more. (Under joint normality, §3's $\Sigma$ governs
everything and $\rho=0$ **does** give independence — that special case is `~ST-15`.)

## 5. Conditional distributions: slicing the joint

Conditioning on an event of positive probability is the elementary rule
$P(B\mid A)=P(A\cap B)/P(A)$ applied at the level of mass functions. The
**conditional pmf** of $Y$ given $X=x$ (with $f_X(x)>0$) is [PSU L19]
$$f_{Y\mid X}(y\mid x)=\frac{f(x,y)}{f_X(x)},\qquad
f_X(x)=\sum_y f(x,y)\ \text{(or }\textstyle\int f(x,y)\,dy\text{)} .$$
It is a *bona fide* distribution in $y$: nonnegative, and
$\sum_y f(y\mid x)=\big(\sum_y f(x,y)\big)/f_X(x)=f_X(x)/f_X(x)=1$. The same
formula defines the **conditional pdf** in the continuous case, with the marginal
$f_X(x)=\int f(x,y)\,dy$ in the denominator. Code: `conditional_pmf(j,x)` returns
$\texttt{(ys, P[i,:]/f\_X(x))}$ and `cont_conditional_expectation` divides by the
integrated marginal `cont_marginal_x`; the validity $\sum f(y\mid x)=1$ is
`test_conditional_pmf_is_a_valid_distribution`. For the running example
$f(x,y)=(x+y)/32$ on $x\in\{1,2\},\,y\in\{1,2,3,4\}$, conditioning on $X=1$ gives
$f(y\mid1)=(1+y)/14$.

## 6. Conditional expectation and the regression function

The mean of the conditional distribution is the **conditional expectation**
[PSU L19]
$$E[Y\mid X=x]=\sum_y y\,f_{Y\mid X}(y\mid x)
\quad\Big(\text{cont.: }\int y\,f(y\mid x)\,dy\Big).$$
As a function of the conditioning value, $x\mapsto E[Y\mid X=x]$ is the
**regression function** — the curve of "best mean prediction" of $Y$ from $X$. It
need **not** be linear. For the discrete example,
$$E[Y\mid X=1]=\sum_{y=1}^{4}y\,\frac{1+y}{14}=\frac{40}{14}=\frac{20}{7},\qquad
E[Y\mid X=2]=\sum_{y=1}^{4}y\,\frac{2+y}{18}=\frac{50}{18}=\frac{25}{9}.$$
For the continuous $f(x,y)=x+y$ on the unit square, $f_X(x)=x+\tfrac12$ and
$$E[Y\mid X=x]=\frac{\int_0^1 y(x+y)\,dy}{x+\tfrac12}
=\frac{\tfrac{x}{2}+\tfrac13}{x+\tfrac12}\qquad(\text{e.g. }x{=}0:\tfrac23,\ \ x{=}1:\tfrac59),$$
a genuinely **nonlinear** regression function (code:
`conditional_expectation`, `regression_function`, `cont_conditional_expectation`;
`test_conditional_expectation_values`, `test_continuous_conditional_and_tower`).

## 7. The law of total expectation (the tower property)

$E[Y\mid X]$ is itself a random variable (a function of $X$). Averaging it over the
distribution of $X$ recovers the plain mean of $Y$ — the **law of total
expectation** [PSU L19, HTZ Ch. 4]:
$$\boxed{\,E\big[E[Y\mid X]\big]=E[Y]\,},\qquad
\sum_x E[Y\mid X=x]\,f_X(x)=\sum_x\Big(\sum_y y\,\frac{f(x,y)}{f_X(x)}\Big)f_X(x)
=\sum_{x,y}y\,f(x,y)=E[Y].$$
The cancellation of $f_X(x)$ is the whole proof: conditioning splits the sum by
$x$, summing back over $x$ reassembles the joint. Code:
`law_of_total_expectation(j)` forms $\sum_iE[Y\mid X=x_i]f_X(x_i)$ and
`test_law_of_total_expectation` checks it equals `mean_y(j)` on four different
laws (including the $Y=X^2$ counterexample, where it gives
$1\cdot\tfrac13+0\cdot\tfrac13+1\cdot\tfrac13=\tfrac23=E[Y]$). The continuous
version `cont_total_expectation` integrates $E[Y\mid X=x]f_X(x)$ and matches $E[Y]$
($=\tfrac{7}{12}$ for $x+y$).

## 8. The best linear predictor and regression to the mean

Among all *straight lines* $\hat Y=a+bX$, the one minimizing the mean-squared
error $E[(Y-a-bX)^2]$ has [PSU L18, HTZ Ch. 4]
$$b=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}=\rho\,\frac{\sigma_Y}{\sigma_X},
\qquad a=\mu_Y-b\,\mu_X,$$
so the **least-squares line** is
$$\hat Y=\mu_Y+\rho\,\frac{\sigma_Y}{\sigma_X}\,(X-\mu_X)
\quad\Longleftrightarrow\quad
\frac{\hat Y-\mu_Y}{\sigma_Y}=\rho\,\frac{X-\mu_X}{\sigma_X}.$$
Two readings. (i) It always **passes through the means** $(\mu_X,\mu_Y)$ (set
$X=\mu_X$). (ii) On the *standardized* scale the predicted deviation of $Y$ is
$\rho$ times the deviation of $X$; since $|\rho|\le1$, **the prediction is closer
to the mean than $X$ is** — an above-average $X$ predicts an above-average but
*less extreme* $Y$. This is **regression to the mean**, the phenomenon Galton
named: it is forced by $|\rho|\le1$, not by any special data. Code:
`regression_line(j)` $\to(a,b)$ and `best_linear_predictor(j,x)`;
`test_regression_line_through_means_and_slope` checks $a+b\mu_X=\mu_Y$,
$b=\operatorname{Cov}/\operatorname{Var}X=\rho\,\sigma_Y/\sigma_X$, and
`test_regression_to_the_mean` checks the pull on the symmetric $\rho=0.6$ law.
**Caution:** the least-squares *line* (§8) and the *regression function* $E[Y\mid X]$
(§6) coincide only when the latter is linear (e.g. the bivariate normal of
`~ST-15`); in general the line is just the best linear approximation to the curve.

## Where this goes

- `~ST-13` (joint distributions, marginals, independence) — the object this module
  measures ($\rho$) and slices ($f(y\mid x)$); the marginals $f_X,f_Y$ are the
  denominators here.
- `~MA-04` (covariance matrix & Cauchy–Schwarz) — the linear algebra behind
  $|\rho|\le1$ and $\det\Sigma\ge0$; §3 is `~ST-15`'s $\Sigma$ in embryo.
- `~ST-15` (the bivariate normal) — where the regression function *becomes* the
  straight line of §8, the conditionals are Gaussian with constant variance, and
  $\rho=0\Leftrightarrow$ independence; this module is the direct prerequisite.
- `~ST-05` (expectation & variance) and `~ST-06` (the MGF) — the one-variable
  moments generalized to the joint cross moment $E[XY]$ and the joint MGF.
- `~MA-19` (probability & statistics) and `~SM-01` (ensembles & fluctuations) —
  the empirical sample correlation / least-squares fit, and correlations of
  fluctuating observables in statistical mechanics.
