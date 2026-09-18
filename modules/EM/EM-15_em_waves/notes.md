# EM-15 — Electromagnetic Waves (notes)

A wave is what Maxwell's equations `~EM-13` do when nobody is pushing them: in
empty space the coupled curl laws feed back on each other and the fields
**propagate**. This module takes that wave equation, builds its simplest
solution — the monochromatic transverse plane wave — and follows it into matter
and across an interface.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e.
Page numbers are the *printed* book pages. The propagation direction is the unit
vector **k̂**; the speed of light is $c=1/\sqrt{\mu_0\varepsilon_0}$ (code: `C`,
assembled from `~EM-01` `EPS0` and `~EM-08` `MU0`).

## 1. The wave equation and dispersion
Taking the curl of Faraday's law and using Ampère–Maxwell in vacuum decouples the
fields: each Cartesian component of **E** and **B** obeys the **wave equation**
(Gr §9.1.1, Eq. 9.2, p.382):
$$\frac{\partial^2 f}{\partial t^2}=v^{2}\nabla^{2} f .$$
Griffiths writes the 1-D form $\partial^2 f/\partial x^2=(1/v^2)\,\partial^2 f/\partial t^2$;
the code keeps the Laplacian so it reads in any dimension. Every $f(z-vt)$ is a
solution; the **sinusoidal** ones (Gr §9.1.2, p.385) are
$$f(z,t)=A\cos(kz-\omega t+\delta),\qquad \boxed{\;\omega = v\,k\;}$$
with wavenumber $k=2\pi/\lambda$, angular frequency $\omega$, and phase velocity
$v=\omega/k$. The boxed **dispersion relation** $\omega=vk$ is the whole content
of "it is a wave." Code: `scalar_plane_wave(k, omega)` builds $\cos(kz-\omega t)$;
`wave_equation_residual(f, v, …)` forms the normalized $\partial^2 f/\partial t^2-v^2\nabla^2 f$
using the MA-02 `laplacian` (space) and a central time difference, returning $\sim0$
**iff** $\omega=vk$ and an $O(1)$ number otherwise; `wavelength(omega, v)` returns
$\lambda=2\pi v/\omega$.

## 2. Polarization
A wave travelling along $\hat{\mathbf z}$ is transverse, so **E** lives in the
$x$–$y$ plane and carries two real amplitudes plus a relative phase (Gr §9.1.4, p.391):
$$\mathbf E=\big(A_x\,\hat{\mathbf x}+A_y e^{i\delta}\,\hat{\mathbf y}\big)e^{i(kz-\omega t)} .$$
The phase difference $\delta=\text{phase}_y-\text{phase}_x$ sets the figure traced
by the real **E** over one period:
- $\delta=0$ or $\pi$ (or one amplitude zero) → **linear** (a fixed tilted line);
- $A_x=A_y$ and $\delta=\pm\pi/2$ → **circular**;
- everything else → **elliptical**.

Code: `classify_polarization(Ax, Ay, delta)` returns exactly these three labels.

## 3. Monochromatic plane waves — B locked to E
For a plane wave $\mathbf E=\mathbf E_0\,e^{i(\mathbf k\cdot\mathbf r-\omega t)}$,
$\nabla\cdot\mathbf E=0$ forces $\mathbf E_0\cdot\hat{\mathbf k}=0$ (transverse),
and Faraday's law then fixes **B** completely (Gr §9.2.2, Eq. 9.49, p.394):
$$\mathbf B_0=\frac1c\,\hat{\mathbf k}\times\mathbf E_0,\qquad
  |\mathbf B_0|=\frac{E_0}{c}.$$
