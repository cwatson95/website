# QO-04 — Problems

Work by hand, then check with `code/open_systems.py`. Citations in `../refs.md`;
**SZ** = Scully & Zubairy, *Quantum Optics*. Two-level basis $(|e\rangle,|g\rangle)$,
units $\hbar=1$; $\gamma$ is the spontaneous-emission rate, $\Omega$ the Rabi
frequency, $\Delta$ the detuning.

### P1.  The Lindblad form conserves probability  *(SZ Ch. 8)*
Show that the Lindblad generator is **trace-preserving**: using the cyclic
property of the trace, prove $\frac{d}{dt}\mathrm{Tr}\,\rho
=\sum_k\big[\mathrm{Tr}(L_k\rho L_k^\dagger)-\mathrm{Tr}(L_k^\dagger L_k\rho)\big]=0$,
so $\mathrm{Tr}\,\rho=1$ for all time. Why does this fail if you drop the
$-\tfrac12\{L_k^\dagger L_k,\rho\}$ "no-jump" term? *Check:* `lindblad_rhs(rho, H,
[√γ σ⁻, L_φ])` has $|\mathrm{Tr}\,\dot\rho|<10^{-12}$ for any `rho`, `H`
(`test_lindblad_generator_is_trace_preserving`).

*Answer:* yes — each dissipator is traceless, so $\frac{d}{dt}\mathrm{Tr}\,\rho=0$ and $\mathrm{Tr}\,\rho=1$ for all $t$.

**Solution.** Trace the generator. The commutator vanishes by cyclicity, $\mathrm{Tr}[H,\rho]=0$. For each dissipator, cyclicity gives $\mathrm{Tr}(L_k\rho L_k^\dagger)=\mathrm{Tr}(L_k^\dagger L_k\rho)$, and the anticommutator term yields $\mathrm{Tr}\{L_k^\dagger L_k,\rho\}=2\,\mathrm{Tr}(L_k^\dagger L_k\rho)$, so
$$\frac{d}{dt}\mathrm{Tr}\,\rho=\sum_k\Big[\mathrm{Tr}(L_k^\dagger L_k\rho)-\tfrac12\cdot2\,\mathrm{Tr}(L_k^\dagger L_k\rho)\Big]=0.$$
The $-\tfrac12\{L_k^\dagger L_k,\rho\}$ "no-jump" term is exactly what cancels the gain term $L_k\rho L_k^\dagger$ under the trace. Drop it and
$$\frac{d}{dt}\mathrm{Tr}\,\rho=\sum_k\mathrm{Tr}(L_k^\dagger L_k\rho)\ge0,$$
so probability would leak in and $\rho$ would stop being normalized. With the full generator `lindblad_rhs` gives $|\mathrm{Tr}\,\dot\rho|<10^{-12}$ for any `rho`, `H`.

### P2.  Spontaneous emission and the $T_1$ time  *(SZ §6.3)*
With the single collapse operator $L=\sqrt\gamma\,\sigma^-$ ($\sigma^-=|g\rangle\langle e|$)
and $H=0$, read off $\dot\rho_{ee}=-\gamma\rho_{ee}$ and solve it. Show the lost
population lands in the ground state ($\dot\rho_{gg}=+\gamma\rho_{ee}$), conserving
the trace. *Check:* starting in $|e\rangle$, `excited_population(evolve_lindblad(...))`
equals $e^{-\gamma t}$ to $10^{-6}$, and `_fit_rate` returns $\gamma=1.0000$
(`test_excited_population_decays_at_gamma`).

*Answer:* $\rho_{ee}(t)=\rho_{ee}(0)\,e^{-\gamma t}$, with $T_1=1/\gamma$.

