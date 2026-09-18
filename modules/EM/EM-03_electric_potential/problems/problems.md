# EM-03 — Problems

Work by hand, then check with `code/electric_potential.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  Point-charge potential, and E = −∇V inverts it  *(Gr §2.3.4, p.84; §2.3.1, p.78)*
From $V(\mathbf r)=-\int_\infty^{\mathbf r}\mathbf E\cdot d\mathbf l$ with the Coulomb
field, show the potential of a point charge $q$ at the origin is
$$V(r)=\frac{1}{4\pi\varepsilon_0}\frac{q}{r},$$
then take $-\nabla V$ in spherical coordinates and recover $\mathbf E=(1/4\pi\varepsilon_0)
(q/r^2)\hat{\mathbf r}$ — the two operations invert. *Check:* `potential_of_charge(q)`
equals $kq/r$ at several radii, and `field_from_potential` of it matches
`point_charge_field(q)` componentwise.

**Solution.** The Coulomb field is radial, $\mathbf E=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\hat{\mathbf r}$,
so integrating in from infinity along a radial path ($d\mathbf l=dr\,\hat{\mathbf r}$):
$$V(r)=-\int_\infty^{r}\frac{1}{4\pi\varepsilon_0}\frac{q}{r'^2}\,dr'
=-\frac{q}{4\pi\varepsilon_0}\Big[-\tfrac1{r'}\Big]_\infty^{r}=\frac{1}{4\pi\varepsilon_0}\frac{q}{r}.$$
Inverting with $\mathbf E=-\nabla V$ (here $V$ depends only on $r$):
$$-\nabla V=-\frac{\partial}{\partial r}\!\left(\frac{1}{4\pi\varepsilon_0}\frac{q}{r}\right)\hat{\mathbf r}
=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\hat{\mathbf r},$$
recovering the EM-01 field — the integral and the gradient invert each other. Numerically
`potential_of_charge(q)` gives $V(0.5)=35.9502\text{ V}=kq/r$, and `field_from_potential`
returns $(102.944,\,68.629,\,-34.315)$ at $(0.3,0.2,-0.1)$, matching `point_charge_field(q)`.

### P2.  Potential difference is path-independent  *(Gr §2.3.1, Eq. 2.21, p.78)*
Using $\nabla\times\mathbf E=\mathbf 0$, argue $\oint\mathbf E\cdot d\mathbf l=0$, so that
$$V(\mathbf b)-V(\mathbf a)=-\int_{\mathbf a}^{\mathbf b}\mathbf E\cdot d\mathbf l$$
does not depend on the path chosen between $\mathbf a$ and $\mathbf b$. Confirm this for a
point-charge field by evaluating the drop between two points along two different routes.
*Check:* build `potential_from_field(E, reference=...)` with **two different** reference
points and verify $V(\mathbf p_1)-V(\mathbf p_2)$ is the same for both (they differ only by
an overall constant).

**Solution.** For any electrostatic field $\nabla\times\mathbf E=\mathbf 0$, so Stokes' theorem gives
$\oint\mathbf E\cdot d\mathbf l=\int(\nabla\times\mathbf E)\cdot d\mathbf a=0$ around every closed loop.
Split a loop into a forward path $\mathcal C_1$ and a return $\mathcal C_2$ between the same endpoints:
$$\int_{\mathcal C_1}\mathbf E\cdot d\mathbf l-\int_{\mathcal C_2}\mathbf E\cdot d\mathbf l=0
\;\Rightarrow\;\int_{\mathcal C_1}=\int_{\mathcal C_2},$$
so $V(\mathbf b)-V(\mathbf a)=-\int_{\mathbf a}^{\mathbf b}\mathbf E\cdot d\mathbf l$ depends only on the
endpoints. Shifting the reference point adds the *same* constant to $V(\mathbf p_1)$ and $V(\mathbf p_2)$,
leaving the difference fixed. Two different references give the drop $12.0903$ V vs $12.0904$ V —
equal up to the finite-step ($n=4000$) integration error — confirming path-independence.

### P3.  The dipole potential and its midplane  *(Gr §2.3.4, Eq. 2.29, p.84)*
For $+q$ at $(-a,0,0)$ and $-q$ at $(a,0,0)$, write $V$ as the scalar sum of the two
$q/\eta$ terms. Show $V$ is **odd** under $x\to-x$, so the entire plane $x=0$ is at $V=0$,
and that for $r\gg a$ it reduces to the dipole form
$V\approx(1/4\pi\varepsilon_0)\,\mathbf p\cdot\hat{\mathbf r}/r^2$ with
$\mathbf p=2qa\,\hat{\mathbf x}$ (the leading term of `~EM-05`). *Check:*
`potential_point_charges([(q,(-a,0,0)),(-q,(a,0,0))])` gives $V=0$ on the $x=0$ plane and
$V(x,\cdot)=-V(-x,\cdot)$.

**Solution.** The scalar sum of the two $q/\eta$ terms is
$$V=\frac{1}{4\pi\varepsilon_0}\!\left(\frac{q}{\eta_+}-\frac{q}{\eta_-}\right),\qquad
\eta_\pm=\sqrt{(x\pm a)^2+y^2+z^2},$$
where $\eta_+$ is the distance to $+q$ at $(-a,0,0)$. Under $x\to-x$, $\eta_+\leftrightarrow\eta_-$,
so $V\to-V$ — odd — and on the plane $x=0$ (where $\eta_+=\eta_-$) it vanishes identically. For
$r\gg a$, expand $1/\eta_\pm\approx\frac1r\mp\frac{a x}{r^3}$:
$$V\approx\frac{1}{4\pi\varepsilon_0}\,q\!\left(-\frac{2ax}{r^3}\right)
=\frac{1}{4\pi\varepsilon_0}\frac{\mathbf p\cdot\hat{\mathbf r}}{r^2},\qquad
\mathbf p=\sum_i q_i\mathbf r_i'=-2qa\,\hat{\mathbf x},$$
a dipole of magnitude $2qa$ pointing from the $-q$ toward the $+q$ charge (the leading `~EM-05` term).
On the $+x$ axis $V<0$ — you sit nearer $-q$ — matching `potential_point_charges(...)`, which returns
$0$ on the $x=0$ plane and $V(0.2)=-47.93\text{ V}=-V(-0.2)$.

### P4.  Laplace's equation in vacuum  *(Gr §2.3.3, Eq. 2.25, p.83)*
Show the point-charge potential satisfies $\nabla^2V=0$ everywhere off the source by
computing the spherical Laplacian of $1/r$. (This is why $1/r$ — not the field $1/r^2$ —
is the harmonic object.) *Check:* `poisson_residual(V, 0.0, point)` is $\approx 0$ at
points away from the charge — the finite-difference residual normalized by the curvature
scale $|V|/L^2$.

**Solution.** Off the source $\rho=0$, so Poisson reduces to Laplace, $\nabla^2V=0$. For $V\propto1/r$
use the radial part of the spherical Laplacian, $\nabla^2 f=\frac{1}{r^2}\frac{d}{dr}\!\left(r^2\frac{df}{dr}\right)$:
$$\nabla^2\!\left(\frac1r\right)=\frac{1}{r^2}\frac{d}{dr}\!\left(r^2\cdot\Big(-\frac1{r^2}\Big)\right)
=\frac{1}{r^2}\frac{d}{dr}(-1)=0\qquad(r\neq0).$$
So the point-charge potential is harmonic everywhere off the charge — it is $1/r$, not the field's
$1/r^2$, that solves Laplace's equation. The code confirms it: `poisson_residual(V, 0.0, point)`
returns $-6.4\times10^{-8}$, zero to finite-difference truncation error.

### P5.  Poisson's equation for a charged region  *(Gr §2.3.3, Eq. 2.24, p.83)*
Where $\rho\neq0$ the potential obeys $\nabla^2V=-\rho/\varepsilon_0$. Take the quadratic
bowl $V(\mathbf r)=A\,(x^2+y^2+z^2)$, compute $\nabla^2V=6A$, and identify the uniform
charge density $\rho=-6A\varepsilon_0$ it represents. *Check:* `poisson_residual(V, rho, point)`
is $\approx 0$ when `rho` $=-6A\varepsilon_0$, and is nonzero if you wrongly feed
`rho=0.0` — the residual is the diagnostic that the source matches the curvature of $V$.

**Solution.** For the quadratic bowl $V=A(x^2+y^2+z^2)$ each second derivative is constant,
$\partial_x^2V=\partial_y^2V=\partial_z^2V=2A$, so
$$\nabla^2V=2A+2A+2A=6A.$$
Poisson's equation $\nabla^2V=-\rho/\varepsilon_0$ then forces a uniform source
$\rho=-\varepsilon_0\nabla^2V=-6A\varepsilon_0$. Feeding this into `poisson_residual(V, rho, point)`
gives $\approx-3\times10^{-9}$ (zero up to truncation), whereas the wrong `rho=0.0` returns $6.0$:
the residual $\nabla^2V+\rho/\varepsilon_0$ normalized by the curvature scale $|V|/L^2=A$ equals
$6A/A=6$, exactly diagnosing the missing source.
