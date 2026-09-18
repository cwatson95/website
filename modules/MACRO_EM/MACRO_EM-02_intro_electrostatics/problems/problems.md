# MACRO_EM-02 — Problems

Every exercise of Wilcox & Thron 2e, Ch. 2 (§2.14, printed pp.69–86; statements
condensed). **Gaussian units** as in the book: $\vec E=-\vec\nabla\Phi$,
$\vec\nabla\cdot\vec E=4\pi\rho$, $\Phi=q/r$. Check functions live in
`code/intro_electrostatics.py`; test names refer to `code/test_intro_electrostatics.py`.
Chapter results are cited by the book's equation numbers (map in `../notes.md`).

### P1.  Exercise 2.1.1 — Dipole potential: gradient and curl forms  *(Wilcox 2e §2.14, p.69)*
For $\Phi=\vec d\cdot\vec x/r^3$ with $\vec d$ constant and $r=|\vec x|$:
(a) compute $\vec E=-\vec\nabla\Phi$; (b) show the same field is a curl,
$\vec E=\vec\nabla\times\vec A$ with $\vec A=\vec d\times\vec x/r^3$ (away from
$\vec x=0$; the origin subtleties wait for §6.8).
*Answer:* $\vec E=[3(\vec d\cdot\hat x)\hat x-\vec d]/r^3$ — the point-dipole field —
and $\vec\nabla\times(\vec d\times\vec x/r^3)$ reproduces it exactly for $r\neq0$.
*Check:* `dipole_E` vs numeric gradient of `dipole_phi` and numeric curl of
`dipole_A` at random points. (`test_p1_dipole_gradient`, `test_p1_dipole_curl`.)

**Solution.** (a) Product rule with $\vec\nabla(\vec d\cdot\vec x)=\vec d$ and
$\vec\nabla r^{-3}=-3\,\vec x/r^5$:
$$\vec\nabla\Phi=\frac{\vec d}{r^3}+(\vec d\cdot\vec x)\Bigl(-\frac{3\vec x}{r^5}\Bigr)
\;\Longrightarrow\;
\vec E=-\vec\nabla\Phi=\frac{3(\vec d\cdot\hat x)\hat x-\vec d}{r^3},\qquad\hat x=\vec x/r.$$
(b) Use $\vec\nabla\times(\vec P\times\vec Q)=\vec P(\vec\nabla\cdot\vec Q)-\vec Q(\vec\nabla\cdot\vec P)+(\vec Q\cdot\vec\nabla)\vec P-(\vec P\cdot\vec\nabla)\vec Q$
with $\vec P=\vec d$ (constant: its divergence and directional derivatives vanish)
and $\vec Q=\vec x/r^3$:
$$\vec\nabla\times\Bigl(\vec d\times\frac{\vec x}{r^3}\Bigr)
=\vec d\,\Bigl(\vec\nabla\cdot\frac{\vec x}{r^3}\Bigr)-(\vec d\cdot\vec\nabla)\frac{\vec x}{r^3}.$$
First piece: $\vec\nabla\cdot(\vec x/r^3)=3/r^3+\vec x\cdot(-3\vec x/r^5)=0$ for $r\neq0$
(this is $\nabla^2(−1/r)$, WT 2.55, minus its delta). Second piece, component $i$:
$(\vec d\cdot\vec\nabla)(x_i r^{-3})=d_i r^{-3}+x_i\,\vec d\cdot(-3\vec x/r^5)
=d_i/r^3-3(\vec d\cdot\vec x)x_i/r^5$. Hence
$$\vec\nabla\times\vec A=-\frac{\vec d}{r^3}+\frac{3(\vec d\cdot\vec x)\vec x}{r^5}
=\frac{3(\vec d\cdot\hat x)\hat x-\vec d}{r^3}=\vec E.\qquad\blacksquare$$
Both routes agree numerically to $\sim10^{-8}$ at random points (central differences,
$h=10^{-5}$). A field that is simultaneously a gradient and a curl is harmonic
component-wise — possible here because $r\neq0$ excludes the source.

### P2.  Exercise 2.2.1 — Jacobians: |det M| as a volume, and UVW  *(Wilcox 2e §2.14, p.69)*
(a) Show the image of the unit cube under $x'_i=\sum_jM_{ij}x_j$ ($M$ nonsingular,
$3\times3$) is a parallelepiped of volume $|\det M|$ (hint: the image's edge vectors
are the columns of $M$, and a parallelepiped's volume is $|\vec v_3\cdot(\vec v_1\times\vec v_2)|$).
(b) Conclude that for *orthogonal* curvilinear coordinates $|\det M|=UVW$, the
product of the scale factors of WT (2.29).
*Answer:* (a) the triple product of the columns is exactly $\det M$;
(b) orthogonal columns of norms $U,V,W$ give $|\det|=UVW$.
*Check:* triple product = $|\det M|$ for random $M$; for the spherical map
$(r,\cos\theta,\phi)$, numeric $|\det J|=UVW=r^2$. (`test_p2_det_volume`,
`test_p2_scale_factors`.)

**Solution.** (a) The unit cube is $\{\sum_j t_j\hat e_j,\ t_j\in[0,1]\}$. Linearity
maps it to $\{\sum_j t_j\vec v_j\}$ with edge vectors $(\vec v_j)_i=M_{ij}$ — the
**columns** of $M$. That set is the parallelepiped spanned by $\vec v_1,\vec v_2,\vec v_3$,
whose volume is the scalar triple product
$$\mathrm{Vol}=|\vec v_3\cdot(\vec v_1\times\vec v_2)|
=\bigl|\epsilon_{ijk}(v_1)_i(v_2)_j(v_3)_k\bigr|
=\bigl|\epsilon_{ijk}M_{i1}M_{j2}M_{k3}\bigr|=|\det M|,$$
the Leibniz expansion of the determinant over columns. $\blacksquare$
(b) For a coordinate map $\vec x(u,v,w)$ the local linearization is
$M=\partial(x,y,z)/\partial(u,v,w)$, whose columns are $\partial\vec x/\partial u$,
$\partial\vec x/\partial v$, $\partial\vec x/\partial w$. *Orthogonal* system means
these are mutually perpendicular, with norms $U,V,W$ (WT 2.29). For a right-handed
orthogonal triple the triple product is the product of the norms:
$|\det M|=|\vec v_3\cdot(\vec v_1\times\vec v_2)|=W\,(UV)=UVW$ (the cross product of
two perpendicular vectors has magnitude $UV$ and points along $\vec v_3$). This is
WT (2.28) — the infinitesimal volume $d^3x=UVW\,du\,dv\,dw$. Numerically, for
spherical $(u,v,w)=(r,\cos\theta,\phi)$: $|\det J|=r^2=UVW$ to $10^{-7}$.

### P3.  Exercise 2.2.2 — Lorentzian delta sequences in 1-D and 2-D  *(Wilcox 2e §2.14, p.69)*
(a) Show $\displaystyle\lim_{\epsilon\to0^+}\frac1\pi\frac{\epsilon}{x^2+\epsilon^2}=\delta(x)$.
(b) By the same reasoning in two dimensions ($\vec x=x\hat i+y\hat j$), show
$\displaystyle\lim_{\epsilon\to0^+}\frac1{2\pi}\frac{\epsilon}{(\vec x^2+\epsilon^2)^{3/2}}=\delta^{(2)}(\vec x)$.
*Answer:* each family has unit integral for every $\epsilon$ and concentrates at the
origin, so it samples test functions at $0$ — the defining property WT (2.8)–(2.10).
*Check:* $\int\varphi_\epsilon=1$ exactly; $\int\varphi_\epsilon f\to f(0)$ with the
error $\to0$ as $\epsilon\downarrow0$. (`test_p3_lorentzian_delta`, `test_p3_delta2d`.)

**Solution.** (a) Write $\varphi_\epsilon(x)=\epsilon^{-1}f(x/\epsilon)$ with
$f(s)=1/[\pi(1+s^2)]$: indeed $\frac1\pi\frac{\epsilon}{x^2+\epsilon^2}
=\frac1\epsilon\cdot\frac1{\pi(1+x^2/\epsilon^2)}$. $f$ is nonnegative and
$$\int_{-\infty}^\infty f(s)\,ds=\frac1\pi\arctan s\Big|_{-\infty}^{\infty}=\frac1\pi\cdot\pi=1,$$
so by WT (2.9)–(2.10) the family is a delta sequence. Concretely, for continuous
bounded $g$: substituting $x=\epsilon s$,
$\int\varphi_\epsilon g\,dx=\int f(s)g(\epsilon s)\,ds\to g(0)$ (dominated
convergence: $|f g|\le\|g\|_\infty f$). Numerically with $g=\cos$, the integral is
$e^{-\epsilon}\to1=g(0)$.
(b) Radial symmetry: total mass with $\rho^2=x^2+y^2$,
$$\int d^2x\,\frac{\epsilon}{2\pi(\rho^2+\epsilon^2)^{3/2}}
=\epsilon\int_0^\infty\frac{\rho\,d\rho}{(\rho^2+\epsilon^2)^{3/2}}
=\epsilon\Bigl[-\frac1{\sqrt{\rho^2+\epsilon^2}}\Bigr]_0^\infty=\epsilon\cdot\frac1\epsilon=1$$
for every $\epsilon$. And for fixed $\vec x\neq0$ the density
$\le\epsilon/2\pi\rho^3\to0$. Scaling form: $\varphi_\epsilon(\vec x)=\epsilon^{-2}f(\vec x/\epsilon)$
with $f(\vec s)=1/[2\pi(s^2+1)^{3/2}]$, nonnegative with unit integral — the 2-D
version of (2.9). Hence $\int\varphi_\epsilon g\,d^2x\to g(0)$: the family tends to
$\delta^{(2)}(\vec x)$. $\blacksquare$ (Physically this $\varphi_\epsilon$ is the
charge density a grounded plane "sees" from a point charge at height $\epsilon$ —
the image-plane induced density of Ch. 3.)

### P4.  Exercise 2.2.3 — Delta function in spherical coordinates  *(Wilcox 2e §2.14, p.70)*
With $x=r\sin\theta\cos\phi$, $y=r\sin\theta\sin\phi$, $z=r\cos\theta$ and new
coordinates $u=r$, $v=\cos\theta$, $w=\phi$, find $\delta(\vec x-\vec x')$ using
(a) the transformation determinant (WT 2.25), (b) scale factors. [Book's answer:
$\delta(\vec x-\vec x')=r^{-2}\,\delta(r-r')\,\delta(\cos\theta-\cos\theta')\,\delta(\phi-\phi')$.]
*Answer:* $|\det\partial(x,y,z)/\partial(r,\cos\theta,\phi)|=r^2$, so
$\delta^{(3)}=\delta(r-r')\delta(\cos\theta-\cos\theta')\delta(\phi-\phi')/r^2$.
*Check:* numeric Jacobian determinant $=r^2$ and scale-factor product $=r^2$ at
random points. (`test_p4_spherical_delta_jacobian`.)

**Solution.** (a) Write $\mu=\cos\theta$, $s=\sin\theta=\sqrt{1-\mu^2}$, so
$\vec x=(rs\cos\phi,\ rs\sin\phi,\ r\mu)$. The Jacobian matrix has columns
$\partial\vec x/\partial r=(s\cos\phi,s\sin\phi,\mu)$,
$\partial\vec x/\partial\mu=(-r\mu\cos\phi/s,\ -r\mu\sin\phi/s,\ r)$
(using $\partial s/\partial\mu=-\mu/s$), and
$\partial\vec x/\partial\phi=(-rs\sin\phi,\ rs\cos\phi,\ 0)$. Expanding along the
third column (or multiplying out) gives
$$\det\frac{\partial(x,y,z)}{\partial(r,\mu,\phi)}
=r^2\bigl[s^2+\mu^2\bigr]\cdot1=r^2 ,$$
(one clean route: this map is spherical $(r,\theta,\phi)$ — Jacobian $r^2\sin\theta$ —
composed with $\theta\mapsto\mu$, which contributes $|d\theta/d\mu|=1/\sin\theta$;
the product is $r^2$). WT (2.25) then gives
$$\delta(\vec x-\vec x')=\frac{\delta(r-r')\,\delta(\cos\theta-\cos\theta')\,\delta(\phi-\phi')}{r^2}. \qquad\blacksquare$$
(b) Scale factors: the three columns above are mutually orthogonal (spherical is an
orthogonal system, and replacing $\theta$ by $\mu$ rescales one column without
rotating it). Norms: $U=|\partial\vec x/\partial r|=1$;
$V=|\partial\vec x/\partial\mu|=\sqrt{r^2\mu^2/s^2+r^2}=r/s$;
$W=|\partial\vec x/\partial\phi|=rs$. Product $UVW=1\cdot(r/s)\cdot rs=r^2$ — same
denominator, by P2(b). Note the $\mu=\cos\theta$ choice absorbs the usual
$\sin\theta$: $d^3x=r^2\,dr\,d\mu\,d\phi$ with no angular weight, which is why the
book prefers it.

### P5.  Exercise 2.2.4 — Delta function in oblate spheroidal coordinates  *(Wilcox 2e §2.14, p.70)*
Oblate spheroidal coordinates ($\xi\ge0$, $0\le\theta\le\pi$, $0\le\phi\le2\pi$, $R>0$ constant):
$$x=R\sqrt{\xi^2+1}\,\sin\theta\cos\phi,\quad
  y=R\sqrt{\xi^2+1}\,\sin\theta\sin\phi,\quad
  z=R\,\xi\cos\theta,$$
with new coordinates $u=\xi$, $v=\cos\theta$, $w=\phi$ ($R\xi\to r$ only for
$\xi\gg1$). Find the form of $\delta(\vec x-\vec x')$.
*Answer:* $|\det J|=R^3(\xi^2+\cos^2\theta)$, so
$$\delta(\vec x-\vec x')=\frac{\delta(\xi-\xi')\,\delta(\cos\theta-\cos\theta')\,\delta(\phi-\phi')}{R^3\,(\xi^2+\cos^2\theta)}.$$
*Check:* numeric Jacobian and scale-factor product both equal
$R^3(\xi^2+\cos^2\theta)$ at random $(\xi,\theta,\phi)$. (`test_p5_oblate_delta_jacobian`.)

**Solution.** Write $\mu=\cos\theta$, $s=\sin\theta$, $A=\sqrt{\xi^2+1}$. Scale
factors (the system is orthogonal in $(\xi,\theta,\phi)$, hence in $(\xi,\mu,\phi)$):
- $\partial\vec x/\partial\xi=\bigl(R\xi s\cos\phi/A,\ R\xi s\sin\phi/A,\ R\mu\bigr)$, so
$$h_\xi^2=R^2\Bigl(\frac{\xi^2s^2}{\xi^2+1}+\mu^2\Bigr)
=R^2\,\frac{\xi^2s^2+(\xi^2+1)\mu^2}{\xi^2+1}
=R^2\,\frac{\xi^2+\mu^2}{\xi^2+1},$$
using $s^2+\mu^2=1$.
- $\partial\vec x/\partial\theta=(RA\mu\cos\phi,\ RA\mu\sin\phi,\ -R\xi s)$, so
$h_\theta=R\sqrt{A^2\mu^2+\xi^2s^2}=R\sqrt{\xi^2+\mu^2}$; converting to
$v=\mu$ costs $|d\theta/d\mu|=1/s$:
$h_\mu=R\sqrt{\xi^2+\mu^2}/s$.
- $h_\phi=RA\,s=R\sqrt{\xi^2+1}\,s$.

Product (= $|\det J|$ by P2(b)):
$$h_\xi h_\mu h_\phi=R\sqrt{\frac{\xi^2+\mu^2}{\xi^2+1}}\cdot\frac{R\sqrt{\xi^2+\mu^2}}{s}\cdot R\sqrt{\xi^2+1}\,s
=R^3\,(\xi^2+\mu^2)=R^3(\xi^2+\cos^2\theta).$$
Hence by WT (2.25)
$$\delta(\vec x-\vec x')=\frac{\delta(\xi-\xi')\,\delta(\cos\theta-\cos\theta')\,\delta(\phi-\phi')}
{R^3(\xi^2+\cos^2\theta)}. \qquad\blacksquare$$
Sanity limits: $\xi\gg1$ gives $R^3\xi^2\to r^2/R\cdot R^2$, matching spherical with
$r=R\xi$ (P4). The factor vanishes at $\xi=0,\ \theta=\pi/2$ — the focal ring
$\rho=R$, where the coordinates degenerate; that ring is exactly the rim of the
charged disk in P12 (Exercise 2.6.1), which is why the disk problem is natural in
these coordinates.

### P6.  Exercise 2.4.1 — Gauss law and the log potential in two dimensions  *(Wilcox 2e §2.14, pp.70–71)*
In 2-D take $\vec E(\vec x)=\int da'\,\sigma(\vec x')\,(\vec x-\vec x')/|\vec x-\vec x'|^2$.
(a) Argue, mirroring the §2.4 solid-angle construction, that
$\oint_C d\ell\,\hat n\cdot\vec E=2\pi\sum_{j\,\text{in}\,S}q_j$ for point charges and
$\vec\nabla\cdot\vec E=2\pi\sigma$ for continuous densities.
(b) For a unit point charge at the origin show
$\nabla^2\ln(|\vec x-\vec x'|/K)=2\pi\,\delta^{(2)}(\vec x-\vec x')$, $K>0$ arbitrary.
(c) Confirm by integrating both sides over a disk about the origin.
(d) The 2-D point-charge potential is thus $-\ln(|\vec x-\vec x'|/K)$; but a unit
line charge in 3-D has potential $-2\ln(|\vec x-\vec x'|/K)$. Where does the 2 come from?
*Answer:* (a) the planar angle subtended by a closed curve is $2\pi$ from inside, $0$
from outside; (b,c) both sides integrate to $2\pi$; (d) 3-D Gauss carries $4\pi q$
where 2-D carries $2\pi q$ — the 3-D line field is $E_\rho=2\lambda/\rho$, twice the
2-D unit-charge field $1/\rho$.
*Check:* `flux2d` of `E2d_point` $=2\pi$ (inside) / $0$ (outside) by quadrature;
5-point Laplacian of $\ln r$ vanishes off-origin while the flux form of
$\int\nabla^2\ln r\,da=2\pi$; line-charge field vs $2\lambda/\rho$.
(`test_p6_flux2d`, `test_p6_log_laplacian`.)

**Solution.** (a) For a unit charge at $\vec x_j$, the flux element through arc
$d\ell$ of $C$ is $d\ell\,\hat n\cdot(\vec x-\vec x_j)/|\vec x-\vec x_j|^2=d\theta_j$
— the **plane angle** subtended by $d\ell$ at $\vec x_j$ (the 2-D copy of WT 2.42:
$d\ell_\parallel/\rho$ instead of $ds_\parallel/r^2$). Closing the curve,
$\oint d\theta_j=2\pi$ if $\vec x_j$ is enclosed (full horizon) and $0$ otherwise
(front/back cancellation) — the same in/out dichotomy as WT Figs. 2.7–2.8, one
dimension down. Superposing, $\oint d\ell\,\hat n\cdot\vec E=2\pi\sum_{\rm in}q_j$;
smearing $q_j\to\sigma\,da$ and applying the 2-D divergence theorem to arbitrary
regions equates integrands: $\vec\nabla\cdot\vec E=2\pi\sigma$. $\blacksquare$
(b) For $q=1$ at $\vec x'$: $\vec E=(\vec x-\vec x')/|\vec x-\vec x'|^2
=\vec\nabla\ln|\vec x-\vec x'|=\vec\nabla\ln(|\vec x-\vec x'|/K)$ (the constant $K$
only fixes the zero of the log and drops under $\vec\nabla$ — needed because a pure
$\ln|\vec x|$ has dimensions inside the log). By (a),
$\vec\nabla\cdot\vec E=2\pi\delta^{(2)}(\vec x-\vec x')$, i.e.
$\nabla^2\ln(|\vec x-\vec x'|/K)=2\pi\delta^{(2)}(\vec x-\vec x')$. Note also
directly $\nabla^2\ln\rho=\rho^{-1}\partial_\rho(\rho\,\partial_\rho\ln\rho)=\rho^{-1}\partial_\rho(1)=0$ for $\rho\neq0$.
(c) Put $\vec x'=0$, integrate over the disk $\rho\le R$: right side gives $2\pi$
by the sampling property. Left side, by the 2-D divergence theorem:
$\int\nabla^2\ln(\rho/K)\,da=\oint_{\rho=R}\partial_\rho\ln(\rho/K)\,R\,d\phi
=\frac1R\cdot R\cdot2\pi=2\pi$. Equal, for every $R$ — consistent. $\blacksquare$
(d) The two "unit charges" are normalized by different Gauss laws. 2-D:
$E\cdot2\pi\rho=2\pi q\Rightarrow E=1/\rho$, potential $-\ln(\rho/K)$. A unit-density
line in 3-D: $E\cdot2\pi\rho=4\pi\lambda\Rightarrow E=2\lambda/\rho$, potential
$-2\lambda\ln(\rho/K)$ (also obtainable by integrating $dz'/\sqrt{\rho^2+z'^2}$ with a
cutoff, P7). The extra 2 is the ratio $4\pi/2\pi$ of the solid angle of a sphere to
the angle of a circle — a bookkeeping constant between dimensions, not new physics.

### P7.  Exercise 2.4.2 — Crossed finite line charges  *(Wilcox 2e §2.14, pp.71–72)*
(a) Two lines of length $2L$, both with uniform density $\lambda$, lie along the
$x$- and $y$-axes crossing at the origin (a "+", Fig. 2.16). Find the exact
$\Phi(x,y,z)$ and show that for $L\gg|x|,|y|,|z|$
$$\Phi\approx-\lambda\,\ln\!\Bigl[\frac{(x^2+z^2)(y^2+z^2)}{16L^4}\Bigr],$$
and explain why this is the expected form given P6. (b) For $L\ll|x|,|y|,|z|$ show
the potential reduces to that of a point charge of the right size. (c) Now keep
only the *positive* $x$- and $y$-axis halves ($0$ to $L$), with density $-\lambda$
on the $x$-line and $+\lambda$ on the $y$-line; find the exact potential and show
for $L\gg|x|,|y|,|z|$ that $\Phi\approx-\lambda\ln[(r-y)/(r-x)]$, $r=\sqrt{x^2+y^2+z^2}$.
*Answer:* each finite line gives
$\lambda[\sinh^{-1}\frac{L-\zeta}{b}+\sinh^{-1}\frac{L+\zeta}{b}]$ ($\zeta$ = coordinate
along the line, $b$ = transverse distance); the limits follow from
$\sinh^{-1}u\approx\ln2u$ and $\sqrt{u^2+b^2}\approx u+b^2/2u$.
*Check:* closed form vs direct quadrature; asymptotic ratios $\to1$ at $L/r=10^3$;
monopole limit $4\lambda L/r$. (`test_p7_plus_potential`, `test_p7_halflines`.)

**Solution.** The single-line building block, for a line along $x$ from $x_1$ to
$x_2$ seen from $(x,y,z)$ with $b^2=y^2+z^2$:
$$\Phi_{\rm line}=\lambda\int_{x_1}^{x_2}\frac{dx'}{\sqrt{(x-x')^2+b^2}}
=\lambda\Bigl[\sinh^{-1}\frac{x_2-x}{b}-\sinh^{-1}\frac{x_1-x}{b}\Bigr],$$
since $\int du/\sqrt{u^2+b^2}=\sinh^{-1}(u/b)=\ln(u+\sqrt{u^2+b^2})-\ln b$.
(a) Superpose the $x$-line ($x_{1,2}=\mp L$, $b_1^2=y^2+z^2$) and the $y$-line
($b_2^2=x^2+z^2$):
$$\Phi=\lambda\ln\frac{L-x+\sqrt{(L-x)^2+b_1^2}}{-(L+x)+\sqrt{(L+x)^2+b_1^2}}
      +\lambda\ln\frac{L-y+\sqrt{(L-y)^2+b_2^2}}{-(L+y)+\sqrt{(L+y)^2+b_2^2}}.$$