**Solution.** With $L=\sqrt\gamma\,\sigma^-$, $\sigma^-=|g\rangle\langle e|$, and $L^\dagger L=\gamma|e\rangle\langle e|$, take the $\langle e|\cdots|e\rangle$ element of the dissipator. The gain term vanishes ($\langle e|\sigma^-=0$) and the anticommutator gives $-\tfrac\gamma2\langle e|\{|e\rangle\langle e|,\rho\}|e\rangle=-\tfrac\gamma2(2\rho_{ee})$, so
$$\dot\rho_{ee}=-\gamma\,\rho_{ee}\quad\Longrightarrow\quad \rho_{ee}(t)=\rho_{ee}(0)\,e^{-\gamma t},\qquad T_1=\frac1\gamma.$$
For the ground state the gain term now survives, $\gamma\langle g|\sigma^-\rho\sigma^+|g\rangle=\gamma\rho_{ee}$, while its anticommutator vanishes, giving $\dot\rho_{gg}=+\gamma\rho_{ee}$. Thus $\dot\rho_{ee}+\dot\rho_{gg}=0$: the population leaving $|e\rangle$ lands in $|g\rangle$, conserving the trace. Starting in $|e\rangle$, `excited_population` follows $e^{-\gamma t}$ to $10^{-6}$ and `_fit_rate` returns $\gamma=1.0000$.

### P3.  Coherence decays at half the rate: $T_2=2T_1$  *(SZ §5.3)*
From the same master equation derive $\dot\rho_{eg}=-\tfrac{\gamma}{2}\rho_{eg}$,
hence $|\rho_{eg}(t)|=|\rho_{eg}(0)|e^{-\gamma t/2}$. Why is the coherence rate
exactly **half** the population rate, and what does the off-diagonal going to zero
mean physically (decoherence)? *Check:* starting in $|+\rangle$,
`abs(coherence(...))` decays at rate $\gamma/2=0.5000$, giving $T_2=2T_1$
(`test_coherence_decays_at_half_gamma`).

*Answer:* $\dot\rho_{eg}=-\tfrac{\gamma}{2}\rho_{eg}$, so $|\rho_{eg}(t)|=|\rho_{eg}(0)|e^{-\gamma t/2}$ and $T_2=2T_1$.

**Solution.** Take the $\langle e|\cdots|g\rangle$ element of the same dissipator. The gain term again vanishes ($\langle e|\sigma^-=0$), and of the two anticommutator pieces only the one acting on the *left* index survives:
$$\dot\rho_{eg}=-\tfrac\gamma2\langle e|\big(|e\rangle\langle e|\rho+\rho|e\rangle\langle e|\big)|g\rangle=-\tfrac\gamma2\big(\rho_{eg}+0\big)=-\frac\gamma2\,\rho_{eg}.$$
The population decay (P2) touched $|e\rangle$ on *both* sides — two factors, rate $\gamma$ — whereas the coherence touches it on only *one* side, hence exactly **half**: $|\rho_{eg}(t)|=|\rho_{eg}(0)|e^{-\gamma t/2}$, i.e. $T_2=2T_1$. The off-diagonal collapsing to zero is the loss of definite relative phase — **decoherence**, $\rho$ becoming diagonal (a classical mixture). Starting in $|+\rangle$, `abs(coherence(...))` decays at rate $\gamma/2=0.5000$, giving $T_2=2T_1$.

### P4.  Pure dephasing and the $T_2$ relation  *(SZ §5.3.3)*
Add the elastic-collision dephasing operator $L_\phi=\sqrt{\gamma_\phi/2}\,\sigma_z$.
Show it leaves the populations untouched but adds $-\gamma_\phi\rho_{eg}$ to the
coherence, so $1/T_2=1/(2T_1)+1/T_\phi$. *Check:* with $\gamma=1$, $\gamma_\phi=0.8$,
the simulated coherence-decay rate from `evolve_lindblad([spontaneous_emission_op,
dephasing_op])` is $1.3000=0.5+0.8$, and the populations are unchanged
(`test_T2_dephasing_relation`).

*Answer:* dephasing adds $-\gamma_\phi\rho_{eg}$ and nothing to the diagonal, giving $1/T_2=1/(2T_1)+1/T_\phi$.

