# QM-20 — Problems

Work them by hand, then check with `code/density_matrix.py`. Sources in `../refs.md`.
Qubit states/operators use natural units $\hbar=1$; $|0\rangle,|1\rangle$ are
spin-up/down along $z$, $|\pm\rangle$ along $x$.

### P1.  Build a pure-state density matrix  *(Griffiths 3e, Example 12.1, p.576–577)*
Construct $\rho$ for an electron with spin up along $x$, $|+\rangle=\tfrac1{\sqrt2}(|0\rangle+|1\rangle)$,
and verify it is Hermitian, has trace 1, and $\mathrm{Tr}(\rho^2)=1$.
*Answer:* $\rho=|+\rangle\langle+|=\tfrac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$;
eigenvalues $\{1,0\}$, so $\mathrm{Tr}\,\rho=1$ and $\mathrm{Tr}(\rho^2)=1$ (pure).
*Check:* `rho = density_matrix_pure(plus)`; `is_density_matrix(rho)` is `True`,
`purity(rho)` $=1$, `is_pure(rho)` is `True`.
(`test_pure_state_is_valid_density_matrix`, `test_purity_pure_vs_mixed`.)

**Solution.** With $|+\rangle=\tfrac1{\sqrt2}\binom{1}{1}$, the projector is
$$\rho=|+\rangle\langle+|=\tfrac12\binom{1}{1}\begin{pmatrix}1&1\end{pmatrix}=\tfrac12\begin{pmatrix}1&1\\1&1\end{pmatrix}.$$
It is real-symmetric, so $\rho=\rho^\dagger$, and $\mathrm{Tr}\,\rho=\tfrac12(1+1)=1$. Squaring,
$\rho^2=\tfrac14\begin{pmatrix}2&2\\2&2\end{pmatrix}=\rho$, so $\rho$ is an idempotent rank-1 projector
with eigenvalues $\{1,0\}$ and $\mathrm{Tr}(\rho^2)=\sum_k\lambda_k^2=1$ — pure. This is exactly
`density_matrix_pure(plus)`, for which `is_density_matrix(rho)` is `True`, `purity(rho)` $=1$, and
`is_pure(rho)` is `True`.

### P2.  A genuine mixture, and the purity test  *(Griffiths 3e, Example 12.2 & Prob. 12.6, p.579–580)*
Construct $\rho$ for an electron that is spin-up or spin-down along $z$ with equal
probability. Is it pure? Show in general that $\mathrm{Tr}(\rho^2)\le1$ with
equality iff the state is pure.
*Answer:* $\rho=\tfrac12|0\rangle\langle0|+\tfrac12|1\rangle\langle1|=\tfrac12 I$;
Hermitian, trace 1, but $\mathrm{Tr}(\rho^2)=\tfrac12<1$ — **not** pure. In general
$\mathrm{Tr}(\rho^2)=\sum_k\lambda_k^2\le(\sum_k\lambda_k)^2=1$, equality iff one
$\lambda_k=1$ (i.e. $\rho^2=\rho$).
*Check:* `rho = density_matrix_mixed([ket0, ket1], [0.5, 0.5])` equals
`maximally_mixed(2)`; `purity(rho)` $=0.5$, `is_pure(rho)` is `False`.
(`test_mixed_state_is_valid_density_matrix`, `test_idempotent_iff_pure`.)

