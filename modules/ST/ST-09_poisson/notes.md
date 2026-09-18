# ST-09 — The Poisson Distribution (notes)

Many experiments count something: calls arriving at a switchboard in an hour,
$\alpha$-particles registered by a detector in ten seconds, typos on a page,
photons hitting a photocathode in a microsecond (`~QO-01`), ionizing collisions
in a discharge cell (`~PK-04`). What unites them is that the events are
**independent**, occur at a **constant average rate**, and are individually
**rare** while the number of opportunities is **large**. The distribution of such
a count is the **Poisson distribution**, $X\sim\mathrm{Poisson}(\lambda)$, with
the single parameter $\lambda=E[X]$. This module derives its pmf, shows that mean
and variance are *both* $\lambda$, and gives its two canonical origins: the
**law of rare events** (a binomial limit, `~ST-07`) and the **Poisson process**
(whose waiting times are exponential, `~ST-11`).

Citation key (full details + granularity in `refs.md`): **STAT 414** = Penn State
STAT 414 OER, **Lesson 12** ("The Poisson Distribution"), cited by sub-lesson
**L12.1 / L12.2**; **HTZ** = Hogg, Tanis & Zimmerman, *Probability and
Statistical Inference* (the text STAT 414 follows), cited at **chapter level**.

## 1. The pmf and its normalization

A Poisson random variable takes the non-negative integers $k=0,1,2,\dots$ with
probabilities [STAT 414 L12.1]
$$\boxed{\;P(X=k)=\frac{e^{-\lambda}\,\lambda^{k}}{k!}\;},\qquad \lambda>0 .$$
This is `poisson_pmf(k, lam)`, evaluated as $\exp\!\big(k\ln\lambda-\lambda-\ln k!\big)$
so that the separately huge $\lambda^{k}$ and $k!$ never overflow. It is a
legitimate pmf because the probabilities are non-negative and sum to one, the sum
being the **Maclaurin series of the exponential**,
$$\sum_{k=0}^{\infty}\frac{e^{-\lambda}\lambda^{k}}{k!}
=e^{-\lambda}\sum_{k=0}^{\infty}\frac{\lambda^{k}}{k!}
=e^{-\lambda}\,e^{\lambda}=1 .$$
`poisson_normalization(lam, kmax)` is this sum truncated at $k_{\max}$; the tail
$\sum_{k>k_{\max}}$ falls off faster than geometrically, so a few hundred terms
already give $1$ to machine precision. A useful structural fact is the
**recurrence** obtained by dividing consecutive terms,
$$\frac{P(X=k+1)}{P(X=k)}=\frac{\lambda}{k+1}
\quad\Longrightarrow\quad P(X=k+1)=\frac{\lambda}{k+1}\,P(X=k),$$
starting from $P(X=0)=e^{-\lambda}$ (tested in `test_pmf_known_values_and_recurrence`).
The ratio exceeds $1$ while $k+1<\lambda$ and drops below it after, so the pmf
rises then falls with **mode** $\lfloor\lambda\rfloor$ — `poisson_mode(lam)` —
(and a tie at $\lambda-1$ and $\lambda$ when $\lambda\in\mathbb Z^{+}$). The
`poisson_cdf(k, lam)` is the partial sum $F(k)=\sum_{j=0}^{\lfloor k\rfloor}P(X=j)$.

## 2. Mean and variance — the Poisson signature

Compute $E[X]$ directly from the pmf. The $k=0$ term drops, and shifting the
index $k\to k+1$ regrows the full exponential series [STAT 414 L12.2]:
$$E[X]=\sum_{k=0}^{\infty}k\,\frac{e^{-\lambda}\lambda^{k}}{k!}
=\lambda e^{-\lambda}\sum_{k=1}^{\infty}\frac{\lambda^{k-1}}{(k-1)!}
=\lambda e^{-\lambda}e^{\lambda}=\lambda .$$
So `poisson_mean(lam)` $=\lambda$. The cleanest route to the variance is the
**second factorial moment**, because the $k(k-1)$ kills two terms and shifts the
series by two:
$$E[X(X-1)]=\sum_{k=0}^{\infty}k(k-1)\frac{e^{-\lambda}\lambda^{k}}{k!}
=\lambda^{2}e^{-\lambda}\sum_{k=2}^{\infty}\frac{\lambda^{k-2}}{(k-2)!}=\lambda^{2}.$$
This is `poisson_factorial_moment(2, lam)` $=\lambda^{2}$, and more generally
$E[X(X-1)\cdots(X-r+1)]=\lambda^{r}$ (`poisson_factorial_moment(r, lam)`). Then
$$\mathrm{Var}(X)=E[X^{2}]-\big(E[X]\big)^{2}
=\underbrace{E[X(X-1)]}_{\lambda^{2}}+\underbrace{E[X]}_{\lambda}-\lambda^{2}
=\lambda .$$
Hence the **Poisson signature**, verified by `poisson_var` and
`test_variance_equals_lambda_and_equals_mean`:
$$\boxed{\;E[X]=\mathrm{Var}(X)=\lambda\;},\qquad
\sigma=\sqrt{\lambda}\ \ (\texttt{poisson\_std}).$$
Mean equals variance is the experimental fingerprint of a Poisson count: in
`~QO-01` it is **shot noise** $\sigma_n=\sqrt{\langle n\rangle}$, the photon-number
fluctuation of a coherent beam; light with $\mathrm{Var}(n)<\langle n\rangle$ is
"sub-Poissonian" and has no classical-field description.

