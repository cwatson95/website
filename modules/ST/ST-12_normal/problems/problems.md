# ST-12 — Problems

Work each by hand, then check with `code/normal.py`. Citations in `../refs.md`;
**PSU L16** = Penn State STAT 414 Lesson 16 *Normal Distributions*, **HTZ** =
Hogg–Tanis–Zimmerman Ch. 5. Throughout, $\Phi$ is the standard-normal cdf and
$Z=(X-\mu)/\sigma$ the standard score.

### P1.  The Gaussian integral and the peak height  *(PSU L16.1)*
Square $I=\int_{-\infty}^\infty e^{-x^2/2}dx$ and pass to polar coordinates to show
$I^2=2\pi$, hence $I=\sqrt{2\pi}$. Conclude that $f(x)=\frac{1}{\sigma\sqrt{2\pi}}
e^{-(x-\mu)^2/2\sigma^2}$ integrates to one, and that the **peak** of the standard
normal is $f(0)=1/\sqrt{2\pi}$. *Check:* `gaussian_integral_check()` $=2.5066283$
$=$ `SQRT_2PI`; `float(standard_normal_pdf(0.0))` $=0.39894228=1/\sqrt{2\pi}$.

**Solution.** Square the integral and pass to polar coordinates:
$$I^2=\int_{-\infty}^\infty\!\!\int_{-\infty}^\infty e^{-(x^2+y^2)/2}\,dx\,dy=\int_0^{2\pi}\!\!\int_0^\infty e^{-r^2/2}\,r\,dr\,d\theta=2\pi\big[-e^{-r^2/2}\big]_0^\infty=2\pi,$$
so $I=\sqrt{2\pi}$. Dividing the bell by $\sigma I$ makes $\int f=1$, and at the peak $x=\mu$ the exponential is $1$, giving the standard-normal height $f(0)=1/\sqrt{2\pi}=0.39894228$. These are `gaussian_integral_check()` $=2.5066283=$ `SQRT_2PI` and `float(standard_normal_pdf(0.0))` $=0.39894228$ of the Check.

### P2.  Standardizing a normal score  *(PSU L16.2)*
Heights are $X\sim N(\mu=3,\sigma=2)$ (in some units). Find the $Z$-score of
$x=5$ and verify the density factorizes as $f_X(5)=\varphi(z)/\sigma$. Why does
this reduce *every* normal probability to a question about $N(0,1)$? *Check:*
`standardize(5, 3, 2)` $=1.0$; `float(normal_pdf(5,3,2))` equals
`float(standard_normal_pdf(1.0))/2`.

**Solution.** The $Z$-score of $x=5$ in $N(3,2^2)$ is
$$z=\frac{x-\mu}{\sigma}=\frac{5-3}{2}=1.0.$$
Substituting $x=\mu+\sigma z$ into the density (with $dx=\sigma\,dz$) shows $f_X(x)=\tfrac1\sigma\varphi(z)$, so $f_X(5)=\varphi(1)/2$. Because the standardization is a fixed affine map, every probability $P(a<X<b)=P\!\big(\tfrac{a-\mu}{\sigma}<Z<\tfrac{b-\mu}{\sigma}\big)$ becomes a statement about the single $N(0,1)$ — one table serves all normals. Numerically `standardize(5, 3, 2)` $=1.0$ and `float(normal_pdf(5,3,2))` equals `float(standard_normal_pdf(1.0))/2`, as in the Check.

### P3.  Mean and variance are the parameters  *(PSU L16.1; HTZ §5.4)*
Show $E[X]=\mu$ by writing $x=(x-\mu)+\mu$ (the first piece integrates to zero by
oddness), and $\operatorname{Var}[X]=\sigma^2$ by the substitution
$u=(x-\mu)/\sigma$ and $\int u^2e^{-u^2/2}du=\sqrt{2\pi}$. So $N(\mu,\sigma^2)$ is
named by its own mean and variance. *Check:* for $N(3,2^2)$,
`normal_mean_by_integration(3,2)` $=3.000000$ and
`normal_variance_by_integration(3,2)` $=4.000000$.

