# ST-07 — Problems

Work each by hand, then check with `code/binomial.py`. Citations in `../refs.md`;
**PSU L10** = Penn State STAT 414, Lesson 10 *The Binomial Distribution*.
Throughout $q\equiv 1-p$, and "trial" means one Bernoulli($p$) experiment
(success prob. $p$). A binomial random variable counts successes in $n$ such
independent, identical trials, $X\sim\mathrm{Bin}(n,p)$ (`~ST-02`, `~ST-05`).

### P1.  The Bernoulli atom and its maximal variance  *(PSU L10)*
For a single Bernoulli($p$) trial with indicator $X\in\{0,1\}$, derive
$E[X]=p$ and $\mathrm{Var}(X)=p(1-p)$ directly from the `~ST-05` definitions, and
show the variance is **maximized at $p=\tfrac12$** (differentiate $p(1-p)$) and
vanishes at $p=0,1$. Explain in one sentence why a fair coin is the "most
uncertain" trial.
*Check:* `bernoulli_var(0.5)` $=0.25$ (the maximum); `bernoulli_var(0.3)` $=0.21<0.25$;
and `bernoulli_mean(p) == binom_mean(1, p)`, `bernoulli_var(p) == binom_var(1, p)`
for any $p$ (the $n=1$ binomial).

**Solution.** With $P(X=1)=p$, $P(X=0)=1-p$ and $X^2=X$,
$$E[X]=0(1-p)+1\cdot p=p,\qquad \operatorname{Var}(X)=E[X^2]-E[X]^2=p-p^2=p(1-p).$$
Setting $\tfrac{d}{dp}\big[p(1-p)\big]=1-2p=0$ locates the unique maximum at $p=\tfrac12$,
where $\operatorname{Var}=\tfrac14$; the variance vanishes at $p=0,1$ (a sure outcome cannot
fluctuate). A fair coin is the "most uncertain" trial because equal $\tfrac12$–$\tfrac12$
odds give the widest spread of a single $\{0,1\}$ outcome. Thus `bernoulli_var(0.5)`$=0.25$
exceeds `bernoulli_var(0.3)`$=0.21$, and since these *are* the $n=1$ binomial,
`bernoulli_mean(p) == binom_mean(1, p)` and `bernoulli_var(p) == binom_var(1, p)`.

### P2.  The pmf and a concrete count  *(PSU L10; `~ST-02`)*
A biased coin lands heads with $p=0.3$; flip it $n=5$ times. Using
$P(X=k)=\binom nk p^kq^{n-k}$, compute $P(X=2)$ by hand: there are $\binom52=10$
arrangements, each of probability $0.3^2\,0.7^3$. Then write $P(X\le2)$ as a sum of
three terms. Confirm $\sum_{k=0}^5 P(X=k)=1$ is the binomial theorem $(0.3+0.7)^5$.
*Check:* `binom_pmf(2, 5, 0.3)` $=0.3087$; `binom_cdf(2, 5, 0.3)` $=0.83692$;
`sum(binom_pmf(k, 5, 0.3) for k in range(6))` $=1.0$.

**Solution.** There are $\binom52=\tfrac{5!}{2!\,3!}=10$ ways to place the $2$ heads among
$5$ flips, each sequence carrying $0.3^2\,0.7^3$, so
$$P(X=2)=\binom52(0.3)^2(0.7)^3=10(0.09)(0.343)=0.3087.$$
Summing the first three terms gives the cdf,
$$P(X\le2)=0.7^5+\binom51(0.3)(0.7)^4+0.3087=0.16807+0.36015+0.3087=0.83692.$$
Over all $k$ the pmf sums to $(0.7+0.3)^5=1$ by the binomial theorem — normalization *is*
that identity. These are `binom_pmf(2, 5, 0.3)`$=0.3087$, `binom_cdf(2, 5, 0.3)`$=0.83692$,
and `sum(binom_pmf(k, 5, 0.3) for k in range(6))`$=1.0$.

### P3.  Mean and variance without the pmf  *(PSU L10)*
Write $X=\sum_{i=1}^{12}X_i$ as a sum of $n=12$ independent Bernoulli($p=0.25$)
indicators. Use **linearity of expectation** to get $E[X]=np$ and **independence**
(variances add) to get $\mathrm{Var}(X)=np(1-p)$, *without* summing $k\,P(X=k)$.
Then verify the answers equal the definitional sums.
*Check:* `binom_mean(12, 0.25)` $=3.0$, `binom_var(12, 0.25)` $=2.25$,
`binom_std(12, 0.25)` $=1.5$; and the brute sums
`sum(k*binom_pmf(k,12,0.25) for k in range(13))` $=3.0$,
`sum((k-3)**2*binom_pmf(k,12,0.25) for k in range(13))` $=2.25$.

