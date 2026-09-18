# ST-17 — Problems

Work each by hand, then check with `code/mgf_technique_sampling.py`. Citations in
`../refs.md`; **PSU L25/L26** = Penn State STAT 414 Lessons 25–26, **HTZ** =
Hogg–Tanis–Zimmerman Ch. 5. Throughout, "independent" means we may **multiply
mgfs** (`~ST-06`), and uniqueness lets us **recognize** the product.

### P1.  Sum of independent normals  *(PSU L25; `~ST-12`)*
Let $X_1\sim N(1,4)$, $X_2\sim N(-0.5,2.25)$, $X_3\sim N(2,1)$ be independent. Use
$M_{\sum X_i}(t)=\prod_iM_{X_i}(t)$ to show $S=X_1+X_2+X_3$ is normal, and find its
mean and variance. Why does the product of three exponential-quadratics stay an
exponential-quadratic? *Check:* `sum_of_normals_via_mgf([1,-0.5,2],[4,2.25,1])`
$=(2.5,7.25)$; `product_of_normal_mgfs(0.3,[1,-0.5,2],[4,2.25,1])` $=2.9336577$
equals `normal_mgf(0.3, 2.5, math.sqrt(7.25))`.

**Solution.** Each factor is $M_{X_i}(t)=\exp(\mu_it+\tfrac12\sigma_i^2t^2)$, so the
product adds the exponents:
$$M_S(t)=\prod_{i=1}^3\exp\!\Big(\mu_it+\tfrac12\sigma_i^2t^2\Big)
=\exp\!\Big(\big(\textstyle\sum\mu_i\big)t+\tfrac12\big(\textstyle\sum\sigma_i^2\big)t^2\Big).$$
A sum of linear-plus-quadratic exponents is again linear-plus-quadratic, i.e. a
normal mgf, with $\sum\mu_i=1-0.5+2=2.5$ and $\sum\sigma_i^2=4+2.25+1=7.25$. By
uniqueness $S\sim N(2.5,7.25)$. Numerically both the assembled product and the
single recognized mgf give $2.9336577$ at $t=0.3$.

### P2.  A difference adds the variances  *(PSU L25)*
Heights of men and women are modeled $X_1\sim N(5,4)$, $X_2\sim N(3,9)$
(independent, some units). Find the distribution of the difference $D=X_1-X_2$.
Students often expect $\operatorname{Var}(D)=4-9<0$ — explain why the correct answer
*adds* the variances. *Check:* `linear_combination_of_normals([1,-1],[5,3],[4,9])`
$=(2.0, 13.0)$.

**Solution.** $D=1\cdot X_1+(-1)\cdot X_2$ is the linear combination of §2 of the
notes with $a_1=1,a_2=-1$, so
$$D\sim N\big(a_1\mu_1+a_2\mu_2,\ a_1^2\sigma_1^2+a_2^2\sigma_2^2\big)
=N(5-3,\ 4+9)=N(2,13).$$
The coefficient $-1$ enters the **variance squared**, $(-1)^2=1$, so subtracting a
variable still *injects* its variability — uncertainties compound, never cancel.
`linear_combination_of_normals([1,-1],[5,3],[4,9])`$=(2.0,13.0)$.

### P3.  Gammas add shapes, chi-squares add d.f.  *(PSU L25; `~ST-11`)*
Independent $V_1\sim\chi^2_3$, $V_2\sim\chi^2_5$, $V_3\sim\chi^2_2$. Show
$V_1+V_2+V_3\sim\chi^2_{10}$ by multiplying mgfs, and explain how this is the same
fact as "a sum of $n$ independent squared standard normals is $\chi^2_n$." *Check:*
`sum_of_chisquares([3,5,2])` $=10.0$; `product_of_chi2_mgfs(0.2,[3,5,2])` equals
`chi2_mgf(0.2,10)`.

**Solution.** With $M_{V_i}(t)=(1-2t)^{-r_i/2}$,
$$M_{\sum V_i}(t)=\prod_i(1-2t)^{-r_i/2}=(1-2t)^{-(3+5+2)/2}=(1-2t)^{-10/2},$$
the mgf of $\chi^2_{10}$; **degrees of freedom add**. Since each $\chi^2_{r_i}$ is
itself a sum of $r_i$ squared standard normals (notes §4), the combined variable is
a sum of $3+5+2=10$ such squares, $\sum_{i=1}^{10}Z_i^2\sim\chi^2_{10}$ — identical
content. This is the $\theta=2$ case of the gamma rule $\sum\mathrm{Gamma}(\alpha_i,
\theta)=\mathrm{Gamma}(\sum\alpha_i,\theta)$. `sum_of_chisquares([3,5,2])`$=10.0$ and
the mgf product matches `chi2_mgf(0.2,10)`.

