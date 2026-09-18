# ST-12 — The Normal Distribution (notes)

The normal distribution is the keystone of probability theory. Every other
distribution in this trunk eventually points at it: the binomial flattens into it
(de Moivre–Laplace, `~ST-07`), the gamma with large shape approaches it (`~ST-11`),
and — most importantly — *any* sum of many independent pieces, whatever their own
law, becomes normal in the limit (the central limit theorem, `~ST-18`). That
universality is why physics is full of Gaussians: thermodynamic fluctuations
(`~SM-01`), measurement errors (`~MA-19`), and the minimum-uncertainty wavepacket
of quantum mechanics (`~QM-07`) are all the same bell. This module builds the
distribution from its defining integral and ties every formula to a function in
`code/normal.py`.

Citation key (full details + granularity in `refs.md`): **PSU L16** = Penn State
STAT 414, Lesson 16 *Normal Distributions*, with subsections L16.1 (the pdf),
L16.2 (the empirical rule / standardizing), L16.3 (the cdf and finding
percentiles); **HTZ** = Hogg, Tanis & Zimmerman, *Probability and Statistical
Inference*, Ch. 5. Cited at **lesson/chapter level**.

## 1. The Gaussian integral — where $\sqrt{2\pi}$ comes from

Before we can call $e^{-x^2/2}$ a density we must know its total area. The trick
is to square the integral and pass to polar coordinates [PSU L16.1; HTZ §5.4]:
$$I=\int_{-\infty}^{\infty}e^{-x^2/2}\,dx,\qquad
I^2=\int_{-\infty}^{\infty}\!\!\int_{-\infty}^{\infty}e^{-(x^2+y^2)/2}\,dx\,dy
=\int_0^{2\pi}\!\!\int_0^\infty e^{-r^2/2}\,r\,dr\,d\theta .$$
The radial integral is elementary, $\int_0^\infty e^{-r^2/2}r\,dr=1$, and the
angular one gives $2\pi$, so
$$I^2=2\pi\quad\Longrightarrow\quad
\boxed{\;\int_{-\infty}^{\infty}e^{-x^2/2}\,dx=\sqrt{2\pi}\;}.$$
This constant `SQRT_2PI` is the normalizer of every Gaussian. Code
`gaussian_integral_check()` integrates $e^{-x^2/2}$ numerically over a wide window
and returns $\sqrt{2\pi}=2.50662827\ldots$; equivalently the peak height of the
standard density is its reciprocal, `standard_normal_pdf(0)`$=1/\sqrt{2\pi}
=0.39894228$. (The same integral is the gamma value $\Gamma(\tfrac12)=\sqrt\pi$
of `~ST-11` after the substitution $u=x^2/2$.)

## 2. The normal density

Shift by a location $\mu$, scale by a spread $\sigma>0$, and divide by the area to
get a bona-fide probability density [PSU L16.1]:
$$f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\!\Big(-\frac{(x-\mu)^2}{2\sigma^2}\Big),
\qquad -\infty<x<\infty .$$
We write $X\sim N(\mu,\sigma^2)$. It is **symmetric about $\mu$** (only $(x-\mu)^2$
appears), **unimodal** with its single maximum at $x=\mu$ where
$f(\mu)=1/(\sigma\sqrt{2\pi})$, and has **inflection points at $x=\mu\pm\sigma$**
(set $f''=0$): $\sigma$ is literally the distance from the peak to the bend of the
curve. That the area is one follows from §1 with the substitution $u=(x-\mu)/\sigma$:
$$\int_{-\infty}^\infty f(x)\,dx
=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^\infty e^{-u^2/2}\,du=1 .$$
Code: `normal_pdf(x, mu, sigma)`; the $\mu=0,\sigma=1$ special case is
`standard_normal_pdf(z)`. The test `test_pdf_normalizes_to_one` integrates `normal_pdf`
over $\mu\pm14\sigma$ and recovers $1$; `test_pdf_peaks_at_mean_and_is_symmetric`
checks the peak height $1/(\sigma\sqrt{2\pi})$ and the symmetry $f(\mu+d)=f(\mu-d)$.

