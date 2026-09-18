# ST-16 — Problems

Work each by hand, then check with `code/transformations.py`. Citations in
`../refs.md`; **PSU L$n$** = Penn State STAT 414 Lesson $n$ (L22 one variable, L23
two variables, L24 several variables). The three methods — cdf, change-of-variables,
2-D Jacobian — plus the convolution of independents are the whole toolkit.

### P1.  The cdf method: a uniform squared  *(PSU L22)*
Let $X\sim U(0,1)$ and $Y=X^2$. Using the **distribution-function method**, find
the inverse image $\{x:x^2\le y\}$ for $0\le y\le1$, integrate $f_X$ over it to get
$F_Y(y)=\sqrt y$, then differentiate to $f_Y(y)=\tfrac{1}{2\sqrt y}$. Note the
density diverges at $y\to0^+$ yet $\int_0^1\tfrac{1}{2\sqrt y}\,dy=1$. *Check:*
`cdf_of_Y(uniform_pdf, lambda x:x*x, 0.64, 0.0, 1.0)` $=0.8=\sqrt{0.64}$ and
`pdf_of_Y_cdf_method(uniform_pdf, lambda x:x*x, 0.25, 0.0, 1.0)` $=1.0=\tfrac{1}{2\sqrt{0.25}}$.

**Solution.** Since $X\in(0,1)$ and $x\mapsto x^2$ is increasing there, the inverse image
of $\{Y\le y\}$ for $0\le y\le1$ is $\{0\le X\le\sqrt y\}$. Integrating the flat density
$f_X=1$ over it,
$$F_Y(y)=\int_0^{\sqrt y}1\,dx=\sqrt y,\qquad f_Y(y)=\frac{d}{dy}\sqrt y=\frac{1}{2\sqrt y},\quad 0<y<1.$$
The density diverges as $y\to0^+$ (squaring crowds mass toward $0$) yet stays a valid
pdf: $\int_0^1\tfrac{1}{2\sqrt y}\,dy=[\sqrt y]_0^1=1$. Numerically
`cdf_of_Y(uniform_pdf, lambda x:x*x, 0.64, 0.0, 1.0)` $=0.8=\sqrt{0.64}$ and
`pdf_of_Y_cdf_method(uniform_pdf, lambda x:x*x, 0.25, 0.0, 1.0)` $=1.0=\tfrac{1}{2\sqrt{0.25}}$.

### P2.  Change of variables: making an exponential  *(PSU L22; HTZ §5.1)*
Let $X\sim U(0,1)$ and $Y=-\tfrac1\lambda\ln X$ with $\lambda=2$. Show $g$ is
decreasing with $g^{-1}(y)=e^{-\lambda y}$ and $dx/dy=-\lambda e^{-\lambda y}$, so
the change-of-variables formula $f_Y(y)=f_X(g^{-1}(y))\,|dx/dy|=\lambda e^{-\lambda y}$
gives $Y\sim\mathrm{Exp}(\lambda)$. Confirm this equals $\tfrac{d}{dy}F_Y$ with
$F_Y(y)=1-e^{-\lambda y}$. *Check:* `change_of_variables_1d(uniform_pdf,
lambda y: math.exp(-2*y), lambda y: -2*math.exp(-2*y), 0.5)` $=0.73576=$
`exp_pdf(0.5, 2.0)`.

**Solution.** Inverting $y=-\tfrac1\lambda\ln x$ gives $x=g^{-1}(y)=e^{-\lambda y}$, a
decreasing map with $dx/dy=-\lambda e^{-\lambda y}$. Since $f_X\equiv1$ on $(0,1)$, the
change-of-variables formula gives
$$f_Y(y)=f_X\!\big(g^{-1}(y)\big)\,\Big|\frac{dx}{dy}\Big|=1\cdot\lambda e^{-\lambda y}=\lambda e^{-\lambda y},\quad y>0,$$
so $Y\sim\mathrm{Exp}(\lambda)$. This agrees with differentiating the cdf directly,
$\tfrac{d}{dy}(1-e^{-\lambda y})=\lambda e^{-\lambda y}$. At $\lambda=2,\ y=0.5$ it is
$2e^{-1}=0.73576$, matching `change_of_variables_1d(...)` $=$ `exp_pdf(0.5, 2.0)`.