**Solution.** Adding the two projectors,
$$\rho=\tfrac12|0\rangle\langle0|+\tfrac12|1\rangle\langle1|
=\tfrac12\begin{pmatrix}1&0\\0&0\end{pmatrix}+\tfrac12\begin{pmatrix}0&0\\0&1\end{pmatrix}=\tfrac12 I.$$
It is Hermitian with $\mathrm{Tr}\,\rho=1$, but $\mathrm{Tr}(\rho^2)=\mathrm{Tr}(\tfrac14 I)=\tfrac12<1$ —
**not** pure. In general, in $\rho$'s eigenbasis $\mathrm{Tr}(\rho^2)=\sum_k\lambda_k^2$; since the
$\lambda_k\ge0$ sum to $1$, $\sum_k\lambda_k^2\le(\sum_k\lambda_k)^2=1$, with equality iff a single
$\lambda_k=1$ (all others $0$), i.e. $\rho^2=\rho$. Hence `density_matrix_mixed([ket0, ket1], [0.5, 0.5])`
equals `maximally_mixed(2)`, with `purity(rho)` $=0.5$ and `is_pure(rho)` `False`.

### P3.  Expectation values from $\rho$  *(Griffiths 3e §12.3.1, Eq. 12.20 & §12.3.2, Eq. 12.28)*
Show $\langle A\rangle=\mathrm{Tr}(\rho A)$ reduces to $\langle\psi|A|\psi\rangle$
for a pure state, and to the ensemble average $\sum_i p_i\langle\psi_i|A|\psi_i\rangle$
for a mixture. Evaluate $\langle\sigma_x\rangle$ in $|+\rangle$ and in $I/2$.
*Answer:* insert completeness for the pure case; linearity of the trace for the
mixed case. $\langle\sigma_x\rangle_{|+\rangle}=+1$ (determinate);
$\langle\sigma_x\rangle_{I/2}=\mathrm{Tr}(\tfrac12 I\,\sigma_x)=0$.
*Check:* `expectation(density_matrix_pure(plus), sigma_x)` $=1.0$;
`expectation(maximally_mixed(2), sigma_x)` $=0.0$.
(`test_expectation_pure_equals_braket`, `test_expectation_mixed_is_ensemble_average`.)

**Solution.** Insert completeness $\sum_n|n\rangle\langle n|=I$ for the pure case:
$$\mathrm{Tr}(\rho A)=\sum_n\langle n|\psi\rangle\langle\psi|A|n\rangle
=\langle\psi|A\Big(\sum_n|n\rangle\langle n|\Big)|\psi\rangle=\langle\psi|A|\psi\rangle,$$
and linearity of the trace gives the mixture $\mathrm{Tr}(\rho A)=\sum_i p_i\langle\psi_i|A|\psi_i\rangle$.
For $|+\rangle$, $\sigma_x|+\rangle=+|+\rangle$, so $\langle\sigma_x\rangle=+1$ (determinate); for $I/2$,
$\langle\sigma_x\rangle=\mathrm{Tr}(\tfrac12 I\,\sigma_x)=\tfrac12\mathrm{Tr}\,\sigma_x=0$. These reproduce
`expectation(density_matrix_pure(plus), sigma_x)` $=1.0$ and
`expectation(maximally_mixed(2), sigma_x)` $=0.0$ — sharp in the pure eigenstate, fully random in the mixture.

### P4.  A subsystem of an entangled pair is mixed  *(Griffiths 3e §12.3.3, p.582)*
For the Bell state $|\Phi^+\rangle=\tfrac1{\sqrt2}(|00\rangle+|11\rangle)$, find the
reduced density matrix of qubit $A$ by tracing out qubit $B$. Is the *global* state
pure? Is the *subsystem* pure? Reconcile this with "we know the state precisely."
*Answer:* $\rho_A=\mathrm{Tr}_B|\Phi^+\rangle\langle\Phi^+|=\tfrac12|0\rangle\langle0|
+\tfrac12|1\rangle\langle1|=I/2$ — maximally mixed. The global state is pure ($S=0$),
the subsystem is mixed ($S=\ln2$): this is **entanglement**, not ignorance —
"the subsystem by itself does not occupy a pure state" (Griffiths p.582).
*Check:* `bell = density_matrix_pure(bell_phi_plus())`; `is_pure(bell)` is `True`;
`partial_trace(bell, [2,2], keep=0)` equals `maximally_mixed(2)`.
(`test_bell_subsystem_is_maximally_mixed`.)