**Solution.** For $L_\phi=\sqrt{\gamma_\phi/2}\,\sigma_z$ we have $L_\phi^\dagger L_\phi=\tfrac{\gamma_\phi}{2}\sigma_z^2=\tfrac{\gamma_\phi}{2}\mathbb 1$, so the no-jump term is $-\tfrac12\{\tfrac{\gamma_\phi}{2}\mathbb 1,\rho\}=-\tfrac{\gamma_\phi}{2}\rho$ and the dissipator collapses to
$$\mathcal D[L_\phi]\rho=\frac{\gamma_\phi}{2}\big(\sigma_z\,\rho\,\sigma_z-\rho\big).$$
Since $(\sigma_z\rho\,\sigma_z)_{ij}=(\sigma_z)_{ii}(\sigma_z)_{jj}\,\rho_{ij}$, the diagonal entries get $(\pm1)^2=1$ — **populations untouched** — while the off-diagonal gets $(+1)(-1)=-1$, so $\mathcal D[L_\phi]\rho|_{eg}=\tfrac{\gamma_\phi}{2}(-\rho_{eg}-\rho_{eg})=-\gamma_\phi\rho_{eg}$. Adding the emission part $-\tfrac\gamma2\rho_{eg}$ from P3,
$$\dot\rho_{eg}=-\Big(\frac{\gamma}{2}+\gamma_\phi\Big)\rho_{eg}\quad\Longrightarrow\quad \frac{1}{T_2}=\frac{1}{2T_1}+\frac{1}{T_\phi}.$$
With $\gamma=1$, $\gamma_\phi=0.8$ the simulated coherence-decay rate is $0.5+0.8=1.3000$ and the populations are unchanged.

### P5.  Optical Bloch steady state  *(SZ Ch. 10)*
For $H=\hbar\Delta|e\rangle\langle e|+\tfrac{\hbar\Omega}{2}\sigma_x$ and
$L=\sqrt\gamma\,\sigma^-$, set $\dot\rho=0$ and solve the optical Bloch equations
for the steady-state excited population
$\rho_{ee}^{\,\mathrm{ss}}=\dfrac{\Omega^2/4}{\Delta^2+\gamma^2/4+\Omega^2/2}$.
Evaluate it on resonance ($\Delta=0$). *Check:* for $\Omega=2,\gamma=1,\Delta=0$
both `steady_state_excited_population(2,1,0)` and the long-time
`excited_population(evolve_lindblad(...))` give $0.4444=\Omega^2/(\gamma^2+2\Omega^2)$
(`test_driven_steady_state_matches_optical_bloch`).

*Answer:* $\rho_{ee}^{\,\mathrm{ss}}=\dfrac{\Omega^2/4}{\Delta^2+\gamma^2/4+\Omega^2/2}$; on resonance $\Omega^2/(\gamma^2+2\Omega^2)$.

**Solution.** With $H=\hbar\Delta|e\rangle\langle e|+\tfrac{\hbar\Omega}{2}\sigma_x$ and $L=\sqrt\gamma\,\sigma^-$, the master equation gives the optical Bloch equations
$$\dot\rho_{eg}=-\Big(\tfrac\gamma2+i\Delta\Big)\rho_{eg}+i\tfrac\Omega2\big(\rho_{ee}-\rho_{gg}\big),\qquad
\dot\rho_{ee}=-\gamma\,\rho_{ee}+i\tfrac\Omega2\big(\rho_{eg}-\rho_{ge}\big).$$
Set both to zero. The first gives $\rho_{eg}=\dfrac{i\Omega\,(\rho_{ee}-\rho_{gg})/2}{\gamma/2+i\Delta}$; feeding its imaginary part into $\gamma\rho_{ee}=-\Omega\,\mathrm{Im}\,\rho_{eg}$ and writing $w=\rho_{ee}-\rho_{gg}=2\rho_{ee}-1$,
$$\gamma\rho_{ee}=-\frac{(\Omega^2\gamma/4)\,w}{\Delta^2+\gamma^2/4}\quad\Longrightarrow\quad \rho_{ee}^{\,\mathrm{ss}}=\frac{\Omega^2/4}{\Delta^2+\gamma^2/4+\Omega^2/2}.$$
On resonance ($\Delta=0$) this is $\Omega^2/(\gamma^2+2\Omega^2)$; for $\Omega=2,\gamma=1$ it equals $4/9=0.4444$, matching both `steady_state_excited_population(2,1,0)` and the long-time `evolve_lindblad` value.