**Solution.** Split $x=(x-\mu)+\mu$ in $E[X]=\int x f\,dx$. The first piece is odd in $(x-\mu)$ against the even density and integrates to zero; the second is $\mu\int f=\mu$, so $E[X]=\mu$. For the variance substitute $u=(x-\mu)/\sigma$:
$$\operatorname{Var}[X]=\int(x-\mu)^2 f(x)\,dx=\frac{\sigma^2}{\sqrt{2\pi}}\int_{-\infty}^\infty u^2 e^{-u^2/2}\,du=\frac{\sigma^2}{\sqrt{2\pi}}\cdot\sqrt{2\pi}=\sigma^2,$$
where $\int u^2 e^{-u^2/2}\,du=\sqrt{2\pi}$ (integrate by parts, $u\cdot ue^{-u^2/2}$). So the parameters $(\mu,\sigma^2)$ are literally the mean and variance, confirmed by `normal_mean_by_integration(3,2)` $=3.000000$ and `normal_variance_by_integration(3,2)` $=4.000000$ of the Check.

### P4.  Reading moments off the mgf  *(PSU L16.1; `~ST-06`)*
Complete the square to derive $M(t)=E[e^{tX}]=\exp(\mu t+\tfrac12\sigma^2 t^2)$.
Differentiate at $t=0$ to get $M'(0)=\mu$ and $M''(0)=\mu^2+\sigma^2$, and confirm
$\operatorname{Var}=M''(0)-M'(0)^2=\sigma^2$. Then show $aX+b\sim
N(a\mu+b,a^2\sigma^2)$ from $e^{bt}M(at)$. *Check:* for $N(3,2^2)$,
`normal_mgf(0,3,2)` $=1.0$, `mgf_moment(1,3,2)` $\approx3.0$, and `mgf_moment(2,3,2)`
$\approx13.0=\mu^2+\sigma^2$.

**Solution.** Complete the square in the exponent of $M(t)=\int e^{tx}f(x)\,dx$:
$$tx-\frac{(x-\mu)^2}{2\sigma^2}=-\frac{\big(x-(\mu+\sigma^2 t)\big)^2}{2\sigma^2}+\mu t+\tfrac12\sigma^2 t^2,$$
and the remaining Gaussian integrates to $1$, leaving $M(t)=\exp(\mu t+\tfrac12\sigma^2 t^2)$. Then $M'(t)=(\mu+\sigma^2 t)M(t)$ gives $M'(0)=\mu$ and $M''(0)=\mu^2+\sigma^2$, so $\operatorname{Var}=M''(0)-M'(0)^2=\sigma^2$. Finally
$$e^{bt}M(at)=\exp\!\big((a\mu+b)t+\tfrac12(a^2\sigma^2)t^2\big),$$
the mgf of $N(a\mu+b,\,a^2\sigma^2)$, so $aX+b$ is normal. For $N(3,2^2)$: `normal_mgf(0,3,2)` $=1.0$, `mgf_moment(1,3,2)` $\approx3.0$, and `mgf_moment(2,3,2)` $\approx13.0=\mu^2+\sigma^2$, as in the Check.

### P5.  The 68–95–99.7 rule  *(PSU L16.2)*
Using $P(|Z|\le k)=2\Phi(k)-1$, fill in the probabilities of $\mu\pm1\sigma$,
$\mu\pm2\sigma$, $\mu\pm3\sigma$. For IQ scores $X\sim N(100,15^2)$, what fraction
of people score between $85$ and $115$ (i.e. within one $\sigma$)? *Check:*
`empirical_rule(1), empirical_rule(2), empirical_rule(3)` $=(0.6827,0.9545,0.9973)$;
`float(normal_interval_prob(85,115,100,15))` $=0.6826895$.

**Solution.** By symmetry $P(|Z|\le k)=\Phi(k)-\Phi(-k)=2\Phi(k)-1$. Evaluating $\Phi$ at $k=1,2,3$,
$$P(|Z|\le1)=0.6827,\qquad P(|Z|\le2)=0.9545,\qquad P(|Z|\le3)=0.9973,$$
the 68–95–99.7 rule. For $X\sim N(100,15^2)$ the band $85$–$115$ is exactly $\mu\pm1\sigma$, so the fraction inside is $P(|Z|\le1)=0.6827$. Thus `empirical_rule(1), empirical_rule(2), empirical_rule(3)` $=(0.6827,0.9545,0.9973)$ and `float(normal_interval_prob(85,115,100,15))` $=0.6826895$, as in the Check.

