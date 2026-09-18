# ST-09 — Problems

Work each by hand, then check with `code/poisson.py`. Citations in `../refs.md`;
**STAT 414 L12** = Penn State Lesson 12, "The Poisson Distribution." Throughout
$X\sim\mathrm{Poisson}(\lambda)$ with pmf $P(X=k)=e^{-\lambda}\lambda^{k}/k!$.

### P1.  The pmf and its recurrence  *(STAT 414 L12.1)*
A call center receives an average of $\lambda=3$ calls per minute, the calls
independent. Write the pmf of the number $X$ of calls in a one-minute window and
evaluate $P(X=0),P(X=1),P(X=2),P(X=3)$ by hand. Verify the recurrence
$P(X{=}k{+}1)=\frac{\lambda}{k+1}P(X{=}k)$ links your four numbers, and note why
$P(X{=}2)=P(X{=}3)$ here (the ratio $\lambda/(k+1)=3/3=1$ at $k=2$).
*Check:* `poisson_pmf(0,3.0)`$=0.049787$, `poisson_pmf(1,3.0)`$=0.149361$,
`poisson_pmf(2,3.0)`$=0.224042$, `poisson_pmf(3,3.0)`$=0.224042$ (equal, as argued).

**Solution.** With $\lambda=3$ the pmf is $P(X=k)=e^{-3}3^{k}/k!$, so the first three values are
$$P(0)=e^{-3}=0.049787,\quad P(1)=3e^{-3}=0.149361,\quad P(2)=\tfrac{9}{2}e^{-3}=0.224042.$$
Each term is the previous one times $\lambda/(k+1)$, the recurrence $P(k{+}1)=\tfrac{\lambda}{k+1}P(k)$: $P(1)=\tfrac31 P(0)$ and $P(2)=\tfrac32 P(1)$. At $k=2$ the multiplier is exactly one,
$$P(3)=\frac{\lambda}{k+1}P(2)=\frac{3}{3}\,P(2)=P(2)=0.224042,$$
so the pmf is flat across its twin modes $k=2,3$. These reproduce `poisson_pmf(0..3, 3.0)` $=0.049787,0.149361,0.224042,0.224042$ with $P(X{=}2)=P(X{=}3)$, as in the Check.

### P2.  "At least one" via the complement  *(STAT 414 L12.1)*
Flaws occur in an optical fiber at rate $\lambda=1.5$ per km. Find the probability
that a 1-km length has **at least one** flaw. Use the complement
$P(X\ge1)=1-P(X=0)=1-e^{-\lambda}$ rather than summing the whole tail — the single
most common Poisson manoeuvre.
*Check:* `poisson_pmf(0,1.5)`$=0.223130$ so $P(X\ge1)=1-0.223130=0.776870$
$=$ `1 - poisson_pmf(0,1.5)`.

**Solution.** "At least one" is the complement of "none," and the empty count has the clean closed form $P(X=0)=e^{-\lambda}$. With $\lambda=1.5$,
$$P(X\ge1)=1-P(X=0)=1-e^{-\lambda}=1-e^{-1.5}=1-0.223130=0.776870.$$
Summing the whole tail $P(1)+P(2)+\cdots$ would give the same number, but the one-term complement is the standard Poisson manoeuvre. This is `1 - poisson_pmf(0,1.5)` $=0.776870$, matching the Check.

### P3.  Cumulative probabilities  *(STAT 414 L12.1)*
Particles strike a detector at $\lambda=4$ per second. Find $P(X\le2)$ and
$P(X\ge3)$ for a one-second count. Sum $P(0)+P(1)+P(2)$ for the first; use
$P(X\ge3)=1-P(X\le2)$ for the second.
*Check:* `poisson_cdf(2,4.0)`$=0.238103$ and `1 - poisson_cdf(2,4.0)`$=0.761897$.

**Solution.** Add the first three terms with $\lambda=4$, factoring out $e^{-4}=0.018316$:
$$P(X\le2)=e^{-4}\Big(1+4+\tfrac{4^{2}}{2}\Big)=13\,e^{-4}=0.238103.$$
The upper tail is then the complement, which avoids an infinite sum,
$$P(X\ge3)=1-P(X\le2)=1-0.238103=0.761897.$$
These are exactly `poisson_cdf(2,4.0)` $=0.238103$ and `1 - poisson_cdf(2,4.0)` $=0.761897$ of the Check.

