# ST-10 — Problems

Work each by hand, then check with `code/continuous_rv.py`. Citations in
`../refs.md`; **PSU** = STAT 414 Lessons 13–14. Throughout, $f$ is a pdf, $F$ its
cdf, and every probability is an **area** $\int f$ — the continuous version of the
sums in `~ST-05`.

### P1.  Find a normalizing constant; then mean and variance  *(PSU L14.1, L14.3)*
Let $f(x)=c\,x^2$ on $[0,3]$ (and $0$ elsewhere). Use $\int_0^3 f=1$ to find $c$,
then compute $E[X]$ and $\operatorname{Var}[X]$.
Solution: $\int_0^3 c x^2\,dx=c\cdot\tfrac{27}{3}=9c=1\Rightarrow c=\tfrac19$. Then
$E[X]=\tfrac19\int_0^3 x^3\,dx=\tfrac19\cdot\tfrac{81}{4}=\tfrac94=2.25$, and
$E[X^2]=\tfrac19\int_0^3 x^4\,dx=\tfrac19\cdot\tfrac{243}{5}=\tfrac{27}{5}=5.4$, so
$\operatorname{Var}[X]=5.4-2.25^2=0.3375$.
*Check:* with `f = lambda x: x*x/9`, `pdf_is_normalized(f, 0, 3)` $=$ `True`;
`expectation_continuous(f, 0, 3)` $=2.25$; `variance_continuous(f, 0, 3)` $=0.3375$.

**Solution.** Normalization fixes $c$: $\int_0^3 cx^2\,dx=c\,[x^3/3]_0^3=9c=1$, so $c=\tfrac19$. The moments are then power-rule integrals,
$$E[X]=\frac19\int_0^3 x^3\,dx=\frac19\cdot\frac{3^4}{4}=\frac94=2.25,\qquad E[X^2]=\frac19\int_0^3 x^4\,dx=\frac19\cdot\frac{3^5}{5}=\frac{27}{5}=5.4,$$
and the shortcut gives $\operatorname{Var}[X]=E[X^2]-(E[X])^2=5.4-2.25^2=0.3375$. These match `pdf_is_normalized(f, 0, 3)` $=$ `True`, `expectation_continuous(f, 0, 3)` $=2.25$, and `variance_continuous(f, 0, 3)` $=0.3375$ of the Check.

### P2.  The cdf as accumulated area, and an interval probability  *(PSU L14.2)*
For the uniform $U(2,8)$ ($f=\tfrac16$ on $[2,8]$), find $F(5)$ and
$P(3<X<5)$ two ways: as $\int f$ and as a difference of the cdf.
Solution: $F(5)=\int_2^5\tfrac16\,dx=\tfrac{5-2}{6}=\tfrac12$; and
$P(3<X<5)=F(5)-F(3)=\tfrac12-\tfrac16=\tfrac13$.
*Check:* with `U = lambda x: uniform_pdf(x,2,8)`, `cdf_from_pdf(U, 5, 2)` $=0.5$ and
`prob_between(U, 3, 5)` $=0.3333\ldots=$ `uniform_cdf(5,2,8)-uniform_cdf(3,2,8)`.

**Solution.** On $U(2,8)$ the density is the constant $\tfrac1{b-a}=\tfrac16$, so the cdf is the accumulated area $F(x)=\tfrac{x-2}{6}$:
$$F(5)=\int_2^5\tfrac16\,dx=\frac{5-2}{6}=\frac12.$$
The interval probability is that same area, read either directly or as a difference of the cdf,
$$P(3<X<5)=\int_3^5\tfrac16\,dx=F(5)-F(3)=\tfrac12-\tfrac16=\tfrac13.$$
Hence `cdf_from_pdf(U, 5, 2)` $=0.5$ and `prob_between(U, 3, 5)` $=0.3333\ldots=$ `uniform_cdf(5,2,8)-uniform_cdf(3,2,8)`, as in the Check.

