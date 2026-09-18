# ST-11 — Exponential, Gamma & Chi-Square Distributions (notes)

The continuous-r.v. toolkit of `~ST-10` — a density $f\ge 0$ with $\int f=1$, a cdf
$F(x)=\int_{-\infty}^x f$, moments $E[g(X)]=\int g\,f$ — is now aimed at one family.
Every distribution here is normalized by a single integral, the **gamma function**
$\Gamma(\alpha)=\int_0^\infty t^{\alpha-1}e^{-t}\,dt$ (`~MA-12`), and every one is a
**waiting time** or a **sum of squares**. The **exponential** is the time to the
first event of a Poisson process (`~ST-09`); the **gamma** is the time to the
$\alpha$-th; the **chi-square** is the sum of squared standard normals that drives
all of sampling theory (`~ST-17`). We derive each pdf, its moments through the
moment-generating function (`~ST-06`), and the identities that knit them together.

Citation key (full details + granularity in `refs.md`): **L15.x** = Penn State
STAT 414 Lesson 15 (*Exponential, Gamma and Chi-Square Distributions*), subsection
$x$; **HTZ** = Hogg, Tanis & Zimmerman, *Probability and Statistical Inference*,
cited at **chapter level** (Ch. 3, continuous distributions). Each result names the
code symbol that evaluates it.

## 1. The gamma function $\Gamma(\alpha)$

Define, for $\alpha>0$, the **gamma function** [L15.1]
$$\Gamma(\alpha)=\int_0^\infty t^{\alpha-1}e^{-t}\,dt .$$
The integral converges at $0$ (since $\alpha-1>-1$) and at $\infty$ (the
exponential beats every power). Integration by parts with $u=t^{\alpha}$,
$dv=e^{-t}dt$ gives the **fundamental recursion**
$$\Gamma(\alpha+1)=\int_0^\infty t^{\alpha}e^{-t}\,dt
=\big[-t^{\alpha}e^{-t}\big]_0^\infty+\alpha\!\int_0^\infty t^{\alpha-1}e^{-t}\,dt
=\alpha\,\Gamma(\alpha).$$
With the base case $\Gamma(1)=\int_0^\infty e^{-t}dt=1$, the recursion makes
$\Gamma$ the continuous interpolant of the factorial,
$$\Gamma(n)=(n-1)!\qquad(n=1,2,3,\dots).$$
A second value we need repeatedly is the half-integer seed
$$\Gamma\!\Big(\tfrac12\Big)=\int_0^\infty t^{-1/2}e^{-t}\,dt
\overset{t=u^2}{=}2\!\int_0^\infty e^{-u^2}\,du=\sqrt\pi,$$
the Gaussian integral (`~ST-12`); combined with the recursion it gives every
half-integer, e.g. $\Gamma(\tfrac72)=\tfrac{5}{2}\cdot\tfrac{3}{2}\cdot\tfrac12\sqrt\pi
=\tfrac{15}{8}\sqrt\pi$. Code: `gamma_function(alpha)` (a thin wrapper on
`math.gamma`), checked against an independent **Lanczos** series `gamma_lanczos(z)`
to $\sim10^{-13}$.

## 2. The exponential distribution