### P4.  Mean and variance from the mgf  *(STAT 414 L12.2; `~ST-06`)*
Starting from $M(t)=\exp\!\big(\lambda(e^{t}-1)\big)$, show $M'(t)=\lambda e^{t}M(t)$,
hence $E[X]=M'(0)=\lambda$, and $M''(0)=\lambda+\lambda^{2}$, hence
$\mathrm{Var}(X)=M''(0)-M'(0)^{2}=\lambda$. Confirm the universal fact $M(0)=1$.
Take $\lambda=5$.
*Check:* `poisson_mgf(0.0,5.0)`$=1.0$; the central-difference derivatives of
`poisson_mgf` give $M'(0)=5.0=$`poisson_mean(5.0)` and
$M''(0)-M'(0)^2=5.0=$`poisson_var(5.0)` (see `test_mgf_value_and_moment_derivatives`).

**Solution.** Setting $t=0$ in $M(t)=\exp(\lambda(e^{t}-1))$ gives the universal $M(0)=e^{0}=1$. Differentiating with the chain rule on the inner $\lambda(e^t-1)$,
$$M'(t)=\lambda e^{t}M(t)\ \Rightarrow\ M'(0)=\lambda\,M(0)=\lambda=E[X]=5.$$
A second derivative gives $M''(t)=(\lambda e^{t}+\lambda^{2}e^{2t})M(t)$, so $M''(0)=\lambda+\lambda^{2}=E[X^2]$ and
$$\mathrm{Var}(X)=M''(0)-M'(0)^{2}=(\lambda+\lambda^{2})-\lambda^{2}=\lambda=5.$$
Thus `poisson_mgf(0.0,5.0)` $=1.0$, and the central differences give $M'(0)=5.0=$`poisson_mean(5.0)` and $M''(0)-M'(0)^2=5.0=$`poisson_var(5.0)`, as in the Check.

### P5.  Law of rare events: binomial → Poisson  *(STAT 414 L12.1; `~ST-07`)*
A page has $n=100$ characters, each mistyped independently with probability
$p=0.02$. The number of typos is $\mathrm{Bin}(100,0.02)$; approximate it by
$\mathrm{Poisson}(\lambda)$ with $\lambda=np=2$ and compare $P(X=3)$ exactly and
approximately. Explain why the approximation is good (large $n$, small $p$,
moderate $\lambda$).
*Check:* `binomial_pmf(3,100,0.02)`$=0.182276$ vs `poisson_pmf(3,2.0)`$=0.180447$;
the worst-case gap `poisson_limit_of_binomial(100,0.02)`$=2.743\times10^{-3}$, and
it shrinks $\approx10\times$ each time $n$ grows $10\times$ at fixed $\lambda$.

**Solution.** Exactly, the typo count is binomial:
$$P(X=3)=\binom{100}{3}(0.02)^{3}(0.98)^{97}=0.182276.$$
With $\lambda=np=2$ held fixed, the law of rare events replaces it by the Poisson term
$$P(X=3)\approx\frac{e^{-2}2^{3}}{3!}=\frac{8e^{-2}}{6}=0.180447.$$
The two agree to $\sim10^{-3}$ because $n=100$ is large, $p=0.02$ is small, and $\lambda=2$ is moderate; the Le Cam error is $\lesssim np^{2}=\lambda p=0.04$. So `binomial_pmf(3,100,0.02)` $=0.182276$ vs `poisson_pmf(3,2.0)` $=0.180447$, with worst-case gap `poisson_limit_of_binomial(100,0.02)` $=2.743\times10^{-3}$ shrinking $\approx10\times$ per decade in $n$, as in the Check.

### P6.  Merging two Poisson streams  *(STAT 414 L12.2)*
Red cars pass at $\lambda_1=3$ per minute and blue cars at $\lambda_2=4$ per
minute, independently. Show via the mgf that the **total** $X_1+X_2$ is
$\mathrm{Poisson}(\lambda_1+\lambda_2)=\mathrm{Poisson}(7)$, and find the
probability of exactly $4$ cars in a minute. Confirm the pmf-level convolution
$\sum_{j=0}^{4}P(X_1{=}j)P(X_2{=}4{-}j)$ gives the same value (binomial theorem).
*Check:* `sum_of_poissons([3.0,4.0])`$=7.0$;
`poisson_convolution_pmf(4,3.0,4.0)`$=0.091226=$`poisson_pmf(4,7.0)`.

