# QM-05 — Formalism (notes)

Quantum theory rests on two constructs: **wave functions** (the *state*) and
**operators** (the *observables*). Wave functions satisfy the defining conditions
for abstract vectors, and operators act on them as linear transformations — so,
as Griffiths puts it, *"the natural language of quantum mechanics is linear
algebra"* (Griffiths 3e §3.1, p.119). This module makes that sentence literal:
states are column vectors, observables are matrices, and every physical statement
becomes a verifiable statement of linear algebra.

## 1. Hilbert space and the inner product

A **Hilbert space** $\mathcal H$ is a complex vector space with an inner product
that is complete (every Cauchy sequence converges). For square-integrable
functions on an interval — physicists' $L^2$, "Hilbert space" — the inner product
is (Griffiths §3.1, Eq. 3.6, p.120)
$$\langle f|g\rangle \;=\; \int f(x)^{*}\,g(x)\,dx .$$
The finite-dimensional shadow, which the code uses throughout, replaces the
integral by a sum over components in an orthonormal basis:
$$\boxed{\;\langle\phi|\psi\rangle=\sum_i \phi_i^{*}\,\psi_i\;}$$
The conjugation sits on the **bra** (first slot), making the product
*conjugate-linear* in $\phi$ and *linear* in $\psi$, and giving conjugate
symmetry (Griffiths Eq. 3.8, p.120)
$$\langle\phi|\psi\rangle=\langle\psi|\phi\rangle^{*}.$$
Consequently $\langle\psi|\psi\rangle=\sum_i|\psi_i|^2$ is **real and
non-negative**, zero only for the zero vector, so $\|\psi\|=\sqrt{\langle\psi|\psi\rangle}$
is a genuine length. A state is **normalized** if $\langle\psi|\psi\rangle=1$, two
states are **orthogonal** if $\langle\phi|\psi\rangle=0$, and a basis $\{|e_i\rangle\}$
is **orthonormal** if $\langle e_i|e_j\rangle=\delta_{ij}$ (Griffiths p.120).
*(Verified: `test_inner_product_conjugate_symmetry`, `test_inner_product_sesquilinearity`,
`test_norm_real_nonnegative_and_value`.)*

## 2. Dirac notation: bras, kets, and the dual space

Dirac "chopped the bracket" $\langle\phi|\psi\rangle$ into a **bra** $\langle\phi|$
and a **ket** $|\psi\rangle$ (Griffiths §3.6.2, p.152). A ket is a vector
(a column); a bra is a *linear functional* — it eats a ket and returns the
complex number $\langle\phi|\psi\rangle$. The bras form the **dual space**; in
matrix terms the ket is a column and the bra is the conjugate-transposed row, so
$\langle\phi|\psi\rangle$ is just the matrix product (a row times a column).

The killer app of the notation is the **outer product** $|\psi\rangle\langle\psi|$,
an *operator*. For a normalized $|n\rangle$ the **projector**
$$\hat P_n=|n\rangle\langle n|$$
picks out the part of any vector lying along $|n\rangle$; it is Hermitian and
idempotent, $\hat P_n^2=\hat P_n$ (Griffiths Eq. 3.92, p.152). If $\{|n\rangle\}$
is a complete orthonormal basis, the projectors sum to the identity — the
**resolution of identity / completeness relation**
$$\boxed{\;\sum_n |n\rangle\langle n| = \hat I\;}$$
(Griffiths Eq. 3.93, p.152). Inserting $\hat I$ between things is how you expand a
state, $|\psi\rangle=\sum_n c_n|n\rangle$ with $c_n=\langle n|\psi\rangle$, and is
the workhorse of every later calculation. *(Verified:
`test_projector_is_hermitian_idempotent`, `test_resolution_of_identity`.)*

## 3. Linear operators and their matrix representation

An operator $\hat A$ takes a vector and returns a vector, $\hat A|\psi\rangle=|\psi'\rangle$,
linearly. Relative to an orthonormal basis it is a **matrix** with elements
$A_{mn}=\langle m|\hat A|n\rangle$, and operator composition is matrix
multiplication; in general $\hat A\hat B\neq\hat B\hat A$ (Griffiths p.153). The
**Hermitian conjugate (adjoint)** $\hat A^\dagger$ is the conjugate transpose,
defined by $\langle\phi|\hat A\psi\rangle=\langle \hat A^\dagger\phi|\psi\rangle$;
it reverses products,
$$(\hat A\hat B)^\dagger=\hat B^\dagger \hat A^\dagger,\qquad (\hat A^\dagger)^\dagger=\hat A$$
(Griffiths Problem 3.5(b), p.124; the same "hermitian conjugate" language he uses
for the ladder operators, p.63). *(Verified: `test_dagger_involution_and_reversal`.)*

