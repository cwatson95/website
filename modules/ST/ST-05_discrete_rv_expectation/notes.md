# ST-05 — Discrete Random Variables & Expectation (notes)

A **random variable** is the bridge from the abstract sample space of `~ST-01` to
the real line: a function $X:\Omega\to\mathbb R$ that attaches a number to every
outcome. When its range is countable it is **discrete**, and its entire
probabilistic content is packed into one object — the **probability mass
function** $f(x)=P(X=x)$. Everything else in this module is built from $f$ by a
single operation, **expectation** $E[\cdot]$, the probability-weighted sum. The
mean, the variance, every moment, and the linearity rules are all just $E$ applied
to a cleverly chosen function of $X$. That weighted sum is not unique to
statistics: it is the quantum expectation value $\langle A\rangle=\sum_a a|c_a|^2$
of `~QM-06` and the ensemble average $\langle\cdot\rangle=\sum_i(\cdot)P_i$ of
`~SM-01`, with the pmf $f$ in the role of the probability weights.

Citation key (full details + granularity in `refs.md`): **PSU L$n$** = Penn State
STAT 414 OER, Lesson $n$ (L7 Discrete Random Variables, L8 Mathematical
Expectation, L9 Moment-Generating Functions); **HTZ** = Hogg, Tanis & Zimmerman,
*Probability and Statistical Inference* (the text STAT 414 follows). Cited at
**lesson / chapter level** (no page numbers — see the granularity note in
`refs.md`).

## 1. Discrete random variables and the pmf

Let $X$ take values in a countable **support** $S_X=\{x_1,x_2,\dots\}$. Its law is
the **probability mass function** [PSU L7]
$$f(x)=P(X=x),\qquad x\in\mathbb R,$$
which is positive exactly on $S_X$ and zero elsewhere. A function $f$ is a valid
pmf if and only if it satisfies the two pmf axioms — directly inherited from the
probability axioms of `~ST-01`:
$$f(x)\ge 0\quad\text{for all }x,\qquad\qquad \sum_{x\in S_X} f(x)=1.$$
The first says probabilities are non-negative; the second is normalization (the
sure event has probability $1$). Code `pmf_is_valid(values, probs)` checks both,
plus that the listed atoms are distinct; `support(values, probs)` returns the set
$S_X=\{x:f(x)>0\}$, discarding any zero-mass atoms. For a fair six-sided die
$f(x)=\tfrac16$ on $x\in\{1,\dots,6\}$; for a Bernoulli trial $f(1)=p$, $f(0)=1-p$.

## 2. The cdf as a step function

The pmf accumulates into the **cumulative distribution function** [PSU L7]
$$F(x)=P(X\le x)=\sum_{x_i\le x} f(x_i).$$
For a discrete $X$, $F$ is a **right-continuous step function**: flat between
consecutive atoms, jumping upward by exactly $f(x_i)$ at each $x_i\in S_X$. It
inherits three structural properties from the axioms,
$$\lim_{x\to-\infty}F(x)=0,\qquad \lim_{x\to+\infty}F(x)=1,\qquad
x\le y\ \Rightarrow\ F(x)\le F(y),$$
i.e. $F$ rises monotonically from $0$ to $1$. The pmf is recovered as the size of
the jump,
$$f(x_i)=F(x_i)-F(x_i^-)=F(x_i)-\lim_{x\uparrow x_i}F(x),$$
so $f$ and $F$ carry the same information. Code `cdf_from_pmf(values, probs)`
returns the callable $F$; `cdf_table(values, probs)` returns the sorted atoms and
the cumulative heights $F(x_i)$ — for the die, $F$ climbs $\tfrac16,\tfrac26,\dots$
up to $1$ at $x=6$, and the successive differences reproduce $f=\tfrac16$.

## 3. Expectation and the law of the unconscious statistician

The **expectation** (or **expected value**, **mean of a function**) of $g(X)$ is
the probability-weighted average of its values [PSU L8]:
$$\boxed{\,E[g(X)]=\sum_{x\in S_X} g(x)\,f(x)\,}$$
provided the sum converges absolutely. This is the **law of the unconscious
statistician (LOTUS)**: to average $g(X)$ you do *not* need the pmf of the new
variable $Y=g(X)$ — you weight $g(x)$ by the *old* pmf $f(x)$. The justification is
a regrouping. Let $f_Y(y)=P(g(X)=y)=\sum_{x:g(x)=y}f(x)$ be the genuine law of $Y$.
Then
$$E[Y]=\sum_y y\,f_Y(y)=\sum_y y\!\!\sum_{x:g(x)=y}\!\! f(x)
=\sum_y\sum_{x:g(x)=y} g(x)\,f(x)=\sum_{x\in S_X} g(x)\,f(x),$$
because on the inner sum $g(x)=y$. The two ways of computing $E[Y]$ therefore
agree, which is exactly what `test_lotus_matches_pushforward` asserts. Code:
`expectation_of(g, values, probs)` (alias `lotus`).

