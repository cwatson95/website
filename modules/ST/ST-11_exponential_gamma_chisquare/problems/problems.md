# ST-11 — Problems

Work each by hand, then check with `code/exponential_gamma_chisquare.py`. Citations
in `../refs.md`; **L15.x** = Penn State STAT 414 Lesson 15. Throughout, $\lambda$ is
a **rate**, $\theta=1/\lambda$ a **scale**, $\alpha$ a **shape**, and $r$ the
chi-square **degrees of freedom**.

### P1.  The gamma function: factorials and half-integers  *(L15.1; `~MA-12`)*
From $\Gamma(\alpha)=\int_0^\infty t^{\alpha-1}e^{-t}dt$ derive the recursion
$\Gamma(\alpha+1)=\alpha\Gamma(\alpha)$ by parts, and use $\Gamma(1)=1$ to get
$\Gamma(n)=(n-1)!$. Then, starting from $\Gamma(\tfrac12)=\sqrt\pi$ (the Gaussian
integral), evaluate $\Gamma(\tfrac72)=\tfrac52\cdot\tfrac32\cdot\tfrac12\,\Gamma(\tfrac12)
=\tfrac{15}{8}\sqrt\pi$. *Check:* `gamma_function(5)` $=24.0=4!$;
`gamma_function(0.5)` $=1.772454=\sqrt\pi$; `gamma_function(3.5)` $=3.323351
=\tfrac{15}{8}\sqrt\pi$; and `gamma_lanczos(5.7)` matches `gamma_function(5.7)` to
$\sim10^{-13}$.

**Solution.** Integrate $\Gamma(\alpha+1)=\int_0^\infty t^{\alpha}e^{-t}\,dt$ by parts with $u=t^{\alpha}$, $dv=e^{-t}dt$; the boundary term $[-t^{\alpha}e^{-t}]_0^\infty$ vanishes, leaving
$$\Gamma(\alpha+1)=\alpha\int_0^\infty t^{\alpha-1}e^{-t}\,dt=\alpha\,\Gamma(\alpha).$$
With $\Gamma(1)=\int_0^\infty e^{-t}dt=1$, induction gives $\Gamma(n)=(n-1)!$. Starting instead from $\Gamma(\tfrac12)=\sqrt\pi$ and stepping up by the same recursion,
$$\Gamma(\tfrac72)=\tfrac52\cdot\tfrac32\cdot\tfrac12\,\Gamma(\tfrac12)=\tfrac{15}{8}\sqrt\pi=3.323351.$$
So `gamma_function(5)` $=24.0=4!$, `gamma_function(0.5)` $=1.772454=\sqrt\pi$, `gamma_function(3.5)` $=3.323351$, and the independent `gamma_lanczos(5.7)` matches `gamma_function(5.7)` to $\sim10^{-13}$, as in the Check.

### P2.  Exponential survival of a lifetime  *(L15.2)*
A device's lifetime is exponential with mean $5$ years, so $\lambda=1/5=0.2$. Find
$P(X>10)$ and $P(X\le 10)$. The survival function is $S(x)=e^{-\lambda x}$, so
$P(X>10)=e^{-2}=0.13534$ and $P(X\le 10)=1-e^{-2}=0.86466$. Confirm the mean and
variance are $1/\lambda=5$ and $1/\lambda^2=25$. *Check:* `exponential_survival(10, 0.2)`
$=0.135335$; `exponential_cdf(10, 0.2)` $=0.864665$; `exponential_mean(0.2)` $=5.0$,
`exponential_var(0.2)` $=25.0$.

**Solution.** Integrating the density $f(x)=\lambda e^{-\lambda x}$ from $x$ to $\infty$ gives the survival function $S(x)=P(X>x)=e^{-\lambda x}$. With $\lambda=0.2$,
$$P(X>10)=e^{-0.2\cdot10}=e^{-2}=0.135335,\qquad P(X\le10)=1-e^{-2}=0.864665.$$
The mean and variance are the standard exponential values $E[X]=1/\lambda=5$ and $\operatorname{Var}(X)=1/\lambda^2=25$. These are `exponential_survival(10, 0.2)` $=0.135335$, `exponential_cdf(10, 0.2)` $=0.864665$, `exponential_mean(0.2)` $=5.0$, and `exponential_var(0.2)` $=25.0$ of the Check.

### P3.  Memorylessness  *(L15.2; `~ST-08`)*
The same device has already run $3$ years. Show the chance it lasts $2$ more is the
same as for a brand-new one: $P(X>5\mid X>3)=P(X>5)/P(X>3)=e^{-\lambda\cdot 5}/
e^{-\lambda\cdot 3}=e^{-2\lambda}=P(X>2)$. With $\lambda=0.4$ both equal
$e^{-0.8}=0.449329$. This is the continuous mirror of the geometric law's
memorylessness (`~ST-08`). *Check:* `exp_memoryless_check(3.0, 2.0, 0.4)`
$=(0.449329,\,0.449329)$ — the two probabilities are equal.

