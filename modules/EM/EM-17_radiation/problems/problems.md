# EM-17 — Problems

Work by hand, then check with `code/radiation.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages). Throughout, $\eta$ is the source-to-field
separation and $\hat{\boldsymbol\eta}\cdot\mathbf v$ the component of the charge's velocity
toward the field point.

### P1.  The retarded time of a charge at rest  *(Gr §10.2.1, p.444)*
A charge sits permanently at the origin; the field point is at distance $r$. Show directly
from $t_r=t-\eta(t_r)/c$ that the retarded time is simply $t_r=t-r/c$, independent of $t$,
and that the retarded potential is the ordinary Coulomb value $V=q/4\pi\varepsilon_0 r$ —
the delay is real but invisible because the source never changed. *Check:* `retarded_time`
with a constant trajectory returns $t-r/c$; `retarded_potential_static` returns
$(K_E\,q/r,\;t-r/c)$.

**Solution.** The retarded time obeys the implicit condition $t_r=t-\eta(t_r)/c$. For a charge fixed
at the origin the separation to the field point never changes, $\eta(t_r)=r$ (constant), so the
condition is no longer implicit and solves at once:
$$t_r=t-\frac{r}{c},$$
the same delay for every $t$. Feeding this unchanging source into the retarded potential (Eq. 10.26),
the integrand is just the static Coulomb density, so
$$V=\frac{1}{4\pi\varepsilon_0}\frac{q}{r}=\frac{q}{4\pi\varepsilon_0 r}.$$
The light-travel delay $r/c$ is physically real but invisible, because $\rho$ never changed. This is
exactly what `retarded_time` (constant trajectory) gives, $t-r/c$, and `retarded_potential_static`
returns $(K_E\,q/r,\;t-r/c)$.

### P2.  Liénard-Wiechert reduces to Coulomb  *(Gr §10.3.1, p.451)*
Take Eq. 10.46–10.47 and set $\mathbf v=\mathbf 0$. Show the beaming denominator becomes
$\eta(1-0)=\eta$, so $V\to q/4\pi\varepsilon_0\eta$ and $\mathbf A=(\mathbf v/c^2)V\to\mathbf 0$:
a charge at rest has no vector potential and the static result is recovered. *Check:*
`lienard_wiechert` with a constant trajectory and zero velocity gives $V=K_E\,q/\eta$ and
$|\mathbf A|=0$ (and $t_r=t-\eta/c$).

**Solution.** The Liénard-Wiechert potentials (Eq. 10.46–10.47) are
$V=\dfrac{1}{4\pi\varepsilon_0}\dfrac{q}{\eta\,(1-\hat{\boldsymbol\eta}\cdot\mathbf v/c)}$ and
$\mathbf A=(\mathbf v/c^2)V$. Setting $\mathbf v=\mathbf 0$ collapses the beaming denominator,
$$\eta\bigl(1-\hat{\boldsymbol\eta}\cdot\mathbf v/c\bigr)\;\to\;\eta(1-0)=\eta,$$
so
$$V\to\frac{1}{4\pi\varepsilon_0}\frac{q}{\eta}=\frac{q}{4\pi\varepsilon_0\eta},\qquad
\mathbf A=\frac{\mathbf v}{c^2}V\to\mathbf 0.$$
A charge at rest carries no vector potential, and $V$ is the ordinary Coulomb value at the retarded
separation $\eta$ — the static limit recovered. With a constant zero-velocity trajectory
`lienard_wiechert` returns $V=K_E\,q/\eta$, $|\mathbf A|=0$, and $t_r=t-\eta/c$.

### P3.  The beaming enhancement  *(Gr §10.3.1, p.451)*
A point charge moves at constant velocity $v=0.6c$ straight along the $+\hat x$ axis toward a
field point on that axis. Show that, evaluated at the retarded time, the Liénard-Wiechert
potential exceeds the instantaneous Coulomb value $q/4\pi\varepsilon_0\eta$ by the factor
$1/(1-\hat{\boldsymbol\eta}\cdot\mathbf v/c)=1/(1-0.6)=2.5$. Confirm $\mathbf A\neq\mathbf 0$
since the charge is moving. *Check:* `lienard_wiechert` for `vel = 0.6*C` head-on returns
$V$ larger than `K_E*q/η` at the retarded separation $\eta$, and $|\mathbf A|>0$.

**Solution.** With $\mathbf v=0.6c\,\hat{\mathbf x}$ aimed straight at a field point on the $+\hat x$
axis, the retarded separation points the same way, $\hat{\boldsymbol\eta}=\hat{\mathbf x}$, so
$\hat{\boldsymbol\eta}\cdot\mathbf v/c=0.6$. The Liénard-Wiechert $V$ (Eq. 10.46) is the Coulomb value
times the beaming factor:
$$\frac{V}{\,q/4\pi\varepsilon_0\eta\,}=\frac{1}{1-\hat{\boldsymbol\eta}\cdot\mathbf v/c}
=\frac{1}{1-0.6}=2.5.$$
Because $\mathbf v\neq\mathbf 0$, the vector potential $\mathbf A=(\mathbf v/c^2)V\neq\mathbf 0$. Running
`lienard_wiechert` for a head-on $0.6c$ charge returns a potential exceeding the instantaneous
$K_E\,q/\eta$ by a ratio of exactly $2.5000$, with $|\mathbf A|=3.60\times10^{-9}>0$.

### P4.  Larmor's $a^2$ law  *(Gr §11.2.1, p.482; Eq. 11.70, p.484)*
From $P=\mu_0 q^2 a^2/6\pi c$, show the radiated power is quadratic in the acceleration:
doubling $a$ quadruples $P$, while uniform motion ($a=0$) radiates nothing. Estimate the
power radiated by an electron ($q=1.602\times10^{-19}$ C) at $a=10^{22}\,\mathrm{m/s^2}$ and
confirm it is of order $10^{-10}$ W. *Check:* `larmor_power(q, 2e22)/larmor_power(q, 1e22)`
$=4$, and `larmor_power(1.602e-19, 1e22)` $\approx 5.7\times10^{-10}$ W.

**Solution.** Larmor's formula $P=\mu_0 q^2 a^2/6\pi c$ is quadratic in $a$, so scaling $a\to 2a$
multiplies the power by $2^2=4$, while $a=0$ (uniform motion) gives $P=0$ — it is *acceleration*, not
speed, that makes a charge radiate. For an electron at $a=10^{22}\ \mathrm{m/s^2}$,
$$P=\frac{\mu_0 q^2 a^2}{6\pi c}
=\frac{(4\pi\times10^{-7})(1.602\times10^{-19})^2(10^{22})^2}{6\pi\,(2.998\times10^{8})}
\approx5.71\times10^{-10}\ \text{W},$$
of order $10^{-10}$ W. This matches `larmor_power(q,2e22)/larmor_power(q,1e22)`$=4$ and
`larmor_power(1.602e-19,1e22)`$\approx5.71\times10^{-10}$ W.

### P5.  The dipole doughnut and its total power  *(Gr §11.1.2, p.467)*
For $dP/d\Omega=(\mu_0 p_0^2\omega^4/32\pi^2 c)\sin^2\theta$, show (i) the pattern is null on
the axis $\theta=0$ and maximal broadside $\theta=\pi/2$; (ii) integrating over the sphere with
$\int\sin^2\theta\,d\Omega=8\pi/3$ recovers $\langle P\rangle=\mu_0 p_0^2\omega^4/12\pi c$;
(iii) the total scales as $\omega^4$ (Rayleigh / blue sky) and as $p_0^2$. *Check:*
`dipole_angular_power(0,p0,ω)` $=0$ and is largest at $\pi/2$; `total_power_from_pattern(p0,ω)`
matches `dipole_radiated_power(p0,ω)` to $<0.1\%$; doubling $\omega$ multiplies
`dipole_radiated_power` by 16 and doubling $p_0$ by 4.

**Solution.** (i) The pattern carries the factor $\sin^2\theta$: it vanishes on the axis
($\sin 0=0$, an exact null along the dipole) and peaks broadside ($\sin\tfrac{\pi}{2}=1$) — the
doughnut. (ii) Integrate over the sphere, pulling out the constant prefactor:
$$\langle P\rangle=\int\frac{dP}{d\Omega}\,d\Omega
=\frac{\mu_0 p_0^2\omega^4}{32\pi^2 c}\int\sin^2\theta\,d\Omega
=\frac{\mu_0 p_0^2\omega^4}{32\pi^2 c}\cdot\frac{8\pi}{3}
=\frac{\mu_0 p_0^2\omega^4}{12\pi c}.$$
(iii) The total scales as $\omega^4$ (Rayleigh's law — high frequencies dominate, so the sky is blue)
and as $p_0^2$: doubling $\omega$ multiplies $P$ by $2^4=16$, doubling $p_0$ by $2^2=4$. Numerically
`dipole_angular_power(0,...)`$=0$, the broadside value is largest, `total_power_from_pattern` matches
`dipole_radiated_power` to a relative $\sim10^{-13}$ ($\ll0.1\%$), and the $\times16$ and $\times4$
scalings hold exactly.
