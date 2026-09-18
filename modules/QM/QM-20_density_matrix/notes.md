# QM-20 — Density matrix & open systems (notes)

By `~QM-05` a quantum state is a vector $|\psi\rangle$ in a Hilbert space and an
observable is a Hermitian operator; by `~QM-06` a measurement of $A$ returns an
eigenvalue with Born probability, and $\langle A\rangle=\langle\psi|\hat
A|\psi\rangle$. That description assumes we **know the ket** — a *pure state*. But
two situations break that assumption:

- **Ignorance.** The preparation is random: the system is in $|\psi_i\rangle$
  with classical probability $p_i$, and we simply don't know which (Griffiths 3e
  §12.3.2, p.579). An electron from an accelerator "might have spin up… or spin
  down… we just don't know."
- **Entanglement.** The system is part of a larger whole in a definite (pure)
  joint state, but we only have access to *our* subsystem; the rest is
  inaccessible (Griffiths 3e §12.3.3, p.582).

In both cases the right object is not a ket but the **density operator** $\rho$, a
Hermitian, unit-trace, positive operator. This module is Griffiths 3e Ch. 12
(the "Afterword"), §12.3 *Mixed States and the Density Matrix* (p.575), turned
into evaluable linear algebra.

## 1. The density operator: pure and mixed states

For a **pure** state — a known, normalized ket — define the density operator as
the projector onto that ray (Griffiths 3e §12.3.1, p.576):
$$\boxed{\,\rho=|\psi\rangle\langle\psi|\,}$$
For a **mixed** state — the system is in $|\psi_i\rangle$ with probability $p_i$,
$p_i\ge 0$, $\sum_i p_i=1$ — generalize to the convex combination (Griffiths 3e
§12.3.2, Eq. 12.30, p.579):
$$\boxed{\,\rho=\sum_i p_i\,|\psi_i\rangle\langle\psi_i|\,}$$
"The density matrix encodes all the information available to us about the system."
The matrix elements in a basis $\{|i\rangle\}$ are $\rho_{ij}=\langle i|\rho|j\rangle$;
the diagonal entries $\rho_{ii}$ are **populations** (probabilities of finding the
system in $|i\rangle$) and the off-diagonal $\rho_{ij}$ are **coherences**.

**Three defining properties** (Griffiths 3e Eqs. 12.17–12.19, 12.31–12.33). Any
density operator is

- **Hermitian**, $\rho=\rho^\dagger$ — so its eigenvalues are real;
- **unit trace**, $\mathrm{Tr}\,\rho=1$ — "like any probabilities," the
  populations sum to 1;
- **positive semidefinite**, $\langle\phi|\rho|\phi\rangle\ge0$ for all $\phi$ —
  equivalently all eigenvalues $\lambda_k\ge0$.

These three are exactly the quantum analogue of a classical probability
distribution: the eigenvalues $\{\lambda_k\}$ of $\rho$ are a genuine probability
distribution over the orthonormal eigenbasis. (`density_matrix_pure`,
`density_matrix_mixed`, `is_density_matrix`; `test_pure_state_is_valid_density_matrix`,
`test_mixed_state_is_valid_density_matrix`, `test_invalid_matrices_rejected`.)

> A pure state is the special case where one $\lambda_k=1$ and the rest vanish, so
> $\rho$ has **rank 1** — it is a projector. A mixed state spreads weight over
> $\ge2$ eigenvalues. The maximally mixed state $\rho=I/d$ has every
> $\lambda_k=1/d$: total ignorance.

## 2. Purity — the one-number test for pure vs mixed

How do you tell a pure state from a mixed one, given only $\rho$? Compute the
**purity**
$$\gamma=\mathrm{Tr}(\rho^2)=\sum_k\lambda_k^2.$$
Because the $\lambda_k$ are a probability distribution, $\sum_k\lambda_k^2\le
(\sum_k\lambda_k)^2=1$ with equality iff one $\lambda_k=1$ (all weight on a single
state). Hence (Griffiths 3e Prob. 12.6(b)(c), p.580):
$$\boxed{\,\mathrm{Tr}(\rho^2)\le1,\quad\text{with equality }\Longleftrightarrow\ \rho^2=\rho\ \Longleftrightarrow\ \text{pure}\,}$$
"$\rho$ is idempotent only if it represents a pure state — indeed, this is a quick
way to test whether the state is pure" (Griffiths 3e §12.3.2, p.579). The lower
bound is $\gamma=1/d$, attained by the maximally mixed $I/d$ (using Cauchy–Schwarz
/ convexity). So $\gamma\in[1/d,1]$: $1$ is sharp (pure), $1/d$ is total mixing.
(`purity`, `is_pure`; `test_purity_pure_vs_mixed`, `test_idempotent_iff_pure`.)