### P3.  A normal squared is chi-square(1)  *(PSU L22; `~ST-17`)*
Let $Z\sim N(0,1)$ and $Y=Z^2$. Because $g(z)=z^2$ is **two-to-one**, the event
$\{Z^2\le y\}=\{-\sqrt y\le Z\le\sqrt y\}$; show
$F_Y(y)=2\Phi(\sqrt y)-1$ and $f_Y(y)=\dfrac{1}{\sqrt{2\pi y}}\,e^{-y/2}$, i.e.
$Y\sim\chi^2_1=\mathrm{Gamma}(\tfrac12,\tfrac12)$ — the first member of the
sampling-distribution family of `~ST-17`. *Check:*
`pdf_of_Y_cdf_method(normal_pdf, lambda x:x*x, 1.0, -12.0, 12.0)` $\approx0.2410$,
matching `gamma_pdf(1.0, 0.5, 0.5)` $=0.24197=e^{-1/2}/\sqrt{2\pi}$.

**Solution.** Because $g(z)=z^2$ is two-to-one, $\{Z^2\le y\}=\{-\sqrt y\le Z\le\sqrt y\}$,
so for $y>0$,
$$F_Y(y)=\Phi(\sqrt y)-\Phi(-\sqrt y)=2\Phi(\sqrt y)-1,\qquad f_Y(y)=2\,\phi(\sqrt y)\cdot\frac{1}{2\sqrt y}=\frac{1}{\sqrt{2\pi y}}\,e^{-y/2}.$$
The two-to-one map supplied the factor $2$ and the chain rule the $\tfrac1{2\sqrt y}$. This
is $\chi^2_1=\mathrm{Gamma}(\tfrac12,\tfrac12)$, whose density
$\tfrac{(1/2)^{1/2}}{\Gamma(1/2)}y^{-1/2}e^{-y/2}=\tfrac{1}{\sqrt{2\pi y}}e^{-y/2}$ matches
(using $\Gamma(\tfrac12)=\sqrt\pi$). At $y=1$ both equal $e^{-1/2}/\sqrt{2\pi}=0.24197$, so
`pdf_of_Y_cdf_method(normal_pdf, lambda x:x*x, 1.0, -12.0, 12.0)` $\approx0.2410$ matches
`gamma_pdf(1.0, 0.5, 0.5)` $=0.24197$.

### P4.  Sum of two uniforms is triangular  *(PSU L23)*
Let $X,Y\sim U(0,1)$ independent and $Z=X+Y$. From the convolution
$f_Z(z)=\int f_X(t)f_Y(z-t)\,dt$, show the integrand is $1$ only on the overlap of
$[0,1]$ and $[z-1,z]$, whose length gives the **triangular** density: $f_Z(z)=z$
on $[0,1]$, $2-z$ on $[1,2]$, peaking at $z=1$. *Check:*
`convolution(uniform_pdf, uniform_pdf, 0.7, 0.0, 1.0)` $=0.7$ and
`convolution(uniform_pdf, uniform_pdf, 1.5, 0.0, 1.0)` $=0.5$, equal to
`triangular_pdf(0.7)` and `triangular_pdf(1.5)`.