**Solution.** Because $S(x)=e^{-\lambda x}$, the conditional survival factorizes and the elapsed time cancels:
$$P(X>s+t\mid X>s)=\frac{P(X>s+t)}{P(X>s)}=\frac{e^{-\lambda(s+t)}}{e^{-\lambda s}}=e^{-\lambda t}=P(X>t).$$
The device "forgets" its age — the continuous mirror of the geometric law's memorylessness (`~ST-08`). With $s=3,\ t=2,\ \lambda=0.4$ both sides equal $e^{-0.8}=0.449329$, so `exp_memoryless_check(3.0, 2.0, 0.4)` returns the equal pair $(0.449329,\,0.449329)$ of the Check.

### P4.  Gamma as a waiting time  *(L15.3; `~ST-09`)*
Customers arrive as a Poisson process at rate $\lambda=1/3$ per minute, so each
inter-arrival is exponential with scale $\theta=3$. The wait for the **2nd** arrival
is gamma with $\alpha=2,\theta=3$. Write its density
$f(x)=x\,e^{-x/3}/(\Gamma(2)\,3^2)=\tfrac{x}{9}e^{-x/3}$, and from
$M(t)=(1-3t)^{-2}$ read off mean $\alpha\theta=6$ and variance $\alpha\theta^2=18$.
Evaluate $f(3)=\tfrac{3}{9}e^{-1}=0.12263$ and the probability the 2nd customer has
arrived by $6$ min, $F(6)$. *Check:* `gamma_pdf(3.0, 2.0, 3.0)` $=0.122626$;
`gamma_mean(2.0, 3.0)` $=6.0$, `gamma_var(2.0, 3.0)` $=18.0$;
`gamma_cdf(6.0, 2.0, 3.0)` $=0.593994$.

**Solution.** The wait for the 2nd arrival is $\mathrm{Gamma}(\alpha=2,\theta=3)$ with density
$$f(x)=\frac{x^{\alpha-1}e^{-x/\theta}}{\Gamma(\alpha)\,\theta^{\alpha}}=\frac{x\,e^{-x/3}}{\Gamma(2)\,3^2}=\frac{x}{9}e^{-x/3},$$
so $f(3)=\tfrac{3}{9}e^{-1}=0.122626$. From the mgf $M(t)=(1-\theta t)^{-\alpha}=(1-3t)^{-2}$ one reads mean $\alpha\theta=6$ and variance $\alpha\theta^2=18$, and the cdf at $x=6$ is the regularized lower incomplete gamma $P(2,\,6/3)=P(2,2)=0.593994$. These match `gamma_pdf(3.0, 2.0, 3.0)` $=0.122626$, `gamma_mean(2.0, 3.0)` $=6.0$, `gamma_var(2.0, 3.0)` $=18.0$, and `gamma_cdf(6.0, 2.0, 3.0)` $=0.593994$ of the Check.

### P5.  A sum of exponentials is gamma  *(L15.3; `~ST-06`)*
Let $X_1,\dots,X_\alpha$ be iid exponential with scale $\theta$. Using that mgfs of
independent sums multiply, show
$M_{\sum X_i}(t)=\big[(1-\theta t)^{-1}\big]^{\alpha}=(1-\theta t)^{-\alpha}$, the
gamma$(\alpha,\theta)$ mgf — so by uniqueness (`~ST-06`) the sum is gamma. For
$\alpha=2$ verify by convolution: $f_{X_1+X_2}(x)=\int_0^x\lambda e^{-\lambda y}
\lambda e^{-\lambda(x-y)}dy=\lambda^2 x e^{-\lambda x}$. *Check:* with $\lambda=0.8$
($\theta=1.25$), `convolve_two_exponentials_pdf(2.5, 0.8)` $=0.216536=$
`gamma_pdf(2.5, 2.0, 1.25)`; and the mgf identity
`exponential_mgf(0.2, 1/1.5)**4` $=4.164931=$ `gamma_mgf(0.2, 4.0, 1.5)`.

