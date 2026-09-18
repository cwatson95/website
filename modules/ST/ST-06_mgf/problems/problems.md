# ST-06 — Problems

Work each by hand, then check with `code/mgf.py`. Citations in `../refs.md`;
**PSU L9** = Penn State STAT 414 Lesson 9. The mgf is $M(t)=E[e^{tX}]$, defined on
an open interval about $t=0$; throughout, `mean`/`variance` denote the direct
`~ST-05` definitions used as ground truth.

### P1.  The mgf passes through 1, and its slope is the mean  *(PSU L9.1–9.2)*
From $M(t)=\sum_x e^{tx}p(x)$ show $M(0)=\sum_x p(x)=1$ for any distribution. Then
expand $e^{tX}=\sum_k(tX)^k/k!$ inside the expectation to get
$M(t)=\sum_k E[X^k]\,t^k/k!$, and conclude $M'(0)=E[X]=\mu$ and, in general,
$M^{(k)}(0)=E[X^k]$. *Check:* `mgf(0.0, *binomial_dist(10,0.3))` $=1.0$ and
`mean_from_mgf(*binomial_dist(10,0.3))` $\approx 3.0$ ($=np$).

**Solution.** At $t=0$ the exponential collapses, $e^{0\cdot x}=1$, so
$$M(0)=\sum_x e^{0}p(x)=\sum_x p(x)=1$$
for any distribution. Expanding $e^{tX}=\sum_{k\ge0}(tX)^k/k!$ and exchanging the sum
with the expectation (valid on the convergence interval),
$$M(t)=\sum_{k=0}^{\infty}\frac{t^k}{k!}E[X^k],$$
the exponential generating function of the raw moments. The coefficient of $t^k$ is
$E[X^k]/k!$, so differentiating $k$ times at $0$ peels them off: $M^{(k)}(0)=E[X^k]$, in
particular $M'(0)=E[X]=\mu$. For $\text{Bin}(10,0.3)$ this gives
`mgf(0.0, *binomial_dist(10,0.3))`$=1.0$ and `mean_from_mgf(...)`$\approx3.0=np$.

