# EM-17 — Radiation (notes)

Radiation = the fields that **escape** an accelerating source. Everything here follows
from one fact electrostatics ignored: a change in the source is not felt instantly, but
only after the news has travelled at the speed of light `c`. That single delay turns the
static potentials into **retarded** potentials, and a source that keeps accelerating
leaves behind a $1/r$ field carrying energy away forever.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page numbers
are the *printed* book pages. Following Griffiths, **η** (script-r) is the **separation
vector** from the source point to the field point; in KaTeX it is written $\eta$ (magnitude),
$\hat{\boldsymbol\eta}$ (direction). For a moving source, **η** is measured to where the
charge *was* at the retarded time, not where it is now.

## 1. Retarded potentials and the retarded time
A source's influence propagates outward at `c`, so the potential at **r** at time $t$ is
set by the charge density not *now* but at the **retarded time** (Gr §10.2.1, p.444),
$$t_r \equiv t-\frac{\eta}{c},$$
one light-crossing-time `η/c` earlier (Eq. 10.19). Solving the wave equation
$\Box V=-\rho/\varepsilon_0$ with this causal delay gives the **retarded potential**
(Gr §10.2.1, Eq. 10.26, p.444),
$$V(\mathbf r,t)=\frac{1}{4\pi\varepsilon_0}\int\frac{\rho(\mathbf r',\,t_r)}{\eta}\,d\tau',
\qquad
\mathbf A(\mathbf r,t)=\frac{\mu_0}{4\pi}\int\frac{\mathbf J(\mathbf r',\,t_r)}{\eta}\,d\tau'.$$
It is the electrostatic/magnetostatic formula with $t\to t_r$ inside the source —
formally the **retarded-Green's-function** (propagator) solution of the wave equation
(`~MA-14`). For a charge that never moved the delay is cosmetic: `retarded_potential_static`
returns the ordinary Coulomb $V=q/4\pi\varepsilon_0\eta$, but tags it with $t_r=t-\eta/c$
to keep the causal bookkeeping explicit; `retarded_time` solves the implicit condition
$t_r=t-\eta(t_r)/c$ for a source on an arbitrary trajectory by fixed-point iteration.

## 2. Liénard-Wiechert potentials of a moving point charge
Collapse the source to a single point charge $q$ on a trajectory $\mathbf w(t)$ and the
retarded integral picks up an extra factor: the charge sweeps through the retarded shell,
so the effective "amount of charge seen" is enhanced. The result is the **Liénard-Wiechert
potentials** (Gr §10.3.1, Eq. 10.46–10.47, p.451),
$$V(\mathbf r,t)=\frac{1}{4\pi\varepsilon_0}\,
  \frac{q\,c}{\eta c-\boldsymbol\eta\cdot\mathbf v}
  =\frac{1}{4\pi\varepsilon_0}\,
  \frac{q}{\eta\,\bigl(1-\hat{\boldsymbol\eta}\cdot\mathbf v/c\bigr)},
\qquad
\mathbf A(\mathbf r,t)=\frac{\mathbf v}{c^{2}}\,V,$$
with $\eta$, $\hat{\boldsymbol\eta}$ and $\mathbf v=\dot{\mathbf w}$ **all evaluated at**
$t_r$. The denominator carries the **beaming factor**
$$\frac{1}{1-\hat{\boldsymbol\eta}\cdot\mathbf v/c}\;:$$
for a charge heading *toward* the field point ($\hat{\boldsymbol\eta}\cdot\mathbf v>0$) it
exceeds 1, enhancing $V$ over the instantaneous Coulomb value; heading away, it suppresses
it. Code: `lienard_wiechert` first calls `retarded_time`, then forms `denom = η·(1−η̂·v/c)`,
`V = K_E q/denom`, `A = (v/c²)V`, returning $(V,\mathbf A,t_r)$. At $\mathbf v=\mathbf 0$
the factor is 1 and $\mathbf A=\mathbf 0$ — the potentials reduce to Coulomb (a tested limit).

## 3. Electric dipole radiation
An electric dipole $\mathbf p(t)=p_0\cos(\omega t)\,\hat{\mathbf z}$ has an accelerating
charge distribution, so its retarded potentials carry a $1/r$ "radiation" tail whose
fields fall as $1/r$ (not $1/r^2$) and therefore drain energy through every sphere. The
time-averaged **angular distribution** is (Gr §11.1.2, Eq. 11.21, p.467)
$$\Big\langle\frac{dP}{d\Omega}\Big\rangle
  =\frac{\mu_0 p_0^{2}\omega^{4}}{32\pi^{2}c}\,\sin^{2}\theta,$$
the **doughnut pattern**: maximum broadside ($\theta=\pi/2$), an exact **null along the
dipole axis** ($\theta=0,\pi$) — no charge radiates along its own line of oscillation.
Integrating over the sphere with $\int\sin^2\theta\,d\Omega=8\pi/3$ gives the **total
radiated power** (Gr §11.1.2, Eq. 11.22, p.467),
$$\langle P\rangle=\frac{\mu_0 p_0^{2}\omega^{4}}{12\pi c}.$$
The $\omega^4$ dependence is the **Rayleigh law** — high frequencies radiate far more
strongly, which is why the sky is blue. Code: `dipole_angular_power(theta, p0, omega)` is
the pattern, `dipole_radiated_power(p0, omega)` the closed-form total, and
`total_power_from_pattern` integrates the first numerically to recover the second (a tested
consistency check, agreement to $<0.1\%$).

## 4. The Larmor formula
For a *single* slow point charge ($v\ll c$) the same calculation gives the power radiated
in terms of its acceleration $a$ — the **Larmor formula** (Gr §11.2.1, p.482; Eq. 11.70 on
p.484),
$$P=\frac{\mu_0 q^{2} a^{2}}{6\pi c}
   =\frac{1}{4\pi\varepsilon_0}\frac{2q^{2}a^{2}}{3c^{3}}.$$
Power scales as the **square of the acceleration**: it is *acceleration*, not speed, that
makes a charge radiate (a charge in uniform motion radiates nothing). Larmor is the
point-charge parent of the dipole result — set $\mathbf p=q\mathbf r$ oscillating and
$\langle a^2\rangle=\tfrac12\omega^4 (p_0/q)^2$ recovers §3. Code: `larmor_power(q, a)`
returns $\mu_0 q^2a^2/6\pi c$; the test confirms the $a^2$ scaling (doubling $a$ quadruples $P$).

## Where this goes
- `~EM-18` recasts the Liénard-Wiechert fields covariantly — the radiation of a charge is
  cleanest in the field tensor $F^{\mu\nu}$ and frame-transformed fields.
- `~QO-03` quantizes this picture: spontaneous and stimulated emission, and laser physics,
  rest on the classical accelerating-dipole radiator analyzed here.
- `~MA-14` is the engine room: the retarded potential **is** the retarded Green's function
  (propagator) of $\Box$, convolved with the source — the same object as the `~QM-19` propagator.
- `~EM-05` supplies the dipole; here it is no longer static but oscillating, and so it radiates.
