# ST-05 — Problems

Work each by hand, then check with `code/discrete_rv_expectation.py`. Citations in
`../refs.md`; **PSU L7/L8** = Penn State STAT 414 Lessons 7 (discrete RVs) and 8
(expectation). Throughout, $f(x)=P(X=x)$ is a pmf, $\mu=E[X]$, $\sigma^2=
\mathrm{Var}(X)$, and "LOTUS" is $E[g(X)]=\sum_x g(x)f(x)$.

### P1. A fair die: pmf, cdf, mean, variance  *(PSU L7–L8)*
Let $X\sim\text{Uniform}\{1,\dots,6\}$, so $f(x)=\tfrac16$ on its support. Verify it
is a valid pmf ($\sum f=1$); compute the cdf value $F(3)=P(X\le3)$; the mean
$\mu=\tfrac16(1+\cdots+6)=\tfrac{21}{6}$; the second raw moment
$E[X^2]=\tfrac16(1+4+\cdots+36)=\tfrac{91}{6}$; and hence
$\sigma^2=E[X^2]-\mu^2=\tfrac{91}{6}-\tfrac{49}{4}=\tfrac{35}{12}$.
*Check:* with `x=np.arange(1,7); p=np.full(6,1/6)`, `pmf_is_valid(x,p)` $=$ `True`;
`cdf_from_pmf(x,p)(3.0)` $=0.5$; `expectation(x,p)` $=3.5$; `raw_moment(x,p,2)`
$=15.1\overline{6}$; `variance(x,p)` $=2.91\overline{6}$; `std(x,p)` $\approx1.7078$.

**Solution.** All six masses equal $\tfrac16\ge0$ and sum to $6\cdot\tfrac16=1$, so $f$
is a valid pmf. The cdf accumulates jumps of $\tfrac16$, so
$$F(3)=f(1)+f(2)+f(3)=\tfrac36=\tfrac12.$$
The mean and second raw moment are equally-weighted averages,
$$\mu=\tfrac16(1+2+\cdots+6)=\tfrac{21}{6}=\tfrac72,\qquad
E[X^2]=\tfrac16(1+4+\cdots+36)=\tfrac{91}{6}.$$
The computational formula then gives
$$\sigma^2=E[X^2]-\mu^2=\tfrac{91}{6}-\tfrac{49}{4}=\tfrac{182-147}{12}=\tfrac{35}{12},$$
so $\sigma=\sqrt{35/12}\approx1.7078$. These reproduce `pmf_is_valid`$=$`True`,
`cdf_from_pmf(...)(3.0)`$=0.5$, `expectation`$=3.5$, `raw_moment(...,2)`$=15.1\overline{6}$,
`variance`$=2.91\overline{6}$ and `std`$\approx1.7078$.

### P2. LOTUS: the variance is an expectation of a function  *(PSU L8)*
For the same die, compute $E[(X-\mu)^2]$ **directly** by LOTUS with $g(x)=(x-3.5)^2$
— summing $g(x)\,f(x)$ over $x=1,\dots,6$ — and confirm it equals the variance from
P1. This is the definitional route $\sigma^2=E[(X-\mu)^2]$; P1 used the
computational route $E[X^2]-\mu^2$. (They are forced equal by the algebra of §5.)
*Check:* `expectation_of(lambda t:(t-3.5)**2, x, p)` $=2.91\overline{6}=$
`variance(x,p)`; equivalently `central_moment(x,p,2)` $=2.91\overline{6}$.

**Solution.** LOTUS evaluates $E[g(X)]=\sum_x g(x)f(x)$ on the *old* pmf with
$g(x)=(x-3.5)^2$. The six deviations $x-3.5$ are $\pm2.5,\pm1.5,\pm0.5$, so the squared
deviations $6.25,2.25,0.25$ each occur twice:
$$E[(X-3.5)^2]=\tfrac16\big[2(6.25)+2(2.25)+2(0.25)\big]=\tfrac{17.5}{6}=\tfrac{35}{12}\approx2.9167.$$
This equals the computational variance of P1 because expanding the square and using
linearity gives $E[(X-\mu)^2]=E[X^2]-2\mu E[X]+\mu^2=E[X^2]-\mu^2$ — the two routes are
algebraically identical. Hence `expectation_of(lambda t:(t-3.5)**2, x, p)`$=2.91\overline{6}=$
`variance(x,p)`$=$`central_moment(x,p,2)`.

### P3. The Bernoulli trial: mean $p$, variance $p(1-p)$  *(PSU L8; `~ST-07`)*
Let $X$ be Bernoulli$(p)$: $f(1)=p$, $f(0)=1-p$. Show $\mu=E[X]=0\cdot(1-p)+1\cdot p
=p$, and since $X^2=X$ here, $E[X^2]=p$ too, so $\sigma^2=E[X^2]-\mu^2=p-p^2=p(1-p)$
— maximal at $p=\tfrac12$. This single trial is the atom the binomial of `~ST-07` is
built from. *Check:* with `bx=np.array([0.,1]); bp=np.array([.7,.3])` ($p=0.3$),
`expectation(bx,bp)` $=0.3$ and `variance(bx,bp)` $=0.21=p(1-p)$.