**Solution.** Each exponential has mgf $(1-\theta t)^{-1}$; independence multiplies them, so
$$M_{\sum_{i=1}^{\alpha}X_i}(t)=\big[(1-\theta t)^{-1}\big]^{\alpha}=(1-\theta t)^{-\alpha},$$
the $\mathrm{Gamma}(\alpha,\theta)$ mgf — by uniqueness (`~ST-06`) the sum is gamma. For $\alpha=2$ the convolution confirms it directly,
$$f_{X_1+X_2}(x)=\int_0^x\lambda e^{-\lambda y}\,\lambda e^{-\lambda(x-y)}\,dy=\lambda^2 e^{-\lambda x}\int_0^x dy=\lambda^2 x\,e^{-\lambda x},$$
the $\mathrm{Gamma}(2,1/\lambda)$ density. With $\lambda=0.8$ ($\theta=1.25$) this gives `convolve_two_exponentials_pdf(2.5, 0.8)` $=0.216536=$ `gamma_pdf(2.5, 2.0, 1.25)`, and the mgf identity `exponential_mgf(0.2, 1/1.5)**4` $=4.164931=$ `gamma_mgf(0.2, 4.0, 1.5)`, as in the Check.

### P6.  Chi-square mean, variance, and the $r=2$ case  *(L15.4)*
The chi-square with $r$ degrees of freedom is gamma$(\alpha=r/2,\theta=2)$, so its
mean is $\alpha\theta=r$ and its variance $\alpha\theta^2=2r$. Show that for $r=2$
(shape $1$, scale $2$) it collapses to the **exponential of mean $2$**, i.e.
$\lambda=\tfrac12$: $f(x)=\tfrac12 e^{-x/2}$. *Check:* `chi2_mean(10)` $=10.0$,
`chi2_var(10)` $=20.0$; `chi2_pdf(3.0, 2)` $=0.111565=$ `exponential_pdf(3.0, 0.5)`;
and `chi2_cdf(3.0, 2)` $=1-e^{-1.5}=0.776870$.

**Solution.** Since $\chi^2_r=\mathrm{Gamma}(\alpha=r/2,\theta=2)$, its mean is $\alpha\theta=r$ and variance $\alpha\theta^2=2r$; at $r=10$ these are $10$ and $20$. For $r=2$ the shape is $\alpha=1$, and a gamma of shape one is exponential:
$$f(x)=\frac{x^{0}e^{-x/2}}{\Gamma(1)\,2^{1}}=\tfrac12 e^{-x/2},$$
the exponential of rate $\lambda=\tfrac12$ (mean $2$). Hence $f(3)=\tfrac12 e^{-1.5}=0.111565$ and $F(3)=1-e^{-1.5}=0.776870$. These match `chi2_mean(10)` $=10.0$, `chi2_var(10)` $=20.0$, `chi2_pdf(3.0, 2)` $=0.111565=$ `exponential_pdf(3.0, 0.5)`, and `chi2_cdf(3.0, 2)` $=0.776870$ of the Check.

### P7.  Chi-square and a molecule's kinetic energy  *(L15.4; `~SM-06`, `~ST-17`)*
In a gas at temperature $T$ a molecule's velocity has three independent normal
components, so its kinetic energy $E=\tfrac12 m v^2$ has $2E/kT=\sum_{i=1}^3
(v_i/\sigma)^2\sim\chi^2_3$ — a gamma of shape $\tfrac32$ (`~SM-06`). Hence
$E[2E/kT]=3$ gives the equipartition mean energy $\tfrac32 kT$, with variance
$\mathrm{Var}(2E/kT)=2\cdot 3=6$. (The same "sum of squared standard normals"
construction, $\chi^2_r=\sum_{i=1}^r Z_i^2$, is the launch point of sampling theory
`~ST-17`; note $P(\chi^2_1\le 1)=0.6827$, the one-$\sigma$ probability.) *Check:*
`chi2_mean(3)` $=3.0$, `chi2_var(3)` $=6.0$, `chi2_cdf(3.0, 3)` $=0.608375$; and
`chi2_cdf(1.0, 1)` $=0.682689$.

**Solution.** Writing each velocity component as a standard normal times $\sigma=\sqrt{kT/m}$, the scaled kinetic energy is a sum of three squared standard normals,
$$\frac{2E}{kT}=\sum_{i=1}^3\Big(\frac{v_i}{\sigma}\Big)^2\sim\chi^2_3,$$
a gamma of shape $\tfrac32$. Its mean is $r=3$, so $E[E]=\tfrac32 kT$ — equipartition — and its variance is $2r=6$. The same construction $\chi^2_r=\sum_{i=1}^r Z_i^2$ launches sampling theory (`~ST-17`); in particular $P(\chi^2_1\le1)=P(|Z|\le1)=0.6827$, the one-$\sigma$ probability. So `chi2_mean(3)` $=3.0$, `chi2_var(3)` $=6.0$, `chi2_cdf(3.0, 3)` $=0.608375$, and `chi2_cdf(1.0, 1)` $=0.682689$, as in the Check.