### P4.  $Z^2$ is a chi-square with one degree of freedom  *(PSU L25; `~ST-16`)*
For $Z\sim N(0,1)$, derive the density of $W=Z^2$ by the change of variables
$w=z^2$ (two branches), and identify it as $\chi^2_1$. Confirm the special case
$\chi^2_2$ is the exponential of mean $2$. *Check:*
`square_of_standard_normal_pdf(2.0)` $=0.103777=$ `chi2_pdf(2.0,1)`; and
`chi2_pdf(2.0,2)` $=0.18394=\tfrac12e^{-1}$.

**Solution.** The map $w=z^2$ has the two preimages $z=\pm\sqrt w$, each contributing
$|dz/dw|=\frac{1}{2\sqrt w}$, so for $w>0$
$$f_W(w)=2\,\varphi(\sqrt w)\,\frac{1}{2\sqrt w}=\frac{\varphi(\sqrt w)}{\sqrt w}
=\frac{1}{\sqrt{2\pi}}\,w^{-1/2}e^{-w/2}.$$
This is the gamma density with $\alpha=\tfrac12,\theta=2$ (using $\Gamma(\tfrac12)
=\sqrt\pi$), i.e. $\chi^2_1$. Adding a second independent square gives $\chi^2_2=
\mathrm{Gamma}(1,2)$, the exponential of mean $2$: $f(w)=\tfrac12e^{-w/2}$. Hence
`square_of_standard_normal_pdf(2.0)`$=\varphi(\sqrt2)/\sqrt2=0.103777=$`chi2_pdf(2.0,1)`,
and `chi2_pdf(2.0,2)`$=\tfrac12e^{-1}=0.18394$.

### P5.  Sampling distribution of the mean  *(PSU L26; HTZ §5.5)*
A normal population has $\mu=100$, $\sigma^2=225$ (so $\sigma=15$). A random sample
of $n=25$ is drawn. Find the distribution of $\bar X$ and its standard error, and
show the standardized mean $Z=(\bar X-\mu)/(\sigma/\sqrt n)$ is *exactly* $N(0,1)$.
*Check:* `sampling_dist_of_mean(100,225,25)` $=(100.0, 9.0)$ (so SE $=\sqrt9=3$);
`standardized_mean_mgf(0.7,100,225,25)` $=1.2776213=e^{0.7^2/2}$.

**Solution.** $\bar X=\frac{1}{25}\sum X_i$ is the linear combination with all
$a_i=1/25$, so $\bar X\sim N\big(\mu,\sigma^2/n\big)=N(100,\,225/25)=N(100,9)$; the
**standard error** is $\sigma/\sqrt n=15/5=3$. Standardizing is the affine map
$Z=a\bar X+b$ with $a=1/3,b=-100/3$, whose mgf is
$$M_Z(t)=e^{bt}M_{\bar X}(at)
=\exp\!\Big(-\tfrac{100}{3}t\Big)\exp\!\Big(100\cdot\tfrac t3+\tfrac12\cdot9\cdot\tfrac{t^2}{9}\Big)
=e^{t^2/2},$$
the standard-normal mgf — true for *any* $\mu,\sigma,n$ when the population is
normal. `sampling_dist_of_mean(100,225,25)`$=(100.0,9.0)$ and
`standardized_mean_mgf(0.7,100,225,25)`$=1.2776213=e^{0.245}$.

### P6.  Student's $t$: heavy tails and the one-sample statistic  *(PSU L26; HTZ §5.6)*
Define $T=Z/\sqrt{V/r}$ with $Z\sim N(0,1)$, $V\sim\chi^2_r$ independent. State the
density, give $E[T]$ and $\operatorname{Var}[T]$, and explain why estimating
$\sigma$ by $S$ turns the standardized mean into $t_{n-1}$. Why is the $t_1$
(Cauchy) so pathological? *Check:* `students_t_pdf(0.0,3)` $=0.367553$;
`students_t_var(5)` $=1.6667=5/3$; `students_t_var(2)` $=\infty$; the $t_1$ peak
`students_t_pdf(0.0,1)` $=0.31831=1/\pi$.

