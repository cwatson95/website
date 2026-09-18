# PK-03 — Plasma Waves & Instabilities — Langmuir, Ion-Acoustic, Landau Damping (notes)

A plasma is a medium full of free charges, so it answers every push with collective
electric fields. Displace the electrons and they ring at the **plasma frequency**;
let that ringing propagate and you get **Langmuir waves**; let the ions sway under
electron pressure and you get **ion-acoustic waves**. Two things have no analogue in
ordinary acoustics: **Landau damping**, a collisionless loss to particles that surf
the wave, and **instabilities** such as the **two-stream** mode, where free streaming
energy feeds the wave instead. The first two are fluid (`~PK-02`, `~CM-23`); the last
two need the kinetic (Vlasov) picture of `~PK-01` and the Landau contour of `~MA-06`.

Citation key (full details in `refs.md`): **M** = Michel, *Introduction to
Laser-Plasma Interactions* — cited at section level (Ch. 1 and Formulary A).

## 1. The two scales: plasma frequency and Debye length
Pull a slab of electrons aside; the restoring field $E=ne x/\varepsilon_0$ gives
$\ddot x=-\omega_p^2 x$, simple harmonic motion (`~CM-15`) at the **plasma
frequency** [M §1.2.2]
$$\omega_p=\sqrt{\frac{n e^2}{\varepsilon_0 m_e}}.$$
Thermal motion limits how far that field reaches: a charge is screened beyond the
**Debye length** [M §1.2.1], one thermal step per plasma period,
$$\lambda_D=\sqrt{\frac{\varepsilon_0 k_B T}{n e^2}}=\frac{v_{th}}{\omega_p},
\qquad v_{th}=\sqrt{\frac{k_B T}{m}}.$$
Code: `plasma_frequency`, `debye_length`, `thermal_speed`. Every dispersion below is
naturally written in the dimensionless wavenumber $k\lambda_D$.

## 2. Langmuir / electron plasma waves (Bohm–Gross)
A cold electron oscillation does not propagate ($\omega=\omega_p$ for all $k$). Warm
electrons carry a **pressure** force; the 1-D adiabatic closure ($\gamma=3$, one
compressional degree of freedom) adds the **Bohm–Gross** term [M §1.3.1.4]:
$$\boxed{\;\omega^2=\omega_p^2+3k^2v_{th}^2=\omega_p^2\big(1+3k^2\lambda_D^2\big)\;}$$
so $\omega\to\omega_p$ as $k\to0$ (the cold cutoff) and the group velocity
$d\omega/dk$ turns on only for warm, short-wavelength waves. Code: `bohm_gross`.

## 3. Ion-acoustic waves
Now let the ions move. On slow timescales the light electrons stay in Boltzmann
equilibrium and supply a pressure $\sim k_BT_e$, while the heavy ions supply the
inertia — a sound wave with the plasma **sound speed** $c_s=\sqrt{k_BT_e/m_i}$
[M §1.3.1.5]:
$$\boxed{\;\omega=\frac{k\,c_s}{\sqrt{1+k^2\lambda_D^2}}\;},\qquad
c_s=\sqrt{\frac{k_BT_e}{m_i}}.$$
For $k\lambda_D\ll1$ this is non-dispersive sound, $\omega\simeq k c_s$; for
$k\lambda_D\gg1$ it saturates at the ion plasma frequency
$\omega_{pi}=c_s/\lambda_D$. Because $c_s/v_{th,e}=\sqrt{m_e/m_i}\ll1$, ion-acoustic
waves are far slower than Langmuir waves. Code: `ion_acoustic`.

## 4. The kinetic origin: dielectric function and the Landau contour
Both branches are real roots of the plasma **dielectric function** $\varepsilon(k,\omega)=0$.
For the 1-D Vlasov plasma (`~PK-01`) with normalized $f_0(v)$ [M §1.3.3]
$$\varepsilon(k,\omega)=1-\frac{\omega_p^2}{k^2}\int_{L}
\frac{\partial_v f_0(v)}{\,v-\omega/k\,}\,dv=0 .$$
The integrand has a **pole at the phase velocity** $v=\omega/k$; Landau showed the
contour $L$ must pass *below* it (the causal/initial-value prescription), an exercise
in contour integration (`~MA-06`). The principal-value (real) part reproduces
Bohm–Gross in §2; the pole contributes an **imaginary** part — Landau damping.