## 3. The moment-generating function

Summing $e^{tk}$ against the pmf is, again, an exponential series — now with
argument $\lambda e^{t}$ [STAT 414 L12.2; `~ST-06`]:
$$M(t)=E\!\big[e^{tX}\big]
=\sum_{k=0}^{\infty}e^{tk}\frac{e^{-\lambda}\lambda^{k}}{k!}
=e^{-\lambda}\sum_{k=0}^{\infty}\frac{(\lambda e^{t})^{k}}{k!}
=e^{-\lambda}e^{\lambda e^{t}}
=\boxed{\,\exp\!\big(\lambda(e^{t}-1)\big)\,}.$$
This is `poisson_mgf(t, lam)`, with $M(0)=1$ for every $\lambda$. Differentiating
and setting $t=0$ recovers the moments without resumming any series:
$$M'(t)=\lambda e^{t}\,M(t),\qquad
M'(0)=\lambda=E[X];$$
$$M''(t)=\big(\lambda e^{t}+\lambda^{2}e^{2t}\big)M(t),\qquad
M''(0)=\lambda+\lambda^{2}=E[X^{2}],$$
so $\mathrm{Var}(X)=M''(0)-M'(0)^{2}=\lambda$ again — the check in
`test_mgf_value_and_moment_derivatives`, evaluated there by central differences of
`poisson_mgf`. The closely related **probability-generating function**
$G(s)=E[s^{X}]=\exp\!\big(\lambda(s-1)\big)$ — `poisson_pgf(s, lam)`, just
$M(\ln s)$ — has the cleaner property that its derivatives at $s=1$ are the
**factorial moments**:
$$G^{(r)}(1)=\lambda^{r}=E\!\big[X(X-1)\cdots(X-r+1)\big],$$
matching `poisson_factorial_moment` (`test_pgf_factorial_moments`). The mgf is the
engine of §4 and §6: combined with the **uniqueness theorem** (`~ST-06`) — equal
mgfs imply equal distributions — it turns limits and sums of random variables into
ordinary algebra of exponentials.

## 4. The law of rare events — the binomial limit

The Poisson is what the **binomial** (`~ST-07`) becomes when successes are rare
but trials are many. Take $X_n\sim\mathrm{Bin}(n,p_n)$ with the mean held fixed,
$np_n=\lambda$, so $p_n=\lambda/n\to0$, and let $n\to\infty$. The mgf route is
immediate: $M_{X_n}(t)=\big(1-p_n+p_n e^{t}\big)^{n}=\big(1+\tfrac{\lambda}{n}(e^{t}-1)\big)^{n}$,
and using $(1+a/n)^{n}\to e^{a}$,
$$M_{X_n}(t)=\Big(1+\frac{\lambda(e^{t}-1)}{n}\Big)^{n}
\;\xrightarrow[n\to\infty]{}\;\exp\!\big(\lambda(e^{t}-1)\big)=M_{\mathrm{Poisson}(\lambda)}(t),$$
so by uniqueness $X_n\Rightarrow\mathrm{Poisson}(\lambda)$ [STAT 414 L12.1]. The
same limit at the level of the pmf reads [STAT 414 L12.1]
$$\binom{n}{k}\Big(\frac{\lambda}{n}\Big)^{k}\Big(1-\frac{\lambda}{n}\Big)^{n-k}
=\underbrace{\frac{n(n{-}1)\cdots(n{-}k{+}1)}{n^{k}}}_{\to\,1}\,
\frac{\lambda^{k}}{k!}\,
\underbrace{\Big(1-\frac{\lambda}{n}\Big)^{n}}_{\to\,e^{-\lambda}}\,
\underbrace{\Big(1-\frac{\lambda}{n}\Big)^{-k}}_{\to\,1}
\;\longrightarrow\;\frac{e^{-\lambda}\lambda^{k}}{k!}.$$
`poisson_limit_of_binomial(n, p)` measures the convergence as
$\max_k\lvert\mathrm{Bin}(n,p)-\mathrm{Poisson}(np)\rvert$; with $\lambda=2$ fixed
the gap falls $\approx7.5\times10^{-2}\to1.5\times10^{-2}\to2.7\times10^{-3}\to2.7\times10^{-4}$
as $n=5,20,100,1000$ — roughly $\propto1/n$ — the content of
`test_limit_of_binomial_law_of_rare_events`. This is why the Poisson is the model
for "$n$ large, $p$ small" counts: defects per batch, rare-disease cases per
population, decays per second. The error of the approximation is itself bounded by
$\lesssim n p^{2}=\lambda p$ (Le Cam), so it is the *small $p$*, not just large
$n$, that makes it good (`~ST-18` gives the complementary large-$\lambda$ normal
approximation).