**Solution.** Decompose $X=\sum_{i=1}^{12}X_i$ into independent $\text{Bernoulli}(0.25)$
indicators. Linearity of expectation (no independence needed) adds $12$ copies of $p$:
$$E[X]=\sum_{i=1}^{12}E[X_i]=12(0.25)=np=3.0.$$
Because the $X_i$ are independent, their variances also add, each contributing $p(1-p)$:
$$\operatorname{Var}(X)=\sum_{i=1}^{12}p(1-p)=12(0.25)(0.75)=np(1-p)=2.25,
\qquad \sigma=\sqrt{2.25}=1.5.$$
These match the brute definitional sums $\sum_k k\,P(k)=3.0$ and $\sum_k(k-3)^2P(k)=2.25$,
i.e. `binom_mean(12, 0.25)`$=3.0$, `binom_var(12, 0.25)`$=2.25$, `binom_std(12, 0.25)`$=1.5$.

### P4.  The mgf delivers the moments  *(PSU L9–L10; `~ST-06`)*
For $X\sim\mathrm{Bin}(6,\tfrac12)$ the mgf is $M(t)=(\tfrac12+\tfrac12e^t)^6$.
Show $M(0)=1$; differentiate to get $M'(0)=np=3$; and from
$M''(0)=E[X^2]=np(1-p)+(np)^2$ recover $\mathrm{Var}(X)=M''(0)-M'(0)^2=np(1-p)=1.5$.
*Check:* with `M = lambda t: binom_mgf(t, 6, 0.5)`, `_deriv1(M, 0.0)` $=3.0$,
`_deriv2(M, 0.0)` $=10.5=E[X^2]$, and `_deriv2(M,0.0) - _deriv1(M,0.0)**2` $=1.5=$
`binom_var(6, 0.5)`.

**Solution.** With $p=q=\tfrac12$ and $n=6$, $M(t)=\big(\tfrac12+\tfrac12e^t\big)^6$, so
$M(0)=1^6=1$. Differentiating the power,
$$M'(t)=6\big(\tfrac12+\tfrac12e^t\big)^5\tfrac12e^t\ \Rightarrow\ M'(0)=6\cdot1\cdot\tfrac12=np=3.$$
The second derivative at $0$ gives $M''(0)=np(1-p)+(np)^2=1.5+9=10.5=E[X^2]$, hence
$$\operatorname{Var}(X)=M''(0)-M'(0)^2=10.5-9=1.5=np(1-p).$$
Numerically `_deriv1(M, 0.0)`$=3.0$, `_deriv2(M, 0.0)`$=10.5=E[X^2]$, and
`_deriv2(M,0.0) - _deriv1(M,0.0)**2`$=1.5=$`binom_var(6, 0.5)`.

### P5.  Independent binomials with a common $p$ add  *(PSU L10)*
Let $X_1\sim\mathrm{Bin}(3,0.4)$ and $X_2\sim\mathrm{Bin}(4,0.4)$ be independent.
Using the mgf product $(q+pe^t)^3(q+pe^t)^4=(q+pe^t)^7$, argue $X_1+X_2\sim
\mathrm{Bin}(7,0.4)$, and confirm the pmf-level statement is **Vandermonde's
identity** $\sum_j\binom3j\binom4{5-j}=\binom75$. Why does the argument fail if
$p_1\ne p_2$?
*Check:* `sum_two_binomials_pmf(5, 3, 4, 0.4)` $=0.0774144=$ `binom_pmf(5, 7, 0.4)`;
and the means/variances add: `binom_mean(3,0.4)+binom_mean(4,0.4) == binom_mean(7,0.4)`.

**Solution.** Each binomial mgf is the Bernoulli factor raised to its $n$, so a common $p$
lets the product just add exponents:
$$M_{X_1}(t)M_{X_2}(t)=(q+pe^t)^3(q+pe^t)^4=(q+pe^t)^7,$$
the $\text{Bin}(7,0.4)$ mgf; uniqueness gives $X_1+X_2\sim\text{Bin}(7,0.4)$. Equating the
$k=5$ coefficients is **Vandermonde's identity**
$$\sum_{j}\binom3j\binom4{5-j}=\binom75,$$
the count of ways to split $5$ successes between the two blocks. The argument fails if
$p_1\ne p_2$, since then $(q_1+p_1e^t)^3(q_2+p_2e^t)^4$ shares no common base and is not a
single binomial mgf. Hence `sum_two_binomials_pmf(5, 3, 4, 0.4)`$=0.0774144=$
`binom_pmf(5, 7, 0.4)`, and the means/variances add.

### P6.  The mode and the tie case  *(PSU L10)*
Using the successive-ratio test $\dfrac{P(X=k)}{P(X=k-1)}=\dfrac{n-k+1}{k}\dfrac pq$,
show the pmf rises while $k<(n+1)p$ and find the mode $\lfloor(n+1)p\rfloor$.
(a) For $\mathrm{Bin}(10,0.35)$ compute the mode. (b) For $\mathrm{Bin}(9,\tfrac12)$
note $(n+1)p=5$ is an integer, so $k=4$ and $k=5$ are **both** modes — verify their
pmfs are equal.
*Check:* `binom_mode(10, 0.35)` $=3$; `binom_mode(9, 0.5)` $=5$ with
`binom_pmf(4, 9, 0.5) == binom_pmf(5, 9, 0.5)` $=0.246094$ (the tie).

