# ST-16 — Transformations of Random Variables (notes)

A random variable $X$ comes with a law — a pdf $f_X$ or cdf $F_X$. Apply a
function, $Y=g(X)$, and $Y$ is a new random variable with its *own* law. The
central question of STAT 414's final section is: **given $f_X$ and $g$, what is
$f_Y$?** Three answers, in increasing slickness — the universal cdf method, the
change-of-variables shortcut for monotone $g$, and the Jacobian rule in two
dimensions — plus the special case $Z=X+Y$ (a sum of independents), which is a
**convolution**. These are the machines that manufacture the sampling
distributions of statistics (`~ST-17`) and, in the limit, the normal law
(`~ST-18`).

Citation key (full details + granularity in `refs.md`): **PSU L$n$** = Penn State
STAT 414 OER, Lesson $n$; **HTZ** = Hogg, Tanis & Zimmerman, *Probability and
Statistical Inference*, Ch. 5; cited at **lesson/chapter level**. Code symbols in
`code/transformations.py`.

## 1. The cdf (distribution-function) method

The one method that *always* works. The cdf of $Y=g(X)$ is, by definition, the
probability of an event in $X$-space [PSU L22]:
$$F_Y(y)=P(Y\le y)=P\big(g(X)\le y\big)=\int_{\{x\,:\,g(x)\le y\}} f_X(x)\,dx .$$
You read off the **inverse image** $\{x:g(x)\le y\}$, integrate $f_X$ over it, and
get $F_Y$; differentiate to get the density, $f_Y(y)=F_Y'(y)$. Code `cdf_of_Y`
performs the integral over a grid (summing $f_X$ where the indicator $g(x)\le y$
holds); `pdf_of_Y_cdf_method` differentiates it numerically.

**Worked example — a square.** Let $X\sim U(0,1)$ and $Y=X^2$. For $0\le y\le1$,
the event $\{X^2\le y\}=\{0\le X\le\sqrt y\}$, so
$$F_Y(y)=P(X\le\sqrt y)=\sqrt y,\qquad
f_Y(y)=\frac{d}{dy}\sqrt y=\frac{1}{2\sqrt y},\quad 0<y<1 .$$
The density **blows up** at $y=0^+$ yet integrates to $1$ — squaring piles up mass
near zero. Check: `cdf_of_Y(uniform_pdf, lambda x:x*x, y, 0,1)` $=\sqrt y$ and
`pdf_of_Y_cdf_method(...)` $=1/(2\sqrt y)$.

**Worked example — a normal squared is $\chi^2_1$.** Let $X\sim N(0,1)$ and
$Y=X^2$. Now $\{X^2\le y\}=\{-\sqrt y\le X\le\sqrt y\}$, so for $y>0$
$$F_Y(y)=\Phi(\sqrt y)-\Phi(-\sqrt y)=2\Phi(\sqrt y)-1,\qquad
f_Y(y)=2\,\phi(\sqrt y)\cdot\frac{1}{2\sqrt y}=\frac{1}{\sqrt{2\pi y}}\,e^{-y/2}.$$
That is exactly the **chi-square distribution with one degree of freedom**,
$\chi^2_1=\mathrm{Gamma}(k=\tfrac12,\ \lambda=\tfrac12)$ — the seed of the whole
sampling-distribution family in `~ST-17`. Check: `pdf_of_Y_cdf_method(normal_pdf,
lambda x:x*x, y, -12, 12)` $\approx$ `gamma_pdf(y, 0.5, 0.5)`.

## 2. The change-of-variables formula (monotone $g$)

