# ST-17 — The MGF Technique & Normal Sampling Distributions (notes)

The moment-generating function of `~ST-06` did two jobs there: it *generated
moments* by differentiation, and it *factored over independent sums*,
$M_{X+Y}=M_XM_Y$. Paired with the **uniqueness theorem** — an mgf that exists in a
neighborhood of $0$ belongs to exactly one distribution — that second job becomes a
constructive tool. To find the distribution of a sum (or a linear combination) of
independent variables, you do not convolve densities (`~ST-16`); you *multiply
their mgfs and recognize the product*. This module runs that technique twice:
first to prove the closure laws (normals add to normals, gammas add their shapes,
chi-squares add their degrees of freedom), then to manufacture the trio of
**sampling distributions** — $\chi^2$, Student's $t$, Snedecor's $F$ — that turn a
normal sample into the machinery of inference. Every formula is tied to a function
in `code/mgf_technique_sampling.py`.

Citation key (full details + granularity in `refs.md`): **PSU L25/L26** = Penn
State STAT 414, Lessons 25 (*The Moment-Generating Function Technique*) and 26
(*Random Functions Associated with Normal Distributions*); **HTZ** = Hogg, Tanis &
Zimmerman, *Probability and Statistical Inference*, Ch. 5. Cited at
**lesson/chapter level**.

## 1. The technique: multiply mgfs, recognize the product

Two facts from `~ST-06` are the whole engine [PSU L25; HTZ §5.x]. For
**independent** $X_1,\dots,X_n$ the mgf of the sum factors,
$$M_{X_1+\cdots+X_n}(t)=E\big[e^{t\sum X_i}\big]=\prod_{i=1}^n E\big[e^{tX_i}\big]
=\prod_{i=1}^n M_{X_i}(t),$$
and by **uniqueness** the function on the left determines the distribution of the
sum. So the **mgf technique** is: compute $\prod_iM_{X_i}(t)$, simplify, and match
it against a catalogue of known mgfs. The matched name *is* the answer — no
integration, no convolution. The same idea handles a scaled variable through
$M_{aX}(t)=M_X(at)$, so a linear combination has
$$M_{\sum a_iX_i}(t)=\prod_iM_{X_i}(a_it).$$
Code provides the building blocks `normal_mgf`, `gamma_mgf`, `chi2_mgf` and the
product assemblers `product_of_normal_mgfs`, `mgf_of_linear_combination_normals`,
`product_of_gamma_mgfs`, `product_of_chi2_mgfs`. The recognition step — reading the
resulting parameters — is `sum_of_normals_via_mgf`, `linear_combination_of_normals`,
`sum_of_gammas_via_mgf`, `sum_of_chisquares`.

## 2. Sums of independent normals are normal

Let $X_i\sim N(\mu_i,\sigma_i^2)$ be independent, each with mgf
$e^{\mu_it+\frac12\sigma_i^2t^2}$ (`~ST-12`). Multiplying [PSU L25; HTZ §5.4]:
$$M_{\sum X_i}(t)=\prod_i\exp\!\Big(\mu_it+\tfrac12\sigma_i^2t^2\Big)
=\exp\!\Big(\big(\textstyle\sum_i\mu_i\big)t+\tfrac12\big(\textstyle\sum_i\sigma_i^2\big)t^2\Big).$$
This is *again* a normal mgf, with mean $\sum\mu_i$ and variance $\sum\sigma_i^2$.
By uniqueness,
$$\sum_iX_i\sim N\Big(\sum_i\mu_i,\ \sum_i\sigma_i^2\Big).$$
The normal family is **closed under addition**. Allowing constant multipliers, the
$a_i$ enter the mgf through $M_{X_i}(a_it)=\exp(a_i\mu_it+\frac12a_i^2\sigma_i^2t^2)$,
so
$$\sum_ia_iX_i\sim N\Big(\sum_ia_i\mu_i,\ \sum_ia_i^2\sigma_i^2\Big).$$
A consequence worth stating loudly: a **difference** adds the variances,
$$X_1-X_2\sim N\big(\mu_1-\mu_2,\ \sigma_1^2+\sigma_2^2\big),$$
because $a_2=-1$ enters squared. Code `sum_of_normals_via_mgf(means, vars)` returns
$(\sum\mu_i,\sum\sigma_i^2)$ and `linear_combination_of_normals(a, means, vars)`
returns $(\sum a_i\mu_i,\sum a_i^2\sigma_i^2)$; the tests
`test_sum_of_normals_is_normal`, `test_linear_combination_of_normals`,
`test_difference_of_two_normals` check that the product of the component mgfs
equals the single recognized normal mgf (e.g. variances $4+2.25+1=7.25$, and the
difference $4+9=13$, never $4-9$). This closure is the *finite-$n$* seed of the
central limit theorem (`~ST-18`), which upgrades it to a limit for *non-normal*
summands.

