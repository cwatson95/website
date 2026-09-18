# QO-02 — Problems

Work each by hand, then check with `code/atom_field.py`. Citations in `../refs.md`;
**SZ** = Scully & Zubairy, *Quantum Optics* (Ch. 5 semiclassical, Ch. 6 quantized).
Natural units $\hbar=1$ (as in the code).

### P1.  The two-level operators  *(SZ §5.1; ~QM-11)*
With $|e\rangle=(1,0)^T$, $|g\rangle=(0,1)^T$, write $\sigma_z,\sigma^+,\sigma^-$ as
$2\times2$ matrices and show $\sigma^+\sigma^-=|e\rangle\langle e|$,
$\sigma^-\sigma^+=|g\rangle\langle g|$, $[\sigma^+,\sigma^-]=\sigma_z$, and
$\{\sigma^+,\sigma^-\}=\mathbb 1$ — the qubit algebra of `~QM-11` with
$\sigma^\pm=\tfrac12(\sigma_x\pm i\sigma_y)$. *Check:* `sigma_plus @ sigma_minus`
$=\mathrm{diag}(1,0)$ and `sigma_plus @ sigma_minus - sigma_minus @ sigma_plus`
$=$ `sigma_z` (`test_atom_pauli_algebra`).

**Solution.** With $|e\rangle=(1,0)^T,\ |g\rangle=(0,1)^T$ the outer products are read
straight off:
$$\sigma^+=|e\rangle\langle g|=\begin{pmatrix}0&1\\0&0\end{pmatrix},\qquad
\sigma^-=|g\rangle\langle e|=\begin{pmatrix}0&0\\1&0\end{pmatrix},\qquad
\sigma_z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.$$
Multiplying, $\sigma^+\sigma^-=\begin{pmatrix}1&0\\0&0\end{pmatrix}=|e\rangle\langle e|$
and $\sigma^-\sigma^+=\begin{pmatrix}0&0\\0&1\end{pmatrix}=|g\rangle\langle g|$ — the two
level projectors. Subtracting gives
$[\sigma^+,\sigma^-]=|e\rangle\langle e|-|g\rangle\langle g|=\sigma_z$; adding gives
$\{\sigma^+,\sigma^-\}=|e\rangle\langle e|+|g\rangle\langle g|=\mathbb 1$. With
$\sigma^\pm=\tfrac12(\sigma_x\pm i\sigma_y)$ these are exactly the spin-$\tfrac12$ ladder
relations of `~QM-11`. Hence `sigma_plus @ sigma_minus`$=\mathrm{diag}(1,0)$ and
`sigma_plus @ sigma_minus - sigma_minus @ sigma_plus`$=$`sigma_z`.

### P2.  The resonant Rabi flop  *(SZ §5.2)*
An atom starts in $|g\rangle$ and is driven on resonance ($\delta=0$). From
$H_\text{RWA}=\tfrac12\Omega\,\sigma_x$ show the excited population is
$P_e(t)=\sin^2(\Omega t/2)$: a complete inversion at $\Omega t=\pi$ (a "$\pi$-pulse")
and a return to the ground state at $\Omega t=2\pi$. *Check:*
`rabi_excited_population(np.pi, 1.0, 0.0)` $=1.0$ and
`rabi_excited_population(2*np.pi, 1.0, 0.0)` $\approx 0$
(`test_rabi_resonant_inversion_and_return`).

**Solution.** On resonance $H_\text{RWA}=\tfrac12\Omega\sigma_x$, and since
$\sigma_x^2=\mathbb 1$ the propagator is a rotation:
$$e^{-iHt}=e^{-i(\Omega t/2)\sigma_x}=\cos\tfrac{\Omega t}{2}\,\mathbb 1
-i\sin\tfrac{\Omega t}{2}\,\sigma_x.$$
Acting on $|g\rangle$ with $\sigma_x|g\rangle=|e\rangle$,
$$|\psi(t)\rangle=\cos\tfrac{\Omega t}{2}\,|g\rangle-i\sin\tfrac{\Omega t}{2}\,|e\rangle,$$
so $P_e=|\langle e|\psi\rangle|^2=\sin^2(\Omega t/2)$. At $\Omega t=\pi$ this is
$\sin^2(\pi/2)=1$ (complete inversion — the $\pi$-pulse) and at $\Omega t=2\pi$ it is
$\sin^2\pi=0$ (the return). Matching `rabi_excited_population(np.pi, 1.0, 0.0)`$=1.0$ and
`rabi_excited_population(2*np.pi, 1.0, 0.0)`$\approx0$.