**Solution.** With only two atoms,
$$\mu=E[X]=0\cdot(1-p)+1\cdot p=p.$$
Since $X\in\{0,1\}$ obeys $X^2=X$ (as $0^2=0$ and $1^2=1$), the second moment is
$E[X^2]=E[X]=p$, and the computational formula gives
$$\sigma^2=E[X^2]-\mu^2=p-p^2=p(1-p).$$
This is maximal at $p=\tfrac12$ (where $\tfrac{d}{dp}[p-p^2]=1-2p=0$) and vanishes at
$p=0,1$. At $p=0.3$ the mass split is $(0.7,0.3)$, giving `expectation(bx,bp)`$=0.3$ and
`variance(bx,bp)`$=0.3(0.7)=0.21=p(1-p)$.

### P4. The computational formula on a signed RV  *(PSU L8)*
Let $X$ take values $\{-1,0,2\}$ with $f=\{0.2,0.5,0.3\}$. Compute $\mu=E[X]=
-0.2+0+0.6=0.4$ and $E[X^2]=0.2(1)+0.5(0)+0.3(4)=1.4$, hence
$\sigma^2=1.4-(0.4)^2=1.24$ and $\sigma=\sqrt{1.24}\approx1.1136$. Verify the
computational formula $E[X^2]-\mu^2$ agrees with the central moment $E[(X-\mu)^2]$.
*Check:* with `cx=np.array([-1.,0,2]); cp=np.array([.2,.5,.3])`,
`expectation(cx,cp)` $=0.4$; `raw_moment(cx,cp,2)` $=1.4$; `variance(cx,cp)` $=1.24$
$=$ `central_moment(cx,cp,2)`; `std(cx,cp)` $\approx1.1136$.

**Solution.** Direct weighted sums give
$$\mu=(-1)(0.2)+0(0.5)+2(0.3)=0.4,\qquad E[X^2]=1(0.2)+0(0.5)+4(0.3)=1.4.$$
The computational formula yields $\sigma^2=E[X^2]-\mu^2=1.4-0.16=1.24$ and
$\sigma=\sqrt{1.24}\approx1.1136$. The definitional route agrees term by term,
$$E[(X-0.4)^2]=(-1.4)^2(0.2)+(-0.4)^2(0.5)+(1.6)^2(0.3)=0.392+0.08+0.768=1.24,$$
confirming $E[(X-\mu)^2]=E[X^2]-\mu^2$. These are `expectation(cx,cp)`$=0.4$,
`raw_moment(cx,cp,2)`$=1.4$, `variance(cx,cp)`$=1.24=$`central_moment(cx,cp,2)`, and
`std(cx,cp)`$\approx1.1136$.

### P5. Linearity and the affine rule  *(PSU L8)*
For the $X$ of P4, let $Y=3X-4$. Use $E[aX+b]=aE[X]+b$ to get $E[Y]=3(0.4)-4=-2.8$,
and $\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$ to get $\mathrm{Var}(Y)=9(1.24)=11.16$,
so $\sigma_Y=3\sigma_X\approx3.341$. Note the shift $b=-4$ moves the mean but leaves
the variance untouched. *Check:* `yx,yp = linear_transform(3.,-4.,cx,cp)`;
`expectation(yx,yp)` $=-2.8$; `variance(yx,yp)` $=11.16$; `std(yx,yp)` $\approx3.341$.
Changing $b$ alone (e.g. `linear_transform(3.,96.,cx,cp)`) leaves `variance` at
$11.16$.

**Solution.** Linearity of expectation passes the additive constant straight through:
$$E[Y]=E[3X-4]=3E[X]-4=3(0.4)-4=-2.8.$$
A shift cannot change spread while a rescale squares it, so
$$\operatorname{Var}(3X-4)=3^2\operatorname{Var}(X)=9(1.24)=11.16,\qquad
\sigma_Y=|3|\,\sigma_X=3(1.1136)\approx3.341.$$
The additive constant is absent from the variance: replacing $-4$ by $+96$ moves the
mean but leaves $\operatorname{Var}=11.16$ untouched. These match `expectation(yx,yp)`$=-2.8$,
`variance(yx,yp)`$=11.16$, `std(yx,yp)`$\approx3.341$, and `linear_transform(3.,96.,cx,cp)`
still gives `variance`$=11.16$.

### P6. First central moment, skewness, and symmetry  *(PSU L8)*
Show the first central moment always vanishes, $\mu_1=E[X-\mu]=0$, and the zeroth
raw moment is $\mu'_0=1$. Then compare **skewness** $\gamma_1=\mu_3/\sigma^3$: the
fair die is symmetric about $3.5$, so $\gamma_1=0$; the RV of P4 is right-skewed
(mass piled at $-1,0$ with a far atom at $2$), giving $\gamma_1>0$. Compute
$\mu_3=\sum(x-0.4)^3 f=0.648$ and $\sigma^3=1.24^{3/2}\approx1.3808$, so
$\gamma_1\approx0.469$. *Check:* `central_moment(cx,cp,1)` $=0$;
`raw_moment(cx,cp,0)` $=1$; `skewness(x,p)` $=0.0$ (die); `skewness(cx,cp)`
$\approx0.4693$.

