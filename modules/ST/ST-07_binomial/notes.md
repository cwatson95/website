# ST-07 — The Binomial Distribution (notes)

The binomial distribution is what you get by **counting** (`~ST-02`) inside a
**probability model** (`~ST-05`). Fix a single success/failure experiment — a
**Bernoulli trial** — and repeat it $n$ times independently; the number of
successes $X$ is the binomial random variable $\mathrm{Bin}(n,p)$. Almost every
formula in this module is one of three moves applied to that picture: (i) count
the equally-weighted success patterns with the binomial coefficient, (ii) sum the
$n$ Bernoulli indicators and use linearity / independence, or (iii) raise the
single-trial generating function to the $n$-th power. Those three give the pmf,
the moments, and the additivity/limit theorems respectively.

Citation key (full details + granularity in `refs.md`): **PSU L$n$** = Penn State
STAT 414 OER, Lesson $n$ (L9 mgf, **L10 the binomial distribution**); **HTZ** =
Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (the text STAT
414 follows), cited at **chapter level**. All sums run over integer $k$; write
$q\equiv 1-p$ throughout.

## 1. The Bernoulli trial — the $n=1$ atom

A **Bernoulli($p$) trial** is the simplest non-trivial random experiment: two
outcomes, *success* with probability $p$ and *failure* with probability $q=1-p$.
Encode it with the indicator $X\in\{0,1\}$ [PSU L10]:
$$P(X=1)=p,\qquad P(X=0)=1-p=q,\qquad
P(X=k)=p^k(1-p)^{1-k}\ \ (k=0,1).$$
Its mean and variance come straight from the `~ST-05` definitions:
$$E[X]=0\cdot q+1\cdot p=p,\qquad
E[X^2]=p,\qquad
\mathrm{Var}(X)=E[X^2]-E[X]^2=p-p^2=p(1-p).$$
Note $\mathrm{Var}(X)=pq$ is **maximal at $p=\tfrac12$** (a fair coin is the most
uncertain trial) and vanishes at $p=0,1$ (a sure thing has no variance). Code:
`bernoulli_pmf`, `bernoulli_mean`, `bernoulli_var`. The whole module is this atom,
repeated $n$ times.

## 2. The binomial pmf — counting success patterns

Run $n$ Bernoulli($p$) trials, **independent and identically distributed**, and
let $X=$ (number of successes). One *specific* sequence with $k$ successes and
$n-k$ failures — say $\mathrm{SSF\!\cdots F}$ — has probability $p^k q^{n-k}$ by
independence, **regardless of the order**. The number of distinct sequences with
exactly $k$ successes is the count of ways to choose which $k$ of the $n$ trials
succeed, the **binomial coefficient** (`~ST-02`)
$$\binom nk=\frac{n!}{k!\,(n-k)!}.$$
Summing the equal probabilities over those mutually exclusive sequences gives the
**binomial probability mass function** [PSU L10]
$$\boxed{\,P(X=k)=\binom nk\,p^k\,(1-p)^{n-k},\qquad k=0,1,\dots,n.\,}$$
Code: `binom_pmf(k, n, p)` (returning $0$ outside $0\le k\le n$). The name comes
from the coefficient; the structure "(count) $\times$ (per-pattern probability)"
is the template for every named discrete law in this trunk.

## 3. Normalization — the binomial theorem

Is this a legitimate pmf? Nonnegativity is clear. Totality is the **binomial
theorem** itself,
$$\sum_{k=0}^{n}\binom nk\,p^k\,q^{n-k}=(p+q)^n=(p+(1-p))^n=1^n=1.$$
So $\sum_k P(X=k)=1$: the algebraic identity that *names* the distribution is
exactly the statement that its probabilities sum to one. Code: in
`test_binomial.py`, `test_pmf_sums_to_one` checks
$\sum_{k=0}^n$ `binom_pmf(k,n,p)` $=1$ across a panel of $(n,p)$; the demo prints
the running sum as $1.0000000000$. The cumulative distribution function is the
partial sum
$$F(k)=P(X\le k)=\sum_{j=0}^{\lfloor k\rfloor}\binom nj p^j q^{n-j},$$
a right-continuous step function with $F(n)=1$ — code `binom_cdf`, with the pmf
recovered as the jump $F(k)-F(k-1)=P(X=k)$.

## 4. Mean and variance — $X$ as a sum of indicators