### P3.  Detuning: generalized Rabi frequency & saturation  *(SZ §5.2)*
Repeat P2 with detuning $\delta\neq0$. Show the flop runs at
$\Omega_R=\sqrt{\Omega^2+\delta^2}$ and the largest transfer is the saturated
amplitude $\Omega^2/(\Omega^2+\delta^2)<1$ — the off-resonant atom never fully
inverts. *Check:* `generalized_rabi(1.0, 1.5)` $=1.803$; the peak
`rabi_excited_population(np.pi/1.803, 1.0, 1.5)` $=\Omega^2/\Omega_R^2=1/3.25=0.3077$
(`test_rabi_detuned_saturation`).

**Solution.** With detuning $H_\text{RWA}=\tfrac12(\delta\sigma_z+\Omega\sigma_x)
=\tfrac12\Omega_R\,\hat n\!\cdot\!\vec\sigma$ is a spin in the tilted field
$\hat n=(\Omega,0,\delta)/\Omega_R$, $\Omega_R=\sqrt{\Omega^2+\delta^2}$. The propagator
$e^{-i(\Omega_R t/2)\hat n\cdot\vec\sigma}=\cos\tfrac{\Omega_R t}{2}\mathbb 1
-i\sin\tfrac{\Omega_R t}{2}\,\hat n\!\cdot\!\vec\sigma$ flips $|g\rangle\to|e\rangle$ with
amplitude $\langle e|\hat n\!\cdot\!\vec\sigma|g\rangle=\Omega/\Omega_R$, so
$$P_e(t)=\frac{\Omega^2}{\Omega_R^2}\sin^2\!\frac{\Omega_R t}{2}.$$
The flop now runs at $\Omega_R>\Omega$ but its amplitude is capped at
$\Omega^2/\Omega_R^2=\Omega^2/(\Omega^2+\delta^2)<1$, reached when $\Omega_R t=\pi$ — the
off-resonant atom never fully inverts. For $\Omega=1,\delta=1.5$:
$\Omega_R=\sqrt{3.25}=1.803$ and the peak is $1/3.25=0.3077$, i.e.
`generalized_rabi(1.0, 1.5)`$=1.803$ and
`rabi_excited_population(np.pi/1.803, 1.0, 1.5)`$=0.3077$.

### P4.  The rotating-wave approximation  *(SZ §5.2.2–5.2.3)*
Expand $H_\text{int}=\hbar\Omega\cos(\omega_L t)(\sigma^++\sigma^-)$ in the
interaction picture and identify the **co-rotating** ($e^{\pm i(\omega_a-\omega_L)t}$)
and **counter-rotating** ($e^{\pm i(\omega_a+\omega_L)t}$) terms. Which does the RWA
drop, and why is it valid for $\Omega,|\delta|\ll\omega_a$? *Check:* evolving
$|g\rangle$ under `two_level_hamiltonian(Omega, detuning)` and projecting on
$|e\rangle$ reproduces the closed-form `rabi_excited_population` to $10^{-9}$
across several $(\Omega,\delta)$ (`test_rabi_matches_two_level_evolution`).