**Solution.** Independence multiplies mgfs, and the Poisson mgf simply adds its $\lambda$ in the exponent:
$$M_{X_1+X_2}(t)=e^{3(e^t-1)}\,e^{4(e^t-1)}=e^{7(e^t-1)},$$
the mgf of $\mathrm{Poisson}(7)$; by uniqueness $X_1+X_2\sim\mathrm{Poisson}(7)$. Hence
$$P(X_1+X_2=4)=\frac{e^{-7}7^{4}}{4!}=0.091226.$$
At the pmf level the convolution $\sum_{j=0}^{4}P(X_1{=}j)P(X_2{=}4{-}j)$ collapses to the same value, since the binomial theorem gives $\sum_{j}\binom{4}{j}3^{j}4^{4-j}=7^{4}$. So `sum_of_poissons([3.0,4.0])` $=7.0$ and `poisson_convolution_pmf(4,3.0,4.0)` $=0.091226=$`poisson_pmf(4,7.0)`, as in the Check.

### P7.  Shape: variance, skewness, kurtosis  *(STAT 414 L12.2)*
For $\lambda=9$ give $\sigma$, the skewness $1/\sqrt{\lambda}$ and the excess
kurtosis $1/\lambda$. Comment on why both shape measures $\to0$ as $\lambda$ grows
and what that says about a normal approximation (`~ST-18`).
*Check:* `poisson_var(9)`$=9.0$, `poisson_std(9)`$=3.0$,
`poisson_skewness(9)`$=0.3333$, `poisson_excess_kurtosis(9)`$=0.1111$; both shape
numbers vanish like $\lambda^{-1/2}$ and $\lambda^{-1}$.

**Solution.** Variance equals the mean, so $\sigma=\sqrt{\lambda}=\sqrt9=3$, and the standardized shape numbers are
$$\text{skewness}=\frac{1}{\sqrt{\lambda}}=\frac{1}{3}=0.3333,\qquad \text{excess kurtosis}=\frac{1}{\lambda}=\frac{1}{9}=0.1111.$$
Both are positive — a Poisson is always right-skewed and leptokurtic — but both vanish as $\lambda\to\infty$, like $\lambda^{-1/2}$ and $\lambda^{-1}$. A large-$\lambda$ Poisson is therefore nearly symmetric and bell-shaped, the content of the normal approximation $(X-\lambda)/\sqrt\lambda\to N(0,1)$ (`~ST-18`). These are `poisson_var(9)` $=9.0$, `poisson_std(9)` $=3.0$, `poisson_skewness(9)` $=0.3333$, and `poisson_excess_kurtosis(9)` $=0.1111$, as in the Check.

### P8.  The Poisson process and the gamma integral  *(STAT 414 L12; `~ST-11`)*
For a unit-rate process, "fewer than $k$ events by time $\lambda$" equals "the
$k$-th arrival is after $\lambda$." Use this to argue the identity
$$\sum_{j=0}^{k-1}\frac{e^{-\lambda}\lambda^{j}}{j!}
=\int_{\lambda}^{\infty}\frac{t^{\,k-1}e^{-t}}{(k-1)!}\,\mathrm{d}t,$$
the survival function of a $\mathrm{Gamma}(k,1)$ arrival time. Verify it
numerically for $\lambda=3,k=4$ (left side $=P(X\le3)$).
*Check:* `poisson_cdf(3,3.0)`$=0.647232$ equals the midpoint integral
$\int_{3}^{\infty}t^{3}e^{-t}/6\,\mathrm{d}t$ to $\sim10^{-4}$ (the continuous
`_integrate` test `test_poisson_process_gamma_integral`).

**Solution.** For a unit-rate process the two events coincide: "fewer than $k$ arrivals by time $\lambda$" is the same event as "the $k$-th arrival $T_k$ falls after $\lambda$," and $T_k\sim\mathrm{Gamma}(k,1)$. Equating the two probabilities,
$$\sum_{j=0}^{k-1}\frac{e^{-\lambda}\lambda^{j}}{j!}=P\big(N(\lambda)\le k-1\big)=P(T_k>\lambda)=\int_{\lambda}^{\infty}\frac{t^{\,k-1}e^{-t}}{(k-1)!}\,\mathrm{d}t,$$
the $\mathrm{Gamma}(k,1)$ survival function. (Integrating the right side by parts $k$ times peels off one Poisson term at a time — an inductive proof.) For $\lambda=3,k=4$ the left side is $P(X\le3)=$ `poisson_cdf(3,3.0)` $=0.647232$, which the midpoint integral $\int_3^\infty t^{3}e^{-t}/6\,\mathrm{d}t$ reproduces to $\sim10^{-4}$, as in the Check.
