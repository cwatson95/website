# ST-08 — Geometric & Negative Binomial Distributions (notes)

The binomial distribution (`~ST-07`) fixes the number of independent Bernoulli$(p)$
trials at $n$ and asks how many **successes** occur. Turn the question around: fix
the number of successes and ask how many **trials** it takes. Asking for the
*first* success gives the **geometric** distribution; asking for the *$r$-th*
success gives the **negative binomial**. These are the two discrete *waiting-time*
laws, and they sit one short bridge from the continuous waiting times of `~ST-11`
(exponential and gamma).

Citation key (full details + granularity in `refs.md`): **PSU L$n$** = Penn State
STAT 414 OER, Lesson $n$; **HTZ** = Hogg, Tanis & Zimmerman, *Probability and
Statistical Inference* (cited at **chapter** level). Throughout, write $q=1-p$ for
the failure probability, and let $X$ count **trials** (so $X\ge 1$), the
convention STAT 414 / HTZ use.

## 1. The geometric pmf and its normalization

Run independent Bernoulli$(p)$ trials until the first success. The event
$\{X=x\}$ is "$x-1$ failures then a success," and by independence [PSU L11]
$$f(x)=P(X=x)=\underbrace{(1-p)^{x-1}}_{x-1\ \text{failures}}\,\underbrace{p}_{\text{success}},
\qquad x=1,2,3,\dots$$
This is `geometric_pmf(x, p)`. It is a genuine pmf because the **geometric series**
sums to one,
$$\sum_{x=1}^{\infty}q^{x-1}p=p\sum_{k=0}^{\infty}q^{k}=\frac{p}{1-q}=\frac{p}{p}=1,$$
which is the identity that names the distribution. The decreasing geometric shape
means $x=1$ is always the **mode** — the single most likely waiting time is one
trial, for every $p$. (`test_geometric_pmf_values`, `test_geometric_normalization`.)

## 2. The cdf and the survival function

Summing the pmf is again a finite geometric series [PSU L11],
$$P(X\le x)=\sum_{k=1}^{x}q^{k-1}p=p\,\frac{1-q^{x}}{1-q}=1-q^{x},
\qquad x=1,2,\dots,$$
so `geometric_cdf(x, p)` $=1-(1-p)^{\lfloor x\rfloor}$ and the **survival function**
is the strikingly simple
$$P(X>x)=1-P(X\le x)=q^{x}=(1-p)^{x},$$
which is `geometric_sf(x, p)`. The survival has an immediate meaning: $P(X>x)$ is
the probability that the **first $x$ trials are all failures**, $q^x$, with no need
to sum anything. This closed form is what makes §3 below trivial.
(`test_geometric_cdf_and_survival`.)

## 3. The memoryless property — and its uniqueness

Condition on having already waited past trial $m$ with no success, and ask for the
chance of waiting at least $n$ more. Using the survival form of §2 [PSU L11; HTZ
Ch. 3],
$$P(X>m+n\mid X>m)=\frac{P(X>m+n)}{P(X>m)}=\frac{q^{\,m+n}}{q^{\,m}}=q^{\,n}=P(X>n).$$
The past $m$ failures are *forgotten*: a coin that has shown $m$ tails is, going
forward, exactly as fresh as a new coin. `memoryless_check(m, n, p)` returns the
pair $\big(P(X>m+n\mid X>m),\,P(X>n)\big)$, which are equal for every $m,n,p$.

This property is **characteristic**: the geometric is the *only* discrete
distribution on $\{1,2,\dots\}$ with no memory. If $S(x)=P(X>x)$ satisfies
$S(m+n)=S(m)\,S(n)$ for all positive integers, then $S(x)=S(1)^x=q^x$ — a geometric
tail and nothing else. (The continuous solutions of the same functional equation
are $S(t)=e^{-\lambda t}$, the **exponential** survival of `~ST-11` — §8.)
(`test_memoryless_property`.)

## 4. Mean and variance from the series