The **exponential** density with rate $\lambda>0$ is [L15.2]
$$f(x)=\lambda e^{-\lambda x},\quad x\ge 0,\qquad
F(x)=\int_0^x\lambda e^{-\lambda u}\,du=1-e^{-\lambda x},\qquad
S(x)=P(X>x)=e^{-\lambda x}.$$
It is the $\alpha=1$ member of §4 (its normalizer is $\Gamma(1)=1$). The
**moment-generating function** (`~ST-06`) is, for $t<\lambda$,
$$M(t)=E[e^{tX}]=\int_0^\infty e^{tx}\lambda e^{-\lambda x}\,dx
=\frac{\lambda}{\lambda-t}=\frac{1}{1-\theta t},\qquad \theta:=\frac1\lambda,$$
where $\theta=1/\lambda$ is the **scale** (mean). Differentiating and setting $t=0$,
$$M'(0)=E[X]=\frac1\lambda=\theta,\qquad
M''(0)=E[X^2]=\frac2{\lambda^2},\qquad
\mathrm{Var}(X)=M''(0)-M'(0)^2=\frac1{\lambda^2}=\theta^2.$$
Code: `exponential_pdf`, `exponential_cdf`, `exponential_survival`,
`exponential_mean` $=1/\lambda$, `exponential_var` $=1/\lambda^2$,
`exponential_mgf` $=\lambda/(\lambda-t)$. The test extracts the mean and variance
both by integrating $x f$, $x^2 f$ and by numerically differentiating $M$ at $0$
($M'(0)=$ mean), so the mgf is verified, not assumed.

## 3. Memorylessness

The exponential is the unique continuous law with **no memory** [L15.2]: a
component that has already survived a time $s$ is *as good as new*. Using the
survival function $S(x)=e^{-\lambda x}$,
$$P(X>s+t\mid X>s)=\frac{P(X>s+t)}{P(X>s)}
=\frac{e^{-\lambda(s+t)}}{e^{-\lambda s}}=e^{-\lambda t}=P(X>t).$$
The waiting time to the next event does not depend on how long you have already
waited — the continuous twin of the **geometric** law's memorylessness (`~ST-08`),
and the reason the Poisson process (`~ST-09`) is "rateless." Code:
`exp_memoryless_check(s, t, lam)` returns the pair $\big(P(X>s+t\mid X>s),\,P(X>t)\big)$;
the test asserts they are equal (e.g. both $=e^{-0.8}=0.449329$ at $\lambda=0.4,t=2$).

## 4. The gamma distribution

Promote the exponential to a two-parameter family by inserting a **shape** $\alpha>0$
[L15.3]. The **gamma** density with shape $\alpha$ and scale $\theta>0$ is
$$f(x)=\frac{1}{\Gamma(\alpha)\,\theta^{\alpha}}\,x^{\alpha-1}e^{-x/\theta},
\qquad x>0 .$$
That this integrates to $1$ is exactly the definition of $\Gamma$: substitute
$u=x/\theta$,
$$\int_0^\infty\frac{x^{\alpha-1}e^{-x/\theta}}{\Gamma(\alpha)\theta^\alpha}\,dx
=\frac{1}{\Gamma(\alpha)}\int_0^\infty u^{\alpha-1}e^{-u}\,du
=\frac{\Gamma(\alpha)}{\Gamma(\alpha)}=1 .$$
The **moment-generating function** comes from the same trick (replace $1/\theta$ by
$1/\theta-t$), valid for $t<1/\theta$:
$$M(t)=\int_0^\infty e^{tx}\frac{x^{\alpha-1}e^{-x/\theta}}{\Gamma(\alpha)\theta^\alpha}dx
=\frac{1}{\theta^\alpha}\Big(\frac1\theta-t\Big)^{-\alpha}=(1-\theta t)^{-\alpha}.$$
Expanding $\ln M=-\alpha\ln(1-\theta t)=\alpha(\theta t+\tfrac12\theta^2t^2+\cdots)$
reads off the cumulants directly:
$$E[X]=M'(0)=\alpha\theta,\qquad
\mathrm{Var}(X)=\alpha\theta^2 .$$
Setting $\alpha=1$ gives $M(t)=(1-\theta t)^{-1}=\lambda/(\lambda-t)$ — the
**exponential** of §2 with $\lambda=1/\theta$. The cdf has no elementary closed
form; it is the **regularized lower incomplete gamma**
$$F(x)=P\!\Big(\alpha,\frac{x}{\theta}\Big)
=\frac{1}{\Gamma(\alpha)}\int_0^{x/\theta}t^{\alpha-1}e^{-t}\,dt .$$
Code: `gamma_pdf(x, alpha, theta)`, `gamma_mean` $=\alpha\theta$, `gamma_var`
$=\alpha\theta^2$, `gamma_mgf` $=(1-\theta t)^{-\alpha}$, and `gamma_cdf` via
`lower_incomplete_gamma_regularized` (series for $x<\alpha+1$, continued fraction
otherwise). Tests confirm normalization, $E[X]$, $E[X^2]$ by integration and the
mgf derivatives.

## 5. A sum of exponentials is gamma (the Erlang waiting time)

The gamma's deepest meaning: with **integer** shape $\alpha$, it is the sum of
$\alpha$ independent exponentials of common rate, i.e. the waiting time to the
$\alpha$-th Poisson event (`~ST-09`). The cleanest proof is the **mgf technique**
(`~ST-06`, `~ST-17`): mgfs of independent sums multiply, so if
$X_1,\dots,X_\alpha\stackrel{\text{iid}}{\sim}\text{Exp}(\theta)$ then
$$M_{\sum X_i}(t)=\prod_{i=1}^{\alpha}M_{X_i}(t)
=\big(1-\theta t\big)^{-1}\cdots\big(1-\theta t\big)^{-1}
=(1-\theta t)^{-\alpha},$$
which is the **gamma$(\alpha,\theta)$ mgf** of §4 — and by the uniqueness theorem
(`~ST-06`) the sum *is* gamma. For $\alpha=2$ the convolution can be done by hand:
$$f_{X_1+X_2}(x)=\int_0^x\lambda e^{-\lambda y}\,\lambda e^{-\lambda(x-y)}\,dy
=\lambda^2 e^{-\lambda x}\!\int_0^x dy=\lambda^2 x\,e^{-\lambda x},$$
exactly the gamma$(2,1/\lambda)$ density. Code: `convolve_two_exponentials_pdf(x, lam)`
returns $\lambda^2 x e^{-\lambda x}$ (the test matches it to `gamma_pdf(x, 2, 1/lam)`
and to the mgf identity `exponential_mgf**alpha == gamma_mgf`);
`simulate_sum_of_exponentials(alpha, theta)` draws $\alpha$ iid exponentials and
confirms the sample mean $\to\alpha\theta$, variance $\to\alpha\theta^2$.

## 6. The chi-square distribution

The **chi-square** with $r$ **degrees of freedom** is simply the gamma with shape
$\alpha=r/2$ and scale $\theta=2$ [L15.4]:
$$f(x)=\frac{1}{\Gamma(r/2)\,2^{r/2}}\,x^{r/2-1}e^{-x/2},\qquad x>0,\quad
M(t)=(1-2t)^{-r/2}\ \ (t<\tfrac12).$$
The general gamma moments specialize to
$$E[X]=\alpha\theta=\frac r2\cdot 2=r,\qquad
\mathrm{Var}(X)=\alpha\theta^2=\frac r2\cdot 4=2r .$$
Two reductions anchor it. With $r=2$: $\alpha=1,\theta=2$, so $\chi^2_2$ is the
**exponential of mean $2$** ($\lambda=\tfrac12$) — its survival $e^{-x/2}$ is the
familiar half-life curve. With $r=1$: $\chi^2_1=Z^2$ for a standard normal $Z$
(`~ST-12`), the seed of sampling theory; indeed $P(\chi^2_1\le 1)=0.6827$ is the
$68\%$ one-$\sigma$ probability. In general (the headline of `~ST-17`) a sum of $r$
squared independent standard normals is $\chi^2_r$,
$$Z_1,\dots,Z_r\stackrel{\text{iid}}{\sim}N(0,1)\ \Longrightarrow\
\sum_{i=1}^r Z_i^2\sim\chi^2_r ,$$
because each $Z_i^2$ is $\chi^2_1=$ gamma$(\tfrac12,2)$ and shapes add under
convolution (§5). Code: `chi2_pdf(x, r)`$=$`gamma_pdf(x, r/2, 2)`, `chi2_cdf`,
`chi2_mean` $=r$, `chi2_var` $=2r$, `chi2_mgf` $=(1-2t)^{-r/2}$; the test checks the
$\chi^2_2=$Exp$(\tfrac12)$ identity exactly and the mean/variance for several $r$.

## Where this goes

- `~ST-10` (continuous random variables — pdf/cdf/percentile machinery) and
  `~ST-06` (moment-generating functions) are the two pillars this module stands on;
  the gamma function comes from `~MA-12` (special functions), and $\Gamma(\tfrac12)
  =\sqrt\pi$ from the Gaussian integral of `~ST-12`.
- `~ST-09` (the Poisson process): exponential inter-arrival times and gamma/Erlang
  arrival times are the continuous-time face of `~ST-08`'s geometric/negative-binomial
  waiting counts — memorylessness ties §3 to both.
- `~ST-17` (the MGF technique & normal sampling distributions): the §6 fact
  $\chi^2_r=\sum Z_i^2$ launches the chi-square, Student-$t$ and $F$ sampling
  distributions and the inference of mathematical statistics; the sum-of-mgfs
  argument of §5 is the technique itself.
- `~SM-06` (kinetic theory): a gas molecule's kinetic energy $E=\tfrac12 mv^2$ has
  $2E/kT\sim\chi^2_3$ — a gamma of shape $\tfrac32$ — so the mean energy
  $\tfrac32 kT$ is just $\tfrac32\theta$ with $\theta=kT$; the Maxwell speed law is
  the matching chi ($\sqrt{\chi^2_3}$) distribution. The gamma family is the
  statistical-mechanics waiting-time/energy distribution as much as the
  probability-theory one.