## 4. Hermitian operators are the observables

The expectation value of an observable in state $|\psi\rangle$ is
$\langle Q\rangle=\langle\psi|\hat Q|\psi\rangle$ (Griffiths Eq. 3.13, p.123). A
measurement outcome — and therefore its average — *must be real*, so
$\langle Q\rangle=\langle Q\rangle^{*}$ for **every** state. Because complex
conjugation reverses an inner product, this forces
$$\boxed{\;\hat Q=\hat Q^\dagger\;}$$
— the operator is **Hermitian** (Griffiths §3.2.1, Eqs. 3.16–3.17, p.123).
Hermiticity is thus not a convenience but the precise mathematical encoding of
"this quantity is measurable, and its values are real." Position $\hat x$ and the
Hamiltonian $\hat H$ are Hermitian (Griffiths Problem 3.4(d), p.124).
*(Verified: `test_is_hermitian`, `test_hermitian_has_real_expectation_values`.)*

## 5. The spectral theorem

The eigenvectors of a Hermitian operator are its **determinate states** — states
in which the observable has no spread, $\hat Q|n\rangle=\lambda_n|n\rangle$
(Griffiths §3.3, p.127). Two theorems make them the bedrock of measurement
(Griffiths §3.3.1, p.128):

- **Theorem 1 — real eigenvalues.** From $\hat Q|n\rangle=\lambda_n|n\rangle$ and
  Hermiticity, $\lambda_n\langle n|n\rangle=\langle n|\hat Q|n\rangle=\langle\hat Q n|n\rangle=\lambda_n^{*}\langle n|n\rangle$,
  so $\lambda_n=\lambda_n^{*}\in\mathbb R$. Good: a measurement returns a real
  number.
- **Theorem 2 — orthogonal eigenvectors.** For $\lambda_m\neq\lambda_n$,
  $\lambda_n\langle m|n\rangle=\langle m|\hat Q n\rangle=\langle\hat Q m|n\rangle=\lambda_m\langle m|n\rangle$,
  and since $\lambda_m\neq\lambda_n$ we need $\langle m|n\rangle=0$. (Degenerate
  eigenvalues can be orthogonalized within their subspace.)

Together: a Hermitian operator has a **complete orthonormal eigenbasis** with
real eigenvalues, and can be written in its **spectral form**
$$\boxed{\;\hat A=\sum_n \lambda_n\,|n\rangle\langle n|\;}$$
i.e. $A=V\Lambda V^\dagger$ with $V$ unitary (columns = eigenvectors) and
$\Lambda=\mathrm{diag}(\lambda_n)$. This is exactly MA-04's diagonalization, now
for complex Hermitian matrices. *(Verified: `test_spectral_theorem_real_eigenvalues`,
`test_spectral_theorem_orthonormal_eigenvectors`, `test_spectral_reconstruction`.)*

## 6. Commutators and compatible observables

The **commutator**
$$\boxed{\;[\hat A,\hat B]=\hat A\hat B-\hat B\hat A\;}$$
measures how badly two operators fail to commute (Griffiths Eq. 2.48, p.59). It
is antisymmetric, $[\hat A,\hat B]=-[\hat B,\hat A]$, bilinear, and obeys the
**Jacobi identity**
$$[\hat A,[\hat B,\hat C]]+[\hat B,[\hat C,\hat A]]+[\hat C,[\hat A,\hat B]]=0,$$
so operators under the commutator form a **Lie algebra**. The commutator of two
Hermitian operators is *anti*-Hermitian, $[\hat A,\hat B]^\dagger=-[\hat A,\hat B]$,
so $i[\hat A,\hat B]$ is again Hermitian — which is why the commutator appears
*with a factor of $i$* in the generalized uncertainty principle (Griffiths
§3.5, p.139). *(Verified: `test_commutator_definition_and_antisymmetry`,
`test_jacobi_identity`, `test_commutator_of_hermitians_is_anti_hermitian`.)*

