# ST-10 — Continuous Random Variables (notes)

A discrete random variable (`~ST-05`) places lumps of probability on isolated
points: a **mass** $p(x)=P(X=x)$ with $\sum_x p(x)=1$. Many quantities — a waiting
time, a length, a measurement error — instead vary over a *continuum*, where no
single value can carry positive probability (there are too many of them). The fix
is to describe probability not as mass on points but as **density spread over
intervals**: a function $f(x)\ge0$ whose *area* over a set is the probability of
landing in it. Everything in `~ST-05` survives the translation $\sum\to\int$:
masses become densities, the cdf becomes an integral, expectations become
integrals. This module sets up that dictionary and works the simplest continuous
law, the **uniform** $U(a,b)$, end to end.

Citation key (full details + granularity in `refs.md`): **PSU** = Penn State
STAT 414 OER (Lessons 13–14); **HTZ** = Hogg, Tanis & Zimmerman, *Probability and
Statistical Inference* (the text STAT 414 follows); **WMS** = Wackerly, Mendenhall
& Scheaffer; **Ross** = Ross, *A First Course in Probability*. Cited at
**lesson/chapter level** (no page numbers — this trunk has no PDF shelf).

## 1. The probability density function (pdf)

A random variable $X$ is **continuous** if its cdf $F(x)=P(X\le x)$ is a
continuous function that can be written as an integral of a nonnegative
**density** $f$ [PSU L14.1; HTZ Ch. 3]:
$$f(x)\ge 0\quad\text{for all }x,\qquad \int_{-\infty}^{\infty}f(x)\,dx=1 .$$
The two conditions — nonnegativity and **total area one** — are the continuous
analogue of $p(x)\ge0,\ \sum p(x)=1$ in `~ST-05`. Probability is *area under the
curve*: for any set $S$,
$$P(X\in S)=\int_S f(x)\,dx .$$
A crucial reading: $f(x)$ is **not** a probability. It has units of
probability-per-unit-$x$, can exceed $1$ (e.g. $f=\tfrac1{b-a}=5$ on a short
interval), and only becomes a probability once integrated over a width. Code
`pdf_is_normalized(f, a, b)` checks $\int_a^b f=1$ via the midpoint helper
`_integrate` — the same `_integrate` idiom as `~SM-06`.

## 2. The cumulative distribution function (cdf) and $f=F'$

