# ST-14 — Problems

Work each by hand, then check with `code/correlation_conditional.py`. Citations in
`../refs.md`; **PSU** = STAT 414 Lessons **L18** (correlation) and **L19**
(conditional distributions). The running discrete example is
$$f(x,y)=\frac{x+y}{32},\qquad x\in\{1,2\},\ y\in\{1,2,3,4\}\qquad(\texttt{demo\_joint()}),$$
with marginals $f_X=\big(\tfrac{7}{16},\tfrac{9}{16}\big)$ and
$f_Y(y)=\tfrac{3+2y}{32}$.

### P1.  Covariance from a joint table  *(PSU L18)*
Using the shortcut $\operatorname{Cov}(X,Y)=E[XY]-E[X]E[Y]$, show for the demo
joint that $E[X]=\tfrac{25}{16}=1.5625$, $E[Y]=\tfrac{45}{16}=2.8125$, and
$E[XY]=\tfrac{35}{8}=4.375$, hence
$$\operatorname{Cov}(X,Y)=\frac{35}{8}-\frac{25}{16}\cdot\frac{45}{16}
=\frac{1120-1125}{256}=-\frac{5}{256}.$$
The negative sign says larger $X$ goes (weakly) with smaller $Y$. *Check:*
`covariance(demo_joint())` $=-0.01953125=-5/256$; `mean_x`, `mean_y`, `mean_xy`
give $1.5625,\,2.8125,\,4.375$.

**Solution.** The shortcut $\operatorname{Cov}=E[XY]-E[X]E[Y]$ needs three moments.
From the marginals $f_X=(\tfrac{14}{32},\tfrac{18}{32})$ and $f_Y(y)=\tfrac{3+2y}{32}$,
$E[X]=\tfrac{50}{32}=\tfrac{25}{16}=1.5625$, $E[Y]=\tfrac{90}{32}=\tfrac{45}{16}=2.8125$,
and the full table gives $E[XY]=\tfrac{140}{32}=\tfrac{35}{8}=4.375$. Over the common
denominator $256$,
$$\operatorname{Cov}(X,Y)=\frac{35}{8}-\frac{25}{16}\cdot\frac{45}{16}=\frac{1120-1125}{256}=-\frac{5}{256}=-0.01953.$$
The negative sign says a larger $X$ accompanies a slightly smaller $Y$. This is
`covariance(demo_joint())` $=-0.01953125$ with `mean_x`, `mean_y`, `mean_xy`
$=1.5625,2.8125,4.375$.

### P2.  Correlation and the $|\rho|\le1$ bound  *(PSU L18; `~MA-04`)*
Rescale the covariance to the dimensionless $\rho=\operatorname{Cov}/(\sigma_X\sigma_Y)$.
With $\operatorname{Var}X=\tfrac{63}{256}$ and $\operatorname{Var}Y=\tfrac{295}{256}$,
$$\rho=\frac{-5/256}{\sqrt{(63/256)(295/256)}}=\frac{-5}{\sqrt{18585}}\approx-0.03668,$$
comfortably inside $[-1,1]$ — a *weak* negative linear association. Explain why
Cauchy–Schwarz ($\det\Sigma=\sigma_X^2\sigma_Y^2(1-\rho^2)\ge0$) guarantees the
bound. *Check:* `correlation(demo_joint())` $\approx-0.036677$ and
`abs(correlation(...)) <= 1`; `covariance_matrix(...)` has determinant
$\sigma_X^2\sigma_Y^2-\operatorname{Cov}^2\approx0.2832>0$.

**Solution.** Dividing the covariance by the two standard deviations removes its
units. With $\operatorname{Var}X=E[X^2]-\mu_X^2=\tfrac{86}{32}-(\tfrac{25}{16})^2=\tfrac{63}{256}$
and $\operatorname{Var}Y=\tfrac{290}{32}-(\tfrac{45}{16})^2=\tfrac{295}{256}$,
$$\rho=\frac{\operatorname{Cov}}{\sigma_X\sigma_Y}=\frac{-5/256}{\sqrt{(63/256)(295/256)}}=\frac{-5}{\sqrt{18585}}\approx-0.03668,$$
a weak negative linear association, safely inside $[-1,1]$. The bound is
Cauchy–Schwarz in matrix form: $\det\Sigma=\sigma_X^2\sigma_Y^2-\operatorname{Cov}^2=\sigma_X^2\sigma_Y^2(1-\rho^2)\ge0$
forces $\rho^2\le1$. Numerically `correlation(demo_joint())` $\approx-0.036677$ with
`abs(...) <= 1`, and $\det\Sigma=\tfrac{18585-25}{256^2}\approx0.2832>0$.