The slick derivation never touches the pmf. Write $X=\sum_{i=1}^{n}X_i$ with each
$X_i$ an independent Bernoulli($p$) indicator. **Linearity of expectation** (which
needs no independence) gives the mean instantly:
$$E[X]=\sum_{i=1}^{n}E[X_i]=\sum_{i=1}^{n}p=\boxed{\,np\,}.$$
Because the $X_i$ are **independent**, variances *also* add (cross-covariances
vanish), and each Bernoulli contributes $pq$ from §1:
$$\mathrm{Var}(X)=\sum_{i=1}^{n}\mathrm{Var}(X_i)=\sum_{i=1}^{n}p(1-p)
=\boxed{\,np(1-p)\,},\qquad \sigma=\sqrt{np(1-p)}.$$
Code: `binom_mean`, `binom_var`, `binom_std`; the tests reproduce both from the
*definitional* sums $\sum_k k\,P(k)$ and $\sum_k(k-np)^2P(k)$ and check they equal
$np$ and $npq$ (`test_mean_equals_np`, `test_variance_equals_npq`). The same
indicator argument shows the **fractional width** $\sigma/E[X]=\sqrt{q/(np)}\sim
1/\sqrt n$ shrinks with $n$ — the thermodynamic sharpening of the two-state system
in `~SM-01`. The **skewness** is $(1-2p)/\sqrt{npq}$: zero at $p=\tfrac12$
(symmetric), positive for $p<\tfrac12$ (right tail), negative for $p>\tfrac12$.
Code: `binom_skewness`.

## 5. The moment-generating function and additivity

The generating-function route (`~ST-06`) packages all of this and yields the key
structural theorem. The mgf of one Bernoulli trial is
$M_{X_i}(t)=E[e^{tX_i}]=q\cdot e^{0}+p\cdot e^{t}=q+pe^t$. For independent random
variables mgfs **multiply**, so the binomial mgf is that single factor raised to
the $n$-th power [PSU L9–L10]:
$$\boxed{\,M(t)=E[e^{tX}]=\big(q+pe^{t}\big)^{n}.\,}$$
Code: `binom_mgf(t, n, p)` (and `test_mgf_is_product_of_bernoulli_mgfs` verifies
$M(t)=[q+pe^t]^n$). Differentiating at $t=0$ returns the moments — the whole point
of the mgf:
$$M'(t)=n\,(q+pe^t)^{n-1}pe^t,\qquad M'(0)=n(q+p)^{n-1}p=np=E[X],$$
$$M''(0)=E[X^2]=np(1-p)+(np)^2,\qquad
\mathrm{Var}(X)=M''(0)-M'(0)^2=np(1-p).$$
Code checks these with numerical derivatives `_deriv1`, `_deriv2` of `binom_mgf`
at $0$ (`test_mgf_value_and_derivatives`). The related **probability generating
function** $G(s)=E[s^X]=(q+ps)^n$ (code `binom_pgf`) gives the **factorial
moments**: $G(1)=1$, $G'(1)=np=E[X]$, and $G''(1)=n(n-1)p^2=E[X(X-1)]$, from which
$\mathrm{Var}=G''(1)+G'(1)-G'(1)^2=np(1-p)$ again.

**Additivity (reproductive property).** Because $M(t)=(q+pe^t)^n$ depends on $n$
only as an exponent, the product of two such mgfs with a *common* $p$ is again
binomial:
$$M_{X_1}(t)\,M_{X_2}(t)=(q+pe^t)^{n_1}(q+pe^t)^{n_2}=(q+pe^t)^{n_1+n_2}
\;\Longrightarrow\; X_1+X_2\sim\mathrm{Bin}(n_1+n_2,\,p).$$
The uniqueness of mgfs (`~ST-06`) turns this equality of mgfs into equality of
distributions. Equivalently, at the level of pmfs it is **Vandermonde's identity**
$$\sum_{j}\binom{n_1}{j}\binom{n_2}{k-j}=\binom{n_1+n_2}{k}.$$
Code: `sum_two_binomials_pmf(k, n1, n2, p)` convolves the two pmfs and
`test_sum_of_binomials_is_binomial` checks it equals `binom_pmf(k, n1+n2, p)` for
every $k$ (the demo gets agreement to $\sim10^{-17}$ via `np.convolve`). The
hypothesis $p_1=p_2$ is essential — without it the sum is *not* binomial.

## 6. The mode — the most likely count