Differentiate the geometric series with respect to $q$ to extract moments. From
$\sum_{x\ge1}q^{x}=q/(1-q)$,
$$\sum_{x=1}^{\infty}x\,q^{x-1}=\frac{d}{dq}\frac{1}{1-q}\Big|=\frac{1}{(1-q)^{2}}=\frac{1}{p^{2}}
\;\Longrightarrow\;
E[X]=\sum_{x\ge1}x\,q^{x-1}p=\frac{p}{p^{2}}=\frac{1}{p}.$$
So `geometric_mean(p)` $=1/p$: a rarer success (smaller $p$) means a longer
expected wait, in exact inverse proportion. For the variance use the second
factorial moment,
$$\sum_{x=2}^{\infty}x(x-1)q^{x-2}=\frac{2}{(1-q)^{3}}=\frac{2}{p^{3}}
\;\Longrightarrow\;
E[X(X-1)]=p\,q\cdot\frac{2}{p^{3}}=\frac{2q}{p^{2}},$$
$$\operatorname{Var}(X)=E[X(X-1)]+E[X]-\big(E[X]\big)^{2}
=\frac{2q}{p^{2}}+\frac{1}{p}-\frac{1}{p^{2}}=\frac{q}{p^{2}}=\frac{1-p}{p^{2}},$$
where the algebra uses $p-1=-q$. This is `geometric_var(p)`.
(`test_geometric_mean_matches_series`, `test_geometric_variance_matches_series`.)

## 5. The moment-generating function

The mgf is itself a geometric series in $e^{t}$ [PSU L9, L11; `~ST-06`]:
$$M(t)=E[e^{tX}]=\sum_{x=1}^{\infty}e^{tx}q^{x-1}p
=pe^{t}\sum_{x=1}^{\infty}(qe^{t})^{x-1}=\frac{pe^{t}}{1-qe^{t}},
\qquad qe^{t}<1\ \ (t<-\ln q).$$
This is `geometric_mgf(t, p)`. The moments fall out by differentiation at $t=0$,
the defining trick of `~ST-06`:
$$M'(0)=\frac{1}{p}=E[X],\qquad M''(0)=\frac{2-p}{p^{2}}=E[X^{2}],\qquad
\operatorname{Var}(X)=M''(0)-M'(0)^{2}=\frac{1-p}{p^{2}},$$
recovering §4. The test evaluates $M'(0)$ and $M''(0)$ by central differences and
checks them against `geometric_mean` and `geometric_var`.
(`test_geometric_mgf_derivative_is_mean_and_var`.)

## 6. The negative binomial: counting the trials to the $r$-th success

Now wait for the **$r$-th** success. The event $\{X=x\}$ requires the $x$-th trial
to be a success **and** exactly $r-1$ successes among the first $x-1$ trials. The
first $x-1$ trials are a binomial pattern (`~ST-07`), contributing
$\binom{x-1}{r-1}p^{r-1}q^{x-r}$, and the final trial contributes one more $p$
[PSU L11]:
$$f(x)=P(X=x)=\binom{x-1}{r-1}p^{r-1}q^{x-r}\cdot p
=\binom{x-1}{r-1}(1-p)^{x-r}\,p^{r},\qquad x=r,r+1,\dots$$
This is `negbinom_pmf(x, r, p)`; the binomial coefficient is the counting of
`~ST-02`. Normalization is the **negative binomial series**: substituting $k=x-r$
and $\binom{x-1}{r-1}=\binom{r-1+k}{k}$,
$$\sum_{x=r}^{\infty}\binom{x-1}{r-1}q^{x-r}p^{r}
=p^{r}\sum_{k=0}^{\infty}\binom{r-1+k}{k}q^{k}
=p^{r}\,(1-q)^{-r}=p^{r}p^{-r}=1.$$
(`test_negbinom_pmf_values`, `test_negbinom_normalization`.)

## 7. Negative-binomial moments, the $r=1$ reduction, and the sum relation

