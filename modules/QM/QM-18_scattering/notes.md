# QM-18 — Scattering theory (notes)

Almost everything we know about the subatomic world comes from scattering: fire a
beam at a target, count where the particles go. The theory connects two objects —
the **potential** $V(\mathbf r)$ (what you want to know) and the **differential
cross-section** $d\sigma/d\Omega$ (what you measure) — through a single complex
function, the **scattering amplitude** $f(\theta)$. This note follows Griffiths 3e
Chapter 10: the amplitude (§10.1), two ways to compute it — partial waves (§10.2),
phase shifts (§10.3) — the optical theorem that ties them together, and the Born
approximation (§10.4).

Units: the code uses $\hbar=2m=1$, so the energy is $E=k^2$; $\hbar$ and $m$ are
kept explicit in the Born formulae below so SI can be restored.

## 1. The amplitude and the cross-section

An incident plane wave $e^{ikz}$ hits a localized target and produces an outgoing
spherical wave. Far away the stationary state is (Griffiths 3e Eq. 10.12, p.481)
$$\psi(\mathbf r)\;\simeq\;A\!\left[\,e^{ikz}+f(\theta)\,\frac{e^{ikr}}{r}\,\right],
\qquad k=\frac{\sqrt{2mE}}{\hbar}.$$
The $1/r$ is forced by probability conservation (the flux through a sphere is
$r$-independent). All the physics is in $f(\theta)$: matching the incident flux to
the scattered flux through area $d\sigma = |f|^2 d\Omega$ gives the central result
(Griffiths Eq. 10.14, p.481)
$$\boxed{\;\frac{d\sigma}{d\Omega}=|f(\theta)|^2\;}$$
and the **total cross-section** is its angular integral,
$$\sigma=\int|f(\theta)|^2\,d\Omega=\int_0^{2\pi}\!\!\int_0^\pi|f|^2\sin\theta\,d\theta\,d\phi.$$
The differential cross-section is what the experimentalist measures; $f$ is what
the Schrödinger equation delivers. The classical version of this whole setup —
impact parameter $b$, scattering angle $\theta$, $d\sigma/d\Omega=(b/\sin\theta)|db/d\theta|$
— is `~CM-08` (Griffiths §10.1.1, p.477). *(`differential_cross_section`,
`total_cross_section`; verified equal via $\int|f|^2d\Omega=\sigma$ in
`test_integrated_dcs_equals_total_cross_section`.)*

## 2. Partial-wave analysis

For a spherically symmetric $V(r)$, angular momentum is conserved, so each value
of $\ell$ scatters independently. Expanding in Legendre polynomials
$P_\ell(\cos\theta)$ (the $m=0$ spherical harmonics of `~QM-10`), Griffiths
Eqs. 10.25–10.27 (p.486) give
$$f(\theta)=\frac1k\sum_{\ell=0}^{\infty}(2\ell+1)\,a_\ell\,P_\ell(\cos\theta),
\qquad
\sigma=4\pi\sum_{\ell=0}^{\infty}(2\ell+1)\,|a_\ell|^2,$$
where $a_\ell$ is the **partial-wave amplitude**. The total cross-section is a bare
*sum* of partial contributions because the $P_\ell$ are orthogonal — the cross
terms integrate to zero (Griffiths uses Eq. 4.34). The job reduces to finding the
$a_\ell$, by solving the radial equation inside the target and matching to the
exterior, where the solution is a combination of spherical Bessel functions
$j_\ell, n_\ell$ (the radiation-zone forms of `~MA-12`/`~QM-12`).

## 3. Phase shifts