## 5. The Poisson process

The second origin is dynamical. Let events occur on $[0,\infty)$ so that (i)
disjoint intervals are **independent**, (ii) the chance of one event in a short
interval $\mathrm{d}t$ is $\nu\,\mathrm{d}t$ for a constant rate $\nu$, and (iii)
two-at-once has probability $o(\mathrm{d}t)$. Let $N(t)$ be the number of events
in $[0,t]$ and $p_k(t)=P(N(t)=k)$. Bookkeeping over $[0,t+\mathrm{d}t]$ gives the
**master equation** (a birth process; cf. the rate equations of `~PK-04`)
$$p_k'(t)=-\nu\,p_k(t)+\nu\,p_{k-1}(t),\qquad p_{-1}\equiv0,\ p_k(0)=\delta_{k0},$$
whose solution is the Poisson pmf with $\lambda=\nu t$:
$$P\big(N(t)=k\big)=\frac{e^{-\nu t}(\nu t)^{k}}{k!}=\mathrm{Poisson}(\lambda),
\qquad \lambda=\nu t .$$
So $\lambda$ is "rate $\times$ window," and the count over a length-$t$ window of a
rate-$\nu$ process is exactly Poisson. The **waiting times** of this process are
the bridge to the continuous distributions: the time to the *first* event is
**exponential**, and the time to the $k$-th event is **gamma**$(k,\nu)$
(`~ST-11`). The identity that ties the two together — and the continuous check in
`test_poisson_process_gamma_integral` — is that "fewer than $k$ events by time
$\lambda$" equals "the $k$-th arrival is later than $\lambda$":
$$\boxed{\;P\big(N\le k-1\big)=\sum_{j=0}^{k-1}\frac{e^{-\lambda}\lambda^{j}}{j!}
=\int_{\lambda}^{\infty}\frac{t^{\,k-1}e^{-t}}{(k-1)!}\,\mathrm{d}t\;}$$
(unit rate $\nu=1$). The right side is the survival function of a $\mathrm{Gamma}(k,1)$
arrival time; the code evaluates it with the midpoint integrator `_integrate` and
matches `poisson_cdf(k-1, lam)` — e.g. for $\lambda=3,k=4$ both equal $0.647232$.

## 6. The reproductive (additivity) property