## 3. Expectation values: $\langle A\rangle=\mathrm{Tr}(\rho A)$

Everything `~QM-06` computed from a ket can be computed from $\rho$. The
expectation value of an observable is (Griffiths 3e Eqs. 12.20, 12.29):
$$\boxed{\,\langle A\rangle=\mathrm{Tr}(\rho A)\,}$$
For a **pure** state this *is* the old formula: with $\rho=|\psi\rangle\langle\psi|$,
$$\mathrm{Tr}(\rho A)=\sum_n\langle n|\psi\rangle\langle\psi|A|n\rangle
=\langle\psi|A\Big(\sum_n|n\rangle\langle n|\Big)|\psi\rangle=\langle\psi|A|\psi\rangle,$$
using completeness. For a **mixed** state it is the average over the ensemble of
*differently* prepared systems (Griffiths 3e Eq. 12.28, p.579):
$$\mathrm{Tr}(\rho A)=\sum_i p_i\,\mathrm{Tr}\big(|\psi_i\rangle\langle\psi_i|A\big)
=\sum_i p_i\,\langle\psi_i|A|\psi_i\rangle.$$
This is the bridge back to `~QM-06`: a mixed state literally *packages measurement
statistics* — the $p_i$ are classical probabilities layered on top of the quantum
Born probabilities. For a Hermitian $A$ the result is real (since $\rho$ and $A$
are Hermitian). (`expectation`; `test_expectation_pure_equals_braket`,
`test_expectation_mixed_is_ensemble_average`.)

## 4. Subsystems & the partial trace — entanglement makes parts mixed

Now the deep reason a state can be mixed even when *nothing* is unknown. Take an
**entangled** pure state of two systems $A,B$, e.g. the singlet/Bell pair. The
joint $\rho_{AB}=|\Psi\rangle\langle\Psi|$ is pure (we know it exactly). But what
is the state of $A$ *alone*? It is the **reduced density matrix**, obtained by the
**partial trace** over $B$ (Griffiths 3e §12.3.3, p.582):
$$\boxed{\,\rho_A=\mathrm{Tr}_B\,\rho_{AB}\,},\qquad
\langle a|\rho_A|a'\rangle=\sum_b\langle a,b|\rho_{AB}|a',b\rangle.$$
Its **defining property** is that $\rho_A$ reproduces every measurement confined
to $A$:
$$\mathrm{Tr}\!\big[(A\otimes I_B)\,\rho_{AB}\big]=\mathrm{Tr}\!\big[A\,\rho_A\big]
\quad\text{for all }A.$$
(That property *is* the definition; the code verifies it directly.)

**The signature of entanglement.** Take the Bell state
$$|\Phi^+\rangle=\frac{1}{\sqrt2}\big(|00\rangle+|11\rangle\big),\qquad
\rho_{AB}=|\Phi^+\rangle\langle\Phi^+|\ \ (\text{pure},\ S=0).$$
Tracing out qubit $B$:
$$\rho_A=\mathrm{Tr}_B\,\rho_{AB}=\tfrac12|0\rangle\langle0|+\tfrac12|1\rangle\langle1|
=\frac{I}{2}.$$
The subsystem is **maximally mixed** — purity $\tfrac12$, $S=\ln2$ — even though
the whole is pure. Griffiths puts it exactly: "the subsystem… by itself does not
occupy a pure state. This has nothing to do with ignorance; I know the state of
the system precisely" (§12.3.3, p.582). Contrast a **product** state
$|a\rangle\otimes|b\rangle$ (no entanglement): then $\rho_A=|a\rangle\langle a|$
stays **pure**, $S=0$. So *the reduced state is mixed iff the global pure state is
entangled* — the operational handle that `~QM-21` builds entanglement measures on.
(`partial_trace`; `test_partial_trace_defining_property`,
`test_bell_subsystem_is_maximally_mixed`, `test_product_subsystem_stays_pure`.)

## 5. von Neumann entropy — how mixed is a state?

The amount of mixedness is measured by the **von Neumann entropy**
$$\boxed{\,S(\rho)=-\mathrm{Tr}(\rho\ln\rho)=-\sum_k\lambda_k\ln\lambda_k\,}$$
(with the convention $0\ln0=0$). It is the Shannon entropy of the eigenvalue
distribution $\{\lambda_k\}$, so:

- $S=0\Longleftrightarrow$ one $\lambda_k=1$ $\Longleftrightarrow$ **pure**;
- $S$ is **maximal**, $S=\ln d$, at the maximally mixed state $I/d$ (uniform
  populations);
- $S$ depends only on the **spectrum**, hence is **invariant under any unitary**
  $S(U\rho U^\dagger)=S(\rho)$.

For a qubit the range is $S\in[0,\ln2]$; in *bits* (log base 2) the maximally
mixed qubit carries exactly $1$ bit. The Bell example above is the cleanest story:
$S(\rho_{AB})=0$ (pure whole) but $S(\rho_A)=\ln2$ (maximally uncertain part) —
the **entanglement entropy**. (`von_neumann_entropy`;
`test_entropy_pure_zero_mixed_positive`, `test_entropy_maximally_mixed_is_log_d`,
`test_entropy_unitarily_invariant`.)

> *Citation honesty:* Griffiths 3e does **not** define the von Neumann entropy
> (the word "entropy" does not appear in Ch. 12). The formula is standard
> (von Neumann 1927; see Sakurai §3.4, *Density Operators…*, unpinned — image-only
> scan), and **the verification here is the code**: the entropy of $I/d$ is
> checked to equal $\ln d$, the pure-state entropy to vanish, and unitary
> invariance to hold, all against closed forms.

## 6. Time evolution — the von Neumann equation & decoherence

How does $\rho$ evolve? For a pure state $|\psi(t)\rangle=U(t)|\psi(0)\rangle$
with $U=e^{-iHt/\hbar}$, so $\rho=|\psi\rangle\langle\psi|\to U\rho U^\dagger$.
Differentiating, $i\hbar\,\dot\rho=H\rho-\rho H$. The same holds for a mixture
(each component evolves with the same $U$). This is the **von Neumann equation**
(Griffiths 3e Prob. 12.4(b), p.577 — "the Schrödinger equation, expressed in
terms of $\rho$"):
$$\boxed{\,i\hbar\,\dot\rho=[H,\rho]\,}\qquad\Longrightarrow\qquad
\rho(t)=U(t)\,\rho(0)\,U^\dagger(t),\quad U(t)=e^{-iHt/\hbar}.$$
Note the **sign** is opposite to the Heisenberg equation for operators — $\rho$ is
a state, not an observable.

Consequences, all verified in code:

- **Unitary $\Rightarrow$ spectrum-preserving.** $\rho(t)$ and $\rho(0)$ are
  unitarily similar, so they share eigenvalues. Therefore **purity and entropy
  are constant**, and a **pure state stays pure forever**
  (`test_unitary_evolution_conserves_purity_and_trace`). A *closed* system cannot
  spontaneously become mixed.
- **Stationarity $\Leftrightarrow$ commuting with $H$.** $\dot\rho=0
  \Leftrightarrow[H,\rho]=0$, i.e. $\rho$ is **diagonal in the energy
  eigenbasis** (a mixture of stationary states). Energy eigenstate populations
  are frozen; only the off-diagonal energy coherences rotate, with phases
  $e^{-i(E_m-E_n)t/\hbar}$ (`test_stationary_state_commutes_with_H`,
  `test_von_neumann_equation_finite_difference`).
- **Decoherence.** In an **open** system coupled to an environment, those
  off-diagonal coherences are damped to zero — the state becomes effectively
  diagonal (classical). "This phenomenon is called decoherence… the fundamental
  mechanism by which quantum mechanics reduces to classical mechanics in the
  macroscopic realm" (Griffiths 3e §12.5, p.586). Modelling that decay
  *irreversibly* requires adding Lindblad dissipators to the von Neumann equation
  — the Lindblad master equation of the unbuilt `~QO-04`. Unitary evolution alone
  (this module) can only *rotate* coherences, never destroy purity.

---
### Where this sits
`~QM-05` gave the operator/trace formalism and `~QM-06` the measurement
statistics; this module fuses them into the density operator, the state object for
*incomplete* knowledge — whether from classical ignorance (§1–§3) or from
entanglement (§4). The partial-trace mixedness of §4 is the operational signature
that `~QM-21` (entanglement & Bell) builds on; the entropy of §5 is its measure;
and the unitary $i\hbar\dot\rho=[H,\rho]$ of §6 is the closed-system limit of the
open-system master equations of `~QO-04`, where decoherence becomes irreversible.
