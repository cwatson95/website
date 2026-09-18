# EM-16 — Waveguides, Cavities & Transmission Lines (notes)

A waveguide is what a plane wave (`~EM-15`) becomes when you **confine** it.
Maxwell's equations are unchanged, but the conducting walls impose boundary
conditions the free wave never felt, and the result is a discrete spectrum of
**modes**, each with a frequency floor (its *cutoff*) and its own dispersion. This
module sets up the guided-wave problem, solves the rectangular guide, reads off its
dispersion, and contrasts all of it with the cutoff-free TEM line.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page
numbers are the *printed* book pages. The guide axis is $z$; $a$ and $b$ are the
cross-section dimensions with $a\ge b$.

## 1. Guided waves & boundary conditions
Look for a monochromatic wave travelling down the guide (Gr §9.5.1, p.425). Every
field rides the same axial factor, with a transverse profile fixed by the
cross-section:
$$\mathbf E(x,y,z,t)=\mathbf E_0(x,y)\,e^{i(kz-\omega t)},\qquad
  \mathbf B(x,y,z,t)=\mathbf B_0(x,y)\,e^{i(kz-\omega t)} .$$
Feeding this into the wave equation, the **longitudinal** components $E_z$, $B_z$
each obey a 2-D Helmholtz equation,
$$\left[\frac{\partial^2}{\partial x^2}+\frac{\partial^2}{\partial y^2}
  +\left(\frac{\omega^2}{c^2}-k^2\right)\right]E_z=0,$$
with the identical equation for $B_z$; the transverse components are then algebraic
in $E_z$, $B_z$. At the conducting walls $E^{\parallel}=0$ and $B^{\perp}=0$. Modes
split by which longitudinal field survives: **TE** ($E_z=0$), **TM** ($B_z=0$),
and **TEM** ($E_z=B_z=0$). A *hollow* (single-conductor) guide admits **no** TEM
mode — that one needs two conductors (§4).

## 2. TE modes in a rectangular guide; the cutoff ω_mn
Take a rectangular guide and solve the $B_z$ Helmholtz equation by separation of
variables (Gr §9.5.2, p.428). The wall conditions quantize the transverse
wavenumbers to $k_x=m\pi/a$, $k_y=n\pi/b$ (integers $m,n$), so
$$k=\sqrt{\frac{\omega^2}{c^2}-\pi^2\!\left(\frac{m^2}{a^2}+\frac{n^2}{b^2}\right)} .$$
The wave propagates only while $k$ is real; the borderline $k=0$ defines the
**cutoff** angular frequency
$$\boxed{\;\omega_{mn}=c\pi\sqrt{\left(\tfrac{m}{a}\right)^2+\left(\tfrac{n}{b}\right)^2}\;}
  \qquad(\text{Eq. 9.186}).$$
Code: `cutoff_angular_frequency(m,n,a,b)`, and `cutoff_frequency` for
$f_{mn}=\omega_{mn}/2\pi$. Because $a\ge b$, the smallest cutoff is the
**dominant** $\mathrm{TE}_{10}$ mode,
$$\omega_{10}=\frac{c\pi}{a}\qquad\Bigl(f_{10}=\frac{c}{2a}\Bigr),$$
returned by `dominant_mode_cutoff(a,b)`. ($\mathrm{TE}_{00}$ has no field, so it
does not count.) The ordering $\omega_{10}<\omega_{20},\omega_{01},\omega_{11}$ is
checked in the tests.

## 3. Guide dispersion; v_p · v_g = c²
Rewrite the wavenumber in terms of the cutoff:
$$k=\frac{1}{c}\sqrt{\omega^2-\omega_{mn}^2} .$$
For $\omega>\omega_{mn}$, $k$ is real and the mode **propagates** —
`guide_wavenumber(omega, omega_co)` (it returns `0.0` at/below cutoff). For
$\omega<\omega_{mn}$, $k$ turns imaginary: the mode is **evanescent**, $\sim
e^{-\kappa z}$ with $\kappa=\frac{1}{c}\sqrt{\omega_{mn}^2-\omega^2}$
(`evanescent_decay`), carrying no power and dissipating nothing. The threshold
itself is `is_propagating`. Above cutoff the guide is **dispersive**, with
$$v_p=\frac{\omega}{k}=\frac{c}{\sqrt{1-(\omega_{mn}/\omega)^2}}>c,\qquad
  v_g=\frac{d\omega}{dk}=c\,\sqrt{1-\Bigl(\tfrac{\omega_{mn}}{\omega}\Bigr)^2}<c .$$
Differentiating $\omega^2=c^2k^2+\omega_{mn}^2$ gives $v_g=c^2k/\omega=c^2/v_p$, i.e.
$$\boxed{\,v_p\,v_g=c^2\,}.$$
Code: `phase_velocity_guide`, `group_velocity_guide`. The superluminal $v_p$ breaks
no rule — a single sinusoid carries no information; the **signal/energy** speed is
$v_g<c$. Far above cutoff $(\omega\gg\omega_{mn})$ both tend to $c$ and the free
plane wave of `~EM-15` is recovered.

## 4. The coaxial transmission line / TEM mode
A line with **two** conductors — a coax (inner wire + outer shield) — supports the
**TEM** mode that the hollow guide forbids (Gr §9.5.3, p.431). With $E_z=B_z=0$ the
Helmholtz constant must vanish, $\omega^2/c^2-k^2=0$, so
$$k=\frac{\omega}{c}\qquad(\text{no cutoff}).$$
The dispersion is exactly that of free space: **every** frequency, down to DC,
propagates at $c$ (vacuum dielectric), and the transverse fields are an
electrostatic-like pattern (**E** radial, **B** azimuthal between the conductors).
This is why coax and transmission lines carry broadband and baseband signals where
a hollow guide would impose a floor. Code: `tem_line_speed()` returns $c$.

## Where this goes
- `~EM-15` — the $\omega\gg\omega_{mn}$ limit *is* the free plane wave; a guide just
  adds a cutoff to it, and the TEM line keeps the free wave intact.
- `~MA-08` — the transverse problem is a 2-D Helmholtz eigenvalue problem solved by
  separation of variables; the cutoffs $\omega_{mn}$ are its eigenvalues.
- `~QO-01` — counting and quantizing these guide/cavity modes gives the photon
  modes of quantized light (one harmonic oscillator per mode).
- `~PK-03` — the guide dispersion $\omega^2=\omega_{mn}^2+c^2k^2$ is identical in
  form to the cold-plasma EM wave $\omega^2=\omega_p^2+c^2k^2$, with the cutoff
  $\omega_{mn}$ playing the role of the plasma frequency $\omega_p$.