**Solution.** The convolution integrand $f_X(t)f_Y(z-t)$ equals $1$ exactly where both
$0\le t\le1$ and $0\le z-t\le1$, i.e. on $t\in[\max(0,z-1),\min(1,z)]$; the density is the
length of that overlap,
$$f_Z(z)=\min(1,z)-\max(0,z-1)=\begin{cases}z,&0\le z\le1,\\ 2-z,&1\le z\le2.\end{cases}$$
This is the **triangular** density on $[0,2]$, rising then falling with a peak of height
$1$ at $z=1$ (two flat laws add to a tent — the first hint of the CLT). Hence
`convolution(uniform_pdf, uniform_pdf, 0.7, 0.0, 1.0)` $=0.7$ and `(..., 1.5, ...)` $=0.5$,
equal to `triangular_pdf(0.7)` and `triangular_pdf(1.5)`.

### P5.  Sum of exponentials is gamma (Erlang)  *(PSU L24)*
Let $X_1,\dots,X_n\sim\mathrm{Exp}(\lambda)$ independent. Convolve two:
$f_{X_1+X_2}(z)=\int_0^z\lambda e^{-\lambda t}\lambda e^{-\lambda(z-t)}\,dt
=\lambda^2 z\,e^{-\lambda z}=\mathrm{Gamma}(2,\lambda)$. By induction the sum of
$n$ is $\mathrm{Gamma}(n,\lambda)=\tfrac{\lambda^n}{(n-1)!}z^{n-1}e^{-\lambda z}$ —
the Erlang waiting time for the $n$-th Poisson event. *Check:* with $\lambda=1$,
`convolution(exp_pdf, exp_pdf, 2.0, 0.0, 2.0)` $=0.27067=$ `gamma_pdf(2.0, 2, 1)`;
convolving that Gamma(2) once more, `convolution(lambda z: gamma_pdf(z,2,1),
exp_pdf, 3.0, 0.0, 3.0)` $=0.22404=$ `gamma_pdf(3.0, 3, 1)`.

**Solution.** Convolve two exponentials; the $e^{-\lambda z}$ factors out and the overlap
integral is just the length $z$,
$$f_{X_1+X_2}(z)=\int_0^z\lambda e^{-\lambda t}\,\lambda e^{-\lambda(z-t)}\,dt=\lambda^2 e^{-\lambda z}\int_0^z dt=\lambda^2 z\,e^{-\lambda z}=\mathrm{Gamma}(2,\lambda).$$
Convolving once more multiplies by another $\lambda e^{-\lambda t}$ and raises the
polynomial degree, so by induction the sum of $n$ is
$\mathrm{Gamma}(n,\lambda)=\tfrac{\lambda^n}{(n-1)!}z^{n-1}e^{-\lambda z}$ — the Erlang
waiting time for the $n$-th Poisson event. With $\lambda=1$,
`convolution(exp_pdf, exp_pdf, 2.0, 0.0, 2.0)` $=0.27067=$ `gamma_pdf(2.0, 2, 1)`, and
convolving that with an exponential at $z=3$ gives `0.22404 =` `gamma_pdf(3.0, 3, 1)`.

### P6.  The 2-D Jacobian: splitting a gamma  *(PSU L23; `~MA-03`)*
Let $X,Y\sim\mathrm{Exp}(1)$ independent, $U=X+Y$, $V=\dfrac{X}{X+Y}$. Invert to
$x=uv,\ y=u(1-v)$, compute the Jacobian
$J=\det\!\begin{pmatrix}v&u\\1-v&-u\end{pmatrix}=-u$, and show
$f_{UV}(u,v)=e^{-uv}e^{-u(1-v)}\,|{-u}|=u\,e^{-u}$, which **factorizes** into
$\mathrm{Gamma}(2,1)$ for $U$ and $U(0,1)$ for $V$ — so the total and the ratio are
*independent*. *Check:* with `fXY = lambda x,y: float(exp_pdf(x,1))*float(exp_pdf(y,1))`
and `inv = lambda u,v: (u*v, u*(1-v))`, `jacobian_det_2d(inv, 2.0, 0.7)` $=-2.0$ and
`jacobian_transform_2d(fXY, inv, 2.0, 0.7)` $=0.27067=2e^{-2}=$
`gamma_pdf(2.0,2,1)*uniform_pdf(0.7)`.

