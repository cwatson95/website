# EM-13 — Problems

Work by hand, then check with `code/maxwell_equations.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  Displacement current in a charging capacitor  *(Gr §7.3.2, p.334)*
A parallel-plate capacitor charges so that the uniform field between the plates grows at
$\partial E/\partial t$ (no medium, $\hat{\mathbf x}$ across the gap). There is **no conduction
current** between the plates, yet Ampère–Maxwell still gives a circulating **B**. Show it is
supplied entirely by the displacement current
$$\mathbf J_d=\varepsilon_0\,\frac{\partial\mathbf E}{\partial t},$$
and evaluate $|\mathbf J_d|$ for $\partial E/\partial t = 10^{12}\ \mathrm{V/m/s}$.
*Check:* `displacement_current_density((1e12, 0, 0))` returns $\varepsilon_0\cdot10^{12}\approx
8.85\ \mathrm{A/m^2}$ for the $x$-component.

**Solution.** Between the plates the conduction current is zero, so Ampère–Maxwell keeps only
the displacement term: $\nabla\times\mathbf B=\mu_0\varepsilon_0\,\partial\mathbf E/\partial t=\mu_0\mathbf J_d$
with $\mathbf J_d=\varepsilon_0\,\partial\mathbf E/\partial t$ — the changing field is the *sole* source
of the circulating **B**. Its magnitude follows directly:
$$|\mathbf J_d|=\varepsilon_0\left|\frac{\partial E}{\partial t}\right|
=(8.854\times10^{-12}\ \mathrm{F/m})(10^{12}\ \mathrm{V/m/s})=8.854\ \mathrm{A/m^2}.$$
So `displacement_current_density((1e12,0,0))` returns $(8.854,0,0)$ — the $x$-component
$\varepsilon_0\cdot10^{12}=8.854\ \mathrm{A/m^2}$, the displacement current that closes Ampère's loop.

### P2.  Why Ampère's law needed fixing — the divergence test  *(Gr §7.3.2, p.334)*
Take the divergence of the **uncorrected** law $\nabla\times\mathbf B=\mu_0\mathbf J$ and show
it forces $\nabla\cdot\mathbf J=0$, contradicting continuity $\partial\rho/\partial t+\nabla\cdot\mathbf J=0$
whenever charge accumulates. Then show that adding $\mathbf J_d=\varepsilon_0\,\partial\mathbf E/\partial t$
restores $\nabla\cdot(\mathbf J+\mathbf J_d)=0$ — using Gauss's law $\nabla\cdot\mathbf E=\rho/\varepsilon_0$
to turn the extra term into $\partial\rho/\partial t$. *Check:* the two laws whose consistency you
are proving are exactly the ones `gauss_E_residual` and `ampere_maxwell_residual` encode;
together they enforce $\nabla\cdot\mathbf J+\partial\rho/\partial t=0$.

**Solution.** Take the divergence of the uncorrected $\nabla\times\mathbf B=\mu_0\mathbf J$. The
left side vanishes identically, $\nabla\cdot(\nabla\times\mathbf B)=0$, so the law *forces*
$\nabla\cdot\mathbf J=0$. But continuity reads $\nabla\cdot\mathbf J=-\partial\rho/\partial t$,
nonzero wherever charge piles up (a charging capacitor plate) — a flat contradiction. Restore
consistency by adding $\mathbf J_d=\varepsilon_0\,\partial\mathbf E/\partial t$ and using Gauss
$\nabla\cdot\mathbf E=\rho/\varepsilon_0$:
$$\nabla\cdot(\mathbf J+\mathbf J_d)=\nabla\cdot\mathbf J+\varepsilon_0\frac{\partial}{\partial t}(\nabla\cdot\mathbf E)=\nabla\cdot\mathbf J+\frac{\partial\rho}{\partial t}=0.$$
Now $\nabla\cdot(\nabla\times\mathbf B)=\mu_0\nabla\cdot(\mathbf J+\mathbf J_d)=0$ holds for *any*
time-varying fields. The two laws whose consistency this proves are precisely Gauss
(`gauss_E_residual`) and Ampère–Maxwell (`ampere_maxwell_residual`); together they enforce exactly
$\nabla\cdot\mathbf J+\partial\rho/\partial t=0$.

### P3.  A plane wave satisfies all four equations  *(Gr §7.3.3, p.337)*
For $\mathbf E=E_0\cos(kz-\omega t)\,\hat{\mathbf x}$ and $\mathbf B=(E_0/c)\cos(kz-\omega t)\,\hat{\mathbf y}$
in vacuum, verify by hand that
$$\nabla\cdot\mathbf E=0,\quad \nabla\cdot\mathbf B=0,\quad
  \nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t},\quad
  \nabla\times\mathbf B=\mu_0\varepsilon_0\frac{\partial\mathbf E}{\partial t},$$
and that the last two balance **only if** $\omega=ck$. *Check:* `plane_wave_fields(1.0, 1.0, c=1.0)`
builds exactly these **E**, **B**; `verify_vacuum_plane_wave(1.0, 1.0, 1.0, point, t)` returns all
four residuals ≈ 0 at any `(point, t)`.

**Solution.** $\mathbf E=E_0\cos(kz-\omega t)\,\hat{\mathbf x}$ depends only on $z,t$, so
$\nabla\cdot\mathbf E=\partial E_x/\partial x=0$; likewise $\nabla\cdot\mathbf B=\partial B_y/\partial y=0$
— the two divergence laws hold with no condition. For the curls only the $z$-derivative survives:
$$\nabla\times\mathbf E=\frac{\partial E_x}{\partial z}\,\hat{\mathbf y}=-E_0k\sin(kz-\omega t)\,\hat{\mathbf y},\qquad
  -\frac{\partial\mathbf B}{\partial t}=-\frac{E_0\omega}{c}\sin(kz-\omega t)\,\hat{\mathbf y},$$
so Faraday balances **only if** $k=\omega/c$. Ampère likewise gives
$\nabla\times\mathbf B=(E_0k/c)\sin(kz-\omega t)\,\hat{\mathbf x}$ versus
$\mu_0\varepsilon_0\,\partial\mathbf E/\partial t=(E_0\omega/c^2)\sin(kz-\omega t)\,\hat{\mathbf x}$,
matching **only if** $\omega=ck$. All four therefore hold exactly at $\omega=ck$, which is what
`verify_vacuum_plane_wave(1.0, 1.0, 1.0, …)` shows: gauss_E and gauss_B are $0$ identically, and
faraday, ampere_maxwell come back $\sim10^{-16}$.

### P4.  What breaks when ω ≠ ck  *(Gr §7.3.3, p.337)*
Keep the **E** above (built with $c=1$, so $\omega=k$) but give **B** the wrong speed — amplitude
$E_0/c'$ and frequency $\omega'=c'k$ with $c'\neq c$. Show Faraday's law $\nabla\times\mathbf E=-\partial\mathbf B/\partial t$
no longer balances, and argue physically that the curl of **E** *sets* the time-derivative of **B**,
locking their amplitudes and frequencies together. *Check:* build `E,_,_ = plane_wave_fields(1.0, 1.0, c=1.0)`
and `_,Bwrong,_ = plane_wave_fields(1.0, 1.0, c=2.0)`; then `faraday_residual(E, Bwrong, …)` jumps well
above 0.1, and `ampere_maxwell_residual` fails the same way.

**Solution.** Keep $\mathbf E$ built with $c=1$ (so $\omega=k=1$) but give $\mathbf B$ the speed
$c'=2$: amplitude $E_0/c'=\tfrac12$ and frequency $\omega'=c'k=2$. Faraday now pits
$\nabla\times\mathbf E=-E_0k\sin(kz-\omega t)\,\hat{\mathbf y}=-\sin(z-t)\,\hat{\mathbf y}$ against
$$-\frac{\partial\mathbf B}{\partial t}=-\frac{E_0}{c'}\,\omega'\sin(kz-\omega' t)\,\hat{\mathbf y}=-\sin(z-2t)\,\hat{\mathbf y}.$$
The two carry different space–time phases, $\sin(z-t)$ versus $\sin(z-2t)$, so they cannot cancel
at every $(z,t)$ — Faraday is broken. Physically the curl of $\mathbf E$ *is* what drives
$\partial\mathbf B/\partial t$ pointwise, so a self-consistent wave is locked to one frequency and
one amplitude ratio $B_0=E_0/c$; mistuning the speed snaps that lock. Numerically
`faraday_residual(E, Bwrong, …)`$=0.79$ and `ampere_maxwell_residual`$=0.58$, both far past the
$0.1$ violation threshold.

### P5.  The speed of light from two static constants  *(Gr §7.3.3, p.337; the wave, `~EM-15`)*
From the vacuum equations derive the wave equation $\nabla^2\mathbf E=\mu_0\varepsilon_0\,\partial^2\mathbf E/\partial t^2$
— note it is $\nabla\cdot\mathbf B=0$ (with $\nabla\cdot\mathbf E=0$) that lets the double curl of **E**
collapse to $-\nabla^2\mathbf E$ — and read off
$$c=\frac{1}{\sqrt{\mu_0\varepsilon_0}} .$$
Plug in $\varepsilon_0$ (from `~EM-01`) and $\mu_0$ (from `~EM-08`) and confirm $c\approx3\times10^8\ \mathrm{m/s}$.
*Check:* `C_SI` equals $1/\sqrt{\mu_0\varepsilon_0}$ to machine precision (≈ 2.998×10⁸ m/s), and
`gauss_B_residual` returns ≈ 0 for the plane-wave **B**, confirming the $\nabla\cdot\mathbf B=0$ the
derivation leans on.

**Solution.** In vacuum ($\rho=0,\,\mathbf J=0$) take the curl of Faraday and substitute
Ampère–Maxwell:
$$\nabla\times(\nabla\times\mathbf E)=-\frac{\partial}{\partial t}(\nabla\times\mathbf B)=-\mu_0\varepsilon_0\frac{\partial^2\mathbf E}{\partial t^2}.$$
The identity $\nabla\times(\nabla\times\mathbf E)=\nabla(\nabla\cdot\mathbf E)-\nabla^2\mathbf E$
loses its first term because $\nabla\cdot\mathbf E=0$, collapsing to $-\nabla^2\mathbf E$; the
companion $\nabla\cdot\mathbf B=0$ does the same for $\mathbf B$, so both fields obey a genuine wave
equation
$$\nabla^2\mathbf E=\mu_0\varepsilon_0\frac{\partial^2\mathbf E}{\partial t^2},\qquad c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}.$$
With $\varepsilon_0=8.854\times10^{-12}$ (`~EM-01`) and $\mu_0=1.257\times10^{-6}$ (`~EM-08`),
$c=2.998\times10^8$ m/s — the speed of light from two *static* constants. This is `C_SI` to
machine precision, and `gauss_B_residual`$\approx0$ for the plane-wave $\mathbf B$ confirms the
$\nabla\cdot\mathbf B=0$ the collapse leans on.