Because each partial wave scatters without change of amplitude (unitarity) — only
of phase — the complex $a_\ell$ collapses to one real number, the **phase shift**
$\delta_\ell$ (Griffiths §10.3, p.490). The connection is (Griffiths Eq. 10.46–10.48,
p.491)
$$a_\ell=\frac1k\,e^{i\delta_\ell}\sin\delta_\ell,$$
$$\boxed{\;f(\theta)=\frac1k\sum_{\ell=0}^{\infty}(2\ell+1)\,e^{i\delta_\ell}\sin\delta_\ell\,P_\ell(\cos\theta)\;}$$
$$\boxed{\;\sigma=\frac{4\pi}{k^2}\sum_{\ell=0}^{\infty}(2\ell+1)\sin^2\delta_\ell\;}$$
Each partial cross-section $\sigma_\ell=(4\pi/k^2)(2\ell+1)\sin^2\delta_\ell$ is
bounded by $4\pi(2\ell+1)/k^2$ (the **unitarity bound**, saturated at
$\delta_\ell=\pi/2$ — a resonance). *(`partial_wave_amplitude`,
`total_cross_section`, `partial_cross_section`; `test_unitarity_bound`.)*

**Hard sphere** ($V=\infty$ for $r<a$). The exterior wave must vanish at $r=a$
(Dirichlet), giving (Griffiths Example 10.3 / Problem 10.6)
$$\tan\delta_\ell=\frac{j_\ell(ka)}{n_\ell(ka)}.$$
For $\ell=0$, with $j_0=\sin x/x$, $n_0=-\cos x/x$, this is $\delta_0=-ka$: the wave
function is $\propto\sin\big(k(r-a)\big)$, simply pushed out by the radius. *(The
overall sign of $\delta_\ell$ follows the Neumann-function convention; only
$\sin^2\delta_\ell$ and the relative phases in $f$ are observable.
`hard_sphere_phase_shift`; `test_hard_sphere_swave_phase_shift`.)*

**The factor of 4.** At low energy ($ka\ll1$), $j_\ell\ll n_\ell$ for $\ell\ge1$,
so the $\ell=0$ term dominates and $\delta_0\approx-ka$:
$$\sigma\;\xrightarrow{\;ka\to0\;}\;\frac{4\pi}{k^2}\sin^2(ka)\approx4\pi a^2.$$
This is **four times** the classical geometric shadow $\pi a^2$ (Griffiths
Eq. 10.36, p.488): a long-wavelength wave diffracts around the *whole* surface,
not just the head-on disc. *(`test_hard_sphere_low_energy_4pi_a2`,
`test_hard_sphere_swave_dominates_at_low_energy`.)*

**Spherical square well** ($V=-V_0$ for $r<a$). The interior solution regular at
the origin is $j_\ell(k_{\rm in}r)$ with $k_{\rm in}=\sqrt{k^2+V_0}$ (using
$\hbar=2m=1$). Matching the logarithmic derivative $R'/R$ to the exterior
$\cos\delta_\ell\,j_\ell(kr)-\sin\delta_\ell\,n_\ell(kr)$ at $r=a$ gives, with
$L=(k_{\rm in}a)\,j_\ell'(k_{\rm in}a)/j_\ell(k_{\rm in}a)$,
$$\tan\delta_\ell=\frac{L\,j_\ell(ka)-(ka)\,j_\ell'(ka)}{L\,n_\ell(ka)-(ka)\,n_\ell'(ka)}.$$
For $\ell=0$ this reduces to the closed form
$\delta_0=-ka+\arctan\!\big[(k/k_{\rm in})\tan(k_{\rm in}a)\big]$. The Dirichlet
limit $L\to\infty$ recovers the hard sphere. *(`square_well_phase_shift`;
`test_square_well_swave_closed_form`, `test_square_well_dirichlet_limit_is_hard_sphere`.)*

## 4. The optical theorem

Set $\theta=0$ in the partial-wave $f$: every $P_\ell(1)=1$, and
$\operatorname{Im}\!\big(e^{i\delta_\ell}\sin\delta_\ell\big)=\sin^2\delta_\ell$, so
$\operatorname{Im}f(0)=\frac1k\sum(2\ell+1)\sin^2\delta_\ell$. Comparing with $\sigma$
above gives the **optical theorem** (Griffiths Problem 10.19, p.504)
$$\boxed{\;\sigma_{\rm tot}=\frac{4\pi}{k}\,\operatorname{Im}f(0)\;}$$
Total scattering removes flux from the forward beam; that removal *is* destructive
interference between the incident wave and the forward-scattered wave, so the
forward amplitude must have an imaginary part proportional to the total
cross-section. It is an exact identity between the two formulas of §3, verified to
machine precision for both potentials in
`test_optical_theorem_hard_sphere` and `test_optical_theorem_square_well`.