### P2.  Binomial mean and variance straight from the mgf  *(PSU L9.2; `~ST-07`)*
For $X\sim\text{Bin}(n,p)$ the mgf is $M(t)=\big((1-p)+pe^t\big)^n$ (a product of
$n$ Bernoulli mgfs). Differentiate: $M'(t)=n((1-p)+pe^t)^{n-1}pe^t$ so $M'(0)=np$;
compute $M''(0)=n(n-1)p^2+np$ and hence
$$\sigma^2=M''(0)-[M'(0)]^2=np-np^2=np(1-p).$$
*Check:* with `d = binomial_dist(10,0.3)`, `mean_from_mgf(*d)` $\approx 3.0$ and
`var_from_mgf(*d)` $\approx 2.1=np(1-p)$ (both agree with `mean(*d)`, `variance(*d)`).

**Solution.** Write $u(t)=(1-p)+pe^t$, so $M(t)=u^n$ with $u'(t)=pe^t$ and $u(0)=1$. Then
$$M'(t)=n\,u^{n-1}pe^t\ \Rightarrow\ M'(0)=n\cdot1\cdot p=np=\mu.$$
Differentiating again by the product rule,
$$M''(t)=n(n-1)u^{n-2}(pe^t)^2+n\,u^{n-1}pe^t\ \Rightarrow\ M''(0)=n(n-1)p^2+np=E[X^2].$$
Hence $\sigma^2=M''(0)-[M'(0)]^2=n(n-1)p^2+np-(np)^2=np-np^2=np(1-p)$. With $n=10,p=0.3$:
`mean_from_mgf(*d)`$\approx3.0$ and `var_from_mgf(*d)`$\approx2.1=np(1-p)$.

### P3.  Poisson: all cumulants equal $\lambda$, and the third moment  *(PSU L9; §8)*
For $X\sim\text{Poi}(\lambda)$, $M(t)=e^{\lambda(e^t-1)}$, so the cumulant
generator is $K(t)=\ln M(t)=\lambda(e^t-1)$. Show $K^{(k)}(0)=\lambda$ for **every**
$k\ge1$, so mean $=$ variance $=\lambda$ and indeed all cumulants equal $\lambda$.
Using $m_k=\sum$(cumulant compositions), derive the third raw moment
$E[X^3]=\lambda^3+3\lambda^2+\lambda$. *Check:* with `dp = poisson_dist(2.0)`,
`[cumulant_from_mgf(k,*dp) for k in (1,2,3)]` $\approx[2,2,2]$ and
`moment_from_mgf(3,*dp)` $\approx 22.0=2^3+3\cdot2^2+2$.

**Solution.** The cumulant generator is $K(t)=\ln M(t)=\lambda(e^t-1)$. Since
$\tfrac{d}{dt}(e^t-1)=e^t$ and every further derivative is again $e^t$,
$$K^{(k)}(t)=\lambda e^t\ \Rightarrow\ \kappa_k=K^{(k)}(0)=\lambda\quad(k\ge1),$$
so mean $=\kappa_1=\lambda$, variance $=\kappa_2=\lambda$, and indeed *all* cumulants equal
$\lambda$. Converting cumulants to the third raw moment via
$m_3=\kappa_3+3\kappa_2\kappa_1+\kappa_1^3$,
$$E[X^3]=\lambda+3\lambda\cdot\lambda+\lambda^3=\lambda^3+3\lambda^2+\lambda.$$
At $\lambda=2$: `[cumulant_from_mgf(k,*dp) for k in (1,2,3)]`$\approx[2,2,2]$ and
`moment_from_mgf(3,*dp)`$\approx22.0=2^3+3\cdot2^2+2$.

### P4.  The product rule: a sum of independents  *(PSU L9.3; `~MA-10`)*
For independent $X,Y$ prove $M_{X+Y}(t)=M_X(t)M_Y(t)$ by factoring the expectation
of $e^{tX}e^{tY}$. Apply it to two independent $\text{Bernoulli}(0.4)$ variables:
their sum has mgf $\big(0.6+0.4e^t\big)^2$, the $\text{Bin}(2,0.4)$ mgf. Confirm the
distribution of the sum (the **convolution** $[0.36,0.48,0.16]$ on $\{0,1,2\}$)
carries that same mgf. *Check:* at $t=0.5$, with `b = bernoulli_dist(0.4)`,
`mgf_of_sum(0.5,[b,b])`, `binomial_mgf(0.5,2,0.4)`, and
`mgf(0.5, *convolve_dists(b,b))` are **all** $\approx 1.5863113$.

**Solution.** Independence makes $e^{tX}$ and $e^{tY}$ independent, so the expectation of
their product factors:
$$M_{X+Y}(t)=E[e^{t(X+Y)}]=E[e^{tX}]\,E[e^{tY}]=M_X(t)M_Y(t).$$
Two independent $\text{Bernoulli}(0.4)$ each have mgf $0.6+0.4e^t$, so the sum carries
$\big(0.6+0.4e^t\big)^2$ — the $\text{Bin}(2,0.4)$ mgf. Its actual distribution is the
convolution
$$P(0)=0.6^2=0.36,\quad P(1)=2(0.6)(0.4)=0.48,\quad P(2)=0.4^2=0.16,$$
whose mgf must coincide. At $t=0.5$ all three routes agree: `mgf_of_sum(0.5,[b,b])`,
`binomial_mgf(0.5,2,0.4)`, and `mgf(0.5, *convolve_dists(b,b))` are all $\approx1.5863113$.

### P5.  Geometric waiting time: mean $1/p$, variance $(1-p)/p^2$  *(PSU L9; `~ST-08`)*
Let $X$ be the trial of the first success, $\text{Geom}(p)$ on $\{1,2,\dots\}$.
Sum the geometric series to get $M(t)=\dfrac{pe^t}{1-(1-p)e^t}$ for
$t<-\ln(1-p)$. Differentiate at $0$ to obtain $\mu=1/p$ and
$\sigma^2=(1-p)/p^2$. *Check:* with `g = geometric_dist(0.25)`,
`mean_from_mgf(*g)` $\approx 4.0=1/p$ and `var_from_mgf(*g)` $\approx 12.0
=(1-0.25)/0.25^2$.

**Solution.** Summing the geometric series in $e^t$ (with $q=1-p$),
$$M(t)=\sum_{x\ge1}e^{tx}q^{x-1}p=pe^t\sum_{x\ge1}(qe^t)^{x-1}=\frac{pe^t}{1-qe^t},
\qquad t<-\ln q.$$
At $t=0$ both $pe^t$ and $1-qe^t$ equal $p$, so the quotient rule gives
$$M'(0)=\frac{p\cdot p-p\cdot(-q)}{p^2}=\frac{p+q}{p}=\frac1p=\mu,$$
and a second derivative yields $M''(0)=(2-p)/p^2$, whence
$\sigma^2=M''(0)-M'(0)^2=\tfrac{2-p}{p^2}-\tfrac1{p^2}=\tfrac{1-p}{p^2}$. At $p=0.25$:
`mean_from_mgf(*g)`$\approx4.0=1/p$ and `var_from_mgf(*g)`$\approx12.0=(1-0.25)/0.25^2$.

### P6.  Normals add; linear transforms shift and scale  *(PSU L9; §4–§6)*
Using $M_N(t)=e^{\mu t+\frac12\sigma^2t^2}$, show that for independent
$N(\mu_1,\sigma_1^2)$ and $N(\mu_2,\sigma_2^2)$ the product of mgfs is again a
normal mgf with mean $\mu_1+\mu_2$ and variance $\sigma_1^2+\sigma_2^2$ — so by
**uniqueness** the sum is normal. Separately verify the rule $M_{aX+b}(t)=e^{bt}M_X(at)$.
*Check:* at $t=0.3$, `normal_mgf(0.3,1,2)*normal_mgf(0.3,-0.5,1.5)` equals
`normal_mgf(0.3,0.5,math.sqrt(2**2+1.5**2))` ($\approx 1.5391803$); and with
`d = binomial_dist(6,0.5)`, `v,p=d`, `mgf(0.3, 2*v+3, p)` equals
`math.exp(3*0.3)*mgf(0.6,*d)` ($\approx 19.41497$).

**Solution.** Multiply the two normal mgfs and collect exponents:
$$M_1(t)M_2(t)=e^{\mu_1 t+\frac12\sigma_1^2t^2}\,e^{\mu_2 t+\frac12\sigma_2^2t^2}
=e^{(\mu_1+\mu_2)t+\frac12(\sigma_1^2+\sigma_2^2)t^2},$$
again a normal mgf with mean $\mu_1+\mu_2$ and variance $\sigma_1^2+\sigma_2^2$; by
**uniqueness** the sum is $N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$. The transform rule follows
by pulling the constant out of the exponential,
$$M_{aX+b}(t)=E[e^{t(aX+b)}]=e^{bt}E[e^{(at)X}]=e^{bt}M_X(at).$$
Since $N(1,2^2)+N(-0.5,1.5^2)$ has std $\sqrt{2^2+1.5^2}=2.5$,
`normal_mgf(0.3,1,2)*normal_mgf(0.3,-0.5,1.5)`$=$`normal_mgf(0.3,0.5,2.5)`$\approx1.5391803$;
and with $a=2,b=3$, `mgf(0.3, 2*v+3, p)`$=e^{0.9}\cdot$`mgf(0.6,*d)`$\approx19.41497$.

### P7.  The continuous mgf is a Laplace transform  *(PSU L9.1; `~MA-10`, `~ST-11`)*
For $X\sim\text{Exp}(\lambda)$ with $f(x)=\lambda e^{-\lambda x}$ ($x\ge0$),
evaluate $M(t)=\int_0^\infty e^{tx}\lambda e^{-\lambda x}dx=\dfrac{\lambda}{\lambda-t}$
for $t<\lambda$, and read off $\mu=M'(0)=1/\lambda$, $\sigma^2=1/\lambda^2$. Note
$M(t)=\mathcal{L}\{f\}(-t)$: the mgf *is* the (two-sided) Laplace transform of the
density at $s=-t$ (`~MA-10`). *Check:* `mgf_continuous(0.5, lambda x:1.5*math.exp(-1.5*x), 0.0, 80.0)`
$\approx 1.5=$ `exponential_mgf(0.5,1.5)`; differentiating the closed form gives
mean $\approx 0.6667=1/1.5$.

**Solution.** The integrand decays for $t<\lambda$ because $e^{tx}e^{-\lambda x}=e^{-(\lambda-t)x}$:
$$M(t)=\int_0^\infty e^{tx}\lambda e^{-\lambda x}\,dx=\lambda\int_0^\infty e^{-(\lambda-t)x}\,dx
=\frac{\lambda}{\lambda-t},\qquad t<\lambda.$$
Differentiating, $M'(t)=\lambda/(\lambda-t)^2$ and $M''(t)=2\lambda/(\lambda-t)^3$, so
$\mu=M'(0)=1/\lambda$ and $\sigma^2=M''(0)-\mu^2=2/\lambda^2-1/\lambda^2=1/\lambda^2$. Because
$$M(t)=\int e^{tx}f(x)\,dx=\mathcal L\{f\}(-t),$$
the mgf *is* the two-sided Laplace transform of the density read at $s=-t$. For
$\lambda=1.5,t=0.5$: `mgf_continuous(...)`$\approx1.5=$`exponential_mgf(0.5,1.5)`, and the
closed form gives mean $\approx0.6667=1/1.5$.

### P8.  Gamma as a sum of exponentials  *(PSU L9.3; §6–§7; `~ST-11`)*
Show that a sum of $\alpha$ independent $\text{Exp}(\lambda)$ variables has mgf
$\big(\lambda/(\lambda-t)\big)^{\alpha}$, the $\text{Gamma}(\alpha,\lambda)$ mgf, so
by uniqueness the sum is $\text{Gamma}(\alpha,\lambda)$ (the Erlang law). Hence its
mean is $\alpha/\lambda$ and variance $\alpha/\lambda^2$ — $\alpha$ times the
exponential's, as additivity demands. *Check:* `gamma_mgf(0.7,4,1.5)` equals
`exponential_mgf(0.7,1.5)**4` ($\approx 12.359619$).

**Solution.** Each $\text{Exp}(\lambda)$ summand has mgf $\lambda/(\lambda-t)$ (P7), and the
mgf of an independent sum is the product, so for $\alpha$ identical terms
$$M_{X_1+\cdots+X_\alpha}(t)=\prod_{i=1}^{\alpha}\frac{\lambda}{\lambda-t}
=\Big(\frac{\lambda}{\lambda-t}\Big)^{\alpha},$$
exactly the $\text{Gamma}(\alpha,\lambda)$ mgf; by **uniqueness** the sum is
$\text{Gamma}(\alpha,\lambda)$ (the Erlang law for integer $\alpha$). Since cumulants add
over independent sums, the mean and variance are $\alpha$ times the exponential's,
$$\mu=\frac{\alpha}{\lambda},\qquad \sigma^2=\frac{\alpha}{\lambda^2}.$$
With $\alpha=4,\lambda=1.5,t=0.7$ this gives `gamma_mgf(0.7,4,1.5)`$=$
`exponential_mgf(0.7,1.5)**4`$\approx12.359619$.
