# QO-04 — Open Quantum Systems: Master Equations & Decoherence (notes)

A real atom is never alone. Even in the dark it is coupled to the infinitely many
vacuum modes of the electromagnetic field — a **reservoir** it cannot track. We
keep only the atom and average over the reservoir; the price is that the atom's
evolution is no longer unitary. Its state must be the **density matrix** $\rho$
(`~QM-20`), and its equation of motion is no longer the von Neumann equation but
the **Lindblad master equation**, whose dissipators make `~QM-20`'s reversible
"rotation of coherences" into **irreversible decoherence**.

Citation key (full details + verified pages in `refs.md`): **SZ** = Scully &
Zubairy, *Quantum Optics* (Cambridge, 1997). Two-level density matrix §5.3;
spontaneous emission §6.3; quantum theory of damping (master equation) Ch. 8;
driven–damped atom / optical Bloch Ch. 10.

## 1. The density matrix of an open system
For a two-level atom (basis $|e\rangle,|g\rangle$) the state is a $2\times2$
Hermitian, unit-trace, positive operator [SZ §5.3]:
$$\rho=\begin{pmatrix}\rho_{ee}&\rho_{eg}\\ \rho_{ge}&\rho_{gg}\end{pmatrix},
\qquad \rho=\rho^\dagger,\quad \mathrm{Tr}\,\rho=\rho_{ee}+\rho_{gg}=1,\quad \rho\succeq0 .$$
The **diagonal** entries $\rho_{ee},\rho_{gg}$ are **populations** (probabilities
of being excited / ground); the **off-diagonal** $\rho_{eg}=\rho_{ge}^{*}$ are
**coherences**, encoding the relative phase of a superposition. Code:
`density_matrix`, `populations`, `excited_population`, `coherence`,
`is_density_matrix`.

## 2. From closed to open: the Lindblad master equation
A *closed* system obeys the von Neumann equation (`~QM-20`),
$$i\hbar\,\dot\rho=[H,\rho]\qquad\Longrightarrow\qquad \rho(t)=U\rho(0)U^\dagger,
\quad U=e^{-iHt/\hbar},$$
which is unitary and therefore **spectrum-preserving**: a pure state stays pure
forever. To describe an atom leaking energy to a reservoir we trace the reservoir
out under the Born–Markov approximation [SZ Ch. 8]; the most general
**generator** of a completely positive, trace-preserving (CPTP) Markovian
semigroup is the **Lindblad (GKSL) form**
$$\boxed{\ \dot\rho=-\frac{i}{\hbar}[H,\rho]
+\sum_k\Big(L_k\,\rho\,L_k^\dagger-\tfrac12\{L_k^\dagger L_k,\rho\}\Big)\ }$$
with **collapse (jump) operators** $L_k$. The commutator is the coherent flow of
§2; each **dissipator** $\mathcal D[L_k]\rho=L_k\rho L_k^\dagger-\tfrac12\{L_k^\dagger L_k,\rho\}$
adds irreversible relaxation. Code: `lindblad_rhs`, `evolve_lindblad` (which
ravels $\rho$ to a 4-vector and integrates with `solve_ivp`).

## 3. Why this form? Trace, Hermiticity, positivity
The structure of the dissipator is exactly what is needed to keep $\rho$ a
legitimate state. **Trace preservation** follows from the cyclic property of the
trace, $\mathrm{Tr}(L\rho L^\dagger)=\mathrm{Tr}(L^\dagger L\,\rho)$:
$$\frac{d}{dt}\,\mathrm{Tr}\,\rho=\sum_k\Big(\mathrm{Tr}(L_k\rho L_k^\dagger)
-\tfrac12\,\mathrm{Tr}\{L_k^\dagger L_k,\rho\}\Big)
=\sum_k\big(\mathrm{Tr}(L_k^\dagger L_k\rho)-\mathrm{Tr}(L_k^\dagger L_k\rho)\big)=0,$$
so probability is conserved. The generator is manifestly **Hermiticity-preserving**
(each term equals its own dagger), and the full flow is **completely positive**:
$\rho(t)$ stays positive semidefinite, its eigenvalues remain genuine
probabilities $\ge0$. These three facts — $\mathrm{Tr}\,\rho=1$, $\rho=\rho^\dagger$,
$\rho\succeq0$ for all $t$ — are the meaning of **CPTP**, and are checked in
`test_lindblad_generator_is_trace_preserving`,
`test_lindblad_generator_is_hermiticity_preserving`,
`test_state_stays_positive_semidefinite`.