### P6.  Saturation — you cannot invert a two-level atom  *(SZ Ch. 10)*
Show $\rho_{ee}^{\,\mathrm{ss}}$ increases monotonically with $\Omega$ but is
bounded by $\tfrac12$, the **saturation** limit, so a classical drive can at best
*equalize* the populations — never achieve inversion $\rho_{ee}>\rho_{gg}$ (the
reason lasing needs $\ge3$ levels, `~QO-03`). *Check:*
`steady_state_excited_population` is increasing in $\Omega$ and tends to $0.4999\to\tfrac12$
as $\Omega\to\infty$ (`test_steady_state_saturates_at_one_half`).

*Answer:* $\rho_{ee}^{\,\mathrm{ss}}$ rises monotonically in $\Omega$ but stays $<\tfrac12$, approaching $\tfrac12$ as $\Omega\to\infty$ — never inverted.

**Solution.** On resonance $\rho_{ee}^{\,\mathrm{ss}}(\Omega)=\dfrac{\Omega^2}{\gamma^2+2\Omega^2}$. Differentiate:
$$\frac{d\rho_{ee}^{\,\mathrm{ss}}}{d\Omega}=\frac{2\Omega(\gamma^2+2\Omega^2)-\Omega^2(4\Omega)}{(\gamma^2+2\Omega^2)^2}=\frac{2\gamma^2\Omega}{(\gamma^2+2\Omega^2)^2}>0,$$
so it increases monotonically with the drive. But the denominator always exceeds $2\Omega^2$ (the $\gamma^2>0$ term), hence
$$\rho_{ee}^{\,\mathrm{ss}}=\frac{\Omega^2}{\gamma^2+2\Omega^2}<\frac{\Omega^2}{2\Omega^2}=\frac12\qquad\xrightarrow{\ \Omega\to\infty\ }\ \frac12.$$
Because $\rho_{ee}<\tfrac12$ means $\rho_{ee}<\rho_{gg}=1-\rho_{ee}$, a classical drive can at best *equalize* the populations, never **invert** them — which is why lasing needs a $\ge3$-level scheme (`~QO-03`). Numerically `steady_state_excited_population` is increasing in $\Omega$ and tends to $0.4999\to\tfrac12$.

### P7.  Decoherence is irreversible: CPTP vs. unitary  *(SZ Ch. 8; bridge `~QM-20`)*
Unitary evolution preserves the spectrum of $\rho$, so a pure state can never
become mixed (`~QM-20`). Argue that the Lindblad flow instead drives the pure
$|+\rangle$ into the mixed ground state, while *remaining a valid state at every
instant* — Hermitian, unit-trace, positive semidefinite (CPTP). *Check:* along a
driven, damped trajectory every `evolve_lindblad` snapshot satisfies
`is_positive_semidefinite(rho)` and the undriven run relaxes to
`density_matrix(ket_g)` ($\rho_{ee}<10^{-6}$)
(`test_state_stays_positive_semidefinite`, `test_undriven_steady_state_is_ground`).

*Answer:* unitary flow preserves $\rho$'s spectrum (pure stays pure); Lindblad is CPTP but non-unitary, so it irreversibly mixes the state while keeping it valid, settling (undriven) into $|g\rangle\langle g|$.

**Solution.** Unitary evolution $\rho(t)=U\rho(0)U^\dagger$ is a similarity transform, so it leaves the eigenvalues — and the purity $\mathrm{Tr}\,\rho^2$ — invariant; a pure state ($\mathrm{Tr}\,\rho^2=1$) can never become mixed (`~QM-20`). The Lindblad generator is **not** a similarity transform. Starting from $|+\rangle$ with $H=0$, the coherence decays as $\rho_{eg}=\tfrac12e^{-\gamma t/2}$ while the populations redistribute, so
$$\mathrm{Tr}\,\rho^2=\rho_{ee}^2+\rho_{gg}^2+2|\rho_{eg}|^2<1$$
at intermediate times: the pure state has genuinely **mixed**, irreversibly (entropy produced, no unitary undoes it). Yet every snapshot stays Hermitian, unit-trace, and positive semidefinite — eigenvalues $\ge0$, a legitimate state at each instant, the meaning of CPTP. Along a driven, damped trajectory `is_positive_semidefinite(rho)` holds at every `evolve_lindblad` snapshot, and the undriven run relaxes to `density_matrix(ket_g)` with $\rho_{ee}<10^{-6}$.
