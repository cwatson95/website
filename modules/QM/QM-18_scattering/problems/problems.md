# QM-18 — Problems

Work them by hand, then check with `code/scattering.py`. Sources in `../refs.md`.
Units $\hbar=2m=1$ (so $E=k^2$), as in the code.

### P1.  Amplitude to cross-section  *(Griffiths 3e Eq. 10.14, p.481)*
Given the asymptotic wave $\psi\simeq A[e^{ikz}+f(\theta)e^{ikr}/r]$, show the
differential cross-section is $d\sigma/d\Omega=|f(\theta)|^2$ and that the total
cross-section is $\sigma=\int|f|^2\,d\Omega$.
*Answer:* matching scattered flux $|A|^2|f|^2 v/r^2$ through $r^2 d\Omega$ to
incident flux $|A|^2 v$ through $d\sigma$ gives $d\sigma=|f|^2d\Omega$.
*Check:* `differential_cross_section(thetas,k,deltas)` equals `abs(partial_wave_amplitude(...))**2`,
and integrating it over $4\pi$ returns `total_cross_section(k,deltas)`.
(`test_differential_cross_section_is_f_squared`, `test_integrated_dcs_equals_total_cross_section`.)

**Solution.** The incident plane wave $Ae^{ikz}$ carries probability current $j_{\rm inc}=|A|^2v$
with $v=\hbar k/m$. The scattered wave $Af(\theta)e^{ikr}/r$ has outward radial current
$j_r=|A|^2|f|^2v/r^2$, so the rate into solid angle $d\Omega$ is $j_r\,r^2\,d\Omega=|A|^2v\,|f|^2\,d\Omega$.
Dividing the scattered rate by the incident flux $|A|^2v$ gives the area
$$d\sigma=|f(\theta)|^2\,d\Omega\quad\Rightarrow\quad\frac{d\sigma}{d\Omega}=|f(\theta)|^2,\qquad
\sigma=\int|f|^2\,d\Omega.$$
The $1/r^2$ in $j_r$ exactly cancels the $r^2$ in the spherical area element — which is why the
$1/r$ amplitude was forced by flux conservation. `differential_cross_section` returns
$|$`partial_wave_amplitude`$|^2$ identically, and Gauss–Legendre integration of it over $4\pi$
gives $7.860153=$`total_cross_section(k,deltas)`.

### P2.  The factor of four  *(Griffiths 3e Example 10.3 / Eq. 10.36, p.488; classical Example 10.2, p.479)*
A hard sphere of radius $a$. (a) Classically, what is the total cross-section?
(b) Quantum mechanically at low energy ($ka\ll1$), what is it, and by what factor
do they differ?
*Answer:* (a) the geometric shadow $\sigma_{\rm cl}=\pi a^2$. (b) the s-wave
dominates with $\delta_0\approx-ka$, so $\sigma\to(4\pi/k^2)\sin^2(ka)\to4\pi a^2$
— **four times** larger; the long-wavelength wave diffracts around the whole
surface, not just the head-on disc.
*Check:* `total_cross_section(k, phase_shifts_hard_sphere(k,1.0,8))/(pi*1.0**2)` → 4 as
$k\to0$. (`test_hard_sphere_low_energy_4pi_a2`.)

**Solution.** (a) Classically every ray with impact parameter $b<a$ is deflected and every
$b>a$ misses, so the cross-section is the geometric disc $\sigma_{\rm cl}=\pi a^2$. (b) At low
energy only $\ell=0$ survives ($\sin^2\delta_\ell\sim(ka)^{2(2\ell+1)}$ suppresses $\ell\ge1$),
and $\delta_0=-ka$, so
$$\sigma=\frac{4\pi}{k^2}\sin^2\delta_0\ \xrightarrow{\ ka\to0\ }\ \frac{4\pi}{k^2}(ka)^2=4\pi a^2.$$
The ratio is exactly $4$: a wave of wavelength $\gg a$ diffracts around the *entire* sphere, not
just the head-on disc. `total_cross_section(k, phase_shifts_hard_sphere(k,1.0,8))/(pi*1.0**2)`
climbs $3.98682$ ($ka{=}0.1$) $\to3.99880$ ($ka{=}0.03$) $\to3.99997$ ($ka{=}0.005$), tending to $4$.

