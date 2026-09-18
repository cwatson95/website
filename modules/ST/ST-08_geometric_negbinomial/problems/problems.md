# ST-08 — Problems

Work each by hand, then check with `code/geometric_negbinomial.py`. Citations in
`../refs.md`; **PSU L11** = Penn State STAT 414 Lesson 11 (*Geometric and Negative
Binomial Distributions*). Convention: $X$ counts **trials**, $q=1-p$, support
$x=1,2,\dots$ (geometric) or $x=r,r+1,\dots$ (negative binomial).

### P1.  The geometric pmf is a probability distribution  *(PSU L11)*
For independent Bernoulli$(p)$ trials, argue $P(X=x)=(1-p)^{x-1}p$ ("$x-1$ failures,
then a success") and verify $\sum_{x\ge1}f(x)=1$ using the geometric series
$\sum_{k\ge0}q^k=1/(1-q)$. With $p=0.3$ evaluate $f(1)$ and $f(3)=q^2p$, and note
that $f$ is strictly decreasing, so the **mode is always $x=1$**.
*Check:* `geometric_pmf(1, 0.3)` $=0.3$; `geometric_pmf(3, 0.3)` $=0.147$
($=0.7^2\cdot0.3$); `sum(geometric_pmf(x,0.3) for x in range(1,2000))` $\approx1$.

**Solution.** The event $\{X=x\}$ is "$x-1$ failures (each prob. $q=1-p$) then a success,"
so by independence $f(x)=q^{x-1}p$ on $x=1,2,\dots$ It normalizes by the geometric series:
$$\sum_{x=1}^{\infty}q^{x-1}p=p\sum_{k=0}^{\infty}q^{k}=\frac{p}{1-q}=\frac pp=1.$$
At $p=0.3$: $f(1)=p=0.3$ and $f(3)=q^2p=0.7^2(0.3)=0.147$. Since $f(x+1)/f(x)=q<1$, the pmf
strictly decreases, so the single most likely wait is always $x=1$ — the **mode**. These
give `geometric_pmf(1, 0.3)`$=0.3$, `geometric_pmf(3, 0.3)`$=0.147$, and the truncated sum
$\approx1$.

### P2.  Cdf and survival from a finite geometric series  *(PSU L11)*
Sum the pmf to get $P(X\le x)=1-q^{x}$, hence the survival
$P(X>x)=q^{x}=(1-p)^{x}$ — interpret the latter directly as "the first $x$ trials
all fail." For $p=0.2$ compute $P(X>5)$ and $P(X\le 5)$, and confirm
$P(X\le 5)+P(X>5)=1$.
*Check:* `geometric_sf(5, 0.2)` $=0.32768$ ($=0.8^5$); `geometric_cdf(5, 0.2)`
$=0.67232$; their sum $=1.0$; `geometric_cdf(10, 0.2)` $=0.8926258176$.

**Solution.** Summing the pmf is a finite geometric series,
$$P(X\le x)=\sum_{k=1}^{x}q^{k-1}p=p\,\frac{1-q^{x}}{1-q}=1-q^{x},$$
so the survival is $P(X>x)=q^{x}=(1-p)^{x}$, reading directly as "the first $x$ trials all
fail." At $p=0.2$ ($q=0.8$),
$$P(X>5)=0.8^5=0.32768,\qquad P(X\le5)=1-0.32768=0.67232,$$
which sum to $1$ by construction. These are `geometric_sf(5, 0.2)`$=0.32768$,
`geometric_cdf(5, 0.2)`$=0.67232$ (sum $=1.0$), and `geometric_cdf(10, 0.2)`$=1-0.8^{10}=0.8926258176$.

### P3.  Mean and variance by differentiating the series  *(PSU L11; `~ST-06`)*
Differentiate $\sum_{x\ge1}q^{x}=q/(1-q)$ to get $\sum x q^{x-1}=1/p^2$, hence
$E[X]=1/p$; use the second factorial moment $\sum x(x-1)q^{x-2}=2/p^3$ to get
$\operatorname{Var}(X)=q/p^2=(1-p)/p^2$. Evaluate both at $p=0.25$ and note the
mean is the reciprocal of the success probability.
*Check:* `geometric_mean(0.25)` $=4.0$; `geometric_var(0.25)` $=12.0$
($=0.75/0.0625$).

**Solution.** Differentiate $\sum_{x\ge0}q^{x}=1/(1-q)$ once to pull down a factor of $x$:
$$\sum_{x\ge1}x\,q^{x-1}=\frac{d}{dq}\frac{1}{1-q}=\frac{1}{(1-q)^2}=\frac1{p^2}
\ \Rightarrow\ E[X]=p\sum_{x\ge1}x\,q^{x-1}=\frac1p.$$
Differentiating again gives $\sum_{x\ge2}x(x-1)q^{x-2}=2/p^3$, so $E[X(X-1)]=pq\cdot2/p^3=2q/p^2$
and
$$\operatorname{Var}(X)=E[X(X-1)]+E[X]-E[X]^2=\frac{2q}{p^2}+\frac1p-\frac1{p^2}=\frac{1-p}{p^2}.$$
At $p=0.25$ the mean is the reciprocal $1/p=4$; thus `geometric_mean(0.25)`$=4.0$ and
`geometric_var(0.25)`$=0.75/0.0625=12.0$.

### P4.  The memoryless property  *(PSU L11; HTZ Ch. 2)*
Using the survival form of P2, prove $P(X>m+n\mid X>m)=q^{m+n}/q^{m}=q^{n}=P(X>n)$:
a coin that has already shown $m$ tails is, going forward, as fresh as a new coin.
Take $p=0.2$, $m=10$, $n=4$ and show both sides equal $0.8^4$.
*Check:* `memoryless_check(10, 4, 0.2)` $=(0.4096,\,0.4096)$ (equal); both equal
$0.8^4=0.4096$.

**Solution.** Use the survival form of P2; since $\{X>m+n\}\subset\{X>m\}$,
$$P(X>m+n\mid X>m)=\frac{P(X>m+n)}{P(X>m)}=\frac{q^{\,m+n}}{q^{\,m}}=q^{\,n}=P(X>n).$$
The $q^{m}$ for the wasted first $m$ trials cancels: a coin that has already shown $m$ tails
is, going forward, as fresh as a new one. With $p=0.2,m=10,n=4$ both sides equal
$$q^{n}=0.8^4=0.4096,$$
which is `memoryless_check(10, 4, 0.2)`$=(0.4096,\,0.4096)$ — the two entries equal, each
$0.8^4$.

### P5.  Moments from the mgf  *(PSU L11; `~ST-06`)*
Sum the geometric series in $e^t$ to get $M(t)=pe^t/(1-qe^t)$ for $t<-\ln q$, and
show $M(0)=1$ and $M'(0)=1/p=E[X]$. Evaluate $M(0.1)$ at $p=0.4$ and confirm the
numerical derivative at $0$ reproduces the mean $2.5$.
*Check:* `geometric_mgf(0.0, 0.4)` $=1.0$; `geometric_mgf(0.1, 0.4)` $\approx1.31217$;
`(geometric_mgf(1e-6,0.4)-geometric_mgf(-1e-6,0.4))/2e-6` $\approx2.5=$
`geometric_mean(0.4)`.

**Solution.** Summing the geometric series in $e^t$ (with $q=1-p$),
$$M(t)=\sum_{x\ge1}e^{tx}q^{x-1}p=\frac{pe^t}{1-qe^t},\qquad t<-\ln q,$$
so $M(0)=p/(1-q)=p/p=1$. By the quotient rule at $t=0$ (numerator and denominator both equal
$p$ there),
$$M'(0)=\frac{p\cdot p-p(-q)}{p^2}=\frac{p+q}{p}=\frac1p=E[X].$$
At $p=0.4$, $1/p=2.5$, so `geometric_mgf(0.0, 0.4)`$=1.0$, `geometric_mgf(0.1, 0.4)`
$\approx1.31217$, and `(geometric_mgf(1e-6,0.4)-geometric_mgf(-1e-6,0.4))/2e-6`$\approx2.5=$
`geometric_mean(0.4)`.

### P6.  The negative binomial pmf  *(PSU L11; `~ST-02`)*
For the trial of the $r$-th success, argue $f(x)=\binom{x-1}{r-1}(1-p)^{x-r}p^{r}$
(the $x$-th trial succeeds; $r-1$ of the first $x-1$ succeed). With $r=3$, $p=0.25$
evaluate $f(3)$ (the fastest possible: SSS) and $f(5)=\binom{4}{2}q^{2}p^{3}$.
*Check:* `negbinom_pmf(3, 3, 0.25)` $=0.015625$ ($=0.25^3$);
`negbinom_pmf(5, 3, 0.25)` $\approx0.052734$ ($=6\cdot0.75^2\cdot0.25^3$).

**Solution.** For the $r$-th success at trial $x$, the final trial succeeds ($p$) and exactly
$r-1$ of the first $x-1$ trials succeed (a binomial pattern $\binom{x-1}{r-1}p^{r-1}q^{x-r}$),
so
$$f(x)=\binom{x-1}{r-1}(1-p)^{x-r}p^{r},\qquad x=r,r+1,\dots$$
With $r=3,p=0.25$ the fastest case is $x=3$ (the run SSS), $f(3)=\binom22(0.25)^3=0.015625$.
For $x=5$ there are $\binom42=6$ ways to place the $2$ early successes among the first $4$
trials:
$$f(5)=\binom42(0.75)^2(0.25)^3=6(0.5625)(0.015625)=0.052734.$$
These are `negbinom_pmf(3, 3, 0.25)`$=0.015625$ and `negbinom_pmf(5, 3, 0.25)`$\approx0.052734$.

### P7.  Negative-binomial moments as $r$ geometrics  *(PSU L11; HTZ Ch. 2)*
Write $X=G_1+\cdots+G_r$ with $G_i$ i.i.d. geometric$(p)$ (the process restarts
after each success). Because means and variances of independent sums add, deduce
$E[X]=r/p$ and $\operatorname{Var}(X)=r(1-p)/p^2$. Verify at $r=4$, $p=0.5$ that
these equal $r$ times the geometric values.
*Check:* `negbinom_mean(4, 0.5)` $=8.0=4\cdot$`geometric_mean(0.5)`;
`negbinom_var(4, 0.5)` $=8.0=4\cdot$`geometric_var(0.5)`.

**Solution.** After each success the memoryless process restarts, so the trial of the $r$-th
success splits into $r$ i.i.d. geometric waits, $X=G_1+\cdots+G_r$. Means add unconditionally
and variances add by independence:
$$E[X]=\sum_{i=1}^{r}E[G_i]=\frac rp,\qquad
\operatorname{Var}(X)=\sum_{i=1}^{r}\operatorname{Var}(G_i)=\frac{r(1-p)}{p^2}.$$
At $r=4,p=0.5$ the geometric pieces are $E[G]=1/p=2$ and $\operatorname{Var}(G)=(1-p)/p^2=2$,
so $E[X]=4(2)=8$ and $\operatorname{Var}(X)=4(2)=8$. These are `negbinom_mean(4, 0.5)`
$=8.0=4\cdot$`geometric_mean(0.5)` and `negbinom_var(4, 0.5)`$=8.0=4\cdot$`geometric_var(0.5)`.

### P8.  Geometric $=$ negbinom$(r{=}1)$, and the mgf product  *(PSU L11)*
Show $\binom{x-1}{0}q^{x-1}p=q^{x-1}p$, so the negative binomial with $r=1$ **is**
the geometric. Then, since the mgf of a sum is the product of mgfs, show
$M_{\text{NB}}(t)=\big(pe^t/(1-qe^t)\big)^r$ equals the geometric mgf raised to $r$.
Verify both with $p=0.3$.
*Check:* `negbinom_pmf(4, 1, 0.3)` $=0.1029=$ `geometric_pmf(4, 0.3)`;
`negbinom_mgf(0.1, 2, 0.3)` $\approx2.144983=$ `geometric_mgf(0.1, 0.3)**2`.

**Solution.** Setting $r=1$ collapses the binomial coefficient, $\binom{x-1}{0}=1$, so the
negative-binomial pmf reduces termwise to the geometric:
$$\binom{x-1}{0}q^{x-1}p=q^{x-1}p.$$
Because the negative binomial is a sum of $r$ i.i.d. geometrics (P7), its mgf is the geometric
mgf raised to the $r$,
$$M_{\text{NB}}(t)=\big[M_{\text{geom}}(t)\big]^{r}=\Big(\frac{pe^t}{1-qe^t}\Big)^{r}.$$
At $p=0.3$: `negbinom_pmf(4, 1, 0.3)`$=0.7^3(0.3)=0.1029=$`geometric_pmf(4, 0.3)`, and
`negbinom_mgf(0.1, 2, 0.3)`$\approx2.144983=$`geometric_mgf(0.1, 0.3)**2`.