Independent Poisson counts **add**, and the sum is Poisson — the natural
consequence of merging two independent streams of events into one. If
$X_i\sim\mathrm{Poisson}(\lambda_i)$ are independent, the mgf of the sum is the
product of the mgfs (`~ST-06`):
$$M_{\sum_i X_i}(t)=\prod_i\exp\!\big(\lambda_i(e^{t}-1)\big)
=\exp\!\Big(\Big(\textstyle\sum_i\lambda_i\Big)(e^{t}-1)\Big),$$
which is the mgf of $\mathrm{Poisson}\big(\sum_i\lambda_i\big)$; by uniqueness
[STAT 414 L12.2],
$$\boxed{\;\sum_i X_i\sim\mathrm{Poisson}\Big(\sum_i\lambda_i\Big)\;}.$$
`sum_of_poissons(lams)` returns the combined parameter $\sum_i\lambda_i$. At the
pmf level the same statement is a **Vandermonde-style convolution**,
$$P(X_1+X_2=k)=\sum_{j=0}^{k}\frac{e^{-\lambda_1}\lambda_1^{j}}{j!}\,
\frac{e^{-\lambda_2}\lambda_2^{k-j}}{(k-j)!}
=\frac{e^{-(\lambda_1+\lambda_2)}}{k!}\sum_{j=0}^{k}\binom{k}{j}\lambda_1^{j}\lambda_2^{k-j}
=\frac{e^{-(\lambda_1+\lambda_2)}(\lambda_1+\lambda_2)^{k}}{k!},$$
the inner sum being the binomial theorem. `poisson_convolution_pmf(k, l1, l2)`
computes the convolution and `test_sum_of_independent_poissons` checks it equals
`poisson_pmf(k, l1+l2)` (e.g. $0.091226$ at $k=4,\lambda_1=3,\lambda_2=4$). The
converse (**Raikov's theorem**) also holds: if a sum of independent variables is
Poisson, each summand is Poisson — the Poisson family is closed and indivisible in
a strong sense.

## 7. Shape and the normal limit

Higher central moments give the shape. They come from the mgf the same way the
raw moments did in §3 — by differentiating and setting $t=0$ — only now we
differentiate the **central** mgf. Every step:

1. Central moments are ordinary moments of $X-\mu$, so they are the $t=0$
   derivatives of
   $$M_c(t)=E\!\big[e^{t(X-\mu)}\big]=e^{-\mu t}M(t).$$
2. Write $M_c=e^{S}$ where, for the Poisson ($\mu=\lambda$, §3),
   $$S(t)=\ln M(t)-\mu t=\lambda\big(e^{t}-1\big)-\lambda t .$$
   Then $S(0)=0$, $S'(t)=\lambda(e^{t}-1)$ so $S'(0)=0$, and every higher
   derivative is $S^{(n)}(t)=\lambda e^{t}$, so
   $$S^{(n)}(0)=\lambda\qquad(n\ge2).$$
3. Differentiate $M_c=e^{S}$ by the chain and product rules (each line is the
   derivative of the one before):
   $$M_c'=S'e^{S},\qquad
   M_c''=\big(S''+S'^2\big)e^{S},\qquad
   M_c'''=\big(S'''+3S''S'+S'^3\big)e^{S},$$
   $$M_c^{(4)}=\big(S^{(4)}+4S'''S'+3S''^2+6S''S'^2+S'^4\big)e^{S}.$$
4. Evaluate at $t=0$, where $S=S'=0$ kills every term containing $S'$ and sets
   $e^{S}=1$:
   $$\mu_2=S''(0)=\lambda\ (=\sigma^2,\ §3),\qquad
   \boxed{\;\mu_3=S'''(0)=\lambda\;},\qquad
   \boxed{\;\mu_4=S^{(4)}(0)+3\big[S''(0)\big]^2=\lambda+3\lambda^{2}\;}.$$

Hence
$$\text{skewness}=\frac{\mu_3}{\sigma^{3}}=\frac{\lambda}{\lambda^{3/2}}=\frac{1}{\sqrt{\lambda}}>0,\qquad
\text{excess kurtosis}=\frac{\mu_4}{\sigma^{4}}-3=\frac{\lambda+3\lambda^2}{\lambda^{2}}-3=\frac{1}{\lambda},$$
which are `poisson_skewness(lam)` and `poisson_excess_kurtosis(lam)`
(`test_skewness_and_excess_kurtosis`). Both are positive and both vanish as
$\lambda\to\infty$: the distribution is always right-skewed but **becomes
symmetric and Gaussian for large $\lambda$**. Indeed a $\mathrm{Poisson}(\lambda)$
is a sum of $\lambda$ independent $\mathrm{Poisson}(1)$'s (§6), so the central
limit theorem (`~ST-18`) gives
$$\frac{X-\lambda}{\sqrt{\lambda}}\;\xrightarrow[\lambda\to\infty]{d}\;N(0,1),$$
the standard **normal approximation to the Poisson** (used with a continuity
correction). Thus the Poisson sits exactly between the discrete and continuous
worlds of this trunk: it is the rare-events limit of the binomial below it
(`~ST-07`), the event-count of a process whose waiting times are exponential/gamma
beside it (`~ST-11`), and a near-Gaussian above it (`~ST-12`, `~ST-18`).

## Where this goes

- `~ST-07` (binomial) — the Poisson is its $n\to\infty,\,p\to0,\,np\to\lambda$
  **law of rare events** limit (§4); `~ST-05`/`~ST-06` supply the $E[X]$,
  $\mathrm{Var}(X)$, and mgf machinery used throughout.
- `~ST-08` (geometric / negative binomial) — the partner discrete laws; `~ST-11`
  (exponential, gamma, chi-square) — the **continuous waiting times** of the same
  Poisson process (§5), via the boxed gamma-integral identity.
- `~ST-18` (central limit theorem) and `~ST-12` (normal) — the large-$\lambda$
  Gaussian limit of §7; `~SM-01` (counting, rare-event limit) on the statistical
  mechanics side.
- `~QO-01` (quantized light) — coherent-state **photon counting** is Poissonian,
  $\mathrm{Var}(n)=\langle n\rangle$ (shot noise of §2); sub-Poissonian light is
  the nonclassical antithesis.
- `~PK-04` (atomic & molecular kinetics) — counts of independent collision /
  reaction events, and the birth-process master equation of §5 reappearing as the
  rate equations of the user's KrF plasma-kinetics code.