**Solution.** Expand $\rho_{AB}=|\Phi^+\rangle\langle\Phi^+|=\tfrac12\big(|00\rangle+|11\rangle\big)\big(\langle00|+\langle11|\big)$
and take the partial trace $\langle a|\rho_A|a'\rangle=\sum_b\langle a,b|\rho_{AB}|a',b\rangle$. The diagonal
terms survive; the cross terms $|00\rangle\langle11|,\,|11\rangle\langle00|$ vanish because their $B$-factor
is $\langle1|0\rangle=0$:
$$\rho_A=\mathrm{Tr}_B\,\rho_{AB}=\tfrac12|0\rangle\langle0|+\tfrac12|1\rangle\langle1|=\frac{I}{2}.$$
The global state is pure ($S=0$) but $\rho_A$ is maximally mixed ($S=\ln2$): the mixedness is **entanglement**,
not ignorance — we know $|\Phi^+\rangle$ exactly. Hence `is_pure(bell)` is `True` while
`partial_trace(bell, [2,2], keep=0)` equals `maximally_mixed(2)`.

### P5.  Entanglement entropy: entangled vs product  *(forward link ~QM-21)*
Compare a product state $|0\rangle\otimes|+\rangle$ with the Bell state of P4.
Compute the von Neumann entropy $S=-\mathrm{Tr}(\rho\ln\rho)$ of qubit $A$ in each.
What does $S_A$ tell you?
*Answer:* product → $\rho_A=|0\rangle\langle0|$, $S_A=0$ (no entanglement); Bell →
$\rho_A=I/2$, $S_A=\ln2$ (maximal entanglement of a qubit pair). The reduced-state
entropy **is** the entanglement measure for a pure bipartite state.
*Check:* `von_neumann_entropy(partial_trace(density_matrix_pure(tensor(ket0,plus)),[2,2],0))`
$=0$; the Bell version $=\ln 2\approx0.6931$.
(`test_product_subsystem_stays_pure`, `test_bell_subsystem_is_maximally_mixed`.)

**Solution.** The product state $\rho_{AB}=|0\rangle\langle0|\otimes|+\rangle\langle+|$ factorizes, so
$\rho_A=\mathrm{Tr}_B\,\rho_{AB}=|0\rangle\langle0|\,\mathrm{Tr}(|+\rangle\langle+|)=|0\rangle\langle0|$ with
eigenvalues $\{1,0\}$, giving
$$S_A=-\sum_k\lambda_k\ln\lambda_k=-(1\ln1+0\ln0)=0.$$
For the Bell state $\rho_A=I/2$ has eigenvalues $\{\tfrac12,\tfrac12\}$, so
$S_A=-2\cdot\tfrac12\ln\tfrac12=\ln2\approx0.6931$. The reduced-state entropy is therefore the entanglement
measure: $0$ for the unentangled product, maximal $\ln2$ for the Bell pair. This matches the code — the
product `von_neumann_entropy(...)` $=0$ and the Bell version $=\ln 2\approx0.6931$.

### P6.  The von Neumann equation & stationary states  *(Griffiths 3e, Prob. 12.4(b), p.577)*
Show that $\rho$ evolves by $i\hbar\dot\rho=[H,\rho]$, with solution
$\rho(t)=U\rho(0)U^\dagger$, $U=e^{-iHt/\hbar}$. (a) Show a pure state stays pure.
(b) Show $\rho$ is stationary ($\dot\rho=0$) iff $[H,\rho]=0$.
*Answer:* differentiate $\rho=U\rho_0U^\dagger$ and use $i\hbar\dot U=HU$. (a)
$\rho(t)$ is unitarily similar to $\rho(0)$, so $\mathrm{Tr}(\rho^2)$ (and the whole
spectrum) is conserved — pure stays pure. (b) $\dot\rho\propto[H,\rho]$ vanishes iff
$\rho$ commutes with $H$, i.e. $\rho$ is diagonal in the energy eigenbasis.
*Check:* with `H` random Hermitian and `rho` pure, `purity(evolve(rho,H,t))` $=1$
for all `t`; a $\rho$ built diagonal in $H$'s eigenbasis has
`von_neumann_rhs(rho,H)` $=0$ and `evolve(rho,H,t)` unchanged.
(`test_unitary_evolution_conserves_purity_and_trace`,
`test_von_neumann_equation_finite_difference`, `test_stationary_state_commutes_with_H`.)