## 3. Gammas add shapes; chi-squares add degrees of freedom

The same one-line argument handles the gamma family (`~ST-11`). If
$X_i\sim\mathrm{Gamma}(\alpha_i,\theta)$ share a **common scale** $\theta$, with mgf
$(1-\theta t)^{-\alpha_i}$, then [PSU L25]
$$M_{\sum X_i}(t)=\prod_i(1-\theta t)^{-\alpha_i}=(1-\theta t)^{-\sum_i\alpha_i}
\quad\Longrightarrow\quad
\sum_iX_i\sim\mathrm{Gamma}\Big(\sum_i\alpha_i,\ \theta\Big).$$
Shapes add (the scale is shared and unchanged). This *is* the Erlang/waiting-time
fact of `~ST-11` — a sum of $n$ exponentials $\mathrm{Gamma}(1,\theta)$ is
$\mathrm{Gamma}(n,\theta)$ — and underlies the Poisson process (`~ST-09`). The
**chi-square** is the special case $\theta=2$, $\alpha=r/2$, with mgf $(1-2t)^{-r/2}$:
$$M_{\sum_iV_i}(t)=\prod_i(1-2t)^{-r_i/2}=(1-2t)^{-(\sum_ir_i)/2}
\quad\Longrightarrow\quad
\sum_iV_i\sim\chi^2_{\sum_ir_i}.$$
**Degrees of freedom add.** Code `sum_of_gammas_via_mgf(alphas, theta)` returns
$(\sum\alpha_i,\theta)$ and `sum_of_chisquares(dfs)` returns $\sum r_i$; tests
`test_gammas_add_shapes`, `test_chisquares_add_df` confirm the mgf products collapse
to the single recognized mgf (and that `chi2_mgf(t,8)`$=$`gamma_mgf(t,4,2)`).

## 4. $Z^2\sim\chi^2_1$ — the seed of sampling theory

Everything in Part B rests on one transformation (`~ST-16`): the **square of a
standard normal is a chi-square with one degree of freedom**. With $Z\sim N(0,1)$
and $W=Z^2$, the change of variable $w=z^2$ (two preimages $\pm\sqrt w$, each with
$|dz/dw|=\tfrac{1}{2\sqrt w}$) gives [PSU L25; HTZ §5.4]
$$f_W(w)=2\,\varphi(\sqrt w)\cdot\frac{1}{2\sqrt w}=\frac{\varphi(\sqrt w)}{\sqrt w}
=\frac{1}{\sqrt{2\pi}}\,w^{-1/2}e^{-w/2},\qquad w>0,$$
which is exactly the $\chi^2_1$ density (gamma with $\alpha=\tfrac12,\theta=2$, using
$\Gamma(\tfrac12)=\sqrt\pi$). One can also see it through mgfs:
$M_{Z^2}(t)=E[e^{tZ^2}]=(1-2t)^{-1/2}$ for $t<\tfrac12$ — the $\chi^2_1$ mgf.
Combining with §3, a **sum of $n$ independent squared standard normals is
$\chi^2_n$**:
$$Z_1,\dots,Z_n\overset{\text{iid}}{\sim}N(0,1)\quad\Longrightarrow\quad
\sum_{i=1}^nZ_i^2\sim\chi^2_n.$$
Code `square_of_standard_normal_pdf(x)` returns $\varphi(\sqrt x)/\sqrt x$; the test
`test_square_of_standard_normal_is_chi2_1` checks it equals `chi2_pdf(x,1)`
pointwise, that $\chi^2_2$ is the exponential of mean $2$, and that $\chi^2_4$
integrates to one.