**Solution.** In the interaction picture w.r.t. $H_A=\tfrac12\hbar\omega_a\sigma_z$ the
ladder operators rotate, $\sigma^\pm(t)=e^{\pm i\omega_a t}\sigma^\pm$, and
$\cos\omega_L t=\tfrac12(e^{i\omega_L t}+e^{-i\omega_L t})$, so
$$H_I(t)=\tfrac12\hbar\Omega\Big[\underbrace{\sigma^+e^{i\delta t}+\sigma^-e^{-i\delta t}}_{\text{co-rotating},\ \delta=\omega_a-\omega_L}+\underbrace{\sigma^+e^{i(\omega_a+\omega_L)t}+\sigma^-e^{-i(\omega_a+\omega_L)t}}_{\text{counter-rotating}}\Big].$$
The RWA drops the counter-rotating pair, which oscillate at $\omega_a+\omega_L\approx
2\omega_a$: over a Rabi period $\sim1/\Omega$ they average to nearly zero when
$\Omega,|\delta|\ll\omega_a$ (the residue is the small Bloch–Siegert shift). What remains,
in the frame rotating at $\omega_L$, is the static
$H_\text{RWA}=\tfrac12(\delta\sigma_z+\Omega\sigma_x)$. Because nothing else is discarded,
evolving $|g\rangle$ under `two_level_hamiltonian` and projecting on $|e\rangle$ reproduces
the closed-form `rabi_excited_population` to $10^{-9}$.

### P5.  Jaynes–Cummings blocks & the conserved excitation number  *(SZ §6.1–6.2)*
For $H=\omega_c a^\dagger a+\tfrac12\omega_a\sigma_z+g(a\sigma^++a^\dagger\sigma^-)$,
show $\hat N=a^\dagger a+|e\rangle\langle e|$ commutes with $H$, so the dynamics stay
inside each doublet $\{|e,n\rangle,|g,n+1\rangle\}$, and compute the coupling
$\langle e,n|H|g,n+1\rangle=g\sqrt{n+1}$. *Check:* `jcm_hamiltonian(5,5.3,0.9,10)` is
Hermitian and commutes with $\hat N$ to $10^{-10}$
(`test_jcm_hamiltonian_hermitian_and_excitation_conserved`).

**Solution.** The free terms commute with $\hat N=a^\dagger a+\sigma^+\sigma^-$ trivially.
For the interaction use $[a^\dagger a,a]=-a$ and $[\sigma^+\sigma^-,\sigma^+]=\sigma^+$
(since $|e\rangle\langle e|\,\sigma^+=\sigma^+$ but $\sigma^+|e\rangle\langle e|=0$):
$$[\hat N,a\sigma^+]=[a^\dagger a,a]\,\sigma^++a\,[\sigma^+\sigma^-,\sigma^+]
=-a\sigma^++a\sigma^+=0,$$
and likewise $[\hat N,a^\dagger\sigma^-]=0$, so $[\hat N,H]=0$. The conserved $\hat N$
cannot mix different excitation numbers, and $a\sigma^+,\,a^\dagger\sigma^-$ connect only
$|e,n\rangle\leftrightarrow|g,n+1\rangle$ (both with $\hat N=n+1$), so $H$ is block diagonal
in those doublets. The off-diagonal element is
$$\langle e,n|H|g,n+1\rangle=g\,\langle n|a|n+1\rangle\,\langle e|\sigma^+|g\rangle
=g\sqrt{n+1}.$$
This is why `jcm_hamiltonian(5,5.3,0.9,10)` comes out Hermitian and commutes with $\hat N$
to $10^{-10}$.

### P6.  Dressed states and the vacuum Rabi splitting  *(SZ §6.2)*
Diagonalize the $2\times2$ block to get
$E_{n,\pm}=\omega_c(n+\tfrac12)\pm\tfrac12\sqrt{\delta^2+4g^2(n+1)}$ and show the gap
is $2g\sqrt{n+1}$ on resonance — for $n=0$ the **vacuum Rabi splitting** $2g$. *Check:*
`dressed_energies(n, ω_a−ω_c, g, ω_c)` matches the eigenvalues of the block of
`jcm_hamiltonian`; `vacuum_rabi_splitting(1.0)` $=2.0$ and the $n=1$ resonant gap is
$2\sqrt2=2.828$ (`test_dressed_energies_match_block_and_vacuum_rabi`).

