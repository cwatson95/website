# ST-18 — Problems

Work each by hand, then check with `code/clt.py`. Citations in `../refs.md`;
**PSU L27** = STAT 414 Lesson 27 *The Central Limit Theorem*, **PSU L28** =
Lesson 28 *Approximations for Discrete Distributions*, **HTZ** = Hogg–Tanis–
Zimmerman Ch. 5. Throughout $\Phi,\varphi$ are the standard-normal cdf/pdf,
$q\equiv1-p$, and a parent law is a pmf array with `probs[k]=P(X=k)`.

### P1.  The CLT made visible: rolling dice  *(PSU L27)*
A fair die $X$ is uniform on $\{1,\dots,6\}$ — flat, nothing like a bell. Let
$S_n=X_1+\dots+X_n$. State the CLT for the standardized sum and explain why
$\max_k|F_{S_n}(k)-\Phi(\tfrac{k+0.5-\mu_n}{\sigma_n})|$ should fall to zero with
$n$, where $\mu_n=3.5n$, $\sigma_n=\sqrt{(35/12)\,n}$. *Check:*
`clt_cdf_max_error(die_pmf(),1)` $=0.05424$ (one die: visibly non-normal), while
`clt_cdf_max_error(die_pmf(),16)` $=0.00163$ and `clt_cdf_max_error(die_pmf(),64)`
$=0.00041$ (the sum is the bell to four places).

**Solution.** With $\mu=3.5$ and $\sigma^2=\tfrac1{6}\sum_{k=1}^6 k^2-3.5^2=\tfrac{91}{6}
-12.25=\tfrac{35}{12}$, the CLT says $Z_n=(S_n-3.5n)/\sqrt{(35/12)n}\to N(0,1)$ in
distribution, i.e. $P(Z_n\le z)\to\Phi(z)$. Equivalently $S_n\approx N(\mu_n,
\sigma_n^2)$, so the standardized cdf of the *exact* convolved law should hug
$\Phi$ ever more tightly. One die is uniform, so its cdf is a staircase far from
$\Phi$ (gap $0.054$); convolving sixteen and then sixty-four copies (`nfold_pmf`)
smooths the staircase into the Gaussian, the gap collapsing to $0.0016$ and
$0.0004$ — the central limit theorem, made quantitative by `clt_cdf_max_error`.

### P2.  Sums add means and variances  *(PSU L27; `~ST-16`)*
For i.i.d. $X_i$ with mean $\mu$ and variance $\sigma^2$, show $E[S_n]=n\mu$ and
$\operatorname{Var}(S_n)=n\sigma^2$ (so $\operatorname{SD}=\sigma\sqrt n$), and that
$\bar X=S_n/n$ has mean $\mu$ and variance $\sigma^2/n$ — the **standard error**.
Why does the pmf of $S_n$ equal the $n$-fold convolution of the parent? *Check:*
for five dice, `nfold_pmf(die_pmf(),5)` sums to $1.0$, with `pmf_mean` $=17.5=5\cdot3.5$
and `pmf_var` $=14.5833=5\cdot\tfrac{35}{12}$; and `convolve_pmf(die_pmf(),die_pmf())`
equals `nfold_pmf(die_pmf(),2)`.

**Solution.** Expectation is linear, so $E[S_n]=\sum_iE[X_i]=n\mu$ unconditionally.
For independents the covariances vanish and variances add,
$\operatorname{Var}(S_n)=\sum_i\operatorname{Var}(X_i)=n\sigma^2$, hence
$\operatorname{SD}(S_n)=\sigma\sqrt n$ and $\operatorname{Var}(\bar X)=
\operatorname{Var}(S_n)/n^2=\sigma^2/n$. The pmf identity is the law of total
probability over the value of $X_1$: $P(S_2=k)=\sum_jP(X_1=j)P(X_2=k-j)=(p*p)[k]$,
and iterating gives the $n$-fold convolution. Numerically the five-die law
normalizes to $1$ and carries mean $17.5$ and variance $14.583$ — exactly $5\mu$
and $5\sigma^2$, the additivity the CLT rescales.

