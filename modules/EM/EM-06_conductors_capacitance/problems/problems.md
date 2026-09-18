# EM-06 — Problems

Work by hand, then check with `code/conductors_capacitance.py`. Citations in
`../refs.md`; **Gr** = Griffiths 4e (printed pages). Throughout $k\equiv1/4\pi\varepsilon_0$.

### P1.  Energy to assemble a square of charges  *(Gr §2.4.2, p.92)*
Four equal charges $q$ sit at the corners of a square of side $a$. Show that the work
to assemble them — four edges of length $a$ and two diagonals of length $a\sqrt2$ — is
$$W=\frac{kq^2}{a}\Bigl(4+\sqrt2\Bigr),$$
and explain why no $1/a\to1/0$ self-term appears. *Check:* `work_to_assemble` on the
four corner charges returns $(kq^2/a)(4+\sqrt2)$; it sums only distinct pairs $i<j$,
so each point charge's (infinite) self-energy is omitted by construction.

**Solution.** Use the pairwise form $W=\tfrac12\sum_i q_iV_i=\sum_{i<j}\dfrac{kq_iq_j}{r_{ij}}$.
The square has $\binom{4}{2}=6$ distinct pairs: the **four edges** at separation $a$ and the
**two diagonals** at separation $a\sqrt2$. With all charges equal to $q$,
$$W=4\cdot\frac{kq^2}{a}+2\cdot\frac{kq^2}{a\sqrt2}
   =\frac{kq^2}{a}\Bigl(4+\frac{2}{\sqrt2}\Bigr)=\frac{kq^2}{a}\bigl(4+\sqrt2\bigr).$$
Because the sum runs only over $i<j$, no term ever has $i=j$, so the divergent $1/r_{ii}=1/0$
self-energy of each point charge never enters. With $q=a=1$ this is
$k(4+\sqrt2)=8.988\times10^9\times5.4142=4.866\times10^{10}$ J, exactly what
`work_to_assemble` returns for the four corner charges.

### P2.  Energy of a uniformly charged sphere, two ways  *(Gr §2.4.3, Ex. 2.9, p.94)*
A solid sphere of radius $R$ carries total charge $Q$ uniformly. Using the `~EM-02`
field ($E=kQr/R^3$ inside, $kQ/r^2$ outside), evaluate $\tfrac{\varepsilon_0}{2}\int
E^2\,d\tau$ over all space, splitting the integral at $r=R$. Show
$$W_\text{out}=\tfrac12\frac{kQ^2}{R},\quad W_\text{in}=\tfrac1{10}\frac{kQ^2}{R}
  \ \Rightarrow\ W=\frac35\frac{kQ^2}{R}.$$
*Check:* `field_energy_spherical` on `field_magnitude(uniform_sphere_field(Q,R))`,
integrated from $0$ to a large multiple of $R$, matches `self_energy_uniform_sphere(Q,R)`
to a fraction of a percent (the $1/r^4$ tail is why the outer limit must be pushed far).

**Solution.** With $u=\tfrac{\varepsilon_0}{2}E^2$ and the spherical shell $d\tau=4\pi r^2\,dr$,
and using $4\pi\varepsilon_0 k=1$ so that $\tfrac{\varepsilon_0}{2}\,4\pi k^2=\tfrac{k}{2}$:
$$W_\text{out}=\frac{\varepsilon_0}{2}\!\int_R^\infty\!\Bigl(\frac{kQ}{r^2}\Bigr)^2 4\pi r^2\,dr
   =\frac{k}{2}Q^2\!\int_R^\infty\!\frac{dr}{r^2}=\frac12\frac{kQ^2}{R},$$
$$W_\text{in}=\frac{\varepsilon_0}{2}\!\int_0^R\!\Bigl(\frac{kQr}{R^3}\Bigr)^2 4\pi r^2\,dr
   =\frac{k}{2}\frac{Q^2}{R^6}\!\int_0^R\! r^4\,dr=\frac{k}{2}\frac{Q^2}{R^6}\frac{R^5}{5}
   =\frac{1}{10}\frac{kQ^2}{R}.$$
Adding, $W=\bigl(\tfrac12+\tfrac1{10}\bigr)kQ^2/R=\tfrac35\,kQ^2/R$. Numerically (for $Q=10^{-9}$ C,
$R=0.05$ m) `self_energy_uniform_sphere` gives $1.0785\times10^{-7}$ J, which
`field_energy_spherical` reproduces as $1.0758\times10^{-7}$ J — agreeing to $0.25\%$ once the
upper limit is pushed to $\sim2000R$ to capture the slow $1/r^4$ tail.

### P3.  A parallel-plate capacitor, field energy vs ½CV²  *(Gr §2.5.4, p.105)*
Plates of area $A$ and gap $d$ are charged to voltage $V$, giving a uniform field
$E=V/d$ in the gap. Show the field energy stored in the gap equals the capacitor energy:
$$\frac{\varepsilon_0}{2}E^2(Ad)=\frac12\Bigl(\frac{\varepsilon_0A}{d}\Bigr)V^2
  =\frac12CV^2 .$$
*Check:* `field_energy` of the uniform gap field `lambda x,y,z: (0,0,V/d)` over the
$A\times d$ box equals `energy_stored(capacitance_parallel_plate(A,d), V)` — and the
box quadrature is *exact* here because the integrand is constant.