## 3. Standardization: every normal is the *same* normal

Define the **standard score** (or $Z$-score)
$$Z=\frac{X-\mu}{\sigma}.$$
A linear change of variables turns $f$ into the **standard normal density**
$\varphi$ [PSU L16.2]. Because $dz=dx/\sigma$,
$$f_X(x)\,dx=\frac{1}{\sigma\sqrt{2\pi}}e^{-z^2/2}\,(\sigma\,dz)
=\underbrace{\frac{1}{\sqrt{2\pi}}e^{-z^2/2}}_{\varphi(z)}\,dz,$$
so $Z\sim N(0,1)$ for *any* $\mu,\sigma$. Concretely
$$f_X(x)=\frac1\sigma\,\varphi\!\Big(\frac{x-\mu}{\sigma}\Big).$$
This is the workhorse identity of the whole lesson: every probability question
about $N(\mu,\sigma^2)$ becomes a question about the one universal curve $N(0,1)$,
which historically lived in a single printed table. Code `standardize(x, mu, sigma)`
returns $z$; `test_standardization_reduces_to_standard_normal` verifies
$f_X(x)=\varphi(z)/\sigma$ and (next section) $F_X(x)=\Phi(z)$.

## 4. The cdf through the error function $\Phi$

The normal cdf has no elementary closed form, but it is exactly the **error
function** in disguise. The standard-normal cdf is [PSU L16.3]
$$\Phi(z)=\int_{-\infty}^z\varphi(t)\,dt
=\frac{1}{2}\Big[\,1+\operatorname{erf}\!\Big(\frac{z}{\sqrt2}\Big)\Big],
\qquad \operatorname{erf}(u)=\frac{2}{\sqrt\pi}\int_0^u e^{-s^2}\,ds .$$
Its three defining properties are immediate from the symmetry of $\varphi$:
$$\Phi(0)=\tfrac12,\qquad \Phi(-z)=1-\Phi(z),\qquad
\Phi(-\infty)=0,\ \Phi(+\infty)=1 .$$
For a general normal, standardize first:
$$F_X(x)=P(X\le x)=\Phi\!\Big(\frac{x-\mu}{\sigma}\Big),\qquad
P(a<X\le b)=\Phi\!\Big(\frac{b-\mu}{\sigma}\Big)-\Phi\!\Big(\frac{a-\mu}{\sigma}\Big).$$
Code uses `math.erf` directly: `standard_normal_cdf(z)`, `normal_cdf(x, mu, sigma)`,
and `normal_interval_prob(a, b, mu, sigma)`. The test
`test_standard_normal_cdf_via_erf` confirms $\Phi(0)=\tfrac12$, the reflection
$\Phi(-z)=1-\Phi(z)$, and the famous value $\Phi(1.95996\ldots)=0.975$ (the
two-sided $95\%$ point); `test_cdf_is_integral_of_pdf` checks $F$ equals the numeric
$\int_{-\infty}^x f$.

## 5. Mean and variance

By symmetry the mean is $\mu$, and the variance works out to exactly $\sigma^2$ —
the parameters *are* the moments. Compute $E[X]$ by splitting $x=(x-\mu)+\mu$
[PSU L16.1; HTZ §5.4]:
$$E[X]=\int_{-\infty}^\infty x\,f(x)\,dx
=\underbrace{\int (x-\mu) f\,dx}_{=0\ (\text{odd})}+\mu\underbrace{\int f\,dx}_{=1}=\mu .$$
For the variance substitute $u=(x-\mu)/\sigma$ and integrate by parts (or use the
$\Gamma(\tfrac32)=\tfrac12\sqrt\pi$ of `~ST-11`):
$$\operatorname{Var}[X]=\int (x-\mu)^2 f\,dx
=\frac{\sigma^2}{\sqrt{2\pi}}\int_{-\infty}^\infty u^2 e^{-u^2/2}\,du
=\frac{\sigma^2}{\sqrt{2\pi}}\cdot\sqrt{2\pi}=\sigma^2 .$$
So $\mu$ is the **center** and $\sigma$ the **scale** (standard deviation). Code
`normal_mean_by_integration(mu, sigma)` and `normal_variance_by_integration(mu, sigma)`
evaluate these integrals numerically (midpoint rule over $\mu\pm12\sigma$) and
return $\mu$ and $\sigma^2$ to high accuracy; `test_mean_and_variance_by_integration`
asserts both. This is the Gaussian face of `~SM-01`: a thermodynamic quantity has
mean given by its equilibrium value and a variance set by a susceptibility, and for
large $N$ that fluctuation is exactly this bell.

