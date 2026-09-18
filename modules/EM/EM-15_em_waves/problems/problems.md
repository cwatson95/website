# EM-15 — Problems

Work by hand, then check with `code/em_waves.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  The wave equation and the dispersion relation  *(Gr §9.1.1–9.1.2, Eq. 9.2, p.382–385)*
Show that $f(z,t)=A\cos(kz-\omega t)$ solves the wave equation
$\partial^2 f/\partial t^2=v^2\nabla^2 f$ **if and only if** $\omega=vk$, and argue
that any twice-differentiable $g(z-vt)$ is also a solution (the d'Alembert form).
What does $\omega=vk$ say physically about all sinusoidal pieces of a
non-dispersive wave? *Check:* `scalar_plane_wave(k, omega)` with `omega = v*k`
makes `wave_equation_residual(f, v, …)` $\approx 0$ at any point; feeding the wrong
speed (`wave_equation_residual(f, 2*v, …)`) makes the residual $O(1)$.

**Solution.** For $f=A\cos(kz-\omega t)$ the two derivatives pull down a factor each:
$$\frac{\partial^2 f}{\partial t^2}=-\omega^2 f,\qquad \nabla^2 f=\frac{\partial^2 f}{\partial z^2}=-k^2 f.$$
Substituting into $\partial_t^2 f=v^2\nabla^2 f$ gives $-\omega^2 f=-v^2k^2 f$, i.e.
$\omega^2=v^2k^2\Rightarrow\boxed{\omega=vk}$ — true **iff** the speed matches. For a general
$g(z-vt)$, set $\xi=z-vt$: then $\partial_t^2 g=v^2g''(\xi)$ and $\partial_z^2 g=g''(\xi)$,
so $\partial_t^2 g=v^2\partial_z^2 g$ identically (d'Alembert). Physically $\omega=vk$ means the
phase velocity $\omega/k=v$ is the *same for every frequency*: the medium is non-dispersive
and a pulse keeps its shape. This is why `wave_equation_residual` $\approx2.2\times10^{-5}$
(numerically $0$) when `omega = v*k`, but jumps to $\approx0.75=O(1)$ when fed `2*v`.

### P2.  Transverse structure — B locked to E  *(Gr §9.2.2, Eq. 9.49, p.394)*
For a plane wave with $\mathbf E_0=E_0\,\hat{\mathbf x}$ travelling along
$+\hat{\mathbf z}$, use $\nabla\cdot\mathbf E=0$ and Faraday's law to show that
both fields are transverse and that
$$\mathbf B_0=\frac1c\,\hat{\mathbf k}\times\mathbf E_0,\qquad |\mathbf B_0|=\frac{E_0}{c},$$
so $(\hat{\mathbf E},\hat{\mathbf B},\hat{\mathbf k})$ is right-handed. Which way
does $\mathbf B_0$ point? *Check:* `transverse_B((E0,0,0), (0,0,1))` returns a
vector along $+\hat{\mathbf y}$ with `norm` $=E_0/$`C`; `is_transverse` confirms
both $\mathbf E_0\cdot\hat{\mathbf k}=0$ and $\mathbf B_0\cdot\hat{\mathbf k}=0$.

**Solution.** For $\mathbf E=\mathbf E_0e^{i(\mathbf k\cdot\mathbf r-\omega t)}$ the operators
become $\nabla\to i\mathbf k$, $\partial_t\to-i\omega$. Gauss in vacuum,
$\nabla\cdot\mathbf E=0$, gives $i\mathbf k\cdot\mathbf E_0=0$, so $\mathbf E_0\perp\hat{\mathbf k}$
(transverse). Faraday $\nabla\times\mathbf E=-\partial\mathbf B/\partial t$ becomes
$i\mathbf k\times\mathbf E_0=i\omega\mathbf B_0$, hence
$$\mathbf B_0=\frac{\mathbf k\times\mathbf E_0}{\omega}=\frac1c\,\hat{\mathbf k}\times\mathbf E_0,\qquad
|\mathbf B_0|=\frac{k}{\omega}E_0=\frac{E_0}{c}.$$
With $\hat{\mathbf k}=\hat{\mathbf z}$ and $\mathbf E_0=E_0\hat{\mathbf x}$,
$\hat{\mathbf z}\times\hat{\mathbf x}=\hat{\mathbf y}$, so $\mathbf B_0$ points along $+\hat{\mathbf y}$:
$(\hat{\mathbf E},\hat{\mathbf B},\hat{\mathbf k})=(\hat{\mathbf x},\hat{\mathbf y},\hat{\mathbf z})$ is
right-handed. For $E_0=1000$ V/m, `transverse_B` returns $(0,\,3.336\times10^{-6},\,0)$ T, matching
$E_0/c=3.336\times10^{-6}$, and `is_transverse` is `True` for both fields.

### P3.  Polarization states  *(Gr §9.1.4, p.391)*
Starting from $\mathbf E=(A_x\,\hat{\mathbf x}+A_y e^{i\delta}\,\hat{\mathbf y})\,e^{i(kz-\omega t)}$,
find the conditions on $A_x,A_y,\delta$ for **linear**, **circular**, and
**elliptical** polarization, and sketch the tip of the real **E** over one period
for $A_x=A_y$, $\delta=\pi/2$ (a circle) versus $A_x=2A_y$, $\delta=\pi/2$ (an
ellipse). *Check:* `classify_polarization(1, 1, math.pi/2)` → `"circular"`,
`classify_polarization(1, 1, 0)` → `"linear"`,
`classify_polarization(2, 1, math.pi/2)` → `"elliptical"`.

**Solution.** Taking real parts at $z=0$, the tip of $\mathbf E$ moves as
$$E_x=A_x\cos\omega t,\qquad E_y=A_y\cos(\omega t-\delta).$$
If $\delta=0$ or $\pi$ then $E_y=\pm(A_y/A_x)E_x$ — a fixed straight line: **linear**
(also linear if one amplitude vanishes). For $\delta=\pi/2$, $E_y=A_y\sin\omega t$, so the tip
traces $(A_x\cos\omega t,\,A_y\sin\omega t)$, the **ellipse** $(E_x/A_x)^2+(E_y/A_y)^2=1$; when
$A_x=A_y$ this is a **circle** of radius $A$. Everything else is a tilted ellipse. So
$A_x=A_y,\delta=\pi/2$ gives a circle while $A_x=2A_y,\delta=\pi/2$ gives a 2:1 ellipse —
exactly `classify_polarization` returning `"circular"`, `"linear"`, `"elliptical"` for the
three checks.

### P4.  Index, speed, and intensity in glass  *(Gr §9.2.3–9.3.1, Eqs. 9.59 & 9.68, p.398–401)*
Glass has $\varepsilon_r=2.25$ (take $\mu_r\approx1$). Find the index $n$, the
phase velocity $v=c/n$, and the wavelength **inside** the glass of light that is
$\lambda_0=500$ nm in vacuum (recall $\omega$ is unchanged at an interface, so
$\lambda=\lambda_0/n$). Then show the time-averaged intensity of a vacuum wave is
$\langle S\rangle=\tfrac12 c\varepsilon_0 E_0^2$. *Check:* `refractive_index(2.25)`
$=1.5$ and `phase_velocity(2.25)` $=$ `C`$/1.5$; with `omega = 2*math.pi*C/500e-9`,
`wavelength(omega, phase_velocity(2.25))` returns $\lambda_0/1.5\approx333$ nm.

**Solution.** The index is $n=\sqrt{\varepsilon_r\mu_r}=\sqrt{2.25}=1.5$, so the phase
velocity is $v=c/n=2.998\times10^8/1.5=1.999\times10^8$ m/s. Since $\omega$ (hence the
frequency) is conserved across the interface, $\lambda=v/f=(c/n)/(c/\lambda_0)=\lambda_0/n
=500/1.5=333.3$ nm. For the intensity, the Poynting vector is
$\mathbf S=\frac1{\mu_0}\mathbf E\times\mathbf B$ with $B=E/c$, so
$S=\frac{E^2}{\mu_0 c}=c\varepsilon_0E^2$ (using $1/(\mu_0c)=c\varepsilon_0$). Averaging
$E^2=E_0^2\cos^2(kz-\omega t)$ over a period gives $\langle\cos^2\rangle=\tfrac12$, hence
$$\langle S\rangle=\tfrac12 c\varepsilon_0 E_0^2.$$
This matches `refractive_index(2.25)`$=1.5$, `phase_velocity(2.25)`$=$`C`$/1.5$, and
`wavelength(...)`$=3.333\times10^{-7}$ m $=333.3$ nm.

### P5.  Normal-incidence reflection and R + T = 1  *(Gr §9.3.2, Eq. 9.82, p.403)*
Light passes from air ($n_1=1$) into glass ($n_2=1.5$) at normal incidence.
Compute the Fresnel amplitudes $r=(n_1-n_2)/(n_1+n_2)$ and $t=2n_1/(n_1+n_2)$, then
the power coefficients $R=r^2$ and $T=(n_2/n_1)t^2$, and verify $R+T=1$. Explain
the sign of $r$ (the $\pi$ phase shift on reflecting off the denser medium) and
find the reflectance going the other way, glass → air. *Check:* `fresnel_normal(1, 1.5)`
$=(-0.2,\,0.8)$; `reflectance(1, 1.5)` $=0.04$ and `transmittance(1, 1.5)` $=0.96$
sum to $1$; `reflectance(1.5, 1.0)` $=0.04$ as well ($|r|^2$ is the same both ways).

**Solution.** With $n_1=1$, $n_2=1.5$ the amplitude coefficients are
$$r=\frac{n_1-n_2}{n_1+n_2}=\frac{1-1.5}{2.5}=-0.2,\qquad t=\frac{2n_1}{n_1+n_2}=\frac{2}{2.5}=0.8.$$
The power fractions are $R=r^2=0.04$ and $T=\dfrac{n_2}{n_1}t^2=1.5\times0.64=0.96$, so
$R+T=0.04+0.96=1$ — energy is conserved with no absorption. The sign $r<0$ (because
$n_2>n_1$) means the reflected $\mathbf E$ is inverted: a $\pi$ phase shift on reflecting off
the *denser* medium. Reversing the trip, glass→air, $r=\dfrac{1.5-1}{2.5}=+0.2$, so
$R=(0.2)^2=0.04$ — identical, since $R=|r|^2$ is insensitive to the sign flip. These are
exactly `fresnel_normal(1,1.5)`$=(-0.2,0.8)$, `reflectance/transmittance`$=0.04/0.96$, and
`reflectance(1.5,1.0)`$=0.04$.
