# MACRO_EM-05 — Problems (Wilcox Ch. 5, all 49 exercises)

Every exercise of Wilcox & Thron 2e §5.13 (printed pp. 242–266), worked in
full. Statements are paraphrased (all given data and equations kept); the book
prints no solutions — everything below is module-authored and machine-checked
in `code/multipole_dielectrics.py` / `code/test_multipole_dielectrics.py`.
Sources in `../refs.md`.

**Conventions (the book's, Gaussian units).** Multipole expansion (5.12)
$$\Phi=\frac{q}{r}+\frac{\vec x\cdot\vec p}{r^3}+\frac12\sum_{ij}Q_{ij}\frac{x_ix_j}{r^5}+\dots,\qquad
Q_{ij}=\int d^3x'\,(3x_i'x_j'-\delta_{ij}r'^2)\rho;$$
polarization $\vec P=n\vec p$ (5.56), bound charge $\rho_b=-\vec\nabla\cdot\vec P$
(5.58), $\sigma_b=\vec P\cdot\hat n$ (5.59); $\vec D=\vec E+4\pi\vec P=\epsilon\vec E$
(5.64/5.68), $\epsilon=1+4\pi\chi$ (5.67); dielectric Green equation
$\vec\nabla\cdot[\epsilon(\vec x)\vec\nabla G]=-4\pi\delta$ (5.72); interface
conditions: $\Phi$ (hence $E_\parallel$) and $D_n$ continuous (5.86–5.87).
Energy $W=\frac1{8\pi}\int\vec E\cdot\vec D$ (5.164);
$\Delta W=\frac12\int\!\!\int\rho[G_D-G^0_D]\rho$ (5.169); forces
$\vec F=-\partial W/\partial\vec x|_Q$ (5.174) $=+\partial W/\partial\vec x|_V$
(5.179). Griffiths-level background: `~EM-05`/`~EM-07`.

---

### P1.  Exercise 5.1.1 — Can an origin shift kill the dipole moment?  *(Wilcox 2e §5.13, p.242)*
Prove or give a counterexample: for a charge distribution with **nonvanishing**
total charge $q$, one can always choose an origin that makes the dipole moment
$\vec p$ vanish.
*Answer:* **True.** Shifting the origin to $\vec R=\vec p/q$ gives $\vec p\,'=0$
(the "center of charge", the electrical analog of the center of mass).
*Check:* random charge sets: after the shift $|\vec p\,'|<10^{-12}$; for $q=0$
the dipole moment is origin-independent (`test_p01_dipole_killing_origin`).

**Solution.** Let the moments about the old origin be $q=\int\rho$,
$\vec p=\int\vec x'\rho$. About a new origin at $\vec R$ the position vectors
are $\vec x'-\vec R$, so
$$\vec p\,'=\int d^3x'\,(\vec x'-\vec R)\,\rho(\vec x')=\vec p-q\vec R.$$
If $q\neq0$ the choice $\vec R=\vec p/q$ is well defined and gives
$\vec p\,'=0$. (Conversely, when $q=0$, $\vec p\,'=\vec p$ for **every**
$\vec R$: the dipole moment of a neutral distribution is intrinsic — Eq. (5.39)
footnote's general pattern: the lowest nonvanishing multipole is
origin-independent.) $\blacksquare$

### P2.  Exercise 5.1.2 — Multipole moments under translation of origin  *(Wilcox 2e §5.13, p.242)*
A distribution has moments $q,\vec p,Q_{ij}$ about one origin and
$q',\vec p\,',Q'_{ij}$ about a second origin displaced by
$\vec R=(X,Y,Z)$ (axes parallel). Find the explicit connections.
*Answer:*
$$q'=q,\qquad \vec p\,'=\vec p-q\vec R,$$
$$Q'_{ij}=Q_{ij}-3(R_ip_j+R_jp_i)+2\,\delta_{ij}\,\vec R\cdot\vec p
+q\,(3R_iR_j-R^2\delta_{ij}).$$
*Check:* closed forms match direct recomputation of the moments about the
shifted origin for random charge sets to $10^{-10}$ (`test_p02_moment_translation`).

**Solution.** In the new frame the source point is $\vec y=\vec x'-\vec R$.
Monopole: $q'=\int\rho=q$. Dipole: $\vec p\,'=\int(\vec x'-\vec R)\rho
=\vec p-q\vec R$ (P1). Quadrupole: insert $\vec y$ into the definition,
$$Q'_{ij}=\int\big[3(x_i'-R_i)(x_j'-R_j)-\delta_{ij}(\vec x'-\vec R)^2\big]\rho.$$
Expand: $3x_i'x_j'-3R_ix_j'-3R_jx_i'+3R_iR_j$ and
$(\vec x'-\vec R)^2=r'^2-2\vec x'\cdot\vec R+R^2$. Integrating term by term,
$$Q'_{ij}=Q_{ij}-3R_i p_j-3R_j p_i+3qR_iR_j
+\delta_{ij}\big(2\vec R\cdot\vec p-qR^2\big),$$
which is the boxed form. Consistency checks: (i) trace: $\sum_iQ'_{ii}
=0-6\vec R\cdot\vec p+6\vec R\cdot\vec p+q(3R^2-3R^2)=0$ — still traceless;
(ii) if $q=0$ **and** $\vec p=0$, then $Q'_{ij}=Q_{ij}$: the quadrupole is
origin-independent exactly when all lower moments vanish (the general rule
stated after (5.39)).

### P3.  Exercise 5.1.3 — Cube with $\rho=Kx$  *(Wilcox 2e §5.13, p.242)*
A cube of side $L$ is centered on the origin, faces perpendicular to the axes,
filled with charge density $\rho(x,y,z)=Kx$ ($K$ constant).
(a) Compute the monopole, dipole, and **all** quadrupole moments.
(b) What is the leading far field?
*Answer:* (a) $q=0$; $\vec p=\dfrac{KL^5}{12}\hat\imath$; $Q_{ij}=0$ (all nine).
(b) A pure dipole field,
$\vec E=\dfrac{3(\vec p\cdot\hat r)\hat r-\vec p}{r^3}$ with the above
$\vec p$ — the first correction is octopole ($\ell=3$), down by $(L/r)^2$.
*Check:* 3-D Gauss–Legendre quadrature of all moments; far-field potential from
quadrature matches $\vec p\cdot\vec x/r^3$ to $2\times10^{-4}$
(`test_p03_cube_rho_Kx`).

**Solution.** (a) Monopole: $q=K\int x\,dV=0$ (odd in $x$).
Dipole: $p_x=K\int x^2dV=K\big(\int_{-L/2}^{L/2}x^2dx\big)L^2=K\frac{L^3}{12}L^2
=\frac{KL^5}{12}$; $p_y=K\int xy\,dV=0$ (odd in $y$), likewise $p_z=0$.
Quadrupole: every component is an integral of $Kx\times(\text{quadratic})$:
- $Q_{11}=K\int x(3x^2-r^2)dV$ — integrand odd in $x$ → 0; same for $Q_{22},Q_{33}$;
- $Q_{12}=3K\int x^2y\,dV=0$ (odd in $y$), $Q_{13}=3K\int x^2z\,dV=0$,
  $Q_{23}=3K\int xyz\,dV=0$ (odd in each).

So the quadrupole vanishes identically — not by symmetry of the *shape* alone
but because $\rho$ is odd under $x\to-x$ while every quadrupole integrand is
even-degree in the coordinates times $x$, hence odd under inversion of one axis.
(b) With $q=0$, $Q=0$, the expansion (5.12) starts and — through $\ell=2$ —
ends with the dipole term, $\Phi=\vec p\cdot\vec x/r^3$, so
$\vec E=[3(\vec p\cdot\hat r)\hat r-\vec p]/r^3$ (5.15). Because $\rho$ is odd
under $\vec x\to-\vec x$... more precisely under $x\to-x$, all *even*-$\ell$
moments vanish, so the next correction is the $\ell=3$ (octopole) term of P4,
smaller by $O(L^2/r^2)$.

### P4.  Exercise 5.1.4 — The octopole term $R_{ijk}$  *(Wilcox 2e §5.13, p.242)*
Work out the integral form of the next moment $R_{ijk}$ in
$$\Phi(\vec x)=\frac qr+\frac{\vec x\cdot\vec p}{r^3}
+\frac12\sum_{i,j}Q_{ij}\frac{x_ix_j}{r^5}
+\frac16\sum_{i,j,k}R_{ijk}\frac{x_ix_jx_k}{r^7}+\dots$$
and show $R_{ijk}$ has only **7** independent components.
*Answer:*
$$R_{ijk}=\int d^3x'\Big[15\,x_i'x_j'x_k'
-3r'^2\big(x_i'\delta_{jk}+x_j'\delta_{ik}+x_k'\delta_{ij}\big)\Big]\rho(\vec x').$$
Symmetric rank-3 → 10 components; the three trace conditions
$\sum_iR_{iik}=0$ cut it to $10-3=7$ ($=2\ell+1$ at $\ell=3$).
*Check:* the tensor from random charge sets is symmetric, traceless on every
pair, spans exactly a 7-dimensional space (matrix rank over samples), and its
contraction reproduces the residual $\Phi_{\rm exact}-\Phi_{q,p,Q}$ at large
$r$ (`test_p04_octopole`).

**Solution.** The $\ell=3$ Taylor term of $1/|\vec x-\vec x'|$ is
$-\frac1{3!}(\vec x'\cdot\vec\nabla)^3\frac1r$ (5.4–5.5). Two gradients gave
(5.8); the third gradient of $(3x_ix_j-\delta_{ij}r^2)/r^5$ gives
$$\partial_i\partial_j\partial_k\frac1r
=-\frac{15\,x_ix_jx_k}{r^7}
+\frac{3\,(x_i\delta_{jk}+x_j\delta_{ik}+x_k\delta_{ij})}{r^5},$$
symmetric and **traceless** on every pair (contract $j=k$:
$-15x_ir^2/r^7+3(x_i+x_i+3x_i)/r^5=0$ — harmonicity of $1/r$). With the
$(-1)^\ell$ of (5.4) the $\ell=3$ contribution to $\Phi$ is
$$\Phi_3=\frac16\int d^3x'\,\rho\sum_{ijk}x_i'x_j'x_k'
\Big[\frac{15x_ix_jx_k}{r^7}
-\frac{3(x_i\delta_{jk}+x_j\delta_{ik}+x_k\delta_{ij})}{r^5}\Big].$$
Regroup source and field factors as in (5.10): the $\delta$-terms contract two
*source* indices into $r'^2$ and leave one $x$-factor, e.g.
$\sum_{jk}x_j'x_k'\delta_{jk}\,x_i x_i'\cdot 3/r^5
=3r'^2(\vec x\cdot\vec x')/r^5=\sum_{ijk}\frac{x_ix_jx_k}{r^7}\,
r'^2x_i'\delta_{jk}\,$-pieces after symmetrization, so
$$\Phi_3=\frac16\sum_{ijk}\frac{x_ix_jx_k}{r^7}\,R_{ijk},\qquad
R_{ijk}=\int\!\big[15x_i'x_j'x_k'
-3r'^2(x_i'\delta_{jk}+x_j'\delta_{ik}+x_k'\delta_{ij})\big]\rho\,d^3x' .$$
(Because the field tensor is traceless, only the traceless part of
$x_i'x_j'x_k'$ survives the contraction — so $R_{ijk}$ may be, and here is,
defined traceless with no loss.)
*Counting:* a symmetric rank-3 tensor in 3-D has $\binom{3+2}{3}=10$
independent entries. Tracelessness $\sum_iR_{iik}=0$ is one condition for each
$k$ (and by symmetry every other trace coincides with these): 3 conditions,
leaving $10-3=7=2\cdot3+1$ — exactly the number of $Y_{3m}$'s, as the spherical
expansion (5.20) predicts.

### P5.  Exercise 5.1.5 — Linear quadrupole  *(Wilcox 2e §5.13, pp.242–243)*
Charges $+1$ at $z=\pm a$ on the 3-axis and $-2$ at the origin (the book's
Fig. 5.21).
(a) From the Cartesian expansion (dipole + quadrupole), find the leading
potential for $r\gg a$.
(b) Confirm by Taylor-expanding the exact potential.
*Answer:* $q=0$, $\vec p=0$;
$Q_{33}=4a^2$, $Q_{11}=Q_{22}=-2a^2$ (off-diagonals zero);
$$\Phi\simeq\frac{a^2(3\cos^2\theta-1)}{r^3}=\frac{2a^2}{r^3}P_2(\cos\theta).$$
*Check:* moments computed from the point set; quadrupole formula equals
$\frac12\sum Q_{ij}x_ix_j/r^5$ exactly and the exact 3-charge potential to
$O(a^2/r^2)$ relative (`test_p05_linear_quadrupole`).

**Solution.** (a) $q=1+1-2=0$; $\vec p=(+1)(a\hat k)+(+1)(-a\hat k)=0$.
Quadrupole ($Q_{ij}=\sum_nq_n(3x_ix_j-\delta_{ij}r^2)_n$): the two $\pm a$
charges each give $3z^2-r^2=2a^2$ on the 33 component and $-a^2$ on 11 and 22;
the central charge sits at $r=0$:
$$Q_{33}=2(3a^2-a^2)=4a^2,\qquad Q_{11}=Q_{22}=2(0-a^2)=-2a^2.$$
Then
$$\Phi=\frac12\sum_{ij}Q_{ij}\frac{x_ix_j}{r^5}
=\frac{-2a^2(x^2+y^2)+4a^2z^2}{2r^5}
=\frac{a^2(3z^2-r^2)}{r^5}=\frac{2a^2}{r^3}P_2(\cos\theta).$$
(b) Exactly, with $\cos\theta=\hat r\cdot\hat k$ and $r>a$ the Legendre
generating function gives
$$\Phi=\frac1{|\vec r-a\hat k|}+\frac1{|\vec r+a\hat k|}-\frac2r
=\frac2r\sum_{\ell\text{ even}}\Big(\frac ar\Big)^\ell P_\ell(\cos\theta)-\frac2r
=\frac{2a^2}{r^3}P_2+\frac{2a^4}{r^5}P_4+\dots,$$
whose leading term is (a); odd $\ell$ cancels between $\pm a$ and the monopole
cancels against $-2/r$. The next correction is down by $(a/r)^2$ — the
prolate ($Q_{33}>0$) case of Fig. 5.3.

### P6.  Exercise 5.1.6 — Dipole above a conducting plane  *(Wilcox 2e §5.13, p.243)*
(a) A neutral atom with dipole moment $\vec p=(p_x,p_y,p_z)$ sits at height
$d$ on the $z$-axis above the grounded conducting plane $z=0$. Find
$\Phi(\vec x)$ for $z>0$ by the image method.
(b) For $\vec p=p_z\hat k$, find the induced surface density $\sigma$.
*Answer:* (a) image dipole $\vec p\,''=(-p_x,-p_y,+p_z)$ at $(0,0,-d)$:
$$\Phi=\frac{\vec p\cdot(\vec x-d\hat k)}{|\vec x-d\hat k|^3}
+\frac{\vec p\,''\cdot(\vec x+d\hat k)}{|\vec x+d\hat k|^3}.$$
(b) $\displaystyle\sigma(\rho)=\frac{p_z}{2\pi}\,
\frac{2d^2-\rho^2}{(\rho^2+d^2)^{5/2}}$, with $\int\sigma\,da=0$.
*Check:* $\Phi=0$ on the plane; $\sigma$ matches
$-\frac1{4\pi}\partial\Phi/\partial z|_{0^+}$ by finite differences; total
induced charge integrates to $0$ (`test_p06_dipole_over_plane`).

**Solution.** (a) A dipole is the limit of charges $\pm q$ at
$d\hat k\pm\frac{\vec\delta}2$ with $\vec p=q\vec\delta$. Each charge images as
usual: $q\to-q$ reflected through $z=0$. The image pair sits at
$-d\hat k\mp\frac{\vec\delta^{\,*}}2$ where $\vec\delta^{\,*}=(\delta_x,\delta_y,-\delta_z)$
is the reflection of $\vec\delta$, with the charges swapped in sign. The image
dipole is therefore $\vec p\,''=-q\vec\delta^{\,*}=(-p_x,-p_y,+p_z)$: the
transverse components flip, the vertical one survives. On $z=0$ the two dipole
potentials cancel pointwise (each charge cancels its own mirror), so $\Phi=0$
there and uniqueness makes this *the* $z>0$ solution.
(b) With $\vec p=p_z\hat k$,
$\Phi=p_z(z-d)/R_1^3+p_z(z+d)/R_2^3$, $R_{1,2}^2=\rho^2+(z\mp d)^2$. On the
plane $R_1=R_2=R=(\rho^2+d^2)^{1/2}$ and
$$\frac{\partial\Phi}{\partial z}\Big|_{z=0}
=2p_z\Big[\frac1{R^3}-\frac{3d^2}{R^5}\Big]
=\frac{2p_z(\rho^2-2d^2)}{R^5}.$$
The conductor's surface charge is $\sigma=\frac1{4\pi}E_n=-\frac1{4\pi}
\partial_z\Phi|_{0^+}$, giving the boxed $\sigma$. For $p_z>0$ the induced
charge is positive in the near zone directly beneath the dipole and switches
sign on the circle $\rho=\sqrt2\,d$. The total,
$\int_0^\infty\sigma\,2\pi\rho\,d\rho\propto\int_{d^2}^\infty
\frac{(3d^2-u)}{u^{5/2}}du=0$: a neutral source induces zero net charge.

### P7.  Exercise 5.2.1 — Cylindrically symmetric quadrupole: energy and force  *(Wilcox 2e §5.13, pp.243–244)*
(a) For a quadrupole with $Q_{11}=Q_{22}=-\tfrac12Q_{33}$ (others zero) in an
external potential $\Phi$, show
$$W=\frac14Q_{33}\frac{\partial^2\Phi}{\partial z^2},\qquad
\vec F=\frac14Q_{33}\frac{\partial^2\vec E}{\partial z^2}.$$
(b) With the quadrupole at the origin and a point dipole
$\vec p=(p_x,p_y,p_z)$ at $\vec x_1=(x_1,0,0)$ (Fig. 5.22), find the force on
the quadrupole along direction 1.
*Answer:* (b) $\displaystyle F_1=-\frac{3\,Q_{33}\,p_x}{x_1^{5}}$.
*Check:* $W=\frac14Q_{33}\Phi_{zz}$ equals $\frac16\sum Q_{ij}\Phi_{ij}$ and the
microscopic $\sum q_i\Phi(x_i)$; $\vec F$ equals $-\vec\nabla W$; (b) matches
the point-charge model of quadrupole + dipole to $5\times10^{-4}$
(`test_p07_quad_energy_and_force`).