### P3.  When does $|\rho|=1$?  The Cauchy–Schwarz equality case  *(PSU L18)*
Prove that $|\rho|=1$ **iff** $Y=aX+b$ almost surely, with $\rho=\operatorname{sgn}(a)$
(the equality case of $0\le E[(U-tV)^2]$, $U=X-\mu_X$, $V=Y-\mu_Y$). Confirm on
two deterministic lines $Y=2X+1$ and $Y=-3X+5$. *Check:*
`correlation(linear_dependence_example(2.0, 1.0))` $=1.0$ and
`correlation(linear_dependence_example(-3.0, 5.0))` $=-1.0$.

**Solution.** Let $U=X-\mu_X$, $V=Y-\mu_Y$. For every $t$,
$0\le E[(U-tV)^2]=E[U^2]-2t\,E[UV]+t^2E[V^2]$; a quadratic in $t$ that never dips below
zero has discriminant $\le0$, i.e. $(E[UV])^2\le E[U^2]E[V^2]$ — exactly $|\rho|\le1$.
**Equality** needs a double root $t_\*$, where
$$E\big[(U-t_\*V)^2\big]=0\ \Longrightarrow\ U=t_\*V\ \text{a.s.}\ \Longrightarrow\ X-\mu_X=t_\*(Y-\mu_Y),$$
so $X,Y$ lie on a line $Y=aX+b$ and $\rho=\operatorname{sgn}(a)$ (rescaling flips the
sign, not the magnitude). Thus the deterministic lines give
`correlation(linear_dependence_example(2.0, 1.0))` $=1.0$ and
`correlation(linear_dependence_example(-3.0, 5.0))` $=-1.0$.

### P4.  Independence $\Rightarrow\rho=0$ — but not conversely  *(PSU L18)*
First show that independence makes $E[XY]=E[X]E[Y]$, so $\rho=0$. Then take
$X\sim U\{-1,0,1\}$ and $Y=X^2$: compute $E[X]=0$, $E[XY]=E[X^3]=0$, so
$\operatorname{Cov}=0$ and $\rho=0$ — yet $Y$ is a *function* of $X$ (maximally
dependent). Explain why $\rho$ misses this: the dependence is purely **quadratic**,
invisible to a linear measure. *Check:* with `u = uncorrelated_dependent_example()`,
`covariance(u)` $=0.0$, `correlation(u)` $=0.0$, but `is_independent(u)` $=$ `False`;
and the conditional means differ, `conditional_expectation(u, -1)` $=1$,
`conditional_expectation(u, 0)` $=0$, `conditional_expectation(u, 1)` $=1$.

**Solution.** If $X\perp Y$ then $f(x,y)=f_X(x)f_Y(y)$, so the cross moment splits,
$E[XY]=\sum_{x,y}xy\,f_X(x)f_Y(y)=E[X]E[Y]$, giving $\operatorname{Cov}=0$ and $\rho=0$.
The converse fails: take $X$ uniform on $\{-1,0,1\}$ and $Y=X^2$. By symmetry
$E[X]=0$ and $E[XY]=E[X^3]=0$, so
$$\operatorname{Cov}(X,Y)=E[X^3]-E[X]\,E[X^2]=0,\qquad \rho=0,$$
yet $Y$ is a deterministic function of $X$. The point: $\rho$ sees only a *linear*
trend, and here the dependence is purely quadratic (symmetric, hence zero slope).
Conditioning exposes it — `conditional_expectation(u, -1)` $=1$, `(u, 0)` $=0$,
`(u, 1)` $=1$ vary with $x$ — while `covariance(u)` $=$ `correlation(u)` $=0.0$ and
`is_independent(u)` $=$ `False`.