### P3.  A single point has probability zero  *(PSU L14.2)*
For the triangular density $f(x)=2x$ on $[0,1]$ (cdf $F(x)=x^2$), show
$P(X=\tfrac12)=0$ and that the endpoints are irrelevant, then evaluate
$P(0.3<X<0.7)$.
Solution: $P(X=\tfrac12)=F(\tfrac12)-F(\tfrac12)=0$, so
$P(0.3<X<0.7)=P(0.3\le X\le 0.7)=F(0.7)-F(0.3)=0.49-0.09=0.40$.
*Check:* with `g = lambda x: 2*x`, `prob_between(g, 0.5, 0.5)` $=0.0$ and
`prob_between(g, 0.3, 0.7)` $=0.40$.

**Solution.** A single point carries no area: with $F(x)=x^2$,
$$P(X=\tfrac12)=F(\tfrac12)-F(\tfrac12)=0,$$
so for a continuous variable open and closed intervals have equal probability — the endpoints are "free." Therefore
$$P(0.3<X<0.7)=F(0.7)-F(0.3)=0.7^2-0.3^2=0.49-0.09=0.40.$$
This matches `prob_between(g, 0.5, 0.5)` $=0.0$ and `prob_between(g, 0.3, 0.7)` $=0.40$ of the Check.

### P4.  Mean and variance of a triangular density  *(PSU L14.3)*
For $f(x)=2x$ on $[0,1]$ compute $E[X]$ and $\operatorname{Var}[X]$.
Solution: $E[X]=\int_0^1 x\cdot2x\,dx=\tfrac23$;
$E[X^2]=\int_0^1 x^2\cdot2x\,dx=\tfrac12$; hence
$\operatorname{Var}[X]=\tfrac12-\big(\tfrac23\big)^2=\tfrac12-\tfrac49=\tfrac1{18}\approx0.05556$.
*Check:* `expectation_continuous(g, 0, 1)` $=0.6667$ and
`variance_continuous(g, 0, 1)` $=0.05556\ (=1/18)$.

**Solution.** For $f(x)=2x$ on $[0,1]$ the first two moments are
$$E[X]=\int_0^1 x\,(2x)\,dx=\Big[\tfrac{2x^3}{3}\Big]_0^1=\frac23,\qquad E[X^2]=\int_0^1 x^2(2x)\,dx=\Big[\tfrac{x^4}{2}\Big]_0^1=\frac12.$$
The variance shortcut then gives
$$\operatorname{Var}[X]=E[X^2]-(E[X])^2=\frac12-\Big(\frac23\Big)^2=\frac12-\frac49=\frac1{18}\approx0.05556.$$
These are `expectation_continuous(g, 0, 1)` $=0.6667$ and `variance_continuous(g, 0, 1)` $=0.05556\ (=1/18)$ of the Check.

### P5.  Percentiles by inverting the cdf  *(PSU L13, L14.4)*
For $F(x)=x^2$ on $[0,1]$ find the median and the 25th percentile.
Solution: solve $F(\pi_p)=p$, i.e. $\pi_p^2=p$, so $\pi_p=\sqrt p$. The median is
$\pi_{0.5}=\sqrt{0.5}\approx0.7071$ and the lower quartile is
$\pi_{0.25}=\sqrt{0.25}=0.5$.
*Check:* with `G = lambda x: x*x`, `quantile(G, 0.5, 0, 1)` $=0.7071$ and
`quantile(G, 0.25, 0, 1)` $=0.5$.

**Solution.** The $p$-th quantile inverts the cdf, $F(\pi_p)=p$. With $F(x)=x^2$ on $[0,1]$ this reads $\pi_p^2=p$, so
$$\pi_p=\sqrt{p}.$$
The median is $\pi_{0.5}=\sqrt{0.5}\approx0.7071$ and the lower quartile is $\pi_{0.25}=\sqrt{0.25}=0.5$. Bisection confirms `quantile(G, 0.5, 0, 1)` $=0.7071$ and `quantile(G, 0.25, 0, 1)` $=0.5$, as in the Check.