## 5. The sampling distribution of the mean

Now take a **random sample** $X_1,\dots,X_n$ iid $N(\mu,\sigma^2)$ and form the
**sample mean** $\bar X=\frac1n\sum X_i$. This is the linear combination of §2 with
all $a_i=1/n$, so [PSU L26; HTZ §5.5]
$$\bar X\sim N\!\Big(\mu,\ \frac{\sigma^2}{n}\Big),\qquad
E[\bar X]=\mu,\quad \operatorname{Var}[\bar X]=\frac{\sigma^2}{n}.$$
The mean is **unbiased** and the variance shrinks like $1/n$: more data sharpens the
estimate (the **standard error** $\sigma/\sqrt n$). Standardizing,
$$Z=\frac{\bar X-\mu}{\sigma/\sqrt n}\sim N(0,1)\quad\text{exactly},$$
for *every* $n$ when the population is normal (the CLT of `~ST-18` is needed only
when it is not). Code `sampling_dist_of_mean(mu, sigma2, n)` returns
$(\mu,\sigma^2/n)$; `standardized_mean_mgf(t, mu, sigma2, n)` computes the mgf of
$(\bar X-\mu)/(\sigma/\sqrt n)$ and returns $e^{t^2/2}$ — the standard-normal mgf —
independently of $\mu,\sigma,n$, verified in `test_standardized_mean_is_standard_normal`
and `test_sampling_dist_of_mean` (where doubling $n$ halves the variance).

## 6. The sample variance: $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$

Define the **sample variance** $S^2=\frac{1}{n-1}\sum_{i=1}^n(X_i-\bar X)^2$. Two
theorems govern it for a normal sample [PSU L26; HTZ §5.5]:

1. **Independence.** $\bar X$ and $S^2$ are **independent** — a property special to
   the normal (it characterizes it). Geometrically, $\bar X$ measures the projection
   of the data vector onto the all-ones direction, while $S^2$ measures the squared
   length of the *orthogonal* complement; for a spherically symmetric Gaussian those
   two are independent.
2. **Chi-square.** $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$. The naive sum of squares
   about the *true* mean is $\sum(X_i-\mu)^2/\sigma^2=\sum Z_i^2\sim\chi^2_n$ (§4).
   Replacing $\mu$ by its estimate $\bar X$ removes exactly **one** degree of
   freedom (the data must satisfy $\sum(X_i-\bar X)=0$), leaving $\chi^2_{n-1}$. The
   algebraic identity behind it is
   $$\underbrace{\sum_{i}\Big(\frac{X_i-\mu}{\sigma}\Big)^2}_{\chi^2_n}
   =\underbrace{\frac{(n-1)S^2}{\sigma^2}}_{\chi^2_{n-1}}
   +\underbrace{\Big(\frac{\bar X-\mu}{\sigma/\sqrt n}\Big)^2}_{\chi^2_1},$$
   and because the two right-hand terms are independent (theorem 1), their mgfs
   multiply: $(1-2t)^{-n/2}=(1-2t)^{-(n-1)/2}\cdot(1-2t)^{-1/2}$ — the degrees of
   freedom partition exactly, which *forces* the middle term to be $\chi^2_{n-1}$.
   This is the mgf technique run in reverse. Code `sample_variance_chi2_df(n)`
   returns $n-1$ (`test_sample_variance_df`).

## 7. Student's $t$: $Z$ over $\sqrt{V/r}$

