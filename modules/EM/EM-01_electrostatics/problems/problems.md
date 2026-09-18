# EM-01 — Problems

Work by hand, then check with `code/electrostatics.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  Field on the axis of a charged ring  *(Gr §2.1.4, Ex. 2.1, p.63)*
A ring of radius $R$ carries uniform line charge with total charge $Q$. Show the
field at height $z$ on the axis is
$$E_z=\frac{1}{4\pi\varepsilon_0}\frac{Qz}{(z^2+R^2)^{3/2}},$$
purely axial by symmetry, and that for $z\gg R$ it reduces to the point charge
$kQ/z^2$. *Check:* build the ring as many small `coulomb_field` charges and compare
`field_magnitude` on the axis to the formula; confirm the far-field monopole limit.

**Solution.** By symmetry the transverse field of each ring element cancels against the
element diametrically opposite, leaving only $E_z$. An element $dq$ lies a distance
$\eta=\sqrt{z^2+R^2}$ from the field point, and its axial projection is $\cos\theta=z/\eta$:
$$dE_z=\frac{1}{4\pi\varepsilon_0}\frac{dq}{\eta^2}\cos\theta
=\frac{1}{4\pi\varepsilon_0}\frac{z\,dq}{(z^2+R^2)^{3/2}}.$$
Every element shares the same $z,R$, so $\int dq=Q$ factors out, giving
$E_z=\dfrac{1}{4\pi\varepsilon_0}\dfrac{Qz}{(z^2+R^2)^{3/2}}$. For $z\gg R$,
$(z^2+R^2)^{3/2}\to z^3$ and $E_z\to kQ/z^2$. Building the ring from $N=400$ point charges,
`field_magnitude` on the axis returns $E_z=8.5634\times10^{2}$ V/m — matching the formula to
all digits (transverse parts $\sim10^{-14}$) — and at $z=2\,\mathrm{m}\gg R$ it reproduces $kQ/z^2$.

### P2.  Superposition nulls — the midpoint and the dipole  *(Gr §2.1.3, p.61)*
Two charges $+q$ sit at $x=\pm a$. Show **E** = 0 at the origin. Replace one with
$-q$ (a dipole, **p** along $-\hat x$): show the origin field no longer vanishes and
that on the $y$-axis (the perpendicular bisector) **E** points along $+\hat x$,
antiparallel to **p**. *Check:* `coulomb_field([(q,(-a,0,0)),(±q,(a,0,0))])` at
`(0,0,0)` and `(0,a,0)`.

**Solution.** Two equal charges: at the origin each field has magnitude $kq/a^2$ and points
*away* from its source (along $\mp\hat x$), so they cancel — $\mathbf E(\mathbf 0)=\mathbf 0$.
Replacing the charge at $x=+a$ by $-q$ makes a dipole with moment
$\mathbf p=\sum_i q_i\mathbf r_i'=q(-a\hat x)+(-q)(a\hat x)=-2qa\,\hat x$. Now both fields point
along $+\hat x$ at the origin (away from $+q$, toward $-q$) and add:
$$\mathbf E(\mathbf 0)=\frac{2kq}{a^2}\,\hat x=1.798\times10^{5}\,\hat x\ \text{V/m}\quad(q=1\ \text{nC},\,a=1\ \text{cm}).$$
On the bisector at $(0,a,0)$ the $y$-components cancel and the $x$-components add to
$\mathbf E=\dfrac{kq}{\sqrt2\,a^2}\hat x=6.355\times10^{4}\,\hat x$ V/m — along $+\hat x$,
antiparallel to $\mathbf p$. These match `coulomb_field(...)` at `(0,0,0)` and `(0,a,0)`.

### P3.  Electric field of a line charge  *(Gr §2.1.4, Ex. 2.2, p.64)*
A straight segment $-L\le z'\le L$ carries uniform $\lambda$. Find $E$ a distance
$s$ from the midpoint, in the perpendicular bisector plane, and show that as
$L\to\infty$ it tends to $E=\lambda/2\pi\varepsilon_0 s$ (the result Gauss's law gives
instantly in `~EM-02`). *Check:* approximate the segment with `field_of_distribution`
on a thin box (or many point charges) and compare to the closed form.

**Solution.** Place the segment on the $z'$-axis and the field point at $(s,0,0)$ in the
bisector plane. The element $dq=\lambda\,dz'$ lies a distance $\eta=\sqrt{s^2+z'^2}$ away;
the $z$-components cancel in pairs, leaving the $s$-component weighted by $\cos\theta=s/\eta$:
$$E_s=\frac{1}{4\pi\varepsilon_0}\int_{-L}^{L}\frac{\lambda\,s\,dz'}{(s^2+z'^2)^{3/2}}
=\frac{\lambda s}{4\pi\varepsilon_0}\left[\frac{z'}{s^2\sqrt{s^2+z'^2}}\right]_{-L}^{L}
=\frac{1}{4\pi\varepsilon_0}\frac{2\lambda L}{s\sqrt{s^2+L^2}}.$$
As $L\to\infty$, $2L/\sqrt{s^2+L^2}\to2$, so $E_s\to\dfrac{\lambda}{2\pi\varepsilon_0\,s}$ — the
infinite-line result Gauss's law gives instantly in `~EM-02`. Modelling the segment as a thin
box of point charges, `field_of_distribution` reproduces this closed form and tends to
$\lambda/2\pi\varepsilon_0 s$ as $L$ grows.

### P4.  Irrotational field  *(Gr §2.2.4, p.77)*
Prove directly from Eq. 2.4 that $\nabla\times\mathbf E=\mathbf 0$ for a point charge,
hence (by superposition) for any electrostatic field. *Check:* `curl(E)` (MA-02) on
`point_charge_field(q)` is zero relative to the gradient scale $|\mathbf E|/r$ — the
property `~EM-03` exploits to define the potential.

**Solution.** Write the point-charge field as a purely radial field,
$\mathbf E=kq\,\dfrac{\hat{\boldsymbol\eta}}{\eta^2}=kq\,\dfrac{\boldsymbol\eta}{\eta^3}$ with
$\boldsymbol\eta=\mathbf r-\mathbf r'$. For any radial $f(\eta)\,\boldsymbol\eta$,
$$\nabla\times\!\big(f(\eta)\,\boldsymbol\eta\big)=f'(\eta)\,\hat{\boldsymbol\eta}\times\boldsymbol\eta
+f(\eta)\,(\nabla\times\boldsymbol\eta)=\mathbf 0,$$
since $\hat{\boldsymbol\eta}\times\boldsymbol\eta=\mathbf 0$ (parallel vectors) and
$\nabla\times\boldsymbol\eta=\mathbf 0$. So one point charge is irrotational; by superposition
(Eq. 2.4) the curl of the sum is the sum of the curls, hence $\nabla\times\mathbf E=\mathbf 0$
for *every* electrostatic field. Numerically `curl(E)` on `point_charge_field(q)` returns
$|\nabla\times\mathbf E|/(|\mathbf E|/r)=9.4\times10^{-10}$ — zero to finite-difference precision —
the property `~EM-03` exploits to write $\mathbf E=-\nabla V$.

### P5.  The monopole limit of a blob  *(Gr §2.1.4, p.63)*
For any localized charge cloud of total charge $Q$, argue from Eq. 2.8 that at
distances large compared with its size the field approaches $kQ/r^2\,\hat{\mathbf r}$
(the shell theorem / leading multipole). *Check:* `field_of_distribution` for a
uniformly charged cube of charge $Q$, evaluated at $r\gg L$, matches $kQ/r^2$ to
fractions of a percent — and the same limit underlies `~EM-05`.

**Solution.** In Eq. 2.8, $\mathbf E(\mathbf r)=\dfrac{1}{4\pi\varepsilon_0}\displaystyle\int
\frac{\hat{\boldsymbol\eta}}{\eta^2}\,\rho(\mathbf r')\,d\tau'$ with $\boldsymbol\eta=\mathbf r-\mathbf r'$.
If the cloud has size $\sim L$ and the field point sits at $r\gg L$, then $|\mathbf r'|\ll r$ for
every source point, so $\eta\to r$ and $\hat{\boldsymbol\eta}\to\hat{\mathbf r}$ uniformly. The
slowly varying factor pulls out of the integral:
$$\mathbf E\to\frac{1}{4\pi\varepsilon_0}\frac{\hat{\mathbf r}}{r^2}\int\rho\,d\tau'
=\frac{1}{4\pi\varepsilon_0}\frac{Q}{r^2}\,\hat{\mathbf r}=\frac{kQ}{r^2}\,\hat{\mathbf r}.$$
Only the total charge $Q$ survives — the monopole / shell-theorem term, leading order of `~EM-05`.
For the uniform cube ($Q=8.00\times10^{-12}$ C) at $r=0.2$ m, `field_of_distribution` returns
$|\mathbf E|=1.7975$ V/m versus $kQ/r^2=1.7975$ V/m — agreement to the quoted digits.