## 4. The mean $\mu=E[X]$ — and the bridge to `~QM-06`/`~SM-01`

Taking $g(x)=x$ in LOTUS gives the **mean** (first raw moment), the center of mass
of the distribution [PSU L8]:
$$\mu=E[X]=\sum_{x\in S_X} x\,f(x)=\mu'_1.$$
Code `expectation(values, probs)` (alias `mean`); for the die $\mu=\tfrac{1}{6}(1+
\cdots+6)=\tfrac{21}{6}=3.5$; for Bernoulli$(p)$, $\mu=0\cdot(1-p)+1\cdot p=p$.

This is the same object that appears across physics. In quantum mechanics the
expectation value of an observable with eigenvalues $a$ and Born probabilities
$|c_a|^2$ is (`~QM-06`)
$$\langle A\rangle=\sum_a a\,|c_a|^2,$$
which is $E[X]$ with the spectrum $\{a\}$ as support and $f(a)=|c_a|^2$ as pmf — the
Born rule *is* a pmf. In statistical mechanics the ensemble average of a quantity
$\mathcal O$ over microstates $i$ with Boltzmann weights $P_i$ (`~SM-01`) is
$$\langle\mathcal O\rangle=\sum_i \mathcal O_i\,P_i,$$
again $E[\cdot]$ with $f=P_i$. The mean is a **linear functional** of $f$; the
"physics" of a problem lives in $f$, while $E[\cdot]$ is a universal averaging rule.

A useful alternative formula for a **non-negative integer** $X$ is the tail (or
survival) sum, obtained by swapping the order of summation in $\sum_x x f(x)$:
$$E[X]=\sum_{k=1}^{\infty}P(X\ge k)=\sum_{k=0}^{\infty}\big(1-F(k)\big),
\qquad S(x):=1-F(x).$$
More generally, integrating the step cdf gives the representation valid for any
$X$ with finite mean,
$$E[X]=\int_0^{\infty}\!\big(1-F(x)\big)\,dx-\int_{-\infty}^{0}\! F(x)\,dx,$$
which `test_mean_via_survival_and_integral` confirms numerically by midpoint
integration of $F$ (`survival`, `mean_via_survival`, `_integrate`) — a continuous
cross-check of a discrete result.

## 5. Variance, standard deviation, and the computational formula

The spread of $X$ about its mean is the **variance**, the expectation of the
squared deviation [PSU L8]:
$$\sigma^2=\mathrm{Var}(X)=E\big[(X-\mu)^2\big]=\sum_{x} (x-\mu)^2 f(x)\ \ge 0.$$
Expanding the square and using linearity (the next section) gives the
**computational formula**, almost always the easier route:
$$\sigma^2=E[X^2-2\mu X+\mu^2]=E[X^2]-2\mu E[X]+\mu^2=E[X^2]-\mu^2,$$
since $E[X]=\mu$. So $\mathrm{Var}(X)=E[X^2]-\mu^2=\mu'_2-(\mu'_1)^2$. The **standard
deviation** $\sigma=\sqrt{\mathrm{Var}(X)}$ restores the units of $X$. Code
`variance` (via $E[X^2]-\mu^2$), `std`; `test_variance_computational_formula`
checks $E[X^2]-\mu^2$ against the definitional $E[(X-\mu)^2]$ (i.e. `central_moment(...,2)`)
and against the closed forms $\sigma^2_{\text{die}}=\tfrac{35}{12}$ and
$\sigma^2_{\text{Bern}}=p(1-p)$. The identical structure governs the quantum
spread $\sigma_A^2=\langle A^2\rangle-\langle A\rangle^2$ of `~QM-06`.

## 6. Raw and central moments; skewness

