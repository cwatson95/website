# QM-04 — Problems

Work by hand, then check with `code/probability_current.py`. Citations in
`../refs.md`; **Gri** = Griffiths Ch.1–2, **Sak** = Sakurai Ch.2.

### P1.  Derive the current  *(Gri §1.5)*
Starting from the time-dependent Schrödinger equation and its conjugate (V real),
show ∂|Ψ|²/∂t = −∇·**j** with **j** = (ℏ/m) Im(Ψ*∇Ψ). Where exactly does the
assumption that V is real get used? *Check:* `continuity_residual(psi0, psi1, dx, dt)`
on a free-evolved packet is ~10⁻⁴, far below the ~0.12 size of ∂ₜρ itself.
*Answer:* the $V$-terms cancel only because $V=V^*$ (real); that single fact turns $\partial_t\rho$ into $-\nabla\!\cdot\mathbf j$.

**Solution.** Solve each equation for its time derivative,
$$\frac{\partial\Psi}{\partial t}=\frac{i\hbar}{2m}\nabla^2\Psi-\frac{i}{\hbar}V\Psi,\qquad \frac{\partial\Psi^*}{\partial t}=-\frac{i\hbar}{2m}\nabla^2\Psi^*+\frac{i}{\hbar}V^*\Psi^*,$$
and assemble $\partial_t\rho=\Psi^*\partial_t\Psi+\Psi\,\partial_t\Psi^*$:
$$\frac{\partial\rho}{\partial t}=\frac{i\hbar}{2m}\big(\Psi^*\nabla^2\Psi-\Psi\nabla^2\Psi^*\big)-\frac{i}{\hbar}\big(V-V^*\big)|\Psi|^2 .$$
The potential piece $-\tfrac{i}{\hbar}(V-V^*)|\Psi|^2$ vanishes **iff $V=V^*$** — that is the one and only place reality of $V$ is used (a complex $V$ would leave a source). With the identity $\Psi^*\nabla^2\Psi-\Psi\nabla^2\Psi^*=\nabla\!\cdot(\Psi^*\nabla\Psi-\Psi\nabla\Psi^*)$,
$$\frac{\partial\rho}{\partial t}=\frac{i\hbar}{2m}\nabla\!\cdot\!\big(\Psi^*\nabla\Psi-\Psi\nabla\Psi^*\big)=-\nabla\!\cdot\mathbf j,\qquad \mathbf j=\frac{\hbar}{m}\mathrm{Im}(\Psi^*\nabla\Psi).$$
Numerically the residual $\partial_t\rho+\partial_x j$ on a free-evolved packet is $1.6\times10^{-4}$, far below the $\sim0.12$ magnitude of $\partial_t\rho$ itself — the continuity equation holds to discretization error.

### P2.  Two forms are one  *(Gri §1.5)*
Show (ℏ/m) Im(Ψ*∇Ψ) = (iℏ/2m)(Ψ∇Ψ* − Ψ*∇Ψ), and that **j** is real. *Check:*
`test_two_current_formulas_agree` compares the two expressions on a Gaussian packet
(equal to 10⁻¹²; imaginary part ~10⁻¹²).
*Answer:* both equal $\tfrac{\hbar}{m}\mathrm{Im}(\Psi^*\nabla\Psi)$ via $\mathrm{Im}\,z=(z-z^*)/2i$, and the current is real.

**Solution.** For any complex number $z$, $\mathrm{Im}\,z=\dfrac{z-z^*}{2i}$. Take $z=\Psi^*\nabla\Psi$; since $(\nabla\Psi)^*=\nabla\Psi^*$ its conjugate is $z^*=\Psi\nabla\Psi^*$, so
$$\frac{\hbar}{m}\mathrm{Im}(\Psi^*\nabla\Psi)=\frac{\hbar}{m}\cdot\frac{\Psi^*\nabla\Psi-\Psi\nabla\Psi^*}{2i}=\frac{i\hbar}{2m}\big(\Psi\nabla\Psi^*-\Psi^*\nabla\Psi\big),$$
using $1/i=-i$ — exactly the second form. Reality is automatic: $\tfrac{\hbar}{m}\mathrm{Im}(\cdots)$ is $\hbar/m$ times a real number; equivalently the bracket $\Psi\nabla\Psi^*-\Psi^*\nabla\Psi=z^*-z=-2i\,\mathrm{Im}\,z$ is purely imaginary, and $i\times(\text{imaginary})$ is real. This is why the two arrays agree to $10^{-12}$ while the imaginary part of the second form is $\sim10^{-12}$ — one real current wearing two algebraic faces.

### P3.  Travelling wave: j = ρv  *(Gri §2.4)*
For Ψ = A e^{i(kx−ωt)}, compute ρ and j and show j = ρ(ℏk/m) = ρv. Interpret v.
*Check:* `prob_current(plane_wave(x,1.5), dx).mean()/prob_density(...).mean()` ≈ 1.5 = k,
and reverses sign for k → −k.
*Answer:* $\rho=|A|^2$ and $j=\tfrac{\hbar k}{m}|A|^2=\rho v$ with $v=\hbar k/m=p/m$; $j$ flips sign with $k$.