**Solution.** In the doublet $(|e,n\rangle,|g,n+1\rangle)$ the diagonal energies are
$\omega_c n+\tfrac12\omega_a$ and $\omega_c(n+1)-\tfrac12\omega_a$, with off-diagonal
$g\sqrt{n+1}$ from P5. Their half-sum is $\omega_c(n+\tfrac12)$ and their difference is
$\delta=\omega_a-\omega_c$, so the block is
$$H_n=\omega_c\big(n+\tfrac12\big)\,\mathbb 1
+\tfrac12\begin{pmatrix}\delta & 2g\sqrt{n+1}\\ 2g\sqrt{n+1} & -\delta\end{pmatrix}.$$
The traceless part $\tfrac12(\delta\sigma_z+2g\sqrt{n+1}\,\sigma_x)$ has eigenvalues
$\pm\tfrac12\sqrt{\delta^2+4g^2(n+1)}$, so
$$E_{n,\pm}=\omega_c\big(n+\tfrac12\big)\pm\tfrac12\sqrt{\delta^2+4g^2(n+1)}.$$
The gap $E_{n,+}-E_{n,-}=\sqrt{\delta^2+4g^2(n+1)}$ becomes $2g\sqrt{n+1}$ on resonance; at
$n=0$ that is the vacuum Rabi splitting $2g$. For $g=1$ this gives
`vacuum_rabi_splitting(1.0)`$=2.0$ and the $n=1$ gap $2\sqrt2=2.828$, matching the
eigenvalues of `jcm_hamiltonian`'s block.

### P7.  Collapse and revival over a coherent field  *(SZ §6.2)*
Prepare $|e\rangle\otimes|\alpha\rangle$ on resonance. Show
$\langle\sigma_z\rangle(t)=\sum_n P_n\cos(2g\sqrt{n+1}\,t)$ with Poissonian $P_n$,
and estimate the collapse ($t_c\sim\sqrt2/g$) and revival ($t_r\sim2\pi\sqrt{\bar n}/g$)
times. Why is a revival impossible for a classical field? *Check:* for
$\alpha=4$ ($\bar n=16$), `revival_time(1.0, 16.0)` $=8\pi=25.13$;
`jcm_inversion` is $\approx0$ at $t_r/2$ and revives to $\approx+0.44$ near $t_r$,
matching `resonant_inversion_series` to $10^{-9}$ (`test_collapse_and_revival`).

**Solution.** On resonance the $|e,n\rangle$ component sits in the doublet with gap
$2g\sqrt{n+1}$, so the atom started excited has each Fock weight oscillate as
$\cos(2g\sqrt{n+1}\,t)$; weighting by the Poissonian $P_n=e^{-\bar n}\bar n^{\,n}/n!$,
$$\langle\sigma_z\rangle(t)=\sum_n P_n\cos\!\big(2g\sqrt{n+1}\,t\big).$$
Expanding $\sqrt{n+1}\approx\sqrt{\bar n}+(n-\bar n)/2\sqrt{\bar n}$ across the Poisson width
$\sigma_n=\sqrt{\bar n}$, the tones dephase and the envelope collapses as $e^{-g^2t^2/2}$,
i.e. $t_c\sim\sqrt2/g$ — independent of $\bar n$. They rephase when neighbouring
frequencies, spaced $\Delta\omega\approx g/\sqrt{\bar n}$, slip by $2\pi$:
$$t_r\sim\frac{2\pi}{\Delta\omega}=\frac{2\pi\sqrt{\bar n}}{g}.$$
A classical field carries a single Rabi frequency and would flop forever; the discrete
spread of $\sqrt{n+1}$ tones — hence the revival — is a fingerprint of field quantization.
For $\alpha=4$ ($\bar n=16$), $t_r=8\pi=25.13$ (`revival_time(1.0, 16.0)`); the inversion is
$\approx0$ at $t_r/2$ and revives to $\approx+0.44$ at $t_r$, matching
`resonant_inversion_series` to $10^{-9}$.