### P3.  The s-wave hard-sphere phase shift  *(Griffiths 3e Problem 10.6, p.492)*
Show the $\ell=0$ hard-sphere phase shift is $\delta_0=-ka$, and interpret the
resulting radial wave function.
*Answer:* the exterior $u_0\propto\sin(kr+\delta_0)$ must vanish at $r=a$, so
$\delta_0=-ka$ and $u_0\propto\sin\!\big(k(r-a)\big)$ — the free wave simply pushed
outward by the radius. (Equivalently $\tan\delta_\ell=j_\ell(ka)/n_\ell(ka)$, which
for $\ell=0$ is $\arctan(-\tan ka)=-ka$.)
*Check:* `hard_sphere_phase_shift(0, ka, 1.0)` $\approx -ka$ for small $ka$.
(`test_hard_sphere_swave_phase_shift`.)

**Solution.** Outside the core the $\ell=0$ reduced radial wave is free, $u_0(r)\propto\sin(kr+\delta_0)$.
A hard core imposes the Dirichlet condition $u_0(a)=0$, so $ka+\delta_0=0\pmod\pi$, giving
$$\delta_0=-ka,\qquad u_0(r)\propto\sin\!\big(k(r-a)\big).$$
Equivalently $\tan\delta_0=j_0(ka)/n_0(ka)=\dfrac{\sin ka/ka}{-\cos ka/ka}=-\tan ka$, the same
$-ka$. The wave function is just the free sine pushed outward by the radius $a$.
`hard_sphere_phase_shift(0, ka, 1.0)` returns exactly $-ka$ ($-0.010000$ at $ka{=}0.01$,
$-0.200000$ at $ka{=}0.2$).