### P5.  Conditional pmf and conditional expectation  *(PSU L19)*
For the demo joint, condition on $X=1$: $f(y\mid 1)=f(1,y)/f_X(1)=\big(\tfrac{1+y}{32}\big)
/\big(\tfrac{14}{32}\big)=\tfrac{1+y}{14}$, a valid pmf ($\sum_{y=1}^4\tfrac{1+y}{14}=1$).
Its mean is the regression function at $x=1$:
$$E[Y\mid X=1]=\sum_{y=1}^{4}y\,\frac{1+y}{14}=\frac{40}{14}=\frac{20}{7}\approx2.857,
\qquad E[Y\mid X=2]=\frac{50}{18}=\frac{25}{9}\approx2.778 .$$
*Check:* `conditional_pmf(demo_joint(), 1)` returns probabilities
$\big(\tfrac{2}{14},\tfrac{3}{14},\tfrac{4}{14},\tfrac{5}{14}\big)$ summing to $1$;
`conditional_expectation(demo_joint(), 1)` $\approx2.857143=20/7$ and
`...(demo_joint(), 2)` $\approx2.777778=25/9$.

**Solution.** Slice the joint at $X=1$ and renormalize by $f_X(1)=\tfrac{14}{32}$:
$$f(y\mid1)=\frac{f(1,y)}{f_X(1)}=\frac{(1+y)/32}{14/32}=\frac{1+y}{14},$$
giving probabilities $\tfrac2{14},\tfrac3{14},\tfrac4{14},\tfrac5{14}$ that sum to
$\tfrac{14}{14}=1$ — a valid pmf. Its mean is the regression value at $x=1$:
$E[Y\mid X{=}1]=\sum_{y=1}^4 y\tfrac{1+y}{14}=\tfrac{2+6+12+20}{14}=\tfrac{40}{14}=\tfrac{20}{7}\approx2.857$.
The same construction at $X=2$ (denominator $\tfrac{18}{32}$, weights $\tfrac{2+y}{18}$)
gives $E[Y\mid X{=}2]=\tfrac{50}{18}=\tfrac{25}{9}\approx2.778$. These are
`conditional_pmf(demo_joint(), 1)` summing to $1$ and `conditional_expectation`
$\approx2.857143,2.777778$.

### P6.  The law of total expectation  *(PSU L19)*
Verify the tower property $E[E[Y\mid X]]=E[Y]$ for the demo joint by averaging the
conditional means over the marginal of $X$:
$$\frac{20}{7}\cdot\frac{14}{32}+\frac{25}{9}\cdot\frac{18}{32}
=\frac{20\cdot14}{7\cdot32}+\frac{25\cdot18}{9\cdot32}=1.25+1.5625=2.8125=E[Y].$$
Do the same for the $Y=X^2$ counterexample: $1\cdot\tfrac13+0\cdot\tfrac13+1\cdot\tfrac13
=\tfrac23=E[Y]$. *Check:* `law_of_total_expectation(demo_joint())` $=2.8125=$
`mean_y(demo_joint())`; `law_of_total_expectation(uncorrelated_dependent_example())`
$\approx0.6667=2/3$.

**Solution.** The tower property averages the conditional means over the marginal of
$X$. Using $f_X=(\tfrac{14}{32},\tfrac{18}{32})$ and the two regression values of P5,
$$E\big[E[Y\mid X]\big]=\frac{20}{7}\cdot\frac{14}{32}+\frac{25}{9}\cdot\frac{18}{32}=\frac{20\cdot14}{7\cdot32}+\frac{25\cdot18}{9\cdot32}=1.25+1.5625=2.8125=E[Y].$$
The cancellations $14/7=2$ and $18/9=2$ are the proof in miniature: dividing by
$f_X(x)$ to condition and multiplying by it to average undo each other, reassembling
$\sum_{x,y}y\,f(x,y)$. The $Y=X^2$ law works the same way,
$1\cdot\tfrac13+0\cdot\tfrac13+1\cdot\tfrac13=\tfrac23=E[Y]$. Hence
`law_of_total_expectation(demo_joint())` $=2.8125=$ `mean_y(demo_joint())` and
`law_of_total_expectation(uncorrelated_dependent_example())` $\approx0.6667$.

### P7.  The least-squares line and regression to the mean  *(PSU L18)*
The best linear predictor has slope $b=\operatorname{Cov}/\operatorname{Var}X=
\rho\,\sigma_Y/\sigma_X$ and intercept $a=\mu_Y-b\mu_X$. For the demo joint
$b=\tfrac{-5/256}{63/256}=-\tfrac{5}{63}\approx-0.07937$ and
$a\approx2.93651$, and the line passes through $(\mu_X,\mu_Y)=(1.5625,2.8125)$.
Now take the symmetric law on $\{-1,1\}^2$ with $\rho=0.6$ (`regression_to_mean_example()`):
since $\mu_X=\mu_Y=0$ and $\sigma_X=\sigma_Y=1$, an extreme $X=+1$ predicts
$\hat Y=\rho\cdot1=0.6$ — *closer to the mean than $X$*, the **regression-to-the-mean**
effect forced by $|\rho|\le1$. *Check:* `regression_line(demo_joint())`
$\approx(2.93651,\,-0.07937)$; `best_linear_predictor(demo_joint(), 1.5625)`
$\approx2.8125$; for `r = regression_to_mean_example()`, `correlation(r)` $=0.6$ and
`best_linear_predictor(r, 1.0)` $=0.6<1$.