**Solution.** The density is
$$f_T(t)=\frac{\Gamma(\frac{r+1}{2})}{\sqrt{r\pi}\,\Gamma(\frac r2)}
\Big(1+\frac{t^2}{r}\Big)^{-\frac{r+1}{2}},$$
symmetric about $0$ with $E[T]=0$ ($r>1$) and $\operatorname{Var}[T]=r/(r-2)$
($r>2$). For the sample, write the $S$-standardized mean over the $\sigma$-standardized one:
$$\frac{\bar X-\mu}{S/\sqrt n}
=\frac{(\bar X-\mu)/(\sigma/\sqrt n)}{\sqrt{[(n-1)S^2/\sigma^2]/(n-1)}}
=\frac{Z}{\sqrt{V/(n-1)}}\sim t_{n-1},$$
with $Z\sim N(0,1)$, $V\sim\chi^2_{n-1}$ independent — $\sigma$ cancels. The tails
decay only as $|t|^{-(r+1)}$, so low-$r$ $t$'s are heavy: at $r=2$ the variance is
already infinite, and the $t_1=$ Cauchy $f(t)=\frac{1}{\pi(1+t^2)}$ has *no* mean.
Checks: `students_t_pdf(0.0,3)`$=0.367553$, `students_t_var(5)`$=5/3=1.6667$,
`students_t_var(2)`$=\infty$, and the Cauchy peak `students_t_pdf(0.0,1)`$=1/\pi
=0.31831$.

### P7.  The normal limit $t_r\to N(0,1)$  *(PSU L26)*
Show $f_T(t)\to\varphi(t)$ as $r\to\infty$ by taking the limits of its two pieces,
and confirm numerically that $t_{2000}$ is essentially standard normal. Why does
$\operatorname{Var}(t_r)=r/(r-2)\to1$? *Check:* `students_t_pdf(1.0,2000)`
$=0.241910$ vs `standard_normal_pdf(1.0)` $=0.241971$; `students_t_var(1000)`
$<$ `students_t_var(10)`.

**Solution.** In $f_T$, the kernel $\big(1+\tfrac{t^2}{r}\big)^{-(r+1)/2}\to e^{-t^2/2}$
(since $(1+a/r)^{-r/2}\to e^{-a/2}$), and the constant
$\Gamma(\tfrac{r+1}{2})/[\sqrt{r\pi}\,\Gamma(\tfrac r2)]\to1/\sqrt{2\pi}$ (Stirling's
ratio $\Gamma(\tfrac{r+1}{2})/\Gamma(\tfrac r2)\sim\sqrt{r/2}$). Their product is
$\varphi(t)=\frac{1}{\sqrt{2\pi}}e^{-t^2/2}$. As $r\to\infty$ the sample $S\to\sigma$,
so the $t$ collapses to the $Z$ of P5; the variance $r/(r-2)=1+\frac{2}{r-2}\to1$.
Numerically `students_t_pdf(1.0,2000)`$=0.241910$ already matches
`standard_normal_pdf(1.0)`$=0.241971$ to four places, and the variance is monotone
toward $1$: `students_t_var(1000)`$<$`students_t_var(10)`.

### P8.  Snedecor's $F$ and the identity $T^2=F_{1,r}$  *(PSU L26; HTZ §5.6)*
Define $F=(U/r_1)/(V/r_2)$ with $U\sim\chi^2_{r_1}$, $V\sim\chi^2_{r_2}$
independent. State its density and mean, then prove that the square of a $t_r$
variable is $F_{1,r}$. *Check:* `f_mean(10)` $=1.25=10/8$; `f_pdf(1.0,5,10)`
$=0.49548$; and the squared-$t$ density `t_squared_pdf(4.0,6)` $=0.032018$ equals
`f_pdf(4.0,1,6)`.

**Solution.** The density is
$$f_F(x)=\frac{(r_1/r_2)^{r_1/2}}{B(\frac{r_1}2,\frac{r_2}2)}\,
\frac{x^{r_1/2-1}}{(1+\frac{r_1}{r_2}x)^{(r_1+r_2)/2}},\quad x>0,$$
with mean $E[F]=r_2/(r_2-2)$ for $r_2>2$ (here $10/8=1.25$). For the identity, take
$T=Z/\sqrt{V/r}$ with $Z\sim N(0,1)$, $V\sim\chi^2_r$ independent; then
$$T^2=\frac{Z^2}{V/r}=\frac{Z^2/1}{V/r}=\frac{U/1}{V/r}\sim F_{1,r},$$
because $U=Z^2\sim\chi^2_1$ (P4) is independent of $V$. As a density transform
$f_{T^2}(w)=f_T(\sqrt w)/\sqrt w$, which the code confirms equals $f_F(w;1,r)$:
`t_squared_pdf(4.0,6)`$=0.032018=$`f_pdf(4.0,1,6)`, while `f_mean(10)`$=1.25$ and
`f_pdf(1.0,5,10)`$=0.49548$. (This $T^2=F_{1,r}$ link is why a two-sided $t$-test
and the corresponding $F$-test agree.)