## 6. The moment-generating function

The cleanest way to *prove* $E[X]=\mu$, $\operatorname{Var}=\sigma^2$, and indeed
all higher moments is the **moment-generating function** of `~ST-06`. Complete the
square in the exponent [PSU L16.1; HTZ §5.4]:
$$M(t)=E\!\big[e^{tX}\big]
=\int_{-\infty}^\infty e^{tx}\,\frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}\,dx
=\exp\!\Big(\mu t+\tfrac12\sigma^2t^2\Big).$$
(The cross term from $tx-(x-\mu)^2/2\sigma^2$ leaves a shifted Gaussian whose
integral is again $1$.) Differentiate at $t=0$:
$$M'(0)=\mu=E[X],\qquad M''(0)=\mu^2+\sigma^2=E[X^2],\qquad
\operatorname{Var}=M''(0)-M'(0)^2=\sigma^2 .$$
Two structural facts drop straight out of this exponential-quadratic form and
power the rest of the trunk:

- **Linear maps stay normal.** If $X\sim N(\mu,\sigma^2)$ then $aX+b$ has mgf
  $e^{bt}M(at)=\exp\!\big((a\mu+b)t+\tfrac12 a^2\sigma^2 t^2\big)$, i.e.
  $aX+b\sim N(a\mu+b,\,a^2\sigma^2)$ — standardizing ($a=1/\sigma,\,b=-\mu/\sigma$)
  is the special case landing on $N(0,1)$, matching §3.
- **Sums of independents stay normal.** Because mgfs multiply,
  $M_{X+Y}(t)=M_X(t)M_Y(t)=\exp\!\big((\mu_X+\mu_Y)t+\tfrac12(\sigma_X^2+\sigma_Y^2)t^2\big)$,
  so $X+Y\sim N(\mu_X+\mu_Y,\,\sigma_X^2+\sigma_Y^2)$. The normal family is **closed
  under addition** — the seed of the CLT (`~ST-18`).

Code `normal_mgf(t, mu, sigma)` returns $M(t)$; `mgf_moment(k, mu, sigma)`
recovers $E[X^k]=M^{(k)}(0)$ by a $k$-th finite difference. The tests
`test_mgf_value_and_generated_moments` (giving $M(0)=1$, $M'(0)=\mu$,
$M''(0)=\mu^2+\sigma^2$) and `test_mgf_factorizes_under_standardization`
($M_X(t)=e^{\mu t}M_Z(\sigma t)$, $M_Z(s)=e^{s^2/2}$) check both facts.

## 7. The 68–95–99.7 (empirical) rule

Symmetric intervals about the mean carry fixed probabilities. With
$Z=(X-\mu)/\sigma$, $P(\mu-k\sigma<X<\mu+k\sigma)=P(-k<Z<k)$, and by the reflection
$\Phi(-k)=1-\Phi(k)$ [PSU L16.2],
$$P(|Z|\le k)=\Phi(k)-\Phi(-k)=2\Phi(k)-1 .$$
Evaluating at $k=1,2,3$ gives the rule of thumb every scientist knows:
$$\begin{aligned}
k=1:&\quad 2\Phi(1)-1=0.6827\ (\approx 68\%),\\
k=2:&\quad 2\Phi(2)-1=0.9545\ (\approx 95\%),\\
k=3:&\quad 2\Phi(3)-1=0.9973\ (\approx 99.7\%).
\end{aligned}$$
About two-thirds of a normal population lies within one standard deviation of the
mean, $95\%$ within two, and all but $0.3\%$ within three. Code `empirical_rule(k)`
returns $2\Phi(k)-1$; `test_empirical_rule_68_95_997` asserts the three values.
(For inference one usually wants the *exact* multipliers the other way: the
two-sided $95\%$ interval uses $z=1.95996$, not $2$ — see §8.)