The fastest route to the moments and to the mgf is to recognize the negative
binomial as a **sum of $r$ independent geometrics**. Between consecutive successes
the process restarts (the memoryless property of §3), so if $G_1,\dots,G_r$ are the
i.i.d. geometric waiting times *between* successes, then the trial of the $r$-th
success is
$$X=G_1+G_2+\cdots+G_r,\qquad G_i\sim\text{Geometric}(p)\ \text{i.i.d.}$$
Means and variances of independent sums add, giving immediately [PSU L11; HTZ Ch. 3]
$$E[X]=r\cdot\frac1p=\frac{r}{p}=\texttt{negbinom\_mean},\qquad
\operatorname{Var}(X)=r\cdot\frac{1-p}{p^{2}}=\frac{r(1-p)}{p^{2}}=\texttt{negbinom\_var}.$$
The mgf of a sum is the **product** of mgfs (`~ST-06`), so the negative-binomial mgf
is the geometric mgf of §5 raised to the $r$,
$$M_X(t)=\big[M_G(t)\big]^{r}=\Big(\frac{pe^{t}}{1-qe^{t}}\Big)^{\!r}
=\texttt{negbinom\_mgf}(t,r,p),$$
which can also be derived directly from §6 by the same series manipulation,
$M_X(t)=p^{r}e^{tr}\sum_{k\ge0}\binom{r-1+k}{k}(qe^t)^k=p^re^{tr}(1-qe^t)^{-r}$.
Two corollaries close the loop. First, **$r=1$ is the geometric**:
$\binom{x-1}{0}q^{x-1}p=q^{x-1}p$, so `negbinom_pmf(x, 1, p)` equals
`geometric_pmf(x, p)` term by term. Second, the **sum relation** is checked
directly: the $r$-fold discrete convolution of the geometric pmf reproduces the
negative-binomial pmf. (`test_negbinom_mean_and_var_series`,
`test_negbinom_mgf_power_and_mean`, `test_geometric_equals_negbinom_r1`,
`test_sum_of_geometrics_is_negbinom`.)

## 8. The continuous limit: geometric $\to$ exponential

Shrink $p\to0$ and rescale. Since $P(X>x)=(1-p)^{x}$, the rescaled waiting time
$pX$ has tail
$$P(pX>t)=P\!\Big(X>\tfrac{t}{p}\Big)=(1-p)^{\lfloor t/p\rfloor}
=\exp\!\big[\lfloor t/p\rfloor\ln(1-p)\big]\ \xrightarrow[p\to0]{}\ e^{-t},$$
because $\ln(1-p)\approx-p$ and $\lfloor t/p\rfloor\,p\to t$. The limit $e^{-t}$ is
exactly the **exponential** survival function, and indeed
$e^{-t}=\int_t^\infty e^{-s}\,ds$ — the continuous tail. So the geometric is the
*discrete exponential*, and the negative binomial (a sum of geometrics) is the
*discrete gamma* (a sum of exponentials): the §3 memorylessness and the §7 sum
structure both carry over to `~ST-11`. The test confirms the limit numerically by
comparing `geometric_sf(t/p, p)` at tiny $p$ to the midpoint integral of $e^{-s}$.
(`test_exponential_limit_continuous`.)

## Where this goes

- `~ST-07` (the binomial — fixed $n$ trials, count successes) is the
  question this module inverts; `~ST-05` (pmf/cdf, $E[X]$, $\operatorname{Var}$)
  and `~ST-02` (the $\binom{x-1}{r-1}$ counting) supply the machinery, and `~ST-06`
  (mgf, uniqueness, moments by differentiation) powers §5 and §7.
- `~ST-09` (Poisson) is the next stop: the Poisson is the law of rare events, the
  limit $n\to\infty,\,np\to\lambda$ of the binomial, and the negative binomial is a
  **Gamma-mixture of Poissons** (overdispersed counts).
- `~ST-11` (exponential, gamma, chi-square) is the continuous mirror of §8 — the
  exponential inherits the geometric's memorylessness, the gamma inherits the
  negative binomial's sum-of-waits structure.
- `~MA-19` (probability & statistics foundations) — the parent the whole ST trunk
  deep-dives; the geometric series and binomial-coefficient identities used here
  are its standard tools.