### P6.  The uniform $U(a,b)$ end to end  *(PSU L14.6)*
For $U(2,8)$ verify mean $\tfrac{a+b}2$, variance $\tfrac{(b-a)^2}{12}$, and find
the 90th percentile.
Solution: mean $=\tfrac{2+8}{2}=5$; variance $=\tfrac{(8-2)^2}{12}=\tfrac{36}{12}=3$;
percentile $\pi_p=a+p(b-a)$ gives $\pi_{0.9}=2+0.9\cdot6=7.4$.
*Check:* `uniform_mean(2,8)` $=5.0$, `uniform_var(2,8)` $=3.0$,
`uniform_quantile(0.9, 2, 8)` $=7.4$, and bisection agrees:
`quantile(lambda x: uniform_cdf(x,2,8), 0.9, 2, 8)` $=7.4$.

**Solution.** For $U(a,b)=U(2,8)$ the symmetric density puts the mean at the midpoint and gives the standard spread,
$$E[X]=\frac{a+b}{2}=\frac{2+8}{2}=5,\qquad \operatorname{Var}[X]=\frac{(b-a)^2}{12}=\frac{36}{12}=3.$$
Inverting the linear cdf $F(x)=\tfrac{x-a}{b-a}$ gives the percentile $\pi_p=a+p(b-a)$, so
$$\pi_{0.9}=2+0.9(6)=7.4.$$
These are `uniform_mean(2,8)` $=5.0$, `uniform_var(2,8)` $=3.0$, and `uniform_quantile(0.9, 2, 8)` $=7.4$, with bisection agreeing, as in the Check.

### P7.  A point mass as a Dirac delta  *(PSU L14.1; `~MA-15`, `~ST-05`)*
Smear a unit point mass at $c=4$ over $[c-\varepsilon,c+\varepsilon]$ with the box
density $f_\varepsilon=\tfrac1{2\varepsilon}$. Show $E[X]=c$ for all $\varepsilon$
and $\operatorname{Var}[X]=\tfrac{\varepsilon^2}{3}\to0$ as $\varepsilon\to0$ — the
density collapses to $\delta(x-4)$ (`~MA-15`), recovering a discrete point mass
(`~ST-05`).
Solution: by symmetry $E[X]=c=4$; and
$\operatorname{Var}[X]=\tfrac1{2\varepsilon}\int_{-\varepsilon}^{\varepsilon}u^2\,du
=\tfrac1{2\varepsilon}\cdot\tfrac{2\varepsilon^3}{3}=\tfrac{\varepsilon^2}{3}$. At
$\varepsilon=0.1$ this is $0.00333\overline{3}$.
*Check:* with `pm = lambda x: point_mass_pdf(x, 4, 0.1)`,
`expectation_continuous(pm, 3.9, 4.1)` $=4.0$ and
`variance_continuous(pm, 3.9, 4.1)` $=0.003333\ (=0.1^2/3)$.

**Solution.** The box density $f_\varepsilon=\tfrac1{2\varepsilon}$ on $[c-\varepsilon,c+\varepsilon]$ is symmetric about $c$, so $E[X]=c=4$ for every $\varepsilon$. Centering with $u=x-c$,
$$\operatorname{Var}[X]=\frac1{2\varepsilon}\int_{-\varepsilon}^{\varepsilon}u^2\,du=\frac1{2\varepsilon}\cdot\frac{2\varepsilon^3}{3}=\frac{\varepsilon^2}{3}\xrightarrow[\varepsilon\to0]{}0,$$
so the density collapses to the spike $\delta(x-4)$ (`~MA-15`), recovering a discrete point mass (`~ST-05`). At $\varepsilon=0.1$ the variance is $0.1^2/3=0.0033\overline{3}$, matching `expectation_continuous(pm, 3.9, 4.1)` $=4.0$ and `variance_continuous(pm, 3.9, 4.1)` $=0.003333\ (=0.1^2/3)$ of the Check.