**Solution.** The successive-ratio test compares neighbours,
$$\frac{P(X=k)}{P(X=k-1)}=\frac{n-k+1}{k}\cdot\frac pq,$$
which exceeds $1$ — the pmf still rising — precisely while $(n-k+1)p>kq$, i.e. $k<(n+1)p$,
and drops below $1$ afterwards, so the peak is $k^\star=\lfloor(n+1)p\rfloor$. (a) For
$\text{Bin}(10,0.35)$, $(n+1)p=11(0.35)=3.85$, giving mode $\lfloor3.85\rfloor=3$. (b) For
$\text{Bin}(9,\tfrac12)$, $(n+1)p=10(\tfrac12)=5$ is an integer, so the ratio equals $1$ at
$k=5$ and $k=4,5$ tie:
$$P(X=4)=P(X=5)=\binom94\big(\tfrac12\big)^9=0.246094.$$
Thus `binom_mode(10, 0.35)`$=3$ and `binom_mode(9, 0.5)`$=5$ (the larger of the tie), with
`binom_pmf(4, 9, 0.5) == binom_pmf(5, 9, 0.5)`$=0.246094$.

### P7.  The Poisson limit — rare events  *(PSU L10 $\to$ `~ST-09`)*
Take $n\to\infty$ with $p=\lambda/n$ fixed at mean $\lambda=2.5$. Using
$\big(1-\tfrac\lambda n\big)^n\to e^{-\lambda}$ and $\tfrac{n!}{(n-k)!\,n^k}\to1$,
show $\binom nk p^kq^{n-k}\to \dfrac{\lambda^k e^{-\lambda}}{k!}$. Evaluate the
$k=3$ term for $n=2500$ and compare to $\mathrm{Poisson}(2.5)$.
*Check:* `binom_pmf(3, 2500, 0.001)` $=0.213881$ vs `_poisson_pmf(3, 2.5)`
$=0.213763$ (difference $\sim10^{-4}$, shrinking like $1/n$).

**Solution.** Substitute $p=\lambda/n$ into the pmf and group the $n$-dependence,
$$\binom nk p^kq^{n-k}=\underbrace{\frac{n!}{(n-k)!\,n^k}}_{\to1}\cdot\frac{\lambda^k}{k!}\cdot
\underbrace{\Big(1-\frac\lambda n\Big)^{n}}_{\to e^{-\lambda}}\Big(1-\frac\lambda n\Big)^{-k}.$$
The first factor $\to1$ (a ratio of $k$ terms each $\to1$), the last $\to1$, and
$(1-\lambda/n)^n\to e^{-\lambda}$, leaving the **Poisson** law $\lambda^k e^{-\lambda}/k!$.
At $\lambda=2.5,k=3,n=2500$ ($p=0.001$) the binomial term is `binom_pmf(3, 2500, 0.001)`
$=0.213881$ versus `_poisson_pmf(3, 2.5)`$=0.213763$ — a gap of $\sim10^{-4}$ that shrinks
like $1/n$.

### P8.  The normal approximation — de Moivre–Laplace  *(PSU L10 $\to$ `~ST-18`)*
For $\mathrm{Bin}(100,\tfrac12)$ (so $np=50$, $npq=25$, $\sigma=5$), use the de
Moivre–Laplace formula $P(X=k)\approx\frac{1}{\sqrt{2\pi npq}}e^{-(k-np)^2/2npq}$
to estimate $P(X=50)$ and compare to the exact binomial value. State the
continuity correction you would use to approximate $P(48\le X\le 52)$.
*Check:* `binom_pmf(50, 100, 0.5)` $=0.079589$ vs `_normal_pdf(50, 50.0, 5.0)`
$=0.079788$ (agreement to $\sim10^{-3}$ at the peak).

**Solution.** With $np=50$, $npq=25$, $\sigma=\sqrt{25}=5$, the de Moivre–Laplace formula at
the peak $k=50$ has zero exponent:
$$P(X=50)\approx\frac{1}{\sqrt{2\pi\,npq}}\,e^{0}=\frac{1}{\sqrt{50\pi}}\approx0.07979,$$
against the exact $0.079589$ (agreeing to $\sim10^{-3}$). For the interval one spreads each
integer over a unit bin — the **continuity correction** — replacing $P(48\le X\le52)$ by the
normal area from $47.5$ to $52.5$:
$$P(48\le X\le52)\approx\Phi\!\Big(\tfrac{52.5-50}{5}\Big)-\Phi\!\Big(\tfrac{47.5-50}{5}\Big)
=\Phi(0.5)-\Phi(-0.5).$$
The peak check is `binom_pmf(50, 100, 0.5)`$=0.079589$ versus `_normal_pdf(50, 50.0, 5.0)`
$=0.079788$.