So $(\hat{\mathbf E},\hat{\mathbf B},\hat{\mathbf k})$ is a right-handed triad:
**B** is perpendicular to both **E** and **k̂**, in phase with **E**, and smaller
by the factor $c$. Code: `transverse_B(E0, khat, v)` returns $(1/v)\,\hat{\mathbf k}\times\mathbf E_0$
(a single MA-01 `cross`); `is_transverse(vec, khat)` checks $\mathbf{vec}\cdot\hat{\mathbf k}=0$.
The tests confirm $|\mathbf B_0|=E_0/c$, $\mathbf E_0\cdot\mathbf B_0=0$, and that
$\mathbf B_0$ points along $+\hat{\mathbf y}$ when $\mathbf E_0\parallel\hat{\mathbf x}$,
$\mathbf k\parallel\hat{\mathbf z}$.

## 4. Energy and momentum
The wave carries energy with density $u=\varepsilon_0 E^2$ (electric and magnetic
parts are equal), and the Poynting vector $\mathbf S=(1/\mu_0)\,\mathbf E\times\mathbf B$
points along **k̂**. Time-averaging the sinusoid gives the **intensity** (Gr §9.2.3,
Eq. 9.59, p.398):
$$\langle S\rangle=\tfrac12\,c\,\varepsilon_0 E_0^{2}=c\,\langle u\rangle .$$
The wave also carries momentum density $\langle g\rangle=\langle S\rangle/c^{2}$,
so it presses on a perfect absorber with radiation pressure $\langle S\rangle/c$ —
the `~EM-14` conservation laws (Poynting's theorem) specialized to a wave. The
amplitude-squared scaling of $\langle S\rangle$ is exactly what turns the Fresnel
*amplitude* coefficients of §6 into *power* fractions (and supplies the $n_2/n_1$
in the transmittance).

## 5. Propagation in linear media
Inside a linear medium Maxwell's equations have the same form with
$\varepsilon_0\mu_0\to\varepsilon\mu$, so the wave equation survives with $c\to v$
(Gr §9.3.1, Eq. 9.68, p.401):
$$v=\frac{c}{n},\qquad n=\sqrt{\varepsilon_r\,\mu_r}\;\approx\sqrt{\varepsilon_r},$$
the **index of refraction**. Code: `refractive_index(eps_r, mu_r)` $=\sqrt{\varepsilon_r\mu_r}$,
`phase_velocity` $=c/n$. Glass with $\varepsilon_r=2.25$ gives $n=1.5$ and
$v\approx2\times10^{8}$ m/s; the frequency is unchanged across an interface, so the
wavelength shrinks by $n$.

## 6. Reflection and transmission at normal incidence
At a flat interface $n_1\to n_2$ struck head-on, matching **E** and **B** across
the boundary splits the wave into reflected and transmitted parts with **Fresnel**
amplitude coefficients (Gr §9.3.2, Eq. 9.82, p.403):
$$r=\frac{n_1-n_2}{n_1+n_2},\qquad t=\frac{2n_1}{n_1+n_2}.$$
Reflection off the **denser** medium ($n_2>n_1$) gives $r<0$ — a $\pi$ phase flip.
Converting to power with the §4 intensity:
$$R=r^{2},\qquad T=\frac{n_2}{n_1}\,t^{2},\qquad \boxed{\;R+T=1\;}$$
(energy conservation, no absorption). Code: `fresnel_normal(n1, n2)` → $(r,t)$;
`reflectance` $=r^2$; `transmittance` $=(n_2/n_1)t^2$. Air → glass reflects
$R=0.04$ — the familiar 4 % per glass surface — and the reflectance is identical
in both directions even though the sign of $r$ flips.

## Where this goes
- `~EM-16` confines the wave between conductors: boundary conditions quantize it
  into discrete **guided modes** with a cutoff frequency (waveguides & cavities).
- `~EM-17` puts a **source** behind it — an accelerating charge — whose far-zone
  radiation field is, locally, one of these plane waves.
- `~MA-09` (Fourier) superposes monochromatic plane waves into pulses and wave
  packets — `KEY BRIDGE B9` (the same spectral idea as CM-16, QM-08).
- `~QO-01` **quantizes** each mode: the classical plane wave becomes a harmonic
  oscillator whose excitations are photons.