Where does the pmf peak? Examine the **ratio of successive terms**:
$$\frac{P(X=k)}{P(X=k-1)}
=\frac{\binom nk p^kq^{n-k}}{\binom{n}{k-1}p^{k-1}q^{n-k+1}}
=\frac{n-k+1}{k}\cdot\frac pq.$$
This ratio exceeds $1$ — the pmf is still rising — exactly while $(n-k+1)p>kq$,
i.e. $k<(n+1)p$, and drops below $1$ afterwards. Hence the pmf increases up to and
then decreases after $k^\star=\lfloor(n+1)p\rfloor$, the **mode** [PSU L10]:
$$\boxed{\,\text{mode}=\big\lfloor (n+1)p\big\rfloor.\,}$$
If $(n+1)p$ is an integer the ratio equals $1$ there, so $k=(n+1)p$ and
$k=(n+1)p-1$ are **both** modes (a tie); otherwise the mode is unique and sits
within one of the mean $np$. Code: `binom_mode(n, p)` returns the larger member of
any tie, and `test_mode_is_argmax` confirms $P(\text{mode})\ge P(\text{mode}\pm1)$
and matches a brute-force argmax.

## 7. The Poisson limit — rare events ($\to$ `~ST-09`)

Let $n\to\infty$ while $p\to0$ with the mean held fixed, $np=\lambda$. Then
$$P(X=k)=\binom nk p^kq^{n-k}
=\underbrace{\frac{n!}{k!\,(n-k)!}}_{}\Big(\frac\lambda n\Big)^k
\Big(1-\frac\lambda n\Big)^{n-k}
\;\longrightarrow\; \frac{\lambda^k e^{-\lambda}}{k!},$$
using $\frac{n!}{(n-k)!\,n^k}\to1$ and $(1-\lambda/n)^n\to e^{-\lambda}$. This is
the **Poisson distribution** (`~ST-09`): the law of the *count of rare events*
(many trials, tiny per-trial probability, moderate expected number). Code:
`test_poisson_limit` drives $p=\lambda/n$ with $\lambda=2.5$ and checks
$\max_k|\mathrm{Bin}-\mathrm{Poisson}|$ shrinks like $1/n$ (the demo:
$1.3\times10^{-2}\to1.2\times10^{-3}\to1.2\times10^{-4}$ as $n=25\to250\to2500$),
benchmarked against the self-contained `_poisson_pmf`.

## 8. The normal limit — de Moivre–Laplace ($\to$ `~ST-18`)

Hold $p$ fixed instead and let $n\to\infty$. By Stirling's approximation applied
to the pmf (or by the central limit theorem applied to the indicator sum of §4),
the binomial flattens into a **Gaussian** centred at the mean with the binomial
variance — the **de Moivre–Laplace theorem**:
$$P(X=k)\;\approx\;\frac{1}{\sqrt{2\pi\,npq}}\,
\exp\!\left(-\frac{(k-np)^2}{2\,npq}\right).$$
For the standardized variable $Z=(X-np)/\sqrt{npq}$ this is the historically
*first* central limit theorem; with the **continuity correction**
$P(a\le X\le b)\approx\Phi\big(\tfrac{b+0.5-np}{\sqrt{npq}}\big)-
\Phi\big(\tfrac{a-0.5-np}{\sqrt{npq}}\big)$ it is the everyday tool for binomial
tail probabilities at large $n$ (`~ST-18`). Code: `test_normal_approximation_near_peak`
compares `binom_pmf` to the self-contained `_normal_pdf` at $\mathrm{Bin}(100,\tfrac12)$
for $k$ near the peak (agreement to $\sim10^{-3}$; the demo prints
$0.0796$ vs $0.0798$ at $k=50$).

## Where this goes

- `~ST-02` (counting) and `~ST-05`/`~ST-06` (discrete RVs, expectation, mgf) — the
  three tools §2–§5 assemble into the binomial; this module is their first joint
  payoff.
- `~ST-08` (geometric & negative binomial) — the **waiting-time** duals of the same
  Bernoulli trials: instead of *fixing $n$ and counting successes*, fix the number
  of successes and count trials. Same atom, transposed question.
- `~ST-09` (Poisson) — the $n\to\infty,\ np=\lambda$ limit of §7; the binomial is
  the parent of the Poisson "law of rare events" and of the Poisson process.
- `~ST-18` (CLT & approximations) — the $n\to\infty,\ p$ fixed limit of §8; the
  normal approximation with continuity correction, and the historical de
  Moivre–Laplace special case of the central limit theorem.
- `~SM-01` (probability foundations / two-state systems) — the fair binomial
  $\mathrm{Bin}(N,\tfrac12)$ is the multiplicity of an $N$-spin paramagnet; the
  $1/\sqrt N$ peak-sharpening of §4 *is* the emergence of thermodynamics, and the
  Gaussian of §8 is its de Moivre–Laplace envelope. `~MA-19` carries the same
  binomial/normal pair in the maths trunk.