## 5. The Born approximation

Partial waves are exact but laborious, and useless at high energy (many $\ell$
contribute). For a **weak** potential there is a shortcut. Writing the Schrödinger
equation in its integral (Green's-function) form and approximating the wave inside
the integral by the *unperturbed* incident plane wave gives the **first Born
approximation** (Griffiths §10.4.2, Eq. 10.79, p.499)
$$\boxed{\;f(\theta)=-\frac{m}{2\pi\hbar^2}\int e^{i\mathbf q\cdot\mathbf r}\,V(\mathbf r)\,d^3r\;},
\qquad \mathbf q=\mathbf k_0-\mathbf k,\quad q=|\mathbf q|=2k\sin\tfrac\theta2.$$
This is nothing but **first-order perturbation theory** (`~QM-15`): $f$ is
proportional to the matrix element of $V$ between the incoming and outgoing plane
waves, i.e. the **Fourier transform of the potential** evaluated at the momentum
transfer $\hbar\mathbf q$ (Griffiths Eq. 10.89, p.500). For a spherically
symmetric $V$ the angular integrals reduce it to (Eq. 10.88)
$$f(\theta)=-\frac{2m}{\hbar^2 q}\int_0^\infty r\,V(r)\sin(qr)\,dr.$$

**Yukawa potential** $V(r)=\beta\,e^{-\mu r}/r$ (a screened Coulomb / nuclear
model). The integral is elementary (Griffiths Example 10.5, Eq. 10.91, p.500):
$$\boxed{\;f(\theta)=-\frac{2m\beta}{\hbar^2}\,\frac{1}{\mu^2+q^2}\;}$$
The screening length $1/\mu$ keeps $f$ **finite in the forward direction**
($f(0)=-2m\beta/\hbar^2\mu^2$); it is **forward-peaked**, falling monotonically as
$q$ grows from $0$ to $2k$. *(`born_amplitude_yukawa`, and `born_amplitude_radial`
which does the integral numerically — verified equal in
`test_born_yukawa_closed_form`; peaking in `test_born_forward_peaking`.)*

**Rutherford / Coulomb limit.** Let $\mu\to0$ and $\beta\to q_1q_2/4\pi\varepsilon_0$:
$$\frac{d\sigma}{d\Omega}=|f|^2=\left(\frac{2m\beta}{\hbar^2}\right)^2\frac1{q^4}
=\left(\frac{\beta}{4E}\right)^2\frac1{\sin^4(\theta/2)},$$
the **Rutherford formula** (Griffiths Example 10.6, Eq. 10.93, p.501). The forward
amplitude now diverges — the infinite range of $1/r$. Remarkably this is the
*identical* $d\sigma/d\Omega$ that classical mechanics gives in `~CM-08`:
classical mechanics, the Born approximation, and QED all agree for the Coulomb
potential. *(`rutherford_cross_section`; `test_born_rutherford_limit`,
`test_yukawa_screening_regularizes_forward`.)*

---
### Where this sits in the trunk
Scattering is where the abstract apparatus of the trunk pays off:
- the **partial waves** are the Legendre/spherical-harmonic machinery of `~QM-10`
  put to work on a continuum (unbound, $E>0$) problem;
- the **Born approximation** is `~QM-15` first-order perturbation theory in the
  plane-wave basis — the Fourier transform of $V$;
- the **classical limit** is `~CM-08` (Rutherford, geometric cross-sections), with
  the factor-of-4 hard-sphere result the cleanest place to see wave optics depart
  from particle mechanics;
- forward references: `~QM-12` (the radial equation / spherical Bessel functions
  reused here), and the field-theory cross-section (`~QF-01`) where $f$ becomes a
  scattering matrix element.
The lesson: *one complex function $f(\theta)$ stands between the potential and the
detector, and there are two complementary ways to compute it.*