**Solution.** For $\Psi=A\,e^{i(kx-\omega t)}$ the density is $\rho=|\Psi|^2=|A|^2$ — uniform and time-independent. The derivative is $\partial_x\Psi=ik\Psi$, so
$$\Psi^*\partial_x\Psi=ik\,|\Psi|^2=ik\,|A|^2\qquad(\text{purely imaginary}),$$
and therefore
$$j=\frac{\hbar}{m}\mathrm{Im}(\Psi^*\partial_x\Psi)=\frac{\hbar}{m}\,k\,|A|^2=\frac{\hbar k}{m}\,\rho=\rho\,v,\qquad v=\frac{\hbar k}{m}=\frac{p}{m}.$$
So $v$ is the de Broglie velocity: the probability fluid drifts rigidly at $v$, the same $\rho\mathbf v$ flux carried by a mass current (`~CM-22`). Sending $k\to-k$ reverses $v$, hence $j$. With $k=1.5$, `prob_current(...).mean()/prob_density(...).mean()` $\approx1.4991\approx k=v$ (the $\sim1\%$ deficit is central-difference error), and it changes sign for $k\to-k$ — exactly $j=\rho v$.

### P4.  A real state carries no current  *(Gri §2.2)*
Show that any wavefunction that is real (up to a constant global phase) — e.g. an
infinite-square-well eigenstate ψₙ ∝ sin(nπx/a) — has **j** = 0 everywhere. Why does
this *not* contradict the particle "moving"? *Check:* `prob_current(np.cos(1.5*x), dx)`
is 0 to 10⁻¹².
*Answer:* a real (constant-global-phase) $\Psi$ gives $\Psi^*\nabla\Psi=\tfrac12\nabla(R^2)$, real, so $\mathbf j=0$; the standing state is equal $\pm k$ currents that cancel ($\langle p\rangle=0$ but $\langle p^2\rangle\neq0$).

**Solution.** Write $\Psi(x)=R(x)\,e^{i\alpha}$ with $R$ real and $\alpha$ a constant global phase. Then
$$\Psi^*\nabla\Psi=R\,e^{-i\alpha}\,\nabla\!\big(R\,e^{i\alpha}\big)=R\,\nabla R=\tfrac12\nabla\!\big(R^2\big),$$
which is **real**, so $\mathrm{Im}(\Psi^*\nabla\Psi)=0$ and $\mathbf j=0$ everywhere. For the well mode $\psi_n\propto\sin(n\pi x/a)$ we have $R=\sin(n\pi x/a)$ real ($\alpha=0$), hence $\mathbf j\equiv0$. This does not contradict "motion": a real eigenstate is a *standing* wave, the equal superposition $\sin(kx)\propto e^{ikx}-e^{-ikx}$ of right- and left-movers whose currents are equal and opposite and cancel. There is real momentum content — $\langle p^2\rangle\neq0$, i.e. nonzero kinetic energy — but $\langle p\rangle=0$ and zero *net* flux, just as a standing wave on a string stores energy yet transports none. Thus `prob_current(np.cos(1.5*x), dx)` is $0$ to $10^{-12}$ (in fact identically zero, since $\mathrm{Im}$ of a real array vanishes).

### P5.  Global conservation  *(Gri §1.4)*
From ∂ₜρ + ∇·**j** = 0 and **j** → 0 at infinity, prove d/dt ∫|Ψ|² dV = 0. *Check:*
`total_probability` stays 1.000000 across 50 free-evolution steps
(`test_normalization_conserved_under_free_evolution`).
*Answer:* $\dfrac{d}{dt}\!\int|\Psi|^2\,dV=-\oint_S\mathbf j\cdot d\mathbf A\to0$, so total probability is constant in time.

**Solution.** Integrate continuity over all space and pull the derivative out of the integral:
$$\frac{d}{dt}\int_V|\Psi|^2\,dV=\int_V\frac{\partial\rho}{\partial t}\,dV=-\int_V\nabla\!\cdot\mathbf j\,dV .$$
By the divergence theorem the right-hand side is a flux through the surface at infinity:
$$-\int_V\nabla\!\cdot\mathbf j\,dV=-\oint_{S_\infty}\mathbf j\cdot d\mathbf A\;\longrightarrow\;0,$$
because any normalizable $\Psi$ — and with it $\mathbf j$ — decays to zero at infinity, killing the surface integral. Hence $\tfrac{d}{dt}\int|\Psi|^2\,dV=0$: normalized once, normalized forever, which is exactly what makes Schrödinger evolution consistent with the Born rule (`~QM-02`). Numerically `total_probability` holds at $1.000000$ across $50$ free-evolution steps (drift $<10^{-9}$) — global conservation confirmed.