**Solution.** (a) The quadrupole energy in an external field is (from (5.25),
written with derivatives at the quadrupole's location)
$W_Q=\frac16\sum_{ij}Q_{ij}\,\partial_i\partial_j\Phi$. With the symmetric
$Q_{ij}$ and $\nabla^2\Phi=0$ at the (source-free) quadrupole position,
$$W_Q=\frac16Q_{33}\Big[\Phi_{33}-\tfrac12(\Phi_{11}+\Phi_{22})\Big]
=\frac16Q_{33}\Big[\Phi_{33}+\tfrac12\Phi_{33}\Big]
=\frac14Q_{33}\frac{\partial^2\Phi}{\partial z^2}.$$
The force is $\vec F=-\vec\nabla W=-\frac14Q_{33}\vec\nabla\Phi_{zz}
=\frac14Q_{33}\partial_z^2(-\vec\nabla\Phi)=\frac14Q_{33}\,
\partial^2\vec E/\partial z^2$ (derivatives commute).
(b) The dipole's field is $\vec E=[3(\vec p\cdot\hat s)\hat s-\vec p]/s^3$ with
$\vec s=\vec x-\vec x_1$. Rather than differentiate blindly, use the
interaction energy with $\vec x$ the separation from dipole to quadrupole
(magnitude $x_1$ along $-\hat 1$): from (5.28)-type algebra, or directly from
(a): $W(\vec x_0)=\frac14Q_{33}\,\partial_z^2\Phi_{\rm dip}(\vec x_0)$.
On the 1-axis ($\vec s=-x_1\hat 1$),
$\Phi_{\rm dip}=\vec p\cdot\vec s/s^3$ gives
$\partial_z^2\Phi_{\rm dip}|_{\vec x_0=0}=3p_xx_1/x_1^5\cdot\ldots$ — carrying
it out (or by the code's algebra):
$W(x_1)=\frac34\,Q_{33}\,p_x/x_1^4$. Moving the quadrupole toward the dipole
decreases the separation, so
$$F_1=-\frac{\partial W}{\partial(\text{quadrupole 1-coordinate})}
=+\frac{dW}{dx_1}=-3\,Q_{33}\,p_x\,x_1^{-5}.$$
Only $p_x$ (the component along the line of centers) contributes at this
order; for $Q_{33}p_x>0$ the quadrupole is pulled *away* from the dipole.

### P8.  Exercise 5.2.2 — Quadrupole–quadrupole interaction  *(Wilcox 2e §5.13, pp.244–245)*
Two cylindrically symmetric quadrupoles $Q^{(1)}_{ij}$, $Q^{(2)}_{ij}$
($Q^{(i)}_{11}=Q^{(i)}_{22}=-\frac12Q^{(i)}_{33}$), both symmetry axes along
the 3-direction, separated by $r=|x_1|$ along the **1**-direction (Fig. 5.23).
Show the interaction energy is $W_{QQ}\propto Q^{(1)}_{33}Q^{(2)}_{33}/r^5$
with coefficient $9/16$. **Extra:** repeat with the axes *and* the separation
all along 3.
*Answer:*
$$W_{QQ}=+\frac{9}{16}\frac{Q^{(1)}_{33}Q^{(2)}_{33}}{r^5}
\qquad\text{(perpendicular geometry)},\qquad
W^{33}_{QQ}=+\frac32\frac{Q^{(1)}_{33}Q^{(2)}_{33}}{r^5}
\quad\text{(collinear)}.$$
**The book prints $-\tfrac9{16}$; the sign is an erratum** — like-sign
$Q_{33}$'s in the Fig. 5.23 geometry *repel* (see check).
*Check:* microscopic 6-charge sums at $a/r=0.05$ and $0.025$ converge to
$+\frac9{16}Q_1Q_2/r^5$ and $+\frac32Q_1Q_2/r^5$ with $O(a^2)$ error — both
positive (`test_p08_quad_quad_energy`).

**Solution.** Use P7(a) with $\Phi_2$ = potential of quadrupole 2. From P5's
algebra, a symmetric quadrupole's potential is
$$\Phi_2(\vec y)=\frac{Q^{(2)}_{33}}{4}\,\frac{3y_3^2-y^2}{y^5},$$
with $\vec y$ measured from quadrupole 2. Then
$W=\frac14Q^{(1)}_{33}\,\partial^2\Phi_2/\partial y_3^2$ evaluated at
quadrupole 1's position.
*Perpendicular case* $\vec y=(\mp r,0,0)$: with
$f=(2y_3^2-y_1^2-y_2^2)/y^5$,
$$\partial_{y_3}^2f\Big|_{(r,0,0)}=\frac4{r^5}-\frac{5(-r^2)}{r^7}
=\frac9{r^5}\;\Longrightarrow\;
W=\frac14Q^{(1)}_{33}\cdot\frac{Q^{(2)}_{33}}4\cdot\frac9{r^5}
=\frac9{16}\frac{Q^{(1)}_{33}Q^{(2)}_{33}}{r^5}.$$
*Collinear case* $\vec y=(0,0,r)$: on the axis $f=2/y_3^3$, so
$\partial_{y_3}^2f=24/r^5$ and
$W=\frac14Q_{33}^{(1)}\frac{Q^{(2)}_{33}}4\frac{24}{r^5}
=\frac32Q^{(1)}_{33}Q^{(2)}_{33}/r^5$.
*Sign verdict:* the microscopic check (two $(+1,-2,+1)$ triplets) gives
$W=+9a^4/r^5\cdot(1+O(a^2/r^2))$ — positive — matching $+9/16\,(4a^2)^2/r^5$;
the printed minus sign cannot be reproduced by any orientation consistent with
Fig. 5.23. Physically: two prolate charge "dumbbells" side by side present
like charges broadside and repel; end-to-end they also repel (positive tips
adjacent), consistent with both signs found. Both configurations are
*unstable* extrema in orientation — tilting one axis lowers $W$ (the T-shaped
$45°$ arrangements are where quadrupoles attract).

### P9.  Exercise 5.2.3 — Charge and grounded sphere: summing the multipole series  *(Wilcox 2e §5.13, p.245)*
A charge $q$ sits a distance $D$ from the center of a grounded conducting
sphere of radius $R<D$. The image solution gives
$$W=q\Big({-q\frac RD}\Big)\frac1{D-\frac{R^2}D}=-\frac{q^2R}{D^2}\,
\frac1{1-\frac{R^2}{D^2}}.$$
Treating charge + image as a separable configuration about the sphere's
center, sum the spherical multipole interaction series (5.32)/(5.37) and
recover this result.
*Answer:* $\displaystyle W=\sum_{\ell=0}^\infty q'\Big(\frac{R^2}D\Big)^\ell
\frac{q}{D^{\ell+1}}=\frac{qq'}{D}\frac1{1-R^2/D^2}$ with $q'=-qR/D$ — a
geometric series in $(R/D)^2$.
*Check:* partial sums converge geometrically to the closed form (ratio
$(R^2/D^2)^{L}$), which equals $qq'/(D-R^2/D)$ exactly
(`test_p09_sphere_multipole_sum`).

**Solution.** The induced surface charge of the grounded sphere is *exactly*
equivalent, for all exterior fields, to the image $q'=-qR/D$ at
$\vec x''=(R^2/D)\hat z$ (taking the charge on $+\hat z$). Take
$\rho_<$ = image charge (interior), $\rho_>$ = the real charge at $D$: the
configuration is separable in the book's sense (all of $\rho_<$ lies at radius
$R^2/D<$ all of $\rho_>$ at $D$). The moments (5.33)–(5.34) of on-axis point
charges carry only $m=0$:
$$(\rho_<)_{\ell0}=q'\Big(\frac{R^2}D\Big)^{\ell},\qquad
(\rho_>)_{\ell0}=\frac{q}{D^{\ell+1}},$$
(using $\sqrt{4\pi/(2\ell+1)}\,Y_{\ell0}(0)=P_\ell(1)=1$). Then (5.37):
$$W=\sum_{\ell m}(\rho_<)^*_{\ell m}(\rho_>)_{\ell m}
=\frac{qq'}D\sum_{\ell=0}^\infty\Big(\frac{R^2}{D^2}\Big)^{\ell}
=\frac{qq'}{D}\,\frac{1}{1-R^2/D^2}=-\frac{q^2R}{D^2\big(1-\frac{R^2}{D^2}\big)}.$$
Note this $W$ is the charge–surface interaction energy (the full image-Coulomb
value), *not* the $\frac12$-weighted work of assembly — exactly what the
product formula (5.37) computes. Each $\ell$ term is the interaction of the
charge with the sphere's induced $2^\ell$-pole; the $\ell=0$ term
$qq'/D=-q^2R/D^2$ is the "grounded monopole" attraction that survives at
$D\gg R$.

### P10.  Exercise 5.3.1 — Alternate force form; torque on a distribution  *(Wilcox 2e §5.13, p.245)*
(a) Show the force (5.51)/(5.52) can also be written
$$\vec F=q\vec E^{(0)}(0)+(\vec p\cdot\vec\nabla)\vec E^{(0)}\big|_0
+\frac16\sum_{ij}Q_{ij}\frac{\partial^2\vec E^{(0)}}{\partial x_i\partial x_j}\Big|_0+\dots,$$
spelling out the assumptions.
(b) Show the torque is (either form)
$$N_i=(\vec p\times\vec E^{(0)}(0))_i
+\frac13\sum_{jkm}\epsilon_{ijk}Q_{jm}\frac{\partial E^{(0)}_k}{\partial x_m}\Big|_0 ,$$
or the same with $\partial E^{(0)}_m/\partial x_k$.
*Answer:* (a) requires $\vec\nabla\times\vec E^{(0)}=0$ **and**
$\vec\nabla\cdot\vec E^{(0)}=0$ throughout the distribution (no external
sources there); (b) the two quoted forms are equal *because*
$\partial_mE_k=\partial_kE_m$ for the curl-free external field.
*Check:* multipole force and torque against exact sums for random compact
clouds in the field of external point charges; error is next-order small and
shrinks with cloud size (`test_p10_force_torque_multipole`).

**Solution.** (a) Start from $\vec F=\int\rho\vec E^{(0)}$ (5.41) and Taylor
expansion (5.42). *Dipole term:* $\int\rho\,(\vec x\cdot\vec\nabla')\vec E^{(0)}$
is already $(\vec p\cdot\vec\nabla)\vec E^{(0)}$ — the identity (5.44),
$\vec\nabla(\vec x\cdot\vec E^{(0)})=(\vec x\cdot\vec\nabla)\vec E^{(0)}$,
needs $\vec\nabla\times\vec E^{(0)}=0$ and converts it to the gradient form of
(5.52); running it backwards is where curl-freeness enters. *Quadrupole term:*
the raw Taylor coefficient is $\frac12\sum_{ij}x_ix_j\partial_i\partial_j\vec E$;
to replace $x_ix_j\to\frac13(3x_ix_j-r^2\delta_{ij})$ (which builds $Q_{ij}$)
one must add $-\frac16r^2\delta_{ij}\partial_i\partial_j\vec E
=-\frac16r^2\nabla^2\vec E$, and $\nabla^2\vec E^{(0)}
=\vec\nabla(\vec\nabla\cdot\vec E^{(0)})-\vec\nabla\times(\vec\nabla\times\vec E^{(0)})=0$
requires **both** $\vec\nabla\cdot\vec E^{(0)}=0$ (no external charge inside
the distribution) and curl-freeness (statics). With those assumptions the
term is $\frac16\sum Q_{ij}\partial_i\partial_j\vec E^{(0)}$. So (5.52) and
(5.53) agree in electrostatics whenever the external sources don't overlap the
distribution — the book's remark after (5.53).
(b) $\vec N=\int\rho\,\vec x\times\vec E^{(0)}(\vec x)\,d^3x$. Expand
$E^{(0)}_k(\vec x)=E^{(0)}_k(0)+x_m\partial_mE^{(0)}_k+\dots$:
$$N_i=\epsilon_{ijk}\Big[\int\rho x_j\Big]E^{(0)}_k(0)
+\epsilon_{ijk}\Big[\int\rho\,x_jx_m\Big]\partial_mE^{(0)}_k+\dots
=(\vec p\times\vec E^{(0)})_i
+\epsilon_{ijk}\,\overline{x_jx_m}\,\partial_mE^{(0)}_k,$$
with $\overline{x_jx_m}\equiv\int\rho x_jx_m=\frac13\big(Q_{jm}+\delta_{jm}\int\rho r^2\big)$.
The $\delta_{jm}$ piece contributes
$\epsilon_{ijk}\partial_jE_k^{(0)}\propto(\vec\nabla\times\vec E^{(0)})_i=0$,
leaving $N_i=(\vec p\times\vec E^{(0)})_i+\frac13\epsilon_{ijk}Q_{jm}\partial_mE^{(0)}_k$.
Since $\partial_mE_k=\partial_kE_m$ (curl-free), swapping them gives the second
quoted form — showing one *is* sufficient. (The $r^2$ moment — the "scalar
radius" — never exerts torque or force in a source-free external field: only
the traceless moments are mechanically visible.)
### P11.  Exercise 5.4.1 — Effective densities from a quadrupole density  *(Wilcox 2e §5.13, p.246)*
Starting from the quadrupole term of the force expansion of P10(a), argue
that atoms with quadrupole density $q_{ij}(\vec x)\equiv n(\vec x)Q_{ij}(\vec x)$
contribute a bulk effective charge density
$$\rho^Q_{\rm eff}=\frac16\sum_{ij}\frac{\partial^2q_{ij}}{\partial x_i\partial x_j},$$
plus surface densities
$$\sigma^Q_{\rm eff}=-\frac16\sum_{ij}\hat n_j\frac{\partial q_{ij}}{\partial x_i},
\qquad
(P^Q_{\rm eff})_j=\frac16\sum_i\hat n_i\,q_{ij}$$
($\hat n$ = outward normal), the last acting like the surface restriction of
(5.55).
*Answer:* two integrations by parts of
$\vec F=\int\frac16q_{ij}\,\partial_i\partial_j\vec E\,d^3x$ generate exactly
these three terms.
*Check:* quadrature for $q_{ij}=x_1(1+r^2/R_b^2)T_{ij}$ in a ball, external
point-charge field: $\vec F_{\rm direct}=\vec F_{\rho}+\vec F_{\sigma}+\vec F_{P}$
to $2\times10^{-4}$ relative (`test_p11_quadrupole_effective_densities`).

**Solution.** Summing P10(a)'s quadrupole force over atoms and smoothing,
$$F_k=\frac16\int_Vd^3x\;q_{ij}(\vec x)\,\partial_i\partial_jE_k.$$
Integrate by parts in $x_i$:
$F_k=\frac16\oint da\,\hat n_i\,q_{ij}\,\partial_jE_k
-\frac16\int(\partial_iq_{ij})\,\partial_jE_k$; integrate the volume term by
parts again in $x_j$:
$$F_k=\underbrace{\frac16\oint da\,(\hat n_iq_{ij})\,\partial_jE_k}_{\text{surface polarization}}
-\underbrace{\frac16\oint da\,\hat n_j(\partial_iq_{ij})\,E_k}_{\sigma^Q_{\rm eff}E_k}
+\underbrace{\frac16\int d^3x\,(\partial_i\partial_jq_{ij})\,E_k}_{\rho^Q_{\rm eff}E_k}.$$
Reading off: the volume piece defines $\rho^Q_{\rm eff}$; the middle surface
piece is an ordinary surface charge $\sigma^Q_{\rm eff}=-\frac16\hat n_j\partial_iq_{ij}$;
the first surface piece has the structure $\oint(\vec{\mathcal P}\cdot\vec\nabla)E_k$
with $(\mathcal P^Q_{\rm eff})_j=\frac16\hat n_iq_{ij}$ — the surface analog of
the bulk dipole-force integrand $(\vec P\cdot\vec\nabla)\vec E$ in (5.55),
i.e. a surface *polarization* (dipole layer), not a surface charge. Note the
bookkeeping is exactly one derivative deeper than the dipole case: there
$-\vec\nabla\cdot\vec P$ plus $\sigma=\vec P\cdot\hat n$; here two derivatives
distribute into (volume) + (surface charge) + (surface dipole layer). The
book's bracketed note — that $\vec{\mathcal P}^Q_{\rm eff}$ can be regrouped as
a volume polarization $\vec P^Q_{\rm eff}$ with $(P^Q)_j=-\frac16\partial_iq_{ij}$
plus the same surface term — is the single-integration-by-parts reading of the
same identity.

### P12.  Exercise 5.4.2 — Bound charge from free charge in a linear dielectric  *(Wilcox 2e §5.13, p.246)*
(a) Show that inside a linear isotropic dielectric of constant $\epsilon$,
$$\rho_{\rm bound}=\Big(\frac{1-\epsilon}{\epsilon}\Big)\rho_{\rm free}.$$
(b) Deduce that for arbitrary geometry the **total** bound surface charge is
$$\int da\,\sigma_{\rm bound}=\Big(\frac{\epsilon-1}{\epsilon}\Big)Q_{\rm free}.$$
*Check:* dielectric sphere with a central free charge: $\sigma_b=(\epsilon-1)q/(4\pi\epsilon a^2)$,
total $(\epsilon-1)q/\epsilon$; net charge seen from outside $=q$
(`test_p12_bound_free_charge`).

**Solution.** (a) Inside the material, $\vec\nabla\cdot\vec E=4\pi(\rho_f+\rho_b)$
(5.61) while $\vec\nabla\cdot\vec D=4\pi\rho_f$ (5.65) with $\vec D=\epsilon\vec E$
and constant $\epsilon$ gives $\vec\nabla\cdot\vec E=4\pi\rho_f/\epsilon$ (5.70).
Subtracting,
$$4\pi\rho_b=4\pi\rho_f\Big(\frac1\epsilon-1\Big)
\;\Longrightarrow\;\rho_b=\frac{1-\epsilon}{\epsilon}\rho_f .$$
Each embedded free charge is screened by a *co-located* bound charge of
opposite sign and fraction $(\epsilon-1)/\epsilon$.
(b) The dielectric is neutral: its total bound charge (volume + surface)
vanishes,
$\int\rho_b\,d^3x+\oint\sigma_b\,da=0$. With (a),
$$\oint\sigma_b\,da=-\int\rho_b\,d^3x
=\frac{\epsilon-1}{\epsilon}\int\rho_f\,d^3x
=\frac{\epsilon-1}{\epsilon}Q_{\rm free}.$$
The screening charge "pushed off" every interior free charge reappears on the
surface, restoring the full $Q_{\rm free}$ as seen by a distant Gaussian
surface — the mechanism behind P25's far-field monopole.

### P13.  Exercise 5.4.3 — Dielectric cylinder in a uniform field  *(Wilcox 2e §5.13, pp.246–247)*
An infinite dielectric cylinder (radius $a$, constant $\epsilon$) is placed in
an initially uniform field $E_0\hat y$ (the book's Fig. 5.24 — its caption
says "magnetic field", an erratum for *electric*). Solve the boundary-value
problem (polar solutions of §3.7) and show
$$\Phi_{\rm in}=-\frac{2E_0}{\epsilon+1}\,\rho\sin\phi,\qquad
\Phi_{\rm out}=-E_0\rho\sin\phi+E_0\,\frac{\epsilon-1}{\epsilon+1}\,
\frac{a^2}{\rho}\sin\phi.$$
*Check:* continuity of $\Phi$ and of $\epsilon\,\partial_\rho\Phi$ at $\rho=a$,
FD-Laplacian $\approx0$ both sides, uniform interior field
$E_{\rm in}=2E_0/(\epsilon+1)$, and the $\epsilon\to1$ limit
(`test_p13_cylinder_in_uniform_field`).

**Solution.** With $y=\rho\sin\phi$, the driving potential is
$-E_0\rho\sin\phi$: pure $m=1$, $\sin\phi$ symmetry. The §3.7 separable
solutions with this symmetry are $\rho\sin\phi$ and $\rho^{-1}\sin\phi$.
Regularity at the axis and the far-field condition force
$$\Phi_{\rm in}=A\rho\sin\phi,\qquad
\Phi_{\rm out}=-E_0\rho\sin\phi+\frac{B}{\rho}\sin\phi .$$
Match at $\rho=a$: continuity of $\Phi$ (tangential $E$): $Aa=-E_0a+B/a$;
continuity of $D_\rho$: $\epsilon A=-E_0-B/a^2$. Solving,
$$A=-\frac{2E_0}{\epsilon+1},\qquad B=E_0a^2\,\frac{\epsilon-1}{\epsilon+1},$$
the quoted forms. Physics: the interior field is uniform and *reduced*,
$\vec E_{\rm in}=\frac2{\epsilon+1}E_0\hat y$ — the 2-D depolarization factor
is $\frac12$ (vs $\frac13$ for the sphere, P24: $\frac3{\epsilon+2}$); the
exterior disturbance is a 2-D (line-)dipole $\propto\sin\phi/\rho$ with moment
per unit length $\frac{\epsilon-1}{\epsilon+1}\frac{a^2E_0}2\cdot2$. Limits:
$\epsilon\to1$ kills the disturbance; $\epsilon\to\infty$ gives
$\Phi_{\rm in}\to0$, $B\to E_0a^2$ — the conducting cylinder. This transverse
polarizability is the engine of P37's rod force.

### P14.  Exercise 5.4.4 — Potential of a polarized body; bubble in a polarized slab  *(Wilcox 2e §5.13, p.247)*
(a) Starting from the potential of an elementary dipole
$d\Phi=d\vec p\cdot(\vec x-\vec x')/|\vec x-\vec x'|^3$, show that a smooth
polarization $\vec P(\vec x')$ produces
$$\Phi(\vec x)=\oint ds'\,\frac{\vec P\cdot\hat n'}{|\vec x-\vec x'|}
-\int d^3x'\,\frac{\vec\nabla'\cdot\vec P}{|\vec x-\vec x'|},$$
consistent with the densities (5.58)–(5.59).
(b) A spherical vacuum bubble of radius $a$ sits in a semi-infinite slab of
uniform polarization $\vec P=P_0\hat z$ (Fig. 5.25). Show the field induced by
$\vec P$ inside the bubble is
$$\vec E_P=\frac{4\pi}3P_0\hat z .$$
*Check:* surface quadrature of the bubble-wall charge $\sigma_b=-P_0\cos\theta$
gives a **uniform** interior field $(4\pi/3)P_0\hat z$ at random interior
points to $2\times10^{-4}$ (`test_p14_bubble_in_polarized_slab`).

**Solution.** (a) Superpose: $d\vec p=\vec P(\vec x')d^3x'$, so
$$\Phi=\int d^3x'\,\vec P(\vec x')\cdot\frac{\vec x-\vec x'}{|\vec x-\vec x'|^3}
=\int d^3x'\,\vec P\cdot\vec\nabla'\frac1{|\vec x-\vec x'|},$$
and $\vec P\cdot\vec\nabla'f=\vec\nabla'\cdot(f\vec P)-f\,\vec\nabla'\cdot\vec P$
with the divergence theorem gives the two stated terms: an effective surface
charge $\sigma=\vec P\cdot\hat n$ and volume charge $-\vec\nabla'\cdot\vec P$ —
precisely (5.59) and (5.58), now derived from the *potential* rather than the
force.
(b) Uniform $\vec P$ has $\vec\nabla\cdot\vec P=0$: only surfaces contribute.
The bubble wall carries $\sigma_b=\vec P\cdot\hat n'$ with $\hat n'=-\hat r$
(outward from the *material* means into the bubble):
$\sigma_b=-P_0\cos\theta$. A $\cos\theta$ surface charge on a sphere produces
a uniform interior field: the interior potential must be $\propto r\cos\theta=z$
(the only regular $\ell=1$ harmonic), and matching the standard boundary
conditions gives $\Phi_{\rm in}=-\frac{4\pi}3P_0z$, i.e.
$\vec E_P=+\frac{4\pi}3P_0\hat z$ — anti-parallel to the wall dipoles'
interior field... directed *along* $+\hat z$ because the negative bound charge
sits on top ($\sigma_b<0$ at $\theta=0$). The slab's remote outer face also
carries bound charge, but its (position-independent) sheet field is part of
the *macroscopic* field $\vec E$ in the Clausius–Mossotti bookkeeping of
P15(c); the exercise's $\vec E_P$ is the local **cavity** (Lorentz) term, and
that is exactly the $\frac{4\pi}3\vec P$ evaluated here. (The exact interior
integral is done by the code as a brute-force surface quadrature — it is
uniform to the quoted accuracy at every sampled interior point.)

### P15.  Exercise 5.4.5 — Cubical hole and the Clausius–Mossotti relation  *(Wilcox 2e §5.13, pp.247–249)*
A cubical vacuum hole sits in a material of uniform polarization
$\vec P=P_0\hat z$ (Fig. 5.26).
(a) Show the field induced by $\vec P$ at the hole's center is
$\vec E_P(0)=2P_0\int_{\rm top}\vec x'\,da'/r'^3$ (integral over the top face).
(b) By symmetry and solid angle, show $\vec E_P(0)=\frac{4\pi}3P_0\hat z$.
(c) With the local-field model $\vec P=N\alpha_{\rm mol}\vec E_T$,
$\vec E_T=\vec E+\vec E_P$, and (5.66) $\vec P=\chi\vec E$, derive
$$\alpha_{\rm mol}=\frac1N\,\frac{\chi}{1+\frac{4\pi}3\chi}
\qquad\text{(Clausius–Mossotti)}.$$
*Check:* face solid angle $=2\pi/3$ by quadrature; $E_P(0)=(4\pi/3)P_0$;
CM inverts consistently ($\chi\leftrightarrow\alpha$ round-trip)
(`test_p15_cubical_hole`).

**Solution.** (a) By P14(a) only the hole's walls contribute (uniform $\vec P$).
On the four side faces $\vec P\cdot\hat n'=0$; the top face ($z'=+L/2$,
material's outward normal $\hat n'=-\hat z$) carries $\sigma_b=-P_0$ and the
bottom $+P_0$. The field at the center is
$\vec E(0)=-\oint\sigma_b\,\hat x'\,da'/r'^3$ (pointing from the walls to the
origin); the two charged faces contribute equally by the symmetry
$\vec x'\to-\vec x'$, so
$$\vec E_P(0)=2P_0\int_{\rm top}\frac{\vec x'\,da'}{r'^3}.$$
(b) The transverse components integrate to zero on the square; the
$z$-component is
$2P_0\int_{\rm top}(z'/r'^3)da'=2P_0\,\Omega_{\rm face}$, where
$\Omega_{\rm face}=\int\cos\theta'\,da'/r'^2$ is the solid angle the face
subtends at the center. Six congruent faces tile the full sphere:
$\Omega_{\rm face}=4\pi/6=2\pi/3$. Hence
$\vec E_P(0)=2P_0\cdot\frac{2\pi}3\hat z=\frac{4\pi}3P_0\hat z$ — identical to
the spherical cavity of P14(b): the $\frac{4\pi}3$ Lorentz factor is shared by
any cavity with cubic-or-better symmetry.
(c) Each molecule polarizes in the *total* local field:
$\vec P=N\alpha\vec E_T=N\alpha(\vec E+\tfrac{4\pi}3\vec P)$. Insert
$\vec P=\chi\vec E$:
$$\chi=N\alpha\Big(1+\frac{4\pi}3\chi\Big)
\;\Longrightarrow\;
\alpha_{\rm mol}=\frac1N\frac{\chi}{1+\frac{4\pi}3\chi},$$
and with $\chi=(\epsilon-1)/4\pi$ (5.67) this is the familiar
$\alpha=\frac3{4\pi N}\frac{\epsilon-1}{\epsilon+2}$. The correction factor
$(1+\frac{4\pi}3\chi)^{-1}$ is exactly the cavity field of (a)–(b): dense media
polarize more easily than the naive $\chi=N\alpha$ because each atom feels its
neighbors' polarization.

### P16.  Exercise 5.6.1 — Dielectric corner by images  *(Wilcox 2e §5.13, p.249)*
Two perpendicular dielectric interfaces (the $x$–$z$ and $y$–$z$ planes) meet
at the origin; the dielectric ($\epsilon\neq1$) occupies the region outside
the first quadrant ($x<0$ or $y<0$, all $z$; Fig. 5.27), with the unit charge
in the vacuum quadrant at $(x',y',z')$, $x',y'>0$. Find the Green function in
Cartesian coordinates.
*Answer:* with $\beta=\dfrac{1-\epsilon}{1+\epsilon}$ (the single-interface
image coefficient of §5.6) and $R_{s_xs_y}=|\vec x-(s_xx',s_yy',z')|$, the
corner ansatz in the vacuum quadrant is
$$G=\frac1{R_{++}}+\frac{\beta}{R_{-+}}+\frac{\beta}{R_{+-}}
+\frac{\beta^2}{R_{--}},$$
with transmitted pieces $\tau(1/R_{++}+\beta/R_{+-})$ in $x<0,y>0$,
$\tau(1/R_{++}+\beta/R_{-+})$ in $x>0,y<0$, and $\tau^2/R_{++}$ in the third
quadrant, $\tau=2/(1+\epsilon)=1+\beta$. **Caveat (module finding):** this
construction satisfies *all* interface conditions exactly only if the third
quadrant has permittivity $\epsilon^2$ (factorizable medium
$\epsilon(x,y)=e(x)e(y)$). For the uniform-$\epsilon$ region of the figure it
is exact on both vacuum–dielectric interfaces and violates only the internal
$x=0,y<0$ / $y=0,x<0$ seam conditions at $O(\beta)$ — it is the
first-order-in-$\beta$ (single-reflection) solution, and one can show **no**
finite image set is exact for the uniform corner.
*Check:* factorized medium: seam continuity $<10^{-12}$, $D$-matching at FD
precision; uniform medium: continuity still exact, internal-seam $D$-residual
scales as $\beta^1$ (`test_p16_dielectric_corner`).

**Solution.** *Construction.* A single plane interface reflects with
coefficient $\beta$ and transmits with $\tau=1+\beta$ (Eqs. 5.106–5.107).
Compose the two perpendicular interfaces as for the conductor corner (§3.1):
each reflection multiplies by $\beta$, so the vacuum-side images at
$(-x',y')$, $(x',-y')$ carry $\beta$ and the doubly reflected $(-x',-y')$
carries $\beta^2$; crossing an interface multiplies by $\tau$.
*Verification.* On $x=0,y>0$: with $R_{++}=R_{-+}$ and $R_{+-}=R_{--}$ there,
$G_{Q1}|_0=(1+\beta)(1/R_{++}+\beta/R_{+-})=\tau(\dots)=G_{Q2}|_0$ —
continuous; the normal derivatives give
$(1-\beta)=\epsilon\tau\iff\beta=(1-\epsilon)/(1+\epsilon)$ — satisfied. The
same works on $y=0,x>0$, and on the internal seams *provided* the media ratio
across them is again $\epsilon$ — i.e. third quadrant $\epsilon^2$. For
uniform $\epsilon$ the internal-seam $D$ condition fails by
$-2\epsilon\tau\beta\,x'/R^3$-type terms: pure $O(\beta)$.
*No-go for the uniform corner:* the dielectric region is connected, so its
potential is one harmonic function whose only allowed image singularity is the
source point itself, $G_d=t/R_{++}$; matching term-by-term on the two
interfaces then forces $b+c=0,\;b-c=0$ from $x=0$ but $b=t-1\neq0$ from
$y=0$ — a contradiction unless $\epsilon=1$. Hence the exercise's expected
$\beta$-composition answer is exact only in the factorizable sense above, or
to first order in $\beta$ (weak dielectric) for the drawn geometry — the
2-D dielectric wedge is in fact a classic problem with no closed image
solution. Both readings are quoted in the answer; the code pins down each
statement numerically.

### P17.  Exercise 5.6.2 — Charge between a conductor and a dielectric slab  *(Wilcox 2e §5.13, pp.249–250)*
A semi-infinite dielectric ($\epsilon$, occupying $z>d$) faces a grounded
conducting plane at $z=0$; a unit charge sits between them at $0<z'<d$
(Fig. 5.28). With the Bessel expansions
$$\delta(\vec x-\vec x')=\sum_m\frac{e^{im(\phi-\phi')}}{2\pi}
\int_0^\infty dk\,k\,J_m(k\rho)J_m(k\rho')\,\delta(z-z'),\qquad
G_D=4\pi\sum_m\frac{e^{im(\phi-\phi')}}{2\pi}\int_0^\infty dk\,kJ_mJ_m'\,g(z,z'),$$
(the $m$ sums collapse via Ex. 4.2.1), show the reduced Green function is
$$g=\begin{cases}f(z_>)\sinh(kz_<),&z<d\\[2pt] K(z')\,e^{k(2d-z)},&z>d\end{cases}
\qquad
f(z_>)=\frac{e^{kz_>}}k\;
\frac{1+\frac{1+\epsilon}{1-\epsilon}e^{2k(d-z_>)}}{1+\frac{1+\epsilon}{1-\epsilon}e^{2kd}},\qquad
K(z')=\frac{\frac2{1-\epsilon}\frac{\sinh(kz')}k}{1+\frac{1+\epsilon}{1-\epsilon}e^{2kd}}.$$
*Check:* the closed form equals an independent 4-coefficient linear solve on a
$(k,z,z')$ grid to $10^{-10}$; $g(0)=0$; unit jump at $z'$; $g'(d^-)=\epsilon g'(d^+)$;
$\epsilon\to1$ reduces to the conductor-only $\sinh(kz_<)e^{-kz_>}/k$;
$\epsilon\to\infty$ makes $g(d)\to0$ (`test_p17_slab_over_conductor`).

**Solution.** Fourier-transforming in the transverse plane turns
$\nabla^2G_D=-4\pi\delta$ into the 1-D problem
$(k^2-\partial_z^2)g=\delta(z-z')$ per mode (§3.2 / Eq. 5.84). The piecewise
ansatz respecting the boundary conditions is
$$g=\begin{cases}A\sinh(kz),&0<z<z'\quad(\text{grounded wall})\\
Be^{kz}+Ce^{-kz},&z'<z<d\\ De^{-kz},&z>d\quad(\text{decay}),\end{cases}$$
with four conditions: continuity at $z'$; slope jump
$g'(z'^-)-g'(z'^+)=1$; continuity at $d$; and $D_n$ continuity
$g'(d^-)=\epsilon g'(d^+)$ (vacuum below, $\epsilon$ above). Eliminating
$A,B,C,D$ (the code does it by linear algebra; by hand one propagates the wall
solution $\sinh(kz)$ upward and the decaying solution downward, gluing at
$z'$) yields exactly the quoted $f(z_>)$, $K(z')$ — the $e^{k(2d-z)}$ writing
of the outer branch absorbs $e^{2kd}$ into the normalization so that
$c\equiv\frac{1+\epsilon}{1-\epsilon}$ appears symmetrically. Notes:
(i) $c<-1$ for $\epsilon>1$, so the denominator $1+ce^{2kd}$ never vanishes;
(ii) the structure is a two-mirror ladder: expanding
$[1+ce^{2kd}]^{-1}$ in powers of $c^{-1}e^{-2kd}$ regenerates the infinite
image series between the conductor ($-1$ reflections) and the dielectric
surface ($\beta$ reflections); (iii) both P40's force integral and P42's
$\epsilon\to\infty$ plate problem are direct corollaries of this $g$.

### P18.  Exercise 5.6.3 — Interchanging the vacuum and dielectric  *(Wilcox 2e §5.13, p.251)*
Find a substitution of parameters that converts P17's Green function into the
one for Fig. 5.29 — dielectric slab attached to the conductor ($0<z<d$),
vacuum beyond, the unit charge still between the plate and the $z=d$ surface
(now *inside* the dielectric).
*Answer:*
$$G_D^{\rm swapped}(\epsilon)=\frac1\epsilon\,G_D^{\rm P17}\!\Big(\epsilon\to\frac1\epsilon\Big),$$
same $(z,z')$ — replace $\epsilon\to1/\epsilon$ everywhere and divide by
$\epsilon$.
*Check:* direct 4-coefficient solve of the swapped geometry equals
$(1/\epsilon)\,g_{\rm P17}(1/\epsilon)$ to $10^{-10}$ across a $(k,z,z')$
grid; $\epsilon=1$ reduces to the conductor-only form
(`test_p18_swap_substitution`).

**Solution.** The swapped problem solves
$\vec\nabla\cdot[\epsilon_s(z)\vec\nabla G]=-4\pi\delta$ with
$\epsilon_s=\epsilon$ for $z<d$ and $1$ for $z>d$. Divide the whole equation
by the constant $\epsilon$:
$$\vec\nabla\cdot\Big[\frac{\epsilon_s(z)}{\epsilon}\vec\nabla G\Big]
=-\frac{4\pi}\epsilon\delta .$$
But $\epsilon_s/\epsilon$ equals $1$ below $d$ and $1/\epsilon$ above — the
*original* P17 medium pattern with dielectric constant $1/\epsilon$, and a
source of strength $1/\epsilon$. By linearity and uniqueness,
$G^{\rm swapped}(\epsilon)=\frac1\epsilon G^{\rm P17}(1/\epsilon)$. Only the
**ratio** of permittivities across an interface (and the value at the source)
matters. Sanity limits: $\epsilon\to\infty$ makes the swapped $G\to0$
(charge frozen inside a conductor-like slab); $\epsilon\to1$ recovers P17's
$\epsilon\to1$ conductor-only kernel; and the $\beta$ coefficient maps as
$\beta(1/\epsilon)=-\beta(\epsilon)$ — reflections off the interface flip
sign, as they must when approaching from the dense side.

### P19.  Exercise 5.6.4 — 1-D Green function with a dielectric slab  *(Wilcox 2e §5.13, p.251)*
Conducting walls at $x=0$ and $x=L$ (the 1-D setting of §2.9); a dielectric
slab of constant $\epsilon$ fills $0<x<d$ ($d<L$). For a charge in the vacuum
region ($d<x'<L$), solve $-d^2G_D/dx^2=\delta(x-x')$ (vacuum-region
normalization) with the dielectric interface conditions and check the
$\epsilon=1$, $d\to0$ limits against §2.9's $G_D=x_<(1-x_>/L)$ (2.136).
*Answer:* with $\Delta\equiv d+\epsilon(L-d)$,
$$G_D=\begin{cases}
\alpha\,x,&x<d\\[4pt]
\alpha\,[\,d+\epsilon(x-d)\,],&d<x<x'\\[4pt]
B\,(L-x),&x>x'
\end{cases}
\qquad
\alpha=\frac{L-x'}{\Delta},\qquad
B=\frac{d+\epsilon(x'-d)}{\Delta}.$$
*Check:* closed form vs a 4000-cell flux-form finite-difference solve of
$-(d/dx)[\epsilon(x)G']=\delta$ (relative $2\times10^{-3}$); exact reduction
to $x_<(1-x_>/L)$ at $\epsilon=1$ and as $d\to0$ (`test_p19_oneD_green`).

**Solution.** Piecewise-linear ansatz (1-D harmonic functions are lines):
$G=\alpha x$ for $x<d$ (wall at 0), $G=\gamma+\beta x$ for $d<x<x'$,
$G=B(L-x)$ for $x>x'$ (wall at $L$). Conditions:
(i) continuity at $d$; (ii) $D$ continuity at $d$: $\epsilon\,\alpha=\beta$
(the 1-D $D=-\epsilon\,dG/dx$); (iii) continuity at $x'$;
(iv) unit source in vacuum: $G'(x'^-)-G'(x'^+)=1$, i.e. $\beta+B=1$.
From (i)–(ii): $G=\alpha d+\epsilon\alpha(x-d)$ in the middle. From (iii):
$\alpha[d+\epsilon(x'-d)]=B(L-x')$. Substituting $B=1-\epsilon\alpha$ and
solving,
$$\alpha=\frac{L-x'}{d+\epsilon(L-d)},\qquad
B=\frac{d+\epsilon(x'-d)}{d+\epsilon(L-d)}.$$
*(The Answer block's second expression for $B$ simplifies to this; the code
uses these forms.)* Limits: $\epsilon=1$: $\alpha=(L-x')/L$, $B=x'/L$ —
exactly (2.136); $d\to0$: same. Interpretation: the slab acts like a series
capacitor — the "electrical thickness" of the dielectric layer is $d/\epsilon$
when referred to the vacuum side (rewrite
$\Delta/\epsilon=d/\epsilon+(L-d)$, the denominator of P43), so the charge's
image weight shifts exactly as the reduced distance dictates.

### P20.  Exercise 5.6.5 — Image solution for two dielectric half-spaces  *(Wilcox 2e §5.13, pp.251–252)*
Media $\epsilon_1$ ($z<0$) and $\epsilon_2$ ($z>0$) meet at the plane $z=0$;
a free point charge $q$ sits at $z'>0$ (Fig. 5.30). Find $\Phi$ everywhere by
images, confirming the book's quoted answer
$$\Phi_{z>0}=\frac1{\epsilon_2}\Big(\frac q{R_1}+\frac{q'}{R_2}\Big),\qquad
\Phi_{z<0}=\frac1{\epsilon_1}\frac{q''}{R_1},$$
$$q'=q\,\frac{\epsilon_2-\epsilon_1}{\epsilon_2+\epsilon_1},\qquad
q''=2q\,\frac{\epsilon_1}{\epsilon_2+\epsilon_1},$$
with $R_1=|\vec x-\vec x'|$, $R_2=|\vec x-\vec x''|$,
$\vec x''=(x',y',-z')$.
*Check:* continuity of $\Phi$ and of $\epsilon\partial_z\Phi$ across $z=0$ on
a grid; FD-harmonic off the charge; $\epsilon_1=\epsilon_2$ reduces to the
uniform-medium Coulomb form (`test_p20_two_halfspace_images`).

**Solution.** *Ansatz:* in the charge's region use the source (screened by
$\epsilon_2$) plus one image at the mirror point; in the far region a single
effective charge at the true source position:
$$\Phi_2=\frac1{\epsilon_2}\Big(\frac q{R_1}+\frac{q'}{R_2}\Big),\qquad
\Phi_1=\frac1{\epsilon_1}\frac{q''}{R_1}.$$
Both are harmonic in their half-spaces (images live outside), and
$\nabla\cdot(\epsilon\nabla\Phi)$ has exactly the $-4\pi q\delta$ source at
$\vec x'$. On $z=0$, $R_1=R_2\equiv R$, so:
*continuity:* $\frac1{\epsilon_2}(q+q')=\frac{q''}{\epsilon_1}$;
*normal $D$:* $\partial_z(1/R_1)|_0=+z'/R^3$ and
$\partial_z(1/R_2)|_0=-z'/R^3$, so
$D_z$ continuity ($\epsilon_2\partial_z\Phi_2=\epsilon_1\partial_z\Phi_1$)
gives $q-q'=q''$. Solving the pair,
$$q'=q\frac{\epsilon_2-\epsilon_1}{\epsilon_2+\epsilon_1},\qquad
q''=\frac{2q\epsilon_1}{\epsilon_1+\epsilon_2}\;
\Big(\Rightarrow \Phi_1=\frac{2q}{(\epsilon_1+\epsilon_2)R_1}\Big).$$
Limits: $\epsilon_1=\epsilon_2=\epsilon$: $q'=0$, $\Phi=q/(\epsilon R_1)$
everywhere ✓; $\epsilon_1\to\infty$: $q'=-q$ — the grounded conductor;
$\epsilon_2=1,\epsilon_1=\epsilon$: the book's (5.106)–(5.107). Sign physics:
for $\epsilon_1>\epsilon_2$ the image $q'$ is *negative* — the charge is
attracted toward the optically denser medium (bound charge of opposite sign
accumulates at the interface, cf. (5.111) and P36).

### P21.  Exercise 5.6.6 — Dielectric slab of finite thickness  *(Wilcox 2e §5.13, pp.252–253)*
A uniform slab (constant $\epsilon$, thickness $d$, infinite transversely)
occupies $-d<z<0$; a unit charge sits at $z'>0$ (Fig. 5.31). Assuming the
reduced form (5.82), give the functional forms of $g(z)$ in every region and
the conditions fixing the coefficients; argue the count closes (no need to
solve).
*Answer:* four regions,
$$g=\begin{cases}Ae^{-kz},&z>z'\\ Be^{kz}+Ce^{-kz},&0<z<z'\\
De^{kz}+Ee^{-kz},&-d<z<0\\ Fe^{kz},&z<-d,\end{cases}$$
six unknowns; six conditions: continuity and unit slope-jump at $z'$;
continuity and $D_n$ ($g'(0^+)=\epsilon g'(0^-)$) at $z=0$; continuity and
$\epsilon g'(-d^+)=g'(-d^-)$ at $z=-d$. A linear system with a nonvanishing
determinant → unique solution.
*Check:* the $6\times6$ solve satisfies all six conditions; $\epsilon\to1$
returns the free $e^{-k|z-z'|}/2k$; for $kd\gg1$ the $z>0$ branch matches the
half-space (5.104) (`test_p21_finite_slab`).

**Solution.** Each region is source-free (except the delta at $z'$), so
$g''=k^2g$ with solutions $e^{\pm kz}$; boundedness kills the growing
exponential in the two outer regions (leaving $A$ and $F$), while both
exponentials survive in the bounded regions ($B,C$ and $D,E$): six constants.
The matching conditions are the standard four interface equations
(continuity + $D_n$ at $z=0$ and $z=-d$) plus the two source conditions at
$z'$ (continuity + jump $g'(z'^-)-g'(z'^+)=1$). Six linear equations, six
unknowns; solvability: the associated homogeneous problem (no source) admits
only $g\equiv0$ (a nontrivial bounded solution would violate uniqueness of
the Dirichlet problem at infinity), so the determinant is nonzero and the
inhomogeneous system has exactly one solution — "enough information."
Physically the solved kernel (code) shows the two-interface ladder: the charge
sees an image train with alternating reflection coefficients
$\beta$ at $z=0$ and $-\beta$-weighted internal reflections between $0$ and
$-d$, summing to a geometric series in $\beta^2e^{-2kd}$; at $kd\gg1$ single
reflection dominates → half-space; at $\epsilon\to1$, $\beta\to0$ → free
space.
### P22.  Exercise 5.7.1 — 2-D Green function of a dielectric cylinder  *(Wilcox 2e §5.13, p.253)*
Using the reduced-Green-function technique with a line-charge source (as in
Ex. 4.8.3), find $G$ for an infinite dielectric cylinder (constant $\epsilon$,
radius $a$), unit-density line charge outside at $\rho'>a$ (the book's
Fig. 5.32 — its caption says "Exercise 5.9.10", an erratum: it belongs here).
Verify the book's hinted answer
$$G=4\sum_{m=0}^{\infty}\cos[m(\phi-\phi')]\,g_m(\rho,\rho'),\qquad
g_0=-\tfrac12\ln(\rho_>/K),$$
$$g_{m\ge1}=\begin{cases}
\dfrac1{m(1+\epsilon)}\Big(\dfrac{\rho}{\rho'}\Big)^m,&\rho<a\\[8pt]
\dfrac1{2m}\Big(\dfrac{\rho_<}{\rho_>}\Big)^m
\Big[1+\dfrac{1-\epsilon}{1+\epsilon}\Big(\dfrac a{\rho_<}\Big)^{2m}\Big],&\rho>a .
\end{cases}$$
*Check:* each $g_m$ satisfies the radial ODE (FD), both $\rho=a$ interface
conditions, and the source jump $\rho'[g'(-)-g'(+)]=1$
($\tfrac12$ for $m{=}0$); the $\epsilon=1$ sum reproduces $-2\ln|\vec x_\perp-\vec x'_\perp|$
to $10^{-6}$; the $\epsilon\neq1$ sum is continuous across $\rho=a$
(`test_p22_cylinder_2d_green`).

**Solution.** In 2-D the Green equation is
$\vec\nabla\cdot(\epsilon\vec\nabla G)=-4\pi\delta^2$, free solution
$-2\ln(\rho/K)$ (Eq. 3.11; $K$ is the line-charge length scale — physics is
$K$-independent). Expand $G$ and
$\delta(\phi-\phi')=\frac1{2\pi}[1+2\sum_m\cos m(\phi-\phi')]$ in azimuthal
modes; with the book's prefactor $4$, the mode problems are
$$\frac1\rho\big(\rho\,\epsilon(\rho)\,g_0'\big)'=-\frac{\delta(\rho-\rho')}{2\rho},
\qquad
\big(\rho g_m'\big)'-\frac{m^2}{\rho}g_m=-\frac{\delta(\rho-\rho')}{1}\cdot\frac1\rho\cdot\rho\Big|_{\rm jump\ } \rho'[g_m'(-)-g_m'(+)]=1 .$$
*$m=0$:* inside the dielectric $g_0=$ const (regular); $D$ continuity forces
the middle region's log coefficient to vanish too, so $g_0$ is constant out to
$\rho'$ and $-\tfrac12\ln(\rho/K)$ beyond — i.e. $g_0=-\tfrac12\ln(\rho_>/K)$,
**independent of $\epsilon$**: a neutral dielectric leaves no monopole image
(total bound charge zero, P12).
*$m\ge1$:* $g_m=A\rho^m$ ($\rho<a$), $B\rho^m+C\rho^{-m}$ ($a<\rho<\rho'$),
$D\rho^{-m}$ ($\rho>\rho'$). Interface at $a$: continuity
$Aa^m=Ba^m+Ca^{-m}$ and $D_\rho$: $\epsilon mAa^{m-1}=mBa^{m-1}-mCa^{-m-1}$
give $C=\beta a^{2m}B$, $A=(1+\beta)B$ with
$\beta=(1-\epsilon)/(1+\epsilon)$; the jump at $\rho'$ fixes
$B=\rho'^{-m}/2m$, $D=B[\rho'^{2m}+\beta a^{2m}]$. Assembling gives exactly
the quoted branches: outside, the induced part is the source's $m$-th image
weight $\beta(a^2/\rho\rho')^m$ — the dielectric analog of the
line-charge-in-cylinder image of §3.3, with strength $\beta$ instead of $-1$;
inside, the transmitted mode $(1+\beta)/2m=(1/m(1+\epsilon))$.
At $\epsilon=1$ the sum telescopes to
$-2\ln\rho_>+2\sum_m\frac1m(\rho_</\rho_>)^m\cos m\Delta\phi
=-2\ln|\vec x_\perp-\vec x'_\perp|$ ✓. (P44 sums the coincidence limit into
the force on the line charge.)

### P23.  Exercise 5.7.2 — Point charge outside a dielectric cylinder  *(Wilcox 2e §5.13, pp.253–254)*
Same cylinder, now a **point** charge outside (Fig. 5.33). Assume the reduced
form (as Ex. 4.7.4)
$$G=\frac2\pi\sum_{m=-\infty}^{\infty}e^{im(\phi-\phi')}
\int_0^\infty dk\,\cos[k(z-z')]\,g_m(\rho,\rho'),\qquad
4\pi\delta=\frac2\pi\sum_me^{im\Delta\phi}\int_0^\infty dk\cos k\Delta z\,
\frac{\delta(\rho-\rho')}\rho .$$
Motivate the solutions in the three radial regions in terms of modified
Bessel functions, and exhibit the conditions that determine the coefficients
(no need to solve).
*Answer:* regular/decaying combinations of $I_m(k\rho)$, $K_m(k\rho)$:
$$g_m=\begin{cases}A\,I_m(k\rho),&\rho<a\\
B\,I_m(k\rho)+C\,K_m(k\rho),&a<\rho<\rho'\\ D\,K_m(k\rho),&\rho>\rho',\end{cases}$$
with (i) continuity at $a$; (ii) $\epsilon\,g_m'(a^-)=g_m'(a^+)$;
(iii) continuity at $\rho'$; (iv) jump $g_m'(\rho'^-)-g_m'(\rho'^+)=1/\rho'$
— four linear conditions for $A,B,C,D$, uniquely solvable (nonzero Wronskian
determinant).
*Check:* the $4\times4$ solve satisfies all four conditions by FD; at
$\epsilon=1$ the assembled double sum reproduces $1/|\vec x-\vec x'|$ to
$2\times10^{-3}$; for $\epsilon\neq1$ the assembled $G$ is continuous across
$\rho=a$ (`test_p23_cylinder_3d_reduced`).

**Solution.** Insert the expansions into
$\vec\nabla\cdot(\epsilon\vec\nabla G)=-4\pi\delta$: each $(m,k)$ mode obeys
the modified Bessel equation
$$g_m''+\frac{g_m'}\rho-\Big(k^2+\frac{m^2}{\rho^2}\Big)g_m
=-\frac{\delta(\rho-\rho')}{\rho},$$
whose homogeneous solutions are $I_m(k\rho)$ (regular at 0, grows) and
$K_m(k\rho)$ (decays, singular at 0) — "Bessel functions of imaginary
argument". Regularity on the axis keeps only $I_m$ inside the dielectric;
decay at $\rho\to\infty$ keeps only $K_m$ outside the source; both survive in
the annulus: four constants. The four conditions above are two interface
conditions at the dielectric surface (tangential $E$ ↔ continuity of $g$;
normal $D$ ↔ the $\epsilon$-weighted slope) and the two source conditions
(the jump normalization follows by integrating the mode equation across
$\rho'$). Uniqueness: the homogeneous system would need a bounded solution of
the modified Bessel problem vanishing in all three regions' boundary senses;
none exists (the Wronskian $I_mK_m'-I_m'K_m=-1/x$ never vanishes), so the
$4\times4$ determinant is nonzero: the coefficients are determined — "enough
information," as the exercise asks. The code's $\epsilon=1$ cross-check
$G\to1/|\vec x-\vec x'|$ validates the normalization ($g_m^{\rm free}
=I_m(k\rho_<)K_m(k\rho_>)$ by the Wronskian, exactly the classic identity).

### P24.  Exercise 5.7.3 — Dielectric sphere in a uniform field, via the Green function  *(Wilcox 2e §5.13, p.254)*
From the Green function of a unit charge near a dielectric sphere, generate
the uniform-field solution by the distant-charge trick of §3.3 (Fig. 5.34),
confirming
$$\Phi_{\rm out}=-E_0z+\frac{\vec p\cdot\vec x}{r^3},\quad
\vec p=\frac{\epsilon-1}{\epsilon+2}a^3E_0\hat z;\qquad
\Phi_{\rm in}=-\frac{3E_0z}{\epsilon+2}.$$
*Check:* interface conditions at $r=a$; the exact series with a source at
$R=300a$, $q=E_0R^2$ matches the closed forms to $2\%$ (the $O(a/R)$ residual);
the $\ell=1$ induced coefficient equals $(\epsilon-1)a^3E_0/(\epsilon+2)$
(`test_p24_sphere_uniform_field`).

**Solution.** Put $q=E_0R^2$ at $z=-R$ ($R\to\infty$): near the origin its
field is $E_0\hat z$ with corrections $O(r/R)$, and its potential is
$q/R+E_0z+\dots$ — after dropping the constant, the applied $-E_0z$ (sign per
the geometry: the code handles the bookkeeping; here quote the standard
orientation). In the exterior Green function (5.141) each induced term scales
as $q\,a^{2\ell+1}/(rR)^{\ell+1}=E_0R^{1-\ell}(\cdots)$: only $\ell=1$
survives $R\to\infty$,
$$q\cdot\frac{(\epsilon-1)\cdot1}{1\cdot(1+\epsilon)+1}\,
\frac{a^3}{r^2R^2}P_1(\cos\gamma)\longrightarrow
\frac{\epsilon-1}{\epsilon+2}\,a^3E_0\,\frac{\cos\theta}{r^2}
=\frac{\vec p\cdot\vec x}{r^3},$$
the field of the induced dipole $\vec p=\frac{\epsilon-1}{\epsilon+2}a^3E_0\hat z$
(Eq. 5.144). Likewise the interior kernel (5.140) keeps only
$\ell=0$ (constant, dropped) and $\ell=1$:
$q\cdot\frac{3}{\epsilon+2}\frac{r}{R^2}P_1\to\frac3{\epsilon+2}E_0r\cos\theta$
with the sign arranging to $\Phi_{\rm in}=-\frac{3}{\epsilon+2}E_0z$ — a
uniform interior field $\vec E_{\rm in}=\frac3{\epsilon+2}E_0\hat z$ (5.146),
reduced by the spherical depolarization factor $\frac13$:
$E_{\rm in}=E_0/[1+\frac{\epsilon-1}3]$. Boundary sanity:
$\Phi$ continuous at $r=a$ ($-E_0a+p/a^2$ vs $-3E_0a/(\epsilon+2)$ — equal by
the $p$ value) and $\epsilon\partial_r\Phi_{\rm in}=\partial_r\Phi_{\rm out}$
✓ (code). This is the sphere twin of P13's cylinder ($\frac2{\epsilon+1}$ vs
$\frac3{\epsilon+2}$).

### P25.  Exercise 5.7.4 — Green function with the source inside the sphere  *(Wilcox 2e §5.13, p.255)*
Find $G$ for the dielectric sphere when the unit source is **inside**
($r'<a$). For $r\gg a$ identify the effective dipole moment and evaluate the
total polarization charge on the surface, comparing with P12(b). [The book's
hint: get part of the answer from the symmetry $G(\vec x,\vec x')=G(\vec x',\vec x)$
and the $r'>a$ solution of §5.7.]
*Answer:* for $r>a$ (by symmetry with (5.140)):
$G=\sum_\ell\frac{2\ell+1}{\ell(1+\epsilon)+1}\frac{r'^\ell}{r^{\ell+1}}P_\ell(\cos\gamma)$;
for $r,r'<a$:
$$G=\frac1\epsilon\frac1{|\vec x-\vec x'|}
+\sum_\ell\frac{(\ell+1)(\epsilon-1)}{\epsilon\,[\ell(1+\epsilon)+1]}
\frac{(rr')^\ell}{a^{2\ell+1}}P_\ell(\cos\gamma).$$
Far field: monopole $1/r$ (the full free charge) and
$\vec p_{\rm eff}=\dfrac{3\,\vec x'}{\epsilon+2}$;
total surface polarization charge $\displaystyle\oint\sigma_b\,da
=\frac{\epsilon-1}\epsilon$ — exactly P12(b) with $Q_{\rm free}=1$.
*Check:* closed coefficients equal an independent $4\times4$ solve for every
$\ell$; far-field monopole $=1$ and dipole $=3r'/(\epsilon+2)$ from the series;
$\oint\sigma_b$ by quadrature $=(\epsilon-1)/\epsilon$ independent of $r'$
(`test_p25_source_inside_sphere`).

**Solution.** Radial ansatz per $\ell$ (source in the dielectric):
$g_\ell=Ar^\ell$ ($r<r'$), $Br^\ell+Cr^{-\ell-1}$ ($r'<r<a$),
$Dr^{-\ell-1}$ ($r>a$). Source conditions at $r'$ (in medium $\epsilon$):
continuity and $\epsilon r'^2[g'(-)-g'(+)]=1\cdot r'^0\Rightarrow
g'(-)-g'(+)=1/(\epsilon r'^2)$, giving directly
$C=r'^\ell/[\epsilon(2\ell+1)]$ — the Coulomb-in-medium direct part.
Interface at $a$: continuity and $\epsilon g'(a^-)=g'(a^+)$ give
$$B=\frac{(\ell+1)(\epsilon-1)}{\ell(1+\epsilon)+1}\,\frac{C}{a^{2\ell+1}},\qquad
D=Ba^{2\ell+1}+C=\frac{r'^\ell}{\ell(1+\epsilon)+1},$$
and $A=B+C\,r'^{-2\ell-1}$. The $D$ coefficient is exactly the
$(r\leftrightarrow r')$ transpose of (5.140) — the hinted symmetry;
$B$ is the interior "reaction" kernel (the engine of P48's force).
*Far field:* $\ell=0$: $D_0=1$ → $\Phi\to1/r$: at large $r$ the full unit
charge is visible (the interior screening cloud $\rho_b=(1-\epsilon)/\epsilon$
at the charge is exactly cancelled by the surface bound charge, P12).
$\ell=1$: $(2\cdot1+1)g_1=3r'/[(\epsilon+2)]\cdot r^{-2}P_1$ →
$\vec p_{\rm eff}=3\vec x'/(\epsilon+2)$: the *displacement* of the charge off
center is what the outside world sees, screened by the same $3/(\epsilon+2)$
as P24 (reciprocity: source inside ↔ observer inside).
*Total surface charge:* $\sigma_b=\frac1{4\pi}[E_r(a^+)-E_r(a^-)]$; only
$\ell=0$ survives the angular integral:
$E_r(a^+)=1/a^2$, $E_r(a^-)=1/(\epsilon a^2)$, so
$\oint\sigma_b\,da=1-\frac1\epsilon=\frac{\epsilon-1}\epsilon$ ✓ — P12(b) from
the explicit solution, independent of where the charge sits inside.

### P26.  Exercise 5.7.5 — Vacuum bubble in a dielectric medium  *(Wilcox 2e §5.13, p.255)*
Find the Green function for a spherical vacuum bubble (radius $a$) embedded
in a medium of constant $\epsilon$, with the free unit charge outside the
bubble (in the dielectric). [Hint: compare boundary conditions with the
dielectric-sphere case — no need to start over.]
*Answer:* the interface conditions swap sides, which is the substitution
$\epsilon\to1/\epsilon$ (plus the in-medium source normalization $1/\epsilon$):
$$G_{\rm bubble}(\epsilon)=\frac1\epsilon\,G_{\rm sphere}\big(\epsilon\to1/\epsilon\big)
=\frac1\epsilon\Big[\frac1{|\vec x-\vec x'|}
+\sum_{\ell\ge1}\frac{(\epsilon-1)\ell}{\ell(1+\epsilon)+\epsilon}\,
\frac{a^{2\ell+1}}{(rr')^{\ell+1}}P_\ell(\cos\gamma)\Big]\quad(r,r'>a),$$
with interior ($r<a$) modes
$(2\ell+1)r^\ell/\{[\ell(1+\epsilon)+\epsilon]r'^{\ell+1}\}$.
Note the induced series has the **opposite sign** to the sphere's (5.141) and
denominators $\ell(1+\epsilon)+\epsilon$ instead of $\ell(1+\epsilon)+1$.
*Check:* the substitution formula equals a direct radial solve mode-by-mode
($10^{-9}$) and mode-sum vs closed-sum agreement at $10^{-8}$
(`test_p26_bubble_green`).

**Solution.** The bubble problem solves
$\vec\nabla\cdot[\epsilon_b(r)\vec\nabla G]=-4\pi\delta$ with
$\epsilon_b=1$ ($r<a$), $\epsilon$ ($r>a$). Divide by $\epsilon$ (P18's
trick): the medium pattern becomes $1/\epsilon$ inside, $1$ outside — a
"dielectric sphere" of constant $1/\epsilon$ in vacuum with source strength
$1/\epsilon$. Uniqueness gives the substitution rule. Explicitly, with
$\epsilon'=1/\epsilon$ in (5.141):
$(\epsilon'-1)\ell/[\ell(1+\epsilon')+1]
=(1-\epsilon)\ell/[\ell(1+\epsilon)+\epsilon]$, whose sign flip converts the
sphere's attractive image series into the bubble's repulsive one (P46): a
cavity in a dielectric behaves like a region of *deficit* polarizability —
an "anti-sphere" with effective $\ell=1$ polarizability
$-\frac{\epsilon-1}{1+2\epsilon}a^3$ (per unit medium-screened source). The
$\ell$-dependence of the denominators means there is again no single image
point (only $\epsilon\to\infty$ collapses the sphere series to one; the
bubble has no conducting limit).

### P27.  Exercise 5.7.6 — Point dipole near a dielectric sphere  *(Wilcox 2e §5.13, pp.255–256)*
A point dipole $\vec p_0$ (arbitrary direction) sits at $\vec x'$ outside a
dielectric sphere of radius $a$ (Fig. 5.35). Find the leading potential
(a) far from everything ($r\gg r',a$), and (b) inside the sphere
($r<a$, with $r'\gg a$).
*Answer:* (a) $\Phi\simeq\vec p_{\rm eff}\cdot\vec x/r^3$ with
$$\vec p_{\rm eff}=\vec p_0+\frac{\epsilon-1}{\epsilon+2}a^3\,\vec E_{\rm dip}(0),
\qquad
\vec E_{\rm dip}(0)=\frac{3(\vec p_0\cdot\hat n')\hat n'-\vec p_0}{r'^3},\quad
\hat n'=\frac{\vec x'}{r'}$$
(the dipole plus the dipole its field induces in the sphere).
(b) a uniform screened field:
$\vec E_{\rm in}=\dfrac{3}{\epsilon+2}\,\vec E_{\rm dip}(0)$, i.e.
$\Phi_{\rm in}={\rm const}-\frac{3}{\epsilon+2}\vec x\cdot\vec E_{\rm dip}(0)$.
*Check:* two-charge dipole + exact series: far-field dipole components match
$\vec p_{\rm eff}$ to $3\%$ ($O(r'/r)$); interior FD field matches (b) with
error $\propto1/r'$ shrinking between $r'=20a$ and $40a$
(`test_p27_dipole_near_sphere`).

**Solution.** Write the dipole as the limit of charges $\pm q$ at
$\vec x'\pm\vec\delta/2$ and superpose the one-charge Green function.
(a) Far away, each source charge contributes its own effective system: the
bare charge (monopoles cancel between $\pm q$, leaving $\vec p_0$) and its
sphere-induced $\ell=1$ image. The induced dipole responds linearly to the
field at the sphere's center, so in the limit
$\vec p_{\rm ind}=\alpha\vec E_{\rm dip}(0)$ with
$\alpha=\frac{\epsilon-1}{\epsilon+2}a^3$ (5.143–5.144). The two dipoles do
not sit at the same point ($\vec p_0$ at $\vec x'$, $\vec p_{\rm ind}$ at the
origin), but the displacement only affects the $\ell=2$ (quadrupole) term:
to leading order $\Phi\simeq(\vec p_0+\vec p_{\rm ind})\cdot\vec x/r^3$.
(b) For $r'\gg a$ the dipole's field is uniform across the sphere,
$\vec E_{\rm dip}(0)+O(a/r')$, so P24's screening applies verbatim:
$\vec E_{\rm in}=\frac3{\epsilon+2}\vec E_{\rm dip}(0)$. From the kernel: the
$\ell=0$ term of (5.140) contributes only a constant
($p_0$-projected $-\vec p_0\cdot\hat n'/r'^2$), and the $\ell=1$ term
differentiates to exactly the uniform interior gradient — the code confirms
by finite-differencing the series. Everything here is the polarizability
algebra reused in P49's force.

### P28.  Exercise 5.7.7 — Dielectric sphere inside a grounded shell  *(Wilcox 2e §5.13, pp.255–256)*
A solid dielectric sphere (radius $a$, constant $\epsilon$) sits concentric
inside a hollow grounded conductor of inner radius $b$; the unit charge is in
the gap, $a<r'<b$. Assuming the (5.116) form, give the $g_\ell(r)$ in each
region and the boundary conditions determining the coefficients (no need to
solve).
*Answer:*
$$g_\ell=\begin{cases}A_\ell r^\ell,&r<a\\
B_\ell r^\ell+C_\ell r^{-\ell-1},&a<r<r'\\
D_\ell r^\ell+E_\ell r^{-\ell-1},&r'<r<b,\end{cases}$$
five unknowns; five conditions: continuity and
$\epsilon g_\ell'(a^-)=g_\ell'(a^+)$ at $a$; continuity and jump
$g_\ell'(r'^-)-g_\ell'(r'^+)=1/r'^2$ at $r'$; and the Dirichlet wall
$g_\ell(b)=0$.
*Check:* the $5\times5$ solve satisfies all five (FD); at $\epsilon=1$ it
equals the grounded-shell interior kernel
$\frac1{2\ell+1}\big[\frac{r_<^\ell}{r_>^{\ell+1}}-\frac{(rr')^\ell}{b^{2\ell+1}}\big]$
(the $b\to$ finite analog of (4.240)) to $10^{-10}$
(`test_p28_sphere_in_conducting_shell`).

**Solution.** Regularity at the origin keeps only $r^\ell$ in the dielectric;
between $a$ and $b$ both radial solutions appear, split at the source radius
into two two-parameter branches. Counting: $1+2+2=5$ constants. The five
stated conditions are all of them: the two dielectric-interface conditions
(tangential $E$, normal $D$), the two source conditions (the jump follows by
integrating $-(r^2g')'+\ell(\ell+1)g=\delta(r-r')$ across $r'$), and the
grounded conductor $g_\ell(b)=0$ ($\Phi=0$ on the wall for every mode). The
homogeneous problem has no nontrivial solution — a source-free potential
regular at 0, matching at $a$, vanishing at $b$ must vanish identically
(uniqueness inside a grounded shell) — so the determinant is nonzero and the
system pins all five coefficients: "enough information." The
$\epsilon=1$ limit collapses $A=B$, $C=0$ and reproduces the image-in-sphere
kernel; $\epsilon\to\infty$ freezes the core ($g(a)\to0$), giving the
conductor-in-conductor annulus kernel.

### P29.  Exercise 5.7.8 — Dielectric sphere facing a uniformly charged plane  *(Wilcox 2e §5.13, p.256)*
Use $\Phi=\int G\rho$ with the interior Green function to find the potential
inside a dielectric sphere (radius $a$) in the field of an infinite plane of
uniform surface charge $\sigma$ at $z=d>a$ (Fig. 5.36); compare the interior
field with P24.
*Answer:* every $\ell\ge2$ plane integral vanishes **exactly** (parity +
orthogonality), $\ell=0$ is an (infinite) constant, and $\ell=1$ gives
$$\Phi_{\rm in}={\rm const}+\frac{3}{\epsilon+2}\,2\pi\sigma\,z
\qquad\Longrightarrow\qquad
\vec E_{\rm in}=-\frac{3}{\epsilon+2}\,2\pi\sigma\,\hat z
=\frac{3}{\epsilon+2}\vec E_{\rm plane},$$
exactly P24's screened uniform field with $E_0=2\pi\sigma$ — exact, not just
far-field, because an infinite uniform plane makes a truly uniform field.
*Check:* the plane moment integrals: $\ell=1\to2\pi$, $\ell=2\ldots5\to0$
(quadrature, cutoff-tail small); interior field matches
$-\frac3{\epsilon+2}2\pi\sigma$ (`test_p29_sphere_and_charged_plane`).

**Solution.** With $\rho=\sigma\,\delta(z'-d)$ and the interior kernel
(5.140),
$$\Phi_{\rm in}(\vec x)=\sigma\sum_\ell\frac{2\ell+1}{\ell(1+\epsilon)+1}\,
r^\ell P_\ell(\cos\theta)\;I_\ell,\qquad
I_\ell\equiv\int_{\rm plane}\frac{P_\ell(\cos\theta')}{r'^{\ell+1}}\,da' ,$$
(azimuthal symmetry kills $m\neq0$). Parametrize the plane by
$r'\in[d,\infty)$ with $\cos\theta'=d/r'$, $da'=2\pi r'dr'$:
$$I_\ell=2\pi\int_d^\infty\frac{P_\ell(d/r')}{r'^\ell}\,dr'
=2\pi d^{\,1-\ell}\int_0^1P_\ell(t)\,t^{\ell-2}\,dt .$$
For $\ell\ge2$, $P_\ell(t)t^{\ell-2}$ has even parity, so
$\int_0^1=\frac12\int_{-1}^1P_\ell(t)\,t^{\ell-2}\,dt=0$ by Legendre
orthogonality ($t^{\ell-2}$ has degree $<\ell$): **every higher multipole of
an infinite uniform plane vanishes**. $\ell=1$: $\int_0^1P_1t^{-1}dt=1$, so
$I_1=2\pi$; $\ell=0$ diverges — the familiar infinite constant of an infinite
plane's potential (gauge; drop it). Hence
$\Phi_{\rm in}=\text{const}+\frac{3}{\epsilon+2}2\pi\sigma\,r\cos\theta$ and
the interior field is uniform: magnitude $\frac3{\epsilon+2}\times2\pi\sigma$,
directed away from the plane (for $\sigma>0$) — the plane's field
$|E|=2\pi\sigma$ screened by P24's factor. The Green-function route thus
*derives* rather than assumes the equivalence to the uniform-field problem.

### P30.  Exercise 5.7.9 — Dielectric sphere inside a charged ring  *(Wilcox 2e §5.13, pp.256–257)*
A ring of radius $b$ and total charge $Q$, uniformly distributed, lies in the
equatorial plane concentric with a dielectric sphere of radius $a<b$
(permittivity $\varepsilon$). Show the interior potential is
$$\Phi(r,\theta)=Q\sum_{n=0}^{\infty}
\frac{(-1)^n(4n+1)}{2n(1+\varepsilon)+1}\,
\frac{(2n-1)!!}{(2n)!!}\,\frac{r^{2n}}{b^{2n+1}}\,P_{2n}(\cos\theta)$$
(Ex. 4.9.1's $P_\ell(0)$ values are the input).
*Check:* the series equals the ring rebuilt from 400 point charges, each with
the one-charge interior kernel, to $10^{-6}$ at several $(r,\theta)$
(`test_p30_ring_around_sphere`).

**Solution.** Superpose the interior kernel (5.140) over the ring. For a
source at $(b,\theta'=\pi/2,\phi')$ the addition theorem reduces the
azimuthal average of $P_\ell(\cos\gamma)$ to
$P_\ell(\cos\theta)P_\ell(\cos\theta')=P_\ell(\cos\theta)P_\ell(0)$
($m\neq0$ terms integrate away around the uniform ring). Hence
$$\Phi_{\rm in}=Q\sum_\ell\frac{2\ell+1}{\ell(1+\varepsilon)+1}\,
\frac{r^\ell}{b^{\ell+1}}P_\ell(0)\,P_\ell(\cos\theta).$$
Ex. 4.9.1(b): $P_\ell(0)=0$ for odd $\ell$ and
$P_{2n}(0)=(-1)^n\frac{(2n-1)!!}{(2n)!!}$; keeping $\ell=2n$,
$2\ell+1\to4n+1$ and $\ell(1+\varepsilon)+1\to2n(1+\varepsilon)+1$ gives the
quoted series verbatim. Structure worth noting: at $n=0$ the term is $Q/b$ —
the ring's constant potential leaks in unscreened (constants feel no
dielectric); the first nontrivial term is $n=1$ with the
$\frac5{2(1+\varepsilon)\cdot?}$-type screened $P_2$ — the sphere reduces
each even harmonic by $\frac{4n+1}{2n(1+\varepsilon)+1}$ relative to vacuum's
$1$, the $\ell$-dependent generalization of $3/(\epsilon+2)$.

### P31.  Exercise 5.7.10 — Split-sphere capacitances with a dielectric filling  *(Wilcox 2e §5.13, p.257)*
Fill the interior of Ex. 4.13.4's split conducting sphere (radius $a$, two
hemispherical shells) with a uniform dielectric $\varepsilon$. Show
$$C_{11}(\varepsilon)=C_{11}+\frac{a(\varepsilon-1)}4
\sum_{\ell\ge1}\ell(2\ell+1)\Big[\int_0^1P_\ell(x)dx\Big]^2,\qquad
C_{12}(\varepsilon)=C_{12}+\frac{a(\varepsilon-1)}4
\sum_{\ell\ge1}(-1)^\ell\,\ell(2\ell+1)\Big[\int_0^1P_\ell(x)dx\Big]^2,$$
where $C_{11},C_{12}$ are Ex. 4.13.4's vacuum values
$\frac a4\sum(2\ell+1)^2I_\ell^2$ and $\frac a4\sum(-1)^\ell(2\ell+1)^2I_\ell^2$,
$I_\ell=\int_0^1P_\ell$.
*Check:* the sums equal direct quadrature of the free charge on the upper
hemisphere for $(V_1,V_2)=(1,0)$ and $(0,1)$ at $\varepsilon=1,2,4.5$; at
$\varepsilon=1$ they collapse to the $(2\ell+1)^2$ forms; the shift formula
matches term by term (`test_p31_split_sphere_dielectric`).

**Solution.** Let the shells carry potentials $V_1$ (upper), $V_2$ (lower);
the surface value is the step function $V(\theta)$ with Legendre projection
$$V_\ell=\tfrac{2\ell+1}2\big(V_1+(-1)^\ell V_2\big)I_\ell\ (\ell\ge1),\qquad
V_0=\tfrac{V_1+V_2}2,$$
using $\int_{-1}^0P_\ell=(-1)^\ell I_\ell$. The potential is
$\sum V_\ell(r/a)^\ell P_\ell$ inside (dielectric) and
$\sum V_\ell(a/r)^{\ell+1}P_\ell$ outside — continuity at $r=a$ is built in
(the shell fixes $\Phi$ there). The **free** charge on the shell is the
$D$-jump:
$$4\pi\sigma_f=D_r(a^+)-D_r(a^-)
=\sum_\ell\frac{V_\ell}{a}\big[(\ell+1)+\varepsilon\,\ell\big]P_\ell(\cos\theta):$$
the exterior contributes $(\ell+1)$, the dielectric interior $\varepsilon\ell$.
Integrate over the upper hemisphere
($\int_{\rm up}P_\ell\,da=2\pi a^2I_\ell$):
$$Q_1=\frac a2\sum_\ell V_\ell\big[(\ell+1)+\varepsilon\ell\big]I_\ell
=\frac a4(V_1+V_2)+\frac a4\sum_{\ell\ge1}(2\ell+1)
\big[(\ell+1)+\varepsilon\ell\big]I_\ell^2\big(V_1+(-1)^\ell V_2\big).$$
Then $C_{11}=\partial Q_1/\partial V_1$ and $C_{12}=\partial Q_1/\partial V_2$
give
$$C_{1j}(\varepsilon)=\frac a4\Big[1+\sum_{\ell\ge1}(\pm1)^\ell(2\ell+1)
\big[(\ell+1)+\varepsilon\ell\big]I_\ell^2\Big],$$
($+$ for $j{=}1$, $(-1)^\ell$ for $j{=}2$). Since
$(\ell+1)+\varepsilon\ell=(2\ell+1)+(\varepsilon-1)\ell$, this is the vacuum
$(2\ell+1)^2$ sum plus the stated $(\varepsilon-1)\ell(2\ell+1)I_\ell^2$
shift. Only odd $\ell$ contribute ($I_{2n}=0$ for $n\ge1$), so the $C_{12}$
shift is negative: the dielectric *strengthens* the inductive coupling. The
symmetric-system capacitance $C=\frac12(C_{11}-C_{12})$ then grows by
$\frac a4(\varepsilon-1)\sum_{\rm odd}\ell(2\ell+1)I_\ell^2$ — dielectric
filling raises $C$, as it must.

### P32.  Exercise 5.7.11 — Dielectric core inside a conducting cylinder  *(Wilcox 2e §5.13, pp.257–258)*
(a) A grounded conducting cylinder of radius $a$ contains a coaxial solid
dielectric cylinder of radius $b<a$; a unit line charge sits in the gap at
$b<\rho'<a$ (Fig. 5.37). By reduced Green functions, exhibit the mode
solutions and all conditions determining the coefficients (no need to solve).
(b) How to get the $\rho'<b$, $b<\rho<a$ branch directly from (a)?
(c) How to get the dielectric↔vacuum swapped problem from (a)?
*Answer:* (a) per azimuthal mode $m\ge1$:
$A\rho^m$ ($\rho<b$), $B\rho^m+C\rho^{-m}$ ($b<\rho<\rho'$),
$D\rho^m+E\rho^{-m}$ ($\rho'<\rho<a$); $m=0$: constants and $\ln\rho$.
Conditions: continuity and $\epsilon g'(b^-)=g'(b^+)$ at $b$; continuity and
jump $g_m'(\rho'^-)-g_m'(\rho'^+)=1/\rho'$ ($\,1/2\rho'$ for $m=0$) at the
source; wall $g_m(a)=0$: five per mode, uniquely solvable.
(b) By symmetry $G(\vec x,\vec x')=G(\vec x',\vec x)$: the $\rho'<b$ branch
is the (a) solution read with arguments exchanged.
(c) By P18's division trick:
$G_{\rm swap}(\epsilon)=\frac1\epsilon G_{(a)}(1/\epsilon)$ (charge again in
the gap region — which is now the dielectric).
*Check:* the $5\times5$ solves satisfy wall/interface/jump conditions per
mode; at $\epsilon=1$ the assembled sum equals the grounded-cylinder image
Green function $-2\ln|\vec x-\vec x'|+2\ln(\rho'|\vec x-\vec x_{\rm im}|/a)$
to $10^{-6}$ (`test_p32_coaxial_dielectric`).

**Solution.** (a) The mode count: regularity at the axis (1 constant in the
core), two 2-parameter annuli split at the source — five per $m$, matching
the five conditions listed (two interface, two source, one wall). For $m=0$
the radial solutions are $\{1,\ln\rho\}$; $D$-continuity at $b$ with a
regular core forces the middle log coefficient to vanish (as in P22), and
the wall then fixes the outer branch to $-\frac12\ln(\rho/a)$-type — the
$m=0$ mode is again $\epsilon$-blind. Uniqueness of the grounded-cavity
Dirichlet problem makes the homogeneous determinant nonzero: "enough
information."
(b) The dielectric Green function is symmetric (5.78), so no new solve is
needed: for $\rho'<b$ evaluate the (a) coefficients at the swapped arguments;
concretely the $\rho<b$ branch $A(\rho')\rho^m$ of (a) becomes, read as a
function of its second argument, the $b<\rho<a$ field of an interior source.
(c) Divide the PDE by $\epsilon$ exactly as in P18/P26:
media $(\epsilon\ \text{core},1\ \text{gap})\to(1\ \text{core},1/\epsilon\ \text{gap})$
with source weight $1/\epsilon$ — the swapped problem with
$\epsilon\to1/\epsilon$, overall factor $1/\epsilon$. (The wall condition
$g(a)=0$ is $\epsilon$-independent and survives both maps.)

### P33.  Exercise 5.7.12 — Quadrupole induced in a dielectric sphere  *(Wilcox 2e §5.13, p.258)*
A unit point charge at $\vec x'$ ($r'>a$) polarizes a dielectric sphere
(radius $a$, permittivity $\epsilon$) centered at the origin. Show the
induced quadrupole moment is
$$Q_{ij}=\frac{2a^5(\epsilon-1)}{3+2\epsilon}
\Big({-\frac{\partial E'_j(0)}{\partial x'_i}}\Big),\qquad
\vec E'(0)=-\frac{\vec x'}{r'^3}$$
(the charge's field at the center) — so a uniform field induces **no**
quadrupole. **[The book prints $a^3$; dimensional analysis and the numeric
check below require $a^5$ — an erratum.]**
*Check:* $Q_{33}$ integrated from the bound surface charge of the exact
series solution matches the formula (with $a^5$) at two radii — confirming
both the coefficient and the $a^5$ scaling; the tensor is traceless-symmetric
with $Q_{11}=Q_{22}=-\frac12Q_{33}$ (`test_p33_induced_quadrupole`).

**Solution.** The $\ell=2$ induced term of the exterior Green function
(5.141) is
$$\Phi_2^{\rm ind}=-\frac{2(\epsilon-1)}{3+2\epsilon}\,
\frac{a^5}{r^3r'^3}\,P_2(\cos\gamma),$$
(coefficient $(\epsilon-1)\ell/[\ell(1+\epsilon)+1]$ at $\ell=2$; note
$2(1+\epsilon)+1=3+2\epsilon$). Compare with the quadrupole potential
$\frac12\sum Q_{ij}x_ix_j/r^5$: for an axisymmetric tensor about $\hat x'$,
$\frac12\sum Q_{ij}x_ix_j/r^5=\frac{Q_{33}}{2}P_2(\cos\gamma)/r^3$ (P5's
algebra with the 3-axis along $\hat x'$), so
$$Q_{33}=-\frac{4(\epsilon-1)}{3+2\epsilon}\,\frac{a^5}{r'^3}.$$
Meanwhile the gradient of the charge's field at the origin is
$$\frac{\partial E'_j(0)}{\partial x'_i}
=-\frac{\partial}{\partial x'_i}\frac{x'_j}{r'^3}
=\frac{3x'_ix'_jr'^{-5}-\delta_{ij}r'^{-3}}{1}
=\frac{3\hat n'_i\hat n'_j-\delta_{ij}}{r'^3},$$
an axisymmetric traceless tensor whose 33-component (along $\hat x'$) is
$2/r'^3$. Hence
$Q_{ij}=\frac{2a^5(\epsilon-1)}{3+2\epsilon}\big(-\partial E'_j/\partial x'_i\big)$
reproduces $Q_{33}$ above and, being proportional to the traceless symmetric
$3\hat n\hat n-\mathbb 1$, all other components — the tensor identity holds,
with $a^5$ (a "quadrupole polarizability" $\propto a^5$, just as the dipole's
is $\propto a^3$; each extra $\ell$ costs $a^2$). Since
$Q_{ij}\propto\partial E'_j/\partial x'_i$, a spatially uniform applied field
(zero gradient) induces no quadrupole — the book's parenthetical remark. The
code's bound-charge quadrature ($\int(3z^2-r^2)\sigma_b\,da$ over the exact
series solution) confirms coefficient and scaling; $a^3$ would be off by
$a^2$ and dimensionally inconsistent ($Q\sim$ charge·length², and
$\partial E'/\partial x'\sim$ charge/length³ leaves length⁵ to supply).
### P34.  Exercise 5.8.1 — Energy identities for permanent polarization  *(Wilcox 2e §5.13, pp.258–259)*
(a) For a material with permanent polarization $\vec P(\vec x)$ and **no free
charge**, show $\displaystyle\int d^3x\,\vec E\cdot\vec D=0$ (all space).
(b) Starting from the pairwise dipole interaction
$\delta W^{\rm int}_{ij}=-\delta\vec p_i\cdot\delta\vec E_j(\vec x_i)$
($i\neq j$), the relation $\vec D=\vec E+4\pi\vec P$, and (a), argue
$$W^{\rm int}=-\frac12\int d^3x\,\vec P\cdot\vec E
=\frac1{8\pi}\int d^3x\,\vec E^2 .$$
*Check:* uniformly polarized sphere: interior + exterior contributions to
$\int\vec E\cdot\vec D$ cancel exactly (closed forms; radial quadrature);
the two $W^{\rm int}$ expressions agree (`test_p34_permanent_polarization_energy`).

**Solution.** (a) With no free charge $\vec\nabla\cdot\vec D=0$ (5.65), and
statics gives $\vec E=-\vec\nabla\Phi$:
$$\int\vec E\cdot\vec D=-\int\vec\nabla\Phi\cdot\vec D
=-\int\vec\nabla\cdot(\Phi\vec D)+\int\Phi\,\vec\nabla\cdot\vec D
=-\oint_{S_\infty}\Phi\,\vec D\cdot\hat n+0=0,$$
the surface term dying because $\Phi\sim1/r$ ($1/r^2$ for neutral bodies) and
$D\sim1/r^3$ while the sphere area grows only as $r^2$.
(b) Summing the pairwise energies over dipole pairs and passing to the
continuum, the interaction energy of the polarized matter is
$W^{\rm int}=-\frac12\int\vec P\cdot\vec E$ — the $\frac12$ correcting the
double count of pairs, with $\vec E$ the *total* (self-consistent) field.
Now eliminate $\vec P$ via $4\pi\vec P=\vec D-\vec E$ and apply (a):
$$-\frac12\int\vec P\cdot\vec E
=-\frac1{8\pi}\int(\vec D-\vec E)\cdot\vec E
=\frac1{8\pi}\int\vec E^2-\frac1{8\pi}\underbrace{\int\vec E\cdot\vec D}_{0}
=\frac1{8\pi}\int\vec E^2 .$$
(The book's comment: the continuum limit quietly *adds* self-energy pieces —
the $i=j$ terms excluded from the sum reappear as the local-field part of the
integral; that is precisely why $W^{\rm int}$ ends up expressible as the
manifestly positive total field energy.) Worked instance (code): uniform
$\vec P_0$ sphere: $\vec E_{\rm in}=-\frac{4\pi}3\vec P_0$,
$\vec D_{\rm in}=+\frac{8\pi}3\vec P_0$ — anti-parallel $E$, $D$! —
and the exterior is the pure dipole $p=\frac{4\pi}3a^3P_0$:
$\int_{\rm in}\vec E\cdot\vec D=-\frac{32\pi^2}9P_0^2V$ exactly cancels
$\int_{\rm out}E^2=+\frac{8\pi}3p^2/a^3$; both $W^{\rm int}$ forms give
$\frac{2\pi}3P_0^2V$.

### P35.  Exercise 5.9.1 — Normal force per unit area on a dielectric surface  *(Wilcox 2e §5.13, p.259)*
(a) Show the normal force per unit area on an arbitrary dielectric surface
($\hat n$ outward from the dielectric; fields $\vec E_1$ inside, $\vec E_2$
outside — Fig. 5.38) is
$$\vec F\cdot\hat n=\frac1{8\pi}\big(E_{2n}^2-E_{1n}^2\big).$$
(b) With only bound charge $\sigma_b$ present:
$\vec F\cdot\hat n=2\pi\sigma_b^2\,\dfrac{1+\epsilon}{\epsilon-1}$.
**Extra:** with both free $\sigma_f$ and bound $\sigma_b$ on the surface:
$$\vec F\cdot\hat n=2\pi\Big[\Big(\frac{\sigma_b\varepsilon}{\varepsilon-1}
+\sigma_f\Big)^2-\frac{\sigma_b^2}{(1-\varepsilon)^2}\Big].$$
*Check:* all three expressions agree pointwise on the charge-above-half-space
interface of P20/P36; the Extra form factors to
$2\pi(\sigma_f+\sigma_b)\big[\sigma_f+\sigma_b\frac{\epsilon+1}{\epsilon-1}\big]$
and reduces to (b) at $\sigma_f=0$ (`test_p35_surface_force_formulas`).

**Solution.** (a) The force on the surface layer is (charge)×(average field),
the §2.11/§5.9 average-field rule (5.185): the layer cannot push on itself,
so the acting field is $\frac12(\vec E_1+\vec E_2)$. The total surface charge
(free+bound) is $4\pi\sigma_{\rm tot}=E_{2n}-E_{1n}$ (tangential components
are continuous and contribute no *normal* force):
$$F_n=\sigma_{\rm tot}\,\frac{E_{1n}+E_{2n}}2
=\frac{(E_{2n}-E_{1n})(E_{2n}+E_{1n})}{8\pi}
=\frac{E_{2n}^2-E_{1n}^2}{8\pi},$$
which is also the jump of the Maxwell normal stress $T_{nn}=E_n^2/8\pi$
(plus continuous tangential pieces that cancel in the difference).
(b) Only bound charge: $D_n$ continuous, $E_{2n}=\epsilon E_{1n}$, and
$4\pi\sigma_b=E_{2n}-E_{1n}=(\epsilon-1)E_{1n}$:
$$F_n=\frac{(E_{2n}-E_{1n})(E_{2n}+E_{1n})}{8\pi}
=\frac{4\pi\sigma_b\cdot4\pi\sigma_b\frac{\epsilon+1}{\epsilon-1}}{8\pi}
=2\pi\sigma_b^2\,\frac{\epsilon+1}{\epsilon-1}\;(>0:\ \text{always outward — 
dielectrics are pulled into the field}).$$
*Extra:* now $E_{2n}-E_{1n}=4\pi(\sigma_f+\sigma_b)$ and
$E_{2n}-\epsilon E_{1n}=4\pi\sigma_f$; solving,
$E_{1n}=4\pi\sigma_b/(\epsilon-1)$,
$E_{2n}=4\pi[\sigma_f+\sigma_b\epsilon/(\epsilon-1)]$, so
$$F_n=\frac{E_{2n}^2-E_{1n}^2}{8\pi}
=2\pi\Big[\Big(\sigma_f+\frac{\sigma_b\epsilon}{\epsilon-1}\Big)^2
-\frac{\sigma_b^2}{(\epsilon-1)^2}\Big],$$
identical to the printed form (note $(1-\varepsilon)^2=(\varepsilon-1)^2$).
Factored, $2\pi(\sigma_f+\sigma_b)[\sigma_f+\sigma_b(\epsilon+1)/(\epsilon-1)]$:
total charge times average field, as it must be.

### P36.  Exercise 5.9.2 — Force on a dielectric half-space, three ways  *(Wilcox 2e §5.13, p.260)*
Compute the force on the semi-infinite dielectric ($z<0$, constant
$\epsilon$) exerted by a unit charge at $z'>0$ (Fig. 5.39):
(a) from the charge–image force; (b) from the energy
$\Delta W=\frac12\int\!\!\int\rho[G_D-G_D^0]\rho$; (c) from P35's surface
stress.
*Answer:* all three give attraction of magnitude
$$F=\frac{\epsilon-1}{\epsilon+1}\,\frac1{4z'^2}$$
(the dielectric is pulled up toward the charge; the charge is pulled down).
*Check:* (a) analytic; (b) $-\partial_{z'}\Delta W$ with
$\Delta W=-\frac{\epsilon-1}{\epsilon+1}\frac1{4z'}$; (c) quadrature of
$2\pi\sigma_b^2\frac{\epsilon+1}{\epsilon-1}$ over the interface — agreement
to $10^{-4}$ (`test_p36_halfspace_force_three_ways`).

**Solution.** (a) The vacuum-side solution is charge $+$ image
$q'=-\frac{\epsilon-1}{\epsilon+1}$ at $-z'$ (P20 with
$\epsilon_1=\epsilon,\epsilon_2=1$). The force on the charge is
$qq'/(2z')^2=-\frac{\epsilon-1}{\epsilon+1}\frac1{4z'^2}$ (toward the
surface). By Newton's third law the dielectric (the physical carrier of the
bound charge that the image summarizes) feels the equal and opposite pull
$+\frac{\epsilon-1}{\epsilon+1}\frac1{4z'^2}$ toward the charge.
(b) The coincidence limit of the induced part:
$G_D-G_D^0=q'/R_2\to q'/(2z')$ at the charge, so
$$\Delta W=\frac12\Big(-\frac{\epsilon-1}{\epsilon+1}\Big)\frac1{2z'}
=-\frac{\epsilon-1}{\epsilon+1}\frac1{4z'} ,\qquad
F_{\rm charge}=-\frac{\partial\Delta W}{\partial z'}
=-\frac{\epsilon-1}{\epsilon+1}\frac1{4z'^2},$$
matching (a) (the $\frac12$ of $\Delta W$ against the *full* image force is
exactly compensated by the $z'$-dependence of the image distance — the same
bookkeeping as the conductor's $W=-q^2/4z'$).
(c) From (5.111)/P20, $\sigma_b(\rho)=-\frac1{2\pi}\frac{\epsilon-1}{\epsilon+1}
\frac{z'}{(\rho^2+z'^2)^{3/2}}$. P35(b):
$$F=\int_0^\infty 2\pi\rho\,d\rho\;2\pi\sigma_b^2\frac{\epsilon+1}{\epsilon-1}
=\frac{\epsilon-1}{\epsilon+1}z'^2\int_0^\infty\frac{\rho\,d\rho}{(\rho^2+z'^2)^3}
=\frac{\epsilon-1}{\epsilon+1}\,\frac{z'^2}{4z'^4}
=\frac{\epsilon-1}{\epsilon+1}\frac1{4z'^2}.$$
Same number, and now with a *location*: half the force accumulates inside
$\rho\lesssim0.64\,z'$ — the stress picture shows where the pull acts, which
the energy methods cannot (the book's §5.9 moral).

### P37.  Exercise 5.9.3 — Thin rod broadside to a distant charge  *(Wilcox 2e §5.13, pp.260–261)*
A dielectric rod ($\epsilon>1$, length $L$, radius $a\ll L$) lies
perpendicular to the line joining its midpoint to a unit positive charge a
distance $z\gg L$ away (Fig. 5.40). Estimate the force; attraction or
repulsion? [The charge's field is nearly uniform over the rod; P13 supplies
the transverse response.]
*Answer:* attraction, of magnitude
$$F=\frac{\epsilon-1}{\epsilon+1}\,\frac{a^2L}{z^5}.$$
*Check:* equals $-\,dW/dz$ of the induced-dipole energy
$W=-\frac{\epsilon-1}{4(\epsilon+1)}a^2L/z^4$; ratio to P38 is
$2/(\epsilon+1)$ (`test_p37_p38_rod_forces`).

**Solution.** The rod sees the charge's field
$E_0=1/z^2$ *transverse* to its axis. P13: a cylinder in a transverse field
carries the uniform interior field $E_{\rm in}=\frac{2E_0}{\epsilon+1}$, so
its polarization is
$\vec P=\frac{\epsilon-1}{4\pi}\vec E_{\rm in}
=\frac{\epsilon-1}{2\pi(\epsilon+1)}\vec E_0$ and the total induced moment
$$p=P\cdot\pi a^2L=\frac{\epsilon-1}{2(\epsilon+1)}\,a^2L\,E_0
\equiv\alpha_\perp E_0,\qquad
\alpha_\perp=\frac{\epsilon-1}{2(\epsilon+1)}a^2L .$$
An *induced* dipole in a nonuniform field has energy
$W=-\frac12\alpha E_0^2(z)=-\frac{\alpha_\perp}{2z^4}$ (the $\frac12$ because
the moment builds with the field), hence
$$F_z=-\frac{dW}{dz}=-\frac{2\alpha_\perp}{z^5}
=-\frac{\epsilon-1}{\epsilon+1}\frac{a^2L}{z^5},$$
negative = toward the charge: **attraction** for $\epsilon>1$ (high-$\epsilon$
matter is always drawn toward stronger field — the $\nabla E^2$ force). The
$z^{-5}$ law is generic for induced dipoles ($F\propto\partial_zE_0^2$).

### P38.  Exercise 5.9.4 — Thin rod pointing at a distant charge  *(Wilcox 2e §5.13, pp.260–261)*
The same long thin cylinder ($\epsilon$, length $L$, radius $a$;
$z\gg L\gg a$) now points **along** the line to the charge (Fig. 5.41). Find
the force; attraction or repulsion for $\epsilon>1$?
*Answer:* attraction,
$$F=\frac{(\epsilon-1)\,a^2L}{2\,z^5}
=\frac{\epsilon+1}2\times F_{\rm P37}$$
— the lengthwise rod is pulled harder by the factor $(\epsilon+1)/2$.
*Check:* $F=-dW/dz$ with $W=-(\epsilon-1)a^2L/(8z^4)$; the needle limit is
justified by the prolate-spheroid depolarization factor
$n_z(\text{aspect}\to\infty)\to0$, verified numerically
($n_z(1)=\frac13$, $n_z(300)<10^{-4}$, $E_{\rm in}\to E_0$)
(`test_p37_p38_rod_forces`).

**Solution.** For a needle *along* the field, the interface condition is
continuity of tangential $E$ along the (dominant) lateral surface: the
interior field equals the applied one, $E_{\rm in}\simeq E_0$, up to end
corrections of order $(a/L)^2\ln$-small — equivalently, the prolate
depolarization factor $n_z\to0$ as the aspect ratio diverges
($E_{\rm in}=E_0/[1+n_z(\epsilon-1)]$). Then
$$p=\frac{\epsilon-1}{4\pi}E_0\cdot\pi a^2L=\frac{(\epsilon-1)a^2L}{4}E_0
\equiv\alpha_\parallel E_0,\qquad
\alpha_\parallel=\frac{(\epsilon-1)a^2L}{4},$$
and the induced-dipole energy/force machinery of P37 gives
$W=-\alpha_\parallel/2z^4$,
$F_z=-2\alpha_\parallel/z^5=-\frac{(\epsilon-1)a^2L}{2z^5}$: attraction.
Comparing polarizabilities:
$\alpha_\parallel/\alpha_\perp=(\epsilon+1)/2>1$ — no depolarization along
the needle versus the factor $\frac2{\epsilon+1}$ broadside. (A free rod
therefore also feels a torque aligning it with the local field before it is
pulled in — needle first.)

### P39.  Exercise 5.9.5 — Slab partially inserted in a capacitor  *(Wilcox 2e §5.13, pp.261–262)*
Parallel plates of length $L$, width $W$, gap $D$; a dielectric block
($\epsilon$) fills the gap to depth $x$ (Fig. 5.42).
(a) Plates held at potential $V$ by a battery: find $F_x$ on the block —
pulled in or pushed out?
(b) The block is withdrawn, a fixed charge $\pm Q$ with
$V/D=4\pi Q/(LW)$ is placed on the plates, and the block re-inserted to
depth $x$: find $F_x$ again. (The book's "soapbox": at any instant the two
protocols give the same force *for the same instantaneous state*;
disconnecting the battery in (a) changes nothing instantaneously, while
reconnecting it in (b) does only because $V$ has meanwhile drifted.)
*Answer:* with $C(x)=\dfrac{W[\epsilon x+(L-x)]}{4\pi D}$:
$$\text{(a)}\ F_x=+\frac{V^2}2\frac{dC}{dx}
=\frac{(\epsilon-1)WV^2}{8\pi D}\ \ (\text{pulled in, $x$-independent});$$
$$\text{(b)}\ F_x=\frac{Q^2}{2C^2}\frac{dC}{dx}
=\frac{(\epsilon-1)WV^2}{8\pi D}\,\frac{L^2}{[L+(\epsilon-1)x]^2}
\ \ (\text{pulled in, weakening as it enters}).$$
*Check:* both equal virtual-work finite differences of $\frac12CV^2$ (at
fixed $V$, with the (5.179) sign) and $Q^2/2C$ (fixed $Q$); they coincide at
$x=0$ (`test_p39_partial_capacitor`).

**Solution.** The two gap regions are capacitors in parallel:
$C(x)=\frac{W}{4\pi D}[\epsilon x+(L-x)]$, $dC/dx=\frac{(\epsilon-1)W}{4\pi D}$.
(a) Fixed $V$ (battery attached): by (5.179) the force is
$+\partial W_{\rm field}/\partial x|_V$ with $W_{\rm field}=\frac12CV^2$
(the battery supplies $VdQ=V^2dC$, twice the field-energy gain, so the net
system energy *falls*):
$F_x=\frac{V^2}2\frac{dC}{dx}=\frac{(\epsilon-1)WV^2}{8\pi D}>0$: sucked in,
uniformly (edge effects neglected).
(b) Fixed $Q=\frac{LWV}{4\pi D}$ (the vacuum-capacitor charge at voltage $V$):
$W_{\rm field}=Q^2/2C(x)$ and
$F_x=-\frac{\partial}{\partial x}\frac{Q^2}{2C}
=\frac{Q^2}{2C^2}\frac{dC}{dx}
=\frac{(\epsilon-1)W}{8\pi D}\Big[\frac{4\pi DQ}{W\,[L+(\epsilon-1)x]}\Big]^2
\cdot\frac{W^2}{(4\pi D)^2}\cdot\ldots
=\frac{(\epsilon-1)WV^2L^2}{8\pi D\,[L+(\epsilon-1)x]^2},$$
i.e. the same formula with $V\to V_{\rm inst}=Q/C(x)=VL/[L+(\epsilon-1)x]$.
Both are positive: dielectrics are *always* drawn into stronger fields,
whatever is held fixed. At the same instantaneous state
($x$, same plate charge) the forces are identical — the sign flip between
$-\partial_x W|_Q$ and $+\partial_x W|_V$ is exactly the battery's ledger
(5.174)–(5.179), not a physical difference; that is the soapbox point.

### P40.  Exercise 5.9.6 — Exact force on the dielectric of P17  *(Wilcox 2e §5.13, p.262)*
For the conductor–gap–dielectric system of P17 (unit charge at $z'$ in the
gap), show the $z$-force on the dielectric is exactly
$$F_z=4\,\frac{1+\epsilon}{1-\epsilon}
\int_0^\infty dk\,k\;\frac{e^{2kd}\,\sinh^2(kz')}
{\big[1+\frac{1+\epsilon}{1-\epsilon}e^{2kd}\big]^2}.$$
*Check:* the integral equals $-\partial_d\Delta W$ (finite difference of
$\Delta W(z',d)=\int_0^\infty k\,dk\,[g-g^0](z',z')$) to $10^{-4}$, and is
negative (dielectric pulled toward the charge) for $\epsilon>1$
(`test_p40_slab_force_integral`).

**Solution.** The dielectric's position enters only through $d$, so at fixed
charge the force on it is $F_z=-\partial\Delta W/\partial d$ with
$$\Delta W(z',d)=\frac12\big[G_D-G^0_D\big]_{\vec x=\vec x'=(0,0,z')}
=\int_0^\infty dk\,k\,\big[g(z',z';k)-g^0\big],$$
($g^0=\sinh(kz')e^{-kz'}/k$ is the conductor-only kernel; the transverse
$k$-integral of $4\pi\int\frac{d^2k}{(2\pi)^2}$ at coincidence is
$2\int_0^\infty k\,dk$). From P17's closed form at $z=z'$, with
$c=\frac{1+\epsilon}{1-\epsilon}$:
$$g(z',z')-g^0=\frac{\sinh(kz')}k\Big\{
\frac{e^{kz'}\big[1+c\,e^{2k(d-z')}\big]}{1+c\,e^{2kd}}-e^{-kz'}\Big\}
=\frac{2\sinh^2(kz')}{k}\,\frac1{1+c\,e^{2kd}},$$
(the $c\,e^{2kd}e^{-kz'}$ pieces cancel between numerator and the
$-e^{-kz'}$ term, leaving $e^{kz'}-e^{-kz'}$). Only the denominator carries
$d$, so per mode
$$-\frac{\partial}{\partial d}\big[g(z',z')-g^0\big]
=\frac{2\sinh^2(kz')}{k}\cdot\frac{2k\,c\,e^{2kd}}{[1+c\,e^{2kd}]^2}
=\frac{4\,c\,e^{2kd}\sinh^2(kz')}{[1+c\,e^{2kd}]^2}.$$
Multiplying by $k\,dk$ and integrating gives the boxed $F_z$. Sign: $c<-1$ for $\epsilon>1$ makes the integrand negative:
$F_z<0$, the slab is pulled *down* toward the charge — consistent with P36's
half-space limit ($d\to z'^+$ dominated by $k\sim1/(d-z')$) and with the
$\epsilon\to\infty$ conductor limit of P42.

### P41.  Exercise 5.9.7 — Weak-dielectric limit and its image reading  *(Wilcox 2e §5.13, p.262)*
(a) Show that for a weak dielectric ($\epsilon-1\ll1$) P40's force becomes
$$F_z\simeq\frac14\,\frac{1-\epsilon}{1+\epsilon}
\Big[\frac1{(d+z')^2}+\frac1{(d-z')^2}-\frac2{d^2}\Big].$$
(b) Confirm by an image computation.
*Check:* the exact integral converges to this form as $\epsilon\to1$ (error
$O((\epsilon-1)^2)$: halving $\epsilon-1$ roughly halves the relative
deviation); the three-term image assembly reproduces it exactly
(`test_p41_weak_dielectric`).

**Solution.** (a) With $\beta=\frac{1-\epsilon}{1+\epsilon}$ small,
$c=1/\beta$ and
$[1+ce^{2kd}]^{-2}\simeq\beta^2e^{-4kd}(1-2\beta e^{-2kd}+\dots)$, so to
first order
$$F_z\simeq4\beta\int_0^\infty dk\,k\,e^{-2kd}\sinh^2(kz')
=\beta\int_0^\infty dk\,k\,\big[e^{-2k(d-z')}+e^{-2k(d+z')}-2e^{-2kd}\big]$$
(using $\sinh^2=\frac14(e^{2kz'}+e^{-2kz'}-2)$), and
$\int_0^\infty k\,e^{-2ks}dk=1/4s^2$ gives the quoted bracket.
(b) To first order in $\beta$ the dielectric surface reflects each vacuum
source once: sources are the charge $+1$ at $z'$ and its conductor image $-1$
at $-z'$; their dielectric images are $\beta$ at $2d-z'$ and $-\beta$ at
$2d+z'$. The force **on the dielectric** is minus the total force its
response exerts... i.e. $-\sum$(forces on the two vacuum sources from the two
$\beta$-images):
$$F^{(+1)}_z=-\frac{\beta}{4(d-z')^2}+\frac{\beta}{4d^2},\qquad
F^{(-1)}_z=+\frac{\beta}{4d^2}-\frac{\beta}{4(d+z')^2},$$
(each pair separated by twice its distance to the plane $z=d$), so
$$F^{\rm diel}_z=-\big[F^{(+1)}_z+F^{(-1)}_z\big]
=\frac\beta4\Big[\frac1{(d-z')^2}+\frac1{(d+z')^2}-\frac2{d^2}\Big].$$
For $\epsilon>1$ ($\beta<0$) the bracket is positive (the $(d-z')^{-2}$
attraction to the near charge wins), so $F<0$: net pull toward the charge.
The $-2/d^2$ piece is the *repulsion* bookkeeping between the dielectric's
response and the conductor image — a genuinely three-body term that a naive
"charge attracts dielectric" estimate misses.

### P42.  Exercise 5.9.8 — The $\epsilon\to\infty$ limit: a second conducting plate  *(Wilcox 2e §5.13, pp.262–263)*
(a) Taking $\epsilon\to\infty$ in P17 (the dielectric face becomes an
equipotential), show the surface charge density on the plane $z=d$ is
$$\sigma(\rho)=-\frac1{2\pi}\int_0^\infty dk\,k\,
\frac{\sinh(kz')}{\sinh(kd)}\,J_0(k\rho).$$
(b) Hence the force on the $z=d$ plate is
$$F_z=-\int_0^\infty dk\,k\,\Big[\frac{\sinh(kz')}{\sinh(kd)}\Big]^2$$
(attraction), and this is the $\epsilon\to\infty$ limit of P40.
*Check:* $\sigma$ and $F$ agree with the two-plate image-ladder values
($10^{-5}$, $10^{-4}$); $F$ equals P40's integral at $\epsilon=10^9$;
$\int\sigma\,da=-z'/d$ (the classic charge-division rule)
(`test_p42_conducting_limit`).

**Solution.** (a) At $\epsilon\to\infty$ P17's kernel becomes the two-plate
Dirichlet kernel $g=\sinh(kz_<)\sinh(k(d-z_>))/[k\sinh(kd)]$ ($g(d)=0$). The
plate charge is $\sigma=\frac1{4\pi}\vec E\cdot\hat n$ with
$\hat n=-\hat z$ (into the gap):
$\sigma=-\frac1{4\pi}\partial_zG|_{z=d^-}\cdot(-1)^{\dots}$ — carefully:
$\sigma=\frac1{4\pi}E_n=-\frac1{4\pi}E_z(d^-)\cdot\ldots$ with
$E_z=-\partial_zG$:
$\sigma=+\frac1{4\pi}\partial_zG|_{d^-}$. Using
$G=2\int_0^\infty k\,dk\,J_0(k\rho)\,g$ (the $m$-sum done by Ex. 4.2.1) and
$\partial_zg|_{z=d}=-\sinh(kz')/\sinh(kd)$:
$$\sigma(\rho)=-\frac1{2\pi}\int_0^\infty dk\,k\,
\frac{\sinh(kz')}{\sinh(kd)}J_0(k\rho).$$
(b) The plate is pulled with pressure $2\pi\sigma^2$ (§2.11) toward the gap:
$$F_z=-\int 2\pi\sigma^2\,da
=-\,2\pi\cdot2\pi\int_0^\infty\rho\,d\rho\,\sigma^2 .$$
Insert (a) and use the Hankel closure
$\int_0^\infty\rho J_0(k\rho)J_0(k'\rho)d\rho=\delta(k-k')/k$:
$$F_z=-\int_0^\infty dk\,k\Big[\frac{\sinh kz'}{\sinh kd}\Big]^2 .$$
*Limit check:* P40 with $c\to-1$:
$4c\,e^{2kd}/[1+ce^{2kd}]^2\to-4e^{2kd}/(e^{2kd}-1)^2=-1/\sinh^2(kd)$ —
exactly (b)'s integrand ✓. And integrating (a):
$\int\sigma\,da=-z'/d$, the standard result that a charge between grounded
plates deposits fractions $z'/d$ and $1-z'/d$ on the far and near plates
(cf. the §3.2/Ex. 3.2.3 induced-charge computation).

### P43.  Exercise 5.9.9 — Capacitor assembled around a dielectric layer  *(Wilcox 2e §5.13, p.263)*
A capacitor consists of a dielectric layer ($\epsilon\neq1$, thickness $d$)
attached to the left plate; the right plate is at distance $x$
($d<x<L$; Fig. 5.43 — the statement's "Figure 5.39" is a figure-number
erratum). A battery establishes $\Delta V$ between the plates.
(a) Battery attached: show the force per unit area on the right plate at
separation $x$ is
$$F=-\frac1{8\pi}\,\frac{\Delta V^2}{[\,d/\epsilon+(x-d)\,]^2}\quad(<0:\ \text{attractive}).$$
(b) The battery is disconnected right after charging at the initial
separation $L$: find $F(x)$ in terms of $\Delta V,\epsilon,d,L,x$.
*Answer:* (b) $F=-2\pi\sigma^2=-\dfrac{\Delta V^2}{8\pi[\,d/\epsilon+(L-d)\,]^2}$
— independent of $x$ (fixed $\sigma$).
*Check:* both from virtual work on $W=\frac12C'\Delta V^2$ (fixed $V$,
(5.179) sign) and $W=2\pi\sigma^2[\,d/\epsilon+(x-d)\,]$ per area (fixed
$Q$) (`test_p43_layered_capacitor`).

**Solution.** Series capacitors: vacuum gap $(x-d)$ plus dielectric layer of
"reduced thickness" $d/\epsilon$ (P19's lesson):
$$\frac1{C'}=4\pi\Big[(x-d)+\frac d\epsilon\Big]\quad(\text{per unit area}).$$
(a) Fixed $\Delta V$: $F=+\partial_x(\tfrac12C'\Delta V^2)|_V
=\frac{\Delta V^2}2\,\frac{dC'}{dx}$ and
$dC'/dx=-C'^2\cdot4\pi$:
$$F=-2\pi C'^2\Delta V^2=-\frac{\Delta V^2}{8\pi[\,d/\epsilon+(x-d)\,]^2},$$
attractive and growing as the gap closes.
(b) Disconnecting at separation $L$ freezes
$\sigma=\frac{\Delta V}{4\pi[\,d/\epsilon+(L-d)\,]}$. At fixed charge the
plate feels the field of everything else, $F=-2\pi\sigma^2$ per area
(equivalently $W/A=2\pi\sigma^2[\,d/\epsilon+(x-d)\,]$ and $F=-\partial_xW$):
constant in $x$,
$$F=-\frac{\Delta V^2}{8\pi[\,d/\epsilon+(L-d)\,]^2}.$$
At $x=L$ (the disconnect instant) the two answers coincide, as they must —
the force is a property of the instantaneous state; thereafter the fixed-$V$
force outgrows the fixed-$Q$ one as the plates approach because the battery
keeps feeding charge.

### P44.  Exercise 5.9.10 — Line charge and dielectric cylinder: force per unit length  *(Wilcox 2e §5.13, p.264)*
Using P22's Green function, with
$F\equiv-\partial\Delta W/\partial\rho'$ and
$\Delta W\equiv\frac12[G_D-G_D^0]_{\vec x=\vec x'}$, find the force per unit
length between the cylinder ($\epsilon>1$, radius $a$) and the unit line
charge at $\rho'>a$; sum the series. Attractive or repulsive?
*Answer:* $\Delta W=-\beta\ln\big(1-\frac{a^2}{\rho'^2}\big)$ with
$\beta=\frac{1-\epsilon}{1+\epsilon}$, and
$$F=-\frac{\partial\Delta W}{\partial\rho'}
=-\frac{\epsilon-1}{\epsilon+1}\,\frac{2a^2}{\rho'(\rho'^2-a^2)}
\qquad\text{— attractive for }\epsilon>1,$$
diverging like $(\rho'-a)^{-1}$ at contact and falling as $2\beta a^2/\rho'^3$
far away.
*Check:* series $=$ closed log to $10^{-10}$; $F=-\partial_{\rho'}\Delta W$
by FD; $\Delta W$ rebuilt from the P22 modes at coincidence matches
(`test_p44_line_charge_cylinder`).

**Solution.** At coincidence the direct parts cancel and only the induced
(image-series) parts of P22's $g_m$ survive:
$$\Delta W=\frac12\sum_{m\ge1}4\cdot\frac1{2m}\,\beta\Big(\frac a{\rho'}\Big)^{2m}
=\beta\sum_{m\ge1}\frac1m\Big(\frac{a^2}{\rho'^2}\Big)^{m}
=-\beta\ln\Big(1-\frac{a^2}{\rho'^2}\Big)$$
($m=0$ contributes nothing — P22's $\epsilon$-blind monopole mode; the
$\sum x^m/m=-\ln(1-x)$ resummation is exact for $\rho'>a$). Then
$$F=-\frac{\partial\Delta W}{\partial\rho'}
=\beta\,\frac{d}{d\rho'}\ln\Big(1-\frac{a^2}{\rho'^2}\Big)
=\beta\,\frac{2a^2}{\rho'(\rho'^2-a^2)}
=-\frac{\epsilon-1}{\epsilon+1}\frac{2a^2}{\rho'(\rho'^2-a^2)} .$$
$\beta<0$ for $\epsilon>1$: attraction, always. Limits: far field
$F\to2\beta a^2/\rho'^3$ — the 2-D induced-dipole law ($W\sim-\alpha_{2D}E_0^2$
with $E_0=2/\rho'$, $\alpha_{2D}=\frac{\epsilon-1}{\epsilon+1}\frac{a^2}2$
per unit length, consistent with P13); near contact the image series piles up
into the half-space result: $F\simeq-\frac{\epsilon-1}{\epsilon+1}/(\rho'-a)$
per... precisely $\beta/(\rho'-a)$ — the 2-D twin of P36 with the line-charge
normalization. The $\epsilon\to\infty$ limit reproduces the conducting
cylinder's image force.
### P45.  Exercise 5.10.1 — Variational structure of the leading-logarithm model  *(Wilcox 2e §5.13, p.264)*
In §5.10's quark-confinement model,
$$\vec E=-\vec\nabla\Phi,\quad \vec D=\epsilon\vec E,\quad
\epsilon=2\alpha\ln\frac{E^2}{K^2}\ (\alpha>0),\qquad
W=\frac1{4\pi}\int d^3x\Big[\frac12\vec E\cdot\vec D+\alpha E^2\Big],$$
and under $\vec E\to\vec E+\delta\vec E$ one has
$\delta W^{(1)}=\frac1{4\pi}\int\vec E\cdot\delta\vec D$ (Eq. 5.189/5.193).
(a) If $\vec\nabla\cdot\delta\vec D=0$ (no change in the free charge), argue
$\delta W^{(1)}=0$: the field configuration is an extremum of $W$.
(b) Expanding to second order in $\delta\vec E$, show $\delta W^{(2)}>0$: the
extremum is a stable minimum.
*Check:* the perfect-differential identity
$\delta[\frac12\vec E\cdot\vec D+\alpha E^2]=\vec E\cdot\delta\vec D$ verified
by finite differences on random $(\vec E,\delta\vec E)$; the second-variation
integrand is positive on random samples in the confinement region $E^2>K^2$
(`test_p45_leading_log_variational`).

**Solution.** (a) With $\vec E=-\vec\nabla\Phi$,
$$\delta W^{(1)}=\frac1{4\pi}\int\vec E\cdot\delta\vec D
=-\frac1{4\pi}\int\vec\nabla\Phi\cdot\delta\vec D
=-\frac1{4\pi}\int\vec\nabla\cdot(\Phi\,\delta\vec D)
+\frac1{4\pi}\int\Phi\,\underbrace{\vec\nabla\cdot\delta\vec D}_{0}=0,$$
the surface term vanishing for localized fields (and on the confinement
boundary $\vec D\cdot\hat n=0$ — the homogeneous Neumann condition of the
flux tube — so $\delta\vec D\cdot\hat n=0$ there too). Fixing
$\vec\nabla\cdot\delta\vec D=0$ is fixing $\delta\rho=0$: among all fields
with the given free charge, the physical one extremizes this particular $W$
— which is *why* the $\alpha E^2$ addition to $\frac12\vec E\cdot\vec D$ is
the right energy functional here (for the nonlinear $\epsilon(E^2)$,
$\frac1{8\pi}\int\vec E\cdot\vec D$ alone is *not* a perfect integral of
$\vec E\cdot\delta\vec D$, cf. (5.162)–(5.163)).
(b) Write $u=E^2$ and the energy density
$4\pi w=\frac12\epsilon(u)u+\alpha u=\alpha[u\ln(u/K^2)+u]\equiv\alpha f(u)$,
with $f'=\ln(u/K^2)+2$, $f''=1/u$. Under $\vec E\to\vec E+\delta\vec E$,
$\delta u=2\vec E\cdot\delta\vec E+|\delta\vec E|^2$, so collecting the
second-order pieces,
$$\delta w^{(2)}=\frac{\alpha}{4\pi}\Big[f'(u)\,|\delta\vec E|^2
+\tfrac12f''(u)\,(2\vec E\cdot\delta\vec E)^2\Big]
=\frac{\alpha}{4\pi}\Big[\Big(\ln\frac{E^2}{K^2}+2\Big)|\delta\vec E|^2
+\frac{2(\vec E\cdot\delta\vec E)^2}{E^2}\Big].$$
In the confinement region the model has $E^2>K^2$, so $\ln(E^2/K^2)>0$ and
both terms are positive for any $\delta\vec E\neq0$: $\delta W^{(2)}>0$, a
strict local minimum. (This convexity is what makes the flux-tube solution
stable and underwrites the linear-confinement bound (5.195)–(5.197):
$W>\frac K{8\pi}\int|\vec D|\ge\frac12K|Q|(R-2r)$ — energy growing linearly
with quark separation.)

### P46.  Exercise 5.11.1 — Bubble in a dielectric fluid vs a free charge  *(Wilcox 2e §5.13, p.265)*
P26's vacuum bubble (radius $a$) sits in a dielectric fluid ($\epsilon$); a
positive unit free charge floats in the fluid at $r_0\gg a$. Find the force
between bubble and charge — attractive or repulsive for $\epsilon>1$?
[Book's hint: adapt Eq. (5.202).]
*Answer:* **repulsive** —
$$\Delta W\simeq+\frac{\epsilon-1}{\epsilon(1+2\epsilon)}\,\frac{a^3}{2r_0^4},
\qquad
F_{r}=-\frac{\partial\Delta W}{\partial r_0}
=+\frac{2(\epsilon-1)}{\epsilon(1+2\epsilon)}\,\frac{a^3}{r_0^5}\;(>0).$$
The (5.202) adaptation: $\epsilon\to1/\epsilon$ **and** an overall $1/\epsilon$
(the charge now sits in the medium).
*Check:* finite-difference force from the exact bubble $\Delta W$ series
matches the far formula at $r_0=12a$ to $2.5\%$ (the $O((a/r_0)^2)$ $\ell=2$
correction); positive, while the sphere counterpart is negative
(`test_p46_bubble_repulsion`).

**Solution.** Repeat (5.198)–(5.202) with P26's kernel, reference medium
$G^0=1/(\epsilon|\vec x-\vec x'|)$:
$$\Delta W=\frac12\big[G_{\rm bubble}-G^0\big]_{\rm coincident}
=\frac{\epsilon-1}{2\epsilon}\sum_{\ell\ge1}
\frac{\ell}{\ell(1+\epsilon)+\epsilon}\,\frac{a^{2\ell+1}}{r_0^{2\ell+2}},$$
whose leading $\ell=1$ term is the boxed $\Delta W$ (denominator
$1+2\epsilon$). Equivalently by the P26 substitution rule applied to (5.202):
$\Delta W_{\rm sphere}=-\frac{\epsilon-1}{\epsilon+2}\frac{a^3}{2r_0^4}
\to\frac1\epsilon\Big[-\frac{\frac1\epsilon-1}{\frac1\epsilon+2}\Big]\frac{a^3}{2r_0^4}
=+\frac{\epsilon-1}{\epsilon(1+2\epsilon)}\frac{a^3}{2r_0^4}$ — "what one has
to do to (5.202)". Since $\Delta W>0$ *increases* as the charge approaches
($r_0\downarrow$), the force pushes the charge away: **repulsion** for
$\epsilon>1$. Physics: the bubble is a hole in a polarizable medium — a
region of polarizability *deficit*. Field energy in a dielectric is lowered
by concentrating field in high-$\epsilon$ material; pushing the low-$\epsilon$
hole away from the strong-field region (equivalently the charge away from the
hole) lowers the energy. This is the electrostatic version of why bubbles in
a dielectric liquid migrate to weak-field regions (and its converse is P47's
attraction of a dielectric sphere in vacuum) — same $1/r_0^5$ law, opposite
sign, $\epsilon$-dependent weight.

### P47.  Exercise 5.11.2 — Sphere–charge force from the polarization-energy formula  *(Wilcox 2e §5.13, p.265)*
Using
$$W-W_0=-\frac12\int_Vd^3x\,\vec P(\vec x)\cdot\vec E_0(\vec x)$$
(Eq. 5.173; the integral only over the dielectric's volume) together with the
interior screening (5.146), re-derive the force between a dielectric sphere
(radius $a$) and a unit point charge at $r'\gg a$.
*Answer:* $\vec P=\frac{\epsilon-1}{4\pi}\frac{3}{\epsilon+2}\vec E_0$ with
$E_0=1/r'^2$ uniform over the sphere:
$$W-W_0=-\frac{\epsilon-1}{\epsilon+2}\,\frac{a^3}{2r'^4}
\qquad\Longrightarrow\qquad
F_r=-\frac{\epsilon-1}{\epsilon+2}\,\frac{2a^3}{r'^5},$$
exactly (5.202): attraction.
*Check:* the closed form equals the exact series (5.201) at large $r'$
(error $O((a/r')^2)$), and $-\partial_{r'}(W-W_0)$ reproduces (5.202) to
$10^{-6}$ (`test_p47_energy_from_polarization`).

**Solution.** For $r'\gg a$ the charge's field is uniform across the sphere,
$\vec E_0\simeq\hat r'/r'^2$ in magnitude $E_0=1/r'^2$. Inside, (5.146):
$\vec E_{\rm in}=\frac3{\epsilon+2}\vec E_0$, so the (uniform) polarization is
$$\vec P=\frac{\epsilon-1}{4\pi}\vec E_{\rm in}
=\frac{3(\epsilon-1)}{4\pi(\epsilon+2)}\vec E_0 .$$
Then
$$W-W_0=-\frac12\,P\,E_0\cdot\frac{4\pi a^3}3
=-\frac12\cdot\frac{3(\epsilon-1)}{4\pi(\epsilon+2)}E_0^2\cdot\frac{4\pi a^3}3
=-\frac{\epsilon-1}{\epsilon+2}\,\frac{a^3E_0^2}2
=-\frac{\epsilon-1}{\epsilon+2}\,\frac{a^3}{2r'^4},$$
which is precisely the $\ell=1$ (leading) term of the exact interaction
energy (5.201) — the Green-function route and the polarization-energy route
are term-for-term the same physics ($-\frac12\alpha E_0^2$ with
$\alpha=\frac{\epsilon-1}{\epsilon+2}a^3$, the induced-dipole energy with the
build-up factor $\frac12$). The force follows:
$F_r=-\partial_{r'}\Delta W=-\frac{\epsilon-1}{\epsilon+2}\frac{2a^3}{r'^5}$,
attractive for $\epsilon>1$, the $1/r'^5$ induced-dipole law (contrast the
grounded conductor's $1/r'^3$: there an $\ell=0$ *monopole* image exists;
the neutral dielectric starts at $\ell=1$ — the book's remark under (5.202)).

### P48.  Exercise 5.11.3 — Charge inside a dielectric droplet  *(Wilcox 2e §5.13, p.265)*
A $+1$ charge sits at radius $r_0$ inside a spherical droplet ("bubble of
dielectric fluid") of radius $a$ and constant $\varepsilon>1$, vacuum outside
(Fig. 5.44). By the Green-function approach, show the radial force on the
charge is
$$F_r=-\frac{\varepsilon-1}{\varepsilon}\sum_{\ell=1}^{\infty}
\frac{\ell(\ell+1)}{[\ell(1+\varepsilon)+1]}\,
\frac{r_0^{2\ell-1}}{a^{2\ell+1}}$$
(negative: the charge is pushed **toward the center**).
*Check:* the force series equals $-\partial_{r_0}\Delta W$ (finite
differences) with $\Delta W$ built from P25's interior coefficients
$B_\ell$; every term negative; the coefficient identity
$\frac12(2\ell+1)B_\ell r_0^{2\ell}$ ↔ series verified term by term
(`test_p48_charge_in_droplet`).

**Solution.** The self-interaction energy of the charge with the droplet's
response is $\Delta W(r_0)=\frac12G_{\rm ind}(\vec r_0,\vec r_0)$, where
$G_{\rm ind}$ is the regular (induced) part of P25's inside–inside kernel —
the reference $G^0=1/(\varepsilon|\vec x-\vec x'|)$ (charge in unbounded
fluid) subtracts the Coulomb-in-medium self-energy. From P25,
$$G_{\rm ind}(\vec x,\vec x')=\sum_\ell(2\ell+1)B_\ell\,(rr')^\ell P_\ell(\cos\gamma),
\qquad
B_\ell=\frac{(\ell+1)(\varepsilon-1)}
{\varepsilon(2\ell+1)[\ell(1+\varepsilon)+1]\,a^{2\ell+1}},$$
so, at coincidence ($P_\ell(1)=1$),
$$\Delta W(r_0)=\frac{\varepsilon-1}{2\varepsilon}\sum_{\ell\ge0}
\frac{\ell+1}{\ell(1+\varepsilon)+1}\,\frac{r_0^{2\ell}}{a^{2\ell+1}} .$$
The $\ell=0$ term is an $r_0$-independent constant (the droplet's overall
self-energy shift); differentiating term by term,
$$F_r=-\frac{\partial\Delta W}{\partial r_0}
=-\frac{\varepsilon-1}{\varepsilon}\sum_{\ell\ge1}
\frac{\ell(\ell+1)}{\ell(1+\varepsilon)+1}\,
\frac{r_0^{2\ell-1}}{a^{2\ell+1}},$$
the quoted series. Every term is negative for $\varepsilon>1$: the charge is
driven to the center. Physically, looking *out* from inside the dense medium,
the interface reflection coefficient has the sign of
$(\varepsilon-1)/(\varepsilon+1)>0$ — the image charge is of the **same**
sign (P20 with the media swapped), so the wall repels the charge; the most
distant wall point pulls least, and the stable point is the center
(restoring force $\propto r_0$ for small $r_0$:
$F_r\simeq-\frac{2(\varepsilon-1)}{\varepsilon(\varepsilon+2)}\frac{r_0}{a^3}$,
a harmonic trap). This is the exact converse of the charge-outside-bubble
repulsion of P46 — both say: the system pushes free charge into the
high-$\varepsilon$ region and keeps it away from interfaces with lower
$\varepsilon$.

### P49.  Exercise 5.11.4 — Dielectric sphere and a distant point dipole  *(Wilcox 2e §5.13, p.266)*
A point dipole $\vec p$ (arbitrary direction) sits at $z=d\gg a$ on the axis
of a dielectric sphere (radius $a$, permittivity $\varepsilon$) centered at
the origin. Show the force components on the dipole are
$$F_i\simeq-3\,\frac{\varepsilon-1}{\varepsilon+2}\,\frac{a^3}{d^7}\times
\begin{cases}-p_3\,p_i,&i=1,2\\[4pt] 3p_3^2+\vec p^{\,2},&i=3 .\end{cases}$$
*Check:* the closed form equals $-\vec\nabla W$ (finite differences) of
$W=-\frac\alpha2|\vec E_p(0)|^2$, and matches the exact two-charge dipole
energy built from the induced kernel at $d=6a$ to $O((a/d)^2)$; $F_3<0$
(attraction toward the sphere) (`test_p49_dipole_sphere_force`).

**Solution.** The sphere responds as an induced dipole
$\vec p_{\rm ind}=\alpha\vec E_p(0)$, $\alpha=\frac{\varepsilon-1}{\varepsilon+2}a^3$
(5.144), in the dipole's field at the center. For the dipole at
$\vec x_d$ ($|\vec x_d|=d$),
$$\vec E_p(0)=\frac{3(\vec p\cdot\hat x_d)\hat x_d-\vec p}{d^3},\qquad
|\vec E_p(0)|^2=\frac{3(\vec p\cdot\hat x_d)^2+\vec p^{\,2}}{d^6},$$
and the induced-response interaction energy (the $\frac12$ of P47) is
$$W(\vec x_d)=-\frac{\alpha}2\,\frac{3(\vec p\cdot\hat x_d)^2+p^2}{d^6}
=-\frac\alpha2\Big[\frac{3(\vec p\cdot\vec x_d)^2}{d^8}+\frac{p^2}{d^6}\Big].$$
Force on the dipole: $\vec F=-\vec\nabla_{x_d}W$. Differentiate:
$$\vec\nabla W=-\frac\alpha2\Big[\frac{6(\vec p\cdot\vec x_d)\,\vec p}{d^8}
-\frac{24(\vec p\cdot\vec x_d)^2\vec x_d}{d^{10}}
-\frac{6p^2\vec x_d}{d^8}\Big],$$
and at $\vec x_d=d\hat z$ ($\vec p\cdot\vec x_d=p_3d$):
$$F_{1,2}=+\frac{3\alpha\,p_3\,p_{1,2}}{d^7},\qquad
F_3=-\frac{3\alpha\,(3p_3^2+p^2)}{d^7},$$
which is exactly the boxed form (note the double negative for $i=1,2$).
Reading it: the radial component is always attractive
($3p_3^2+p^2>0$) with the strongest pull when $\vec p$ is radial
($|E_p(0)|^2=4p^2/d^6$) and weakest broadside ($p^2/d^6$) — factor 4, the
induced-dipole anisotropy; the transverse force $\propto p_3p_{1,2}$ torques
the trajectory unless $\vec p$ is purely radial or purely transverse
(those are the symmetry axes where $\hat x_d$ is a principal direction of
$\vec p\otimes\vec p$). The $d^{-7}$ law completes the module's force ladder:
charge–sphere $r^{-5}$ (P47), dipole–sphere $d^{-7}$ — each source derivative
costs $d^{-1}$ twice in $W=-\frac\alpha2E^2$.
