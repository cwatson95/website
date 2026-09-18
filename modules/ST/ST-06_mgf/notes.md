# ST-06 — Moment-Generating Functions (notes)

A random variable carries an infinite list of numbers — its **moments**
$E[X],E[X^2],E[X^3],\dots$ — and, more subtly, *which distribution* it follows.
The **moment-generating function** packs all of that into a single function of a
dummy variable $t$:
$$M(t)=E\!\left[e^{tX}\right].$$
Differentiating $M$ at $t=0$ reads off the moments one at a time; multiplying
mgfs adds independent variables; and (the deep fact) the mgf, when it exists,
*uniquely determines the distribution*. This is the same move that makes the
Laplace transform (`~MA-10`) and the partition function (`~SM-03`) so powerful,
specialized to probability. We build on the discrete random variables and the
expectation operator of `~ST-05`.

Citation key (full details + granularity in `refs.md`): **PSU L9** = Penn State
STAT 414, Lesson 9 *Moment Generating Functions*; **HTZ** = Hogg, Tanis &
Zimmerman, *Probability and Statistical Inference*; **WMS** = Wackerly,
Mendenhall & Scheaffer, *Mathematical Statistics with Applications*. Cited at
**lesson/chapter level**.

## 1. Definition and existence

For a discrete random variable $X$ with probability mass function $p(x)$, and for
a continuous one with density $f(x)$, the **moment-generating function** is
$$M(t)=E\!\left[e^{tX}\right]
=\sum_{x} e^{tx}\,p(x)
\qquad\text{or}\qquad
M(t)=\int_{-\infty}^{\infty} e^{tx}\,f(x)\,dx ,$$
provided the sum/integral is finite for all $t$ in an **open interval**
$(-h,h)$ around $0$ [PSU L9.1]. That convergence requirement is real: the mgf of a
heavy-tailed law (Cauchy, log-normal) does *not* exist, and one then falls back on
the characteristic function $\varphi(t)=E[e^{itX}]$, which always exists. Code:
`mgf(t, values, probs)` evaluates the discrete sum; `mgf_continuous(t, pdf, a, b)`
evaluates the integral by midpoint quadrature.

Two immediate values. At $t=0$,
$$M(0)=E[e^{0}]=E[1]=\sum_x p(x)=1 ,$$
so **every mgf passes through $1$** — it is just the statement that the
probabilities sum to one. And because $e^{tx}>0$, $M(t)>0$ everywhere it is
defined, so the **cumulant generating function**
$$K(t)=\ln M(t)$$
is well defined, with $K(0)=0$. Code: `cgf(t, values, probs)`.

## 2. The moment series: why it "generates" moments

Expand the exponential inside the expectation and exchange sum and expectation
(legitimate on the interval of convergence):
$$M(t)=E\!\left[\sum_{k=0}^{\infty}\frac{(tX)^k}{k!}\right]
=\sum_{k=0}^{\infty}\frac{t^k}{k!}\,E[X^k] .$$
So the mgf is the **exponential generating function of the raw moments**
$m_k=E[X^k]$: the moment $m_k$ is $k!$ times the coefficient of $t^k$. Reading off
the Taylor coefficient is the same as differentiating $k$ times at $0$
(`~MA-08`/`~MA-13`):
$$\boxed{\,M^{(k)}(0)=E[X^k]=m_k\,}\qquad k=0,1,2,\dots$$
This is the headline identity of the lesson [PSU L9.2]. Code:
`moment_from_mgf(k, values, probs)` evaluates $M^{(k)}(0)$ with an accurate
symmetric finite-difference stencil (`_central_derivative`), recovering
$E[X^k]$ directly from the mgf.

## 3. Mean and variance from the mgf