### P3.  Why universality holds: the mgf limit  *(PSU L27; `~ST-06`, `~MA-21`)*
Let $Y_i=(X_i-\mu)/\sigma$, so $E[Y]=0$, $E[Y^2]=1$, and $Z_n=\frac1{\sqrt n}\sum_iY_i$.
Using $M_{Z_n}(t)=[M_Y(t/\sqrt n)]^n$ and the expansion $M_Y(s)=1+\tfrac12 s^2+o(s^2)$,
show $M_{Z_n}(t)\to e^{t^2/2}$, the mgf of $N(0,1)$, and conclude $Z_n\to N(0,1)$ by
uniqueness. Which features of the parent survive the limit? *Check:* the limit
target is the standard normal: `float(standard_normal_cdf(0.0))` $=0.5$,
`float(standard_normal_cdf(1.96))` $=0.975002$, and (continuous check) the integral
of `standard_normal_pdf` up to $1$ equals `float(standard_normal_cdf(1.0))` $=0.841345$.

**Solution.** Independence factorizes the mgf, and the identical scaling gives
$M_{Z_n}(t)=[M_Y(t/\sqrt n)]^n$. With $M_Y(0)=1$, $M_Y'(0)=E[Y]=0$, $M_Y''(0)=E[Y^2]=1$,
Taylor gives $M_Y(s)=1+\tfrac12s^2+o(s^2)$, so
$$M_{Z_n}(t)=\Big[1+\frac{t^2}{2n}+o\!\big(\tfrac1n\big)\Big]^n\xrightarrow{n\to\infty}e^{t^2/2},$$
the `~MA-21` limit $(1+a/n)^n\to e^a$. Since $e^{t^2/2}$ is the mgf of $N(0,1)$
(`~ST-12`), uniqueness gives $Z_n\to N(0,1)$. Only the **first two moments** of the
parent enter (through $E[Y]=0$, $E[Y^2]=1$); all higher structure is $o(1/n)$ and
washes out — that is universality. The code confirms the limit law: $\Phi(0)=\tfrac12$,
$\Phi(1.96)=0.975$, and $\Phi=\int\varphi$.

### P4.  How fast: the Berry–Esseen rate  *(HTZ §5.6; `~MA-21`)*
State the Berry–Esseen bound $\sup_x|F_{S_n}(x)-\Phi(\tfrac{x-n\mu}{\sigma\sqrt n})|
\le C\rho/(\sigma^3\sqrt n)$ with $\rho=E|X-\mu|^3$, and read off the rate. For the
die, compute $\rho$ and verify the bound at $n=1$. *Check:* `pmf_third_abs_moment(die_pmf())`
$=6.375$; `berry_esseen_bound(die_pmf(),1)` $=0.9797$ and `kolmogorov_cdf_error(die_pmf(),1)`
$=0.1434\le0.9797$; the bound at $n=4$ is $0.4899=0.9797/\sqrt4$.

**Solution.** The Berry–Esseen theorem upgrades the CLT to a *uniform* statement
with an explicit $O(n^{-1/2})$ rate: doubling $n$ shrinks the worst-case cdf error
by $1/\sqrt2$, and the constant is universal ($C\le0.7655$). For the die,
$\rho=E|X-3.5|^3=\tfrac1{6}\cdot2\,(2.5^3+1.5^3+0.5^3)=\tfrac1{3}(15.625+3.375+0.125)=6.375$,
$\sigma=\sqrt{35/12}=1.7078$, so the $n=1$ bound is $0.7655\cdot6.375/1.7078^3=0.9797$.
The actual Kolmogorov distance is $0.1434$ — well inside the bound, with the slack
$\Phi$ already absorbing most of the staircase. Because the bound scales as
$1/\sqrt n$, at $n=4$ it is $0.9797/2=0.4899$, matching `berry_esseen_bound`.

### P5.  Normal approximation to the binomial & the continuity correction  *(PSU L28; `~ST-07`)*
For $X\sim\mathrm{Bin}(20,\tfrac12)$ ($\mu=10$, $\sigma=\sqrt5$), approximate
$P(X\le13)$ with and without the continuity correction
$P(X\le k)\approx\Phi(\tfrac{k+0.5-\mu}{\sigma})$, and compare to the exact value.
Why is the correction needed? *Check:* `binom_cdf(13,20,0.5)` $=0.942341$ (exact),
`normal_approx_binomial(13,20,0.5,False)` $=0.910144$ (no correction),
`normal_approx_binomial(13,20,0.5)` $=0.941238$ (corrected).

