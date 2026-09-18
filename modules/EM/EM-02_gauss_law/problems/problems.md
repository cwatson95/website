# EM-02 — Problems

Work by hand, then check with `code/gauss_law.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  Flux of a point charge is surface-independent  *(Gr §2.2.1, p.66)*
A point charge $q$ sits inside a closed surface. Show that the outward electric flux is
$$\oint_{\mathcal S}\mathbf E\cdot d\mathbf a=\frac{q}{\varepsilon_0},$$
independent of the size or shape of the surface, and that a charge placed *outside*
contributes zero net flux. *Check:* `flux_through_sphere(point_charge_field(q))` at
several radii (each gives `q/EPS0`), `enclosed_charge` reads $q$ back, and a charge at
$(3,0,0)$ outside an $R=1$ sphere returns ~0.

**Solution.** Centre a sphere of radius $r$ on the charge. With
$\mathbf E=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\hat{\mathbf r}$ and
$d\mathbf a=r^2\sin\theta\,d\theta\,d\varphi\,\hat{\mathbf r}$, the two factors of $r^2$ cancel:
$$\oint_{\mathcal S}\mathbf E\cdot d\mathbf a=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\,(4\pi r^2)=\frac{q}{\varepsilon_0}.$$
The radius drops out, so the flux is identical through *any* enclosing surface (field lines
are unbroken in charge-free space); a charge placed *outside* contributes nothing, since every
line that enters the surface also leaves it. Hence $\Phi_E=q/\varepsilon_0$, independent of size
and shape. (`flux_through_sphere` gives $\varepsilon_0\Phi_E=q=10^{-9}$ C at $R=0.1,0.5,2$ m,
`enclosed_charge` reads $q$ back, and the charge at $(3,0,0)$ returns $\sim2\times10^{-15}\approx0$.)

### P2.  Uniformly charged solid sphere  *(Gr §2.2.3, p.71)*
A sphere of radius $R$ carries total charge $Q$ at uniform density. With a concentric
Gaussian sphere, show
$$E(r)=\frac{1}{4\pi\varepsilon_0}\frac{Q}{r^2}\ (r\ge R),\qquad
E(r)=\frac{1}{4\pi\varepsilon_0}\frac{Q\,r}{R^3}\ (r<R),$$
continuous at $r=R$ — point-charge-like outside, linear inside. *Check:*
`uniform_sphere_field(Q, R)`; compare `field_magnitude` at $r=3R$ and $r=R/2$ to the two
formulas and confirm continuity across $r=R$.

**Solution.** Symmetry forces $\mathbf E=E(r)\hat{\mathbf r}$, so a concentric Gaussian sphere of
radius $r$ gives $\oint\mathbf E\cdot d\mathbf a=E(r)\,4\pi r^2=Q_{\text{enc}}/\varepsilon_0$.
Outside ($r\ge R$) the surface encloses all of $Q$:
$$E(r)\,4\pi r^2=\frac{Q}{\varepsilon_0}\ \Rightarrow\ E=\frac{1}{4\pi\varepsilon_0}\frac{Q}{r^2},$$
the point-charge field. Inside ($r<R$) only the fraction $(r/R)^3$ of the uniform charge lies
within, $Q_{\text{enc}}=Q(r/R)^3$:
$$E(r)\,4\pi r^2=\frac{Q}{\varepsilon_0}\frac{r^3}{R^3}\ \Rightarrow\ E=\frac{1}{4\pi\varepsilon_0}\frac{Qr}{R^3}.$$
At $r=R$ both branches give $kQ/R^2$, so $E$ is continuous. For $Q=2$ nC, $R=0.1$ m,
`field_magnitude` returns $199.7$ V/m at $r=3R$ ($=kQ/9R^2$) and $898.8$ V/m at $r=R/2$
($=kQ/2R^2$), matching the two formulas, and both branches meet at $kQ/R^2=1797.5$ V/m across
$r=R$.

### P3.  Infinite line charge  *(Gr §2.2.3, p.71)*
An infinite line carries uniform $\lambda$. With a coaxial Gaussian cylinder of radius
$s$ and length $\ell$ (only the curved wall carries flux), show
$$\mathbf E=\frac{\lambda}{2\pi\varepsilon_0 s}\,\hat{\mathbf s},$$
purely radial and falling off as $1/s$ — the field `~EM-01` reached only as the
$L\to\infty$ limit of a finite segment. *Check:* `line_charge_field(lam)`; verify
`field_magnitude` $\propto 1/s$ and that the axial component vanishes off-axis.

**Solution.** Cylindrical symmetry makes $\mathbf E=E(s)\hat{\mathbf s}$, radial and the same all
along and around the axis. On a coaxial cylinder of radius $s$ and length $\ell$ the flat caps
carry no flux ($\mathbf E\perp\hat{\mathbf n}$), and the curved wall (area $2\pi s\ell$) has
$\mathbf E\parallel d\mathbf a$:
$$\oint\mathbf E\cdot d\mathbf a=E(s)\,(2\pi s\ell)=\frac{Q_{\text{enc}}}{\varepsilon_0}=\frac{\lambda\ell}{\varepsilon_0}.$$
The length cancels, leaving
$$\mathbf E=\frac{\lambda}{2\pi\varepsilon_0 s}\,\hat{\mathbf s},$$
purely radial and falling as $1/s$. For $\lambda=2$ nC/m, `field_magnitude` of `line_charge_field`
gives $359.5$ V/m at $s=0.1$ m and $179.8$ V/m at $s=0.2$ m — a clean factor-of-two $1/s$ drop —
while the axial component $E_z=0$ off-axis, confirming the field is exactly radial.

### P4.  Infinite sheet of charge and the field jump  *(Gr §2.2.3, p.71)*
An infinite plane carries uniform $\sigma$. With a Gaussian pillbox straddling the sheet,
show the field is *uniform*,
$$\mathbf E=\frac{\sigma}{2\varepsilon_0}\,\hat{\mathbf n},$$
pointing away on both sides, so it is discontinuous by $\sigma/\varepsilon_0$ across the
sheet (the boundary condition of `~EM-03`). *Check:* `plane_sheet_field(sigma)`; confirm
the magnitude is distance-independent and the jump
$E_z(0^+)-E_z(0^-)=\sigma/\varepsilon_0$.

**Solution.** By symmetry the field points straight away from the sheet with equal magnitude on
each side, $\mathbf E=\pm E\,\hat{\mathbf n}$. A pillbox of face area $A$ straddling the sheet
catches flux only through its two faces (the field grazes the side walls):
$$\oint\mathbf E\cdot d\mathbf a=2EA=\frac{Q_{\text{enc}}}{\varepsilon_0}=\frac{\sigma A}{\varepsilon_0}\ \Rightarrow\ E=\frac{\sigma}{2\varepsilon_0}.$$
No $A$ and no distance survive, so the field is **uniform**. It reverses across the sheet, so the
normal component jumps by
$$E_z(0^+)-E_z(0^-)=\frac{\sigma}{2\varepsilon_0}-\Bigl(-\frac{\sigma}{2\varepsilon_0}\Bigr)=\frac{\sigma}{\varepsilon_0}.$$
For $\sigma=1$ nC/m², `plane_sheet_field` returns the distance-independent $56.5$ V/m on either
side and a jump of $112.9$ V/m $=\sigma/\varepsilon_0$ across $z=0$.

### P5.  The differential law inside the sphere  *(Gr §2.2.2, Eq. 2.16, p.71)*
From the integral law and the divergence theorem, derive
$\nabla\cdot\mathbf E=\rho/\varepsilon_0$, and verify it on the uniform sphere of P2:
$\nabla\cdot\mathbf E=\rho/\varepsilon_0$ inside and $0$ outside. Note the companion curl
law $\nabla\times\mathbf E=\mathbf 0$ (Gr §2.2.4, p.77), checked in `~EM-01`. *Check:*
`gauss_residual(uniform_sphere_field(Q,R), rho, point)` with
$\rho=Q/\tfrac{4}{3}\pi R^3$ returns ~0 at an interior point (it is normalized by
$\rho/\varepsilon_0$).

**Solution.** Write $Q_{\text{enc}}=\int_{\mathcal V}\rho\,d\tau$ and convert the flux with the
divergence theorem (`~MA-02`):
$$\oint_{\mathcal S}\mathbf E\cdot d\mathbf a=\int_{\mathcal V}(\nabla\cdot\mathbf E)\,d\tau=\int_{\mathcal V}\frac{\rho}{\varepsilon_0}\,d\tau.$$
Since this holds for *every* volume, the integrands match: $\nabla\cdot\mathbf E=\rho/\varepsilon_0$.
On the P2 sphere, inside $\mathbf E=\tfrac{kQ}{R^3}\mathbf r$ (with $\mathbf r=(x,y,z)$), so
$$\nabla\cdot\mathbf E=\frac{kQ}{R^3}\,\nabla\cdot\mathbf r=\frac{3kQ}{R^3}=\frac{3}{R^3}\frac{Q}{4\pi\varepsilon_0}=\frac{\rho}{\varepsilon_0},\qquad \rho=\frac{Q}{\tfrac43\pi R^3};$$
outside, the inverse-square $\mathbf E=kQ\hat{\mathbf r}/r^2$ has $\nabla\cdot\mathbf E=0$. The
companion $\nabla\times\mathbf E=\mathbf 0$ completes the pair. Hence `gauss_residual` with
$\rho=Q/\tfrac43\pi R^3$ returns $\sim1.4\times10^{-13}$ at the interior point — zero up to the
finite-difference truncation, confirming $\nabla\cdot\mathbf E=\rho/\varepsilon_0$.