## 5. Landau damping
Splitting $\varepsilon=\varepsilon_r+i\varepsilon_i$ and writing
$\omega=\omega_r+i\gamma$ with $|\gamma|\ll\omega_r$ gives
$\gamma=-\varepsilon_i/(\partial\varepsilon_r/\partial\omega)$, and the pole's
residue makes the growth rate proportional to the **slope of $f_0$ at resonance**:
$$\gamma=\frac{\pi}{2}\,\frac{\omega_p^{3}}{k^{2}}\,
\left.\frac{\partial f_0}{\partial v}\right|_{v=\omega/k}.$$
Resonant particles slightly slower than the wave gain energy, slightly faster ones
lose it; a **falling** $f_0$ (more slow than fast, $\partial_v f_0<0$) means net
energy *to* the particles, so $\gamma<0$ — collisionless damping with no entropy
production. For a Maxwellian this evaluates to the standard closed form
[M §1.3.4, Formulary A.4]
$$\frac{\gamma}{\omega_p}=-\sqrt{\frac{\pi}{8}}\,\frac{1}{(k\lambda_D)^{3}}\,
\exp\!\left(-\frac{1}{2(k\lambda_D)^{2}}-\frac{3}{2}\right)<0.$$
It is exponentially weak when $k\lambda_D\ll1$ (the resonance $v=\omega/k\approx
v_{th}/k\lambda_D$ sits far out on the tail, where almost no particles live) and
strengthens as $k\lambda_D\to1$. Code: `landau_damping_rate`. A *rising* slope
(a beam, $\partial_v f_0>0$) flips the sign — growth — which is the next section.

## 6. Two-stream instability
Replace the Maxwellian by two **counter-streaming cold beams** at $\pm v_0$ (a
double bump: positive slope between them). Each beam (density $n/2$) adds a cold
susceptibility $-\tfrac12\omega_p^2/(\omega\mp kv_0)^2$, so $\varepsilon=0$ reads
$$1=\frac{\omega_p^2}{2}\left[\frac{1}{(\omega-kv_0)^2}+\frac{1}{(\omega+kv_0)^2}\right].$$
Cleared of denominators this is a bi-quadratic, $\omega^4-(2a+\omega_p^2)\omega^2+
(a^2-\omega_p^2a)=0$ with $a=(kv_0)^2$, whose lower root can go **negative**:
$$\omega^2=\tfrac12\Big[(2a+\omega_p^2)-\omega_p\sqrt{8a+\omega_p^2}\Big]<0
\quad\Longleftrightarrow\quad kv_0<\omega_p,$$
giving a purely growing mode $\omega=i\gamma$. Maximizing over $k$, the **peak
growth rate** is
$$\gamma_{\max}=\frac{\omega_p}{\sqrt 8}\quad\text{at}\quad kv_0=\sqrt{\tfrac38}\,\omega_p .$$
The free streaming energy of the beams feeds the wave; the instability is the time-
reversed, opposite-sign cousin of Landau damping. Code solves the quartic
numerically with `numpy.roots`: `two_stream_growth_rate` returns $\mathrm{Im}\,\omega$
(zero outside the band $kv_0<\omega_p$).

## Where this goes
- `~PK-01` — the Vlasov equation and $f_0(v)$ behind the dielectric function and Landau's contour (the KrF/LoKI kinetic code in this repo).
- `~CM-15` / `~CM-25` — the plasma frequency is an oscillator (`~CM-15`) and these are dispersive waves in a medium (`~CM-25`, `~EM-15`).
- `~MA-06` — the Landau contour is a residue/branch-cut computation in complex analysis.
- `~PK-02` / `~CM-23` — the fluid (moment) limit gives Bohm–Gross and ion-acoustic without the kinetic damping; the two are reconciled by `~PK-01`.