### P6.  A tail probability with $\Phi$ via erf  *(PSU L16.3)*
SAT-section scores are modeled $X\sim N(500,100^2)$. Standardize $x=650$ to
$z=1.5$ and find $P(X>650)=1-\Phi(1.5)$. Separately, what is $P(X>130)$ for the
IQ model $N(100,15^2)$ (a two-$\sigma$ event)? *Check:* `1-float(normal_cdf(650,500,100))`
$=0.0668072$ (so $z=1.5\Rightarrow\Phi=0.9331928$); `1-float(normal_cdf(130,100,15))`
$=0.0227501$ (the upper-$2\sigma$ tail, half of $1-0.9545$).

**Solution.** Standardize each threshold. For $X\sim N(500,100^2)$ and $x=650$, $z=(650-500)/100=1.5$, so
$$P(X>650)=1-\Phi(1.5)=1-0.9331928=0.0668072.$$
For the IQ model $X\sim N(100,15^2)$ and $x=130$, $z=(130-100)/15=2$ — a two-$\sigma$ event — so
$$P(X>130)=1-\Phi(2)=0.0227501,$$
which is half of $1-0.9545$ by the empirical rule. These are `1-float(normal_cdf(650,500,100))` $=0.0668072$ and `1-float(normal_cdf(130,100,15))` $=0.0227501$ of the Check.

### P7.  Percentiles by inverting $\Phi$  *(PSU L16.3)*
The probit values $\Phi^{-1}(0.90)=1.2816$, $\Phi^{-1}(0.95)=1.6449$,
$\Phi^{-1}(0.975)=1.9600$ are the multipliers behind one-sided $90\%/95\%$ limits
and two-sided $95\%$ intervals. Find the $90$th percentile of the SAT model
$N(500,100^2)$ from $x_p=\mu+\sigma\Phi^{-1}(p)$, and check $\Phi^{-1}(\tfrac12)=0$.
*Check:* `probit(0.5)` $=0$; `probit(0.975)` $=1.9599640$;
`normal_quantile(0.90,500,100)` $=628.1552=500+100(1.2816)$.

**Solution.** A normal percentile undoes the standardization: from $\Phi(z_p)=p$ and $x_p=\mu+\sigma z_p$,
$$x_{0.90}=\mu+\sigma\,\Phi^{-1}(0.90)=500+100(1.2816)=628.16$$
for $N(500,100^2)$. Symmetry of $\varphi$ forces the median multiplier to vanish, $\Phi^{-1}(\tfrac12)=0$, since $\Phi(0)=\tfrac12$. The probit values $\Phi^{-1}(0.90,0.95,0.975)=1.2816,1.6449,1.9600$ are the usual confidence multipliers. So `probit(0.5)` $=0$, `probit(0.975)` $=1.9599640$, and `normal_quantile(0.90,500,100)` $=628.1552=500+100(1.2816)$, as in the Check.

### P8.  Symmetry of the cdf and the $1.96$ point  *(PSU L16.3)*
Prove $\Phi(-z)=1-\Phi(z)$ from the evenness of $\varphi$, and use it to show the
central $95\%$ of $N(0,1)$ lies in $(-1.96,1.96)$ — i.e. $\Phi(1.96)\approx0.975$,
not the round $\Phi(2)=0.9772$ of the empirical rule. *Check:*
`float(standard_normal_cdf(1.96))` $=0.9750021$ while `float(standard_normal_cdf(2.0))`
$=0.9772499$; and `float(standard_normal_cdf(-1.96))` $=1-0.9750021=0.0249979$.

**Solution.** Because $\varphi$ is even, the left tail below $-z$ equals the right tail above $z$:
$$\Phi(-z)=\int_{-\infty}^{-z}\varphi(u)\,du=\int_{z}^{\infty}\varphi(u)\,du=1-\Phi(z).$$
The central $95\%$ then sits between the symmetric points $\pm z_0$ with $\Phi(z_0)=0.975$, namely $z_0=1.96$, since $2(0.975)-1=0.95$. This is slightly tighter than the empirical-rule $\Phi(2)=0.9772$. Indeed `float(standard_normal_cdf(1.96))` $=0.9750021$ while `float(standard_normal_cdf(2.0))` $=0.9772499$, and `float(standard_normal_cdf(-1.96))` $=1-0.9750021=0.0249979$, confirming $\Phi(-z)=1-\Phi(z)$ as in the Check.