Accumulate the density from the left to get the **cdf** [PSU L14.2; HTZ Ch. 3]:
$$F(x)=P(X\le x)=\int_{-\infty}^{x}f(t)\,dt,
\qquad F(-\infty)=0,\quad F(+\infty)=1,$$
a nondecreasing, continuous function running from $0$ to $1$. By the **fundamental
theorem of calculus** the density is the *slope* of the cdf:
$$f(x)=F'(x).$$
This is the single most useful fact of the module: a pdf and a cdf are derivative
and integral of each other. Code: `cdf_from_pdf(f, x, a)` returns
$F(x)=\int_a^x f$ for a variable with support starting at $a$; numerically
differentiating it (a central difference) recovers $f$, which the test
`test_pdf_is_derivative_of_cdf` verifies on $f(x)=2x$ (whose cdf is exactly
$F(x)=x^2$, $F'=2x$).

## 3. Intervals, and why $P(X=x)=0$

Because the cdf is an integral, interval probabilities are **differences of the
cdf** [PSU L14.2]:
$$P(a<X\le b)=F(b)-F(a)=\int_a^b f(x)\,dx.$$
Now shrink the interval to a point. A single value subtends *zero width*, hence
zero area:
$$P(X=c)=\lim_{\varepsilon\to0}\int_{c-\varepsilon}^{\,c+\varepsilon}f
=\big(F(c)-F(c)\big)=0 .$$
So for a continuous variable a single outcome has probability **zero** even though
it is possible, and consequently the endpoints do not matter:
$$P(a<X<b)=P(a\le X\le b)=P(a\le X<b)=F(b)-F(a).$$
This is the sharpest break from `~ST-05`, where $P(X=x)=p(x)$ could be positive.
Code: `prob_between(f, lo, hi)` computes $\int_{lo}^{hi}f$, and
`prob_between(f, c, c)=0` realizes $P(X=c)=0$ exactly (a zero-width integral).

## 4. Expectation, variance, and moments as integrals

Replace the sum of `~ST-05` by an integral. The **expectation** (mean) is
[PSU L14.3; HTZ Ch. 3]
$$\mu=E[X]=\int_{-\infty}^{\infty} x\,f(x)\,dx,$$
and, more generally, the **law of the unconscious statistician** gives the
expectation of any function without first finding its distribution,
$$E[g(X)]=\int_{-\infty}^{\infty} g(x)\,f(x)\,dx .$$
The **$k$-th raw moment** is $E[X^k]=\int x^k f$, and the **variance** is the
second central moment, with the same shortcut identity as in `~ST-05`:
$$\operatorname{Var}[X]=E\!\big[(X-\mu)^2\big]
=\int (x-\mu)^2 f(x)\,dx
=E[X^2]-\big(E[X]\big)^2 .$$
The standard deviation is $\sigma=\sqrt{\operatorname{Var}[X]}$. Linearity
survives unchanged: $E[aX+b]=aE[X]+b$ and $\operatorname{Var}[aX+b]=a^2
\operatorname{Var}[X]$. Code: `expectation_continuous`, `expectation_of` (LOTUS),
`moment_continuous`, `variance_continuous` (which uses the shortcut
$E[X^2]-\mu^2$). These integrals are the *continuous* moments that the
moment-generating function $M(t)=E[e^{tX}]=\int e^{tx}f\,dx$ of `~ST-06` packages
into a single transform.

## 5. Percentiles and quantiles: inverting the cdf

A **percentile** answers the inverse question — "what value of $X$ has $p$ of the
probability below it?" The $100p$-th percentile (the $p$-**quantile**) $\pi_p$
solves [PSU L13; L14.4]
$$F(\pi_p)=p,\qquad 0<p<1 .$$
When $F$ is continuous and strictly increasing this has a unique solution
$\pi_p=F^{-1}(p)$. The **median** $m=\pi_{0.5}$ ($F(m)=\tfrac12$) splits the area in
half; the **quartiles** are $\pi_{0.25},\pi_{0.75}$ and the **interquartile range**
is $\pi_{0.75}-\pi_{0.25}$ — the robust spread summaries of Lesson 13's exploratory
data analysis. Code: `quantile(F, p, lo, hi)` solves $F(\pi_p)=p$ by **bisection**
on $[lo,hi]$ (the cdf is monotone, so the sign of $F(x)-p$ brackets the root);
`median_continuous` is the $p=\tfrac12$ case. The test confirms the inverse
property $F(\text{quantile}(F,p))=p$ for both the uniform cdf and $F(x)=x^2$.

## 6. The continuous uniform distribution $U(a,b)$

The simplest continuous law spreads probability **evenly** over $[a,b]$: constant
density [PSU L14.6; HTZ Ch. 3]
$$f(x)=\begin{cases}\dfrac{1}{b-a}, & a\le x\le b,\\[4pt] 0,&\text{otherwise,}\end{cases}
\qquad
F(x)=\begin{cases}0,& x<a,\\[2pt]\dfrac{x-a}{b-a},& a\le x\le b,\\[4pt]1,& x>b.\end{cases}$$
It is normalized because the rectangle has area $\tfrac1{b-a}\cdot(b-a)=1$. Its
moments are clean integrals. The **mean** is the midpoint,
$$E[X]=\int_a^b \frac{x}{b-a}\,dx=\frac{1}{b-a}\cdot\frac{b^2-a^2}{2}
=\frac{a+b}{2},$$
and the **variance** is
$$\operatorname{Var}[X]=E[X^2]-\mu^2
=\frac{1}{b-a}\cdot\frac{b^3-a^3}{3}-\Big(\frac{a+b}{2}\Big)^2
=\frac{(b-a)^2}{12},$$
where the last step uses $b^3-a^3=(b-a)(b^2+ab+a^2)$. Inverting the linear cdf
$F=\tfrac{x-a}{b-a}$ gives the closed-form percentile
$$\pi_p=a+p\,(b-a).$$
Code: `uniform_pdf`, `uniform_cdf`, `uniform_mean` $=\tfrac{a+b}2$, `uniform_var`
$=\tfrac{(b-a)^2}{12}$, `uniform_quantile` $=a+p(b-a)$. The tests check both the
closed forms *and* that the integral routines of §4–§5 reproduce them. The uniform
is the continuous twin of the discrete uniform of `~ST-05`, and — via the
**probability integral transform** $U=F(X)\sim U(0,1)$ — it is the seed from which
all other continuous laws (`~ST-11`, `~ST-12`) are sampled.

## 7. The discrete→continuous bridge: a point mass is a Dirac delta

How does the *mass* picture of `~ST-05` fit inside the *density* picture? Take a
point mass of probability $1$ at $x=c$ and smear it over a width $2\varepsilon$:
the **box density**
$$f_\varepsilon(x)=\frac{1}{2\varepsilon}\,\mathbf 1_{\{|x-c|\le\varepsilon\}}$$
is a perfectly good pdf ($\int f_\varepsilon=1$) with mean $c$ (by symmetry) and
variance
$$\operatorname{Var}[X]=\int_{c-\varepsilon}^{c+\varepsilon}\frac{(x-c)^2}{2\varepsilon}\,dx
=\frac{1}{2\varepsilon}\cdot\frac{2\varepsilon^3}{3}=\frac{\varepsilon^2}{3}.$$
As $\varepsilon\to0$ the density concentrates to infinite height and zero width
while keeping unit area — this is precisely a **nascent Dirac delta**
$f_\varepsilon\to\delta(x-c)$ (`~MA-15`), and the variance $\varepsilon^2/3\to0$. In
the limit the "continuous" variable is really a degenerate discrete one: a single
mass at $c$, with $E[X]=c$ and no spread. Writing a discrete pmf as a sum of
deltas, $f(x)=\sum_i p_i\,\delta(x-x_i)$, lets the **same** integral formulas of
§4 reproduce the **sums** of `~ST-05` (the sifting property $\int g(x)\delta(x-c)\,dx
=g(c)$ turns $\int g f$ back into $\sum_i p_i g(x_i)$). So discrete and continuous
are two faces of one framework. Code: `point_mass_pdf(x, c, eps)`; the test drives
$\varepsilon\in\{0.5,0.1,0.01\}$ and confirms mean $\to c$ and
$\operatorname{Var}=\varepsilon^2/3\to0$.

## Where this goes

- `~ST-05` (discrete random variables) — the sum-based original of every
  integral here; §7 is the explicit $\sum\leftrightarrow\int$ bridge, and `~MA-15`
  (the Dirac delta) is the technical device that unifies them.
- `~ST-06` (moment-generating functions) — packages the §4 moments into
  $M(t)=\int e^{tx}f\,dx$; $M'(0)=E[X]$, $M''(0)=E[X^2]$.
- `~ST-11` (exponential, gamma, chi-square) and `~ST-12` (the normal) — the named
  continuous distributions; each is just a particular $f$ run through the §1–§5
  machinery (normalize, integrate for moments, invert for percentiles), with the
  **gamma function** replacing the factorials of `~ST-05`.
- `~SM-01` and `~SM-06` (statistical mechanics) — continuous densities in physics:
  the Maxwell–Boltzmann speed pdf obeys the identical $\int f=1$, $E[g(v)]=\int g f$,
  with characteristic speeds that are exactly the percentiles/moments of §4–§5.