For $L\gg$ everything: numerator $\to2L$; denominator
$\sqrt{(L+x)^2+b^2}-(L+x)=\dfrac{b^2}{\sqrt{(L+x)^2+b^2}+(L+x)}\to\dfrac{b^2}{2L}$.
Each log $\to\ln(4L^2/b^2)$, so
$$\Phi\approx\lambda\ln\frac{4L^2}{y^2+z^2}+\lambda\ln\frac{4L^2}{x^2+z^2}
=-\lambda\ln\frac{(x^2+z^2)(y^2+z^2)}{16L^4}. \qquad\blacksquare$$
This is exactly two copies of the 3-D line-charge potential $-2\lambda\ln(b/K)$ of
P6(d), one per line, with the cutoff scale $K=2L$ set by the line length — the
finite ends regulate the log divergence.
(b) For $L\ll r$: $\sinh^{-1}\frac{L\mp\zeta}{b}$ expands as
$\int dx'/\sqrt{\cdots}\approx2L/r$ per line (the integrand is $\approx1/r$ across
the whole segment), so $\Phi\approx\lambda(2L/r)+\lambda(2L/r)=4\lambda L/r=Q_{\rm tot}/r$
with $Q_{\rm tot}=2\times2L\lambda$ — the expected monopole.
(c) Half-lines: $+\lambda$ on $0\le y'\le L$, $-\lambda$ on $0\le x'\le L$:
$$\Phi=\lambda\Bigl[\sinh^{-1}\frac{L-y}{b_2'}+\ln\frac{b_2'}{r-y}\Bigr]
      -\lambda\Bigl[\sinh^{-1}\frac{L-x}{b_1'}+\ln\frac{b_1'}{r-x}\Bigr]$$
— more transparently, using the antiderivative directly,
$$\Phi=\lambda\ln\frac{L-y+\sqrt{(L-y)^2+x^2+z^2}}{r-y}
      -\lambda\ln\frac{L-x+\sqrt{(L-x)^2+y^2+z^2}}{r-x},$$
where the lower limits produced $\sqrt{y^2+x^2+z^2}-y=r-y$ and $r-x$. For
$L\gg|x|,|y|,|z|$ both numerators $\to2L$ and cancel between the two logs:
$$\Phi\approx\lambda\ln\frac{2L}{r-y}-\lambda\ln\frac{2L}{r-x}
=-\lambda\ln\frac{r-y}{r-x}. \qquad\blacksquare$$
The $L$-dependence drops because the far ends of the $\pm\lambda$ lines cancel; what
survives is the near-origin imbalance. (The equipotentials $r-y=c(r-x)$ are the
cones of the classic "bent-wire" problem.)

