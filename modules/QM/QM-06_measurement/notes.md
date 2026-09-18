# QM-06 — Measurement postulates (notes)

By `~QM-02` we have a normalized state $|\psi\rangle$ whose modulus-squared is a
probability density (Born), and by `~QM-05` a Hilbert space with Hermitian
operators acting on it. What is still missing is the bridge between the *state*
and an *experiment*: what does a measuring device read, with what probability,
and what happens to the state afterwards? That bridge is the **measurement
postulates** — for Griffiths the centrepiece is the *generalized statistical
interpretation* (Griffiths 3e §3.4, p.133).

The thread of this module: an experiment is a **Hermitian operator**; its
**eigenvalues** are the dial readings; the state's **overlap** with each
eigenvector gives the probability; the act of reading **collapses** the state to
the corresponding eigenvector; and whether two experiments can be done without
spoiling each other is decided by their **commutator**.

## 1. An observable is a Hermitian operator

Postulate: every measurable quantity $A$ (position, momentum, energy, a spin
component) is represented by a Hermitian operator $\hat A=\hat A^\dagger$ acting
on the state space (Griffiths 3e §3.2.1, p.123). Hermiticity is not decoration —
it is forced by two physical demands:

- **Real readings.** The expectation value $\langle A\rangle=\langle\psi|\hat
  A\psi\rangle$ is an average of real meter readings, so it must be real for
  *every* $\psi$. $\langle\psi|\hat A\psi\rangle=\langle\hat A\psi|\psi\rangle$
  for all $\psi$ is exactly the statement $\hat A=\hat A^\dagger$ (Griffiths 3e
  §3.2.1, p.123).
- **A complete set of outcomes.** The spectral theorem (`~MA-04`) says a
  Hermitian operator has *real* eigenvalues and an *orthonormal, complete* set of
  eigenvectors,
  $$\hat A|a_n\rangle=a_n|a_n\rangle,\qquad \langle a_m|a_n\rangle=\delta_{mn},
  \qquad \sum_n|a_n\rangle\langle a_n|=\mathbb{1}.$$
  (Griffiths 3e §3.3, p.127, discrete case.) In code: `eigensystem` returns the
  real eigenvalues and orthonormal eigenvectors via `numpy.linalg.eigh`;
  `test_eigenbasis_orthonormal_and_complete` checks $V^\dagger V=VV^\dagger=
  \mathbb{1}$ and rebuilds $\hat A=\sum_n a_n|a_n\rangle\langle a_n|$.

## 2. A measurement yields an eigenvalue

Postulate: a measurement of $A$ can only ever return one of the eigenvalues
$a_n$ of $\hat A$ (Griffiths 3e §3.4, p.133). The classical idea that an
observable has a sharp value waiting to be read is gone; what is sharp is the
*spectrum* of allowed readings.

A state for which the reading is certain is a **determinate state**: every
measurement gives the same $q$, so the standard deviation vanishes,
$$\sigma_A^2=\langle(\hat A-\langle A\rangle)^2\rangle=0
\;\Longleftrightarrow\; \hat A|\psi\rangle=q|\psi\rangle.$$
That is precisely the eigenvalue equation (Griffiths 3e §3.2.2, p.125):
**determinate states are eigenstates, and the certain values are eigenvalues.**
(`variance`, `test_variance_nonneg_and_determinacy`,
`test_eigenstate_is_determinate`.)

## 3. The generalized statistical interpretation: $P(a_n)=|\langle a_n|\psi\rangle|^2$

Postulate (the heart of the module): expand the state in the eigenbasis of the
observable being measured,
$$|\psi\rangle=\sum_n c_n|a_n\rangle,\qquad c_n=\langle a_n|\psi\rangle,$$
then a measurement of $A$ yields the eigenvalue $a_n$ with probability
$$\boxed{\,P(a_n)=|\langle a_n|\psi\rangle|^2=|c_n|^2\,}$$
(Griffiths 3e §3.4, p.133, Eq. 3.43). This is `~QM-02`'s Born rule, now read in
the *eigenbasis of the measured operator* rather than in position space — the
same rule, generalized to any observable.

Normalization makes the probabilities a distribution:
$$\sum_n P(a_n)=\sum_n|c_n|^2=\langle\psi|\Big(\sum_n|a_n\rangle\langle a_n|\Big)|\psi\rangle
=\langle\psi|\psi\rangle=1,$$
using completeness from §1. (`outcome_probabilities`,
`test_probabilities_sum_to_one`, `test_born_rule_nondegenerate`.)

**Degeneracy.** If $a$ is $d$-fold degenerate, the probability is the weight in
the whole eigenspace, $P(a)=\langle\psi|\hat P_a|\psi\rangle=\lVert\hat P_a
\psi\rVert^2$, where $\hat P_a=\sum_{k}|a^{(k)}\rangle\langle a^{(k)}|$ projects
onto it. This reduces to $|c_n|^2$ when the level is non-degenerate. The code
works at the level of these eigenspace projectors throughout (`eigenspaces`), so
degeneracy is handled correctly by construction
(`test_degenerate_projector_weight_and_collapse`).

## 4. Expectation value — two equal routes