## 4. Spontaneous emission and the $T_1$ time
The Weisskopf–Wigner result [SZ §6.3] is that an excited atom decays to ground at
the rate $\gamma$ (the Einstein $A$ coefficient, `~QO-03`). In Lindblad language
this is a **single** collapse operator $L=\sqrt{\gamma}\,\sigma^-$ with
$\sigma^-=|g\rangle\langle e|$ the **lowering operator**: each "jump" carries the
atom $|e\rangle\to|g\rangle$ and emits a photon into the reservoir. Inserting it
into the master equation and reading off the matrix elements gives
$$\begin{aligned}
\dot\rho_{ee}&=-\gamma\,\rho_{ee}, &\qquad
\dot\rho_{gg}&=+\gamma\,\rho_{ee},\\
\dot\rho_{eg}&=-\tfrac{\gamma}{2}\,\rho_{eg}, &\qquad
\dot\rho_{ge}&=-\tfrac{\gamma}{2}\,\rho_{ge}.
\end{aligned}$$
The population thus decays exponentially,
$$\boxed{\ \rho_{ee}(t)=\rho_{ee}(0)\,e^{-\gamma t}\ },\qquad T_1\equiv\frac1\gamma,$$
defining the **energy-relaxation ($T_1$) time**; the lost population reappears in
the ground state, conserving the trace. Code: `spontaneous_emission_op`;
`excited_population`; `test_excited_population_decays_at_gamma`. The unique
steady state (undriven) is $\rho=|g\rangle\langle g|$ — everything ends in the
ground state (`test_undriven_steady_state_is_ground`).

## 5. Coherence, decoherence, and the $T_2$ time
The same jump operator damps the **coherence at half the population rate** (the
factor $\tfrac12$ in $\dot\rho_{eg}$ above), $\rho_{eg}(t)=\rho_{eg}(0)\,e^{-\gamma t/2}$.
The off-diagonal element decaying to zero **is decoherence** — the superposition
loses its definite phase and $\rho$ becomes diagonal (classical). From emission
alone $T_2=2T_1$. Real atoms also suffer **elastic, phase-scrambling collisions**
that randomize the phase without changing populations [SZ §5.3.3]; these are a
second collapse operator, the **pure-dephasing** term
$$L_\phi=\sqrt{\gamma_\phi/2}\;\sigma_z\quad\Longrightarrow\quad
\dot\rho_{eg}\big|_\phi=-\gamma_\phi\,\rho_{eg},$$
which leaves the populations untouched. Adding the two coherence-decay rates gives
the **transverse-relaxation ($T_2$) time**:
$$\boxed{\ \frac{1}{T_2}=\frac{1}{2T_1}+\frac{1}{T_\phi}\ },\qquad
\gamma_\phi=\frac{1}{T_\phi}.$$
Code: `dephasing_op`; `test_coherence_decays_at_half_gamma`,
`test_T2_dephasing_relation`.

## 6. The optical Bloch equations: driven, damped, saturated
Now drive the atom with a near-resonant laser (Rabi frequency $\Omega$, detuning
$\Delta$, `~QO-02`). In the rotating frame and rotating-wave approximation the
Hamiltonian is
$$H=\hbar\Delta\,|e\rangle\langle e|+\frac{\hbar\Omega}{2}\,\sigma_x ,$$
and the master equation with $L=\sqrt\gamma\,\sigma^-$ becomes the **optical Bloch
equations** [SZ Ch. 10] — coherent Rabi driving competing against relaxation. The
drive pumps population up and builds coherence; decay drains it. Their balance is
a **steady state**, $\dot\rho=0$, with excited population
$$\boxed{\ \rho_{ee}^{\,\mathrm{ss}}
=\frac{\Omega^2/4}{\Delta^2+\gamma^2/4+\Omega^2/2}\ },\qquad
\lim_{\Omega\to\infty}\rho_{ee}^{\,\mathrm{ss}}=\tfrac12 .$$
On resonance $\rho_{ee}^{\,\mathrm{ss}}=\Omega^2/(\gamma^2+2\Omega^2)$, rising from
$0$ to the **saturation** value $\tfrac12$: a classical field can at best
*equalize* the populations, never **invert** a two-level atom (the physics behind
needing three- or four-level schemes to make a laser, `~QO-03`). Code:
`two_level_hamiltonian`, `steady_state_excited_population`;
`test_driven_steady_state_matches_optical_bloch`,
`test_steady_state_saturates_at_one_half`.

## Where this goes
- `~QM-20` — the density matrix and the **closed-system** limit ($i\hbar\dot\rho=[H,\rho]$);
  this module is its irreversible, open-system generalization.
- `~QO-02` / `~QO-03` — the two-level atom & Rabi frequency, and the
  spontaneous-emission rate $\gamma$ that here becomes the collapse operator.
- `~QO-05` — squeezed reservoirs replace the ordinary vacuum bath, modifying which
  quadrature decoheres (SZ §8.2.2).
- The **quantum-jump / Monte-Carlo wavefunction** unravelling of the master
  equation (SZ §8.5) is the stochastic picture behind the same Lindblad average,
  and the engine of single-trajectory simulations.