**Solution.** Differentiate $\rho(t)=U\rho_0U^\dagger$ using $i\hbar\dot U=HU$ (hence $i\hbar\dot U^\dagger=-U^\dagger H$):
$$i\hbar\dot\rho=(i\hbar\dot U)\rho_0U^\dagger+U\rho_0(i\hbar\dot U^\dagger)=HU\rho_0U^\dagger-U\rho_0U^\dagger H=[H,\rho].$$
(a) $\rho(t)=U\rho_0U^\dagger$ is unitarily similar to $\rho_0$, so it shares the same spectrum; thus
$\mathrm{Tr}(\rho^2)=\sum_k\lambda_k^2$ is conserved and a pure state ($\lambda=\{1,0\}$) stays pure. (b)
$\dot\rho=-\tfrac{i}{\hbar}[H,\rho]$ vanishes iff $[H,\rho]=0$, i.e. $\rho$ is diagonal in the energy
eigenbasis. Numerically `purity(evolve(rho,H,t))` $=1$ for a pure $\rho$, and a state built diagonal in
$H$'s eigenbasis gives `von_neumann_rhs(rho,H)` $=0$ (norm $0$) and unchanged `evolve`.

### P7.  Decoherence vs unitary evolution  *(Griffiths 3e §12.5, p.586; bridge ~QO-04)*
A qubit starts in $|+\rangle\langle+|=\tfrac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$,
which has large off-diagonal **coherences**. (a) Under closed (unitary) evolution,
can $\rho$ ever become the *diagonal* mixed state $I/2$? (b) What additional
ingredient turns the coherences off, and what is it called?
*Answer:* (a) **No.** Unitary evolution conserves the spectrum, so a pure state
($\lambda=\{1,0\}$) can never become mixed ($\lambda=\{\tfrac12,\tfrac12\}$); it can
only *rotate* the coherences, not destroy them. (b) Coupling to an **environment**
(an open system) damps the off-diagonal terms — **decoherence** — described by a
Lindblad master equation (`~QO-04`); it is "the fundamental mechanism by which
quantum mechanics reduces to classical mechanics" (Griffiths p.586).
*Check:* `purity(density_matrix_pure(plus))` $=1$ and stays $1$ under any
`evolve(...)`; reaching $I/2$ (`purity` $=0.5$) is impossible unitarily.
(`test_unitary_evolution_conserves_purity_and_trace`.)

**Solution.** Closed evolution $\rho(t)=U\rho_0U^\dagger$ keeps the eigenvalues of $\rho_0$ fixed for all
$t$. The start $|+\rangle\langle+|$ has spectrum $\{1,0\}$ ($\mathrm{Tr}(\rho^2)=1$), while $I/2$ has spectrum
$\{\tfrac12,\tfrac12\}$ ($\mathrm{Tr}(\rho^2)=\tfrac12$); the two spectra differ, so **no unitary** maps one
to the other. (a) Hence $\rho$ can never become $I/2$ — unitary evolution only *rotates* the off-diagonal
coherences, never erases them. (b) Erasing them needs coupling to an **environment**: the coherences then
decay irreversibly — **decoherence** — described by a Lindblad master equation (`~QO-04`). So
`purity(density_matrix_pure(plus))` $=1$ and stays $1$ under any `evolve(...)`, making `purity` $=0.5$
($I/2$) unreachable unitarily.
