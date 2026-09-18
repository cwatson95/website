# EM-08 — Problems

Work by hand, then check with `code/magnetostatics.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  Cyclotron motion — the magnetic force does no work  *(Gr §5.1.2, p.212)*
A charge $Q$ enters a uniform field $\mathbf B = B\,\hat{\mathbf z}$ with velocity
$\mathbf v$. Show $\mathbf F = Q(\mathbf v\times\mathbf B)$ is perpendicular to **v**, so
$dW = \mathbf F\cdot\mathbf v\,dt = 0$ and the speed is constant; the in-plane motion is a
circle of radius $r = mv_\perp/QB$ at frequency $\omega = QB/m$. *Check:*
`lorentz_force(Q, (v,0,0), (0,0,B))` points along $-\hat{\mathbf y}$ with `dot(F, v) == 0`
and `dot(F, B) == 0` — the magnetic force does no work.

**Solution.** The cross product $\mathbf v\times\mathbf B$ is perpendicular to both factors, so
$\mathbf F\cdot\mathbf v = Q(\mathbf v\times\mathbf B)\cdot\mathbf v = 0$ (a vector dotted with a
cross product that contains it). Hence the work done is
$$dW = \mathbf F\cdot d\boldsymbol\ell = \mathbf F\cdot\mathbf v\,dt = 0,$$
so $|\mathbf v|$ is constant. For $\mathbf v = v\,\hat{\mathbf x}$ and $\mathbf B = B\,\hat{\mathbf z}$,
$\hat{\mathbf x}\times\hat{\mathbf z} = -\hat{\mathbf y}$, giving $\mathbf F = -QvB\,\hat{\mathbf y}$.
Numerically $QvB = (1.602\times10^{-19})(10^{6})(0.5) = 8.01\times10^{-14}\,$N, so
$\mathbf F = (0,\,-8.01\times10^{-14},\,0)\,$N — exactly what `lorentz_force` returns, with
`dot(F, v)` and `dot(F, B)` both zero. With the speed fixed, the magnetic force supplies the
centripetal force, $Qv_\perp B = mv_\perp^2/r$, so $r = mv_\perp/QB$ and $\omega = v_\perp/r = QB/m$.

### P2.  Force on a wire, and why parallel currents attract  *(Gr §5.1.3, p.216)*
A straight segment carrying $I$ along **L** sits in a uniform **B**: show $\mathbf F =
I(\mathbf L\times\mathbf B)$. Now let that field be the one set up by a *second* wire
(current $I_2$ a distance $d$ away): using $B = \mu_0 I_2/2\pi d$, show two parallel
currents attract with force per length $\mu_0 I_1 I_2/2\pi d$. *Check:*
`force_on_wire(I, (0,L,0), (0,0,B))` $= (ILB,0,0)$; then feed `infinite_wire_field(I2)`
evaluated at the second wire into `force_on_wire` and recover the $\mu_0 I_1 I_2/2\pi d$
per-length force.

**Solution.** Each element feels $d\mathbf F=I\,d\boldsymbol\ell\times\mathbf B$, which for a
straight segment $\mathbf L$ in uniform $\mathbf B$ integrates to
$\mathbf F=I(\mathbf L\times\mathbf B)$. With $\mathbf L=L\hat{\mathbf y}$, $\mathbf B=B\hat{\mathbf z}$
and $\hat{\mathbf y}\times\hat{\mathbf z}=\hat{\mathbf x}$, this is $\mathbf F=ILB\,\hat{\mathbf x}$.
Let $\mathbf B$ now be the field of a parallel wire $I_2$ a distance $d$ off, $B=\mu_0 I_2/2\pi d$;
a length $\ell$ of wire $I_1$ then feels
$$\frac{F}{\ell}=I_1B=\frac{\mu_0 I_1 I_2}{2\pi d},$$
and the right-hand rule points the force on $I_1$ toward $I_2$ — parallel currents attract.
Numerically `force_on_wire(10, (0,1,0), (0,0,0.5))` $=(5,0,0)$ N $=ILB$; feeding
`infinite_wire_field(10)` at $d=0.05$ m (so $B=4\times10^{-5}$ T) into `force_on_wire` gives
$F/\ell=4\times10^{-4}$ N/m pointing at the other wire — exactly $\mu_0 I_1 I_2/2\pi d$.

### P3.  Infinite wire from Biot–Savart  *(Gr §5.2.2, Ex. 5.5, p.224)*
Integrate the Biot–Savart law along an infinite straight wire and show $B = \mu_0 I/2\pi s$,
directed azimuthally. *Check:* `infinite_wire_field(I)` reproduces $\mu_0 I/2\pi s$ for the
magnitude; approximate the wire by `biot_savart` over a long finite segment $[-L, L]$ and
confirm it converges to `infinite_wire_field` at the mid-plane as $L \gg s$.

**Solution.** Put the wire on the $z$-axis and the field point at distance $s$ in the mid-plane.
With $d\boldsymbol\ell'=dz'\,\hat{\mathbf z}$ and separation length $\eta=\sqrt{s^2+{z'}^2}$, the
cross product $d\boldsymbol\ell'\times\hat{\boldsymbol\eta}$ is azimuthal with magnitude
$\sin\theta\,dz'$ where $\sin\theta=s/\eta$:
$$B=\frac{\mu_0 I}{4\pi}\int_{-\infty}^{\infty}\frac{s\,dz'}{(s^2+{z'}^2)^{3/2}}=\frac{\mu_0 I}{4\pi}\cdot\frac{2}{s}=\frac{\mu_0 I}{2\pi s},$$
since $\int_{-\infty}^{\infty}s\,dz'/(s^2+{z'}^2)^{3/2}=2/s$, with the field circling the wire
azimuthally. For $I=10$ A, `infinite_wire_field` gives exactly $\mu_0 I/2\pi s$
($1.000\times10^{-4}$ T at $s=0.02$ m); approximating the wire by `biot_savart` over $[-L,L]$ climbs
toward it — $9.95\times10^{-5}$, $9.998\times10^{-5}$, $9.99992\times10^{-5}$ T for $L=0.2,1,5$ m —
converging once $L\gg s$.

### P4.  On-axis field of a circular loop  *(Gr §5.2.2, Ex. 5.6, p.224)*
A loop of radius $R$ carries $I$. Show the axial field is
$$B_z = \frac{\mu_0 I R^2}{2\,(R^2 + z^2)^{3/2}},$$
purely axial by symmetry, equal to $\mu_0 I/2R$ at the centre and falling as $\mu_0 I R^2/2z^3$
(a dipole) for $z \gg R$ — the leading term `~EM-09` expands. *Check:* `circular_loop_field(I, R)`
on the axis matches `loop_axis_field_closed(I, R, z)`, with the transverse components
vanishing and the centre value $\mu_0 I/2R$.

**Solution.** On the axis every element $I\,d\boldsymbol\ell'$ sits the same distance
$\eta=\sqrt{R^2+z^2}$ from the field point with $d\boldsymbol\ell'\perp\boldsymbol\eta$, so
$|d\mathbf B|=\tfrac{\mu_0 I}{4\pi}\,d\ell'/(R^2+z^2)$. Symmetry cancels the transverse parts around
the loop, leaving only the $z$-projection, weighted by $\cos\alpha=R/\sqrt{R^2+z^2}$:
$$B_z=\frac{\mu_0 I}{4\pi}\frac{R}{(R^2+z^2)^{3/2}}\oint d\ell'=\frac{\mu_0 I}{4\pi}\frac{R(2\pi R)}{(R^2+z^2)^{3/2}}=\frac{\mu_0 I R^2}{2(R^2+z^2)^{3/2}}.$$
At the centre $z=0$ this is $\mu_0 I/2R$; for $z\gg R$ it falls as $\mu_0 I R^2/2z^3$ — a magnetic
dipole. Numerically `circular_loop_field` (Biot–Savart) and `loop_axis_field_closed` agree on the
axis — $3.142\times10^{-5}$ T at the centre ($=\mu_0 I/2R$ for $I=5$ A, $R=0.1$ m),
$1.111\times10^{-5}$ at $z=0.1$, $9.935\times10^{-7}$ at $z=0.3$ — with the transverse components
vanishing.

### P5.  Ampère's law and the absence of monopoles  *(Gr §5.3.2–5.3.3, p.231 & 233)*
Use Ampère's law $\oint\mathbf B\cdot d\boldsymbol\ell = \mu_0 I_{\text{enc}}$ on a circle
round an infinite wire to get $B\,(2\pi s) = \mu_0 I$ instantly, and argue from
$\nabla\cdot\mathbf B = 0$ that **B** has no sources or sinks. *Check:*
`ampere_circulation(infinite_wire_field(I), s)` equals $\mu_0 I$ for any radius $s$, and
`div_B_residual(infinite_wire_field(I), point)` $\approx 0$ — no magnetic monopoles.

**Solution.** Symmetry makes $\mathbf B$ azimuthal with constant magnitude on a circle of radius
$s$ about the wire, so $\oint\mathbf B\cdot d\boldsymbol\ell=B\oint d\ell=B(2\pi s)$. Ampère's law
sets this equal to $\mu_0 I_{\text{enc}}=\mu_0 I$:
$$B(2\pi s)=\mu_0 I\ \Rightarrow\ B=\frac{\mu_0 I}{2\pi s},$$
the Biot–Savart result in one line, the radius dropping out of the circulation. Its companion
$\nabla\cdot\mathbf B=0$ says $\mathbf B$ has no sources or sinks — field lines never start or stop,
so there are **no magnetic monopoles** (the contrast with $\nabla\cdot\mathbf E=\rho/\varepsilon_0$).
Numerically `ampere_circulation(infinite_wire_field(10), s)` returns $\mu_0 I=1.257\times10^{-5}$ for
every radius (e.g. $s=0.03$ m), and `div_B_residual` $\approx9.6\times10^{-8}\approx0$ — no
monopoles.
