# EM-16 — Problems

Work by hand, then check with `code/waveguides.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  Cutoffs of a rectangular guide  *(Gr §9.5.2, Eq. 9.186, p.428)*
For a guide of cross-section $a\times b$ with $a\ge b$, show the $\mathrm{TE}_{mn}$
cutoff is $\omega_{mn}=c\pi\sqrt{(m/a)^2+(n/b)^2}$, and that the lowest is the
dominant $\mathrm{TE}_{10}$ with $\omega_{10}=c\pi/a$, i.e. $f_{10}=c/2a$. For
WR-90 ($a=22.9$ mm, $b=10.2$ mm) evaluate $f_{10}$ (expect $\approx 6.55$ GHz).
*Check:* `cutoff_angular_frequency(1,0,a,b)`, `cutoff_frequency(1,0,a,b)`, and
`dominant_mode_cutoff(a,b)` (which orders $a,b$ for you).

**Solution.** Separation of variables on the $B_z$ Helmholtz equation gives a
transverse profile $\cos(k_x x)\cos(k_y y)$; the wall conditions quantize
$k_x=m\pi/a$, $k_y=n\pi/b$. Propagation needs real $k$ in
$k=\sqrt{\omega^2/c^2-k_x^2-k_y^2}$, and $k=0$ marks the cutoff:
$$\omega_{mn}=c\sqrt{k_x^2+k_y^2}=c\pi\sqrt{\left(\tfrac{m}{a}\right)^2+\left(\tfrac{n}{b}\right)^2}.$$
With $a\ge b$, the smallest nonzero cutoff is $(m,n)=(1,0)$, giving
$\omega_{10}=c\pi/a$ and $f_{10}=\omega_{10}/2\pi=c/2a$. For WR-90,
$f_{10}=\dfrac{2.998\times10^8}{2(0.0229)}=6.55\text{ GHz}$ — exactly what
`cutoff_frequency(1,0,a,b)` and `dominant_mode_cutoff(a,b)/2\pi` return ($6.546$ GHz,
$\omega_{10}=4.113\times10^{10}$ rad/s).

### P2.  Single-mode (dominant-mode) bandwidth  *(Gr §9.5.2, p.428)*
Take $a=2b$. Show $\omega_{20}=2\omega_{10}$ and $\omega_{01}=c\pi/b=2\omega_{10}$,
so above $\omega_{10}$ the guide carries **only** $\mathrm{TE}_{10}$ until
$2\omega_{10}$, where $\mathrm{TE}_{20}$ and $\mathrm{TE}_{01}$ switch on together —
a one-octave single-mode band. *Check:* compare `cutoff_angular_frequency` for
$(1,0),(2,0),(0,1)$, and use `is_propagating(1.5*w10, m, n, a, b)` to confirm only
$\mathrm{TE}_{10}$ propagates at $\omega=1.5\,\omega_{10}$.

**Solution.** With $a=2b$ substitute into $\omega_{mn}=c\pi\sqrt{(m/a)^2+(n/b)^2}$:
$$\omega_{10}=\frac{c\pi}{a},\quad \omega_{20}=\frac{2c\pi}{a}=2\omega_{10},\quad
\omega_{01}=\frac{c\pi}{b}=\frac{c\pi}{a/2}=\frac{2c\pi}{a}=2\omega_{10}.$$
So nothing else turns on between $\omega_{10}$ and $2\omega_{10}$: only
$\mathrm{TE}_{10}$ carries power across that octave, and at $2\omega_{10}$ the
degenerate $\mathrm{TE}_{20}$ and $\mathrm{TE}_{01}$ switch on together. Numerically
(with $a=2b$) the code gives $\omega_{20}/\omega_{10}=\omega_{01}/\omega_{10}=2.0$,
and at $\omega=1.5\,\omega_{10}$ `is_propagating` is `True` for $(1,0)$ but `False`
for $(2,0)$ and $(0,1)$ — confirming the single-mode band.

### P3.  Dispersion and evanescence about cutoff  *(Gr §9.5.2, Eq. 9.186, p.428)*
For a mode of cutoff $\omega_{co}$ driven at $\omega$, show
$k=\frac{1}{c}\sqrt{\omega^2-\omega_{co}^2}$ when $\omega>\omega_{co}$, and that for
$\omega<\omega_{co}$ the field decays as $e^{-\kappa z}$ with
$\kappa=\frac{1}{c}\sqrt{\omega_{co}^2-\omega^2}$ — no propagation, no dissipation.
At $\omega=\tfrac12\omega_{co}$ find $\kappa$ (expect $\tfrac{\sqrt3}{2}\,
\omega_{co}/c\approx 0.866\,\omega_{co}/c$). *Check:* `guide_wavenumber` returns 0
below cutoff and positive above; `evanescent_decay` is positive below cutoff and 0
above; `is_propagating` marks the threshold.

**Solution.** The longitudinal wavenumber follows from $\omega^2/c^2=k^2+(\omega_{co}/c)^2$,
i.e. $k=\frac1c\sqrt{\omega^2-\omega_{co}^2}$. For $\omega>\omega_{co}$ this is real and
the mode propagates as $e^{i(kz-\omega t)}$. For $\omega<\omega_{co}$ the radicand goes
negative, $k=i\kappa$ with
$$\kappa=\frac1c\sqrt{\omega_{co}^2-\omega^2},$$
so $e^{ikz}=e^{-\kappa z}$ — pure exponential decay, no oscillation and (since $\kappa$
is real, not complex) no Joule loss. At $\omega=\tfrac12\omega_{co}$,
$\kappa=\frac1c\sqrt{\omega_{co}^2-\tfrac14\omega_{co}^2}=\frac{\sqrt3}{2}\frac{\omega_{co}}{c}\approx0.866\,\omega_{co}/c$.
The code confirms `guide_wavenumber`$=0$ below cutoff while `evanescent_decay`$=288.87$
m⁻¹ $=0.866\,\omega_{co}/c$ (for $\omega_{co}=10^{11}$ rad/s).

### P4.  Phase and group velocity; v_p · v_g = c²  *(Gr §9.5.2, p.428)*
From $k=\frac{1}{c}\sqrt{\omega^2-\omega_{co}^2}$ derive
$v_p=\omega/k=c/\sqrt{1-(\omega_{co}/\omega)^2}$ and (differentiating
$\omega^2=c^2k^2+\omega_{co}^2$) $v_g=d\omega/dk=c\sqrt{1-(\omega_{co}/\omega)^2}$.
Hence $v_p>c>v_g$ and $v_p\,v_g=c^2$. Explain why $v_p>c$ violates no relativity (a
single sinusoid carries no information) while $v_g$ is the energy/signal speed, and
show both $\to c$ as $\omega\gg\omega_{co}$. *Check:* `phase_velocity_guide` and
`group_velocity_guide` — confirm their product equals `C**2` and that each tends to
`C` for $\omega\gg\omega_{co}$.

**Solution.** The phase velocity is $v_p=\omega/k=\omega\big/\frac1c\sqrt{\omega^2-\omega_{co}^2}
=\dfrac{c}{\sqrt{1-(\omega_{co}/\omega)^2}}$, which exceeds $c$. Differentiating the
dispersion $\omega^2=c^2k^2+\omega_{co}^2$ gives $2\omega\,d\omega=2c^2k\,dk$, so
$$v_g=\frac{d\omega}{dk}=\frac{c^2k}{\omega}=\frac{c^2}{v_p}=c\sqrt{1-(\omega_{co}/\omega)^2}<c.$$
Their product is $v_p v_g=c^2$ identically. The superluminal $v_p$ is the speed of a
pure phase front, which carries no information; energy and signals travel at
$v_g<c$, so relativity is safe. As $\omega\gg\omega_{co}$ the radical $\to1$ and both
$\to c$. The code confirms $v_p v_g=8.988\times10^{16}=$`C**2`, and at $\omega=100\,\omega_{co}$
both velocities sit within $10^{-4}$ of `C`.

### P5.  The coaxial line / TEM mode — no cutoff  *(Gr §9.5.3, p.431)*
Argue that a hollow single-conductor guide cannot carry a TEM ($E_z=B_z=0$) wave,
but a coax (two conductors) can; show the TEM mode obeys the free-space dispersion
$\omega=ck$ (the Helmholtz constant vanishes), so a coax passes **every** frequency,
down to DC, at $c$ in a vacuum dielectric. Contrast with the cutoff of P3.
*Check:* `tem_line_speed()` returns `C`; compare with `phase_velocity_guide` /
`group_velocity_guide`, which only approach `C` in the $\omega\gg\omega_{co}$ limit.

**Solution.** A TEM mode has $E_z=B_z=0$, so the transverse field obeys
$\nabla\cdot\mathbf E_\perp=0$ and $\nabla\times\mathbf E_\perp=0$ in the cross-section — an
*electrostatic* pattern, the gradient of a potential solving Laplace's equation there. Inside a
single hollow conductor the wall is one connected equipotential, forcing the potential constant
and $\mathbf E_\perp=0$: a hollow guide carries **no** TEM wave. A coax has *two* conductors at
different potentials, so a nontrivial radial $\mathbf E$ (and azimuthal $\mathbf B$) lives between
them. Setting $E_z=B_z=0$ also kills the Helmholtz constant, $\omega^2/c^2-k^2=0$, so
$$k=\frac{\omega}{c}\quad\Longrightarrow\quad\omega=ck\qquad(\text{no cutoff}),$$
the free-space dispersion: every frequency, down to DC, travels at $c$. This is the opposite of
P3's guided mode, where $\omega^2/c^2-k^2=k_c^2>0$ imposes a cutoff. Hence `tem_line_speed()`$=c=
2.998\times10^8$ m/s at all frequencies, whereas `phase_velocity_guide`/`group_velocity_guide` only
approach $c$ in the $\omega\gg\omega_{co}$ limit.