### P6.  Current in a superposition  *(Sak §2.4)*
Take Ψ = c₁ψ₁ + c₂ψ₂ with ψ₁, ψ₂ real energy eigenstates (E₁ ≠ E₂). Show the current
oscillates at the Bohr frequency (E₂−E₁)/ℏ even though each ψₙ alone has j = 0 — the
microscopic origin of dipole radiation (`~QM-16`). *Check (optional):* build two
real well-states on the grid, add them with a relative phase e^{−i(E₂−E₁)t/ℏ}, and
watch `prob_current` slosh back and forth.
*Answer:* $j=\dfrac{\hbar}{m}\,c_1c_2\big(\psi_2\psi_1'-\psi_1\psi_2'\big)\sin\!\big[(E_2-E_1)t/\hbar\big]$ — a current oscillating at the Bohr frequency $\omega_{21}=(E_2-E_1)/\hbar$.

**Solution.** Stationary states evolve by a pure phase, so (taking $c_1,c_2$ real WLOG — a phase in $c_n$ only shifts the sine)
$$\Psi(x,t)=c_1\psi_1(x)\,e^{-iE_1t/\hbar}+c_2\psi_2(x)\,e^{-iE_2t/\hbar},\qquad \omega_{21}\equiv\frac{E_2-E_1}{\hbar}.$$
Form $\Psi^*\partial_x\Psi$. The diagonal pieces $c_1^2\psi_1\psi_1'+c_2^2\psi_2\psi_2'$ are real (the $\psi_n$ are real), so they drop out of $\mathrm{Im}$ — each state alone gives $j=0$, recovering P4. Only the cross terms remain:
$$\Psi^*\partial_x\Psi\big|_{\text{cross}}=c_1c_2\big(\psi_1\psi_2'\,e^{-i\omega_{21}t}+\psi_2\psi_1'\,e^{+i\omega_{21}t}\big).$$
Taking the imaginary part with $\mathrm{Im}\,e^{\pm i\omega_{21}t}=\pm\sin\omega_{21}t$,
$$j=\frac{\hbar}{m}\,\mathrm{Im}(\Psi^*\partial_x\Psi)=\frac{\hbar}{m}\,c_1c_2\big(\psi_2\psi_1'-\psi_1\psi_2'\big)\,\sin\!\Big(\frac{(E_2-E_1)t}{\hbar}\Big).$$
The current sloshes sinusoidally at the **Bohr frequency** $\omega_{21}=(E_2-E_1)/\hbar$, though each $\psi_n$ alone carries none; its spatial moment $\frac{d}{dt}\langle x\rangle\propto\int j\,dx$ is the oscillating dipole that radiates at the transition frequency (`~QM-16`). Building two real well-states with relative phase $e^{-i(E_2-E_1)t/\hbar}$ and evaluating `prob_current` shows exactly this back-and-forth slosh, of period $2\pi\hbar/(E_2-E_1)$.

### P7.  The B2 bridge  *(this module §6)*
Write the continuity equation for mass (`~CM-22`), charge (`~EM-14`), probability
(here), and phase space (`~PK-01`) in one table, identifying ρ and **j** in each.
What new feature does EM-14 add that QM-04 lacks, and why? *(Answer: a source term
−**J**·**E**; probability has none because V is real.)*

**Solution.** Every one of these laws has the same skeleton $\partial_t\rho+\nabla\!\cdot\mathbf j=0$; only the conserved "stuff" and its flux change:
$$
\begin{array}{lll}
\textbf{quantity} & \textbf{density }\rho & \textbf{current / flux }\mathbf j\\
\text{mass (CM-22)} & \rho_\text{mass} & \rho_\text{mass}\,\mathbf v\\
\text{charge (EM-14)} & \rho_\text{charge} & \mathbf J=\rho_\text{charge}\,\mathbf v\\
\text{probability (QM-04)} & |\Psi|^2 & \tfrac{\hbar}{m}\mathrm{Im}(\Psi^*\nabla\Psi)\\
\text{phase space (PK-01)} & f(\mathbf x,\mathbf v,t) & f\,\mathbf v
\end{array}
$$
Written out, the phase-space row is the collisionless Boltzmann/Liouville (Vlasov) equation $\partial_t f+\mathbf v\cdot\nabla_x f+\mathbf a\cdot\nabla_v f=0$. What **EM-14 adds** is a *source*: bookkeeping field energy (Poynting) instead of charge turns bare continuity into a balance law
$$\frac{\partial u}{\partial t}+\nabla\!\cdot\mathbf S=-\,\mathbf J\cdot\mathbf E,$$
where $-\mathbf J\cdot\mathbf E$ is the rate the field does work on charges (Joule heating) — energy is exchanged between field and matter, so the field-energy flux is *not* source-free. Probability has **no** such source because $V$ is real: in P1 the potential terms cancelled exactly, leaving $\partial_t\rho+\nabla\!\cdot\mathbf j=0$ with zero right-hand side. (A complex optical potential $V=V_R-iV_I$ breaks this, adding a sink $-\tfrac{2V_I}{\hbar}|\Psi|^2$ that models absorption — the direct analog of $-\mathbf J\cdot\mathbf E$.) This is the B2 capstone: the QM-04 code verifies the probability row numerically — `continuity_residual` $\sim10^{-4}$ and `total_probability` fixed at $1.000000$ — and the residual stays at discretization noise precisely because the law is source-free.