### P4.  Square well by log-derivative matching  *(Griffiths 3e §10.2.2, p.487)*
For an attractive well $V=-V_0$ ($r<a$), set up the $\ell$-th phase shift by
matching the interior $j_\ell(k_{\rm in}r)$, $k_{\rm in}=\sqrt{k^2+V_0}$, to the
exterior $\cos\delta_\ell\,j_\ell(kr)-\sin\delta_\ell\,n_\ell(kr)$. Specialize to
$\ell=0$.
*Answer:* continuity of $R'/R$ gives
$\tan\delta_\ell=\dfrac{Lj_\ell(ka)-(ka)j_\ell'(ka)}{Ln_\ell(ka)-(ka)n_\ell'(ka)}$,
$L=(k_{\rm in}a)\dfrac{j_\ell'(k_{\rm in}a)}{j_\ell(k_{\rm in}a)}$; for $\ell=0$,
$\delta_0=-ka+\arctan[(k/k_{\rm in})\tan(k_{\rm in}a)]$. As $V_0\to0$, $\delta_\ell\to0$.
*Check:* `square_well_phase_shift(0,k,a,V0)` matches the closed form (in $\sin^2$),
and $V_0\to0$ gives no scattering.
(`test_square_well_swave_closed_form`, `test_square_well_zero_depth_no_scattering`.)

**Solution.** Inside the well, regularity at the origin forces $R=j_\ell(k_{\rm in}r)$,
$k_{\rm in}=\sqrt{k^2+V_0}$ (with $\hbar=2m=1$); outside,
$R=\cos\delta_\ell\,j_\ell(kr)-\sin\delta_\ell\,n_\ell(kr)$. Continuity of the logarithmic
derivative $rR'/R$ at $r=a$, with $L=(k_{\rm in}a)\,j_\ell'(k_{\rm in}a)/j_\ell(k_{\rm in}a)$, gives
$$\tan\delta_\ell=\frac{L\,j_\ell(ka)-(ka)\,j_\ell'(ka)}{L\,n_\ell(ka)-(ka)\,n_\ell'(ka)}.$$
For $\ell=0$ ($j_0=\sin x/x,\ n_0=-\cos x/x$) this collapses to
$\delta_0=-ka+\arctan[(k/k_{\rm in})\tan(k_{\rm in}a)]$; as $V_0\to0$, $k_{\rm in}\to k$ and
$\delta_\ell\to0$. `square_well_phase_shift(0,k,a,V0)` matches the closed form in $\sin^2\delta_0$
($0.575489$ at $k{=}0.5,V_0{=}2$; $0.882053$ at $k{=}1.5,V_0{=}4$), and $V_0\to0$ gives
$\sin^2\delta_\ell\to0$ (no scattering).

### P5.  The optical theorem  *(Griffiths 3e Problem 10.19, p.504)*
Prove $\sigma_{\rm tot}=\frac{4\pi}{k}\operatorname{Im}f(0)$ from the partial-wave
expressions for $f(\theta)$ and $\sigma$, and explain physically why the forward
amplitude must be complex.
*Answer:* at $\theta=0$, $P_\ell(1)=1$ and $\operatorname{Im}(e^{i\delta_\ell}\sin\delta_\ell)=\sin^2\delta_\ell$,
so $\frac{4\pi}{k}\operatorname{Im}f(0)=\frac{4\pi}{k^2}\sum(2\ell+1)\sin^2\delta_\ell=\sigma$.
Physically: flux scattered into all angles is removed from the forward beam by
destructive interference, which requires $\operatorname{Im}f(0)>0$.
*Check:* `optical_theorem_sigma(k,deltas)` equals `total_cross_section(k,deltas)` for
both the hard sphere and the square well.
(`test_optical_theorem_hard_sphere`, `test_optical_theorem_square_well`.)

**Solution.** Set $\theta=0$ in $f(\theta)=\frac1k\sum_\ell(2\ell+1)e^{i\delta_\ell}\sin\delta_\ell
P_\ell(\cos\theta)$; every $P_\ell(1)=1$ and
$\operatorname{Im}(e^{i\delta_\ell}\sin\delta_\ell)=\sin^2\delta_\ell$, so
$$\operatorname{Im}f(0)=\frac1k\sum_\ell(2\ell+1)\sin^2\delta_\ell
\ \Rightarrow\ \frac{4\pi}{k}\operatorname{Im}f(0)=\frac{4\pi}{k^2}\sum_\ell(2\ell+1)\sin^2\delta_\ell=\sigma.$$
Physically, total scattering depletes the forward beam, and that depletion *is* the destructive
interference of the incident wave with the forward-scattered one — which requires $f(0)$ to carry
a positive imaginary part. `optical_theorem_sigma(k,deltas)` and `total_cross_section(k,deltas)`
agree to machine precision, both $=7.860153$ for the $k{=}1.5,V_0{=}4$ well.

### P6.  Born approximation for the Yukawa potential  *(Griffiths 3e Example 10.5, Eq. 10.91, p.500)*
Use the first Born approximation to find $f(\theta)$ for $V(r)=\beta e^{-\mu r}/r$.
*Answer:* $f(\theta)=-\dfrac{2m\beta}{\hbar^2}\dfrac{1}{\mu^2+q^2}$, $q=2k\sin(\theta/2)$,
from the radial integral $-\frac{2m}{\hbar^2 q}\int_0^\infty\beta e^{-\mu r}\sin(qr)\,dr
=-\frac{2m\beta}{\hbar^2}\frac{1}{\mu^2+q^2}$. It is forward-peaked, and the
screening $\mu$ keeps $f(0)$ finite.
*Check:* `born_amplitude_radial(theta,k,V)` (numerical integral) equals
`born_amplitude_yukawa(theta,k,beta,mu)` (closed form); $|f|$ decreases from $\theta=0$.
(`test_born_yukawa_closed_form`, `test_born_forward_peaking`,
`test_yukawa_screening_regularizes_forward`.)

**Solution.** For a spherically symmetric $V$ the Born amplitude reduces to
$f(\theta)=-\frac{2m}{\hbar^2q}\int_0^\infty rV(r)\sin(qr)\,dr$, $q=2k\sin(\theta/2)$. With
$V=\beta e^{-\mu r}/r$ the $r$ cancels, and $\int_0^\infty e^{-\mu r}\sin(qr)\,dr=q/(\mu^2+q^2)$:
$$f(\theta)=-\frac{2m\beta}{\hbar^2q}\int_0^\infty e^{-\mu r}\sin(qr)\,dr
=-\frac{2m\beta}{\hbar^2q}\cdot\frac{q}{\mu^2+q^2}=-\frac{2m\beta}{\hbar^2}\,\frac{1}{\mu^2+q^2}.$$
Since $q$ grows monotonically from $0$ to $2k$, $|f|$ falls monotonically — forward-peaked — and
$\mu>0$ keeps $f(0)=-2m\beta/\hbar^2\mu^2$ finite. The numerical `born_amplitude_radial(theta,k,V)`
equals the closed-form `born_amplitude_yukawa(theta,k,beta,mu)` ($-2.062907$ at $\theta{=}0.3$,
$-0.598600$ at $\theta{=}1.0$).

### P7.  Rutherford from the screened limit  *(Griffiths 3e Example 10.6, Eq. 10.93, p.501; `~CM-08`)*
Take the Yukawa amplitude to the Coulomb limit ($\mu\to0$, $\beta=q_1q_2/4\pi\varepsilon_0$)
and find $d\sigma/d\Omega$. Compare to the classical result of `~CM-08`.
*Answer:* $\dfrac{d\sigma}{d\Omega}=\Big(\dfrac{2m\beta}{\hbar^2}\Big)^2\dfrac1{q^4}
=\Big(\dfrac{\beta}{4E}\Big)^2\dfrac1{\sin^4(\theta/2)}$ — exactly the classical
Rutherford formula. (Classical mechanics, the Born approximation, and QED all
agree for $1/r$.)
*Check:* `rutherford_cross_section(theta,k,beta)*sin(theta/2)**4` is $\theta$-independent
and equals $\beta^2/(16E^2)$ with $E=k^2$; it equals $|$`born_amplitude_yukawa(...,mu=1e-6)`$|^2$.
(`test_born_rutherford_limit`.)

**Solution.** Drop the screening ($\mu\to0$) in the Yukawa amplitude: $f=-\frac{2m\beta}{\hbar^2q^2}$, so
$$\frac{d\sigma}{d\Omega}=|f|^2=\Big(\frac{2m\beta}{\hbar^2}\Big)^2\frac{1}{q^4},\qquad
q^4=(2k)^4\sin^4\tfrac\theta2=16E^2\sin^4\tfrac\theta2,$$
with $E=k^2$ ($\hbar=2m=1$). Hence $d\sigma/d\Omega=(\beta/4E)^2/\sin^4(\theta/2)$ — the Rutherford
formula, identical to the classical `~CM-08` result, the famous agreement of classical mechanics,
the Born approximation and QED for $1/r$. `rutherford_cross_section(theta,k,beta)*sin(theta/2)**4`
is angle-independent at $\beta^2/(16E^2)=0.0625$ ($\beta{=}E{=}1$), and
$|$`born_amplitude_yukawa(...,mu=1e-6)`$|^2=0.465933$ equals `rutherford_cross_section` at $\theta{=}1.3$.

### P8.  The unitarity bound  *(Griffiths 3e Eq. 10.48, p.491)*
From $\sigma=\frac{4\pi}{k^2}\sum(2\ell+1)\sin^2\delta_\ell$, what is the largest a
single partial wave can contribute, and when is it reached?
*Answer:* $\sin^2\delta_\ell\le1$, so $\sigma_\ell\le\dfrac{4\pi}{k^2}(2\ell+1)$,
saturated at $\delta_\ell=\pi/2$ — a **resonance** (the partial wave is fully
"on"). 
*Check:* `partial_cross_section(l,k,delta_l)` $\le 4\pi(2\ell+1)/k^2$ for every $\ell$.
(`test_unitarity_bound`.)

**Solution.** Each partial wave contributes
$\sigma_\ell=\frac{4\pi}{k^2}(2\ell+1)\sin^2\delta_\ell$. Since $\sin^2\delta_\ell\le1$,
$$\sigma_\ell\le\frac{4\pi}{k^2}(2\ell+1),$$
the **unitarity bound**, reached only when $\delta_\ell=\pi/2$ — a resonance, where that partial
wave scatters as strongly as conservation of probability allows. `partial_cross_section(l,k,delta_l)`
stays under $4\pi(2\ell+1)/k^2$ for every $\ell$ (e.g. the near-resonant $\ell=1$ wave of the
$k{=}1.8,V_0{=}7$ well gives $\sigma_1=11.44140\le11.63553$).