The mean reading over many identically prepared systems is the expectation value.
It can be written two ways:
$$\langle A\rangle=\sum_n a_n\,P(a_n)\qquad\text{(average of outcomes)}$$
$$\langle A\rangle=\langle\psi|\hat A|\psi\rangle\qquad\text{(sandwich the operator).}$$
They are identically equal: insert $|\psi\rangle=\sum_n c_n|a_n\rangle$ into the
sandwich,
$$\langle\psi|\hat A|\psi\rangle=\sum_{m,n}c_m^*c_n\,a_n\langle a_m|a_n\rangle
=\sum_n a_n|c_n|^2=\sum_n a_n P(a_n).$$
(Griffiths 3e §3.4, p.134, Eqs. 3.48–3.51; the sandwich form is introduced
already for $\langle x\rangle$ and $\langle p\rangle$ in §1.5, p.32–33.)

> **Ensemble caveat (Griffiths 3e §1.5, p.32).** $\langle A\rangle$ is *not* the
> time-average of repeated measurements on *one* system — after the first
> measurement the state has collapsed (§5) and subsequent quick measurements just
> repeat it. It is the average over an *ensemble* of systems each freshly
> prepared in $|\psi\rangle$.

The code computes both forms and asserts they agree, so a successful call is a
numerical proof of the identity for that $(\psi,\hat A)$ (`expectation`,
`test_expectation_two_ways`). For the spin-$\tfrac12$ state pointing at
$(\theta,\phi)$ this gives the clean projection law
$\langle\sigma_z\rangle=\cos\theta$, $\langle\sigma_x\rangle=\sin\theta\cos\phi$,
$\langle\sigma_y\rangle=\sin\theta\sin\phi$ (`test_spin_expectation_law`) — the
spin-$\tfrac12$ cousin of Malus's law.

## 5. Collapse — the state jumps to the measured eigenstate

Postulate: immediately after a measurement that returns $a_n$, the state is no
longer $|\psi\rangle$ but the **normalized projection onto that eigenspace**,
$$\boxed{\,|\psi\rangle\;\longrightarrow\;|\psi'\rangle=\frac{\hat P_n|\psi\rangle}{\lVert\hat P_n|\psi\rangle\rVert}\,}$$
(Griffiths 3e §3.4, p.133: *"the wave function collapses to the corresponding
eigenstate"*; non-degenerate case $|\psi'\rangle=|a_n\rangle$).

The signature of collapse is **idempotence/reproducibility**: $|\psi'\rangle$ is
now a determinate state of $\hat A$, so an immediate re-measurement returns the
same $a_n$ with probability $1$:
$$P'(a_n)=\lVert\hat P_n|\psi'\rangle\rVert^2=1.$$
(`collapse`, `measure`; `test_collapse_idempotent`.) This is what makes a
measurement *repeatable* and is the discontinuous, non-unitary partner to the
smooth Schrödinger evolution of `~QM-03`. (Whether collapse is "physical" or an
update of knowledge is the measurement problem; the density-matrix /
decoherence view is taken up in `~QM-20`.)

## 6. Compatible vs incompatible — when measurements disturb each other

Can two observables both have sharp values at once? Only if they share an
eigenbasis. Griffiths 3e §3.5.1 (p.139) states it directly:

> *"Incompatible observables do not have shared eigenfunctions… By contrast,
> compatible (commuting) observables do admit complete sets of simultaneous
> eigenfunctions."*

So the decisive object is the **commutator** $[\hat A,\hat B]=\hat A\hat B-\hat
B\hat A$ (`~QM-05`, `~CM-20` via the Poisson-bracket→commutator bridge):

- **Compatible** ($[\hat A,\hat B]=0$): a simultaneous eigenbasis exists.
  Measuring $A$, then $B$, then $A$ returns the *original* $A$-value with
  certainty — the intervening $B$ does no damage, because the post-$A$ state is
  already a $B$-eigenstate and the post-$B$ state is still the same
  $A$-eigenstate. (`commute`; `test_compatible_no_disturbance`.)
- **Incompatible** ($[\hat A,\hat B]\neq0$): no common eigenbasis. Measuring $B$
  in between *re-randomizes* $A$. The textbook case is spin: from the Pauli
  algebra
  $$[\sigma_x,\sigma_y]=2i\sigma_z,\quad[\sigma_y,\sigma_z]=2i\sigma_x,\quad
  [\sigma_z,\sigma_x]=2i\sigma_y,$$
  so $\sigma_x$ and $\sigma_z$ do not commute. Prepare $|{+x}\rangle$ (so a
  $\sigma_x$ measurement gives $+1$ for sure); measure $\sigma_z$ (collapses to
  $|0\rangle$, a $50/50$ event); then measure $\sigma_x$ again — the once-certain
  $+1$ is now $50/50$. (`test_incompatible_randomized`, `test_pauli_commutators`.)

The *quantitative* version of this disturbance is the generalized uncertainty
principle $\sigma_A\sigma_B\ge\tfrac12|\langle[\hat A,\hat B]\rangle|$ proved in
Griffiths 3e §3.5.1 (p.138) — that is the subject of `~QM-07`.

---
### Where this sits
`~QM-02` gave the Born rule for position; `~QM-05` gave the operator formalism.
This module fuses them into the rules for *any* measurement: Hermitian operator →
eigenvalue spectrum → $|c_n|^2$ probabilities → expectation → collapse →
(in)compatibility. The disturbance seen in §6 is sharpened into the uncertainty
principle in `~QM-07`; the spin example is developed fully in `~QM-11`; and the
collapse/ensemble questions of §4–§5 are reformulated with the density matrix in
`~QM-20`.