**Solution.** Inverting $(U,V)=(X+Y,\ \tfrac{X}{X+Y})$ gives $x=uv,\ y=u(1-v)$, with
Jacobian of the inverse map
$$J=\det\begin{pmatrix}x_u & x_v\\ y_u & y_v\end{pmatrix}=\det\begin{pmatrix}v & u\\ 1-v & -u\end{pmatrix}=-uv-u(1-v)=-u,\qquad |J|=u.$$
With $f_{XY}=e^{-x}e^{-y}$ the transform rule gives
$$f_{UV}(u,v)=e^{-uv}\,e^{-u(1-v)}\cdot u=u\,e^{-u}=\underbrace{u\,e^{-u}}_{\mathrm{Gamma}(2,1)}\cdot\underbrace{1}_{U(0,1)},$$
which factorizes with no $v$-dependence, so the total $U\sim\mathrm{Gamma}(2,1)$ and the
ratio $V\sim U(0,1)$ are independent. At $(u,v)=(2.0,0.7)$, `jacobian_det_2d(inv, 2.0, 0.7)`
$=-2.0$ and `jacobian_transform_2d(fXY, inv, 2.0, 0.7)` $=2e^{-2}=0.27067=$
`gamma_pdf(2.0,2,1)*uniform_pdf(0.7)`.

### P7.  The probability integral transform & inverse-transform sampling  *(PSU L22)*
(a) Show that for any continuous $X$ with cdf $F_X$, the variable $U=F_X(X)$ has
density $f_U(u)=f_X(F^{-1}(u))\,|dF^{-1}/du|=1$ on $(0,1)$, i.e. $U\sim U(0,1)$.
(b) Run it backwards: if $U\sim U(0,1)$ then $X=F_X^{-1}(U)$ has cdf $F_X$, so
drawing $X=-\tfrac1\lambda\ln(1-U)$ samples $\mathrm{Exp}(\lambda)$. *Check:* (a)
`probability_integral_transform_pdf(lambda x: exp_pdf(x,2.0), lambda u: exp_quantile(u,2.0), 0.6)`
$=1.0$ and the same for the linear density, `probability_integral_transform_pdf(linear_pdf, linear_quantile, 0.6)`
$=1.0$. (b) `exp_cdf(exp_quantile(0.8, 2.0), 2.0)` $=0.8$ and the median
`exp_quantile(0.5, 2.0)` $=0.34657=\ln 2/2$.

**Solution.** (a) With $U=F_X(X)$ the inverse is the quantile $F_X^{-1}$, and since
$\tfrac{d}{du}F_X^{-1}(u)=1/F_X'(x)=1/f_X(x)$ at $x=F_X^{-1}(u)$, change of variables gives
$$f_U(u)=f_X\!\big(F_X^{-1}(u)\big)\,\Big|\frac{dF_X^{-1}}{du}\Big|=f_X(x)\cdot\frac{1}{f_X(x)}=1,\quad 0<u<1,$$
so $U\sim U(0,1)$ for *any* continuous $X$. (b) Run it backwards: if $U\sim U(0,1)$ then
$X=F_X^{-1}(U)$ has $P(X\le x)=P(U\le F_X(x))=F_X(x)$; for the exponential
$F_X^{-1}(u)=-\tfrac1\lambda\ln(1-u)$, so $X=-\tfrac1\lambda\ln(1-U)$ samples
$\mathrm{Exp}(\lambda)$. Hence (a) `probability_integral_transform_pdf(...)` $=1.0$ for both
the exponential and the linear density, and (b) `exp_cdf(exp_quantile(0.8, 2.0), 2.0)` $=0.8$
with median `exp_quantile(0.5, 2.0)` $=\ln2/2=0.34657$.