**Solution.** The gap field is uniform, $E=V/d$, so the energy density
$u=\tfrac{\varepsilon_0}{2}E^2$ is constant and the stored energy is $u$ times the gap volume $Ad$:
$$W=\frac{\varepsilon_0}{2}E^2(Ad)=\frac{\varepsilon_0}{2}\frac{V^2}{d^2}\,Ad=\frac{\varepsilon_0 A}{2d}\,V^2.$$
Identifying the parallel-plate capacitance $C=\varepsilon_0 A/d$,
$$W=\frac12\Bigl(\frac{\varepsilon_0 A}{d}\Bigr)V^2=\frac12CV^2,$$
so the field picture (Eq. 2.45) and the circuit picture (Eq. 2.55) land on one number. For
$A=0.01$ m², $d=1$ mm, $V=12$ V this is $C=88.5$ pF and $\tfrac12CV^2=6.375\times10^{-9}$ J;
`field_energy` over the $A\times d$ box returns the identical $6.375\times10^{-9}$ J — exact here
because the constant integrand makes the midpoint quadrature exact.

### P4.  Spherical and coaxial capacitors, and a limit  *(Gr §2.5.4, Ex. 2.11, p.105)*
From $C=Q/V$ with the `~EM-02` fields, derive $C=4\pi\varepsilon_0\,ab/(b-a)$ for
concentric spheres (radii $a<b$) and $C=2\pi\varepsilon_0L/\ln(b/a)$ for coaxial
cylinders of length $L$. Show the spherical result $\to4\pi\varepsilon_0a$ as
$b\to\infty$ — the isolated sphere. *Check:* `capacitance_spherical(a, b)` tends to
`capacitance_isolated_sphere(a)` as $b$ grows large, and `capacitance_cylindrical`
increases with $L$ (and with shrinking gap $b/a$).

**Solution.** Place $\pm Q$ on the conductors, integrate the `~EM-02` field across the gap for $V$,
and form $C=Q/V$. **Spheres** ($E=kQ/r^2$ between $a$ and $b$):
$$V=\int_a^b\frac{kQ}{r^2}\,dr=kQ\Bigl(\frac1a-\frac1b\Bigr)=\frac{Q}{4\pi\varepsilon_0}\frac{b-a}{ab}\ \Rightarrow\ C=4\pi\varepsilon_0\frac{ab}{b-a}.$$
As $b\to\infty$, $ab/(b-a)\to a$, recovering the isolated sphere $C=4\pi\varepsilon_0 a$.
**Cylinders** ($E=\lambda/2\pi\varepsilon_0 s$, $\lambda=Q/L$):
$$V=\int_a^b\frac{\lambda}{2\pi\varepsilon_0 s}\,ds=\frac{Q}{2\pi\varepsilon_0 L}\ln\frac{b}{a}\ \Rightarrow\ C=\frac{2\pi\varepsilon_0 L}{\ln(b/a)},$$
which grows with $L$ and with a tighter gap (smaller $\ln(b/a)$). Numerically
`capacitance_spherical(0.05, b)` runs $1.11\times10^{-11}\to5.62\times10^{-12}\to5.564\times10^{-12}$ F
for $b=0.1,5,500$ m, closing on `capacitance_isolated_sphere(0.05)` $=5.563\times10^{-12}$ F; and
`capacitance_cylindrical` rises from $5.06\times10^{-11}$ F at $L=1$ m to $1.01\times10^{-10}$ F at
$L=2$ m (and to $8.03\times10^{-11}$ F as the gap tightens to $b=2$ mm).

### P5.  The outward force on a conductor  *(Gr §2.5.3, Eq. 2.51, p.103)*
A conductor carries surface charge density $\sigma$, so $E=\sigma/\varepsilon_0$ just
outside and $0$ inside. Argue that the charge sheet feels the **average** of these
fields and hence an outward pressure
$$P=\frac{\sigma^2}{2\varepsilon_0}=\frac{\varepsilon_0}{2}E^2 ,$$
independent of the sign of $\sigma$. Apply it to one plate of the P3 capacitor: each
plate is pulled toward the other at this pressure. *Check:* `surface_pressure(sigma)`
returns $\sigma^2/2\varepsilon_0$ and equals $\tfrac{\varepsilon_0}{2}(\sigma/$`EPS0`$)^2$,
the field form of the same result.

**Solution.** The surface layer itself produces the jump from $0$ inside to $\sigma/\varepsilon_0$
outside; the field acting *on* the layer omits its own contribution and is the **average** of the
two sides, $E_{\text{avg}}=\tfrac12(\sigma/\varepsilon_0+0)=\sigma/2\varepsilon_0$. The force per
area is the charge density times this field:
$$P=\sigma E_{\text{avg}}=\frac{\sigma^2}{2\varepsilon_0}=\frac{\varepsilon_0}{2}E^2,\qquad E=\frac{\sigma}{\varepsilon_0}\ \text{just outside}.$$
Because it goes as $\sigma^2$ it is positive whatever the sign of $\sigma$, so the pull is always
*outward*, into the field. For one plate of the P3 capacitor ($\sigma=\varepsilon_0 V/d$) this is
the attraction toward the opposite plate. Numerically `surface_pressure(1e-6)` $=5.647\times10^{-2}$
Pa, equal to $\tfrac{\varepsilon_0}{2}(\sigma/\varepsilon_0)^2$ — the same result in field form.
