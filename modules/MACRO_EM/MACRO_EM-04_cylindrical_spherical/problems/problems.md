# MACRO_EM-04 — Problems (Wilcox Ch. 4, all 49 exercises)

Every exercise of Wilcox & Thron 2e §4.16 (printed pp. 180–202), worked in
full. Statements are paraphrased (all given equations and data kept); the book
prints no solutions — everything below is module-authored and machine-checked
in `code/cylindrical_spherical.py` / `code/test_cylindrical_spherical.py`.
Sources in `../refs.md`.

**Conventions (the book's, Gaussian units).** Unit point charge
$\Phi=1/|\vec x-\vec x'|$; Green equation $\nabla^2G=-4\pi\delta^3$ (4.73);
2-D line charge $G_f=-2\ln(\rho/L)$ with the reduced radial jump
$dg/d\rho|_{-}^{+}=-1/\rho'$; the 1-D convention (2.124) has **no** $4\pi$:
$d^2G/dx^2=-\delta$. Fourier–Bessel normalization (4.67)/(4.286):
$\mathcal J_{1m}(k_{mn}\rho)=\frac{\sqrt2}{a}\,\frac{J_m(x_{mn}\rho/a)}{J_{m+1}(x_{mn})}$,
$J_m(x_{mn})=0$, $k_{mn}=x_{mn}/a$. Reduced Green functions come from the
Wronskian recipe (4.128)–(4.130): $g=C\,\psi_1(x_<)\psi_2(x_>)$,
$C=D(x)/W_x[\psi_1,\psi_2]$. Spherical harmonics use the book's
Condon–Shortley convention (4.167)/(4.185), which is scipy's. Griffiths-level
background: `~EM-04`; the Ch. 3 toolbox: `~MACRO_EM-03`.

---

### P1.  Exercise 4.1.1 — Taylor series of $J_m$ two ways  *(Wilcox 2e §4.16, p.180)*
Derive the Taylor expansion (4.8),
$$J_m(t)=\sum_{n=0}^{\infty}\frac{(-1)^n\,(t/2)^{m+2n}}{n!\,(m+n)!},$$
(a) from the generating function (4.7), $e^{\frac t2(u-\frac1u)}=\sum_m u^mJ_m(t)$,
and (b) from the integral representation (4.13),
$J_n(t)=i^{-n}\int_0^{2\pi}\frac{d\phi}{2\pi}e^{i(t\cos\phi-n\phi)}$.
*Answer:* both routes give exactly (4.8); with $J_{-m}=(-1)^mJ_m$ (4.10) for
negative order.
*Check:* `jm_taylor` (log-stabilized series) $=$ `scipy.jv` $=$
`jn_intrep_413` to $10^{-12}$, including $m<0$ (`test_p1_taylor_series`).

**Solution.** (a) Factor the generating function and expand each exponential:
$$e^{tu/2}\,e^{-t/2u}=\sum_{j=0}^\infty\frac{(t/2)^j}{j!}u^j
\sum_{i=0}^\infty\frac{(-1)^i(t/2)^i}{i!}u^{-i}.$$
The coefficient of $u^m$ collects all $(j,i)$ with $j-i=m$, i.e. $j=m+n$,
$i=n$:
$$J_m(t)=\sum_{n}\frac{(-1)^n(t/2)^{m+2n}}{n!\,(m+n)!},$$
the sum starting at $n=\max(0,-m)$ — which for $m\ge0$ is (4.8), and for
$m<0$ reproduces $(-1)^mJ_{|m|}$ after shifting the index.
(b) Expand $e^{it\cos\phi}=\sum_k\frac{(it)^k}{k!}\cos^k\phi$ inside (4.13)
and use $\cos^k\phi=2^{-k}(e^{i\phi}+e^{-i\phi})^k$. The $\phi$ average kills
every term except those where the binomial supplies $e^{+in\phi}$, i.e.
$k=n+2j$ with binomial coefficient $\binom{n+2j}{j}$:
$$J_n=i^{-n}\sum_j\frac{(it)^{n+2j}}{(n+2j)!}\,\frac{1}{2^{n+2j}}\binom{n+2j}{j}
=\sum_j\frac{i^{2j}\,(t/2)^{n+2j}}{j!\,(n+j)!}
=\sum_j\frac{(-1)^j(t/2)^{n+2j}}{j!\,(n+j)!}.$$

### P2.  Exercise 4.1.2 — Two Bessel sum rules  *(Wilcox 2e §4.16, p.180)*
From the plane-wave form of the generating function,
$e^{it\cos\phi}=\sum_{m}i^me^{im\phi}J_m(t)$, prove
(a) $\sum_{m=-\infty}^{\infty}J_m(t)^2=1$ and
(b) $J_0(2t)=\sum_{m=-\infty}^{\infty}(-1)^mJ_m(t)^2$.
*Answer:* (a) is the $\phi$-average of $|e^{it\cos\phi}|^2=1$; (b) is the
$\phi$-average of $(e^{it\cos\phi})^2=e^{2it\cos\phi}$.
*Check:* both sums at $t=0.4,1.3,3.1,6.4$ to $10^{-11}$
(`test_p2_sum_rules`).

**Solution.** (a) Multiply the expansion by its complex conjugate:
$$1=|e^{it\cos\phi}|^2=\sum_{m,m'}i^{m-m'}e^{i(m-m')\phi}J_mJ_{m'}.$$
Averaging over $\phi\in[0,2\pi)$ keeps only $m=m'$: $1=\sum_mJ_m^2$.
(b) Square instead of conjugating: $e^{2it\cos\phi}$ has the same expansion
with $t\to2t$, and its $\phi$ average is the $m=0$ term, $J_0(2t)$. On the
other side the average of $\bigl(\sum_mi^me^{im\phi}J_m\bigr)^2$ keeps
$m'=-m$:
$$J_0(2t)=\sum_m i^{m}i^{-m}J_mJ_{-m}=\sum_m(-1)^mJ_m^2,$$
using $J_{-m}=(-1)^mJ_m$.

### P3.  Exercise 4.1.3 — The $\int\rho^{m+1}J_m$ integral  *(Wilcox 2e §4.16, p.180)*
Show
$$\int_0^a d\rho\,\rho^{m+1}J_m(k\rho)=\frac{a^{m+1}}{k}\bigl(J_{m+1}(ka)-\delta_{m,-1}\bigr).$$
*Answer:* immediate from the derivative identity
$\frac{d}{dt}[t^{m+1}J_{m+1}(t)]=t^{m+1}J_m(t)$; the $\delta_{m,-1}$ is the
lower boundary term $J_0(0)=1$.
*Check:* closed form vs Gauss–Legendre quadrature for $m=0,1,2,5$ **and**
$m=-1$ (`test_p3_rho_power_integral`).

**Solution.** From the series (4.8),
$\frac{d}{dt}\bigl[t^{m+1}J_{m+1}(t)\bigr]
=\frac{d}{dt}\sum_n\frac{(-1)^n t^{2m+2n+2}}{2^{m+1+2n}n!(m+n+1)!}
=t^{m+1}\sum_n\frac{(-1)^n(t/2)^{m+2n}}{n!(m+n)!}=t^{m+1}J_m(t)$.
Substituting $t=k\rho$ and integrating,
$$\int_0^a\rho^{m+1}J_m(k\rho)\,d\rho
=\frac{1}{k^{m+2}}\Bigl[t^{m+1}J_{m+1}(t)\Bigr]_0^{ka}
=\frac{a^{m+1}}{k}J_{m+1}(ka)-\lim_{t\to0}\frac{t^{m+1}J_{m+1}(t)}{k^{m+2}}.$$
For $m>-1$ the lower limit vanishes ($t^{m+1}J_{m+1}\sim t^{2m+2}$). For
$m=-1$ it is $J_0(0)=1$, giving $-1/k=-a^{m+1}\delta_{m,-1}/k$ — the quoted
Kronecker term. (Numerically: $J_{-1}=-J_1$ and $\int_0^aJ_1\,d\rho=(1-J_0(ka))/k$,
consistent.)

### P4.  Exercise 4.1.4 — The other two integral representations  *(Wilcox 2e §4.16, p.180)*
Starting from the characterizations already established (generating function
(4.7), representation (4.13)), verify
$$J_n(t)=\frac1{2\pi}\int_{-\pi}^{\pi}d\phi\,e^{i(t\sin\phi-n\phi)}\quad(4.15),
\qquad
J_n(t)=\frac1{\pi}\int_0^{\pi}d\phi\,\cos(t\sin\phi-n\phi)\quad(4.16).$$
*Answer:* (4.15) is (4.13) after the rotation $\phi\to\pi/2-\phi$ (which trades
$\cos$ for $\sin$ and cancels the $i^{-n}$); (4.16) is the real part of (4.15).
*Check:* both quadratures vs `scipy.jv` for $n=0,2,5$
(`test_p4_integral_representations`).

**Solution.** In (4.13) substitute $\phi=\pi/2-\psi$ (a shift plus reflection
of the periodic integrand, so the domain stays one full period):
$\cos\phi=\sin\psi$ and $e^{-in\phi}=e^{-in\pi/2}e^{in\psi}=i^{-n}e^{in\psi}$,
so
$$J_n=i^{-n}\!\int\frac{d\psi}{2\pi}e^{it\sin\psi}\,i^{-n}e^{in\psi}
=(-1)^n\!\int_{-\pi}^{\pi}\frac{d\psi}{2\pi}e^{i(t\sin\psi+n\psi)}.$$
Now let $\psi\to-\psi$: the integral becomes
$\int e^{-i(t\sin\psi-n\psi)}\frac{d\psi}{2\pi}$, whose value must equal its own
conjugate (swap back), i.e. it is real; and multiplying by
$(-1)^n=J_{-n}/J_n$ bookkeeping is avoided by noting the result equals
$\int e^{i(t\sin\psi-n\psi)}d\psi/2\pi$ directly — Eq. (4.15).
For (4.16): split $e^{i(\cdot)}=\cos(\cdot)+i\sin(\cdot)$ on $[-\pi,\pi]$.
$\sin(t\sin\phi-n\phi)$ is odd under $\phi\to-\phi$ and integrates to zero;
$\cos(t\sin\phi-n\phi)$ is even, so the half-range integral doubles:
$J_n=\frac1\pi\int_0^\pi\cos(t\sin\phi-n\phi)\,d\phi$.

### P5.  Exercise 4.2.1 — Bessel addition theorem and the 2-D delta  *(Wilcox 2e §4.16, pp.180–181)*
(a) Evaluate
$\int_0^{2\pi}\frac{d\alpha}{(2\pi)^2}\,e^{i\vec k_\perp\cdot(\vec x-\vec x')_\perp}$
two different ways ($\alpha$ = cylindrical angle of $\vec k$, book Fig. 4.6)
to establish the addition theorem
$$J_0(kD)=\sum_{m=-\infty}^{\infty}J_m(k\rho)J_m(k\rho')e^{im(\phi-\phi')},
\qquad D\equiv|(\vec x-\vec x')_\perp|$$
(the book's $\rho'=|\vec x_\perp|$ is a typo for $|\vec x'_\perp|$).
(b) Use (a) to show
$\int_0^\infty\frac{dk\,k}{2\pi}J_0(kD)=\frac1\rho\delta(\rho-\rho')\delta(\phi-\phi')$.
*Answer:* (a) the direct route gives $J_0(kD)/2\pi$ via (4.13) with $n=0$; the
expanded route gives the $m$ sum. (b) the $k$ integral is a delta family:
Gaussian-regulated it is $\frac1{4\pi p^2}e^{-D^2/4p^2}$, a unit-mass 2-D
delta as $p\to0$.
*Check:* series $=J_0(kD)$ on random geometry; Weber's regulated integral:
closed form $=$ quadrature $=$ Fourier–Bessel lattice; unit mass and $1/p^2$
concentration (`test_p5_addition_theorem`, `test_p5_completeness_delta`).

**Solution.** (a) *Directly:* $(\vec x-\vec x')_\perp$ has some azimuth
$\phi_D$, so $\vec k_\perp\cdot(\vec x-\vec x')_\perp=kD\cos(\alpha-\phi_D)$
and (4.13) with $n=0$ gives $\int_0^{2\pi}\frac{d\alpha}{2\pi}e^{ikD\cos(\alpha-\phi_D)}=J_0(kD)$;
the extra $1/2\pi$ tags along.
*Expanded:* write
$e^{i\vec k_\perp\cdot\vec x_\perp}e^{-i\vec k_\perp\cdot\vec x'_\perp}$ and
expand each factor with (4.14), $e^{ik\rho\cos(\phi-\alpha)}=\sum_mi^me^{im(\phi-\alpha)}J_m(k\rho)$:
$$\int_0^{2\pi}\frac{d\alpha}{2\pi}\sum_{m,m'}i^{m-m'}e^{im\phi-im'\phi'}
e^{-i(m-m')\alpha}J_m(k\rho)J_{m'}(k\rho')
=\sum_mJ_m(k\rho)J_m(k\rho')e^{im(\phi-\phi')}.$$
Equating the two evaluations proves the theorem.
(b) Multiply the theorem by $k/2\pi$ and integrate. With the Gaussian
regulator $e^{-p^2k^2}$, Weber's second exponential integral gives in closed
form
$$\int_0^\infty\frac{k\,dk}{2\pi}J_0(kD)e^{-p^2k^2}=\frac1{4\pi p^2}e^{-D^2/4p^2},$$
a normalized 2-D Gaussian of width $p\sqrt2$ centered at
$\vec x_\perp=\vec x'_\perp$: unit mass
$\int2\pi D\,dD\,(\cdot)=1$ for every $p$, peak $\propto1/p^2$. As $p\to0$
this is exactly $\delta^2\bigl((\vec x-\vec x')_\perp\bigr)
=\frac1\rho\delta(\rho-\rho')\delta(\phi-\phi')$ — the completeness relation
(4.39) resolved into azimuthal components.

### P6.  Exercise 4.3.1 — Normalization at zeros of $J_m'$  *(Wilcox 2e §4.16, p.181)*
For $\bar k_{mn}=y_{mn}/a$ with $J_m'(y_{mn})=0$, show
$$\int_0^a d\rho\,\rho\,[J_m(\bar k_{mn}\rho)]^2
=\frac{a^2}{2}\Bigl(1-\frac{m^2}{y_{mn}^2}\Bigr)[J_m(y_{mn})]^2,$$
using the method the book sketches after Eq. (4.52).
*Answer:* as stated; it is the Neumann-eigenfunction analog of the
$J_{m+1}^2$ normalization (4.58).
*Check:* quadrature vs closed form for $(m,n)$ up to $(5,4)$
(`test_p6_deriv_zero_normalization`).

**Solution.** Let $u(\rho)=J_m(\bar k\rho)$, which satisfies Bessel's equation
$(\rho u')'+(\bar k^2\rho-m^2/\rho)u=0$. Multiply by $2\rho u'$ and regroup
into a total derivative:
$$\frac{d}{d\rho}\Bigl[\rho^2u'^2+(\bar k^2\rho^2-m^2)u^2\Bigr]=2\bar k^2\rho u^2 .$$
Integrate from $0$ to $a$. At $\rho=0$ the bracket vanishes ($u\sim\rho^m$
kills $-m^2u^2$ and $\rho^2u'^2$ separately, including $m=0$). At $\rho=a$,
$u'(a)=\bar kJ_m'(y)=0$ by the choice of $\bar k$, leaving
$(y^2-m^2)J_m(y)^2$. Hence
$$2\bar k^2\int_0^a\rho\,u^2\,d\rho=(y^2-m^2)J_m(y)^2
\;\Longrightarrow\;
\int_0^a\rho\,u^2=\frac{a^2}{2}\Bigl(1-\frac{m^2}{y^2}\Bigr)J_m(y)^2 .$$

### P7.  Exercise 4.4.1 — Conducting wall in cylindrical coordinates  *(Wilcox 2e §4.16, pp.181–182)*
For the grounded infinite plane $z=0$ (charge in $z>0$; book Fig. 4.7), show
the reduced-Green-function method in cylindrical coordinates gives
$$G_D=4\int_0^\infty dk\,k\,g(k;z,z')\Bigl[\tfrac12J_0(k\rho)J_0(k\rho')
+\sum_{m\ge1}J_mJ_m'\cos m(\phi-\phi')\Bigr]
=2\int_0^\infty dk\,k\,g\,J_0(kD),$$
and find $g(k;z,z')$.
*Answer:* $g=\dfrac{e^{-k|z-z'|}-e^{-k(z+z')}}{2k}=\dfrac{\sinh(kz_<)\,e^{-kz_>}}{k}$
— the Ch. 3 result (3.30).
*Check:* $g$ vanishes at $z=0$, carries the unit $-dg/dz$ jump, is symmetric;
the assembled Hankel integral equals the image answer
$1/|\vec x-\vec x'|-1/|\vec x-\vec x''|$ to $10^{-6}$ (`test_p7_wall_green`).

**Solution.** Expand the transverse delta with the $m$-resolved completeness
(4.39) and the azimuthal exponentials:
$4\pi\delta^3=2\!\int_0^\infty\!k\,dk\sum_me^{im(\phi-\phi')}J_m(k\rho)J_m(k\rho')\,\delta(z-z')$
(Eq. 4.108). Seeking $G$ with the same transverse structure and a reduced
$g(k;z,z')$ turns $\nabla^2G=-4\pi\delta$ into the 1-D problem
$$\Bigl(k^2-\frac{\partial^2}{\partial z^2}\Bigr)g=\delta(z-z'),\qquad
g(0,z')=0,\quad g\to0\ (z\to\infty).$$
Homogeneous solutions $e^{\pm kz}$: take $\psi_1=\sinh kz$ (wall condition),
$\psi_2=e^{-kz}$ (decay). The Wronskian recipe (4.130) with unit jump
$-\partial_zg|^+_-=1$ gives $C=1/k$ ($W_z[\sinh kz,e^{-kz}]=-k$), so
$g=\sinh(kz_<)e^{-kz_>}/k$, which expands to
$\bigl(e^{-k|z-z'|}-e^{-k(z+z')}\bigr)/2k$ — visibly the free part minus its
mirror image. The $m$ sum collapses to $J_0(kD)$ by P5's addition theorem,
giving the second (Hankel) form; carrying out that integral term by term
(free + image, each a Lipschitz integral $\int J_0(kD)e^{-k\Delta}dk=1/\sqrt{D^2+\Delta^2}$)
reproduces the image Green function — the numeric check does exactly this
comparison.

### P8.  Exercise 4.4.2 — Conducting half-plane sheet: $\sin m\phi$ expansion  *(Wilcox 2e §4.16, p.182)*
A grounded conducting plate fills the $z$–$x$ plane; free space is $y>0$,
i.e. $0<\phi<\pi$ in cylindrical coordinates $(\rho,\phi,z)$. Show by the
reduced-Green-function technique that
$$G_D=4\int_0^\infty dk\sum_{m=1}^{\infty}J_m(k\rho)J_m(k\rho')
\sin(m\phi)\sin(m\phi')\,e^{k(z_<-z_>)}.$$
*Answer:* as stated — Dirichlet sine modes in $\phi$, free (Wronskian) $g$
in $z$.
*Check:* equals the image pair $1/|\vec x-\vec x'|-1/|\vec x-\vec x''|$
($\phi''=-\phi'$) on random points; vanishes at $\phi=0,\pi$
(`test_p8_halfplane_green`).

**Solution.** The wall now cuts the *azimuth*: Dirichlet conditions at
$\phi=0$ and $\phi=\pi$ select $\sin(m\phi)$, integer $m\ge1$, with
completeness $\delta(\phi-\phi')=\frac2\pi\sum_m\sin m\phi\sin m\phi'$ on
$(0,\pi)$. The radial delta stays $\int k\,dk\,J_mJ_m'$ (valid per $m$), and
$z$ is now the *unbounded* direction, so its reduced equation
$(k^2-\partial_z^2)g=\delta(z-z')$ with decay both ways has the free solution
$g=e^{-k|z-z'|}/2k$ (P7 without the wall term). Assembling with
$\nabla^2G=-4\pi\delta$:
$$G_D=4\pi\sum_m\frac2\pi\sin m\phi\sin m\phi'
\int_0^\infty k\,dk\,J_mJ_m'\,\frac{e^{-k|z-z'|}}{2k}
=4\int_0^\infty dk\sum_{m\ge1}J_mJ_m'\sin m\phi\sin m\phi'\,e^{k(z_<-z_>)} .$$
Physically the same object as the plane-image Green function — reflection
$y'\to-y'$ is $\phi'\to-\phi'$, and
$\sin m\phi\sin m\phi'=\tfrac12[\cos m(\phi-\phi')-\cos m(\phi+\phi')]$
is precisely (source) $-$ (image) of the full-space azimuthal kernel. The
test verifies the numerical identity.

### P9.  Exercise 4.4.3 — Parallel plates driven by a charged disk (Neumann data)  *(Wilcox 2e §4.16, pp.182–183)*
Parallel plates at $z=0$ and $z=d$ (book Fig. 4.8). The top plate carries the
Neumann data $E_z|_{z=d}=E_z^0$ (constant) on the disk $\rho<a$ and
$E_z|_{z=d}=0$ outside it.
(a) With the bottom plate also Neumann, $E_z|_{z=0}=0$, show that (up to a
constant)
$$\Phi(\rho,z)=-aE_z^0\int_0^\infty\frac{dk}{k}J_0(k\rho)J_1(ka)
\frac{\cosh(kz)}{\sinh(kd)} .$$
(b) With the bottom plate grounded instead, $\Phi|_{z=0}=0$, show
$$\Phi(\rho,z)=-aE_z^0\int_0^\infty\frac{dk}{k}J_0(k\rho)J_1(ka)
\frac{\sinh(kz)}{\cosh(kd)} .$$
*Answer:* as stated. (In (a) the $k\to0$ end of the integral is
logarithmically divergent — an infinite additive *constant*, reflecting that a
pure-Neumann potential is defined only up to a constant; every field is
finite.)
*Check:* both forms are harmonic in the gap; $E_z(z{=}0)=0$ (a) /
$\Phi(z{=}0)=0$ (b); $-\partial_z\Phi\to E_z^0$ on the top disk and $\to0$
off it ($e^{-\epsilon k}$-regulated, Richardson $\epsilon\to0$)
(`test_p9_capacitor_disk`).

**Solution.** No volume charge, so the Neumann representation (2.103) leaves
only the surface term $\Phi=\frac1{4\pi}\oint G_N\,\partial_{n'}\Phi\,da'+\langle\Phi\rangle$.
Build $G_N$ for the gap by the reduced method (P7 with Neumann walls):
$\psi_1=\cosh kz$, $\psi_2=\cosh k(d-z)$, Wronskian $=k\sinh(kd)$, so
$g_N=\cosh(kz_<)\cosh(k(d-z_>))/(k\sinh kd)$, and
$G_N=2\int k\,dk\,J_0(kD)\,g_N+\dots$ (azimuthally symmetric part suffices —
the data is axisymmetric). On the top plate the *outward* normal is $+\hat z$
and $\partial_{n'}\Phi=\partial_z\Phi|_{z'=d}=-E_z^0$ on the disk. The
$\phi'$ integral gives $2\pi J_0(k\rho)J_0(k\rho')$ (addition theorem) and
the radial integral is P3 with $m=0$:
$\int_0^a\rho'J_0(k\rho')d\rho'=aJ_1(ka)/k$. With
$g_N(z,z'{=}d)=\cosh(kz)/(k\sinh kd)$,
$$\Phi=\frac{-E_z^0}{4\pi}\,2\pi\cdot2\int_0^\infty k\,dk\,J_0(k\rho)\frac{aJ_1(ka)}{k}
\frac{\cosh kz}{k\sinh kd}
=-aE_z^0\int_0^\infty\frac{dk}kJ_0(k\rho)J_1(ka)\frac{\cosh kz}{\sinh kd}.$$
(b) Swapping the bottom BC changes only the reduced function:
$\psi_1=\sinh kz$ (Dirichlet at 0), $\psi_2=\cosh k(d-z)$ (Neumann at $d$),
$W=-k\cosh(kd)$, so $g(z,d)=\sinh(kz)/(k\cosh kd)$ — the quoted mixed form.
*Consistency:* $-\partial_z\Phi|_{z=d}=aE_z^0\int dk\,J_0(k\rho)J_1(ka)=E_z^0\,\theta(a-\rho)$
(the classic discontinuous Weber–Schafheitlin integral) — the imposed plate
data, which the test recovers numerically by regularization.

### P10.  Exercise 4.4.4 — Capped half-infinite cylinder  *(Wilcox 2e §4.16, p.183)*
Find $G_D$ inside the half-infinite conducting cylinder $\rho<a$, $z>0$,
closed by a conducting cap at $z=0$ (all surfaces grounded), by the reduced
Green function technique.
*Answer:*
$$G_D=2\sum_{m=-\infty}^{\infty}\sum_{n=1}^{\infty}e^{im(\phi-\phi')}
\mathcal J_{1m}(k_{mn}\rho)\,\mathcal J_{1m}(k_{mn}\rho')\,
\frac{\sinh(k_{mn}z_<)\,e^{-k_{mn}z_>}}{k_{mn}},\qquad k_{mn}=\frac{x_{mn}}{a}.$$
*Check:* vanishes on the cap and the side wall; symmetric; equals the
independent construction (infinite-cylinder $G$ from P16's $\rho$-reduced
$g$, minus its image reflected through the cap) to $2\times10^{-5}$
(`test_p10_capped_cylinder_green`).

**Solution.** The transverse (bounded) directions get the discrete complete
set: $e^{im\phi}/\sqrt{2\pi}$ in azimuth and the Fourier–Bessel functions
$\mathcal J_{1m}(k_{mn}\rho)$, which obey Dirichlet at $\rho=a$
($J_m(x_{mn})=0$) with completeness (4.71)
$\sum_n\mathcal J_{1m}(k_{mn}\rho)\mathcal J_{1m}(k_{mn}\rho')=\delta(\rho-\rho')/\rho$.
The remaining $z$ problem is P7's half-line equation
$(k_{mn}^2-\partial_z^2)g=\delta(z-z')$, $g(0)=0$, $g(\infty)=0$, so
$g=\sinh(k z_<)e^{-kz_>}/k$ with $k=k_{mn}$. Assembling
($4\pi\times\frac1{2\pi}=2$):
$$G_D=2\sum_{m,n}e^{im\Delta\phi}\,\mathcal J_{1m}\mathcal J_{1m}'\,
\frac{\sinh(k_{mn}z_<)e^{-k_{mn}z_>}}{k_{mn}} .$$
Every factor is manifestly zero on its wall. The check exploits uniqueness
the other way round: the same region is (infinite cylinder) minus (mirror
through $z=0$), so $G_D$ must equal
$G_{\rm cyl}(\Delta z)-G_{\rm cyl}(z+z')$ built from the completely
independent $\rho$-reduced representation (4.122)/P16 — the two expansions
agree numerically, certifying both.

### P11.  Exercise 4.6.1 — Finite-domain completeness limits onto the Hankel integral  *(Wilcox 2e §4.16, p.183)*
The chapter asserts that the infinite-domain completeness relation (4.39),
$\int_0^\infty k\,dk\,J_\nu(k\rho)J_\nu(k\rho')=\delta(\rho-\rho')/\rho$, is
the $a\to\infty$ limit of the finite-domain eigen-sum (4.71),
$\sum_n\mathcal J_{1\nu}(k_{\nu n}\rho)\mathcal J_{1\nu}(k_{\nu n}\rho')=\delta(\rho-\rho')/\rho$.
Demonstrate the consistency using the large-$n$ zero asymptotics (4.98),
$x_{mn}\simeq(n+\tfrac m2-\tfrac14)\pi$.
*Answer:* with $k_n=x_{mn}/a$ the eigenvalues become dense,
$\Delta k=\pi/a$, and the normalization $2/[aJ_{m+1}(x_{mn})]^2\to\pi k_n/a$
turns the sum into the Riemann sum of $\int k\,dk\,J_mJ_m'$.
*Check:* zero asymptotics vs `jn_zeros` (residual = McMahon's next order);
Gaussian-regulated: the eigen-lattice sum equals Weber's closed form once $a$
covers the test function, with the wall felt exponentially at small $a$
(`test_p11_zero_asymptotics`, `test_p11_completeness_limit`).

**Solution.** Fix $m$ and write the $n$-th term of (4.71) with weight
$w_n=2/[aJ_{m+1}(x_{mn})]^2$. At a zero of $J_m$ the asymptotic amplitude
form $J_{m+1}(x)\simeq\sqrt{2/\pi x}\,|\!\cos(\cdot)|=\sqrt{2/\pi x_{mn}}$
(the cosine is $\pm1$ at the partner phase), so
$$w_n\simeq\frac{2}{a^2}\,\frac{\pi x_{mn}}{2}\cdot\frac1{1}\cdot\frac1{a^{-1}}
\Big/ a\;=\;\frac{\pi k_n}{a},$$
i.e. $w_n=\pi k_n/a$ with $k_n=x_{mn}/a$. By (4.98) successive zeros are
spaced $\Delta x=\pi$, so $\Delta k=\pi/a$ and
$$\sum_n w_nJ_m(k_n\rho)J_m(k_n\rho')
=\sum_n \Delta k\;k_n\,J_m(k_n\rho)J_m(k_n\rho')
\xrightarrow[a\to\infty]{}\int_0^\infty k\,dk\,J_mJ_m',$$
which is (4.39). The numeric check smears both sides with the Gaussian
$e^{-p^2k^2}$: the lattice sum then equals Weber's closed form
$\frac1{2p^2}e^{-(\rho^2+\rho'^2)/4p^2}I_\nu(\rho\rho'/2p^2)$ to machine
precision once $a$ exceeds the Gaussian support, the small-$a$ deficit dying
like the image term $e^{-(2a-\rho-\rho')^2/4p^2}$.

### P12.  Exercise 4.6.2 — Grounded caps, side at $V$  *(Wilcox 2e §4.16, pp.183–184)*
A right circular cylinder of radius $a$ and height $L$ (book Fig. 4.9) has
both caps ($z=0$ and $z=L$) grounded and the side wall $\rho=a$ (insulated
from the caps by narrow gaps) at constant potential $V$. Find
$\Phi(\rho,\phi,z)$ inside.
*Answer:*
$$\Phi=\frac{4V}{\pi}\sum_{n\ {\rm odd}}\frac1n\,
\frac{I_0(n\pi\rho/L)}{I_0(n\pi a/L)}\,\sin\frac{n\pi z}{L}.$$
*Check:* vanishes on both caps; $\to V$ on the wall (2×10⁻³ with $10^5$
terms, Gibbs-limited); harmonic (FD Laplacian $<10^{-5}$); matches a sparse
finite-difference solve of the axisymmetric Laplace problem to $3\times10^{-3}$
(`test_p12_cylinder_side_at_V`).

**Solution.** Grounded caps make $z$ the oscillatory direction:
$Z_n=\sin(n\pi z/L)$, forcing the separation constant sign that turns the
radial equation into the *modified* Bessel equation (4.92); regularity at
$\rho=0$ selects $I_\nu$, and axisymmetric data ($V$ independent of $\phi$)
kills all but $\nu=0$:
$$\Phi=\sum_{n\ge1}A_n\,I_0\!\Bigl(\frac{n\pi\rho}{L}\Bigr)\sin\frac{n\pi z}{L}.$$
The wall condition $\Phi(a,z)=V$ is a sine expansion of a constant:
$A_nI_0(n\pi a/L)=\frac2L\int_0^LV\sin\frac{n\pi z}L\,dz=\frac{2V}{n\pi}\bigl(1-(-1)^n\bigr)$,
i.e. $4V/n\pi$ for odd $n$, zero for even. Hence the quoted series. (The
code evaluates the $I_0$ ratio with scaled `ive` to avoid overflow at large
$n\pi a/L$.) Uniqueness is exercised numerically: an independent
finite-difference solution of the same boundary-value problem agrees
pointwise.

### P13.  Exercise 4.7.1 — Variational capacitance of the charged disk  *(Wilcox 2e §4.16, p.184)*
(a) Combine the variational principle (3.144), $C^{-1}[\sigma]=2W[\sigma]/Q^2$,
with the cylindrical Coulomb expansion (4.120) to show that a thin disk of
radius $a$ carrying axisymmetric surface density $\sigma(\rho)$ (total $Q$)
has
$$C^{-1}[\sigma]=\frac{4\pi^2}{Q^2}\int_0^\infty dk
\Bigl[\int_0^a d\rho\,\rho\,J_0(k\rho)\,\sigma(\rho)\Bigr]^2 .$$
(b) With the trial family $\sigma=A+B(\rho/a)^2$, establish the bound
$C>0.6213\,a$, and compare with the exact $C=\frac2\pi a=0.6366\,a$
(Ex. 2.6.1).
*Answer:* (a) as stated; (b) optimizing $\beta=B/A$ gives
$C_{\max}=0.62126\,a$ at $\beta\simeq7$ — density *growing* toward the rim,
as the exact $\sigma\propto(a^2-\rho^2)^{-1/2}$ does.
*Check:* $\beta=0$ reproduces the uniform-disk value $3\pi a/16=0.58905a$
exactly; optimized bound $>0.62125a$ and $<2a/\pi$; $\beta^*>0$
(`test_p13_disk_variational`).

**Solution.** (a) Put both points of
$W=\frac12\int\!\!\int\sigma\sigma'/|\vec x-\vec x'|$ on the plane
$z=z'=0$ and insert (4.120): $e^{-k(z_>-z_<)}\to1$, and the $\phi,\phi'$
integrals of $e^{im(\phi-\phi')}$ keep only $m=0$, each giving $2\pi$:
$$W=\frac12\int_0^\infty dk\,(2\pi)^2\Bigl[\int_0^a\rho\,d\rho\,J_0(k\rho)\sigma\Bigr]^2 ,$$
so $C^{-1}=2W/Q^2$ is the quoted functional — every trial density gives a
*lower* bound on $C$ (Thompson, §3.10).
(b) The two radial integrals are P3 closed forms:
$\int_0^a\rho J_0=aJ_1(t)/k$ and, integrating $\rho^3J_0$ by parts with the
same identity, $\int_0^a\rho(\rho/a)^2J_0=\frac ak\bigl(J_1(t)-\tfrac{2J_2(t)}{t}\bigr)$,
$t=ka$. With $Q=\pi a^2A(1+\beta/2)$, $C(\beta)$ is a ratio of quadratics in
$\beta$; numerical maximization gives $C=0.62126\,a$ at $\beta=7.0$ —
matching the book's $0.6213$ and safely below the exact $2a/\pi$. The
uniform member $\beta=0$ lands on $3\pi a/16$, the same number the Ch. 3
notes-check produced by real-space quadrature — two independent
representations of one variational value.

### P14.  Exercise 4.7.2 — Neumann patch on a half-space  *(Wilcox 2e §4.16, pp.184–185)*
The half-space $z>0$ is bounded by a Neumann surface: on the disk $\rho<a$
of the plane $z=0$, $-\partial\Phi/\partial z=E_z^0$ (constant), and
$E_z=0$ on the rest of the plane. Using the Neumann Green function and
(4.120), show
$$\Phi(\rho,z)=E_z^0\,a\int_0^\infty\frac{dk}{k}\,J_0(k\rho)\,J_1(ka)\,e^{-kz}.$$
*Answer:* as stated; on the axis it sums to
$\Phi(0,z)=E_z^0(\sqrt{a^2+z^2}-z)$, and far away
$\Phi\to E_z^0a^2/2z$ (the monopole of the patch flux).
*Check:* axis quadrature vs closed form ($10^{-7}$); $-\partial_z\Phi\to E_z^0$
on the patch and $\to0$ off it (Richardson in $z$); far-field monopole
(`test_p14_patch_neumann`).

**Solution.** The half-space Neumann function adds the *same-sign* image:
reduced $g_N=\bigl(e^{-k|z-z'|}+e^{-k(z+z')}\bigr)/2k$, so on the wall
$g_N(z,0)=e^{-kz}/k$. With no volume charge, (2.103) leaves
$\Phi=\frac1{4\pi}\oint G_N\,\partial_{n'}\Phi\,da'$; the outward normal of
the region is $-\hat z$, so on the patch
$\partial_{n'}\Phi=-\partial_{z'}\Phi=E_z^0$. The azimuthal integral gives
$2\pi J_0(k\rho)J_0(k\rho')$ and the radial one $aJ_1(ka)/k$ (P3):
$$\Phi=\frac{E_z^0}{4\pi}\,2\pi\cdot2\int_0^\infty k\,dk\,
J_0(k\rho)\,\frac{aJ_1(ka)}{k}\,\frac{e^{-kz}}{k}
=E_z^0a\int_0^\infty\frac{dk}kJ_0J_1(ka)e^{-kz}.$$
On the axis ($J_0=1$) the integral is elementary:
$\int_0^\infty J_1(ka)e^{-kz}dk/k=(\sqrt{a^2+z^2}-z)/a$. Gauss's law
sanity check: the patch injects flux $\pi a^2E_z^0$ into the half-space, so
far away $\Phi\simeq(\pi a^2E_z^0/2\pi)/r=E_z^0a^2/2r$ — the $1/2$ because
the flux fills a half-space; the closed form's large-$z$ expansion agrees.

### P15.  Exercise 4.7.3 — Wronskians of Bessel pairs  *(Wilcox 2e §4.16, p.185)*
(a) Using the differential equation
$\bigl[\frac{d^2}{dt^2}+\frac1t\frac d{dt}-\frac{\nu^2}{t^2}+1\bigr]J_{\pm\nu}=0$,
show $W_t[J_\nu,J_{-\nu}]=C/t$ with $C$ constant.
(b) Using the large-$t$ asymptotics, evaluate
$W_t[J_\nu,J_{-\nu}]=-\dfrac{2\sin\nu\pi}{\pi t}$ and, for integer $m$,
$W_t[J_m,N_m]=\dfrac{2}{\pi t}$.
*Answer:* as stated — these are the constants that normalize every reduced
Green function of the chapter.
*Check:* $t\,W$ constant over $t$ (spread $<10^{-7}$) and equal to the closed
forms, by finite-difference Wronskians for $\nu=0.3,0.6,1.7$ and $m=0,2,5$
(`test_p15_wronskians`).

**Solution.** (a) With $u=J_\nu$, $v=J_{-\nu}$ (same equation, same $\nu^2$),
$$W'=uv''-vu''=-\frac1t\,(uv'-vu')=-\frac Wt
\quad\Longrightarrow\quad (tW)'=0,\ \ W=\frac Ct .$$
(b) Evaluate $C$ where the functions are simple:
$J_{\pm\nu}(t)\to\sqrt{2/\pi t}\cos(t\mp\nu\pi/2-\pi/4)$. Then
$$W\to\frac{2}{\pi t}\bigl[\cos\theta_+(-\sin\theta_-)-\cos\theta_-(-\sin\theta_+)\bigr]
=\frac{2}{\pi t}\sin(\theta_+-\theta_-)=-\frac{2\sin\nu\pi}{\pi t},$$
where $\theta_\pm=t\mp\nu\pi/2-\pi/4$ and the $O(t^{-3/2})$ derivative
corrections drop out of the constant. For the Neumann function use its
definition $N_\nu=(J_\nu\cos\nu\pi-J_{-\nu})/\sin\nu\pi$:
$$W[J_\nu,N_\nu]=\frac{\cos\nu\pi\,W[J_\nu,J_\nu]-W[J_\nu,J_{-\nu}]}{\sin\nu\pi}
=\frac{2\sin\nu\pi/\pi t}{\sin\nu\pi}=\frac2{\pi t},$$
finite as $\nu\to m$ — the integer-order limit quoted.

### P16.  Exercise 4.7.4 — Reduced Green functions of the conducting cylinder  *(Wilcox 2e §4.16, pp.185–186)*
An infinite grounded conducting cylinder of radius $a$ lies along $z$ (book
Fig. 4.10). Assume
$$G_D=4\pi\sum_{m}\frac{e^{im(\phi-\phi')}}{2\pi}\,\frac1\pi\int_0^\infty
dk\,\cos[k(z-z')]\,g_m(k;\rho,\rho'),$$
with the matching delta expansion
$4\pi\delta^3=4\pi\sum_m\frac{e^{im\Delta\phi}}{2\pi}\frac1\pi\int dk\cos(k\Delta z)\frac{\delta(\rho-\rho')}\rho$.
Find the reduced Green function for (a) the exterior and (b) the interior.
*Answer:* with $W_t[I_m,K_m]=-1/t$ fixing $C=1$,
$$g_m^{\rm out}=\Bigl[I_m(k\rho_<)-K_m(k\rho_<)\frac{I_m(ka)}{K_m(ka)}\Bigr]K_m(k\rho_>),
\qquad
g_m^{\rm in}=I_m(k\rho_<)\Bigl[K_m(k\rho_>)-I_m(k\rho_>)\frac{K_m(ka)}{I_m(ka)}\Bigr].$$
*Check:* wall zeros, decay/regularity, the $-1/\rho'$ jump; free-space member
$I_m(k\rho_<)K_m(k\rho_>)$ assembles to $1/|\vec x-\vec x'|$ ($10^{-4}$);
interior $G$ vanishes on the wall (`test_p16_cylinder_reduced_g`).

**Solution.** Substituting the ansatz into $\nabla^2G=-4\pi\delta$ and
matching the delta expansion mode by mode gives the radial problem (4.123),
$$\frac1\rho\frac d{d\rho}\Bigl(\rho\frac{dg_m}{d\rho}\Bigr)
-\Bigl(k^2+\frac{m^2}{\rho^2}\Bigr)g_m=-\frac{\delta(\rho-\rho')}{\rho},$$
whose homogeneous solutions are $I_m(k\rho)$, $K_m(k\rho)$. The jump is
$dg/d\rho|^+_-=-1/\rho'$, so in the recipe (4.130) $D=-1/\rho$ while
$W_\rho[\psi_1,\psi_2]=k\,W_t[I_m,K_m]\cdot(\text{combo})=-(\text{combo})/\rho$:
the constant is $C=1$ whenever $\psi_{1,2}$ are *unit-coefficient* in the
$I$, $K$ that carry the Wronskian.
(a) Exterior $(a<\rho<\infty)$: $\psi_1$ must vanish at $a$ —
$\psi_1=I_m(k\rho)-K_m(k\rho)I_m(ka)/K_m(ka)$; $\psi_2=K_m(k\rho)$ decays.
(b) Interior: $\psi_1=I_m(k\rho)$ is the regular one;
$\psi_2=K_m(k\rho)-I_m(k\rho)K_m(ka)/I_m(ka)$ vanishes at $a$. In both, the
admixed term contributes nothing to the Wronskian, so $C=1$ and
$g=\psi_1(\rho_<)\psi_2(\rho_>)$ — the two quoted forms. Dropping the wall
($a\to\infty$ or $a\to0$) leaves $g=I_m(k\rho_<)K_m(k\rho_>)$, Eq. (4.125)
with $A=1$: assembled through the $\cos k\Delta z$ integral it must equal
$1/|\vec x-\vec x'|$, which the test verifies — that is the Wronskian
derivation of the cylindrical free-space Green function.

### P17.  Exercise 4.7.5 — Toroid of rectangular cross-section  *(Wilcox 2e §4.16, pp.186–187)*
A conducting toroidal box (book Fig. 4.11): height $L$ (caps $z=0,L$), inner
radius $a$, outer radius $b$, all grounded. Construct the interior Dirichlet
Green function in cylindrical coordinates, taking $\rho$ as the
non-oscillatory direction (the book's hint).
*Answer:* with $k_n=n\pi/L$ and
$\psi_1=I_m(k\rho)K_m(ka)-K_m(k\rho)I_m(ka)$ (zero at $a$),
$\psi_2=I_m(k\rho)K_m(kb)-K_m(k\rho)I_m(kb)$ (zero at $b$),
$$G_D=\frac4L\sum_{m=-\infty}^\infty\sum_{n=1}^\infty
e^{im(\phi-\phi')}\sin(k_nz)\sin(k_nz')\,
\frac{\psi_1(k_n\rho_<)\,\psi_2(k_n\rho_>)}{I_m(k_na)K_m(k_nb)-K_m(k_na)I_m(k_nb)} .$$
*Check:* reduced $g$ vanishes at both radii with the $-1/\rho'$ jump;
assembled $G$ vanishes on all four walls, is symmetric, and satisfies
$G\,R\to1$ near the source (Richardson in the offset)
(`test_p17_toroid_green`).

**Solution.** Both $z$ (grounded caps) and $\phi$ (periodic) are oscillatory;
$\rho$ carries the delta:
$$\delta^3=\frac{\delta(\rho-\rho')}\rho\cdot\frac1{2\pi}\sum_me^{im\Delta\phi}
\cdot\frac2L\sum_n\sin k_nz\,\sin k_nz' .$$
Each $(m,n)$ mode obeys the *modified* radial equation (4.123) with
$k=k_n$ — modified because the $z$ eigenvalue entered with the sign that
makes $e^{\pm ikz}\to\sin$. Two-wall Dirichlet conditions pick the quoted
$\psi_1$, $\psi_2$ (each a $I,K$ combination vanishing at its wall). Their
Wronskian: bilinearity and $W[I,K]=-1/\rho$ give
$$W_\rho[\psi_1,\psi_2]
=\bigl[I_m(ka)K_m(kb)-K_m(ka)I_m(kb)\bigr]\cdot\frac{1}{\rho}\times(-1)^{\#}
=\frac{K_m(ka)I_m(kb)-I_m(ka)K_m(kb)}{\rho},$$
so $C=D/W=(-1/\rho)/W$ gives the quoted denominator. Assembling with the
mode weights, $4\pi\cdot\frac1{2\pi}\cdot\frac2L=\frac4L$. (The code
evaluates everything in `ive`/`kve` scaled form and falls back to the exact
$m\gg kb$ power law — the 2-D annulus modes of P23 — where the scaled
products underflow.)

### P18.  Exercise 4.7.6 — The cylindrical Coulomb expansion at work  *(Wilcox 2e §4.16, p.187)*
(a) Given the representation (4.120),
$$\frac1{|\vec x-\vec x'|}=\int_0^\infty dk\sum_{m=-\infty}^\infty
e^{im(\phi-\phi')}J_m(k\rho)J_m(k\rho')\,e^{-k(z_>-z_<)},$$
verify explicitly that $\nabla^2|\vec x-\vec x'|^{-1}=-4\pi\delta^3$, using
the delta expansion (4.108).
(b) Show that averaging $1/|\vec x-\vec x'|$ over a disk of radius $a$
(source coordinates $\rho'\le a$, all $\phi'$, fixed $z'$) gives
$$\int_0^a\rho'd\rho'\int_0^{2\pi}\frac{d\phi'}{|\vec x-\vec x'|}
=2\pi a\int_0^\infty\frac{dk}kJ_0(k\rho)J_1(ka)e^{-k|z-z'|}.$$
*Answer:* (a) each mode is annihilated by the operator except for the kink of
$e^{-k|z-z'|}$, whose $-2k\,\delta(z-z')$ reassembles (4.108); (b) as stated.
*Check:* (4.120) equals $1/R$ on random points ($10^{-8}$); the disk integral:
2-D quadrature vs the closed $k$-form ($10^{-7}$)
(`test_p18_coulomb_cylJ`, `test_p18_disk_source_integral`).

**Solution.** (a) Apply the cylindrical Laplacian mode by mode. The
$\rho,\phi$ part of each term satisfies Bessel's equation:
$\bigl[\frac1\rho\partial_\rho(\rho\partial_\rho)-\frac{m^2}{\rho^2}\bigr]J_m(k\rho)e^{im\Delta\phi}
=-k^2J_me^{im\Delta\phi}$. The $z$ factor satisfies
$\partial_z^2e^{-k|z-z'|}=k^2e^{-k|z-z'|}-2k\,\delta(z-z')$ — the $+k^2$
cancels the $-k^2$, leaving only the kink term:
$$\nabla^2\frac1R=-2\delta(z-z')\int_0^\infty k\,dk\sum_me^{im\Delta\phi}J_mJ_m'
=-4\pi\,\delta^3(\vec x-\vec x'),$$
where the last equality is exactly the expansion (4.108) of the
three-dimensional delta. (b) Integrate (4.120) over the disk: the $\phi'$
integral kills all $m\ne0$ (factor $2\pi\delta_{m0}$), and the radial
integral is P3's $m=0$ case, $\int_0^a\rho'J_0(k\rho')d\rho'=aJ_1(ka)/k$:
$$\int_{\rm disk}\frac{da'}{R}
=2\pi\int_0^\infty dk\,J_0(k\rho)\,\frac{aJ_1(ka)}k\,e^{-k|z-z'|},$$
the quoted form — the potential of a uniformly charged disk (unit surface
density), and the workhorse behind P9, P13, P14.

### P19.  Exercise 4.8.1 — Summing the wedge Green function  *(Wilcox 2e §4.16, pp.187–188)*
Eq. (4.143) gives the open-wedge (angle $\beta$, grounded flats, line-charge
source; book Fig. 4.12) Dirichlet Green function as
$$G_D=\sum_{n=1}^{\infty}\frac4n\Bigl(\frac{\rho_<}{\rho_>}\Bigr)^{\gamma}
\sin\frac{n\pi\phi}{\beta}\sin\frac{n\pi\phi'}{\beta},\qquad\gamma=\frac{n\pi}\beta.$$
Using the §3.9 summation method, sum it to the closed form
$$G_D=\ln\!\left[\frac{1+u^{2q}-2u^{q}\cos\bigl(q(\phi+\phi')\bigr)}
{1+u^{2q}-2u^{q}\cos\bigl(q(\phi-\phi')\bigr)}\right],
\qquad u=\frac{\rho_<}{\rho_>},\ q=\frac\pi\beta,$$
and confirm that $\beta=\pi/2$ recovers the quadrant image answer of
Ex. 3.1.3.
*Answer:* as stated.
*Check:* series $=$ closed form ($10^{-9}$, three $\beta$'s); zero on both
flats; $\beta=\pi/2$ equals the $\rho^4$-log quadrant formula
(`test_p19_wedge_closed_form`).

**Solution.** Use $\sin A\sin B=\tfrac12[\cos(A-B)-\cos(A+B)]$ and the
elementary complex sum $\sum_{n\ge1}\frac{x^n}n\cos n\theta
=-\tfrac12\ln(1-2x\cos\theta+x^2)$ (real part of $-\ln(1-xe^{i\theta})$,
$0\le x<1$). With $x=u^{q}$ and $\theta_\mp=q(\phi\mp\phi')$:
$$G_D=\sum_n\frac2n u^{nq}\bigl[\cos n\theta_--\cos n\theta_+\bigr]
=\ln\frac{1-2u^q\cos\theta_++u^{2q}}{1-2u^q\cos\theta_-+u^{2q}},$$
the quoted form. Both flats are grounded on inspection: at $\phi=0$ or
$\phi=\beta$, $\cos\theta_+=\cos\theta_-$ and the ratio is 1.
For $\beta=\pi/2$ ($q=2$) multiply numerator and denominator by $\rho_>^4$:
$$G_D=\ln\frac{\rho^4+\rho'^4-2\rho^2\rho'^2\cos2(\phi+\phi')}
{\rho^4+\rho'^4-2\rho^2\rho'^2\cos2(\phi-\phi')},$$
exactly the four-image quadrant Green function of Ex. 3.1.3
(`~MACRO_EM-03` P3) — the $w\mapsto w^{q}$ conformal unfolding in
Green-function form.

### P20.  Exercise 4.8.2 — Closed wedge with two grounded arcs  *(Wilcox 2e §4.16, p.188)*
The vacuum wedge of opening $\beta$ is now closed by grounded circular arcs
at $\rho=a$ and $\rho=b$ ($a<b$; book Fig. 4.13). Find $G_D$ for a unit line
charge by the reduced Green function method.
*Answer:* $G_D=\dfrac{8\pi}\beta\sum_n\sin\frac{n\pi\phi}\beta\sin\frac{n\pi\phi'}\beta\,g_n(\rho,\rho')$
(4.133) with
$$g_n=\frac{(\rho_</\rho_>)^{\gamma}+\bigl(a^2\rho_>/b^2\rho_<\bigr)^{\gamma}
-\bigl(\rho_<\rho_>/b^2\bigr)^{\gamma}-\bigl(a^2/\rho_<\rho_>\bigr)^{\gamma}}
{2\gamma\,\bigl[1-(a/b)^{2\gamma}\bigr]},\qquad\gamma=\frac{n\pi}\beta .$$
*Check:* $g_n$ vanishes at both arcs and carries the $-1/\rho'$ jump; the
assembled sum vanishes on all four boundaries, is symmetric, and
$a\to0$ recovers the outer-arc-only wedge (4.142)
(`test_p20_wedge_annulus`).

**Solution.** The angular delta on $(0,\beta)$ expands as (4.132), and each
$n$ mode obeys the $k=0$ radial equation (4.134),
$\frac1\rho\frac d{d\rho}(\rho\frac{dg_n}{d\rho})-\frac{\gamma^2}{\rho^2}g_n=-\frac{\delta(\rho-\rho')}\rho$,
with power-law homogeneous solutions $\rho^{\pm\gamma}$ (4.136). Build the
two-wall solutions
$$\psi_1=\Bigl(\frac\rho a\Bigr)^{\gamma}-\Bigl(\frac a\rho\Bigr)^{\gamma}
\ \ (\psi_1(a)=0),\qquad
\psi_2=\Bigl(\frac\rho b\Bigr)^{\gamma}-\Bigl(\frac b\rho\Bigr)^{\gamma}
\ \ (\psi_2(b)=0).$$
Their Wronskian: $W_\rho[\rho^{\gamma},\rho^{-\gamma}]=-2\gamma/\rho$, so by
bilinearity
$W_\rho[\psi_1,\psi_2]=\frac{2\gamma}\rho\bigl[(b/a)^{\gamma}-(a/b)^{\gamma}\bigr]$.
With $D=-1/\rho$ the recipe gives
$C=-1/\bigl(2\gamma[(b/a)^\gamma-(a/b)^\gamma]\bigr)$, and expanding
$C\,\psi_1(\rho_<)\psi_2(\rho_>)$ produces the four-power form quoted
(dividing through by $(b/a)^\gamma$ to make every base $\le1$ — the
numerically stable grouping the code uses). As $a\to0$ only the first and
third powers survive,
$g_n\to\frac1{2\gamma}u^\gamma[1-(\rho_>/b)^{2\gamma}]$ — Eq. (4.141) with
outer wall $b$, whose $b\to\infty$ limit is P19's open wedge.

### P21.  Exercise 4.8.3 — Line charge inside a conducting cylinder  *(Wilcox 2e §4.16, pp.188–189)*
Show (reduced Green function or otherwise) that a unit line charge inside the
grounded cylinder $\rho=a$ has
$$G_D=-\ln\frac{\rho_>^2}{a^2}
+2\sum_{m=1}^\infty\frac{\cos m(\phi-\phi')}m\,\rho_<^m
\Bigl(\frac1{\rho_>^m}-\frac{\rho_>^m}{a^{2m}}\Bigr).$$
*Extra:* sum the series (§3.9 method) into the image form of Ex. 3.3.5(b).
*Answer:* series as stated; the sum is
$G_D=\ln\dfrac{a^4+\rho^2\rho'^2-2a^2\rho\rho'\cos\Delta\phi}
{a^2\,(\rho^2+\rho'^2-2\rho\rho'\cos\Delta\phi)}$ — source line plus opposite
image line at the inverse point $a^2/\rho'$.
*Check:* series $=$ image form ($10^{-11}$); both vanish at $\rho=a$
(`test_p21_cylinder_2d_series`).

**Solution.** Full azimuth: modes $e^{im\Delta\phi}$, radial equation (4.134)
with $\gamma\to m$ and, for $m=0$, solutions $\{1,\ln\rho\}$. Regularity at
the axis and $g(a)=0$ give
$$g_0=-\ln\frac{\rho_>}a,\qquad
g_m=\frac{\rho_<^m}{2m}\Bigl(\frac1{\rho_>^m}-\frac{\rho_>^m}{a^{2m}}\Bigr)\ (m\ge1),$$
each with the $-1/\rho'$ jump ($W[\ln\rho,1]=-1/\rho$;
$W[\rho^m,\rho^{-m}]=-2m/\rho$). Assembling
$G=2g_0+4\sum_{m\ge1}\cos m\Delta\phi\,g_m$ (the $4\pi\delta$ normalization
with $\delta(\phi)=\frac1{2\pi}\sum e^{im\Delta\phi}$) gives the quoted
series. *Extra:* apply $\sum\frac{x^m}m\cos m\theta=-\frac12\ln(1-2x\cos\theta+x^2)$
twice, with $x_1=\rho_</\rho_>$ (free + ) and $x_2=\rho_<\rho_>/a^2$ (image $-$):
$$G_D=-\ln\frac{\rho_>^2}{a^2}
-\ln\frac{1-2x_1\cos\Delta\phi+x_1^2}{1-2x_2\cos\Delta\phi+x_2^2}
=\ln\frac{a^4+\rho^2\rho'^2-2a^2\rho\rho'\cos\Delta\phi}
{a^2(\rho^2+\rho'^2-2\rho\rho'\cos\Delta\phi)} .$$
Reading the numerator as $a^2\times$(distance to the image at $a^2/\rho'$
weighted by $\rho'/a$) recovers the cylinder-image construction
(`~MACRO_EM-03` P14).

### P22.  Exercise 4.8.4 — Point charge in a wedge-shaped hole  *(Wilcox 2e §4.16, p.189)*
An infinite wedge-shaped channel (opening $\beta$, radius $a$) is hollowed
out of a conductor; a unit **point** charge sits inside (book Fig. 4.14).
Derive a form of $G_D(\rho,\phi,z;\rho',\phi',z')$ by the reduced Green
function method (the book hints that writing the correct 3-D delta expansion
is the crux; either $\rho$ or $z$ can carry the reduced equation).
*Answer:* carrying the reduced equation in $\rho$,
$$G_D=\frac8\beta\sum_{n=1}^\infty\sin\frac{n\pi\phi}\beta\sin\frac{n\pi\phi'}\beta
\int_0^\infty dk\,\cos k(z-z')\;g^{\rm in}_{\nu}(k;\rho,\rho'),
\qquad\nu=\frac{n\pi}\beta,$$
with $g^{\rm in}_\nu$ the interior-cylinder reduced Green function of P16(b)
at **fractional** order $\nu$.
*Check:* vanishes on both flats and on the arc $\rho=a$; for $\beta=\pi$ it
equals the half-cylinder image construction (interior-cylinder $G$ minus its
reflection) to $10^{-6}$ (`test_p22_wedge3d_point_charge`).

**Solution.** The correct start (the hint) is
$$4\pi\delta^3=4\pi\,\frac{\delta(\rho-\rho')}\rho\cdot
\frac2\beta\sum_{n\ge1}\sin\frac{n\pi\phi}\beta\sin\frac{n\pi\phi'}\beta\cdot
\frac1\pi\int_0^\infty dk\,\cos k(z-z'),$$
i.e. Dirichlet sine modes on the restricted azimuth and a cosine transform
in the free $z$ direction. The matching ansatz for $G$ turns
$\nabla^2G=-4\pi\delta$ into the radial problem (4.123) with $m^2\to\nu^2$,
$\nu=n\pi/\beta$ — Bessel's *modified* equation of fractional order, since
nothing in its derivation required integer order (the book's footnote 7).
Regularity at the axis and the wall zero at $\rho=a$ give exactly P16(b)'s
$g^{\rm in}_\nu=I_\nu(k\rho_<)\bigl[K_\nu(k\rho_>)-I_\nu(k\rho_>)K_\nu(ka)/I_\nu(ka)\bigr]$,
$C=1$ as before. Collecting weights,
$4\pi\cdot\frac2\beta\cdot\frac1\pi=\frac8\beta$. For $\beta=\pi$ the region
is the half-cylinder $y>0$: uniqueness says $G$ must equal
$G_{\rm cyl}(\phi-\phi')-G_{\rm cyl}(\phi+\phi')$ built from the full
interior cylinder kernel — the test confirms the fractional-order sum
collapses onto that integer-order image difference.

### P23.  Exercise 4.8.5 — Line charge between concentric cylinders  *(Wilcox 2e §4.16, p.189)*
Construct $G_D(\rho,\phi;\rho',\phi')$ for a unit line charge between
grounded concentric cylinders, inner radius $b$, outer radius $a$
($b<\rho'<a$), by a reduced Green function technique.
*Answer:* $G_D=2g_0+4\sum_{m\ge1}\cos m(\phi-\phi')\,g_m$ with
$$g_0=-\frac{\ln(\rho_</b)\,\ln(\rho_>/a)}{\ln(a/b)},\qquad
g_m=\frac{(\rho_</\rho_>)^m+\bigl(b^2\rho_>/a^2\rho_<\bigr)^m
-\bigl(\rho_<\rho_>/a^2\bigr)^m-\bigl(b^2/\rho_<\rho_>\bigr)^m}
{2m\,\bigl[1-(b/a)^{2m}\bigr]}.$$
*Check:* wall zeros and $-1/\rho'$ jumps for $m=0,1,3,4$; assembled $G$
vanishes on both cylinders, is symmetric; $b\to0$
($1/\ln(a/b)$-extrapolated) recovers P21's single-cylinder answer
(`test_p23_concentric_2d`).

**Solution.** Identical machinery to P20 with the angle unrestricted
(integer $m$, cosine assembly as in P21). For $m\ge1$ the two-wall power
solutions are P20's with $(a,b)\to(b,a)$ and $\gamma\to m$. The new case is
$m=0$, where the homogeneous solutions are $1$ and $\ln\rho$: take
$\psi_1=\ln(\rho/b)$ (zero at the inner wall) and $\psi_2=\ln(\rho/a)$ (zero
at the outer). Then $W_\rho[\psi_1,\psi_2]=\ln(\rho/b)\frac1\rho-\ln(\rho/a)\frac1\rho
=\frac{\ln(a/b)}\rho$, and $D=-1/\rho$ gives $C=-1/\ln(a/b)$, i.e. the
quoted $g_0$ — the 2-D analog of the $\sinh$ ladder, linear in $\ln\rho$ on
each side of the source. Consistency limits: $b\to0$ sends
$g_0\to-\ln(\rho_>/a)$ and $g_m\to$ P21's modes (the approach is $\propto1/\ln(a/b)$,
which the test removes by extrapolation); $\ln$-mode charge bookkeeping:
$-\partial g_0/\partial\rho$ jumps by $1/\rho'$, the induced charge splitting
between the walls in the ratio $\ln(\rho'/b):\ln(a/\rho')$ — the 2-D version
of P45's plate split.

### P24.  Exercise 4.9.1 — Explicit Legendre coefficients and values at 0  *(Wilcox 2e §4.16, p.190)*
(a) From the binomial theorem (applied inside Rodrigues' formula (4.179)),
show
$$P_\ell(x)=\frac1{2^\ell}\sum_{r=0}^{[\ell/2]}
\frac{(-1)^r}{r!\,(\ell-r)!}\frac{(2\ell-2r)!}{(\ell-2r)!}\,x^{\ell-2r}
=\sum_{r=0}^{[\ell/2]}\frac{(-1)^r(2\ell-2r-1)!!}{(2r)!!\,(\ell-2r)!}\,x^{\ell-2r},$$
with $(N)!!$ the double factorial, $(0)!!=(-1)!!\equiv1$.
(b) Deduce $P_\ell(0)=0$ ($\ell$ odd) and
$P_\ell(0)=(-1)^{\ell/2}\dfrac{(\ell-1)!!}{\ell!!}$ ($\ell$ even).
(c) Show
$\bigl(\frac d{dx}\bigr)^mP_\ell\big|_{x=0}=0$ for $\ell-m$ odd and
$(-1)^{(\ell-m)/2}\dfrac{(\ell+m-1)!!}{(\ell-m)!!}$ for $\ell-m$ even
($m\le\ell$).
*Answer:* as stated.
*Check:* explicit sum $=$ `eval_legendre` for $\ell\le10$; (b), (c) against
exact polynomial derivatives from `numpy.polynomial` for all $\ell\le8$,
$m\le\ell$ (`test_p24_legendre_explicit`).

**Solution.** (a) Expand
$(x^2-1)^\ell=\sum_r\binom{\ell}{r}(-1)^rx^{2\ell-2r}$ and differentiate
$\ell$ times term by term:
$\frac{d^\ell}{dx^\ell}x^{2\ell-2r}=\frac{(2\ell-2r)!}{(\ell-2r)!}x^{\ell-2r}$
(zero once $2\ell-2r<\ell$, truncating at $r=[\ell/2]$). Dividing by
$2^\ell\ell!$ gives the first form. For the second, split
$(2\ell-2r)!=(2\ell-2r-1)!!\,(2\ell-2r)!!$ and
$(2\ell-2r)!!=2^{\ell-r}(\ell-r)!$; then
$\frac{(2\ell-2r)!}{2^\ell\,r!\,(\ell-r)!}=\frac{(2\ell-2r-1)!!}{2^r\,r!}
=\frac{(2\ell-2r-1)!!}{(2r)!!}$, using $(2r)!!=2^rr!$.
(b) At $x=0$ only the constant term $\ell-2r=0$ survives: $\ell$ even,
$r=\ell/2$, giving $(-1)^{\ell/2}(\ell-1)!!/\ell!!$ (with $(2r)!!=\ell!!$ and
$(\ell-2r)!=1$); odd $\ell$ has no constant term.
(c) The $m$-th derivative shifts the surviving term to $\ell-2r=m$
(so $\ell-m$ even, $r=(\ell-m)/2$), with factor $m!$ from
$\frac{d^m}{dx^m}x^m$:
$$P_\ell^{(m)}(0)=(-1)^{\frac{\ell-m}2}\frac{(\ell+m-1)!!\,m!}{(\ell-m)!!\,m!}
=(-1)^{\frac{\ell-m}2}\frac{(\ell+m-1)!!}{(\ell-m)!!},$$
after writing $(2\ell-2r-1)!!=(\ell+m-1)!!$ and $(2r)!!=(\ell-m)!!$ at
$r=(\ell-m)/2$.

### P25.  Exercise 4.9.2 — Parity of the spherical harmonics  *(Wilcox 2e §4.16, p.190)*
The inversion $\vec r\to-\vec r$ acts on angles as $\theta\to\pi-\theta$ with
$\phi\to\phi+\pi$ (if $\phi<\pi$) or $\phi\to\phi-\pi$ (if $\phi\ge\pi$).
What does it do to $Y_{\ell m}(\theta,\phi)$? (Hint: an overall phase.)
*Answer:* $Y_{\ell m}\to(-1)^{\ell}\,Y_{\ell m}$ — parity $(-1)^\ell$,
independent of $m$.
*Check:* both $\phi$ branches, all $|m|\le\ell\le4$, to $10^{-12}$
(`test_p25_ylm_parity`).

**Solution.** Use the Schwinger/Rodrigues form (4.167):
$Y_{\ell m}\propto e^{im\phi}(\sin\theta)^{-m}
\bigl(\tfrac{d}{d\cos\theta}\bigr)^{\ell-m}(\cos^2\theta-1)^\ell$.
Under the inversion: $\sin\theta$ is unchanged; $\cos\theta\to-\cos\theta$
flips each derivative, giving $(-1)^{\ell-m}$ from the $\ell-m$ derivatives
of the even function $(\cos^2\theta-1)^\ell$; and
$e^{im(\phi\pm\pi)}=(-1)^me^{im\phi}$ (either sign of the shift, since
$e^{\pm im\pi}=(-1)^m$ — which is why the two branches give one answer).
Total phase $(-1)^{\ell-m}(-1)^m=(-1)^\ell$. Equivalently: $Y_{\ell m}$ is a
degree-$\ell$ homogeneous harmonic polynomial in $\hat r$ divided by
$r^\ell$, and any degree-$\ell$ polynomial picks up $(-1)^\ell$ under
$\vec r\to-\vec r$.

### P26.  Exercise 4.9.3 — Legendre orthogonality and normalization  *(Wilcox 2e §4.16, p.191)*
(a) Using Rodrigues' formula (4.179) and the fact that $P_n$ has degree $n$,
show $\int_{-1}^1P_n(x)P_m(x)\,dx=0$ for $m\ne n$.
(b) Using (a), the recursion (4.181),
$(2n+1)xP_n=(n+1)P_{n+1}+nP_{n-1}$, and induction, show
$\int_{-1}^1P_n^2\,dx=\dfrac2{2n+1}$.
*Answer:* as stated.
*Check:* Gauss–Legendre quadrature of the products for several $(n,m)$ pairs
and of the norms for $n=0,1,3,6$ ($10^{-12}$)
(`test_p26_legendre_orthogonality`).

**Solution.** (a) Take $n>m$ and integrate by parts $n$ times:
$$\int_{-1}^1\frac{d^n(x^2-1)^n}{dx^n}\,P_m\,dx
=(-1)^n\int_{-1}^1(x^2-1)^n\,\frac{d^nP_m}{dx^n}\,dx=0,$$
because every boundary term contains an underdifferentiated
$(x^2-1)^{n-j}$, which vanishes at $\pm1$, and the surviving integrand needs
the $n$-th derivative of the degree-$m<n$ polynomial $P_m$, which is zero.
(b) Let $N_n=\int P_n^2$. Multiply (4.181) by $P_{n+1}$ and integrate — by
(a) only the $P_{n+1}^2$ term survives on the right:
$(2n+1)\int xP_nP_{n+1}=(n+1)N_{n+1}$. Now write (4.181) again with
$n\to n+1$, multiply by $P_n$ and integrate:
$(2n+3)\int xP_{n+1}P_n=(n+1)N_n$. The same cross-integral appears in both,
so
$$\frac{N_{n+1}}{N_n}=\frac{2n+1}{2n+3}.$$
Induction: $N_0=\int_{-1}^1dx=2=\frac2{2\cdot0+1}$; if $N_n=\frac2{2n+1}$
then $N_{n+1}=\frac{2n+1}{2n+3}\cdot\frac2{2n+1}=\frac2{2(n+1)+1}$. $\square$

### P27.  Exercise 4.11.1 — Recursions from the generating function  *(Wilcox 2e §4.16, p.191)*
With the Legendre generating function (4.204)/(4.205),
$$G(x,t)=\frac1{\sqrt{1-2xt+t^2}}=\sum_{n=0}^\infty t^nP_n(x),$$
derive (a) Eq. (4.180), $x P'_{n+1}(x)-P'_n(x)=(n+1)P_{n+1}(x)$, and
(b) Eq. (4.181), $(2n+1)xP_n=(n+1)P_{n+1}+nP_{n-1}$. (Hint: $t$- and
$x$-derivatives.)
*Answer:* both follow from the two first-derivative identities of $G$.
*Check:* generating-function partial sums vs the closed form ($10^{-11}$);
both recursions verified numerically for several $(n,x)$
(`test_p27_generating_function`).

**Solution.** Differentiate the closed form:
$$\frac{\partial G}{\partial t}=\frac{x-t}{(1-2xt+t^2)^{3/2}},\qquad
\frac{\partial G}{\partial x}=\frac{t}{(1-2xt+t^2)^{3/2}}
\;\Longrightarrow\;
(x-t)\frac{\partial G}{\partial x}=t\,\frac{\partial G}{\partial t}. \tag{i}$$
(a) Insert the series into (i):
$\sum_n\bigl[xP_n'-P_{n-1}'\bigr]t^n=\sum_n nP_nt^n$, so
$xP_n'-P_{n-1}'=nP_n$; relabeling $n\to n+1$ gives (4.180).
(b) Multiply the $t$-derivative identity through by the root:
$(1-2xt+t^2)\,\partial_tG=(x-t)\,G$. Substituting the series and collecting
$t^n$:
$$(n+1)P_{n+1}-2xnP_n+(n-1)P_{n-1}=xP_n-P_{n-1}
\;\Longrightarrow\;(2n+1)xP_n=(n+1)P_{n+1}+nP_{n-1},$$
which is (4.181) — the three-term recursion behind every stable Legendre
evaluation in the module's code.

### P28.  Exercise 4.11.2 — Rodrigues' formula: recursion and $P_n(1)$  *(Wilcox 2e §4.16, p.191)*
(a) Show by direct substitution that the Rodrigues polynomials (4.179),
$P_n=\frac1{2^nn!}\frac{d^n}{dx^n}(x^2-1)^n$, satisfy Eq. (4.182),
$$\frac{dP_{n+1}}{dx}=(2n+1)P_n+\frac{dP_{n-1}}{dx}.$$
(b) Show from (4.179) that $P_n(1)=1$.
*Answer:* as stated. ((4.182) is the identity that turns $\int P_\ell\,dx$
into Legendre values — used constantly from P33 on.)
*Check:* (4.182) verified at the *coefficient* level (exact polynomial
arithmetic) for $n\le7$, and $P_n(1)=1$ (`test_p28_rodrigues`).

**Solution.** (a) Write $D=d/dx$ and $u_n=(x^2-1)^n$, so
$P_n=D^nu_n/(2^nn!)$. Since $Du_{n+1}=2(n+1)x\,u_n$,
$$P'_{n+1}=\frac{D^{n+2}u_{n+1}}{2^{n+1}(n+1)!}
=\frac{D^{n+1}\bigl(x\,u_n\bigr)}{2^nn!}
=\frac{x\,D^{n+1}u_n+(n+1)D^nu_n}{2^nn!}
=\frac{x\,D^{n+1}u_n}{2^nn!}+(n+1)P_n \tag{i}$$
by Leibniz. Similarly $Du_n=2nx\,u_{n-1}$ gives
$$P'_{n-1}=\frac{D^nu_{n-1}}{2^{n-1}(n-1)!},\qquad
D^{n+1}u_n=2n\,D^n(x\,u_{n-1})=2n\bigl[xD^nu_{n-1}+nD^{n-1}u_{n-1}\bigr].$$
Also $u_n=(x^2-1)u_{n-1}$, so
$D^{n+1}u_n=D^{n+1}\bigl[(x^2-1)u_{n-1}\bigr]
=(x^2-1)D^{n+1}u_{n-1}+2(n+1)xD^nu_{n-1}+n(n+1)D^{n-1}u_{n-1}$.
Eliminating $D^{n+1}u_{n-1}$ between the two expressions and substituting
into (i) collapses, after dividing by $2^nn!$, to
$P'_{n+1}=(2n+1)P_n+P'_{n-1}$. (The module verifies this identity *exactly*
on polynomial coefficients — the honest replacement for the last page of
algebra.)
(b) $(x^2-1)^n=(x-1)^n(x+1)^n$. In the Leibniz expansion of $D^n$ at $x=1$,
any term leaving a positive power of $(x-1)$ vanishes; only the term with
all $n$ derivatives on $(x-1)^n$ survives:
$D^n u_n|_{x=1}=n!\,(x+1)^n|_{x=1}=n!\,2^n$, so $P_n(1)=1$.

### P29.  Exercise 4.11.3 — The $\int P_\ell P_\ell$ angular integral  *(Wilcox 2e §4.16, p.192)*
Evaluate, as concisely as possible,
$$\int d\Omega'\;P_\ell(\cos\gamma_1)\,P_\ell(\cos\gamma_2),\qquad
\cos\gamma_1=\frac{\vec r\cdot\vec r\,'}{rr'},\quad
\cos\gamma_2=\frac{\vec r\,'\cdot\vec r\,''}{r'r''},$$
where the integration is over the directions of $\vec r\,'$.
*Answer:* $\dfrac{4\pi}{2\ell+1}\,P_\ell(\cos\gamma_{12})$, with
$\gamma_{12}$ the angle between $\vec r$ and $\vec r\,''$.
*Check:* sphere quadrature vs closed form on random direction pairs,
$\ell=1,3,5$ (`test_p29_PlPl_integral`).

**Solution.** Apply the addition theorem (4.223) to each factor:
$$P_\ell(\cos\gamma_1)=\frac{4\pi}{2\ell+1}\sum_mY_{\ell m}(\hat n')Y^*_{\ell m}(\hat r),
\qquad
P_\ell(\cos\gamma_2)=\frac{4\pi}{2\ell+1}\sum_{m'}Y^*_{\ell m'}(\hat n')Y_{\ell m'}(\hat r'').$$
The $d\Omega'$ integral is the orthonormality relation
$\int Y_{\ell m}Y^*_{\ell m'}d\Omega'=\delta_{mm'}$, collapsing the double
sum:
$$\Bigl(\frac{4\pi}{2\ell+1}\Bigr)^2\sum_mY^*_{\ell m}(\hat r)Y_{\ell m}(\hat r'')
=\frac{4\pi}{2\ell+1}\,P_\ell(\hat r\cdot\hat r''),$$
the last step being the addition theorem read backwards. (This "reproducing"
property is the projector identity: $\frac{2\ell+1}{4\pi}P_\ell(\hat u\cdot\hat v)$
is the kernel of the projection onto the $\ell$-th harmonic subspace, and a
projector composed with itself is itself.)

### P30.  Exercise 4.11.4 — Variational capacitance of a hemispherical bowl  *(Wilcox 2e §4.16, p.192)*
(a) Combining the variational bound (3.144) with the Coulomb expansion
(4.225), show that a hemispherical shell of radius $a$ carrying an
axisymmetric density $\sigma(x)$ ($x=\cos\theta$, total charge $Q$) has
$$C^{-1}[\sigma]=\frac{4\pi^2a^3}{Q^2}\sum_{\ell=0}^\infty
\Bigl[\int_0^1dx\,P_\ell(x)\,\sigma(x)\Bigr]^2 .$$
(b) With the trial $\sigma(x)=A+Bx$, establish $C>0.8052\,a$. Does the
optimal density grow or shrink toward the edge $\theta=\pi/2$? (Book note:
the exact value is $C=(\frac12+\frac1\pi)a\approx0.8183\,a$, from Loh's
toroidal-coordinate solution.)
*Answer:* (a) as stated; (b) $C_{\max}=0.80515\,a$ at $\beta=B/A=-0.684$:
the density **grows toward the edge** ($\beta<0$ weights $x=0$ hardest),
as the exact edge-diverging solution suggests.
*Check:* optimized bound in $(0.80515,\,0.8183)$; $\beta^*<0$; $\beta=0$
strictly worse (`test_p30_hemisphere_variational`).

**Solution.** (a) Both source points of $W=\frac12\int\int\sigma\sigma'/|\vec x-\vec x'|$
sit on the shell $r=r'=a$, where (4.225) gives
$|\vec x-\vec x'|^{-1}=\sum_{\ell m}\frac{4\pi}{(2\ell+1)a}Y_{\ell m}(\hat n)Y^*_{\ell m}(\hat n')$.
Axisymmetry keeps only $m=0$; with
$Y_{\ell0}=\sqrt{\tfrac{2\ell+1}{4\pi}}P_\ell$ and $da=a^2d\Omega$,
$$W=\frac{a^3}2\sum_\ell\frac{4\pi}{2\ell+1}\cdot\frac{2\ell+1}{4\pi}
\Bigl[2\pi\!\int_0^1P_\ell\,\sigma\,dx\Bigr]^2
=2\pi^2a^3\sum_\ell\Bigl[\int_0^1P_\ell\,\sigma\Bigr]^2$$
(the $x$ integral stops at 0 because $\sigma$ lives on the upper hemisphere
only). Then $C^{-1}=2W/Q^2$ is the quoted sum — every trial is a lower bound
on $C$ (§3.10).
(b) With $\sigma=A(1+\beta x)$: $\int_0^1P_\ell\sigma=A(c_\ell+\beta d_\ell)$
where $c_\ell=\int_0^1P_\ell dx$ (P33's numbers) and
$d_\ell=\int_0^1xP_\ell dx$, computed stably from
$xP_\ell=\frac{(\ell+1)P_{\ell+1}+\ell P_{\ell-1}}{2\ell+1}$; and
$Q=2\pi a^2A(1+\beta/2)$. Maximizing the ratio numerically (the $\ell$ sum
taken to $6000$, converging like $1/\ell^2$ per term) gives
$C=0.80515\,a$ at $\beta^*=-0.684$ — the book's $0.8052$, and $1.6\%$ under
Loh's exact $0.8183$. Since $x=\cos\theta$ *decreases* toward the rim,
$\beta^*<0$ means $\sigma$ is largest at the rim: the linear family is doing
its best to imitate the true edge singularity.

### P31.  Exercise 4.11.5 — Rotations mix only within fixed $\ell$  *(Wilcox 2e §4.16, pp.192–193)*
Completeness of the $Y_{\ell m}$ (4.220) rests on writing $P_\ell(\cos\gamma)$
as a combination of harmonics (4.219). Prove the stronger statement (4.288):
for two spherical frames sharing an origin,
$$Y_{\ell m}(\theta',\phi')=\sum_{m'=-\ell}^{\ell}C^{(\ell)}_{mm'}\,Y_{\ell m'}(\theta,\phi).$$
(a) Express $(\vec a\cdot\vec r\,)^\ell$ of the Schwinger identity (4.168) in
both frames to obtain a linear relation of the form (4.289),
$$(\xi_-)^{2\ell}\sum_m\Bigl(\frac{\xi_+}{\xi_-}\Bigr)^{\ell+m}d_{\ell m}Y_{\ell m}(\theta,\phi)
=(\xi'_-)^{2\ell}\sum_m\Bigl(\frac{\xi'_+}{\xi'_-}\Bigr)^{\ell+m}c_{\ell m}Y_{\ell m}(\theta',\phi'),$$
with $\xi_\pm$-independent constants $c_{\ell m},d_{\ell m}$.
(b) Choosing $2\ell+1$ different null vectors $\vec a$ (different
$\xi'_+/\xi'_-$), solve the resulting system for $Y_{\ell m}(\theta',\phi')$
— the invertibility being a Vandermonde-matrix fact.
(c) Conclude (4.219): with $\hat z'$ along $\vec r$,
$P_\ell(\cos\gamma)\propto Y_{\ell0}(\theta',\phi')$ is a combination of the
$Y_{\ell m}(\theta,\phi)$.
*Answer:* as stated; the rotation matrix $C^{(\ell)}$ is what representation
theory calls the Wigner $D^{(\ell)}$.
*Check:* $C^{(\ell)}$ solved numerically from $2\ell+1$ random directions
reproduces $Y_{\ell m}(R^T\hat n)$ at fresh directions to $10^{-9}$
($\ell=1,2,3$); Vandermonde $\det=\prod_{i<j}(t_j-t_i)$; the $\ell$-closure
gives the addition theorem (4.223) on random pairs
(`test_p31_ylm_rotation`).

**Solution.** (a) The Schwinger construction (4.168) expands, for the null
vector $\vec a=(\tfrac{\xi_+^2-\xi_-^2}{2i},\,\tfrac{\xi_+^2+\xi_-^2}{2},\,i\xi_+\xi_-)$-type
parametrization, the $\ell$-th power of the scalar $\vec a\cdot\vec r$ as a
generating polynomial in $\xi_+/\xi_-$ whose $Y_{\ell m}$ coefficients carry
fixed numerical weights. But $\vec a\cdot\vec r$ is a *scalar*: computing it
in the primed frame (where $\vec a$ has parameters $\xi'_\pm$ and $\vec r$
has angles $\theta',\phi'$) must give the same number, whence (4.289) — one
linear relation between the $2\ell+1$ unprimed harmonics and the $2\ell+1$
primed ones, with coefficients polynomial in the ratio $t'=\xi'_+/\xi'_-$.
(b) Each choice of $\vec a$ gives such a relation with a different $t'$;
stacking $2\ell+1$ of them, the left sides are known and the coefficient
matrix on the primed side is $V_{jm}=(t'_j)^{\ell+m}$ — a Vandermonde
matrix, invertible whenever the $t'_j$ are distinct, since
$\det V=\prod_{i<j}(t'_j-t'_i)\ne0$. Inverting expresses each
$Y_{\ell m}(\theta',\phi')$ as a fixed combination of the
$Y_{\ell m'}(\theta,\phi)$ — Eq. (4.288). No $\ell'\ne\ell$ enters: rotations
cannot mix degrees.
(c) Take the primed frame with $\hat z'\parallel\vec r$. Then $\theta'$ of
the point $\vec r\,''$... more directly: $P_\ell(\cos\gamma)$, with $\gamma$
the angle of $\hat n$ from $\hat z'$, equals
$\sqrt{4\pi/(2\ell+1)}\,Y_{\ell0}(\theta',\phi')$ evaluated in the primed
frame; by (4.288) that is a linear combination of the unprimed
$Y_{\ell m}(\theta,\phi)$ — which is (4.219), the input the chapter needed
for completeness (4.220) and, after computing the coefficients, the addition
theorem (4.223). The numeric check closes the loop by verifying (4.223)
itself on random direction pairs.

### P32.  Exercise 4.11.6 — Two spherical averages of the Coulomb kernel  *(Wilcox 2e §4.16, pp.193–194)*
Using a spherical (free-space) Green function expansion, evaluate
(a) $\displaystyle\int\frac{d\Omega'}{|\vec r-\vec r\,'|}$ and
(b) $\displaystyle\int\frac{\cos\theta'\,d\Omega'}{|\vec r-\vec r\,'|}$
as completely as possible ($P_1(x)=x$ is the hint for (b)).
*Answer:* (a) $\dfrac{4\pi}{r_>}$; (b)
$\dfrac{4\pi}{3}\dfrac{r_<}{r_>^2}\cos\theta$, with $\theta$ the polar angle
of the field point $\vec r$.
*Check:* both against direct sphere quadrature, inside and outside
(`test_p32_sphere_coulomb_integrals`).

**Solution.** Insert the Coulomb expansion (4.225),
$\frac1{|\vec r-\vec r'|}=\sum_{\ell m}\frac{4\pi}{2\ell+1}\frac{r_<^\ell}{r_>^{\ell+1}}Y_{\ell m}(\hat r)Y^*_{\ell m}(\hat r')$.
(a) $\int d\Omega'\,Y^*_{\ell m}(\hat r')=\sqrt{4\pi}\,\delta_{\ell0}\delta_{m0}$
(orthogonality against $Y_{00}=1/\sqrt{4\pi}$): only the monopole survives,
$$\int\frac{d\Omega'}{|\vec r-\vec r'|}
=\frac{4\pi}{1}\cdot\frac1{r_>}\cdot\sqrt{4\pi}\,Y_{00}(\hat r)=\frac{4\pi}{r_>}.$$
(This is the shell theorem in kernel form: a uniform shell looks like a point
charge outside, a constant potential inside.)
(b) $\cos\theta'=\sqrt{4\pi/3}\,Y_{10}(\hat r')$, so the integral projects
out $\ell=1$, $m=0$:
$$\int\frac{\cos\theta'\,d\Omega'}{|\vec r-\vec r'|}
=\frac{4\pi}{3}\,\frac{r_<}{r_>^2}\,\sqrt{\frac{4\pi}3}\,Y_{10}(\hat r)
=\frac{4\pi}{3}\,\frac{r_<}{r_>^2}\,\cos\theta .$$
Physically: the potential of the shell density $\sigma\propto\cos\theta'$ —
uniform field inside ($\propto r\cos\theta$), pure dipole outside
($\propto\cos\theta/r^2$), continuous at $r=r'$.

### P33.  Exercise 4.12.1 — The hemispherical-caps capacitor  *(Wilcox 2e §4.16, p.194)*
Two thin conducting hemispherical caps of radius $a$, separated by a narrow
equatorial gap, are held at $+V$ (upper) and $-V$ (lower) (book Fig. 4.15).
Define $C\equiv Q/V$ with $Q$ the charge on the upper cap.
(a) Treating this as a boundary value problem (or with this geometry's Green
function), show
$$C=\frac a2\sum_{n=0}^\infty\bigl[P_{2n}(0)-P_{2n+2}(0)\bigr]^2 .$$
(Hints: Eq. (4.182) and Ex. 4.11.2(b).)
(b) Using Ex. 4.9.1, rewrite it as
$$C=\frac a2\sum_{n=0}^\infty\Bigl[(4n+3)\,\frac{(2n-1)!!}{(2n+2)!!}\Bigr]^2 .$$
*Answer:* as stated — and the series **diverges logarithmically**
($t_n\sim4/\pi n$): an ideal, gapless split sphere has infinite capacitance,
the 3-D cousin of the parallel-plate $d\to0$ divergence. A physical gap
width cuts the sum off.
*Check:* the two term forms agree to $10^{-15}$; $C$ from direct quadrature
of $\sigma$ ($Q/V$) equals the partial series; increments per doubling
$\to\frac2\pi\ln2$ (`test_p33_caps_capacitor`).

**Solution.** (a) Interior/exterior harmonic expansions matched to the
surface data $V\,\mathrm{sgn}(x)$, $x=\cos\theta$:
$\Phi_{\rm in}=\sum A_\ell(r/a)^\ell P_\ell$,
$\Phi_{\rm out}=\sum A_\ell(a/r)^{\ell+1}P_\ell$, with
$$A_\ell=\frac{2\ell+1}2\,V\!\int_{-1}^1\mathrm{sgn}(x)P_\ell\,dx
=(2\ell+1)V\!\int_0^1P_\ell\,dx\quad(\ell\ {\rm odd};\ {\rm even}\ \ell\ {\rm vanish}).$$
Integrating (4.182) from $x$ to $1$ and using $P_\ell(1)=1$ (Ex. 4.11.2b)
gives the workhorse identity
$$\int_x^1P_\ell(x')\,dx'=\frac{P_{\ell-1}(x)-P_{\ell+1}(x)}{2\ell+1}
\;\Longrightarrow\;
A_\ell=V\bigl[P_{\ell-1}(0)-P_{\ell+1}(0)\bigr].$$
The surface charge adds the interior and exterior normal derivatives:
$\sigma=\frac1{4\pi}\bigl(-\partial_r\Phi_{\rm out}+\partial_r\Phi_{\rm in}\bigr)_{r=a}
=\sum_\ell\frac{2\ell+1}{4\pi a}A_\ell P_\ell$. The upper-cap charge is then
$$Q=2\pi a^2\int_0^1\sigma\,dx
=\frac a2\sum_\ell A_\ell\,(2\ell+1)\!\int_0^1P_\ell\,dx
=\frac a2\,V\sum_{\ell\ {\rm odd}}\bigl[P_{\ell-1}(0)-P_{\ell+1}(0)\bigr]^2,$$
i.e. $C=Q/V$ as quoted with $\ell=2n+1$.
(b) Insert $P_{2n}(0)=(-1)^n\frac{(2n-1)!!}{(2n)!!}$ (P24b):
$$P_{2n}(0)-P_{2n+2}(0)
=(-1)^n\Bigl[\frac{(2n-1)!!}{(2n)!!}+\frac{(2n+1)!!}{(2n+2)!!}\Bigr]
=(-1)^n\frac{(2n-1)!!}{(2n+2)!!}\bigl[(2n+2)+(2n+1)\bigr],$$
whose bracket is $4n+3$ — the quoted form. Stirling gives
$t_n\to4/\pi n$, so $C_N\simeq\frac{2a}\pi\ln N$: log-divergent, confirmed
numerically ($\frac2\pi\ln2$ per doubling).

### P34.  Exercise 4.12.2 — Neumann Green function outside a sphere  *(Wilcox 2e §4.16, p.195)*
Find the electrostatic Neumann Green function for the region outside a
sphere of radius $a$ (unit charge on the $+z$ axis at $r'$, book Fig. 4.16;
$G_N\to0$ at infinity). The book supplies the answer to check against:
$$G_N=\frac1{r_>}+\sum_{\ell\ge1}\Bigl[\frac{r_<^\ell}{r_>^{\ell+1}}
+\frac{\ell}{\ell+1}\,\frac{a^{2\ell+1}}{(rr')^{\ell+1}}\Bigr]P_\ell(\cos\theta).$$
*Answer:* the series above; it also sums to the closed image form
$$G_N=\frac1{|\vec r-\vec r\,'|}+\frac{a/r'}{|\vec r-\vec r_a|}
-\frac1a\ln\frac{t-\cos\theta+\sqrt{1-2t\cos\theta+t^2}}{1-\cos\theta},
\qquad \vec r_a=\frac{a^2}{r'^2}\vec r\,',\ t=\frac{a^2}{rr'},$$
i.e. Kelvin image $+a/r'$ at the inverse point plus a uniform **line image**
from the center to the inverse point.
*Check:* series $=$ closed form ($10^{-9}$); $\partial G_N/\partial r|_{r=a}\to0$;
symmetric in $r\leftrightarrow r'$ (`test_p34_neumann_exterior_sphere`).

**Solution.** Expand in Legendre modes (azimuthal symmetry):
$G_N=\sum_\ell(2\ell+1)g_\ell(r,r')P_\ell(\cos\theta)$ with the radial
equation (4.230). For the exterior region the bounding "surface" is the
sphere plus the sphere at infinity, so $S\to\infty$ and the Neumann boundary
condition (2.106), $\partial_nG_N=-4\pi/S$, becomes homogeneous:
$\partial_rg_\ell|_{r=a}=0$ for **every** $\ell$. From $r^\ell$, $r^{-\ell-1}$
build
$$\psi_1(r)=r^\ell+\frac{\ell}{\ell+1}\frac{a^{2\ell+1}}{r^{\ell+1}}
\ \ (\psi_1'(a)=0),\qquad \psi_2(r)=\frac1{r^{\ell+1}},$$
with jump $-1/r'^2$ in $g'_\ell$ fixing $C=1/(2\ell+1)$; multiplying by
$(2\ell+1)P_\ell$ gives the book's series (the $\ell=0$ member being
$1/r_>$: a Neumann sphere cannot hide the monopole).
*Closed form:* split $\frac{\ell}{\ell+1}=1-\frac1{\ell+1}$. The "$1$" part
sums by the generating function to the Kelvin image $\frac{a}{r'}\frac1{|\vec r-\vec r_a|}$;
the $\frac1{\ell+1}$ part uses
$\sum_\ell\frac{t^{\ell+1}}{\ell+1}P_\ell(x)=\int_0^t\frac{ds}{\sqrt{1-2sx+s^2}}
=\ln\frac{t-x+\sqrt{1-2tx+t^2}}{1-x}$,
a uniform line-charge image of density $-1/a$ stretched from the center to
the inverse point — the standard trick to repair the flux a lone image would
push through the Neumann wall. The test also confirms the $\vec r\leftrightarrow\vec r'$
symmetry that the $t=a^2/rr'$ variable makes manifest.

### P35.  Exercise 4.12.3 — Interior Neumann Green function between spheres  *(Wilcox 2e §4.16, pp.195–196)*
(a) Solve the Neumann problem for the shell $a<r<b$:
$\nabla^2G_N=-4\pi\delta$, $G_N=\sum_\ell(2\ell+1)g_\ell(r,r')P_\ell(\cos\gamma)$,
and show that for $\ell>0$
$$g_\ell=\frac{\ell(\ell+1)}{(2\ell+1)\bigl(b^{2\ell+1}-a^{2\ell+1}\bigr)}
\Bigl[\frac{r_<^\ell}{\ell}+\frac{a^{2\ell+1}}{(\ell+1)r_<^{\ell+1}}\Bigr]
\Bigl[\frac{r_>^\ell}{\ell}+\frac{b^{2\ell+1}}{(\ell+1)r_>^{\ell+1}}\Bigr].$$
Can $g_0$ be determined? Is it unique? (Recall §2.8.) Show the $b\to\infty$
limit recovers Ex. 4.12.2.
(b) Verify that the §2.8/(2.115) surface delta functions are present.
*Answer:* (a) as stated; $g_0$ is fixed only up to an additive constant
(pure-Neumann interior problem): the wall-flux condition
$\partial_rg_0=+\frac1{a^2+b^2}$ at $r=a$ and $-\frac1{a^2+b^2}$ at $r=b$
(i.e. $\mp4\pi/S$ along the outward normals, $S=4\pi(a^2+b^2)$) gives the
symmetric representative
$g_0=\frac1{r_>}-\frac{a^2}{a^2+b^2}\bigl(\frac1r+\frac1{r'}\bigr)+{\rm const}$.
(b) present: as the source approaches a wall, $G_N\to2/|\vec x-\vec x'|$ —
the same-sign image merges with the source (the surface delta of (2.115)).
*Check:* wall derivatives zero ($\ell\ge1$) and $\pm1/(a^2+b^2)$ ($\ell=0$);
$-1/r'^2$ jump; $b\to\infty$ matches P34's modes; boundary doubling
$G_N\,R\to2$ (`test_p35_neumann_shell`).

**Solution.** (a) For $\ell\ge1$ the $-4\pi/S$ flux can be (and, for the
expansion to close, must be) carried entirely by the $\ell=0$ mode, so the
higher modes obey homogeneous Neumann walls: from $r^\ell,r^{-\ell-1}$,
$$\psi_1=\frac{r^\ell}{\ell}+\frac{a^{2\ell+1}}{(\ell+1)r^{\ell+1}},\qquad
\psi_2=\frac{r^\ell}{\ell}+\frac{b^{2\ell+1}}{(\ell+1)r^{\ell+1}}$$
(each normalized so $\psi'=r^{\ell-1}-a^{2\ell+1}/r^{\ell+2}$-type vanishes
at its wall). Radial equation $-(r^2g')'+\ell(\ell+1)g=\delta(r-r')$ demands
the jump $g'|^+_-=-1/r'^2$;
$W_r[\psi_1,\psi_2]=\frac{(2\ell+1)\bigl(b^{2\ell+1}-a^{2\ell+1}\bigr)}{\ell(\ell+1)\,r^2}$,
so $C=\ell(\ell+1)/[(2\ell+1)(b^{2\ell+1}-a^{2\ell+1})]$ — the quoted
$g_\ell$ (the module evaluates it in ratio form to avoid overflow at large
$\ell$). $b\to\infty$: $\psi_2\to\frac{b^{2\ell+1}}{(\ell+1)r^{\ell+1}}$ and
$C\psi_1\psi_2\to$ P34's mode, term by term.
*The $\ell=0$ mode:* Gauss's law forces total flux $-4\pi$ through the two
walls, and (2.106) distributes it as $-4\pi/S$ per unit area:
$\partial_rg_0|_a=+4\pi/S$, $\partial_rg_0|_b=-4\pi/S$ with
$S=4\pi(a^2+b^2)$ — one checks $-a^2(+\frac1{a^2+b^2})\cdot4\pi+b^2(-\frac1{a^2+b^2})\cdot4\pi=-4\pi$.
Solving $-(r^2g_0')'=\delta(r-r')$ with those wall slopes gives
$g_0=\frac1{r_>}-\frac{a^2}{a^2+b^2}\bigl(\frac1r+\frac1{r'}\bigr)+{\rm const}$:
determined **up to the constant** — the §2.8 zero mode of the interior
Neumann problem (only potential *differences* are physical; equivalently
$\langle\Phi\rangle_S$ in (2.103) absorbs it). It is *not* unique, and no
boundary condition can make it so.
(b) The (2.115) refinement says the normal derivative of $G_N$ acquires a
surface delta when the source point lies on the wall. Its integrated
signature: a source *on* a Neumann wall coincides with its same-sign image,
so the Green function doubles, $G_N\to2/|\vec x-\vec x'|$, as
$\vec x\to\vec x'$ with $r'=a$. The test drives the 500-mode sum to the wall
and watches $G_N\,|\vec x-\vec x'|\to2$.

### P36.  Exercise 4.12.4 — Sphere-surface data: mode sum and Poisson kernel  *(Wilcox 2e §4.16, p.196)*
(a) Show that a sphere of radius $a$ with prescribed surface potential
$V(\theta,\phi)$ produces outside
$$\Phi(\vec x)=\sum_{\ell m}\Bigl(\frac ar\Bigr)^{\ell+1}Y_{\ell m}(\theta,\phi)\,B_{\ell m},
\qquad B_{\ell m}=\oint_SdΩ'\,V(\theta',\phi')\,Y^*_{\ell m}(\theta',\phi'),$$
and give the interior solution.
(b) Show both are equivalent to the closed kernel form ($+$ inside, $-$
outside)
$$\Phi(\vec x)=\pm\frac{a\,(a^2-r^2)}{4\pi}\oint
\frac{d\Omega'\,V(\theta',\phi')}{(a^2+r^2-2ar\cos\gamma)^{3/2}},\qquad
\cos\gamma=\hat r\cdot\hat r'.$$
*Answer:* (a) as stated; inside, $(a/r)^{\ell+1}\to(r/a)^{\ell}$.
(b) the spherical Poisson kernel.
*Check:* mode series $=$ kernel quadrature at interior and exterior points
(random smooth data, $10^{-8}$); both reproduce the boundary data as
$r\to a^\pm$ (`test_p36_sphere_poisson`).

**Solution.** (a) Outside, harmonicity + decay force
$\Phi=\sum_{\ell m}c_{\ell m}r^{-\ell-1}Y_{\ell m}$; matching at $r=a$ and
projecting with $\oint Y^*_{\ell m}$ (orthonormality) gives
$c_{\ell m}=a^{\ell+1}B_{\ell m}$ — the quoted form. Inside, regularity at
the origin swaps the radial factor for $(r/a)^\ell$ with the **same**
$B_{\ell m}$. (Equivalently: feed the sphere's Dirichlet Green function into
the surface term of (2.98); the modes of $-\frac1{4\pi}\partial_{n'}G_D$ are
exactly these radial ratios.)
(b) Resum. Insert $B_{\ell m}$, use the addition theorem to collapse the $m$
sum, and evaluate the $\ell$ sum with the generating-function derivative
identity: for $t=r/a<1$,
$$\sum_\ell(2\ell+1)\,t^\ell P_\ell(\cos\gamma)
=\Bigl(2t\frac{d}{dt}+1\Bigr)\frac1{\sqrt{1-2t\cos\gamma+t^2}}
=\frac{1-t^2}{(1-2t\cos\gamma+t^2)^{3/2}} .$$
Then
$\Phi_{\rm in}=\frac1{4\pi}\oint d\Omega'V\sum_\ell(2\ell+1)t^\ell P_\ell
=\frac{a(a^2-r^2)}{4\pi}\oint\frac{d\Omega'V}{(a^2+r^2-2ar\cos\gamma)^{3/2}}$,
restoring dimensions by $a^3$ from $t$-powers. Outside, $t=a/r$ gives the
same kernel with $(r^2-a^2)$ — the overall $\mp$ sign quoted. As
$r\to a^\pm$ the kernel is a normalized, concentrating family on the sphere
(unit mass by the $\ell=0$ term), so $\Phi\to V$: the boundary data is
recovered, which is the numeric check.

### P37.  Exercise 4.12.5 — Hemisphere: grounded dome, charged base  *(Wilcox 2e §4.16, p.196)*
Solve the interior of the half-ball $0\le\theta\le\pi/2$, $r\le a$ (book
Fig. 4.17): the hemispherical dome $r=a$ is at potential $0$, the flat base
($\theta=\pi/2$, i.e. $z=0$, $r<a$) at potential $V$. Determine all
coefficients of the series solution.
*Answer:*
$$\Phi(r,\theta)=V\Bigl[1-\sum_{\ell\ {\rm odd}}
\bigl(P_{\ell-1}(0)-P_{\ell+1}(0)\bigr)\Bigl(\frac ra\Bigr)^{\ell}P_\ell(\cos\theta)\Bigr].$$
*Check:* $\Phi=V$ on the base (exactly, term by term), $\to0$ on the dome
($2\times10^{-3}$ at 4000 terms, Gibbs-limited), harmonic inside, $\to V$ at
the center (`test_p37_hemisphere_basin`).

**Solution.** Write $\Phi=V+u$: then $u$ is harmonic with $u=0$ on the base
and $u=-V$ on the dome. Harmonics regular at the origin that vanish on the
base $\theta=\pi/2$ are exactly the **odd**-$\ell$ family
$r^\ell P_\ell(\cos\theta)$ (odd $P_\ell(0)=0$), so
$u=-V\sum_{\rm odd}c_\ell(r/a)^\ell P_\ell$. The dome condition needs
$\sum_{\rm odd}c_\ell P_\ell(x)=1$ on $0<x<1$ — i.e. the odd-$\ell$ Legendre
expansion of $\mathrm{sgn}(x)$ restricted to the upper half:
$$c_\ell=\frac{2\ell+1}{2}\int_{-1}^1\mathrm{sgn}(x)P_\ell\,dx
=(2\ell+1)\int_0^1P_\ell\,dx=P_{\ell-1}(0)-P_{\ell+1}(0),$$
by P33's integral identity. Hence the quoted series. Sanity limits: at the
center ($r\to0$) only the "1" survives, $\Phi\to V$ — correct, the center
sits on the base plate; on the axis the series is alternating with
$(r/a)^\ell$ decay. (The coefficients are evaluated with the stable
$P_{2n}(0)$ recursion — the double-factorial form overflows past
$\ell\sim300$, an implementation lesson the code encodes.)

### P38.  Exercise 4.12.6 — Capacitance matrix of concentric spheres  *(Wilcox 2e §4.16, p.197)*
From the §4.12 Dirichlet Green function for concentric spheres (inner radius
$a$, outer $b$), deduce the capacitance coefficients $C_{aa}$, $C_{bb}$ and
the induction coefficient $C_{ab}$ (§2.12 supplies the framework
$Q_i=\sum_jC_{ij}V_j$).
*Answer:*
$$C_{aa}=\frac{ab}{b-a},\qquad C_{ab}=C_{ba}=-\frac{ab}{b-a},\qquad
C_{bb}=\frac{ab}{b-a}+b .$$
*Check:* against the explicit $\ell=0$ two-sphere potential (Gauss-law
charges for three $(V_a,V_b)$ pairs, $10^{-12}$); $b\to\infty$ isolated
sphere $C_{aa}\to a$; symmetry and positivity of the matrix
(`test_p38_concentric_capacitances`).

**Solution.** Conductors are equipotentials, so only the $\ell=0$ sector of
the §4.12 Green function is engaged (all $Y_{\ell m}$ surface moments of
constant data vanish for $\ell\ge1$). Between the spheres the general
monopole solution is $\Phi=\alpha/r+\beta$; the data
$\Phi(a)=V_a$, $\Phi(b)=V_b$ give
$$\alpha=\frac{ab\,(V_a-V_b)}{b-a},\qquad
\beta=\frac{bV_b-aV_a}{b-a}.$$
Gauss's law reads the charges off: the inner sphere carries
$Q_a=\alpha=\frac{ab}{b-a}(V_a-V_b)$, so
$C_{aa}=\frac{ab}{b-a}$, $C_{ab}=-\frac{ab}{b-a}$. The outer conductor's
inner face carries $-\alpha$ (the field between must terminate), while its
outer face sees the exterior solution $\Phi=bV_b/r$ and carries $bV_b$:
$$Q_b=-\alpha+bV_b=-\frac{ab}{b-a}V_a+\Bigl(\frac{ab}{b-a}+b\Bigr)V_b,$$
giving $C_{ba}=C_{ab}$ (reciprocity, automatic) and the quoted $C_{bb}$.
Limits: $b\to\infty$: $C_{aa}\to a$ (isolated sphere), $C_{bb}\to b$;
$b-a\to0$: the parallel-plate divergence. The matrix is symmetric with
$C_{aa}C_{bb}-C_{ab}^2>0$ — the §2.12 energy positivity, which the test
asserts.

### P39.  Exercise 4.13.1 — Field at the center of an unequally split sphere  *(Wilcox 2e §4.16, p.197)*
A conducting sphere of radius $a$ is cut into two insulated pieces along the
cone $\theta=\theta_0$ (book Fig. 4.18): the cap $\theta<\theta_0$ is at
potential $V$, the remainder at $-V$. Find $\vec E$ at the center $O$.
*Answer:* $\vec E(O)=-\dfrac{3V}{2a}\sin^2\!\theta_0\,\hat z$ — set by the
$\ell=1$ interior coefficient alone; for the symmetric split
($\theta_0=\pi/2$) it is $-\frac{3V}{2a}\hat z$.
*Check:* closed form vs finite-difference gradient of the truncated interior
series at three $(\theta_0,V,a)$ (`test_p39_center_field`).

**Solution.** Inside, $\Phi=\sum_\ell A_\ell(r/a)^\ell P_\ell(\cos\theta)$;
at the origin only the $\ell=1$ term has a nonzero gradient
($\nabla[rP_1\cos]=\hat z$; higher $\ell$ vanish like $r^{\ell-1}$, and
$\ell=0$ is constant). Project the boundary data:
$$A_1=\frac32\Bigl[V\!\int_{x_0}^1x\,dx+(-V)\!\int_{-1}^{x_0}x\,dx\Bigr]
=\frac32\,V\Bigl[\frac{1-x_0^2}{2}-\frac{x_0^2-1}{2}\Bigr]
=\frac{3V}{2}\bigl(1-x_0^2\bigr),\qquad x_0=\cos\theta_0 .$$
Then $\vec E(O)=-\nabla\Phi|_0=-\frac{A_1}{a}\hat z
=-\frac{3V}{2a}\sin^2\theta_0\,\hat z$. Sanity: for $\theta_0\to0$ or $\pi$
the sphere is (almost) all one potential and the field dies like the cap
area; the maximum is the symmetric split. The test differentiates the
800-term series numerically at the origin and matches.

### P40.  Exercise 4.13.2 — Point electrostatics on a sphere  *(Wilcox 2e §4.16, pp.197–198)*
Do 2-D electrostatics **on the unit sphere**: solve
$$\nabla^2_{\theta\phi}G=-2\pi\,\delta(\cos\theta-\cos\theta')\,\delta(\phi-\phi')
+2\pi\,\delta(\cos\theta+\cos\theta')\,\delta\bigl(\phi-{\rm mod}_{2\pi}(\phi'+\pi)\bigr),$$
i.e. a $+1$ point charge at $(\theta',\phi')$ and a $-1$ charge at the
antipode, where
$\nabla^2_{\theta\phi}=(\vec r\times\vec\nabla)^2
=\frac1{\sin\theta}\partial_\theta(\sin\theta\,\partial_\theta)+\frac1{\sin^2\theta}\partial_\phi^2$.
(a) Show $G=Q_0(x)=\frac12\ln\frac{1+x}{1-x}$, $x=\cos\gamma=\hat r\cdot\hat r'$,
with $Q_0$ the zeroth Legendre function of the second kind.
(b) Show the eigenfunction form: the book prints
$G=2\sum_{\ell\ {\rm odd}}\frac{2\ell+1}{\ell(\ell+1)}P_\ell(\cos\gamma)$ —
but the prefactor $2$ is inconsistent with (a)'s $-2\pi$ normalization: the
PDE gives coefficient $\frac{2\ell+1}{\ell(\ell+1)}$ **without** the 2
(flagged erratum, settled numerically).
*Answer:* $G=Q_0(\cos\gamma)=\sum_{\ell\ {\rm odd}}\frac{2\ell+1}{\ell(\ell+1)}P_\ell(\cos\gamma)$.
Why the antipodal $-1$? A compact surface admits no net charge
(Gauss: the flux has nowhere to go) — the opposite charge is obligatory.
*Check:* Cesàro-averaged series $=Q_0$ at several $\cos\gamma$ ($10^{-6}$,
coefficient $1\times$, not $2\times$); $Q_0(\cos\gamma)$ is angularly
harmonic away from the two charges; near-charge behavior
$G\to-\ln\gamma+\ln2$ — the 2-D Coulomb log in the $-2\pi$ convention
(`test_p40_sphere_point_electrostatics`).

**Solution.** (a) Rotational symmetry: put $\hat z$ along $\hat r'$, so
$G=G(\gamma)$ with the $+$ charge at $\gamma=0$ and the $-$ at $\gamma=\pi$.
Away from both, $\frac1{\sin\gamma}\frac d{d\gamma}\bigl(\sin\gamma\,\frac{dG}{d\gamma}\bigr)=0$
integrates to $\sin\gamma\,G'=c_1$. Try $G=Q_0(\cos\gamma)$:
$Q_0'(x)=1/(1-x^2)$, so
$\frac{dG}{d\gamma}=-\sin\gamma\cdot\frac1{\sin^2\gamma}=-\frac1{\sin\gamma}$
and $\sin\gamma\,G'=-1$: harmonic in the punctured sphere. Near $\gamma=0$,
$1-x\simeq\gamma^2/2$ gives $G\simeq\ln(2/\gamma)$: exactly the 2-D point
charge $-\ln(\text{distance})$ demanded by the $-2\pi$ delta (flux
bookkeeping: $\oint(\partial G/\partial\gamma)\,\sin\gamma\,d\phi=-2\pi$ ✓);
near $\gamma=\pi$, $G\simeq-\ln(2/(\pi-\gamma))\cdot$… i.e. $+\ln$
divergence of the opposite sign — the $-1$ charge. Uniqueness on the compact
surface holds up to a constant; $Q_0$ is the zero-average representative
($\int_{-1}^1Q_0\,dx=0$ by oddness).
(b) Expand $G=\sum_\ell g_\ell\frac{2\ell+1}{4\pi}\cdot4\pi\,(\dots)$ —
cleanly: use
$\delta^2(\hat n-\hat n')=\sum_{\ell m}Y_{\ell m}(\hat n)Y^*_{\ell m}(\hat n')$
and $Y_{\ell m}(-\hat n')=(-1)^\ell Y_{\ell m}(\hat n')$ (P25): the source
difference keeps odd $\ell$ only, with the $m$ sums collapsing by the
addition theorem to $\frac{2\ell+1}{4\pi}P_\ell(\cos\gamma)\times2$. Since
$\nabla^2_{\theta\phi}P_\ell=-\ell(\ell+1)P_\ell$,
$$-\ell(\ell+1)\,g_\ell=-2\pi\quad\Longrightarrow\quad g_\ell=\frac{2\pi}{\ell(\ell+1)},
\qquad
G=\sum_{\ell\ {\rm odd}}\frac{2\ell+1}{\ell(\ell+1)}P_\ell(\cos\gamma).$$
The Cesàro-averaged numerical sum matches $Q_0(\cos\gamma)$ with coefficient
exactly 1 — the printed extra factor 2 in the book's (b) would double the
charge and contradict its own part (a).

### P41.  Exercise 4.13.3 — Sphere split at $\theta_0$: potentials and capacitance  *(Wilcox 2e §4.16, pp.198–199)*
The shell of radius $a$ is separated at polar angle $\theta_0$ (book
Fig. 4.19): the top piece carries charge $Q$ at potential $V_1$, the bottom
$-Q$ at $V_2$.
(a) Show $V_2=-\dfrac{1-\cos\theta_0}{1+\cos\theta_0}\,V_1$.
(b) With $x_0=\cos\theta_0$ and $C\equiv Q/(V_1-V_2)$, show
$$C=\frac a8\sum_{\ell\ge1}(2\ell+1)^2
\Bigl[\int_{x_0}^1P_\ell\,dx\Bigr]
\Bigl[(1+x_0)\int_{x_0}^1P_\ell\,dx+(x_0-1)\int_{-1}^{x_0}P_\ell\,dx\Bigr],$$
and explain how the integrals become sums (no need to evaluate).
(c) Reconnect to Ex. 4.12.1 at $\theta_0=\pi/2$.
*Answer:* (a) equivalent to zero mean surface potential (zero total charge);
(b) as stated — and since $\int_{-1}^{x_0}=-\int_{x_0}^1$ for $\ell\ge1$, it
simplifies to $C=\frac a4\sum(2\ell+1)^2\bigl[\int_{x_0}^1P_\ell\bigr]^2$;
the integrals are $[P_{\ell-1}(x_0)-P_{\ell+1}(x_0)]/(2\ell+1)$ via (4.182);
(c) $C(x_0{=}0)=\frac12C_{4.12.1}$ — consistent, because this $C$ divides by
$V_1-V_2=2V$ where 4.12.1 divided by $V$.
*Check:* (a) as the $\langle V\rangle=0$ condition ($10^{-13}$); printed and
simplified series identical; $x_0=0$ reconnection exact
(`test_p41_unequal_caps`).

**Solution.** (a) The exterior monopole reads the total charge:
$\Phi_{\rm out}=\sum A_\ell(a/r)^{\ell+1}P_\ell$ has
$Q_{\rm tot}=aA_0=a\,\langle V\rangle$, the average of the surface
potential. Zero net charge ($+Q-Q$) therefore forces
$$\langle V\rangle=\tfrac12\bigl[V_1(1-x_0)+V_2(1+x_0)\bigr]=0
\;\Longrightarrow\;V_2=-\frac{1-x_0}{1+x_0}V_1,$$
the cap area fractions being $(1\mp x_0)/2$.
(b) Project the two-level data:
$A_\ell=\frac{2\ell+1}2\bigl[V_1I_+ + V_2I_-\bigr]$ with
$I_+=\int_{x_0}^1P_\ell$, $I_-=\int_{-1}^{x_0}P_\ell$. Then
$\sigma=\sum\frac{2\ell+1}{4\pi a}A_\ell P_\ell$ and the top-piece charge is
$Q=2\pi a^2\int_{x_0}^1\sigma\,dx=\frac a2\sum(2\ell+1)A_\ell I_+$.
Using (a) to write $V_1,V_2$ in terms of $V_1-V_2$
($V_1=\frac{1+x_0}2(V_1-V_2)$, $V_2=-\frac{1-x_0}2(V_1-V_2)$) gives
$$Q=(V_1-V_2)\,\frac a8\sum_{\ell\ge1}(2\ell+1)^2
I_+\bigl[(1+x_0)I_+ +(x_0-1)I_-\bigr],$$
the printed form ($\ell=0$ drops: $A_0=\langle V\rangle=0$). *Integrals to
sums:* integrate (4.182) as in P33:
$I_+=[P_{\ell-1}(x_0)-P_{\ell+1}(x_0)]/(2\ell+1)$, and
$I_-=-I_+$ because $\int_{-1}^1P_\ell=0$ for $\ell\ge1$ — which also
collapses the bracket to $2I_+$ and the sum to
$\frac a4\sum(2\ell+1)^2I_+^2$.
(c) At $x_0=0$, $(2\ell+1)I_+=P_{\ell-1}(0)-P_{\ell+1}(0)$ (odd $\ell$), so
$C=\frac a4\sum_{\rm odd}[P_{\ell-1}(0)-P_{\ell+1}(0)]^2$ — exactly half of
Ex. 4.12.1's $\frac a2\sum[\cdot]^2$: there $C=Q/V$ with $V_{1,2}=\pm V$,
here $C=Q/2V$. Same physics, factor-two of definition.

### P42.  Exercise 4.13.4 — Capacitance matrix of the two hemispheres  *(Wilcox 2e §4.16, p.199)*
For the sphere of radius $a$ split symmetrically into halves 1 (upper) and 2
(lower) (book Fig. 4.20), show
$$C_{11}=C_{22}=\frac a4\sum_{\ell\ge0}(2\ell+1)^2\Bigl[\int_0^1P_\ell\,dx\Bigr]^2,
\qquad
C_{12}=C_{21}=\frac a4\sum_{\ell\ge0}(-1)^\ell(2\ell+1)^2\Bigl[\int_0^1P_\ell\,dx\Bigr]^2 .$$
(The book notes the system capacitance is $C=\frac12(C_{11}-C_{12})$, and
the integrals reduce as in Ex. 4.12.1.)
*Answer:* as stated. Bonus structure the checks exploit: $C_{11}+C_{12}=a/2$
**exactly at every truncation** (even $\ell\ge2$ have
$\int_0^1P_\ell=0$), which is the full sphere at one potential
($Q=\frac a2\cdot2V/2\dots$ i.e. $C_{\rm sphere}=a$ split over two halves);
and $C_{11}-C_{12}$ is Ex. 4.12.1's log-divergent gap series.
*Check:* both identities at two truncations ($10^{-12}$); $C_{11}>0>C_{12}$
(`test_p42_halves_capacitance_matrix`).

**Solution.** Give the halves independent potentials $V_1$, $V_2$. Since
$\int_{-1}^0P_\ell=(-1)^\ell\int_0^1P_\ell$ (parity of $P_\ell$), the
projection is
$$A_\ell=\frac{2\ell+1}2\,I_\ell\,\bigl[V_1+(-1)^\ell V_2\bigr],\qquad
I_\ell\equiv\int_0^1P_\ell\,dx .$$
The upper-half charge (P41's bookkeeping at $x_0=0$):
$$Q_1=\frac a2\sum_\ell(2\ell+1)A_\ell I_\ell
=\frac a4\sum_\ell(2\ell+1)^2I_\ell^2\,V_1
+\frac a4\sum_\ell(-1)^\ell(2\ell+1)^2I_\ell^2\,V_2 ,$$
and reading off $Q_1=C_{11}V_1+C_{12}V_2$ gives both quoted series;
$C_{22}=C_{11}$ and $C_{21}=C_{12}$ by the up-down symmetry.
*Consistency:* odd-$\ell$ terms cancel in $C_{11}+C_{12}$, and even
$\ell\ge2$ have $I_\ell=0$ (their $P_{\ell\mp1}(0)$ vanish), leaving only
$\ell=0$: $C_{11}+C_{12}=\frac a4\cdot1\cdot1\cdot2=\frac a2$ exactly — set
$V_1=V_2=V$: the full sphere holds $Q_{\rm tot}=2Q_1=(C_{11}+C_{12})2V=aV$ ✓.
Setting $V_2=-V_1$ instead isolates $C_{11}-C_{12}=\frac a2\sum_{\rm odd}(2\ell+1)^2I_\ell^2$
— Ex. 4.12.1's series, so the gap capacitance $\frac12(C_{11}-C_{12})$
diverges logarithmically as it must.

### P43.  Exercise 4.13.5 — Half-space Green function in spherical harmonics  *(Wilcox 2e §4.16, p.200)*
Find $G_D$ for the free half-space above a grounded conducting plane at
$\theta=\pi/2$ (all $\phi$; book Fig. 4.21), as a sum over spherical
harmonics.
*Answer:*
$$G_D=\sum_{\ell,m\,:\;\ell+m\ {\rm odd}}\frac{8\pi}{2\ell+1}\,
\frac{r_<^\ell}{r_>^{\ell+1}}\,Y_{\ell m}(\theta,\phi)\,Y^*_{\ell m}(\theta',\phi') .$$
*Check:* equals the plane-image pair $1/R-1/R''$ on random point pairs
($2\times10^{-4}$ at $L=80$); vanishes on the plane
(`test_p43_halfspace_spherical`).

**Solution.** Image route: $G_D=\frac1{|\vec r-\vec r'|}-\frac1{|\vec r-\vec r''|}$
with $\vec r''$ the mirror of $\vec r'$ ($\theta'\to\pi-\theta'$, same
$\phi'$, same $r'$). Expand both by the Coulomb expansion (4.225); the
image term carries
$Y^*_{\ell m}(\pi-\theta',\phi')=(-1)^{\ell+m}Y^*_{\ell m}(\theta',\phi')$
(the $\theta$-half of P25's parity: $P_\ell^{|m|}(-x)=(-1)^{\ell+|m|}P_\ell^{|m|}(x)$,
no azimuth flip here). Subtracting kills $\ell+m$ even and doubles
$\ell+m$ odd:
$$G_D=\sum_{\ell+m\ {\rm odd}}2\cdot\frac{4\pi}{2\ell+1}\frac{r_<^\ell}{r_>^{\ell+1}}
Y_{\ell m}Y^*_{\ell m}{}' ,$$
the quoted form. On the plane $\theta=\pi/2$: $Y_{\ell m}(\pi/2,\phi)\propto P_\ell^{|m|}(0)$,
which vanishes exactly when $\ell+m$ is odd — every surviving term is
individually zero on the conductor. (Equivalently, one can *derive* it
without images: expand $G_D$ in the half-space harmonic basis — the
$\ell+m$-odd $Y_{\ell m}$, complete for functions vanishing at
$\theta=\pi/2$ — and solve the radial jump problem; the doubling $8\pi$
appears because the half-basis resolves only the odd part of the delta.)

### P44.  Exercise 4.14.1 — Completeness relation for orthonormal sets  *(Wilcox 2e §4.16, p.200)*
Prove the relation (4.267),
$\delta(\vec x\,'-\vec x)=\sum_n\psi^*_n(\vec x\,')\psi_n(\vec x)$, for a
complete orthonormal set $\{\psi_n\}$.
*Answer:* it is the statement that the expansion
$f=\sum_nc_n\psi_n$, $c_n=\int\psi_n^*f$, reproduces every $f$ in the
space — i.e. the kernel $\sum\psi^*_n(\vec x')\psi_n(\vec x)$ acts as the
identity.
*Check:* the sine-basis kernel on $[0,L]$ applied to two smooth test
functions returns their point values ($10^{-6}$)
(`test_p44_completeness_action`).

**Solution.** *Completeness* of $\{\psi_n\}$ means every admissible $f$
expands as $f(\vec x)=\sum_nc_n\psi_n(\vec x)$; *orthonormality*
($\int\psi^*_n\psi_m=\delta_{nm}$) fixes the coefficients:
$c_n=\int d^3x'\,\psi^*_n(\vec x\,')f(\vec x\,')$. Substituting the
coefficients back and exchanging sum and integral,
$$f(\vec x)=\int d^3x'\Bigl[\sum_n\psi^*_n(\vec x\,')\psi_n(\vec x)\Bigr]f(\vec x\,')
\qquad\text{for every }f .$$
An object that reproduces every test function under the integral **is** the
delta distribution — Eq. (4.267). (The equality is distributional: the sum
does not converge pointwise, but its action on smooth functions does, which
is precisely what the numeric check exercises with a truncated sine basis.)
Conversely, if (4.267) holds, expanding any $f$ succeeds — completeness and
the delta relation are equivalent.

### P45.  Exercise 4.14.2 — Parallel plates: the Bessel–eigenfunction form  *(Wilcox 2e §4.16, p.200)*
Show (eigenfunction expansion or otherwise) that the Dirichlet Green
function between grounded plates $z=0$ and $z=a$ (book Fig. 4.22; cf.
Exercises 3.1.1 and 3.2.3) can be written
$$G_D=\frac4a\int_0^\infty dk\,k\,J_0(kD)
\sum_{n=1}^\infty\frac{\sin(n\pi z/a)\,\sin(n\pi z'/a)}{k^2+(n\pi/a)^2},
\qquad D=|(\vec x-\vec x')_\perp| .$$
*Answer:* as stated — transverse plane waves ($\to J_0(kD)$ after the
angular average) times the sine eigenfunctions in $z$, divided by the
eigenvalue.
*Check:* equals the Ex. 3.1.1 image ladder (12000 images) to $10^{-7}$,
including the coincident-plane case $z=z'$ (the code sums the $n$ series
first via P48's sum rule and splits off the free part analytically); zero on
both plates (`test_p45_plates_bessel_form`).

**Solution.** The Laplacian eigenfunctions of the slab that vanish on the
plates are
$\psi_{\vec k,n}=\frac{e^{i\vec k\cdot\vec x_\perp}}{2\pi}\sqrt{\frac2a}\sin\frac{n\pi z}a$
with eigenvalue $-(k^2+k_n^2)$, $k_n=n\pi/a$; they are orthonormal and
complete. The eigenfunction recipe (4.268-style) inverts
$-\nabla^2G=4\pi\delta$ mode by mode:
$$G_D=4\pi\int d^2k\sum_n\frac{\psi_{\vec k,n}(\vec x)\psi^*_{\vec k,n}(\vec x\,')}{k^2+k_n^2}
=\frac4a\cdot\frac1{2\pi}\int d^2k\,e^{i\vec k\cdot(\vec x-\vec x')_\perp}
\sum_n\frac{\sin k_nz\,\sin k_nz'}{k^2+k_n^2}.$$
The angular part of $d^2k$ is P5's addition-theorem average,
$\int_0^{2\pi}d\alpha\,e^{ikD\cos\alpha}=2\pi J_0(kD)$, leaving the quoted
single $k$ integral. It is the same object as Ex. 3.1.1's image ladder and
§3.2's reduced-$g$ $k$-integral — three representations, and the numeric
check pins the eigenfunction one against the ladder. (Practical note: at
$z=z'$ the raw $k$ integrand decays only like $J_0(kD)/2k$ — conditionally
convergent; doing the $n$ sum first (P48) and pulling out
$e^{-k|z-z'|}/2k\to1/|\vec x-\vec x'|$ analytically leaves an exponentially
convergent remainder. The code does exactly this.)

### P46.  Exercise 4.14.3 — Eigenvalue form of the cylinder's reduced $g$  *(Wilcox 2e §4.16, p.201)*
Returning to Ex. 4.7.4(b): show the interior reduced Green function has the
eigenvalue expansion
$$g^{\rm in}_m(k;\rho,\rho')=\sum_{n=1}^\infty
\frac{\mathcal J_{1m}(k_{mn}\rho)\,\mathcal J_{1m}(k_{mn}\rho')}{k^2+k_{mn}^2},
\qquad k_{mn}=\frac{x_{mn}}a .$$
*Answer:* as stated — the Fourier–Bessel resolvent of the radial operator.
*Check:* the $N=6000$ eigen-sum equals P16(b)'s $I,K$ closed form for
$(m,k)=(0,0.7),(2,1.3)$ to $2\times10^{-6}$, and converges steadily in the
delicate near-wall case (`test_p46_cylinder_eigen_g`).

**Solution.** The reduced equation (P16) is
$\bigl[\mathcal L_\rho-k^2\bigr]g_m=-\delta(\rho-\rho')/\rho$ with
$\mathcal L_\rho=\frac1\rho\partial_\rho(\rho\partial_\rho)-\frac{m^2}{\rho^2}$
and $g_m(a)=0$. The $\mathcal J_{1m}(k_{mn}\rho)$ are exactly the Dirichlet
eigenfunctions of $\mathcal L_\rho$:
$\mathcal L_\rho\mathcal J_{1m}=-k_{mn}^2\mathcal J_{1m}$, orthonormal with
weight $\rho$ (4.69) and complete (4.71). Expand
$g_m=\sum_nc_n\mathcal J_{1m}(k_{mn}\rho)$ and the delta by (4.71); matching
coefficients,
$$-(k_{mn}^2+k^2)\,c_n=-\mathcal J_{1m}(k_{mn}\rho')
\quad\Longrightarrow\quad
c_n=\frac{\mathcal J_{1m}(k_{mn}\rho')}{k^2+k_{mn}^2},$$
the quoted sum. Its closed resummation is P16(b)'s
$I_m(k\rho_<)[K_m(k\rho_>)-I_m(k\rho_>)K_m(ka)/I_m(ka)]$ — the identity the
test verifies numerically; it is the radial analog of P48's sine sum rule.

### P47.  Exercise 4.14.4 — The 1-D Dirichlet Green function by eigenfunctions  *(Wilcox 2e §4.16, p.201)*
Expand the one-dimensional Dirichlet Green function of §2.9,
$$\frac{d^2G_D(x,x')}{dx^2}=-\delta(x-x'),\qquad G_D(0,x')=G_D(L,x')=0,$$
in eigenfunctions.
*Answer:* $G_D=\dfrac2L\sum_{n\ge1}\dfrac{\sin(k_nx)\sin(k_nx')}{k_n^2}$,
$k_n=n\pi/L$ — summing to the §2.9 closed form $x_<(L-x_>)/L$.
*Check:* eigen-sum $=$ closed form ($10^{-4}$ at $N=2\times10^4$; the series
converges like $1/N$); BCs exact; unit kink in $G'$
(`test_p47_g1d_eigen`).

**Solution.** Eigenfunctions of $d^2/dx^2$ with Dirichlet ends:
$\psi_n=\sqrt{2/L}\sin k_nx$, eigenvalues $-k_n^2$, complete and
orthonormal. The (2.124) normalization has **no** $4\pi$:
$G_D=\sum_n\psi_n(x)\psi_n(x')/k_n^2$, the quoted series. Closed form: solve
directly — $G$ is linear on each side of $x'$ (no source), vanishes at both
ends, is continuous at $x'$, and its slope drops by 1 there:
$$G_D=\begin{cases}\alpha x,&x<x'\\ \beta(L-x),&x>x'\end{cases}
\;\Longrightarrow\;
\alpha x'=\beta(L-x'),\ \ \alpha+\beta=1
\;\Longrightarrow\;
G_D=\frac{x_<\,(L-x_>)}{L}.$$
Physical reading (§2.9): a string pulled transversally at $x'$ — the
triangle profile; or the potential of a unit charge between grounded points
in 1-D. The test verifies series $=$ triangle, the exact zeros, and the unit
kink.

### P48.  Exercise 4.14.5 — Finite cylinder by eigenfunctions; the sine sum rule  *(Wilcox 2e §4.16, p.201)*
Solve for $G_D$ inside the finite conducting cylinder (radius $a$, height
$L$) by a full eigenfunction expansion. Doing the $z$ eigensum should
reproduce Eq. (4.79); deduce from that the sum rule
$$\sum_{n=1}^\infty\frac{\sin(k_nz)\sin(k_nz')}{k^2+k_n^2}
=\frac L2\,\frac{\sinh(kz_<)\,\sinh\bigl(k(L-z_>)\bigr)}{k\,\sinh(kL)},
\qquad k_n=\frac{n\pi}L$$
($k$ a real parameter) — which also simplifies the Ex. 4.14.2 answer.
*Answer:* $G_D=4\pi\sum_{mnp}\psi\psi^*/\lambda$ with
$\psi=\mathcal J_{1m}(k_{mn}\rho)\frac{e^{im\phi}}{\sqrt{2\pi}}\sqrt{\frac2L}\sin\frac{p\pi z}L$,
$\lambda=k_{mn}^2+(p\pi/L)^2$; the sum rule as stated.
*Check:* sum rule at three $(k,z,z')$ ($10^{-8}$); the triple eigen-sum
equals the (4.79) $z$-reduced form at two interior points ($10^{-4}$)
(`test_p48_sine_sum_rule`).

**Solution.** The box eigenfunctions are the products quoted (Dirichlet
Fourier–Bessel radially, exponentials azimuthally, sines axially), with
$-\nabla^2\psi=\lambda\psi$. The 4.267/4.268 recipe gives
$G_D=4\pi\sum\psi(\vec x)\psi^*(\vec x')/\lambda$. Now fix $(m,n)$ and do
the $p$ sum: it is exactly
$\frac2L\sum_p\sin(k_pz)\sin(k_pz')/(k_{mn}^2+k_p^2)$ — and comparing with
the *reduced-Green-function* route to the same $G_D$ (Eq. (4.79), built in
§4.4 from $g=\sinh(kz_<)\sinh(k(L-z_>))/(k\sinh kL)$, which solves
$(k^2-\partial_z^2)g=\delta$ with grounded ends) forces, mode by mode,
$$\frac2L\sum_p\frac{\sin k_pz\,\sin k_pz'}{k^2+k_p^2}=g(k;z,z')$$
— the quoted rule (multiply by $L/2$). Direct proof without (4.79): expand
$g(k;z,z')$ itself in the sine basis; its coefficients are
$\int_0^Lg\sin k_pz\,dz=\sin(k_pz')/(k^2+k_p^2)$ by two integrations by
parts (the boundary terms vanish, the kink supplies the numerator). The rule
turns P45's $n$ sum into the exponentially convergent (4.79) form — the
identity the code's `G_plates_bessel`/`G_finite_cyl_79` exploit, and the
triple-sum test confirms end to end.

### P49.  Exercise 4.14.6 — Eigenfunctions inside a conducting sphere  *(Wilcox 2e §4.16, p.201)*
(a) Show that the Dirichlet eigenfunctions for the interior of a conducting
sphere are
$$\psi(r,\theta,\phi)\propto j_\ell(kr)\,Y_{\ell m}(\theta,\phi),$$
where the spherical Bessel function $j_\ell$ satisfies
$$\frac1{r^2}\frac d{dr}\Bigl(r^2\frac{dj_\ell(kr)}{dr}\Bigr)
+\Bigl(k^2-\frac{\ell(\ell+1)}{r^2}\Bigr)j_\ell(kr)=0 .$$
(b) How are the eigenvalues $k$ determined for radius $a$?
*Answer:* (a) as stated — the regular radial solution ($n_\ell$, the
singular partner, is excluded by the origin); (b) $j_\ell(ka)=0$, i.e.
$k=z_{\ell n}/a$ with $z_{\ell n}$ the $n$-th zero of $j_\ell$ (for
$\ell=0$: $z_{0n}=n\pi$, since $j_0=\sin t/t$).
*Check:* radial ODE residual $<10^{-5}$ (FD); zeros located by bracketing
satisfy $j_\ell=0$ to $10^{-12}$ and $z_{02}=2\pi$ exactly; radial
orthogonality $\int_0^ar^2j_\ell(z_{\ell n}r/a)j_\ell(z_{\ell n'}r/a)\,dr=0$
(`test_p49_spherical_eigenfunctions`).

**Solution.** (a) Separate the Helmholtz eigenproblem
$\nabla^2\psi=-k^2\psi$ in spherical coordinates: the angular operator is
$-\ell(\ell+1)$ on $Y_{\ell m}$ (the §4.13 separation), leaving the radial
equation quoted — Bessel's equation in disguise: substituting
$j_\ell(t)=\sqrt{\pi/2t}\,J_{\ell+1/2}(t)$ maps it to the half-odd-order
Bessel equation. Of the two solutions $j_\ell$ (regular, $\sim t^\ell$) and
$n_\ell$ (singular, $\sim t^{-\ell-1}$), the origin inside the domain keeps
only $j_\ell$.
(b) The Dirichlet wall demands $\psi(a,\theta,\phi)=0$ for all angles, i.e.
$j_\ell(ka)=0$: the spectrum is $k_{\ell n}=z_{\ell n}/a$, discrete and
$\ell$-dependent (degenerate in $m$: $2\ell+1$ each). These are the modes
that would assemble the sphere's interior $G_D$ as
$4\pi\sum\psi\psi^*/k^2$ — and, in Ch. 10, the resonant frequencies of the
spherical cavity. The $\ell=0$ tower $k=n\pi/a$ is the 1-D box in radial
disguise ($rj_0(kr)=\sin(kr)/k$ obeys P47's problem on $[0,a]$).