## 8. The inverse cdf: probit / quantiles

To find percentiles we invert $\Phi$. The **probit** $z_p=\Phi^{-1}(p)$ solves
$\Phi(z_p)=p$; since $\Phi$ is continuous and strictly increasing the root is
unique and can be bracketed by **bisection** [PSU L16.3]. The $p$-th quantile of a
general normal is then
$$x_p=\mu+\sigma\,\Phi^{-1}(p).$$
By the reflection symmetry $\Phi^{-1}(1-p)=-\Phi^{-1}(p)$, so quantiles come in
$\pm$ pairs about $\mu$. The values worth memorizing:
$$\Phi^{-1}(0.5)=0,\quad \Phi^{-1}(0.90)=1.2816,\quad
\Phi^{-1}(0.95)=1.6449,\quad \Phi^{-1}(0.975)=1.9600 .$$
Code `probit(p)` runs the bisection on `standard_normal_cdf`, and
`normal_quantile(p, mu, sigma)` returns $\mu+\sigma\,\text{probit}(p)$. The test
`test_probit_inverts_the_cdf` checks $\Phi(\Phi^{-1}(p))=p$, $\Phi^{-1}(\tfrac12)=0$,
and the odd symmetry. Inversion is exactly how one turns the uniform numbers of
`~ST-10` into normal samples (the inverse-cdf / probability-integral transform).

## 9. Why the Gaussian is everywhere

Three appearances justify the central place of this curve and the cross-links of
this module.

- **The central limit theorem (`~ST-18`).** The mgf algebra of §6 shows the normal
  family is closed under addition with $\sigma^2$ adding; the CLT upgrades this to a
  *limit*: the standardized sum $\frac{1}{\sqrt n}\sum(X_i-\mu)/\sigma$ of *any*
  finite-variance i.i.d. sequence converges to $N(0,1)$. The normal is the unique
  attractor — that is why it shows up whenever many small independent effects add.
- **Thermodynamic fluctuations (`~SM-01`).** The two-state / Einstein-solid
  multiplicity, peaked and of fractional width $1/\sqrt N$, is in the large-$N$
  limit a Gaussian of variance $N/4$ (de Moivre–Laplace). Macroscopic observables
  fluctuate about their means by a normal law with variance fixed by a
  susceptibility; `SM-01`'s `gaussian_approx_two_state` is exactly this `normal_pdf`.
- **The quantum wavepacket (`~QM-07`).** The Gaussian $\psi(x)\propto
  e^{-x^2/4\sigma^2}$ is the *unique* state saturating the Heisenberg bound
  $\Delta x\,\Delta p=\hbar/2$; its position density is this `normal_pdf` and its
  Fourier transform is again Gaussian (a fixed point of the transform, `~MA-10`),
  so momentum is normal too. The bell that minimizes statistical spread also
  minimizes quantum uncertainty.

## Where this goes

- `~ST-10` (continuous random variables) and `~ST-11` (gamma family, $\Gamma(\tfrac12)
  =\sqrt\pi$) — the immediate predecessors this module specializes; `~ST-06` (mgf)
  supplies §6.
- `~ST-18` (**central limit theorem & normal approximation**) — the payoff: §6's
  closure under addition becomes a universal limit; the continuity-corrected normal
  approximation to the binomial (`~ST-07`) lives there.
- `~ST-15` (the **bivariate normal**) and `~ST-17` (normal sampling distributions —
  $\chi^2$, $t$, $F$ built from normals) — the multivariate and inferential sequels.
- `~SM-01` (statistical-mechanics fluctuations) and `~QM-07` (minimum-uncertainty
  wavepacket) — the two physics homes of the Gaussian; `~MA-10` (Laplace/Fourier
  transforms) underlies both the mgf of §6 and the wavepacket's self-Fourier
  property; `~MA-19` is the trunk's parent probability survey.
