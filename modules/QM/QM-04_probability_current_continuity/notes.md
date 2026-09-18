# QM-04 — Probability Current & Continuity (notes)

Probability is conserved *locally*, not just globally: it cannot vanish here and
reappear there without flowing through the space between. The carrier of that flow
is the **probability current j**, and the bookkeeping is the **continuity equation** —
the very same law that conserves mass (`~CM-22`) and charge (`~EM-14`).

Citation key (full details in `refs.md`): **Gri** = Griffiths, *Introduction to
Quantum Mechanics*; **Sak** = Sakurai, *Modern Quantum Mechanics*.

## 1. Derivation from the Schrödinger equation
Take the time-dependent Schrödinger equation [Gri §1.5] and its complex conjugate
(with $V$ real):
$$i\hbar\frac{\partial\Psi}{\partial t}=-\frac{\hbar^2}{2m}\nabla^2\Psi+V\Psi,
\qquad
-i\hbar\frac{\partial\Psi^*}{\partial t}=-\frac{\hbar^2}{2m}\nabla^2\Psi^*+V\Psi^*.$$
The density is $\rho=\Psi^*\Psi=|\Psi|^2$ (`~QM-02`). Differentiate in time and use
both equations; the **potential terms cancel** because $V$ is real:
$$\frac{\partial\rho}{\partial t}
=\Psi^*\frac{\partial\Psi}{\partial t}+\Psi\frac{\partial\Psi^*}{\partial t}
=\frac{i\hbar}{2m}\big(\Psi^*\nabla^2\Psi-\Psi\nabla^2\Psi^*\big)
=\frac{i\hbar}{2m}\nabla\!\cdot\!\big(\Psi^*\nabla\Psi-\Psi\nabla\Psi^*\big).$$

## 2. The current and the continuity equation
Define the **probability current**
$$\boxed{\ \mathbf j=\frac{\hbar}{m}\,\mathrm{Im}\!\left(\Psi^*\nabla\Psi\right)
=\frac{i\hbar}{2m}\big(\Psi\nabla\Psi^*-\Psi^*\nabla\Psi\big)\ }$$
and §1 collapses to the **continuity equation** [Gri §1.5; Sak §2.4]
$$\boxed{\ \frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf j=0\ },\qquad \rho=|\Psi|^2 .$$
Code: `prob_density`, `prob_current`, `continuity_residual`.

## 3. Global conservation — normalization is forever
Integrate over all space and use the divergence theorem:
$$\frac{d}{dt}\int_V|\Psi|^2\,dV=-\int_V\nabla\cdot\mathbf j\,dV=-\oint_S\mathbf j\cdot d\mathbf A\;\to\;0,$$
since $\mathbf j\to 0$ at infinity for any normalizable state. So if $\Psi$ is
normalized once, it stays normalized — the Schrödinger equation is consistent with
the Born rule for all time (`~QM-02`). Code: `total_probability`.

## 4. Reading the current: flow vs. standing
**Travelling wave** $\Psi=A\,e^{i(kx-\omega t)}$: then $\rho=|A|^2$ and
$$j=\frac{\hbar k}{m}|A|^2=\rho\,v,\qquad v=\frac{\hbar k}{m}=\frac{p}{m},$$
probability flows at the de Broglie velocity, exactly like the mass flux $\rho\mathbf v$
of `~CM-22`. Code: `plane_wave`, `mean_velocity` (gives $\langle v\rangle=$ group
velocity, the Ehrenfest result `~QM-07`).

**Real stationary state** (bound eigenstates can be chosen real, e.g. infinite-well
$\sin$ modes): $\Psi^*\nabla\Psi$ is real, so $\mathrm{Im}=0$ and $\mathbf j=0$
everywhere — a standing wave carries **no net current**. A complex superposition of
two real eigenstates *does* carry an oscillating current (this is what sloshes charge
in a radiating atom, `~QM-16`).

## 5. With a magnetic field (a look ahead)
Minimal coupling $\mathbf p\to\mathbf p-q\mathbf A$ (`~EM-09`) makes the
**gauge-invariant** current
$$\mathbf j=\frac{\hbar}{m}\mathrm{Im}(\Psi^*\nabla\Psi)-\frac{q}{m}\mathbf A\,|\Psi|^2 ,$$
the quantum object behind the London equation of superconductivity. The bare
$(\hbar/m)\mathrm{Im}(\Psi^*\nabla\Psi)$ is the canonical piece; the $\mathbf A$ term
restores gauge invariance.

## 6. KEY BRIDGE B2 — one law, four densities
Continuity is the same equation everywhere; only the conserved "stuff" changes:

$$
\begin{array}{lll}
\textbf{quantity} & \textbf{density }\rho & \textbf{current / flux} \\
\text{mass (CM-22)} & \rho_\text{mass} & \mathbf j=\rho\mathbf v \\
\text{charge (EM-14)} & \rho_\text{charge} & \mathbf J \\
\text{probability (QM-04)} & |\Psi|^2 & \tfrac{\hbar}{m}\mathrm{Im}(\Psi^*\nabla\Psi) \\
\text{phase space (PK-01)} & f(\mathbf x,\mathbf v,t) & f\mathbf v \\
\end{array}
$$

each obeying $\partial_t\rho+\nabla\cdot\mathbf j=0$ (the phase-space version,
$\partial_t f+\mathbf v\cdot\nabla f+\mathbf a\cdot\nabla_{\!v}f=0$, is Liouville/Vlasov).
EM-14 adds the lesson that a **source** turns continuity into a balance law
($\partial_t u+\nabla\cdot\mathbf S=-\mathbf J\cdot\mathbf E$, Poynting); probability
has no source because $V$ is real (a *complex* "optical potential" would model
absorption and break it).

## Where this goes
- `~CM-22` / `~EM-14` — the mass and charge faces of this identical law (B2).
- `~PK-01` — the phase-space density and the Boltzmann/Vlasov equation (the KrF/LoKI code).
- `~QM-07` — Ehrenfest's theorem: $\langle v\rangle$ from the current; `~QM-16` — radiating transition currents.
- `~EM-09` — the vector potential and the gauge-invariant current.