**Solution.** The least-squares slope is
$b=\operatorname{Cov}/\operatorname{Var}X=\tfrac{-5/256}{63/256}=-\tfrac{5}{63}\approx-0.07937$,
and the intercept pins the line to the means,
$a=\mu_Y-b\mu_X=2.8125+\tfrac{5}{63}(1.5625)\approx2.93651$. By construction
$a+b\mu_X=\mu_Y$, so the line passes through $(1.5625,2.8125)$. In standardized form the
shrinkage is explicit,
$$\frac{\hat Y-\mu_Y}{\sigma_Y}=\rho\,\frac{X-\mu_X}{\sigma_X}.$$
For the symmetric $\rho=0.6$ law ($\mu_X=\mu_Y=0$, $\sigma_X=\sigma_Y=1$), a $+1\sigma$
outlier $X=1$ predicts $\hat Y=\rho\cdot1=0.6$ — *less extreme than $X$*, the
regression-to-the-mean effect forced by $|\rho|\le1$. Thus `regression_line(demo_joint())`
$\approx(2.93651,-0.07937)$, `best_linear_predictor(demo_joint(), 1.5625)` $\approx2.8125$,
and for `r` with `correlation(r)` $=0.6$, `best_linear_predictor(r, 1.0)` $=0.6<1$.

### P8.  A continuous law: nonlinear regression  *(PSU L19)*
For $f(x,y)=x+y$ on the unit square, $f_X(x)=x+\tfrac12$, so
$$E[Y\mid X=x]=\frac{\int_0^1 y(x+y)\,dy}{x+\tfrac12}=\frac{\tfrac{x}{2}+\tfrac13}{x+\tfrac12},$$
a **nonlinear** regression function ($\tfrac23$ at $x=0$, $\tfrac59$ at $x=1$).
Show also $E[X]=\tfrac{7}{12}$, $\operatorname{Cov}=-\tfrac{1}{144}$, and
$\rho=-\tfrac{1}{11}$, and confirm the tower $\int_0^1 E[Y\mid X{=}x]f_X(x)\,dx=
E[Y]=\tfrac{7}{12}$. *Check:* with `f = lambda x,y: x+y`, `bd = (0,1,0,1)`:
`cont_covariance(f, bd)` $\approx-0.006944=-1/144$, `cont_correlation(f, bd)`
$\approx-0.0909=-1/11$, `cont_conditional_expectation(f, 0.0, bd)` $\approx0.6667=2/3$,
`cont_conditional_expectation(f, 1.0, bd)` $\approx0.5556=5/9$, and
`cont_total_expectation(f, bd)` $\approx0.5833=7/12$.

**Solution.** With $f_X(x)=x+\tfrac12$ the conditional mean is the ratio
$$E[Y\mid X=x]=\frac{\int_0^1 y(x+y)\,dy}{x+\tfrac12}=\frac{\tfrac{x}{2}+\tfrac13}{x+\tfrac12},$$
a genuinely **nonlinear** function of $x$ ($\tfrac23$ at $x=0$, $\tfrac59$ at $x=1$). For
the moments, $E[X]=\tfrac7{12}$, and with
$\operatorname{Var}X=\operatorname{Var}Y=\tfrac{11}{144}$ and
$\operatorname{Cov}=E[XY]-E[X]E[Y]=\tfrac13-(\tfrac7{12})^2=-\tfrac1{144}$, the
correlation is $\rho=\tfrac{-1/144}{11/144}=-\tfrac1{11}$. The tower closes because the
numerator *is* $E[Y\mid X{=}x]f_X(x)$:
$\int_0^1(\tfrac x2+\tfrac13)\,dx=\tfrac14+\tfrac13=\tfrac7{12}=E[Y]$. These match
`cont_covariance` $\approx-0.006944$, `cont_correlation` $\approx-0.0909$,
`cont_conditional_expectation` $\approx0.6667,0.5556$, and `cont_total_expectation`
$\approx0.5833$.