In practice $\sigma$ is unknown, so we replace it in the standardized mean by the
sample $S$. The result is no longer normal: dividing a standard normal by an
independent (scaled) chi-square root gives **Student's $t$** [PSU L26; HTZ §5.6].
Define, with $Z\sim N(0,1)$ and $V\sim\chi^2_r$ **independent**,
$$T=\frac{Z}{\sqrt{V/r}}\ \sim\ t_r.$$
Its density, obtained from the joint density of $(Z,V)$ by the change of variables
$(Z,V)\to(T,V)$ and integrating out $V$, is
$$\boxed{\;f_T(t)=\frac{\Gamma\!\big(\frac{r+1}{2}\big)}{\sqrt{r\pi}\,
\Gamma\!\big(\frac r2\big)}\Big(1+\frac{t^2}{r}\Big)^{-\frac{r+1}{2}}
=\frac{1}{\sqrt r\,B\!\big(\frac12,\frac r2\big)}\Big(1+\frac{t^2}{r}\Big)^{-\frac{r+1}{2}}\;}$$
using the **Beta function** $B(\frac12,\frac r2)=\Gamma(\frac12)\Gamma(\frac r2)/
\Gamma(\frac{r+1}{2})$ (`~MA-12`). The density is **symmetric and bell-shaped** but
**heavier-tailed** than the normal: it decays only polynomially, $\sim|t|^{-(r+1)}$.
Hence its moments are limited,
$$E[T]=0\ (r>1),\qquad \operatorname{Var}[T]=\frac{r}{r-2}\ (r>2),$$
with the variance **infinite for $1<r\le2$** and undefined mean at $r=1$ (the $t_1$
is the **Cauchy** distribution, $f(t)=\frac{1}{\pi(1+t^2)}$, with no mean at all).
Applied to the sample, the unknown $\sigma$ cancels:
$$\frac{\bar X-\mu}{S/\sqrt n}
=\frac{(\bar X-\mu)/(\sigma/\sqrt n)}{\sqrt{\frac{(n-1)S^2/\sigma^2}{n-1}}}
=\frac{Z}{\sqrt{V/(n-1)}}\sim t_{n-1},$$
where $Z\sim N(0,1)$ (§5) and $V=(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$ (§6) are
independent (§6, theorem 1). This is the **one-sample $t$ statistic** of inference,
and the price of estimating $\sigma$ is the extra tail weight of $t_{n-1}$ relative
to $N(0,1)$. Code `students_t_pdf(t, r)`, `students_t_mean(r)`, `students_t_var(r)`;
tests `test_students_t_density_normalizes_and_moments` (normalization, $E[T]=0$,
$\operatorname{Var}=r/(r-2)$, and the Beta-form constant $f(0)=1/(\sqrt r\,
B(\tfrac12,\tfrac r2))$).

## 8. The normal limit $t_r\to N(0,1)$

As the degrees of freedom grow, $S\to\sigma$ and the $t$ collapses onto the normal.
Analytically, in $f_T$,
$$\Big(1+\frac{t^2}{r}\Big)^{-\frac{r+1}{2}}\xrightarrow[r\to\infty]{}e^{-t^2/2},
\qquad
\frac{\Gamma(\frac{r+1}{2})}{\sqrt{r\pi}\,\Gamma(\frac r2)}
\xrightarrow[r\to\infty]{}\frac{1}{\sqrt{2\pi}},$$
the first by $\lim_r(1+a/r)^{-r/2}=e^{-a/2}$ and the second by Stirling's ratio
$\Gamma(\frac{r+1}{2})/\Gamma(\frac r2)\sim\sqrt{r/2}$. Hence
$$f_T(t)\xrightarrow[r\to\infty]{}\frac{1}{\sqrt{2\pi}}e^{-t^2/2}=\varphi(t).$$
The heavy tails retract toward the Gaussian's exponential ones, and the variance
$r/(r-2)\to1$. Practically, $t_{30}$ is already very close to $N(0,1)$. Code
verifies the limit in `test_students_t_var_tails_and_limit`: the variance decreases
toward $1$ as $r$ grows and $|f_T(1;r)-\varphi(1)|$ shrinks with $r$ (at $r=5000$
it agrees with $\varphi(1)=0.241971$ to $<10^{-3}$).

## 9. Snedecor's $F$: a ratio of scaled chi-squares

The last sampling distribution compares **two** variances. With
$U\sim\chi^2_{r_1}$ and $V\sim\chi^2_{r_2}$ **independent**, the ratio of the two
*per-degree-of-freedom* chi-squares is **Snedecor's $F$** [PSU L26; HTZ §5.6]:
$$F=\frac{U/r_1}{V/r_2}\ \sim\ F_{r_1,r_2}.$$
The joint density of $(U,V)$, transformed to $(F,V)$ and integrated over $V$, gives
$$\boxed{\;f_F(x)=\frac{(r_1/r_2)^{r_1/2}}{B\!\big(\frac{r_1}2,\frac{r_2}2\big)}\,
\frac{x^{r_1/2-1}}{\big(1+\frac{r_1}{r_2}x\big)^{(r_1+r_2)/2}},\qquad x>0\;}$$
again normalized by a Beta function (`~MA-12`). Its moments depend only on the
**denominator** degrees of freedom for the mean,
$$E[F]=\frac{r_2}{r_2-2}\ (r_2>2),\qquad
\operatorname{Var}[F]=\frac{2r_2^2(r_1+r_2-2)}{r_1(r_2-2)^2(r_2-4)}\ (r_2>4),$$
so $E[F]\to1$ as $r_2\to\infty$ (the denominator chi-square concentrates at its
mean). Two structural facts:

- **Reciprocal symmetry.** $1/F\sim F_{r_2,r_1}$ — swapping numerator and
  denominator swaps the degrees of freedom, the identity behind reading lower-tail
  $F$ percentiles from upper-tail tables.
- **$t^2=F_{1,r}$.** Squaring a $t$ gives an $F$ with one numerator degree of
  freedom: since $T=Z/\sqrt{V/r}$,
  $$T^2=\frac{Z^2}{V/r}=\frac{Z^2/1}{V/r}=\frac{U/1}{V/r}\sim F_{1,r},
  \qquad U=Z^2\sim\chi^2_1\ (\S4).$$
  As a density transform $f_{T^2}(w)=f_T(\sqrt w)/\sqrt w$. Code
  `f_pdf(x, r1, r2)`, `f_mean(r2)`, `f_var(r1, r2)`, and `t_squared_pdf(w, r)`;
  tests `test_f_density_normalizes_and_mean` (normalization, $E[F]=r_2/(r_2-2)$) and
  `test_t_squared_is_F_1_r` (the densities $f_{T^2}(w)$ and $f_F(w;1,r)$ agree). The
  ratio of two independent sample variances $S_1^2/S_2^2$ from normal populations of
  equal variance is exactly $F_{n_1-1,\,n_2-1}$ — the basis of the variance-ratio
  test and ANOVA.

## Where this goes

- `~ST-06` (moment-generating functions — the product rule and uniqueness this
  module *uses*), `~ST-12` (the normal mgf $e^{\mu t+\sigma^2t^2/2}$ powering §2 and
  §5), `~ST-11` (the gamma/chi-square mgfs of §3 and the $\Gamma(\tfrac12)=\sqrt\pi$
  of §4), `~ST-16` ($Z^2\sim\chi^2_1$ and the $T^2\to F_{1,r}$ change of variable).
- `~ST-18` (**central limit theorem**) — the limiting form of §2's closure: even
  non-normal summands give an asymptotically normal $\bar X$, so the $Z$ of §5 and
  the $t$ of §7 stay approximately valid for large $n$.
- `~ST-10` (continuous random variables) and `~MA-12` (gamma & **Beta** functions) —
  the analytic home of the $t$ and $F$ densities; `~ST-09` (the Poisson process) —
  the gamma sums of §3 as Erlang arrival times.
- Physics: `~SM-06` (kinetic theory) — a molecule's energy $E=\tfrac12m(v_x^2+v_y^2
  +v_z^2)$ makes $2E/kT$ a sum of three squared standard normals, a $\chi^2_3$
  (gamma shape $\tfrac32$); the equipartition and Maxwell–Boltzmann speed
  distributions are §4 in disguise.