**Solution.** The first central moment vanishes for any RV by linearity,
$$\mu_1=E[X-\mu]=E[X]-\mu=0,$$
and the zeroth raw moment is normalization, $\mu'_0=E[X^0]=\sum_x f(x)=1$. Skewness
$\gamma_1=\mu_3/\sigma^3$ measures asymmetry: the die is symmetric about $3.5$, so
deviations pair off and $\mu_3=0\Rightarrow\gamma_1=0$. For the atoms $\{-1,0,2\}$,
$$\mu_3=(-1.4)^3(0.2)+(-0.4)^3(0.5)+(1.6)^3(0.3)=-0.5488-0.032+1.2288=0.648,$$
and with $\sigma^3=1.24^{3/2}\approx1.3808$ this gives $\gamma_1=0.648/1.3808\approx0.469>0$
(right-skewed — the far atom at $2$ stretches the right tail). Matches
`central_moment(cx,cp,1)`$=0$, `raw_moment(cx,cp,0)`$=1$, `skewness(x,p)`$=0$ (die) and
`skewness(cx,cp)`$\approx0.4693$.

### P7. The mean from the survival function  *(PSU L8)*
Let $X$ take values $\{0,1,2,3\}$ with $f=\{0.1,0.2,0.3,0.4\}$. Compute the mean two
ways: directly $\mu=\sum x f(x)=0.2+0.6+1.2=2.0$; and by the tail-sum identity for a
non-negative integer RV, $E[X]=\sum_{k\ge0}\big(1-F(k)\big)$ with $1-F(0)=0.9$,
$1-F(1)=0.7$, $1-F(2)=0.4$ (and $0$ thereafter), summing to $2.0$. *Check:* with
`x=np.array([0.,1,2,3]); p=np.array([.1,.2,.3,.4])`, `expectation(x,p)` $=2.0$ and
`mean_via_survival(x,p)` $=2.0$; `cdf_from_pmf(x,p)(1.0)` $=0.3$.

**Solution.** The direct mean is the weighted sum
$$\mu=\sum_x x f(x)=0(0.1)+1(0.2)+2(0.3)+3(0.4)=2.0.$$
The tail-sum identity $E[X]=\sum_{k\ge0}\big(1-F(k)\big)$ rearranges the same total by
counting each unit of $x$ once for every threshold it clears. Here $F(0)=0.1$,
$F(1)=0.3$, $F(2)=0.6$, so
$$1-F(0)=0.9,\quad 1-F(1)=0.7,\quad 1-F(2)=0.4,\quad 1-F(k\ge3)=0,$$
summing to $0.9+0.7+0.4=2.0$ — the same mean. Confirms `expectation(x,p)`$=2.0=$
`mean_via_survival(x,p)`, with `cdf_from_pmf(x,p)(1.0)`$=F(1)=0.3$.

### P8. The mgf generates the moments  *(PSU L9; `~ST-06`)*
For Bernoulli$(p)$ the moment-generating function is $M(t)=E[e^{tX}]=(1-p)+p\,e^{t}$.
Check the normalization $M(0)=1$; differentiate to get $M'(t)=p\,e^t$, so
$M'(0)=p=\mu$; and $M''(0)=p=E[X^2]$, recovering $\sigma^2=M''(0)-M'(0)^2=p-p^2$.
This is the §8 preview made explicit, and the method `~ST-06` generalizes.
*Check:* with the $p=0.3$ Bernoulli, `mgf(bx,bp,0.0)` $=1.0$; the finite difference
`(mgf(bx,bp,1e-6)-mgf(bx,bp,-1e-6))/2e-6` $\approx0.3=$ `expectation(bx,bp)`.

**Solution.** For Bernoulli$(p)$ the mgf is the two-term sum
$$M(t)=E[e^{tX}]=e^{0}(1-p)+e^{t}p=(1-p)+pe^t,$$
so $M(0)=(1-p)+p=1$ (the probabilities normalize). Every derivative of $pe^t$ is again
$pe^t$, hence
$$M'(t)=pe^t\ \Rightarrow\ M'(0)=p=\mu,\qquad M''(0)=p=E[X^2],$$
and $\sigma^2=M''(0)-M'(0)^2=p-p^2=p(1-p)$, recovering P3 from the generator alone. At
$p=0.3$, `mgf(bx,bp,0.0)`$=1.0$ and the symmetric difference
`(mgf(bx,bp,1e-6)-mgf(bx,bp,-1e-6))/2e-6`$\approx0.3=$`expectation(bx,bp)`$=M'(0)$.