The two most useful cases of §2 are $k=1,2$. The **mean** is the first
derivative,
$$\mu=E[X]=M'(0),$$
and the **variance** combines the first two moments,
$$\sigma^2=\mathrm{Var}(X)=E[X^2]-\big(E[X]\big)^2=M''(0)-\big[M'(0)\big]^2 .$$
Code: `mean_from_mgf` returns $M'(0)$ and `var_from_mgf` returns
$M''(0)-[M'(0)]^2$; both are checked against the direct `~ST-05` definitions
`mean` and `variance`. *Worked check (binomial, §7):* for $X\sim\text{Bin}(n,p)$,
$M(t)=((1-p)+pe^t)^n$, so
$$M'(t)=n\big((1-p)+pe^t\big)^{n-1}pe^t,\qquad M'(0)=np=\mu,$$
$$M''(0)=n(n-1)p^2+np \;\Rightarrow\; \sigma^2=M''(0)-(np)^2=np(1-p),$$
the familiar binomial mean and variance, obtained without summing a single
series by hand.

## 4. The linear-transform rule

If $Y=aX+b$ then
$$M_Y(t)=E\!\left[e^{t(aX+b)}\right]=e^{bt}\,E\!\left[e^{(at)X}\right]
=e^{bt}\,M_X(at).$$
Differentiating at $0$ reproduces $E[aX+b]=a\mu+b$ and
$\mathrm{Var}(aX+b)=a^2\sigma^2$. Standardizing $Z=(X-\mu)/\sigma$ therefore has
$$M_Z(t)=e^{-\mu t/\sigma}\,M_X\!\big(t/\sigma\big),$$
which is the engine behind the standardized central-limit argument (`~ST-18`).
Code: the rule is verified numerically by transforming the support,
`mgf(t, a*values+b, probs) == exp(b t) * mgf(a t, values, probs)`.

## 5. Sums of independent variables: the product rule

Let $X$ and $Y$ be **independent**. Then $e^{tX}$ and $e^{tY}$ are independent,
expectations factor, and
$$\boxed{\,M_{X+Y}(t)=E\!\left[e^{t(X+Y)}\right]
=E\!\left[e^{tX}\right]E\!\left[e^{tY}\right]=M_X(t)\,M_Y(t)\,}$$
and by induction $M_{X_1+\cdots+X_n}(t)=\prod_{i=1}^{n}M_{X_i}(t)$ [PSU L9.3].
This is the heart of why mgfs matter: the **convolution** of densities (the
distribution of a sum) becomes an ordinary **product** of mgfs — exactly the
Laplace/Fourier convolution theorem of `~MA-10`. Code: `mgf_of_sum(t, dists)`
returns the product $\prod_i M_{X_i}(t)$, and `convolve_dists` builds the actual
distribution of $X+Y$ so that
$$M_{\text{convolve}(X,Y)}(t)=M_X(t)\,M_Y(t)$$
can be checked term by term. For $n$ i.i.d. $\text{Bernoulli}(p)$ this gives the
binomial mgf, $M(t)=((1-p)+pe^t)^n$, i.e. a binomial is a sum of Bernoullis
(`~ST-07`).

## 6. Uniqueness — the mgf *is* the distribution

The reason §5 is decisive is the **uniqueness theorem** [PSU L9; HTZ Ch. 3]:

> If $X$ and $Y$ have mgfs $M_X(t)=M_Y(t)$ for all $t$ in an open interval about
> $0$, then $X$ and $Y$ have the **same distribution**.

Equivalently, the map (distribution) $\mapsto$ (mgf) is **injective**. So to
identify the distribution of a sum or a transform, you compute its mgf and
*recognize* it — no convolution integral required. This is the **mgf technique**
of `~ST-17`. Examples that fall out instantly from §5 + uniqueness:

$$\text{Poisson: } M(t)=e^{\lambda(e^t-1)}\;\Rightarrow\;
\text{Poi}(\lambda_1)+\text{Poi}(\lambda_2)=\text{Poi}(\lambda_1+\lambda_2),$$
$$\text{Normal: } M(t)=e^{\mu t+\frac12\sigma^2 t^2}\;\Rightarrow\;
N(\mu_1,\sigma_1^2)+N(\mu_2,\sigma_2^2)=N(\mu_1{+}\mu_2,\ \sigma_1^2{+}\sigma_2^2),$$
$$\text{Gamma: } M(t)=\Big(\tfrac{\lambda}{\lambda-t}\Big)^{\!\alpha}\;\Rightarrow\;
\sum_{i=1}^{\alpha}\text{Exp}(\lambda)=\text{Gamma}(\alpha,\lambda).$$
In each line the product of the summands' mgfs is again of the same form with the
parameters added, and uniqueness *concludes the distribution of the sum*. Code:
`poisson_mgf`, `normal_mgf`, `gamma_mgf`, `exponential_mgf`, `bernoulli_mgf`,
`binomial_mgf`, `geometric_mgf` are the closed forms; the additivity identities
are asserted directly. Uniqueness has a transform reading: $M(t)$ is the
two-sided **Laplace transform** of the density at $s=-t$,
$$M(t)=\int e^{tx}f(x)\,dx=\mathcal{L}\{f\}(-t),$$
and the theorem is just the **invertibility** of that transform (`~MA-10`). For a
nonnegative $X$ the ordinary one-sided Laplace transform $\mathcal{L}\{f\}(s)$
equals $M(-s)$; code: `mgf_continuous(-s, pdf, 0, b)` reproduces
$\mathcal{L}\{f\}(s)$ by quadrature.

## 7. A catalogue of mgfs

Each closed form is obtained by summing/integrating $e^{tx}$ against the law; its
derivatives at $0$ regenerate the moments of §3. (Code symbol in brackets.)

| distribution | $M(t)$ | domain | $\mu=M'(0)$ | $\sigma^2$ |
|---|---|---|---|---|
| Bernoulli$(p)$ `[bernoulli_mgf]` | $(1-p)+pe^t$ | all $t$ | $p$ | $p(1-p)$ |
| Binomial$(n,p)$ `[binomial_mgf]` | $((1-p)+pe^t)^n$ | all $t$ | $np$ | $np(1-p)$ |
| Geometric$(p)$ `[geometric_mgf]` | $\dfrac{pe^t}{1-(1-p)e^t}$ | $t<-\ln(1-p)$ | $1/p$ | $(1-p)/p^2$ |
| Poisson$(\lambda)$ `[poisson_mgf]` | $e^{\lambda(e^t-1)}$ | all $t$ | $\lambda$ | $\lambda$ |
| Exponential$(\lambda)$ `[exponential_mgf]` | $\dfrac{\lambda}{\lambda-t}$ | $t<\lambda$ | $1/\lambda$ | $1/\lambda^2$ |
| Gamma$(\alpha,\lambda)$ `[gamma_mgf]` | $\big(\tfrac{\lambda}{\lambda-t}\big)^{\alpha}$ | $t<\lambda$ | $\alpha/\lambda$ | $\alpha/\lambda^2$ |
| Normal$(\mu,\sigma^2)$ `[normal_mgf]` | $e^{\mu t+\frac12\sigma^2t^2}$ | all $t$ | $\mu$ | $\sigma^2$ |

The geometric here is the "number of trials to the first success" convention,
support $\{1,2,\dots\}$ (`~ST-08`). The binomial row is the Bernoulli row raised
to the $n$ (§5); the gamma row is the exponential row raised to the $\alpha$.

## 8. Cumulants and the $\ln Z$ bridge to statistical mechanics

Differentiating $K(t)=\ln M(t)$ instead of $M(t)$ gives the **cumulants**
$\kappa_k=K^{(k)}(0)$. The first two are the mean and the variance,
$$\kappa_1=K'(0)=\frac{M'(0)}{M(0)}=\mu,\qquad
\kappa_2=K''(0)=\frac{M''(0)}{M(0)}-\Big(\frac{M'(0)}{M(0)}\Big)^2
=M''(0)-[M'(0)]^2=\sigma^2,$$
using $M(0)=1$. Cumulants beat moments for sums: because §5 makes mgfs multiply,
**log-mgfs add**, so cumulants are *additive* over independent variables,
$$K_{X+Y}(t)=K_X(t)+K_Y(t)\quad\Longrightarrow\quad
\kappa_k(X+Y)=\kappa_k(X)+\kappa_k(Y).$$
For the **Poisson** law $K(t)=\lambda(e^t-1)$, so $K^{(k)}(0)=\lambda$ for *every*
$k$ — all cumulants equal $\lambda$, the cleanest possible signature. Code:
`cumulant_from_mgf(k, values, probs)` differentiates `cgf`; the tests confirm
$\kappa_1=\kappa_2=\kappa_3=\lambda$ for Poisson and additivity for a sum.

This is verbatim the structure of equilibrium **statistical mechanics**
(`~SM-03`). The canonical distribution $P_i=e^{-\beta E_i}/Z$ has energy mgf
$$M_E(t)=\sum_i P_i\,e^{tE_i}=\frac{Z(\beta-t)}{Z(\beta)},\qquad
K_E(t)=\ln Z(\beta-t)-\ln Z(\beta),$$
so the partition function's log generates the energy cumulants:
$$K_E'(0)=-\frac{\partial \ln Z}{\partial\beta}=\langle E\rangle=U,\qquad
K_E''(0)=\frac{\partial^2 \ln Z}{\partial\beta^2}=\mathrm{Var}(E)=k_BT^2\,C.$$
The mean energy $U$ and the **energy fluctuations** $=$ heat capacity are the
first two cumulants of the energy — the simplest fluctuation–response relation,
and exactly the $\mu=K'(0)$, $\sigma^2=K''(0)$ of this module read in the variable
$\beta$. The "$\ln$ of the generating function generates cumulants" idea is one
object wearing two hats: $\ln M(t)$ in probability, $\ln Z(\beta)$ in physics.

## 9. Numerics: how the code differentiates at $0$

Because the analytic point of the mgf is its derivatives *at one point*, the code
uses **symmetric finite-difference stencils** centered at $t=0$
(`_central_derivative`): the 5-point stencils for $M'(0)$ and $M''(0)$ are
$O(h^4)$-accurate,
$$M'(0)\approx\frac{-M(2h)+8M(h)-8M(-h)+M(-2h)}{12h},\qquad
M''(0)\approx\frac{-M(2h)+16M(h)-30M(0)+16M(-h)-M(-2h)}{12h^2},$$
and the 3rd/4th-derivative stencils are $O(h^2)$. With $h\sim10^{-2}$ this
recovers $E[X]$, $E[X^2]$, $E[X^3]$ and the cumulants to $\sim10^{-5}$–$10^{-2}$,
matching the closed forms in `test_mgf.py`. Continuous mgfs are integrated by the
midpoint rule (`_integrate`, the `~SM-06` quadrature idiom) before differentiating.

## Where this goes

- `~ST-05` (expectation, $E[X]$, variance, raw moments) — the quantities this
  module *generates*; `mean`/`variance` here are its definitions, used as ground
  truth.
- `~MA-10` (Laplace/Fourier transforms) — the mgf is the two-sided Laplace
  transform of the density at $s=-t$; the product rule of §5 is the convolution
  theorem and uniqueness (§6) is transform invertibility.
- `~SM-03` (partition function & ensembles) — $\ln Z(\beta)$ is the cumulant
  generating function of the energy (§8); $U$ and $C$ are its first two cumulants.
- `~ST-17` (the mgf technique & normal sampling distributions) — recognize the
  mgf of a sum/transform to name its distribution; the $\chi^2$, $t$, $F$ laws are
  derived this way.
- `~ST-07`/`~ST-08`/`~ST-09`/`~ST-11`/`~ST-12` (binomial, geometric/negative
  binomial, Poisson, gamma, normal) — each named law's mean, variance and
  additivity come straight from its mgf in §7.
- `~ST-18` (central limit theorem) — the standardized-sum mgf of §4–§5 converges
  to $e^{t^2/2}$, the normal mgf; uniqueness then gives the CLT.