When $g$ is **one-to-one** (strictly monotone) on the support of $X$, the cdf
method collapses to a formula. For increasing $g$, $\{g(X)\le y\}=\{X\le g^{-1}(y)\}$,
so $F_Y(y)=F_X(g^{-1}(y))$; differentiate with the chain rule and write
$x=g^{-1}(y)$:
$$f_Y(y)=f_X\!\big(g^{-1}(y)\big)\,\frac{dg^{-1}}{dy}.$$
For decreasing $g$ the inequality flips, $F_Y(y)=1-F_X(g^{-1}(y))$, and the
derivative $dg^{-1}/dy$ is negative; both cases combine into the **change-of-variables
(Jacobian) formula** [PSU L22; HTZ §5.1]:
$$\boxed{\,f_Y(y)=f_X\!\big(g^{-1}(y)\big)\,\Big|\frac{dx}{dy}\Big|\,},\qquad
\frac{dx}{dy}=\frac{dg^{-1}}{dy}=\frac{1}{g'(x)}\Big|_{x=g^{-1}(y)} .$$
The absolute value $|dx/dy|$ is the **local stretch factor**: it conserves
probability mass, $f_Y(y)\,|dy|=f_X(x)\,|dx|$, so that wherever $g$ stretches an
interval the density thins, and where $g$ compresses it the density piles up. Code
`change_of_variables_1d(fX, ginv, dxdy, y)` evaluates the boxed formula given the
back-substitution $g^{-1}$ and its derivative.

**Worked example — generating an exponential.** Let $X\sim U(0,1)$ and
$Y=g(X)=-\tfrac1\lambda\ln X$ (decreasing). Then $g^{-1}(y)=e^{-\lambda y}$ and
$dx/dy=-\lambda e^{-\lambda y}$, and since $f_X\equiv1$ on $(0,1)$,
$$f_Y(y)=1\cdot\big|-\lambda e^{-\lambda y}\big|=\lambda e^{-\lambda y},\quad y>0,$$
i.e. $Y\sim\mathrm{Exp}(\lambda)$. This is **inverse-transform sampling** (§6) in
action. Check: `change_of_variables_1d(uniform_pdf, exp(-rate y), -rate exp(-rate y), y)`
$=$ `exp_pdf(y, rate)`. Test `test_change_of_variables_equals_differentiated_cdf`
also confirms the formula equals the numeric derivative of the true cdf $F_Y=1-e^{-\lambda y}$.

A subtlety: when $g$ is *not* one-to-one (like $g(x)=x^2$ on all of $\mathbb R$),
sum the formula over **all branches** $g^{-1}_k(y)$ — which is exactly how the two
roots $\pm\sqrt y$ produced the factor of $2$ in the $\chi^2_1$ example of §1.

## 3. The 2-D Jacobian transformation

In two dimensions, transform the pair $(X,Y)$ with joint density $f_{XY}$ by a
one-to-one map $(U,V)=T(X,Y)$, with inverse $(X,Y)=T^{-1}(U,V)$, i.e.
$x=x(u,v),\ y=y(u,v)$. Conservation of mass over an area element,
$f_{UV}(u,v)\,du\,dv=f_{XY}(x,y)\,dx\,dy$, together with the area-rescaling rule of
multivariable calculus $dx\,dy=|J|\,du\,dv$ (`~MA-03`), gives [PSU L23; HTZ §5.2]
$$\boxed{\,f_{UV}(u,v)=f_{XY}\!\big(x(u,v),y(u,v)\big)\,\big|J\big|\,},\qquad
J=\det\frac{\partial(x,y)}{\partial(u,v)}
=\det\begin{pmatrix}x_u & x_v\\[2pt] y_u & y_v\end{pmatrix}=x_uy_v-x_vy_u .$$
$J$ is the **Jacobian determinant** of the inverse map — the signed factor by
which $T^{-1}$ scales areas. Code `jacobian_det_2d(inv_map, u, v)` forms it by
central differences; `jacobian_transform_2d(fXY, inv_map, u, v)` multiplies
$f_{XY}\,|J|$. To find the law of a *single* function $U=g(X,Y)$, introduce an
auxiliary $V$ (often $V=Y$ or $V=X$), apply the rule, then **marginalize** out $V$.

**Worked example — exponentials to gamma $\times$ uniform.** Let $X,Y\sim\mathrm{Exp}(1)$
independent, $f_{XY}(x,y)=e^{-x}e^{-y}$ on the first quadrant. Define
$$U=X+Y,\qquad V=\frac{X}{X+Y}\quad\Longrightarrow\quad x=uv,\ \ y=u(1-v),$$
with $u>0$, $0<v<1$. The Jacobian is
$$J=\det\begin{pmatrix}v & u\\ 1-v & -u\end{pmatrix}=-uv-u(1-v)=-u,\qquad |J|=u,$$
so
$$f_{UV}(u,v)=e^{-uv}e^{-u(1-v)}\cdot u=u\,e^{-u}
=\underbrace{u\,e^{-u}}_{\mathrm{Gamma}(2,1)}\cdot\underbrace{1}_{U(0,1)} .$$
The joint density **factorizes**: $U\sim\mathrm{Gamma}(2,1)$ and
$V\sim U(0,1)$ are **independent**. (The sum $X+Y$ being Gamma$(2,1)$ is exactly
the convolution result of §4.) Check: `jacobian_transform_2d(fXY, inv, u, v)`
$=u\,e^{-u}=$ `gamma_pdf(u,2,1)*uniform_pdf(v)`, with `jacobian_det_2d` $=-u$, and
integrating over $v$ recovers the Gamma$(2,1)$ marginal of $U$
(`test_jacobian_marginal_of_U_is_gamma2`).

## 4. Sums of independent variables: convolution

The most important transform is the **sum** $Z=X+Y$ of *independent* $X,Y$. Slice
the event $\{X+Y\le z\}$ at fixed $X=t$ and use independence $f_{XY}=f_Xf_Y$:
$$F_Z(z)=\iint_{x+y\le z}f_X(x)f_Y(y)\,dx\,dy
=\int_{-\infty}^{\infty}f_X(t)\,F_Y(z-t)\,dt,$$
and differentiating under the integral gives the **convolution formula** [PSU L23;
HTZ §5.2]:
$$\boxed{\,f_{X+Y}(z)=(f_X * f_Y)(z)=\int_{-\infty}^{\infty}f_X(t)\,f_Y(z-t)\,dt\,}.$$
This is the *probabilistic* convolution theorem: **adding independent variables
convolves their densities**, mirroring the Fourier convolution theorem (`~MA-09`).
The transform-domain shortcut — convolution becomes a *product* — is the
moment-generating-function technique of `~ST-17`: $M_{X+Y}(t)=M_X(t)\,M_Y(t)$. Code
`convolution(fX, fY, z, t_lo, t_hi)` integrates over $t$ (the support of $f_X$).

**Worked example — two uniforms make a triangle.** With $X,Y\sim U(0,1)$, the
integrand $f_X(t)f_Y(z-t)$ is $1$ only where both $0\le t\le1$ and $0\le z-t\le1$;
the length of that overlap is
$$f_{X+Y}(z)=\begin{cases}z, & 0\le z\le1,\\ 2-z, & 1\le z\le2,\\ 0, &\text{else,}\end{cases}$$
the **triangular** density on $[0,2]$, peaking at $z=1$ with height $1$. (Two
flat distributions add to a tent — the first whisper of the CLT, `~ST-18`.) Check:
`convolution(uniform_pdf, uniform_pdf, z, 0, 1)` $=$ `triangular_pdf(z)`, peak
$=1$ at $z=1$.

**Worked example — exponentials make a gamma (Erlang).** With $X,Y\sim\mathrm{Exp}(\lambda)$,
$$f_{X+Y}(z)=\int_0^z\lambda e^{-\lambda t}\,\lambda e^{-\lambda(z-t)}\,dt
=\lambda^2 e^{-\lambda z}\!\int_0^z dt=\lambda^2 z\,e^{-\lambda z},\quad z>0,$$
which is $\mathrm{Gamma}(2,\lambda)$. By induction the sum of $n$ i.i.d.
$\mathrm{Exp}(\lambda)$ is
$$f_{S_n}(z)=\frac{\lambda^n}{(n-1)!}\,z^{\,n-1}e^{-\lambda z}=\mathrm{Gamma}(n,\lambda)
\ \ (\text{Erlang}),$$
the waiting time for the $n$-th event of a Poisson process. Check:
`convolution(exp_pdf, exp_pdf, z, 0, z)` $=$ `gamma_pdf(z,2,λ)` and convolving once
more with an exponential gives `gamma_pdf(z,3,λ)`
(`test_sum_of_exponentials_is_gamma`).

## 5. The probability integral transform

A special transform with outsized importance. Take a continuous $X$ with cdf
$F_X$ and feed $X$ through *its own* cdf, $U=F_X(X)$. Because $F_X$ is increasing
with inverse the quantile function $F_X^{-1}$, the change-of-variables formula
(§2) gives, for $0<u<1$,
$$f_U(u)=f_X\!\big(F_X^{-1}(u)\big)\,\Big|\frac{d}{du}F_X^{-1}(u)\Big|
=f_X(x)\cdot\frac{1}{f_X(x)}=1,$$
using $\dfrac{dF_X^{-1}}{du}=1/F_X'(x)=1/f_X(x)$. Hence the **probability integral
transform** [PSU L22]:
$$\boxed{\,U=F_X(X)\sim \mathrm{Uniform}(0,1)\,}\qquad(\text{any continuous }X).$$
Every continuous distribution is a "stretched uniform." Code
`probability_integral_transform_pdf(fX, Finv, u)` evaluates $f_X(F^{-1}(u))\,|dF^{-1}/du|$
and returns $1$ for an exponential base law *and* for the linear density $f(x)=2x$
(`test_probability_integral_transform_is_uniform`).

## 6. Inverse-transform sampling — the payoff

Run §5 backwards. If $U\sim U(0,1)$ then $X=F_X^{-1}(U)$ has cdf $F_X$:
$$P(X\le x)=P\big(F_X^{-1}(U)\le x\big)=P\big(U\le F_X(x)\big)=F_X(x).$$
So to *simulate* any continuous law, draw a uniform and apply the inverse cdf. For
the exponential this is $X=-\tfrac1\lambda\ln(1-U)$ — the very transform of §2.
Code `exp_quantile(u, rate)` is $F^{-1}$, and
`test_inverse_transform_sampling_consistency` verifies $F_X(F_X^{-1}(u))=u$. This
identity is why pseudo-random generators only ever need a uniform source.

## Where this goes

- `~ST-17` (the **MGF technique** & normal sampling distributions) — the natural
  sequel: convolution of densities (§4) becomes *multiplication* of
  moment-generating functions (`~ST-06`), so sums of independents are read off
  instantly; the $\chi^2_1=Z^2$ derived in §1 generates the $\chi^2$, Student-$t$,
  and $F$ laws of statistics.
- `~MA-03` (coordinate systems & **Jacobians**) — the determinant $|J|$ of §3 *is*
  the area-rescaling factor of a curvilinear coordinate change.
- `~MA-09` (Fourier transforms & **convolution**) — §4 is the probabilistic face
  of the convolution theorem; characteristic functions are Fourier transforms of
  densities, the analytic backbone of `~ST-18`.
- `~ST-18` (the **central limit theorem**) — iterating the sum-of-independents
  convolution drives the standardized sum to the normal law; the triangular tent
  of §4 is its first step.
- `~ST-12` (the normal distribution) and `~ST-11` (exponential, gamma, chi-square)
  — the distributions transformed here; `~SM-06` (Maxwell speed distribution) — a
  physics change-of-variables from a Gaussian velocity to the speed.