**Solution.** The binomial is a sum of $20$ Bernoulli$(\tfrac12)$ indicators, so by
de Moivre–Laplace $\mathrm{Bin}(20,\tfrac12)\approx N(10,5)$. Without correction,
$P(X\le13)\approx\Phi(\tfrac{13-10}{\sqrt5})=\Phi(1.342)=0.9101$ — off by $0.032$,
because a smooth normal cdf evaluated at the integer $13$ ignores the probability
mass in the bar *at* $13$. Giving each integer the interval $[k-\tfrac12,k+\tfrac12]$
moves the boundary to $13.5$: $P(X\le13)\approx\Phi(\tfrac{13.5-10}{\sqrt5})=\Phi(1.565)
=0.9412$, matching the exact $0.9423$ to three digits. The half-unit
**continuity correction** is the difference between a one-digit and a three-digit
approximation; over all $k$ it cuts the max cdf error for $\mathrm{Bin}(10,\tfrac12)$
from $0.123$ to $0.0027$.

### P6.  The local limit and interval probabilities  *(PSU L28; HTZ §5.7)*
Two refinements: (a) the **local** de Moivre–Laplace theorem $P(X=k)\approx
\tfrac1\sigma\varphi(\tfrac{k-\mu}\sigma)$ approximates a single bar; (b) an interval
uses $P(a\le X\le b)\approx\Phi(\tfrac{b+0.5-\mu}\sigma)-\Phi(\tfrac{a-0.5-\mu}\sigma)$.
For $\mathrm{Bin}(20,\tfrac12)$ estimate $P(X=10)$ and $P(8\le X\le12)$. *Check:*
`de_moivre_laplace_pmf(10,20,0.5)` $=0.178412$ vs exact `binom_pmf(10,20,0.5)` $=0.176197$;
`normal_approx_binomial_interval(8,12,20,0.5)` $=0.736448$ vs exact $0.736824$
(`binom_cdf(12,20,0.5)-binom_cdf(7,20,0.5)`).

**Solution.** (a) Dividing the continuity-corrected single-bar probability by its
unit width gives the local theorem: the *bars* of the pmf trace the normal density.
At the center, $P(X=10)\approx\tfrac1{\sqrt5}\varphi(0)=\tfrac{0.39894}{2.2361}=0.17841$,
within $0.002$ of the exact $0.17620$, and the local densities sum to $\approx1$
across the support. (b) For an interval both endpoints are widened outward — $b$ up
to $b+\tfrac12$, $a$ down to $a-\tfrac12$ — so $P(8\le X\le12)\approx\Phi(\tfrac{12.5-10}
{\sqrt5})-\Phi(\tfrac{7.5-10}{\sqrt5})=\Phi(1.118)-\Phi(-1.118)=0.7364$, matching the
exact $0.7368$. This is the de Moivre–Laplace Gaussian that `~SM-01` puts on the
two-state multiplicity.

### P7.  Normal approximation to the Poisson & the rule of thumb  *(PSU L28; `~ST-09`)*
Since $\mathrm{Poisson}(\lambda)$ is a sum of $m$ independent
$\mathrm{Poisson}(\lambda/m)$ pieces, the CLT gives $\mathrm{Poisson}(\lambda)\approx
N(\lambda,\lambda)$ as $\lambda\to\infty$. Argue the max cdf error decays like
$1/\sqrt\lambda$, and state the binomial rule of thumb $np\ge5,\ n(1-p)\ge5$.
*Check:* `poisson_approx_max_error(4.0)` $=0.03218$, `poisson_approx_max_error(16.0)`
$=0.01648$, `poisson_approx_max_error(64.0)` $=0.00829$ (each $\times4$ in $\lambda$
halves the error); `normal_approx_applicable(20,0.5)` $=$ `True` but
`normal_approx_applicable(8,0.5)` $=$ `False` ($np=4<5$).

**Solution.** The reproductive property (`~ST-09`) writes $\mathrm{Poisson}(\lambda)$
as a sum of $m$ i.i.d. Poissons, so the CLT applies with $\mu=\operatorname{Var}=
\lambda$, giving $\mathrm{Poisson}(\lambda)\approx N(\lambda,\lambda)$ and
$P(X\le k)\approx\Phi(\tfrac{k+0.5-\lambda}{\sqrt\lambda})$. The Berry–Esseen rate
is $\propto1/\sqrt\lambda$ (the "sample size" is $\lambda$), so quadrupling $\lambda$
halves the worst-case error: $0.0322\to0.0165\to0.0083$ at $\lambda=4,16,64$. For
the binomial the same logic demands the mean sit several $\sigma=\sqrt{npq}$ from
both boundaries $0$ and $n$; the usual threshold is $np\ge5$ **and** $n(1-p)\ge5$.
$\mathrm{Bin}(20,\tfrac12)$ passes ($np=n q=10$); $\mathrm{Bin}(8,\tfrac12)$ fails
($np=4$), too few trials for the bell to fit — exactly what `normal_approx_applicable`
reports.