The mean and variance are the first two of an infinite ladder of **moments**
[PSU L8]. The **raw moments** (about the origin) and **central moments** (about the
mean) are
$$\mu'_k=E[X^k]=\sum_x x^k f(x),\qquad
\mu_k=E\big[(X-\mu)^k\big]=\sum_x (x-\mu)^k f(x).$$
Their first values are fixed by normalization and the definition of the mean:
$$\mu'_0=\sum_x f(x)=1,\qquad \mu'_1=\mu,\qquad \mu_1=E[X-\mu]=\mu-\mu=0,\qquad
\mu_2=\sigma^2.$$
Code `raw_moment(values, probs, k)`, `central_moment(values, probs, k)`;
`test_moment_normalizations` asserts $\mu'_0=1$, $\mu'_1=\mu$, $\mu_1=0$. Higher
central moments describe shape. **Standardizing** to $Z=(X-\mu)/\sigma$ (which has
$E[Z]=0,\ \mathrm{Var}(Z)=1$ — code `standardize`) makes them scale-free; the third
standardized moment is the **skewness**
$$\gamma_1=E[Z^3]=\frac{\mu_3}{\sigma^3},$$
a measure of asymmetry that vanishes for any distribution symmetric about its mean
(code `skewness`; the die gives $\gamma_1=0$, the skewed atom set $\{-1,0,2\}$ with
$p=\{.2,.5,.3\}$ gives $\gamma_1\approx0.469$). The fourth gives the **excess
kurtosis** $\gamma_2=\mu_4/\sigma^4-3$ (`excess_kurtosis`). These higher moments are
exactly the quantities the **moment-generating function** of §8 packages.

## 7. Linearity of expectation and affine transformations

Because $E[\cdot]$ is a sum weighted by a fixed $f$, it is **linear**: for
constants $a,b$ and the affine map $Y=aX+b$ [PSU L8],
$$E[aX+b]=\sum_x (ax+b)f(x)=a\sum_x x f(x)+b\sum_x f(x)=a\,E[X]+b.$$
The constant $b$ rides straight through (it shifts the mean by $b$); the scale $a$
factors out. Variance transforms differently — a shift cannot change spread, and a
rescale squares it:
$$\mathrm{Var}(aX+b)=E\big[(aX+b-(a\mu+b))^2\big]
=E\big[a^2(X-\mu)^2\big]=a^2\,\mathrm{Var}(X).$$
So $\sigma(aX+b)=|a|\,\sigma(X)$, independent of $b$. Code `linear_transform(a, b,
values, probs)` builds the image RV $(ax+b,\ f)$; `test_linearity_of_expectation_and_variance`
verifies $E[3X-4]=3E[X]-4$ and $\mathrm{Var}(3X-4)=9\,\mathrm{Var}(X)$, and that
adding $100$ to $b$ leaves the variance unchanged. (Standardization in §6 is the
special case $a=1/\sigma$, $b=-\mu/\sigma$.) Linearity holds **without any
independence assumption** — it is the workhorse that, in `~ST-07`, collapses the
binomial mean to $np$ by writing $X=\sum_i X_i$.

## 8. Preview: the moment-generating function

All the raw moments can be read off a single function, the **moment-generating
function** [PSU L9]
$$M(t)=E\big[e^{tX}\big]=\sum_x e^{tx} f(x),$$
because differentiating under the sum and setting $t=0$ peels them off one at a
time:
$$M^{(k)}(0)=E[X^k]=\mu'_k,\qquad\text{so}\quad M'(0)=\mu,\ \ M''(0)=E[X^2],
\ \ \sigma^2=M''(0)-M'(0)^2.$$
Code `mgf(values, probs, t)`; `test_mgf_derivatives_give_moments` confirms
$M(0)=1$, $M'(0)=\mu$, $M''(0)=E[X^2]$ by finite differences. This is only a
preview — the uniqueness theorem ("equal mgf $\Rightarrow$ equal distribution") and
the systematic moment extraction are the subject of `~ST-06`, and the mgf is the
tool that derives the means and variances of every named distribution in
`~ST-07`–`~ST-09` in one stroke.

## Where this goes

- `~QM-06` (measurement & expectation values) — $\langle A\rangle=\sum_a a|c_a|^2$
  and $\sigma_A^2=\langle A^2\rangle-\langle A\rangle^2$ are §4 and §5 with the Born
  pmf $f(a)=|c_a|^2$; `~SM-01` (ensembles) — the same $E[\cdot]$ over Boltzmann
  weights, where the sharpness of macrostates is a variance statement.
- `~ST-06` (moment-generating functions) — the §8 preview made into a full method:
  moments by differentiation, the uniqueness theorem, sums of independent RVs.
- `~ST-07` (binomial), `~ST-08` (geometric / negative binomial), `~ST-09` (Poisson)
  — the named discrete laws; their $\mu,\sigma^2$ are computed with exactly the
  `expectation`/`variance` machinery here (binomial $\mu=np$ via the linearity of §7).
- `~ST-10`–`~ST-12` (continuous random variables) — the same definitions with
  $\sum_x\to\int dx$ and the pmf $f(x)$ becoming a density; the cdf $F$ becomes
  continuous and LOTUS becomes $E[g(X)]=\int g(x)f(x)\,dx$.
- `~MA-19` (probability & statistics) — the sample mean $\bar x$ and sample
  variance $s^2$ are the empirical estimators of the population $\mu,\sigma^2$
  defined here; the law of large numbers (`~ST-18`) makes them converge.