The physics of commuting: **compatible (commuting) observables admit a complete
set of simultaneous eigenvectors**; incompatible (non-commuting) ones do not
(Griffiths §3.5, p.139). The proof both ways: if $[\hat A,\hat B]=0$ and $\hat A$
is non-degenerate, then $\hat A(\hat B|n\rangle)=\hat B\hat A|n\rangle=\lambda_n(\hat B|n\rangle)$,
so $\hat B|n\rangle$ is again an eigenvector of $\hat A$ with eigenvalue
$\lambda_n$, hence proportional to $|n\rangle$ — i.e. $|n\rangle$ is also an
eigenvector of $\hat B$. In the code we build $\hat A=U D_1 U^\dagger$ and
$\hat B=U D_2 U^\dagger$ from a **common** unitary $U$: they commute, and $\hat A$'s
eigenbasis diagonalizes $\hat B$. Two *generic* Hermitian matrices do neither.
*(Verified: `test_compatible_observables_share_eigenbasis`,
`test_incompatible_observables_do_not_share_eigenbasis`.)*

## 7. The canonical commutator $[\hat x,\hat p]=i\hbar$

Acting on a test function, $[\hat x,\hat p]f=x(-i\hbar f') -(-i\hbar)(xf)'=i\hbar f$,
so (Griffiths Eq. 2.52, p.60)
$$\boxed{\;[\hat x,\hat p]=i\hbar\;}$$
— the **canonical commutation relation**, the algebraic seed of the entire
theory (it gives the uncertainty principle on p.139, and the harmonic-oscillator
ladder on p.60). We build $\hat x,\hat p$ in the harmonic-oscillator **number
basis** $|0\rangle,|1\rangle,\dots$ from the ladder operators (Griffiths §2.3.1,
p.59–65):
$$a|n\rangle=\sqrt n\,|n-1\rangle,\quad a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle,
\quad a^\dagger=a^{\dagger}\ \text{(the adjoint of }a,\ \text{p.63)},$$
$$\hat x=\sqrt{\tfrac{\hbar}{2m\omega}}\,(a+a^\dagger),\qquad
\hat p=i\sqrt{\tfrac{\hbar m\omega}{2}}\,(a^\dagger-a).$$
A short calculation gives $[\hat x,\hat p]=i\hbar\,[a,a^\dagger]$, and in infinite
dimensions $[a,a^\dagger]=I$, recovering $i\hbar I$.

### The honest finite-dimensional caveat
A computer can only hold an $N\times N$ truncation, and **there
$[\hat x,\hat p]=i\hbar$ cannot hold exactly.** The reason is a one-line theorem:
the trace of any commutator of finite matrices vanishes,
$\mathrm{tr}[\hat A,\hat B]=\mathrm{tr}(\hat A\hat B)-\mathrm{tr}(\hat B\hat A)=0$,
whereas $\mathrm{tr}(i\hbar I)=i\hbar N\neq0$. So $[\hat x,\hat p]=i\hbar I$ is
*algebraically impossible* in finite dimensions (Wintner 1947, Wielandt 1949) —
the canonical commutation relation has only infinite-dimensional
representations.

Concretely, the number operator $a^\dagger a=\mathrm{diag}(0,1,\dots,N-1)$ is
*exact*, but $a a^\dagger$ loses its top contribution (the rung $a^\dagger|N-1\rangle$
would land on the discarded $|N\rangle$), so
$$[a,a^\dagger]=I-N\,|N{-}1\rangle\langle N{-}1|,\qquad\text{hence}\qquad
[\hat x,\hat p]=i\hbar\big(I-N\,|N{-}1\rangle\langle N{-}1|\big).$$
This is **$i\hbar$ exactly on the $(N{-}1)$-dimensional interior block**, with the
*only* deviation the bottom-right corner, which reads $-i\hbar(N-1)$. (Its trace
$i\hbar[(N-1)-(N-1)]=0$, as it must.) The test therefore checks **only the
interior block** equals $i\hbar I_{N-1}$, and *separately* verifies the corner is
exactly the predicted $-i\hbar(N-1)$ and that the trace is $0\neq i\hbar N$. We
never assert the false exact identity. *(Verified:
`test_ladder_relations`, `test_canonical_commutator_holds_on_interior`,
`test_canonical_commutator_truncation_artifact`.)*

---
### Why this is the trunk's spine
Everything downstream is this algebra in action: **measurement** (`~QM-06`) reads
off eigenvalues with probabilities $|\langle n|\psi\rangle|^2$; **ladder
operators** (`~QM-09`) exploit $[a,a^\dagger]=1$; the **uncertainty principle**
is $i[\hat A,\hat B]$ bounded below. And the bridge to classical mechanics,
**B7** (`~CM-20`), is the dictionary $\{A,B\}\to\frac{1}{i\hbar}[A,B]$: the
classical Poisson bracket $\{x,p\}=1$ becomes precisely $[\hat x,\hat p]=i\hbar$.