### P8.  Exercise 2.4.3 — On-axis field of a charged cylinder  *(Wilcox 2e §2.14, p.71)*
A solid cylinder of radius $b$ and thickness $a$ (faces at $z=\pm a/2$, Fig. 2.17)
carries constant charge density $\rho$. (a) Find $E_z(z)$ on the symmetry axis.
(b) Show that near the center $E_z=\text{(const)}\cdot z$ and find the constant.
Can the $b\gg a$ limit be predicted easily?
*Answer:* stacking charged disks,
$$E_z(z)=2\pi\rho\Bigl[\textstyle\int_{-a/2}^{a/2}\mathrm{sgn}(z-z')\,dz'
-\sqrt{(z+\frac a2)^2+b^2}+\sqrt{(z-\frac a2)^2+b^2}\Bigr],$$
and near the origin $E_z\approx4\pi\rho\bigl[1-a/\sqrt{a^2+4b^2}\bigr]\,z$; for
$b\gg a$ the constant $\to4\pi\rho$ — the interior of an infinite slab, predictable
from Gauss.
*Check:* closed form vs direct quadrature over the volume; numeric slope at $0$;
slab limit. (`test_p8_cylinder_axis`.)

**Solution.** (a) The on-axis field of a uniform disk (radius $b$, surface density
$\sigma$, at $z'=0$) follows from the ring formula (P9a) integrated over radius:
$E_z^{\rm disk}(z)=2\pi\sigma[\mathrm{sgn}(z)-z/\sqrt{z^2+b^2}]$. Slice the cylinder
into disks $\sigma=\rho\,dz'$ at height $z'$ and superpose:
$$E_z(z)=2\pi\rho\int_{-a/2}^{a/2}\Bigl[\mathrm{sgn}(z-z')-\frac{z-z'}{\sqrt{(z-z')^2+b^2}}\Bigr]dz'.$$
Both pieces integrate exactly. With $\int\mathrm{sgn}(z-z')dz'=a$, $2z$, $-a$ for
$z>a/2$, $|z|\le a/2$, $z<-a/2$, and
$\frac{d}{dz'}\sqrt{(z-z')^2+b^2}=-\frac{z-z'}{\sqrt{(z-z')^2+b^2}}$:
$$E_z(z)=2\pi\rho\Bigl[\{a,\,2z,\,-a\}-\sqrt{(z+\tfrac a2)^2+b^2}+\sqrt{(z-\tfrac a2)^2+b^2}\Bigr].$$
(b) Inside, set $f(z)=\sqrt{(z+\frac a2)^2+b^2}-\sqrt{(z-\frac a2)^2+b^2}$;
$f(0)=0$ and
$$f'(0)=\frac{a/2}{\sqrt{a^2/4+b^2}}+\frac{a/2}{\sqrt{a^2/4+b^2}}
=\frac{a}{\sqrt{a^2/4+b^2}}=\frac{2a}{\sqrt{a^2+4b^2}} .$$
So $E_z\approx2\pi\rho[2z-f'(0)z]=4\pi\rho\Bigl[1-\dfrac{a}{\sqrt{a^2+4b^2}}\Bigr]z$:
$$\text{Constant}=4\pi\rho\Bigl[1-\frac{a}{\sqrt{a^2+4b^2}}\Bigr].$$
For $b\gg a$ the bracket $\to1$ and $E_z\to4\pi\rho z$ — predictable *without*
calculation: an infinite slab has, by Gauss on a pillbox straddling $|z|$,
$2E_z=4\pi\rho\cdot2z$, i.e. $E_z=4\pi\rho z$; the edge correction
$-a/\sqrt{a^2+4b^2}\approx-a/2b$ is the finite-radius leak. (Both linear
coefficients are checked numerically against a symmetric-difference slope.)

### P9.  Exercise 2.4.4 — Ring field and the truncated cone  *(Wilcox 2e §2.14, pp.72–73)*
(a) A circular loop of radius $R$ in the $x$–$y$ plane with uniform linear density
$\lambda$: show the axial field is $E_z=2\pi\lambda R\,z/[R^2+z^2]^{3/2}$.
(b) A cone of (half-)opening angle $\alpha$ about the $z$-axis, truncated so its
surface runs from axial distance $L_1$ to $L_2$ from the theoretical tip at the
origin (Fig. 2.18), carries uniform *surface* density $\sigma$. Using (a), evaluate
$E_z$ at the tip.
*Answer:* (a) $q_{\rm ring}=2\pi R\lambda$ at hoop distance $\sqrt{R^2+z^2}$ gives the
stated field. (b) $E_z(0)=-2\pi\sigma\sin\alpha\cos\alpha\,\ln(L_2/L_1)$
($=-\pi\sigma\sin2\alpha\ln\frac{L_2}{L_1}$; directed away from the cone for $\sigma>0$).
*Check:* ring closed form vs quadrature and vs point limit $z\gg R$; cone closed form
vs 2-D surface quadrature. (`test_p9_ring_and_cone`.)

**Solution.** (a) Every element $dq=\lambda R\,d\phi$ sits at distance
$s=\sqrt{R^2+z^2}$ from the axis point $(0,0,z)$. Transverse components cancel by
symmetry; the axial projection is $z/s$:
$$E_z=\oint\frac{dq}{s^2}\cdot\frac zs=\frac{2\pi R\lambda\,z}{(R^2+z^2)^{3/2}}. \qquad\blacksquare$$
(Limit $z\gg R$: $E_z\to2\pi R\lambda/z^2=q_{\rm ring}/z^2$ ✓.)
(b) Parametrize the cone surface by the axial coordinate $z'\in[L_1,L_2]$: the ring
at height $z'$ has radius $\rho'=z'\tan\alpha$ and slant width
$d\ell=dz'/\cos\alpha$, hence charge
$dq=\sigma\,2\pi\rho'\,d\ell=2\pi\sigma\tan\alpha\,z'\,dz'/\cos\alpha$.
By (a) with the field point at the origin ($z=0$, i.e. axial offset $-z'$):
$$dE_z=\frac{dq\,(0-z')}{(z'^2+\rho'^2)^{3/2}}
=-dq\,\frac{z'}{z'^3(1+\tan^2\alpha)^{3/2}}=-dq\,\frac{\cos^3\alpha}{z'^2},$$
using $1+\tan^2\alpha=1/\cos^2\alpha$. So
$$E_z(0)=-2\pi\sigma\frac{\tan\alpha}{\cos\alpha}\cos^3\alpha\int_{L_1}^{L_2}\frac{z'\,dz'}{z'^2}
=-2\pi\sigma\sin\alpha\cos\alpha\,\ln\frac{L_2}{L_1}. \qquad\blacksquare$$
Every ring contributes $\propto dz'/z'$ — the cone is the classic *logarithmic*
geometry (self-similar: each octave of distance contributes equally). The sign says
the field at the tip points *away* from the (positive) cone, down the $-z$ axis;
the magnitude $\pi\sigma\sin2\alpha\ln(L_2/L_1)$ is extremal at $\alpha=45°$.
### P10.  Exercise 2.5.1 — Cavendish spheres with a $1/r^{1+\epsilon}$ potential  *(Wilcox 2e §2.14, pp.73–74)*
Assume the modified potential $\Phi=(1+\epsilon)^{-1}\int d^3x'\,\rho(\vec x')/|\vec x-\vec x'|^{1+\epsilon}$,
$|\epsilon|\ll1$ (WT 2.59). (a) For concentric conducting spheres of radii $a<b$ and
charges $q_a,q_b$, show the potential in $a\le r\le b$ is
$\Phi(r)=\Phi_{\rm out}(r)+\Phi_{\rm in}(r)$ with the shell forms (2.62)–(2.63).
(b) After wiring the spheres together ($\Phi(a)=\Phi(b)$), show
$$q_a\approx\frac{q_b\,\epsilon}{2(a-b)}\Bigl[b\ln\frac{b-a}{a+b}+a\ln\frac{4b^2}{b^2-a^2}\Bigr]$$
(use $x^{1-\epsilon}=xe^{-\epsilon\ln x}\approx x(1-\epsilon\ln x)$).
(c) Is there a quick way to fix the sign of $q_a$ from the signs of $\epsilon$ and $q_b$?
*Answer:* (a) the shell integral gives
$\Phi_{\rm shell}(r)=\frac{q}{1-\epsilon^2}\frac{(r+s)^{1-\epsilon}-|r-s|^{1-\epsilon}}{2sr}$
(shell radius $s$); (b) as stated — $q_a=O(\epsilon)$, vanishing for exact
inverse-square; (c) yes: for $\epsilon>0$ a shell's interior potential *rises*
outward, so the inner sphere must take on same-sign charge:
$\mathrm{sgn}\,q_a=\mathrm{sgn}(\epsilon q_b)$.
*Check:* closed shell form vs surface quadrature at finite $\epsilon$; the exact
linear solve for $q_a$ vs the first-order formula as $\epsilon\to0$.
(`test_p10_shell_potential_eps`, `test_p10_qa_approx`.)

**Solution.** (a) For a uniform shell of radius $s$, charge $q$, surface density
$\sigma=q/4\pi s^2$, put the field point at distance $r$ and use the axial angle
$\theta$ of the source point: $u^2\equiv|\vec x-\vec x'|^2=r^2+s^2-2rs\cos\theta$,
so $u\,du=rs\sin\theta\,d\theta$ and $da'=s^2\sin\theta\,d\theta\,d\phi$:
$$\Phi_{\rm shell}(r)=\frac{\sigma}{1+\epsilon}\int\frac{da'}{u^{1+\epsilon}}
=\frac{2\pi s^2\sigma}{1+\epsilon}\int_{|r-s|}^{r+s}\frac{u\,du}{rs\,u^{1+\epsilon}}
=\frac{q}{2rs}\,\frac{(r+s)^{1-\epsilon}-|r-s|^{1-\epsilon}}{(1+\epsilon)(1-\epsilon)},$$
i.e. $\Phi_{\rm shell}=\dfrac{q}{1-\epsilon^2}\dfrac{(r+s)^{1-\epsilon}-|r-s|^{1-\epsilon}}{2rs}$.
With $s=a\le r$ this is $\Phi_{\rm out}$ (2.62) ($|r-a|=r-a$); with $s=b\ge r$ it is
$\Phi_{\rm in}$ (2.63) ($|r-b|=b-r$). Superposition gives $\Phi=\Phi_{\rm out}+\Phi_{\rm in}$
in the gap. (Conductors keep each shell uniform by symmetry, so this is exact.) $\blacksquare$
(b) Impose $\Phi(a)=\Phi(b)$ and multiply through by $2ab(1-\epsilon^2)$:
$$q_a\underbrace{\Bigl[\tfrac ba(2a)^{1-\epsilon}-(a+b)^{1-\epsilon}+(b-a)^{1-\epsilon}\Bigr]}_{\mathcal A}
=q_b\underbrace{\Bigl[\tfrac ab(2b)^{1-\epsilon}-(a+b)^{1-\epsilon}+(b-a)^{1-\epsilon}\Bigr]}_{\mathcal B}.$$
Expand $x^{1-\epsilon}\approx x(1-\epsilon\ln x)$. The $O(1)$ parts:
$\mathcal A_0=2b-(a+b)+(b-a)=2(b-a)$, while
$\mathcal B_0=2a-(a+b)+(b-a)=0$ — the whole right bracket is first order, which is
the Cavendish point: $q_a=O(\epsilon)$. The $O(\epsilon)$ part of $\mathcal B$:
$$\mathcal B_1=-\epsilon\bigl[2a\ln2b-(a+b)\ln(a+b)+(b-a)\ln(b-a)\bigr].$$
Hence $q_a\approx q_b\,\mathcal B_1/\mathcal A_0=-\dfrac{q_b\,\epsilon}{2(b-a)}\,N$ with
$N=2a\ln2b-(a+b)\ln(a+b)+(b-a)\ln(b-a)$. Regroup $N$ by collecting the $a$- and
$b$-coefficients of the logs:
$$N=b\bigl[\ln(b-a)-\ln(a+b)\bigr]+a\bigl[2\ln2b-\ln(a+b)-\ln(b-a)\bigr]
=b\ln\frac{b-a}{a+b}+a\ln\frac{4b^2}{b^2-a^2},$$
so, flipping the denominator sign,
$$q_a\approx\frac{q_b\,\epsilon}{2(a-b)}\Bigl[b\ln\frac{b-a}{a+b}+a\ln\frac{4b^2}{b^2-a^2}\Bigr]. \qquad\blacksquare$$
(Numerically, $a=1,b=2$: $N=2\ln4-3\ln3=-0.5232$, so
$q_a=-\epsilon q_bN/[2(b-a)]=+0.2616\,\epsilon\,q_b$; the exact linear solve at
$\epsilon=10^{-4}$ matches to $\sim10^{-4}$ relative.)
(c) Expand the outer shell's interior potential to first order:
$\Phi_{\rm in}(r)\approx q_b\bigl[\frac1b-\epsilon\bigl(\frac{\ln b+1}{b}-\frac{r^2}{6b^3}\bigr)\bigr]$,
which **increases with $r$ when $\epsilon>0$** (faster-than-Coulomb fall-off makes
the near wall dominate). So with $q_a=0$ the inner sphere would sit *below* the
outer's potential ($q_b>0$); since a charge $q_a$ raises $\Phi(a)$ by
$\approx q_a/a$ but $\Phi(b)$ only by $\approx q_a/b$, equalization needs $q_a>0$:
same sign as $q_b$. Flipping $\epsilon$ or $q_b$ flips the argument:
$\mathrm{sgn}\,q_a=\mathrm{sgn}(\epsilon\,q_b)$ — matching (b) since the bracket
$N/(a-b)>0$.

### P11.  Exercise 2.5.2 — Cavendish with a Yukawa potential (photon mass)  *(Wilcox 2e §2.14, p.74)*
Suppose the point potential is $\Phi=\exp(-|\vec x-\vec x'|/R)/|\vec x-\vec x'|$ with
$R$ very large. For the Fig. 2.10 setup (concentric conducting spheres $a<b$ wired
together): (a) given $q_b$ on the outer sphere, find $q_a$ (book answer:
$$q_a=q_b\;\frac{\frac ab\bigl(1-e^{-2b/R}\bigr)-e^{(a-b)/R}+e^{-(a+b)/R}}
             {\frac ba\bigl(1-e^{-2a/R}\bigr)-e^{(a-b)/R}+e^{-(a+b)/R}}\;);$$
(b) show for $R\gg a,b$ that $q_a\approx q_b\,\frac{ab}{6R^2}(1+\frac ab)$ — same
sign as $q_b$. ($R=\hbar/m_\gamma c$ connects the null test to the photon mass.)
*Answer:* (a) as displayed — from the shell potential
$\varphi_s(r)=\frac{qR}{2sr}[e^{-|r-s|/R}-e^{-(r+s)/R}]$ and $\Phi(a)=\Phi(b)$;
(b) the $1/R$ and $1/R^2$ terms cancel, leaving
$q_a\to q_b\,a(a+b)/6R^2$.
*Check:* shell closed form vs quadrature; the ratio formula vs an independent
linear solve; the approximation at $R/b=50$. (`test_p11_yukawa_shell`, `test_p11_qa_yukawa`.)

**Solution.** (a) Same substitution as P10(a) — the "perfect differential" hint:
with $u=|\vec x-\vec x'|$, $\int da'\,f(u)=\frac{2\pi s}{r}\int_{|r-s|}^{r+s}u f(u)\,du$,
and here $uf(u)=e^{-u/R}$ integrates immediately:
$$\varphi_s(r)=\frac{q}{4\pi s^2}\,\frac{2\pi s}{r}\,R\bigl[e^{-|r-s|/R}-e^{-(r+s)/R}\bigr]
=\frac{qR}{2sr}\bigl[e^{-|r-s|/R}-e^{-(r+s)/R}\bigr].$$
Evaluate the four combinations:
$$\varphi_a(a)=\frac{q_aR}{2a^2}\bigl(1-e^{-2a/R}\bigr),\qquad
\varphi_b(a)=\varphi_a(b)=\frac{R}{2ab}\,q_{b,a}\bigl[e^{-(b-a)/R}-e^{-(a+b)/R}\bigr],$$
$$\varphi_b(b)=\frac{q_bR}{2b^2}\bigl(1-e^{-2b/R}\bigr).$$
The wire enforces $\varphi_a(a)+\varphi_b(a)=\varphi_a(b)+\varphi_b(b)$; multiplying
by $2ab/R$ and collecting the $q_a$ and $q_b$ terms:
$$q_a\Bigl[\tfrac ba\bigl(1-e^{-2a/R}\bigr)-e^{(a-b)/R}+e^{-(a+b)/R}\Bigr]
=q_b\Bigl[\tfrac ab\bigl(1-e^{-2b/R}\bigr)-e^{(a-b)/R}+e^{-(a+b)/R}\Bigr],$$
(the sign of the exponent flips to $e^{(a-b)/R}$ because $e^{-(b-a)/R}$ moved across
with the same value: $b>a$). Solving for $q_a$ gives the displayed ratio. $\blacksquare$
(b) Expand each bracket in $1/R$ (write $x=1/R$):
$1-e^{-2bx}=2bx-2b^2x^2+\tfrac43b^3x^3+\ldots$, so
$\tfrac ab(1-e^{-2bx})=2ax-2abx^2+\tfrac43ab^2x^3$; and
$$-e^{(a-b)x}+e^{-(a+b)x}=-2ax+2abx^2-\tfrac13(a^3+3ab^2)x^3+\ldots$$
(the odd/even split of the two exponentials leaves
$-[(a-b)+(a+b)]x=-2ax$, $+\frac{(a+b)^2-(a-b)^2}{2}x^2=+2abx^2$,
$-\frac{(a+b)^3+(a-b)^3}{6}x^3=-\frac{a^3+3ab^2}{3}x^3$).
**Numerator**: the $x$ and $x^2$ terms cancel exactly, leaving
$\bigl[\tfrac43ab^2-ab^2-\tfrac13a^3\bigr]x^3=\tfrac13a(b^2-a^2)x^3$.
**Denominator**: swap $a\leftrightarrow b$ in the first bracket only:
$2bx-2abx^2+\tfrac43a^2bx^3-2ax+2abx^2-\ldots=2(b-a)x+O(x^3)$.
Hence
$$q_a\approx q_b\,\frac{a(b^2-a^2)/3R^3}{2(b-a)/R}
=q_b\,\frac{a(a+b)}{6R^2}=q_b\,\frac{ab}{6R^2}\Bigl(1+\frac ab\Bigr). \qquad\blacksquare$$
Positive for $q_b>0$: unlike P10, the Yukawa deviation is *even* in the sense that
the induced charge appears only at second order in $b/R$ — which is why Cavendish
null results translate into such strong photon-mass limits
($\epsilon_{\rm eff}\sim(b/R)^2$; Williams–Fowler–Hill 1971 reach
$\epsilon\sim3\times10^{-16}$, i.e. $R\gtrsim10^{7}\,$m).

### P12.  Exercise 2.6.1 — The charged conducting disk  *(Wilcox 2e §2.14, pp.74–75)*
A thin isolated conducting disk of radius $R$ is raised to potential $V$. In the
oblate spheroidal coordinates of P5 (origin at the disk center, $z$-axis
perpendicular; the disk is $\xi=0$) the solution is $\Phi=A\tan^{-1}(1/\xi)$.
(a) Change variables to show
$$\Phi=A\tan^{-1}\!\Biggl[\frac{\sqrt2\,R}{\sqrt{(r^2-R^2)+\sqrt{(r^2-R^2)^2+4R^2z^2}}}\Biggr],
\qquad r^2=x^2+y^2+z^2 .$$
(b) Take $z\to0$ with $r<R$ to argue $A=2V/\pi$. (c) Show the (two-sided) surface
density is $\sigma(\rho)=\dfrac{V}{\pi^2\sqrt{R^2-\rho^2}}$. (d) What is the disk's
capacitance?
*Answer:* (a) invert $\xi$ from $(r,z)$; (b) on the disk $\xi\to0$,
$\tan^{-1}\to\pi/2$, so $A\pi/2=V$; (c) $\sigma=-\frac1{2\pi}\partial_z\Phi|_{0^+}$;
(d) $C=Q/V=2R/\pi$.
*Check:* the spherical form equals the oblate form; $\Phi\to V$ on the disk;
$\int\sigma\,da=Q=2RV/\pi$; far field $\to Q/r$. (`test_p12_disk_potential`.)

**Solution.** (a) From P5's map: $\rho^2\equiv x^2+y^2=R^2(\xi^2+1)\sin^2\theta$ and
$z=R\xi\cos\theta$, so
$r^2=\rho^2+z^2=R^2\xi^2+R^2\sin^2\theta$, giving $\sin^2\theta=(r^2-R^2\xi^2)/R^2$ and
$$\frac{z^2}{R^2}=\xi^2\cos^2\theta=\xi^2\Bigl(1-\frac{r^2}{R^2}+\xi^2\Bigr)
\;\Longrightarrow\;
\xi^4+\Bigl(1-\frac{r^2}{R^2}\Bigr)\xi^2-\frac{z^2}{R^2}=0 .$$
The positive root of this quadratic in $\xi^2$:
$$\xi^2=\frac{(r^2-R^2)+\sqrt{(r^2-R^2)^2+4R^2z^2}}{2R^2}
\;\Longrightarrow\;
\frac1\xi=\frac{\sqrt2\,R}{\sqrt{(r^2-R^2)+\sqrt{(r^2-R^2)^2+4R^2z^2}}},$$
which substituted in $\Phi=A\tan^{-1}(1/\xi)$ is the displayed form. $\blacksquare$
(b) On the disk ($z\to0$, $r=\rho<R$): $r^2-R^2<0$, and
$\sqrt{(r^2-R^2)^2+4R^2z^2}\to R^2-r^2$, so the inner sum $\to0^+$ and
$1/\xi\to\infty$: $\tan^{-1}(1/\xi)\to\pi/2$. Consistency with the boundary value
$\Phi|_{\rm disk}=V$ forces $A=2V/\pi$. (Check the other limits: $r\to\infty$ gives
$\xi\to r/R$, $\Phi\to AR/r\to0$ ✓; the potential is continuous across the plane
outside the disk ✓.)
(c) Near the disk $\xi\to0$: $\Phi=A\tan^{-1}(1/\xi)=A(\pi/2-\xi+O(\xi^3))$, and at
fixed $\rho<R$, $z=R\xi\cos\theta$ with $\cos\theta=\sqrt{1-\rho^2/R^2}$ at $\xi=0$,
so $\partial\xi/\partial z=1/(R\cos\theta)=1/\sqrt{R^2-\rho^2}$ and
$$\frac{\partial\Phi}{\partial z}\Big|_{0^+}=-\frac{A}{\sqrt{R^2-\rho^2}} .$$
By symmetry $E_z(0^-)=-E_z(0^+)$, so the *total* (both faces) density from the jump
condition (WT 2.68), $E_z(0^+)-E_z(0^-)=4\pi\sigma$:
$$\sigma(\rho)=\frac{2E_z(0^+)}{4\pi}=-\frac1{2\pi}\frac{\partial\Phi}{\partial z}\Big|_{0^+}
=\frac{A}{2\pi\sqrt{R^2-\rho^2}}=\frac{V}{\pi^2}\frac1{\sqrt{R^2-\rho^2}} . \qquad\blacksquare$$
(The inverse-square-root rim divergence is the conductor's edge singularity.)
(d) Total charge:
$$Q=\int_0^R\sigma(\rho)\,2\pi\rho\,d\rho=\frac{2V}{\pi}\int_0^R\frac{\rho\,d\rho}{\sqrt{R^2-\rho^2}}
=\frac{2V}{\pi}\bigl[-\sqrt{R^2-\rho^2}\bigr]_0^R=\frac{2RV}{\pi},$$
so
$$C=\frac QV=\frac{2R}{\pi}\approx0.6366\,R$$
— the $C_{\rm cir}$ quoted and reused in P37–P39 (Exercises 2.12.7–2.12.9). Far
field check: $\Phi\to A R/r=Q/r$ ✓ (numerically the ratio $\to1$ at $r/R\sim10^3$).

### P13.  Exercise 2.6.2 — Deriving the dipole-layer potential  *(Wilcox 2e §2.14, p.75)*
Two nearby surfaces carry equal-and-opposite surface densities at points separated
by the constant offset $d$ along the common perpendicular:
$\sigma_1(\vec x'-\hat n_{21}d)=-\sigma(\vec x')$ (Fig. 2.13), so
$$\Phi(\vec x)=\int_{S_2}\frac{\sigma(\vec x')}{|\vec x-\vec x'|}\,da'
-\int_{S_2}\frac{\sigma(\vec x')}{|\vec x-\vec x''|}\,da',\qquad \vec x''=\vec x'-\hat n_{21}d .$$
Using the first-order expansion of $1/|\vec x-\vec x''|$ in $d$, derive WT (2.77):
$\Phi(\vec x)=\int_S da'\,D(\vec x')\,\hat n_{21}\cdot\vec\nabla'\,|\vec x-\vec x'|^{-1}$
with $D=\sigma d$.
*Answer:* the shifted denominator expands as
$1/|\vec x-\vec x''|=1/|\vec x-\vec x'|-d\,\hat n_{21}\cdot\vec\nabla'|\vec x-\vec x'|^{-1}$;
the zeroth-order terms cancel between the layers.
*Check:* two coaxial uniformly charged disks $\pm\sigma$ at separation $d$: the exact
two-layer axial potential converges to the dipole-layer formula as $d\to0$ at fixed
$D=\sigma d$ (error $O(d^2)$). (`test_p13_dipole_limit`.)

**Solution.** The geometric content: the negative layer sits at
$\vec x''=\vec x'-\hat n_{21}d$, so
$|\vec x-\vec x''|=|(\vec x-\vec x')+\hat n_{21}d|$. Expand in the small shift
$\vec a=\hat n_{21}d$ using $f(\vec v+\vec a)\approx f(\vec v)+\vec a\cdot\vec\nabla_v f$
with $f=1/|\cdot|$, $\vec v=\vec x-\vec x'$:
$$\frac1{|\vec x-\vec x''|}=\frac1{|\vec v+\vec a|}
\approx\frac1{|\vec v|}-\frac{\vec a\cdot\vec v}{|\vec v|^3}
=\frac1{|\vec x-\vec x'|}-d\,\hat n_{21}\cdot\frac{\vec x-\vec x'}{|\vec x-\vec x'|^3}.$$
But $\vec\nabla'\,|\vec x-\vec x'|^{-1}=+(\vec x-\vec x')/|\vec x-\vec x'|^3$
(derivative with respect to the *source* point — the sign that makes the book's
hint come out right), so
$$\frac1{|\vec x-\vec x''|}\approx\frac1{|\vec x-\vec x'|}-d\,\hat n_{21}\cdot\vec\nabla'\frac1{|\vec x-\vec x'|}.$$
Insert into the two-layer superposition: the leading $1/|\vec x-\vec x'|$ pieces
cancel (equal and opposite charge at corresponding points), leaving
$$\Phi(\vec x)=\int_{S}da'\,\sigma(\vec x')\,d\;\hat n_{21}\cdot\vec\nabla'\frac1{|\vec x-\vec x'|}
=\int_Sda'\,D(\vec x')\,\hat n_{21}\cdot\vec\nabla'\frac1{|\vec x-\vec x'|},$$
with $D\equiv\sigma d$ held finite as $d\to0$, $\sigma\to\infty$ (WT 2.76). This is
(2.77); combined with the solid-angle identity (2.71) it is $\Phi=-\int D\,d\Omega'$
(2.78). $\blacksquare$ Numerically: two disks of radius $1$ carrying
$\pm\sigma=\pm D/d$ at separation $d$ reproduce the $d\to0$ formula with error
$\propto d^2$ (the next, quadrupole, order — the linear term *is* the answer).

### P14.  Exercise 2.6.3 — Dipole surface with a fixed separation direction  *(Wilcox 2e §2.14, p.76)*
Now build the double layer differently (Fig. 2.19): put $+\sigma(\vec x')$ on open
surface 2 and $-\sigma$ on a *complementary copy displaced by the constant vector*
$\hat x\,d$ (not the local normal). (a) Show that in both regions
$\Phi_d(\vec x)=\hat x\cdot\vec E^{(2)}(\vec x)\,d$, where $\vec E^{(2)}$ is the field of
surface 2 alone. (b) Show the potential discontinuity across the pair is
$\Phi_2^d-\Phi_1^d=4\pi D(\vec x)\,\hat x\cdot\hat n_{21}$, $D\equiv\sigma d$.
*Answer:* (a) the shifted-layer potential is a directional finite difference of the
single-layer potential: $\Phi_d=\Phi^{(2)}(\vec x)-\Phi^{(2)}(\vec x+\hat xd)\to
-d\,\hat x\cdot\vec\nabla\Phi^{(2)}=\hat x\cdot\vec E^{(2)}d$. (b) only the normal
component of $\vec E^{(2)}$ jumps (by $4\pi\sigma$), so the jump of $\Phi_d$ is
$4\pi\sigma d\,\hat x\cdot\hat n_{21}$.
*Check:* single charged disk, oblique offset $\hat x$: numeric two-layer potential
vs $\hat x\cdot\vec E^{(2)}d$ at off-axis points (quadrature field); jump across the
layer $\to4\pi D\,\hat x\cdot\hat n$ including the $\hat x\perp\hat n$ null case.
(`test_p14_tilted_layer`.)

**Solution.** (a) Let $\Phi^{(2)}(\vec x)=\int_{S_2}\sigma(\vec x')/|\vec x-\vec x'|\,da'$
be the single-layer potential. The negative copy lives at source points
$\vec x'+\hat xd$ (displaced rigidly by $\hat xd$; Fig. 2.19's orientation makes the
pair's dipole moment point along $+\hat x$), so its potential at $\vec x$ is
$$-\int_{S_2}\frac{\sigma(\vec x')\,da'}{|\vec x-\vec x'-\hat xd|}=-\Phi^{(2)}(\vec x-\hat xd)
\quad\text{— wait: }|\vec x-(\vec x'+\hat xd)|=|(\vec x-\hat xd)-\vec x'| .$$
So the *pair* potential is a finite difference of the same function at two field
points:
$$\Phi_d(\vec x)=\Phi^{(2)}(\vec x)-\Phi^{(2)}(\vec x-\hat xd)
=d\,\hat x\cdot\vec\nabla\Phi^{(2)}(\vec x)+O(d^2)
=-\,d\,\hat x\cdot\vec E^{(2)}(\vec x)+O(d^2).$$
The overall sign tracks which copy is positive: with the *positive* layer displaced
by $+\hat xd$ relative to the negative one (equivalently the negative copy at
$\vec x'-\hat xd$), the same two lines give
$\Phi_d(\vec x)=\Phi^{(2)}(\vec x)-\Phi^{(2)}(\vec x+\hat xd)=+\,\hat x\cdot\vec E^{(2)}(\vec x)\,d$,
which is the book's orientation (Fig. 2.19). Either way: **the pair potential is the
$d$-weighted component of the single-layer field along the offset direction**, valid
in both regions since only $\Phi^{(2)}$, defined everywhere, enters. $\blacksquare$
(b) $\Phi_d$ inherits its discontinuity from $\vec E^{(2)}$. Crossing $S_2$ along
$\hat n_{21}$, the tangential part of $\vec E^{(2)}$ is continuous (WT 2.67) and the
normal part jumps by (WT 2.68): $\vec E^{(2)}_2-\vec E^{(2)}_1=4\pi\sigma\,\hat n_{21}$.
Hence
$$\Phi_2^d-\Phi_1^d=\hat x\cdot\bigl(\vec E^{(2)}_2-\vec E^{(2)}_1\bigr)d
=4\pi\sigma d\;\hat x\cdot\hat n_{21}=4\pi D(\vec x)\,\hat x\cdot\hat n_{21}. \qquad\blacksquare$$
This generalizes (2.80): the standard normal-offset layer is $\hat x=\hat n_{21}$,
jump $4\pi D$; a layer sheared *parallel* to itself ($\hat x\perp\hat n_{21}$)
produces **no** potential jump — numerically the two-disk potential with in-plane
offset is continuous across the disk to $O(d^2)$.

### P15.  Exercise 2.6.4 — Dipole shells: hemisphere, disk, full sphere  *(Wilcox 2e §2.14, pp.76–77)*
(a) A hemispherical shell of radius $a$ (rim in the $z=0$ plane, center O at the
origin) carries constant dipole surface density $D$ along its outward normal $\hat n$
(Fig. 2.20a). Find $\vec E$ on the whole $z$-axis, and show the far field is
$$E_r=\frac{2D\pi a^2}{r^3}\cos\theta,\qquad E_\theta=\frac{D\pi a^2}{r^3}\sin\theta$$
(the point-dipole field, cf. §5.1). (b) Same for a flat disk of radius $a$
(Fig. 2.20b). (c) For a full sphere with uniform $D$ along the outward normal
(Fig. 2.20c), find $\vec E$ inside and outside.
*Answer:* (a) $\Phi=2\pi D[\pm1-z/\sqrt{z^2+a^2}]$ (upper sign outside the shell,
i.e. $z>a$), so on the entire axis $E_z=2\pi Da^2/(z^2+a^2)^{3/2}$; the layer's
dipole moment is $\vec p=D\,(\text{vector area})=\pi a^2D\,\hat z$, giving the stated
far field. (b) the disk gives the *same* axis field and the same $\vec p$ — same rim,
same solid angle. (c) $\vec E\equiv0$ both inside and outside; only $\Phi$ jumps by
$4\pi D$ across the shell.
*Check:* quadrature of the layer integral vs closed forms for hemisphere and disk;
$E_z$ agreement between the two; far-field ratio $\to$ dipole; sphere: quadrature
potential constant in/out. (`test_p15_hemisphere`.)

**Solution.** Work from the layer potential in solid-angle form (P13 / WT 2.77):
$$\Phi(\vec x)=D\int_S da'\;\hat n'\cdot\frac{\vec x-\vec x'}{|\vec x-\vec x'|^3}
\qquad(\text{constant }D).$$
(a) On the axis, $\vec x=(0,0,z)$; hemisphere points
$\vec x'=a(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta)$, $\hat n'=\vec x'/a$,
$\mu=\cos\theta\in[0,1]$:
$\hat n'\cdot(\vec x-\vec x')=(z\mu a-a^2)/a=z\mu-a$ and
$|\vec x-\vec x'|^2=z^2+a^2-2az\mu$, so
$$\Phi(z)=2\pi a^2D\int_0^1\frac{(z\mu-a)\,d\mu}{(z^2+a^2-2az\mu)^{3/2}} .$$
Substitute $Q=z^2+a^2-2az\mu$ (so $z\mu-a=(z^2-a^2-Q)/2a$, $d\mu=-dQ/2az$):
$$\int\frac{(z\mu-a)\,d\mu}{Q^{3/2}}
=\frac1{2a^2z}\Bigl[(z^2-a^2)Q^{-1/2}+Q^{1/2}\Bigr],$$
evaluated between $\mu=0$ ($Q=z^2+a^2$, bracket $=2z^2/\sqrt{z^2+a^2}$) and $\mu=1$
($Q=(z-a)^2$, bracket $=(z^2-a^2)/|z-a|+|z-a|=\pm2z$ — $+$ for $z>a$, $-$ for $z<a$).
Hence
$$\Phi(z)=\frac{\pi D}{z}\Bigl[\pm2z-\frac{2z^2}{\sqrt{z^2+a^2}}\Bigr]
=2\pi D\Bigl[\pm1-\frac{z}{\sqrt{z^2+a^2}}\Bigr],$$
upper sign for $z>a$ (outside the dome), lower for $z<a$ (below/inside — including
all $z<0$). Limits: $\Phi\to0$ as $z\to\pm\infty$ ✓; crossing the dome at $z=a$,
$\Phi(a^+)-\Phi(a^-)=4\pi D$ ✓ (WT 2.81). The constant $\pm$ never differentiates:
$$E_z=-\frac{d\Phi}{dz}=2\pi D\,\frac{d}{dz}\frac{z}{\sqrt{z^2+a^2}}
=\frac{2\pi D\,a^2}{(z^2+a^2)^{3/2}}\qquad\text{for all }z\ \text{(off the layer)},$$
a *single smooth formula on the whole axis*, pointing along $+\hat z$ for $D>0$
(value $2\pi D/a$ at O). Far field: the layer's dipole moment is
$\vec p=\int D\,\hat n'\,da'=D\times(\text{vector area of the dome})=D\,\pi a^2\hat z$
(the vector area of any cap equals that of its rim disk). A point dipole $p\hat z$
has $E_r=2p\cos\theta/r^3$, $E_\theta=p\sin\theta/r^3$, i.e. exactly
$E_r=2\pi Da^2\cos\theta/r^3$, $E_\theta=\pi Da^2\sin\theta/r^3$; on the axis
$E_z\to2\pi Da^2/z^3$, matching the exact form. $\blacksquare$
(b) Disk of radius $a$ in the $z=0$ plane, $\hat n'=\hat z$:
$\hat n'\cdot(\vec x-\vec x')=z$, $|\vec x-\vec x'|^2=z^2+\rho'^2$:
$$\Phi(z)=2\pi Dz\int_0^a\frac{\rho'\,d\rho'}{(z^2+\rho'^2)^{3/2}}
=2\pi D\Bigl[\mathrm{sgn}(z)-\frac{z}{\sqrt{z^2+a^2}}\Bigr],$$
so again $E_z=2\pi Da^2/(z^2+a^2)^{3/2}$ everywhere off the layer, and
$\vec p=D\pi a^2\hat z$: **identical** axis field and far field. No accident: the
dome and the disk share the same rim, and a constant-$D$ layer's potential is
$-D\,\Omega(\vec x)$ with $\Omega$ the (signed) solid angle of the surface — which
depends only on the rim, up to the $4\pi$ jump bookkeeping of which side you're on.
(c) Full sphere: from (a) plus the complementary dome ($\mu\in[-1,0]$, bracket at
$\mu=-1$: $(z^2-a^2)/(z+a)+(z+a)=2z$ for $z>-a$), the lower dome contributes
$2\pi D[z/\sqrt{z^2+a^2}-1]$, so
$$\Phi_{\rm out}=2\pi D\Bigl[1-\tfrac{z}{\sqrt{\cdot}}\Bigr]+2\pi D\Bigl[\tfrac{z}{\sqrt{\cdot}}-1\Bigr]=0,\qquad
\Phi_{\rm in}=2\pi D\Bigl[-1-\tfrac{z}{\sqrt{\cdot}}\Bigr]+2\pi D\Bigl[\tfrac{z}{\sqrt{\cdot}}-1\Bigr]=-4\pi D,$$
both constants (the axis calculation suffices — by symmetry $\Phi$ depends only on
$r$, and the solid-angle form gives $\Omega=4\pi$ inside, $0$ outside). Therefore
$$\vec E=0\ \text{everywhere, inside and outside};\qquad \Phi_{\rm out}-\Phi_{\rm in}=4\pi D,$$
the pure gauge-jump of a closed uniform double layer — the "Neumann conductor"
field configuration of §2.7. $\blacksquare$
### P16.  Exercise 2.7.1 — Green's first identity  *(Wilcox 2e §2.14, p.77)*
Prove Green's first identity (WT 2.83),
$\int_V d^3x\,(\phi\nabla^2\psi+\vec\nabla\psi\cdot\vec\nabla\phi)=\oint_S da\,\phi\,\partial_n\psi$,
from the Gauss (divergence) theorem.
*Answer:* apply the divergence theorem to the vector field $\phi\vec\nabla\psi$.
*Check:* radial test pair $\phi=r^2$, $\psi=r^4$ on a ball of radius $R$: both sides
equal $16\pi R^7$ (quadrature vs closed form); plus a second nontrivial pair.
(`test_p16_green_identity`.)

**Solution.** The product rule for divergences gives, for any $C^2$ pair,
$$\vec\nabla\cdot(\phi\,\vec\nabla\psi)=\phi\,\nabla^2\psi+\vec\nabla\phi\cdot\vec\nabla\psi .$$
Integrate over $V$ and apply the divergence theorem (WT 1.9) to the left side:
$$\int_V\vec\nabla\cdot(\phi\vec\nabla\psi)\,d^3x=\oint_S\phi\,\vec\nabla\psi\cdot\hat n\,da
=\oint_S\phi\,\frac{\partial\psi}{\partial n}\,da ,$$
$\hat n$ the outward normal. Hence
$$\int_V\bigl(\phi\nabla^2\psi+\vec\nabla\phi\cdot\vec\nabla\psi\bigr)d^3x=\oint_S\phi\,\partial_n\psi\,da. \qquad\blacksquare$$
(Antisymmetrizing in $\phi\leftrightarrow\psi$ kills the symmetric
$\vec\nabla\phi\cdot\vec\nabla\psi$ term and yields Green's *second* identity
(2.95) — the engine of §2.8.) Closed-form check used by the tests: on the ball
$r\le R$ with $\phi=r^2,\ \psi=r^4$: $\nabla^2r^4=20r^2$,
$\vec\nabla r^2\cdot\vec\nabla r^4=8r^4$, so the volume side is
$\int_0^R28r^4\,4\pi r^2dr=16\pi R^7$; the surface side is
$R^2\cdot4R^3\cdot4\pi R^2=16\pi R^7$. Equal. (analytic — the numeric check is of
the verifying-instance kind.)

### P17.  Exercise 2.7.2 — Green's reciprocation theorem; shells around a point charge  *(Wilcox 2e §2.14, pp.77–78)*
(a) Prove the reciprocation theorem: for two electrostatic states of the *same*
geometry with conducting boundaries — state 1 with $(\Phi,\rho,\sigma)$, state 2
with $(\Phi',\rho',\sigma')$ —
$$\oint da\,\sigma\,\Phi'+\int d^3x\,\rho\,\Phi'=\oint da\,\sigma'\,\Phi+\int d^3x\,\rho'\,\Phi .$$
(b) A point charge $q$ sits at radius $r$ between grounded concentric conducting
shells $a<r<b$ (Fig. 2.21). Use (a) to find the induced charges on the two shells.
*Answer:* (b) $Q_a=-q\,\dfrac{a(b-r)}{r(b-a)}=-q\,\dfrac{1/r-1/b}{1/a-1/b}$,
$Q_b=-q\,\dfrac{b(r-a)}{r(b-a)}$; they sum to $-q$.
*Check:* reciprocation result vs an independent Gauss/continuity construction of
the radial potential; $Q_a+Q_b=-q$; limits $r\to a,b$. (`test_p17_reciprocation_shells`.)

**Solution.** (a) Both states' potentials are Coulomb superpositions of *all* their
charges (volume + surface):
$\Phi'(\vec x)=\int d^3y\,\rho'(\vec y)/|\vec x-\vec y|+\oint da_y\,\sigma'(\vec y)/|\vec x-\vec y|$.
Insert into the left side:
$$\oint\!da\,\sigma\Phi'+\int\!d^3x\,\rho\Phi'
=\iint\frac{[\rho(\vec x)+\sigma(\vec x)\delta_S]\,[\rho'(\vec y)+\sigma'(\vec y)\delta_{S}]}{|\vec x-\vec y|}\,d^3x\,d^3y,$$
writing surface charge as a surface-delta volume density (P–§2.3). The double
integral is **symmetric** under exchanging primed and unprimed sources (the kernel
$1/|\vec x-\vec y|$ is symmetric), and the right side is the same double integral
with the roles swapped. Hence LHS = RHS. $\blacksquare$ (Equivalently: both sides
equal twice the mutual interaction energy of the two charge systems.)
(b) **Choose the auxiliary state to convert unknown induced charges into knowns.**
State 1 (actual): $q$ at radius $r$; both shells grounded, $\Phi=0$ on $S_a$ and
$S_b$; unknown totals $Q_a$, $Q_b$. State 2 (auxiliary): *no* interior charge,
inner shell at potential $V'$, outer grounded; between the shells the auxiliary
potential is the standard capacitor form
$$\Phi'(s)=V'\,\frac{1/s-1/b}{1/a-1/b},\qquad a\le s\le b .$$
Reciprocation: the RHS vanishes ($\rho'=0$; $\sigma'$ lives on shells where the
*actual* $\Phi=0$). The LHS: the actual surface charge on $S_a$ sees $\Phi'=V'$, on
$S_b$ sees $0$; the point charge sees $\Phi'(r)$:
$$Q_a\,V'+q\,\Phi'(r)=0\ \Longrightarrow\
Q_a=-q\,\frac{1/r-1/b}{1/a-1/b}=-q\,\frac{a(b-r)}{r(b-a)} .$$
Repeating with the auxiliary roles swapped (outer at $V'$, inner grounded,
$\Phi'(s)=V'(1/a-1/s)/(1/a-1/b)$):
$$Q_b=-q\,\frac{1/a-1/r}{1/a-1/b}=-q\,\frac{b(r-a)}{r(b-a)} .$$
Sum: $Q_a+Q_b=-q\,[a(b-r)+b(r-a)]/[r(b-a)]=-q$ — all field lines from $q$ end on
the grounded pair. Limits: $r\to a$ gives $(Q_a,Q_b)\to(-q,0)$; $r\to b$ gives
$(0,-q)$ ✓. **Independent verification** (used by the test): solve the $\ell=0$
radial problem directly — $\Phi=\alpha(1/s-1/a)$ for $s<r$, $\beta(1/s-1/b)$ for
$s>r$; Gauss gives $\alpha=Q_a$, $\beta=q+Q_a$; continuity at $s=r$ reproduces
exactly $Q_a=-qa(b-r)/[r(b-a)]$. $\blacksquare$

### P18.  Exercise 2.7.3 — Mean value theorem and uniqueness again  *(Wilcox 2e §2.14, p.78)*
(a) Prove the electrostatic mean value theorem (MVT): in charge-free space, $\Phi$
at a point equals its average over any sphere centered on that point. (b) Use the
MVT to re-prove Dirichlet uniqueness (§2.7) for $\Phi$.
*Answer:* (a) the derivative of the spherical average with respect to the radius is
the flux of $\vec\nabla\Phi$, which vanishes by Laplace; (b) the difference of two
solutions obeys the MVT, so it can have no interior extremum, and it vanishes on
the boundary.
*Check:* spherical averages of harmonic test functions ($1/|\vec x-\vec x_0|$ with
outside source, $x^2-y^2$, linear) equal center values by quadrature; a
*non*-harmonic control ($x^2$) fails by exactly $R^2/3$. (`test_p18_mvt`.)

**Solution.** (a) Define the average over the sphere of radius $R$ about $\vec x_0$,
$$\langle\Phi\rangle_R=\frac1{4\pi}\oint\Phi(\vec x_0+R\hat n)\,d\Omega .$$
Differentiate under the integral with respect to $R$:
$$\frac{d\langle\Phi\rangle_R}{dR}=\frac1{4\pi}\oint\hat n\cdot\vec\nabla\Phi\,d\Omega
=\frac1{4\pi R^2}\oint_{S_R}\partial_n\Phi\,da
=\frac1{4\pi R^2}\int_{B_R}\nabla^2\Phi\,d^3x=0,$$
by the divergence theorem and $\nabla^2\Phi=0$ (charge-free). So
$\langle\Phi\rangle_R$ is independent of $R$; letting $R\to0$, continuity gives
$\langle\Phi\rangle_R=\Phi(\vec x_0)$ for every admissible $R$. $\blacksquare$
(b) Let $\Phi_1,\Phi_2$ solve Poisson's equation in $V$ with the same $\rho$ and the
same Dirichlet values on $S$; $U=\Phi_1-\Phi_2$ is harmonic with $U|_S=0$. Suppose
$U>0$ somewhere. $U$ is continuous on the compact $\overline V$, so it attains its
maximum $M>0$ at some interior $\vec x_*$ (not on $S$, where $U=0$). Take any small
sphere around $\vec x_*$ inside $V$: the MVT says $M=U(\vec x_*)=\langle U\rangle_R\le M$,
with equality **only if $U\equiv M$ on the whole sphere** (an average of values
$\le M$ equals $M$ only when all equal $M$). Hence $U=M$ on every sphere around
$\vec x_*$ up to the boundary of its neighborhood — the set $\{U=M\}$ is open and
closed in $V$, so $U\equiv M$ on the connected component, contradicting $U\to0$ at
$S$. So $U\le0$; symmetrically $U\ge0$; therefore $U\equiv0$ and $\Phi_1=\Phi_2$.
(This is the max-principle route — same squeeze as Griffiths' proof, with the MVT
supplying the "no interior extrema" step; cf. `~EM-04` notes §2.)

### P19.  Exercise 2.8.1 — Relating the Neumann and Dirichlet Green functions  *(Wilcox 2e §2.14, p.78)*
For a region with boundary $S$, show
$$G_N(\vec x,\vec x'')=G_D(\vec x'',\vec x)-\frac1{4\pi}\oint_S da'\,G_N(\vec x',\vec x'')\,
\frac{\partial G_D(\vec x',\vec x)}{\partial n'} .$$
*Answer:* Green's second identity applied to the pair
$\phi(\vec x')=G_D(\vec x',\vec x)$, $\psi(\vec x')=G_N(\vec x',\vec x'')$, using each
function's defining property.
*Check:* 1-D analog verified exactly on a grid — with $G_D=x_<(1-x_>/L)$ and the
unsymmetrized $G_N$, the identity (with $\frac1{4\pi}\oint\to$ endpoint sum) holds to
machine precision. (`test_p19_gn_gd_identity`.)

**Solution.** Green's second identity in the primed variable:
$$\int_Vd^3x'\bigl[\phi\,\nabla'^2\psi-\psi\,\nabla'^2\phi\bigr]
=\oint_Sda'\Bigl[\phi\,\frac{\partial\psi}{\partial n'}-\psi\,\frac{\partial\phi}{\partial n'}\Bigr].$$
Insert $\phi(\vec x')=G_D(\vec x',\vec x)$ and $\psi(\vec x')=G_N(\vec x',\vec x'')$,
both Green functions in their **first** argument:
$\nabla'^2G_D(\vec x',\vec x)=-4\pi\delta(\vec x'-\vec x)$,
$\nabla'^2G_N(\vec x',\vec x'')=-4\pi\delta(\vec x'-\vec x'')$. The volume side
collapses onto the two deltas:
$$-4\pi G_D(\vec x'',\vec x)+4\pi G_N(\vec x,\vec x'') .$$
The surface side: $G_D(\vec x',\vec x)=0$ for $\vec x'\in S$ (2.100) kills the first
term, leaving $-\oint da'\,G_N(\vec x',\vec x'')\,\partial_{n'}G_D(\vec x',\vec x)$.
Divide by $4\pi$:
$$G_N(\vec x,\vec x'')=G_D(\vec x'',\vec x)-\frac1{4\pi}\oint_Sda'\,G_N(\vec x',\vec x'')\,
\frac{\partial G_D(\vec x',\vec x)}{\partial n'} . \qquad\blacksquare$$
Reading: the Neumann function is the Dirichlet one *plus a boundary correction*
whose kernel $-\partial_{n'}G_D/4\pi$ is exactly the Dirichlet "boundary influence"
weight of (2.98) — the correction re-distributes the $-4\pi/S$ wall field. 1-D
version (what the test checks, WT 1-D conventions $G''=-\delta$, no $4\pi$):
$G_N(x,x'')=G_D(x'',x)-\sum_{x'\in\{0,L\}}G_N(x',x'')\,\partial_{n'}G_D(x',x)$, with
$\partial_{n'}=\mp d/dx'$ at $0,L$. With $G_D=x_<(1-x_>/L)$,
$\partial_{n'}G_D|_{x'=0}=-(1-x/L)$, $\partial_{n'}G_D|_{x'=L}=-x/L$, and the
unsymmetrized $G_N$ of P23 ($G_N(0,x'')=0$, $G_N(L,x'')=x''-L/2$), the right side is
$G_D(x'',x)+(x''-L/2)\,x/L$, which equals $x/2$ ($x<x''$) or $x''-x/2$ ($x>x''$) —
precisely $G_N(x,x'')$. Exact.

### P20.  Exercise 2.8.2 — The symmetrized Neumann function changes nothing  *(Wilcox 2e §2.14, p.79)*
For the interior Neumann problem, show that using the symmetrized
$G_N^{\rm symm}$ (2.111) in the representation (2.103) leaves the potential
unchanged up to a constant: $\Phi=\Phi_{\rm symm}+\langle\Phi\rangle-\langle\Phi_{\rm symm}\rangle$.
*Answer:* $G_N^{\rm symm}$ differs from $G_N$ by $-\langle G_N(\cdot,\vec x'')\rangle_S$,
a term constant in the integration variable; its volume and surface contributions
cancel (they carry $Q$ and $-Q$), so only the additive constant convention differs.
*Check:* 1-D analog — the representation (2.138) evaluated with the unsymmetrized
vs symmetrized $G_N$ on a test problem gives potentials whose difference is
grid-constant. (`test_p20_symm_vs_unsym_rep`.)

**Solution.** First, $G^{\rm symm}_N$ is itself a legitimate Neumann Green function:
(2.111) subtracts $g(\vec x'')\equiv\langle G_N(\vec x,\vec x'')\rangle_{S(\vec x)}$,
which depends only on the *second* slot, so in the first slot
$\nabla'^2G^{\rm symm}_N=-4\pi\delta$ and
$\partial_{n'}G^{\rm symm}_N|_S=-4\pi/S$ still hold. Now substitute
$G^{\rm symm}_N(\vec x',\vec x)=G_N(\vec x',\vec x)-g(\vec x)$ into the two integrals
of (2.103):
$$\Delta_{\rm vol}=-g(\vec x)\int d^3x'\rho(\vec x')=-g(\vec x)\,Q,\qquad
\Delta_{\rm surf}=-\frac{g(\vec x)}{4\pi}\oint da'\,\frac{\partial\Phi}{\partial n'} .$$
But Gauss (Green's first identity with $\phi\equiv1$) gives
$\oint\partial_{n'}\Phi\,da'=\int\nabla'^2\Phi\,d^3x'=-4\pi Q$, so
$\Delta_{\rm surf}=+g(\vec x)\,Q$ and the two shifts **cancel identically**: the
integral part of the representation is the same function of $\vec x$ for both
kernels. The only freedom left is the additive constant each convention appends —
(2.103) adds $\langle\Phi\rangle$; calling $\Phi_{\rm symm}$ the symmetric-kernel
representation with *its* average constant, the two answers differ by the constant
$\langle\Phi\rangle-\langle\Phi_{\rm symm}\rangle$:
$$\Phi(\vec x)=\Phi_{\rm symm}(\vec x)+\langle\Phi\rangle-\langle\Phi_{\rm symm}\rangle . \qquad\blacksquare$$
Exactly the expected Neumann non-uniqueness: the physical field
$-\vec\nabla\Phi$ is untouched. (1-D numeric check: kernels $G_N=\{x/2;\,x''-x/2\}$
vs $G^{\rm symm}_N=-|x-x''|/2+L/4$ in (2.138) give $\Phi$'s differing by a constant
$\sim$ machine-flat across the grid.)

### P21.  Exercise 2.8.3 — Potential at the center of a regular polyhedron  *(Wilcox 2e §2.14, p.79)*
A closed volume is bounded by the $n$ conducting faces of a regular polyhedron
($n=4,6,8,12,20$), face $i$ held at $V_i$. Using the Dirichlet-Green-function
representation of the interior potential, show
$\Phi(\text{center})=\frac1n\sum_iV_i$. (Compare Jackson, Problem 2.28.)
*Answer:* charge-free (2.98) makes $\Phi(\vec x_c)=\sum_iV_iF_i$ with weights
$F_i=-\frac1{4\pi}\int_{S_i}\partial_{n'}G_D\,da'$; symmetry equates the $F_i$, and
Gauss forces $\sum F_i=1$, so each is $1/n$.
*Check:* Jacobi relaxation of the cube ($n=6$, one face at $V=1$): center
$\to1/6$ to $\sim10^{-4}$. (`test_p21_cube_average`.)

**Solution.** With $\rho=0$ inside, (2.98) reduces to the boundary term
$$\Phi(\vec x)=-\frac1{4\pi}\oint_Sda'\,\Phi(\vec x')\,\frac{\partial G_D(\vec x',\vec x)}{\partial n'}
=\sum_{i=1}^{n}V_i\,F_i(\vec x),\qquad
F_i(\vec x)\equiv-\frac1{4\pi}\int_{S_i}da'\,\frac{\partial G_D(\vec x',\vec x)}{\partial n'},$$
since $\Phi=V_i$ is constant on face $i$. Two observations at $\vec x=\vec x_c$
(the center):
1. **Symmetry.** The rotation group of the regular polyhedron acts transitively on
the faces and fixes $\vec x_c$. $G_D$ is determined uniquely by the geometry
(2.99)–(2.100), so it is invariant: $G_D(g\vec x',g\vec x)=G_D(\vec x',\vec x)$ for
any symmetry $g$. Mapping face $i$ onto face $j$ therefore maps the integral $F_i(\vec x_c)$
onto $F_j(\vec x_c)$: all the $F_i(\vec x_c)$ are **equal**.
2. **Normalization.** Summing over all faces,
$$\sum_iF_i(\vec x_c)=-\frac1{4\pi}\oint_S\partial_{n'}G_D\,da'
=-\frac1{4\pi}\int_V\nabla'^2G_D\,d^3x'=-\frac1{4\pi}(-4\pi)=1$$
(Gauss, then the defining delta of $G_D$ with the source $\vec x_c$ inside).
Equal weights summing to 1 must each be $1/n$:
$$\Phi(\vec x_c)=\frac1n\sum_{i=1}^nV_i . \qquad\blacksquare$$
(Physical reading: $-\partial_{n'}G_D/4\pi\,da'$ is the probability-like "influence
measure" of boundary patch $da'$ — nonnegative, total mass 1 — and the center sees
every face identically. The cube relaxation check lands at $0.1667$.)

### P22.  Exercise 2.9.1 — Working the 1-D Dirichlet Green function  *(Wilcox 2e §2.14, p.79)*
For the 1-D box $[0,L]$ with $G_D(x,x')=x_<(1-x_>/L)$ (2.136):
(a) find the force $F=E_{\rm avg}q$ (with $E=-dG_D/dx$) on the unit charge at $x'$;
(b) find the induced charges on the endpoints $x=0,L$;
(c) using $G_D$ and (2.127), find $\Phi$ inside the box when $\lambda=0$,
$\Phi(0)=V$, $\Phi(L)=0$.
*Answer:* (a) $F=x'/L-\tfrac12$ (pulled toward the *nearer* wall);
(b) $\sigma_0=-(1-x'/L)$, $\sigma_L=-x'/L$ (sum $=-1$);
(c) $\Phi(x)=V(1-x/L)$.
*Check:* jump/continuity/BC properties of $G_D$ on a grid; two-sided numeric slope
average; endpoint charges from the field; (c) against the linear interpolant.
(`test_p22_force_and_charges`.)

**Solution.** The two branches of $G_D$ as a function of the *field* coordinate $x$:
$$G_D=\begin{cases}x\,(1-x'/L), & x<x'\\[2pt] x'\,(1-x/L), & x>x'\end{cases}
\qquad\Longrightarrow\qquad
E(x)=-\frac{dG_D}{dx}=\begin{cases}-(1-x'/L), & x<x'\\[2pt] +\,x'/L, & x>x'.\end{cases}$$
(a) The self-field average at the particle (the §2.11 prescription — the mean of
the two one-sided fields removes the particle's own symmetric contribution):
$$E_{\rm avg}=\frac{E(x'^+)+E(x'^-)}2=\frac{x'/L-(1-x'/L)}2=\frac{x'}L-\frac12,
\qquad F=q\,E_{\rm avg}=\frac{x'}L-\frac12\quad(q=1).$$
$F<0$ (toward $0$) for $x'<L/2$, $F>0$ (toward $L$) for $x'>L/2$: the charge is
attracted to its nearer grounded wall by its induced charge, with the (1-D) force
growing linearly, vanishing by symmetry at midbox.
(b) In these 1-D conventions ($\Phi''=-\lambda$) Gauss reads $dE/dx=\lambda$, so a
wall's surface charge is the jump of $E$ across it (field vanishes outside the box):
$$\sigma_0=E(0^+)-0=\frac{x'}L-1=-\Bigl(1-\frac{x'}L\Bigr),\qquad
\sigma_L=0-E(L^-)=-\frac{x'}L .$$
Both negative (they attract the unit charge — consistent with (a)); total induced
$\sigma_0+\sigma_L=-1$, screening the unit source completely. Note the proximity
rule: the wall *nearer* the charge takes the larger share, exactly like the 3-D
parallel-plate image problem.
(c) With $\lambda=0$, (2.127) keeps only the boundary term
$\Phi(x)=-[\Phi(x')\,\partial_{x'}G_D(x,x')]_{x'=0}^{x'=L}$. From the branches (now
differentiating in $x'$): $\partial_{x'}G_D|_{x'=L}=-x/L$ and
$\partial_{x'}G_D|_{x'=0}=1-x/L$, so
$$\Phi(x)=-\bigl[\Phi(L)(-x/L)-\Phi(0)(1-x/L)\bigr]=V\Bigl(1-\frac xL\Bigr),$$
the straight line from $V$ to $0$ — which indeed solves $\Phi''=0$ with the given
endpoint data. $\blacksquare$

### P23.  Exercise 2.9.2 — The 1-D Neumann Green function  *(Wilcox 2e §2.14, pp.79–80)*
(a) Complete the derivation of the symmetric Neumann function (2.139),
$G^{\rm symm}_N(x,x')=-\tfrac12|x-x'|+C$, from the general linear form (2.128) and
the endpoint conditions (2.137) $\partial_xG_N(0)=\tfrac12$, $\partial_xG_N(L)=-\tfrac12$.
(b) Find the force on the unit charge at $x'$.
(c) With $\lambda=0$ and endpoint fields $E(0)=E(L)=V/L$, use (2.138) to find $\Phi$
(note the neutrality bookkeeping $E\big|_0^L=Q$).
*Answer:* (a) the BCs fix the slopes $\pm\tfrac12$; continuity + the free
per-source constant give $-\tfrac12|x-x'|+C$, with $C=L/4$ from the (2.111) recipe;
(b) $F=0$; (c) $\Phi(x)=V/2-Vx/L+\langle\Phi\rangle$ — the uniform field $V/L$.
*Check:* BCs, slope jump $-1$, symmetry on a grid; $C=L/4$ from endpoint averaging;
force $=0$; (c) linear with slope $-V/L$. (`test_p23_neumann_gf`.)

**Solution.** (a) Write $G_N=C_1x+C_2$ ($x>x'$), $C_3x+C_4$ ($x<x'$). The endpoint
conditions land on one branch each: $C_3=\tfrac12$ (at $x=0$), $C_1=-\tfrac12$ (at
$x=L$). The unit-source jump $\partial_xG_N|^{x'^+}_{x'^-}=C_1-C_3=-1$ is then
*automatically* satisfied — that is the 1-D image of the $-4\pi/S$ consistency
(2.102): total wall flux must swallow the unit charge, and $\tfrac12+\tfrac12=1$
splits it evenly. Continuity at $x'$: $-\tfrac{x'}2+C_2=\tfrac{x'}2+C_4$, i.e.
$C_2=x'+C_4$ with $C_4=c(x')$ **free for each source position** (Neumann
non-uniqueness). So
$$G_N(x,x')=\begin{cases}\tfrac x2+c(x'), & x<x'\\[2pt] x'-\tfrac x2+c(x'), & x>x'\end{cases}
\;=\;-\tfrac12|x-x'|+\tfrac{x+x'}2\cdot0+\tfrac{x'}2+c(x')\ \ \text{(compact form below)} .$$
Both branches combine as $G_N=-\tfrac12|x-x'|+\tfrac{x'}2+c(x')$. Choosing
$c(x')=C-\tfrac{x'}2$ — allowed, it's a function of $x'$ only — gives the symmetric
$$G^{\rm symm}_N(x,x')=-\tfrac12|x-x'|+C .$$
The (2.111) prescription picks the constant: subtract the endpoint average of the
$c=0$ function, $\tfrac12[G_N(0,x')+G_N(L,x')]=\tfrac12[0+(x'-\tfrac L2)]=\tfrac{x'}2-\tfrac L4$,
which yields exactly $-\tfrac12|x-x'|+\tfrac L4$: $C=L/4$. $\blacksquare$
(b) $E(x)=-\partial_xG^{\rm symm}_N=\tfrac12\,\mathrm{sgn}(x-x')$:
$E(x'^\pm)=\pm\tfrac12$, so $E_{\rm avg}=0$ and $F=0$ for every $x'$. Physical:
constant-field Neumann walls exert no position-dependent pull — the "image
pressure" is the same from both sides (contrast P22a).
(c) In (2.138) with $\lambda=0$ and $\partial_{x'}\Phi(0)=\partial_{x'}\Phi(L)=-V/L$
(remember $E=-\Phi'$):
$$\Phi(x)=\Bigl[G^{\rm symm}_N(x,x')\,\partial_{x'}\Phi(x')\Bigr]_{x'=0}^{x'=L}+\langle\Phi\rangle
=-\frac VL\bigl[G(x,L)-G(x,0)\bigr]+\langle\Phi\rangle .$$
$G(x,L)-G(x,0)=-\tfrac12(L-x)+\tfrac12x=x-\tfrac L2$, so
$$\Phi(x)=\frac V2-\frac{Vx}L+\langle\Phi\rangle,$$
the uniform field $E=V/L$, determined up to the arbitrary average — and consistent:
the Neumann data $E(L)-E(0)=0=Q$ matches the empty box ($\lambda=0$), which is the
solvability condition the book's note flags. $\blacksquare$

### P24.  Exercise 2.9.3 — Green-function solve with mixed data  *(Wilcox 2e §2.14, p.80)*
1-D box, conducting walls at $x=0,L$: $\Phi''=-\lambda$ with **constant** $\lambda$,
$\Phi(0)=V$, $\Phi(L)=-V$. Solve for $\Phi(x)$ using the Dirichlet Green function
$G_D(x,x')=x_<(1-x_>/L)$ (Green-function route required; direct verification
optional).
*Answer:* $\Phi(x)=\dfrac{\lambda\,x(L-x)}2+V\Bigl(1-\dfrac{2x}L\Bigr)$.
*Check:* GF quadrature (volume term) + boundary term vs the closed form; direct
substitution $\Phi''=-\lambda$ and endpoint values; agreement with a dense
finite-difference BVP solve. (`test_p24_gf_solution`.)

**Solution.** (2.127) splits the answer into a source part and a boundary part:
$$\Phi(x)=\underbrace{\int_0^LG_D(x,x')\,\lambda\,dx'}_{\Phi_\lambda}
-\underbrace{\Bigl[\Phi(x')\,\partial_{x'}G_D(x,x')\Bigr]_{x'=0}^{x'=L}}_{\Phi_{\rm bdy}} .$$
**Volume term.** Split at $x'=x$:
$$\Phi_\lambda=\lambda\Bigl[(1-\tfrac xL)\int_0^xx'\,dx'+x\int_x^L(1-\tfrac{x'}L)\,dx'\Bigr]
=\lambda\Bigl[(1-\tfrac xL)\frac{x^2}2+x\Bigl(\frac L2-x+\frac{x^2}{2L}\Bigr)\Bigr]
=\frac{\lambda\,x(L-x)}2 ,$$
after the cubic terms cancel — the textbook parabola (zero at both walls,
curvature $-\lambda$).
**Boundary term.** From P22(c), $\partial_{x'}G_D|_{x'=0}=1-x/L$ and
$\partial_{x'}G_D|_{x'=L}=-x/L$:
$$\Phi_{\rm bdy}=-\Bigl[(-V)\Bigl(-\frac xL\Bigr)-V\Bigl(1-\frac xL\Bigr)\Bigr]
=V\Bigl(1-\frac{2x}L\Bigr),$$
the straight line from $+V$ to $-V$. Total:
$$\Phi(x)=\frac{\lambda x(L-x)}2+V\Bigl(1-\frac{2x}L\Bigr). \qquad\blacksquare$$
Verification: $\Phi''=-\lambda$ ✓; $\Phi(0)=V$, $\Phi(L)=-V$ ✓ — the GF machinery
assembled superposition (particular + harmonic) automatically, which is its point.

### P25.  Exercise 2.9.4 — The 1-D Helmholtz Green function  *(Wilcox 2e §2.14, pp.80–81)*
For $\bigl(\frac{d^2}{dx^2}+k_0^2\bigr)\Phi=-\lambda(x)$ on $[0,L]$ with the Green
function satisfying $\bigl(\frac{d^2}{dx^2}+k_0^2\bigr)G(x,x')=-\delta(x-x')$:
(a) using $G(x,x')=G(x',x)$, derive the representation
$$\Phi(x)=\int_0^Ldx'\,G(x,x')\lambda(x')-\Bigl[\Phi(x')\,\frac{dG(x,x')}{dx'}\Bigr]_{x'=0}^{x'=L},$$
the same shape as (2.127); (b) with Dirichlet conditions $G(0,x')=G(L,x')=0$ show
$$G(x,x')=\frac{\sin k_0x_<\,\sin k_0(L-x_>)}{k_0\,\sin k_0L}.$$
*Answer:* (a) the 1-D Green's-second-identity computation, with the $k_0^2$ terms
cancelling between the pair; (b) glue $\sin k_0x$ and $\sin k_0(L-x)$ with the
$-1$ slope jump; the Wronskian normalization gives $k_0\sin k_0L$.
*Check:* ODE away from the source; slope jump $=-1$; symmetry; $k_0\to0$
degeneration to $x_<(1-x_>/L)$; a full solve at $\lambda=\text{const}$ vs the
closed-form direct solution. (`test_p25_helmholtz`.)

**Solution.** (a) Multiply the $\Phi$ equation (in $x'$) by $G(x',x)$, the $G$
equation (source at $x$, variable $x'$) by $\Phi(x')$, subtract, and integrate:
$$\int_0^L\!\!dx'\Bigl[G(x',x)\Phi''(x')-\Phi(x')\,\partial_{x'}^2G(x',x)\Bigr]
=\int_0^L\!\!dx'\Bigl[-G(x',x)\lambda(x')+\Phi(x')\,\delta(x'-x)\Bigr],$$
where the $k_0^2\,G\Phi$ cross terms cancelled identically — that's why the whole
(2.127) structure survives the Helmholtz shift. The left side is a total derivative,
$\bigl[G\Phi'-\Phi\,\partial_{x'}G\bigr]_0^L$; with homogeneous Dirichlet data for
$G$ the $G\Phi'$ endpoint piece dies, so
$$\Phi(x)=\int_0^LG(x',x)\lambda(x')\,dx'-\bigl[\Phi(x')\,\partial_{x'}G(x',x)\bigr]_{x'=0}^{x'=L},$$
and the symmetry $G(x',x)=G(x,x')$ (proved as in (2.108), or read off the explicit
form in (b)) rewrites it in the stated field-point form. $\blacksquare$
(b) Away from $x'$ the function solves $G''+k_0^2G=0$, so it is a sinusoid on each
branch; the boundary conditions pick $\sin k_0x$ (vanishes at $0$) below the source
and $\sin k_0(L-x)$ (vanishes at $L$) above:
$$G(x,x')=A\,\sin k_0x_<\,\sin k_0(L-x_>)$$
(automatically continuous and symmetric). The unit source fixes $A$ via the slope
jump $\partial_xG|^{x'^+}_{x'^-}=-1$:
$$A\,k_0\bigl[-\sin k_0x'\cos k_0(L-x')-\cos k_0x'\sin k_0(L-x')\bigr]=-1
\;\Longrightarrow\;
A\,k_0\sin\bigl(k_0x'+k_0(L-x')\bigr)=1,$$
by the sine addition formula — the $x'$-dependence collapses (this is the constancy
of the Wronskian of the two homogeneous solutions), leaving $A=1/(k_0\sin k_0L)$:
$$G(x,x')=\frac{\sin k_0x_<\,\sin k_0(L-x_>)}{k_0\sin k_0L},\qquad k_0L\neq n\pi .$$
At resonance $\sin k_0L=0$ the construction fails — the homogeneous problem has a
nontrivial mode and no Green function exists (the 1-D cavity resonance). Limits:
$k_0\to0$ gives $x_<(L-x_>)/L=x_<(1-x_>/L)$, recovering (2.136) ✓. Worked check:
for $\lambda=$ const the GF quadrature reproduces
$\Phi=\frac{\lambda}{k_0^2}\bigl[\cos k_0(x-L/2)/\cos(k_0L/2)-1\bigr]$, the direct
particular-plus-homogeneous solution. $\blacksquare$
### P26.  Exercise 2.10.1 — An uncharged conductor lowers the energy  *(Wilcox 2e §2.14, p.81)*
Prove: with a set of conductors fixed in position, each carrying a given total
charge, introducing an additional *uncharged, insulated* conductor into the region
lowers the electrostatic energy.
*Answer:* the new equilibrium field differs from the old by a field whose cross
term integrates to zero; $W_0-W_1=\frac1{8\pi}\int|\vec E_0-\vec E_1|^2>0$.
*Check:* closed-form instance — charged sphere ($Q$, radius $a$) plus a neutral
concentric conducting shell $b<c$: quadrature energies give
$W_1-W_0=\frac{Q^2}2(\frac1c-\frac1b)<0$. (`test_p26_energy_lowered`.)

**Solution.** Let $\vec E_0=-\vec\nabla\Phi_0$ be the equilibrium field before, and
$\vec E_1=-\vec\nabla\Phi_1$ after the neutral conductor (occupying $v$, surface
$\partial v$) is inserted; all *old* conductors keep their totals $Q_i$, the new one
has total $0$. Compare energies over the field region $\mathcal V$ (all space
outside the old conductors; note $\vec E_1=0$ inside $v$ while $\vec E_0$ is not):
$$W_0-W_1=\frac1{8\pi}\int_{\mathcal V}\bigl(E_0^2-E_1^2\bigr)
=\frac1{8\pi}\int_{\mathcal V}|\vec E_0-\vec E_1|^2
+\frac1{4\pi}\int_{\mathcal V}\vec E_1\cdot(\vec E_0-\vec E_1),$$
the algebraic identity $a^2-b^2=(a-b)^2+2b(a-b)$. Kill the cross term: with
$\vec E_1=-\vec\nabla\Phi_1$,
$$\int\vec E_1\cdot(\vec E_0-\vec E_1)
=-\int\vec\nabla\cdot\bigl[\Phi_1(\vec E_0-\vec E_1)\bigr]
+\int\Phi_1\,\vec\nabla\cdot(\vec E_0-\vec E_1).$$
The second integral vanishes: both fields obey Gauss's law with the *same* volume
charge (none, or the same fixed $\rho$) in $\mathcal V\setminus v$, and inside $v$
$\vec\nabla\cdot\vec E_0=0$ (no charge sat there before) while $\vec E_1\equiv0$.
The first becomes boundary terms over the old conductors, $\partial v$, and
infinity: on each old conductor $\Phi_1=$ const and
$\oint(\vec E_0-\vec E_1)\cdot d\vec a=4\pi(Q_i-Q_i)=0$; on $\partial v$, $\Phi_1=$
const (it *is* a conductor in state 1) and
$\oint\vec E_0\cdot d\vec a=0$ (no enclosed charge), $\oint\vec E_1\cdot d\vec a=4\pi\cdot0$
(neutral); at infinity the product falls as $1/r^3$. So the cross term is zero and
$$W_0-W_1=\frac1{8\pi}\int|\vec E_0-\vec E_1|^2\;>\;0,$$
strictly, because $\vec E_1\equiv\vec E_0$ is impossible: $\vec E_0\neq0$ in $v$
generically while $\vec E_1=0$ there. $\blacksquare$
Instance with closed forms (the numeric check): sphere $a$ with $Q$, neutral shell
$(b,c)$: $W_0=Q^2/2a$; after insertion $E=Q/r^2$ except for the dead zone
$b<r<c$, so $W_1=\frac{Q^2}2(\frac1a-\frac1b+\frac1c)$ and
$W_1-W_0=\frac{Q^2}2(\frac1c-\frac1b)<0$ — energy drops by exactly the energy the
shell's metal expelled. (Physically: the induced surface charges rearrange to
*screen*; any rearrangement allowed at fixed totals that changes the field can only
have been adopted because it lowers $W$ — Thompson's principle in action.)

### P27.  Exercise 2.10.2 — Self-energy of a finite line charge  *(Wilcox 2e §2.14, p.81)*
A straight 1-D string of length $a$ carries uniform density $\lambda=Q/a$ (in 3-D
space). Is its self-energy divergent — and if so, quadratically, linearly, or
logarithmically?
*Answer:* logarithmically: with a short-distance cutoff $\delta$,
$W(\delta)=\lambda^2a\bigl[\ln(a/\delta)-1\bigr]+O(\delta)$ — between the finite
surface and the linearly divergent point (2.149).
*Check:* quadrature of the cutoff double integral at $\delta=a\cdot10^{-k}$,
$k=2..5$: successive differences constant ($=\lambda^2a\ln10$), i.e. linear growth
in $\ln(1/\delta)$ matching the closed form. (`test_p27_log_divergence`.)

**Solution.** The (2.144) double integral on the segment:
$$W=\frac{\lambda^2}2\int_0^a\!\!\int_0^a\frac{dx\,dx'}{|x-x'|},$$
which diverges on the diagonal. Regulate by cutting out $|x-x'|<\delta$:
$$W(\delta)=\frac{\lambda^2}2\cdot2\int_0^{a-\delta}\!\!dx\int_{x+\delta}^a\frac{dx'}{x'-x}
=\lambda^2\int_0^{a-\delta}\ln\frac{a-x}{\delta}\,dx ,$$
using the $x\leftrightarrow x'$ symmetry. Substituting $u=a-x$:
$$W(\delta)=\lambda^2\int_\delta^a\ln\frac u\delta\,du
=\lambda^2\Bigl[u\ln\frac u\delta-u\Bigr]_\delta^a
=\lambda^2\Bigl[a\ln\frac a\delta-a+\delta\Bigr]
=\frac{Q^2}{a}\Bigl[\ln\frac a\delta-1\Bigr]+O(\delta).$$
So $W\to\infty$ as $\delta\to0$, but only **logarithmically** — each decade of
resolution adds the same $\lambda^2a\ln10$. $\blacksquare$
Placement in the §2.10 hierarchy: point charge $\sim1/\delta$ (linear, WT 2.149);
line $\sim\ln(1/\delta)$; surface — finite (P28 computes one). The dimensional
rule of thumb: $W\sim\int\rho\Phi$, and the potential a $d$-dimensional uniform
charge produces *on itself* scales as $\int d^dx\,/r$ near a point — convergent for
$d\ge2$, log-marginal at $d=1$, divergent at $d=0$. (Same log that made the
physical "wire" capacitance depend on its radius.)

### P28.  Exercise 2.10.3 — Self-energy of a charged square sheet  *(Wilcox 2e §2.14, p.81)*
An infinitely thin square sheet of side $R$ carries uniform $\sigma$ and total
charge $Q$. Show $W_{\rm square}=1.48660\ldots\,Q^2/R$. (Hint: a center-of-mass /
difference-variable change collapses the 4-fold integral; the book's value is
numerical — cf. O. Ciftja, *Adv. Math. Phys.* 2016 for a closed-form treatment.)
*Answer:* $W=\frac{Q^2}{R}\bigl[2\ln(1+\sqrt2)+\frac23(1-\sqrt2)\bigr]=1.4866048\ldots\,Q^2/R$
— this module evaluates the reduced integral in closed form and confirms the
book's numerics.
*Check:* 2-D quadrature of the reduced integral vs the closed form vs $1.48660$.
(`test_p28_square_sheet`.)

**Solution.** With $\sigma=Q/R^2$, scale lengths by $R$ ($\vec u,\vec v$ in the unit
square):
$$W=\frac{\sigma^2}2\iint\frac{da\,da'}{|\vec x-\vec x'|}
=\frac{Q^2}{2R}\underbrace{\int_{[0,1]^2}\!\!\int_{[0,1]^2}\frac{d^2u\,d^2v}{|\vec u-\vec v|}}_{I}.$$
**Difference-variable reduction** (the hint): for each Cartesian component,
$\int_0^1\!\int_0^1f(|u-v|)\,du\,dv=2\int_0^1(1-w)f(w)\,dw$ (the density of
$w=|u-v|$ on $[0,1]$ is $2(1-w)$). Applying it in $x$ and $y$ independently:
$$I=4\int_0^1\!\!\int_0^1\frac{(1-w_x)(1-w_y)}{\sqrt{w_x^2+w_y^2}}\,dw_x\,dw_y\equiv4A .$$
Expand the numerator; each piece has an elementary primitive
($L\equiv\ln(1+\sqrt2)=\sinh^{-1}1$):
1. $\displaystyle\int_0^1\!\!\int_0^1\frac{dw_xdw_y}{\sqrt{w_x^2+w_y^2}}
   =2L$ — integrate $\sinh^{-1}(1/w)$-type terms; standard square integral.
2. $\displaystyle\int_0^1\!\!\int_0^1\frac{w_x\,dw_xdw_y}{\sqrt{w_x^2+w_y^2}}
   =\int_0^1\bigl[\sqrt{1+w_y^2}-w_y\bigr]dw_y
   =\frac{\sqrt2+L}2-\frac12$ (and the same with $x\leftrightarrow y$).
3. $\displaystyle\int_0^1\!\!\int_0^1\frac{w_xw_y\,dw_xdw_y}{\sqrt{w_x^2+w_y^2}}
   =\int_0^1w_y\bigl[\sqrt{1+w_y^2}-w_y\bigr]dw_y
   =\frac{2\sqrt2-1}3-\frac13=\frac{2\sqrt2-2}3 .$
So
$$A=2L-2\Bigl[\frac{\sqrt2+L}2-\frac12\Bigr]+\frac{2\sqrt2-2}3
=L+1-\sqrt2+\frac{2\sqrt2-2}3=L+\frac{1-\sqrt2}3 .$$
Numerically $A=0.8813736-0.1380712=0.7433023$, $I=4A=2.9732093$, and
$$W=\frac{Q^2}{2R}\,I=\frac{Q^2}{R}\Bigl[2\ln(1+\sqrt2)+\frac23\bigl(1-\sqrt2\bigr)\Bigr]
=1.4866047\ldots\frac{Q^2}{R}\approx1.48660\,\frac{Q^2}{R}. \qquad\blacksquare$$
(The book quotes the value from numerics; the reduction above gives it in closed
form, agreeing to all quoted digits. Compare the *disk* of equal area: a disk of
radius $R_d$, $W_{\rm disk}=\frac{8}{3\pi}Q^2/R_d$; at equal area
$R_d=R/\sqrt\pi$, $W=1.5045\,Q^2/R$ — the square, being more spread out into its
corners, stores slightly less.)

### P29.  Exercise 2.10.4 — Self-energy of a power-law ball; classical electron radius  *(Wilcox 2e §2.14, pp.81–82)*
(a) A spherically symmetric ball, $\rho(r)=Cr^\alpha$ for $r\le a$, total charge
$Q$: show $W_{\rm sphere}=\dfrac{3+\alpha}{5+2\alpha}\,\dfrac{Q^2}{a}$, finite only
for $\alpha>-\tfrac52$. (b) Set the self-energy of a *uniform* ball equal to
$E=mc^2$ for the electron and find the radius.
*Answer:* (a) as stated (interior field energy contributes
$\frac{Q^2}{2a}\frac1{5+2\alpha}$, exterior $\frac{Q^2}{2a}$); (b)
$a=\frac35\,e^2/m_ec^2=\frac35\,r_e=1.6908\times10^{-13}$ cm.
*Check:* field-energy quadrature vs formula for several $\alpha$ (including the
uniform $3/5$ and shell-limit checks); the cgs electron-radius number.
(`test_p29_ball_energy`.)

**Solution.** (a) Enclosed charge:
$Q(r)=\int_0^r4\pi C r'^{2+\alpha}dr'=\dfrac{4\pi C}{3+\alpha}r^{3+\alpha}$
(needs $\alpha>-3$), and $Q=Q(a)$ fixes $C$. Gauss:
$$E(r)=\frac{Q(r)}{r^2}=\frac{Q}{a^{3+\alpha}}\,r^{1+\alpha}\ (r\le a),\qquad
E=\frac{Q}{r^2}\ (r\ge a).$$
Field energy (2.147):
$$W=\frac1{8\pi}\Bigl[\int_0^a\frac{Q^2r^{2+2\alpha}}{a^{6+2\alpha}}4\pi r^2dr
+\int_a^\infty\frac{Q^2}{r^4}4\pi r^2dr\Bigr]
=\frac{Q^2}{2a^{6+2\alpha}}\cdot\frac{a^{5+2\alpha}}{5+2\alpha}+\frac{Q^2}{2a}
=\frac{Q^2}{2a}\Bigl[\frac1{5+2\alpha}+1\Bigr],$$
provided the interior integral converges at $r=0$: exponent $4+2\alpha>-1$, i.e.
$\boxed{\alpha>-\tfrac52}$. Combine:
$$W=\frac{Q^2}{2a}\,\frac{6+2\alpha}{5+2\alpha}=\frac{3+\alpha}{5+2\alpha}\,\frac{Q^2}{a}. \qquad\blacksquare$$
Sanity: $\alpha=0$ (uniform) $\to\frac35Q^2/a$; $\alpha\to\infty$ (charge pushed to
the surface) $\to\frac12Q^2/a$, the conducting-shell value; $\alpha\to-\frac52^+$
diverges — too much charge concentrated at the center.
(b) Uniform ball: $\frac35\,e^2/a=m_ec^2$, so
$$a=\frac35\,\frac{e^2}{m_ec^2}=\frac35\,r_e .$$
Gaussian numbers: $e=4.80321\times10^{-10}$ esu, $m_e=9.10938\times10^{-28}$ g,
$c=2.99792\times10^{10}$ cm/s give $r_e=e^2/m_ec^2=2.81794\times10^{-13}$ cm and
$$a=1.6908\times10^{-13}\ \text{cm}\approx1.7\ \text{fm}$$
— the classical electron radius picture whose tensions (what holds it together?
cf. §14.1) previewed the need for QED, where the divergence softens to a log
(footnote to (2.149)).

### P30.  Exercise 2.11.1 — Sphere with volume and surface charge; surface force  *(Wilcox 2e §2.14, p.82)*
A sphere of radius $R$ has constant volume density $\rho$ *and* uniform surface
density $\sigma$. (a) Find $\vec E$ inside and outside. (b) Find the outward
electrostatic force per unit area $F/A$ on the surface.
*Answer:* (a) $E(r)=\frac{4\pi\rho r}{3}$ inside;
$E(r)=\bigl(\frac{4\pi R^3\rho}{3}+4\pi R^2\sigma\bigr)/r^2$ outside.
(b) $F/A=\sigma\bigl(\frac{4\pi\rho R}{3}+2\pi\sigma\bigr)$, outward.
*Check:* Gauss-law forms vs direct flux quadrature; the $\rho=0$ limit $2\pi\sigma^2$
(WT 2.161) and the average-field prescription. (`test_p30_sphere_force`.)

**Solution.** (a) Spherical symmetry ⟹ radial field, Gauss (2.44) on a sphere of
radius $r$:
- $r<R$: enclosed charge $\frac43\pi r^3\rho$, so
  $4\pi r^2E=4\pi\cdot\frac43\pi r^3\rho\Rightarrow E_{\rm in}=\dfrac{4\pi\rho\,r}3$.
- $r>R$: enclosed $Q_{\rm tot}=\frac43\pi R^3\rho+4\pi R^2\sigma$, so
  $E_{\rm out}=\dfrac{Q_{\rm tot}}{r^2}=\dfrac{4\pi\rho R^3}{3r^2}+\dfrac{4\pi\sigma R^2}{r^2}$.

The jump at $R$: $E_{\rm out}(R)-E_{\rm in}(R)=4\pi\sigma$ ✓ (2.68) — the volume
charge contributes continuously, the sheet does the jumping.
(b) The force per area on the *surface layer* is $\sigma$ times the field acting on
it, which excludes its own (discontinuous) self-field: by the disk/remainder
argument (2.158)–(2.159) that is the **average** of the fields on the two sides:
$$\frac FA=\sigma\,\frac{E_{\rm in}(R)+E_{\rm out}(R)}2
=\sigma\,\frac{\frac{4\pi\rho R}3+\bigl(\frac{4\pi\rho R}3+4\pi\sigma\bigr)}2
=\sigma\Bigl(\frac{4\pi\rho R}{3}+2\pi\sigma\Bigr),$$
directed along $+\hat r$ when positive. Checks: $\rho=0$ gives the conductor-style
$2\pi\sigma^2$ (2.161); $\sigma=0$ gives zero — the volume charge feels a body
force, not a surface one; and the expression is exactly
$\sigma E_{\rm remainder}(R)$, the sheet riding in the field of everything else
(volume charge $+$ its own smooth continuation). $\blacksquare$

### P31.  Exercise 2.12.1 — Schwarz inequality for the capacitance matrix  *(Wilcox 2e §2.14, p.82)*
In an $N$-conductor system, only $V_A$ and $V_B$ are nonzero. Show from the
positivity of the field energy that $C_{AB}^2<C_{AA}\,C_{BB}$.
*Answer:* $W=\frac12(C_{AA}V_A^2+2C_{AB}V_AV_B+C_{BB}V_B^2)>0$ for
$(V_A,V_B)\neq0$ — a positive-definite quadratic form has negative discriminant.
*Check:* the concentric-shell matrix of P33: all three $2\times2$ principal minors
positive; strictness margin computed. (`test_p31_schwarz`.)

**Solution.** With every other conductor grounded, (2.170) gives
$$W=\tfrac12\bigl[C_{AA}V_A^2+2C_{AB}V_AV_B+C_{BB}V_B^2\bigr]
=\tfrac1{8\pi}\int E^2\,d^3x\;\ge\;0 ,$$
and $W=0$ forces $\vec E\equiv0$ everywhere. Could a nonzero $(V_A,V_B)$ give
$\vec E\equiv0$? No: zero field means $\Phi$ constant in each connected component
of the vacuum; the grounded conductors (or the boundary at infinity, $\Phi\to0$,
which is part of every open system's boundary) pin that constant to $0$, forcing
$V_A=V_B=0$. So $W$ is **positive definite** on $(V_A,V_B)$.
A quadratic form $\frac12(c_{11}v_1^2+2c_{12}v_1v_2+c_{22}v_2^2)$ is positive
definite iff $c_{11}>0$ and $\det\begin{psmallmatrix}c_{11}&c_{12}\\c_{12}&c_{22}\end{psmallmatrix}>0$:
take $(1,0)$ to get $C_{AA}>0$; then minimize over $V_B$ at fixed $V_A$
(complete the square):
$$2W=C_{AA}V_A^2-\frac{C_{AB}^2}{C_{BB}}V_A^2+C_{BB}\Bigl(V_B+\frac{C_{AB}}{C_{BB}}V_A\Bigr)^2>0
\ \Longrightarrow\ C_{AA}C_{BB}-C_{AB}^2>0 ,$$
i.e. $C_{AB}^2<C_{AA}C_{BB}$. $\blacksquare$
Boundary case worth flagging: the idealized *closed two-conductor system* (e.g.
infinite parallel plates, (2.179)) has $C_{AB}^2=C_{AA}C_{BB}$ — there $V_A=V_B$
produces no field and no grounded reference exists to pin the constant; the strict
inequality is restored the moment infinity (or any third grounded surface) belongs
to the boundary. The concentric-shell numbers confirm strictness:
$C_{ab}^2/C_{aa}C_{bb}=\frac{a(c-b)}{b(c-a)}<1$.

### P32.  Exercise 2.12.2 — Symmetry and positivity of the coefficients  *(Wilcox 2e §2.14, p.82)*
(a) Use Green's reciprocation theorem (P17) to prove $C_{ij}=C_{ji}$ ($i\neq j$).
(b) Show the same from the Green-function representation (2.166). (c) Show
$C_{ii}>0$ from first principles.
*Answer:* (a) reciprocate the two unit-potential states; (b) (2.166) is a double
normal derivative of the symmetric $G_D$ over $S_i\times S_j$; (c) $W=\frac12C_{ii}>0$
for the state $V_i=1$, rest grounded.
*Check:* numeric inversion of the shell elastance matrix: symmetric to machine
precision, positive diagonal. (`test_p32_symmetry`.)

**Solution.** (a) State 1: $V_i=1$, all others $0$ — surface charges give
$Q_k=C_{ki}$ by the definition of the coefficients. State 2: $V_j=1$, others $0$ —
$Q'_k=C_{kj}$. Reciprocation with no volume charge,
$\sum_k Q_kV'_k=\sum_kQ'_kV_k$: the left side keeps only $k=j$ (the only conductor
with $V'\neq0$): $Q_j\cdot1=C_{ji}$; the right keeps $k=i$: $Q'_i\cdot1=C_{ij}$.
Hence $C_{ji}=C_{ij}$. $\blacksquare$
(b) The (2.166) representation writes each coefficient as
$$C_{ij}=-\frac1{16\pi^2}\oint_{S_i}\!\!da\oint_{S_j}\!\!da'\;
\frac{\partial^2G_D(\vec x,\vec x')}{\partial n\,\partial n'} ,$$
(unit potential on $S_j$ enters through $-\partial_{n'}G_D/4\pi$ as in (2.98), and
the induced density on $S_i$ through $\sigma=\partial_n\Phi/4\pi$, (2.92)). The
kernel is symmetric, $G_D(\vec x,\vec x')=G_D(\vec x',\vec x)$ (2.107), and the two
normal derivatives act on separate slots, so swapping $(i,\vec x)\leftrightarrow(j,\vec x')$
is a relabeling of integration variables: $C_{ij}=C_{ji}$. $\blacksquare$
(c) Put $V_i=1$, all others grounded. Then
$W=\frac12\sum_{kl}C_{kl}V_kV_l=\frac12C_{ii}$. But $W=\frac1{8\pi}\int E^2>0$
strictly — the field cannot vanish identically while conductor $i$ sits at unit
potential against grounded company (P31's pinning argument). Hence $C_{ii}>0$:
a conductor at positive potential above its grounded surroundings carries positive
charge. $\blacksquare$

### P33.  Exercise 2.12.3 — Capacitance matrix of three concentric shells  *(Wilcox 2e §2.14, p.82)*
Using $Q_i=\sum_jC_{ij}V_j$, find the six independent coefficients for three
concentric conducting shells of radii $a<b<c$ ($C_{aa},C_{bb},C_{cc},C_{ab},C_{ac},C_{bc}$).
Verify the P31 inequality on the three induction coefficients, the two sums (2.171)
for $j=a,b$, and the sum rule (2.178).
*Answer:*
$$C_{aa}=\frac{ab}{b-a},\quad C_{ab}=-\frac{ab}{b-a},\quad C_{ac}=0,\quad
C_{bb}=\frac{b^2(c-a)}{(b-a)(c-b)},\quad C_{bc}=-\frac{bc}{c-b},\quad
C_{cc}=\frac{c^2}{c-b};$$
$\sum_iC_{ia}=\sum_iC_{ib}=0$, $\sum_iC_{ic}=c=C_{\infty\infty}$; all Schwarz
inequalities strict.
*Check:* closed forms vs numeric inversion of the elastance matrix; the sums; the
inequalities. (`test_p33_shell_caps`.)

**Solution.** Charges $q_a,q_b,q_c$ produce (isolated-shell superposition, each
shell an equipotential):
$$V_a=\frac{q_a}a+\frac{q_b}b+\frac{q_c}c,\qquad
V_b=\frac{q_a+q_b}b+\frac{q_c}c,\qquad
V_c=\frac{q_a+q_b+q_c}c,$$
i.e. $V=P\,q$ with the elastance matrix (u=1/a etc.)
$P=\begin{psmallmatrix}u&v&w\\ v&v&w\\ w&w&w\end{psmallmatrix}$, $u=\frac1a,v=\frac1b,w=\frac1c$.
Then $C=P^{-1}$. Row-reducing, $\det P=(u-v)(v-w)w$, and the adjugate gives
$$C=\begin{pmatrix}\dfrac1{u-v}&-\dfrac1{u-v}&0\\[6pt]
-\dfrac1{u-v}&\dfrac{u-w}{(u-v)(v-w)}&-\dfrac1{v-w}\\[6pt]
0&-\dfrac1{v-w}&\dfrac{v}{(v-w)\,w}\end{pmatrix}.$$
Translate with $u-v=\frac{b-a}{ab}$, $v-w=\frac{c-b}{bc}$, $u-w=\frac{c-a}{ac}$:
$$C_{aa}=\frac{ab}{b-a},\quad C_{ab}=-\frac{ab}{b-a},\quad C_{ac}=0,$$
$$C_{bb}=\frac{c-a}{ac}\cdot\frac{ab}{b-a}\cdot\frac{bc}{c-b}=\frac{b^2(c-a)}{(b-a)(c-b)},\quad
C_{bc}=-\frac{bc}{c-b},\quad
C_{cc}=\frac1b\cdot\frac{bc}{c-b}\cdot c=\frac{c^2}{c-b}.$$
Physical reading: the $(a,b)$ gap is the standard spherical capacitor
$ab/(b-a)$; **$C_{ac}=0$** because shell $b$, grounded, completely screens $a$ from
$c$; $C_{cc}=c+\frac{bc}{c-b}$ is "sphere to infinity" plus the inner $(b,c)$ gap.
**Verifications.**
- *Schwarz (P31)*: $\dfrac{C_{ab}^2}{C_{aa}C_{bb}}=\dfrac{a(c-b)}{b(c-a)}<1$
  (since $b>a$, $c-b<c-a$); $\dfrac{C_{bc}^2}{C_{bb}C_{cc}}=\dfrac{b-a}{c-a}<1$;
  $C_{ac}^2=0<C_{aa}C_{cc}$. All strict ✓.
- *(2.171), $j=a$*: $C_{aa}+C_{ba}+C_{ca}=\frac{ab}{b-a}-\frac{ab}{b-a}+0=0$ ✓
  (every field line from the innermost shell lands on its neighbors — closed
  interior).
  *$j=b$*: over the common denominator $(b-a)(c-b)$:
  $-ab(c-b)+b^2(c-a)-bc(b-a)=b[-ac+ab+bc-ab-bc+ac]=0$ ✓.
- *(2.178)*: $j=c$ is *not* closed — the outer surface sees infinity:
  $C_{ac}+C_{bc}+C_{cc}=\frac{c^2-bc}{c-b}=c=C_{\infty\infty}$, the isolated
  capacitance of a sphere of radius $c$ ✓ — exactly the book's sum rule relating
  interior coefficients to the external capacitance. $\blacksquare$
### P34.  Exercise 2.12.4 — A hollow conductor beats its content  *(Wilcox 2e §2.14, p.83)*
Conductor B is hollow and encloses conductor A (arbitrary shapes, Fig. 2.22).
Show $C_{BB}>C_{AA}$.
*Answer:* enclosure forces $C_{AB}=-C_{AA}$ (every A field line ends on B); then
P31 gives $C_{AA}C_{BB}>C_{AB}^2=C_{AA}^2$, so $C_{BB}>C_{AA}$.
*Check:* two concentric spheres: $C_{BB}-C_{AA}=b>0$; and the 3-shell matrix
($C_{bb}>C_{aa}$, $C_{cc}>C_{bb}$ for the nested pairs). (`test_p34_enclosed`.)

**Solution.** Ground B and put A at $V_A=1$: the field is confined to the cavity
between A and B (outside B, the grounded shell and infinity are both at $\Phi=0$
with no enclosed net driving — by uniqueness $\Phi\equiv0$ there). Gauss over a
surface inside B's metal gives $Q_B^{\rm inner}=-Q_A$, and B's outer surface
carries nothing; hence the *totals* in this state, $Q_A=C_{AA}$ and $Q_B=C_{BA}$,
satisfy
$$C_{BA}=-C_{AA}.$$
(This is $\sum_iC_{ij}=0$, (2.171), applied to the closed cavity subsystem.)
Now invoke the strict Schwarz inequality (P31) on the pair $(A,B)$ — strict because
infinity is available as the zero reference outside B:
$$C_{AA}\,C_{BB}>C_{AB}^2=C_{AA}^2 .$$
Since $C_{AA}>0$ (P32c), divide: $C_{BB}>C_{AA}$. $\blacksquare$
Interpretation: $C_{BB}=C_{\rm gap}+C_{\rm out}$ — at $V_B=1,V_A=0$ conductor B
charges *both* its inner surface (against A, the gap capacitance, which equals
$C_{AA}$) *and* its outer surface (against infinity, $C_{\rm out}>0$); the hollow
conductor holds strictly more. Spheres make it concrete:
$C_{AA}=\frac{ab}{b-a}$, $C_{BB}=\frac{ab}{b-a}+b$, difference exactly $b$.

### P35.  Exercise 2.12.5 — The two-conductor system capacitance  *(Wilcox 2e §2.14, p.83)*
Conductors A and B in free space carry $+Q$ and $-Q$. With
$C\equiv Q/(V_A-V_B)$, show
$$C=\frac{\det\begin{pmatrix}C_{AA}&C_{AB}\\ C_{AB}&C_{BB}\end{pmatrix}}{\sum_{i,j}C_{ij}}
=\frac{C_{AA}C_{BB}-C_{AB}^2}{C_{AA}+2C_{AB}+C_{BB}},$$
and (b) that the field energy is $W=Q^2/2C$.
*Answer:* invert the $2\times2$ relation $q=CV$ for $V$ at $q=(Q,-Q)$; the
potential difference is $Q\sum C_{ij}/\det$. Energy: $W=\frac12q\cdot V=\frac12Q(V_A-V_B)$.
*Check:* shell matrix: $\det/\sum$ vs direct $Q/\Delta V$ from the inverted system;
$W$ both ways. (`test_p35_system_C`.)

**Solution.** (a) The state is defined by charges, so invert:
$V=C^{-1}q$ with
$C^{-1}=\dfrac1{\det C}\begin{psmallmatrix}C_{BB}&-C_{AB}\\-C_{AB}&C_{AA}\end{psmallmatrix}$,
$\det C=C_{AA}C_{BB}-C_{AB}^2$. With $q=(Q,-Q)$:
$$V_A=\frac{Q\,(C_{BB}+C_{AB})}{\det C},\qquad
V_B=-\frac{Q\,(C_{AA}+C_{AB})}{\det C},$$
$$V_A-V_B=\frac{Q\,\bigl(C_{AA}+2C_{AB}+C_{BB}\bigr)}{\det C}
\;\Longrightarrow\;
C=\frac{Q}{V_A-V_B}=\frac{\det C}{\sum_{i,j}C_{ij}} . \qquad\blacksquare$$
Note $\sum_{ij}C_{ij}>0$ (it is $2W$ for $V_A=V_B=1$, a legitimate nonzero state in
open space) and $\det C>0$ (P31): the system capacitance is positive.
(b) The energy at prescribed charges:
$$W=\tfrac12\sum_iQ_iV_i=\tfrac12\bigl[Q\,V_A+(-Q)\,V_B\bigr]
=\tfrac12\,Q\,(V_A-V_B)=\frac{Q^2}{2C} . \qquad\blacksquare$$
This is why $C$ as defined *is* the "capacitor" of circuit theory: charge $\pm Q$,
voltage $\Delta V=Q/C$, energy $Q^2/2C$ — with the matrix formula exposing how the
self- and induction coefficients combine (used numerically in P37–P39).

### P36.  Exercise 2.12.6 — A neighbor raises your capacitance  *(Wilcox 2e §2.14, p.84)*
Isolated conductor A has capacitance $C_A$. Let $C'_{AA}$ be its self-coefficient
after conductor B is brought nearby. Show $C'_{AA}>C_A$. (Hint: combine
Exercises 2.10.1 and 2.12.1.)
*Answer:* fix charge $Q$ on A and insert B uncharged: P26 lowers the energy,
$\frac{Q^2C'_{BB}}{2\det C'}<\frac{Q^2}{2C_A}$, i.e.
$C_A<\det C'/C'_{BB}=C'_{AA}-C'^2_{AB}/C'_{BB}<C'_{AA}$ by P31.
*Check:* sphere + grounded concentric shell: $ab/(b-a)>a$; and the energy chain
verified numerically on the shell system. (`test_p36_raising`.)

**Solution.** Work at **fixed charges**, where P26 (Exercise 2.10.1) applies.
Before: A alone with charge $Q$; $W_{\rm before}=Q^2/2C_A$. After: B introduced,
uncharged and insulated; the new equilibrium energy at charges $q=(Q,0)$ is, in
terms of the new matrix $C'$ (inverting as in P35),
$$W_{\rm after}=\tfrac12\,q\cdot C'^{-1}q=\frac{Q^2}2\,(C'^{-1})_{AA}
=\frac{Q^2}{2}\,\frac{C'_{BB}}{\det C'} .$$
P26: introducing the uncharged conductor strictly lowers the energy,
$W_{\rm after}<W_{\rm before}$:
$$\frac{C'_{BB}}{\det C'}<\frac1{C_A}
\;\Longleftrightarrow\;
C_A<\frac{\det C'}{C'_{BB}}=C'_{AA}-\frac{C'^2_{AB}}{C'_{BB}} .$$
And by P31 (Exercise 2.12.1) the subtracted term is positive whenever B actually
couples ($C'_{AB}\neq0$), so
$$C_A<C'_{AA}-\frac{C'^2_{AB}}{C'_{BB}}<C'_{AA}. \qquad\blacksquare$$
Two readings of $C'_{AA}$: it is A's charge at $V_A=1$ with **B grounded** — the
grounded neighbor pulls extra charge onto A; while $\det C'/C'_{BB}$ is the
effective capacitance with **B floating** (uncharged), which is *also* $\ge C_A$
but smaller than the grounded case. Concentric instance: $C_A=a$;
$C'_{AA}=ab/(b-a)>a$ always; floating shell $(b,c)$:
$\det C'/C'_{BB}=\bigl(\frac1a-\frac1b+\frac1c\bigr)^{-1}$, between $a$ and
$ab/(b-a)$. The test verifies the full chain numerically.

### P37.  Exercise 2.12.7 — Parallel-disk capacitance: near and far  *(Wilcox 2e §2.14, p.84)*
Two identical thin coaxial conducting disks of radius $R$ sit a distance $d$ apart
(system capacitance $C(d)$ in the sense of P35). Find the leading behavior for
(a) $d\ll R$; (b) $d\gg R$ (use $C_{\rm cir}=2R/\pi$ for a single thin disk, P12).
*Answer:* (a) $C\approx A/4\pi d=R^2/4d$ — the parallel-plate formula;
(b) $C\to C_{\rm cir}/2=R/\pi$ — two isolated disks in series through infinity.
*Check:* (a) from (2.182); (b) as the $d\to\infty$ limit of the P38/P39
monopole model; crossover scale $d\sim\pi R/4$ where the two expressions meet.
(`test_p37_plates_limits`.)

**Solution.** (a) For $d\ll R$ the gap field is the uniform slab field of (2.182):
charge $\pm Q$ spreads at $\sigma=\pm Q/\pi R^2$, $E_{\rm gap}=4\pi\sigma$,
$\Delta V=E\,d=4\pi\sigma d$, so
$$C=\frac{Q}{\Delta V}=\frac{\pi R^2}{4\pi d}=\frac{R^2}{4d}\qquad(d\ll R),$$
diverging as the plates close — edge (fringe) corrections are relative
$O\bigl(\frac dR\ln\frac Rd\bigr)$ and ignorable at leading order.
(b) For $d\gg R$ each disk is, to leading order, an isolated disk plus the
monopole potential of its partner (the P39 elastance model):
$$V_A=\frac{Q}{C_{\rm cir}}-\frac Qd,\qquad V_B=-\frac{Q}{C_{\rm cir}}+\frac Qd,$$
$$C(d)=\frac{Q}{V_A-V_B}=\frac1{2\bigl(\frac1{C_{\rm cir}}-\frac1d\bigr)}
\xrightarrow[d\to\infty]{}\frac{C_{\rm cir}}2=\frac R\pi\qquad(d\gg R).$$
The $\tfrac12$ is the series combination of each disk's capacitance "to infinity":
pulling the plates apart does not send $C\to0$ but to a floor set by the plates'
own size — the physical content of the isolated-disk $2R/\pi$ (P12). The two
regimes meet at $R^2/4d\sim R/\pi$, i.e. $d\sim\pi R/4$ — comparable to $R$, where
neither expansion is trustworthy. $\blacksquare$

### P38.  Exercise 2.12.8 — First correction at large separation  *(Wilcox 2e §2.14, p.84)*
Same two coaxial disks, $d\gg R$, $C_{\rm cir}=2R/\pi$: show
$$C(d)\approx\frac R\pi\Bigl(1+\frac{2R}{\pi d}\Bigr).$$
(Hint: far apart, each disk looks like a point charge to the other.)
*Answer:* expanding $C=\bigl[2(1/C_{\rm cir}-1/d)\bigr]^{-1}=\frac{R/\pi}{1-2R/\pi d}$
to first order.
*Check:* the exact monopole-model value vs the first-order form at $d/R=20,50$:
agreement $O((R/d)^2)$. (`test_p38_plates_correction`.)

**Solution.** Keep the P37(b) model to first order in $R/d$ — disk at potential
(own charge)/(own capacitance) plus partner monopole $\mp Q/d$:
$$V_A-V_B=2Q\Bigl(\frac1{C_{\rm cir}}-\frac1d\Bigr)
=2Q\,\frac{\pi}{2R}\Bigl(1-\frac{2R}{\pi d}\Bigr),$$
so
$$C(d)=\frac{Q}{V_A-V_B}=\frac{R}{\pi}\,\frac1{1-\dfrac{2R}{\pi d}}
\approx\frac R\pi\Bigl(1+\frac{2R}{\pi d}\Bigr). \qquad\blacksquare$$
Structure of the correction: $\frac R\pi\cdot\frac{2R}{\pi d}=C_{\rm sys}^0\,C_{\rm cir}/d$
— the partner's monopole *reduces* the voltage needed for the same charge
(opposite charges attract each other's potential down), so $C$ *rises* as the
plates approach, smoothly heading toward the $R^2/4d$ regime. Higher orders would
need the disk's response to a nonuniform field (induced multipoles, $O(d^{-3})$),
consistently dropped here. The test checks the expansion error scales as
$(R/d)^2$.

### P39.  Exercise 2.12.9 — Distant conductors of arbitrary shape  *(Wilcox 2e §2.14, pp.84–85)*
Two arbitrary conductors with isolated capacitances $C^0_{11}$, $C^0_{22}$ sit a
large distance $d$ apart ($d\gg$ any internal dimension).
(a) Argue $C_{12}(d)=C_{21}(d)\approx-\,C^0_{11}C^0_{22}/d$.
(b) From (a) argue $C_{22}(d)\approx C^0_{22}\big/\bigl(1+C_{12}(d)/d\bigr)$.
(c) Apply to the two coaxial disks and recover P38.
*Answer:* the monopole elastance matrix $P=\begin{psmallmatrix}1/C^0_{11}&1/d\\1/d&1/C^0_{22}\end{psmallmatrix}$
inverts to exactly these forms.
*Check:* numeric inversion of $P$ vs both approximations at large $d$; the disk
case reproduces $C(d)=(R/\pi)(1+2R/\pi d)$. (`test_p39_distant`.)

**Solution.** (a) To leading order each conductor is a point source to its partner
(shape enters only through its isolated capacitance):
$$V_1=\frac{Q_1}{C^0_{11}}+\frac{Q_2}d,\qquad V_2=\frac{Q_1}d+\frac{Q_2}{C^0_{22}},$$
i.e. $V=Pq$ with the symmetric elastance matrix above. Then $C=P^{-1}$:
$$C_{12}=\frac{-1/d}{\det P},\qquad
\det P=\frac1{C^0_{11}C^0_{22}}-\frac1{d^2}
=\frac1{C^0_{11}C^0_{22}}\Bigl(1-\frac{C^0_{11}C^0_{22}}{d^2}\Bigr),$$
$$C_{12}(d)=-\frac{C^0_{11}C^0_{22}}{d}\,\frac1{1-C^0_{11}C^0_{22}/d^2}
\approx-\frac{C^0_{11}C^0_{22}}{d}. \qquad\blacksquare$$
Physical version of the argument: put conductor 1 at $V_1=1$ with 2 grounded.
Conductor 1 carries $\approx C^0_{11}$; at distance $d$ it lifts 2's potential by
$C^0_{11}/d$; grounded 2 must neutralize that with charge
$Q_2\approx-C^0_{22}\cdot C^0_{11}/d=C_{21}$. Symmetric in $1\leftrightarrow2$ ✓.
(b) From the same inverse,
$$C_{22}=\frac{1/C^0_{11}}{\det P}=\frac{C^0_{22}}{1-C^0_{11}C^0_{22}/d^2}
=\frac{C^0_{22}}{1+C_{12}(d)/d}\,,$$
using (a) to rewrite $-C^0_{11}C^0_{22}/d^2=C_{12}/d$ — the book's form, exact
within the monopole model. Iterative reading: 2's own charge at unit potential is
$C^0_{22}$; its partner's induced $C_{12}$ feeds back potential $C_{12}/d$,
requiring a compensating geometric series
$C^0_{22}\bigl[1-C_{12}/d\cdot(-1)\cdots\bigr]$ that sums to the displayed ratio.
(c) Disks: $C^0_{11}=C^0_{22}=C_{\rm cir}=2R/\pi$. System capacitance (P35):
$$C(d)=\frac{\det C}{\sum C_{ij}}=\frac1{P_{11}+P_{22}-2P_{12}}
=\frac1{\frac{\pi}{2R}+\frac{\pi}{2R}-\frac2d}
=\frac{R/\pi}{1-\frac{2R}{\pi d}}\approx\frac R\pi\Bigl(1+\frac{2R}{\pi d}\Bigr),$$
(the middle identity — $C_{\rm sys}=1/(P_{11}+P_{22}-2P_{12})$ — follows from
$\Delta V=(P_{11}-P_{12})Q-(P_{12}-P_{22})(-Q)$), recovering P38 exactly. $\blacksquare$

### P40.  Exercise 2.12.10 — Variational upper bound on capacitance  *(Wilcox 2e §2.14, p.85)*
(a) A vacuum region $V$ is bounded by conducting surfaces; one is at unit
potential, the rest at zero. Given (2.147)/(2.181), the capacitance is
$C=\frac1{4\pi}\int_V|\vec\nabla\Phi|^2d^3x$ at the true solution $\Phi$. Show
that for *any* trial $\Psi$ matching the potential boundary values,
$$C\;\le\;C[\Psi]\equiv\frac1{4\pi}\int_V|\vec\nabla\Psi|^2\,d^3x .$$
(b) For a thin cylindrical capacitor (length $L$, radii $a<b$, end effects
ignored) use the trial $\Psi=(b-\rho)/(b-a)$ and compare $C[\Psi]$ with the exact
$C=L/[2\ln(b/a)]\approx0.721\,L$ at $b=2a$. (Fixed-potential trials bound $C$ from
above; fixed-charge methods, §3.10, bound from below.)
*Answer:* (a) $\Psi=\Phi+\eta$ with $\eta|_S=0$: the cross term vanishes by
Green's first identity, leaving $C[\Psi]=C+\frac1{4\pi}\int|\vec\nabla\eta|^2\ge C$.
(b) $C[\Psi]=\dfrac{L(a+b)}{4(b-a)}=0.750\,L$ at $b=2a$ — an upper bound $\sim4\%$
above $0.7213\,L$.
*Check:* quadrature of the functional for both trial and exact potentials;
$C[\Psi_{\rm exact}]=C$; inequality margin. (`test_p40_variational`.)

**Solution.** (a) Both $\Psi$ and the true $\Phi$ equal the same constants on every
boundary piece, so $\eta\equiv\Psi-\Phi$ vanishes on all of $S$. Expand:
$$C[\Psi]=\frac1{4\pi}\int|\vec\nabla\Phi|^2
+\frac1{2\pi}\int\vec\nabla\Phi\cdot\vec\nabla\eta
+\frac1{4\pi}\int|\vec\nabla\eta|^2 .$$
Cross term by Green's first identity (P16) with $\phi=\eta$, $\psi=\Phi$:
$$\int_V\vec\nabla\Phi\cdot\vec\nabla\eta
=\oint_S\eta\,\partial_n\Phi\,da-\int_V\eta\,\nabla^2\Phi\,d^3x=0-0=0,$$
($\eta|_S=0$; $\nabla^2\Phi=0$ in the charge-free region). Hence
$$C[\Psi]=C+\frac1{4\pi}\int_V|\vec\nabla\eta|^2\,d^3x\;\ge\;C,$$
with equality iff $\vec\nabla\eta\equiv0$, i.e. $\Psi=\Phi$. Dirichlet trials can
only *overestimate*: any deviation from harmonicity costs positive field energy at
fixed voltage. $\blacksquare$
(b) Trial $\Psi=(b-\rho)/(b-a)$: matches $\Psi=1$ at $\rho=a$, $0$ at $\rho=b$;
$|\vec\nabla\Psi|=1/(b-a)$:
$$C[\Psi]=\frac1{4\pi}\,\frac1{(b-a)^2}\int_a^b2\pi\rho L\,d\rho
=\frac{L}{2(b-a)^2}\cdot\frac{b^2-a^2}2=\frac{L\,(a+b)}{4(b-a)} .$$
At $b=2a$: $C[\Psi]=\frac{3a}{4a}L=0.750\,L$. The exact solution
$\Phi=\ln(b/\rho)/\ln(b/a)$ gives
$$C=\frac1{4\pi}\int_a^b\frac{2\pi L\,\rho\,d\rho}{\rho^2\ln^2(b/a)}
=\frac{L}{2\ln(b/a)}=\frac{L}{2\ln2}=0.7213\,L .$$
Indeed $0.750>0.7213$ — the linear trial overshoots by $4.0\%$: it misallocates
field energy toward the outer radius where the true field is weaker
($E\propto1/\rho$). The companion principle (§3.10) with charges fixed brackets
$C$ from below, sandwiching the true value — the standard variational squeeze for
capacitances. $\blacksquare$

### P41.  Exercise 2.12.11 — Three parallel wires in a triangle  *(Wilcox 2e §2.14, p.86)*
Three long parallel cylindrical conductors of common radius $a$ sit at the corners
of an equilateral triangle of side $d\gg a$ (Fig. 2.23), carrying charge per
length $-\lambda,-\lambda,+2\lambda$ on wires 1, 2, 3.
(a) With $C_L\equiv\lambda/(2V_3-V_1-V_2)$, show the energy per length is
$w=\lambda^2/(2C_L)$ — "standard form".
(b) Show $C_L=1/[N\ln(d/a)]$ and determine $N$.
*Answer:* (a) $w=\frac12\sum_i\lambda_iV_i=\frac\lambda2(2V_3-V_1-V_2)=\lambda^2/2C_L$;
(b) $V_1=V_2=-2\lambda\ln(d/a)$, $V_3=+4\lambda\ln(d/a)$, so
$2V_3-V_1-V_2=12\lambda\ln(d/a)$: $N=12$ (and $w=6\lambda^2\ln(d/a)$).
*Check:* the 2-D log-potential matrix: $N=12$, neutrality (K-independence), and
$w$ computed both as $\frac12\sum\lambda_iV_i$ and as $\lambda^2/2C_L$.
(`test_p41_three_wires`.)

**Solution.** (a) Energy per unit length of a set of line charges on equipotential
surfaces (the 2-D copy of (2.169)):
$$w=\frac12\sum_i\lambda_iV_i
=\frac12\bigl[(-\lambda)V_1+(-\lambda)V_2+2\lambda V_3\bigr]
=\frac\lambda2\,(2V_3-V_1-V_2)
=\frac\lambda2\cdot\frac{\lambda}{C_L}=\frac{\lambda^2}{2C_L},$$
directly from the definition of $C_L$ — the "standard form" $Q^2/2C$ with $\lambda$
playing $Q$. $\blacksquare$
(b) For $d\gg a$, each wire's potential is its own surface value plus the partners'
line potentials at distance $d$ (P6d: a line $\lambda_j$ contributes
$-2\lambda_j\ln(s/K)$ at distance $s$):
$$V_i=-2\lambda_i\ln\frac aK-2\sum_{j\neq i}\lambda_j\ln\frac dK .$$
Since $\sum_j\lambda_j=-\lambda-\lambda+2\lambda=0$, the arbitrary $K$ cancels —
the potentials are well defined without a far cutoff. Evaluate (take $K=1$):
$$V_1=2\lambda\ln a+2\lambda\ln d-4\lambda\ln d=-2\lambda\ln\frac da,\qquad V_2=V_1,$$
$$V_3=-4\lambda\ln a+2\lambda\ln d+2\lambda\ln d=+4\lambda\ln\frac da .$$
Then
$$2V_3-V_1-V_2=8\lambda\ln\frac da+4\lambda\ln\frac da=12\,\lambda\ln\frac da
\;\Longrightarrow\;
C_L=\frac{\lambda}{12\,\lambda\ln(d/a)}=\frac1{12\ln(d/a)} :\qquad N=12 .$$
Cross-check via the energy: $w=\frac12\sum\lambda_iV_i
=\frac12[2\lambda^2+2\lambda^2+8\lambda^2]\ln(d/a)=6\lambda^2\ln(d/a)
=\lambda^2/(2C_L)$ ✓ consistent. $\blacksquare$
(Each wire being $\ll d$ guarantees the equipotential surfaces are circles to
$O(a/d)$; corrections would enter as image-line displacements, shifting $N$ at
relative order $a/d$ — negligible by hypothesis. Note the combination
$2V_3-V_1-V_2$ is exactly the voltage conjugate to $\lambda$ under the charge
pattern $(-1,-1,+2)\lambda$: the mode actually excited.)
