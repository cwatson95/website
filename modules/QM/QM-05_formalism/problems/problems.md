# QM-05 — Problems

Work them by hand, then check with `code/formalism.py`. Sources in `../refs.md`.
All `Check:` snippets assume `from formalism import *` and `import numpy as np`.

### P1.  Conjugate symmetry of the inner product
Show from $\langle\phi|\psi\rangle=\sum_i\phi_i^{*}\psi_i$ that
$\langle\phi|\psi\rangle=\langle\psi|\phi\rangle^{*}$, and hence that
$\langle\psi|\psi\rangle$ is real. *(Griffiths 3e §3.1, Eq. 3.8, p.120.)*
*Answer:* swapping the arguments conjugates every term; with $\phi=\psi$ the sum
is $\sum|\psi_i|^2\ge0$.
*Check:* `inner_product([1,1j],[1,2])` $=1-2j$ while `inner_product([1,2],[1,1j])`
$=1+2j$. (`test_inner_product_conjugate_symmetry`.)

**Solution.** Start from the definition $\langle\phi|\psi\rangle=\sum_i\phi_i^{*}\psi_i$ and
swap the arguments:
$$\langle\psi|\phi\rangle=\sum_i\psi_i^{*}\phi_i\;\Longrightarrow\;
\langle\psi|\phi\rangle^{*}=\sum_i\psi_i\phi_i^{*}=\sum_i\phi_i^{*}\psi_i=\langle\phi|\psi\rangle,$$
which is conjugate symmetry. Setting $\phi=\psi$ gives $\langle\psi|\psi\rangle=\sum_i\phi_i^{*}\psi_i\big|_{\phi=\psi}=\sum_i|\psi_i|^2$,
a sum of non-negative reals, so it is real and $\ge0$. Numerically the bra is conjugated:
`inner_product([1,1j],[1,2])` $=1^{*}\cdot1+(i)^{*}\cdot2=1-2i$, while reversing the slots gives
$1+2i$ — the conjugate, exactly as the check reports.

### P2.  Why observables are Hermitian
An observable's expectation value $\langle Q\rangle=\langle\psi|\hat Q|\psi\rangle$
must be real for *every* state. Show this forces $\hat Q=\hat Q^\dagger$.
*(Griffiths 3e §3.2.1, Eqs. 3.16–3.17, p.123.)*
*Answer:* $\langle Q\rangle=\langle Q\rangle^{*}$ for all $\psi$ means
$\langle\psi|\hat Q\psi\rangle=\langle\hat Q\psi|\psi\rangle=\langle\psi|\hat Q^\dagger\psi\rangle$
for all $\psi$, i.e. $\hat Q=\hat Q^\dagger$.
*Check:* for Hermitian `A`, `expectation(A, psi).imag` $\approx0$; for a generic
matrix it is nonzero. (`test_hermitian_has_real_expectation_values`.)

**Solution.** Reality of $\langle Q\rangle=\langle\psi|\hat Q\psi\rangle$ means $\langle Q\rangle=\langle Q\rangle^{*}$.
Conjugate symmetry turns the right side into a statement about the adjoint:
$$\langle\psi|\hat Q\psi\rangle^{*}=\langle\hat Q\psi|\psi\rangle=\langle\psi|\hat Q^\dagger\psi\rangle,$$
using $\langle\hat Q\psi|\psi\rangle=\langle\psi|\hat Q^\dagger\psi\rangle$ from the definition of $\hat Q^\dagger$.
So $\langle\psi|(\hat Q-\hat Q^\dagger)\psi\rangle=0$ for **every** $\psi$; polarization (apply it to $\psi+\phi$ and
$\psi+i\phi$) extends this to all matrix elements $\langle\phi|(\hat Q-\hat Q^\dagger)\psi\rangle=0$, forcing
$\hat Q=\hat Q^\dagger$. Hence `expectation(A, psi).imag` $\approx0$ exactly when `A` is Hermitian, and is
nonzero for a generic matrix.

### P3.  Spectral theorem (Theorems 1 & 2)
Prove that a Hermitian operator has (1) real eigenvalues and (2) orthogonal
eigenvectors for distinct eigenvalues, and conclude $\hat A=\sum_n\lambda_n|n\rangle\langle n|$.
*(Griffiths 3e §3.3.1, p.128; spectral form §3.6, p.152.)*
*Answer:* (1) $\lambda\langle n|n\rangle=\langle n|\hat A n\rangle=\langle\hat A n|n\rangle=\lambda^{*}\langle n|n\rangle\Rightarrow\lambda=\lambda^{*}$.
(2) $\lambda_n\langle m|n\rangle=\langle m|\hat A n\rangle=\langle\hat A m|n\rangle=\lambda_m\langle m|n\rangle$,
so $\langle m|n\rangle=0$ when $\lambda_m\neq\lambda_n$.
*Check:* `w, V = spectral_decomposition(random_hermitian(8, seed=42))`; then
`np.allclose(w.imag, 0)`, `np.allclose(dagger(V)@V, np.eye(8))`, and
`np.allclose(reconstruct_from_spectrum(w, V), random_hermitian(8, seed=42))`.
(`test_spectral_theorem_real_eigenvalues`, `..._orthonormal_eigenvectors`,
`test_spectral_reconstruction`.)

**Solution.** Let $\hat A|n\rangle=\lambda_n|n\rangle$ with $\hat A=\hat A^\dagger$.
*(1) Real eigenvalues:* $\lambda_n\langle n|n\rangle=\langle n|\hat A n\rangle=\langle\hat A n|n\rangle=\lambda_n^{*}\langle n|n\rangle$,
and $\langle n|n\rangle\neq0$, so $\lambda_n=\lambda_n^{*}\in\mathbb R$.
*(2) Orthogonality:* for $\lambda_m\neq\lambda_n$,
$$\lambda_n\langle m|n\rangle=\langle m|\hat A n\rangle=\langle\hat A m|n\rangle=\lambda_m^{*}\langle m|n\rangle=\lambda_m\langle m|n\rangle,$$
so $(\lambda_n-\lambda_m)\langle m|n\rangle=0\Rightarrow\langle m|n\rangle=0$. The eigenvectors thus form a
complete orthonormal basis, and inserting $\hat I=\sum_n|n\rangle\langle n|$ gives the spectral form
$\hat A=\hat A\hat I=\sum_n\lambda_n|n\rangle\langle n|$. The check confirms `w.imag`$\approx0$,
`dagger(V)@V`$=I$, and `reconstruct_from_spectrum(w,V)` rebuilds the matrix.

### P4.  Commutator algebra and the Jacobi identity
Show $[A,B]=-[B,A]$ and verify the Jacobi identity
$[A,[B,C]]+[B,[C,A]]+[C,[A,B]]=0$ (so operators form a Lie algebra).
*(Griffiths 3e Eq. 2.48, p.59.)*
*Answer:* antisymmetry is immediate from $AB-BA$; expanding the nine double
products in the Jacobi sum cancels them in pairs.
*Check:* `A,B,C = random_matrix(6,32),random_matrix(6,33),random_matrix(6,34)`;
`np.allclose(commutator(A,B), -commutator(B,A))`; the Jacobi combination is
$\approx0$. (`test_commutator_definition_and_antisymmetry`, `test_jacobi_identity`.)

**Solution.** Antisymmetry is immediate: $[A,B]=AB-BA=-(BA-AB)=-[B,A]$. For the Jacobi identity,
expand one term, $[A,[B,C]]=A(BC-CB)-(BC-CB)A=ABC-ACB-BCA+CBA$, and likewise for the two cyclic
rotations $A\to B\to C\to A$:
$$[B,[C,A]]=BCA-BAC-CAB+ACB,\qquad [C,[A,B]]=CAB-CBA-ABC+BAC.$$
Adding all three, each of the six orderings $ABC,ACB,\dots$ appears once with $+$ and once with $-$, so
the sum is $0$. Operators under $[\,\cdot\,,\cdot\,]$ therefore satisfy the Lie-algebra axioms, matching the
check that `commutator(A,B)`$=-$`commutator(B,A)` and the Jacobi combination $\approx0$.

### P5.  $i[A,B]$ is an observable
Show that for Hermitian $A,B$ the commutator $[A,B]$ is *anti*-Hermitian, so
$i[A,B]$ is Hermitian. *(This is why the uncertainty bound carries a factor $i$;
Griffiths 3e §3.5, p.139.)*
*Answer:* $[A,B]^\dagger=(AB-BA)^\dagger=B^\dagger A^\dagger-A^\dagger B^\dagger=BA-AB=-[A,B]$.
*Check:* with `A,B = random_hermitian(5,35), random_hermitian(5,36)`,
`is_hermitian(1j*commutator(A,B))` is `True`.
(`test_commutator_of_hermitians_is_anti_hermitian`.)

**Solution.** With $A=A^\dagger$ and $B=B^\dagger$, the adjoint reverses the product (and conjugates):
$$[A,B]^\dagger=(AB-BA)^\dagger=B^\dagger A^\dagger-A^\dagger B^\dagger=BA-AB=-[A,B],$$
so $[A,B]$ is **anti**-Hermitian. Multiplying by $i$ flips the sign that the dagger pulls through:
$$(i[A,B])^\dagger=\bar i\,[A,B]^\dagger=(-i)(-[A,B])=i[A,B],$$
so $i[A,B]$ is Hermitian — a genuine observable. This is the factor of $i$ in the generalized uncertainty
bound. Accordingly `is_hermitian(1j*commutator(A,B))` returns `True` for the random Hermitian pair.

### P6.  Compatible vs incompatible observables
Show that commuting Hermitian operators share a complete eigenbasis, while
non-commuting ones cannot. *(Griffiths 3e §3.5, p.139.)*
*Answer:* if $[A,B]=0$ and $A|n\rangle=\lambda_n|n\rangle$ (nondegenerate), then
$A(B|n\rangle)=\lambda_n(B|n\rangle)$, so $B|n\rangle\propto|n\rangle$: the
$|n\rangle$ diagonalize $B$ too. Generic Hermitian $A,B$ have $[A,B]\neq0$, so no
common eigenbasis exists.
*Check:* build `A = U@np.diag([1,2,3,4,5])@dagger(U)`,
`B = U@np.diag([-2,.5,7,1,3])@dagger(U)` with `U = haar_unitary(5, seed=50)`:
`np.linalg.norm(commutator(A,B))` $\approx0$, and `dagger(VA)@B@VA` is diagonal.
For `random_hermitian` pairs the off-diagonal is large.
(`test_compatible_observables_share_eigenbasis`,
`test_incompatible_observables_do_not_share_eigenbasis`.)

**Solution.** Suppose $[A,B]=0$ and $A|n\rangle=\lambda_n|n\rangle$ with $\lambda_n$ nondegenerate. Then
$$A\,(B|n\rangle)=B\,A|n\rangle=\lambda_n\,(B|n\rangle),$$
so $B|n\rangle$ is an eigenvector of $A$ with the same eigenvalue $\lambda_n$; nondegeneracy forces
$B|n\rangle\propto|n\rangle$, i.e. $B|n\rangle=\mu_n|n\rangle$. Thus the eigenbasis of $A$ diagonalizes $B$
simultaneously. The check builds $A=U\,\mathrm{diag}(1..5)\,U^\dagger$ and $B=U\,\mathrm{diag}(-2,.5,7,1,3)\,U^\dagger$
from a *common* $U$, so they commute (`np.linalg.norm(commutator(A,B))`$\approx1.3\times10^{-14}$) and $A$'s
eigenvectors $V_A$ render $V_A^\dagger B\,V_A$ diagonal. Two generic Hermitian matrices have $[A,B]\neq0$ and
no shared eigenbasis.

### P7.  Build $\hat x,\hat p$ from ladder operators and read off $[\hat x,\hat p]$
With $\hat x=\sqrt{\hbar/2m\omega}\,(a+a^\dagger)$ and
$\hat p=i\sqrt{\hbar m\omega/2}\,(a^\dagger-a)$, show
$[\hat x,\hat p]=i\hbar[a,a^\dagger]$, which is $i\hbar$ when $[a,a^\dagger]=1$.
*(Griffiths 3e §2.3.1, Example 2.5 p.65; canonical relation Eq. 2.52, p.60.)*
*Answer:* the prefactors multiply to $i\hbar/2$, and
$[a+a^\dagger,\,a^\dagger-a]=2[a,a^\dagger]$, giving $i\hbar[a,a^\dagger]$.
*Check:* on the interior of an $N=8$ truncation,
`canonical_commutator(8)[:7,:7]` $\approx i\,I_7$ (with $\hbar=1$).
(`test_canonical_commutator_holds_on_interior`, `test_ladder_relations`.)

**Solution.** The scalar prefactors multiply to
$$\sqrt{\tfrac{\hbar}{2m\omega}}\cdot i\sqrt{\tfrac{\hbar m\omega}{2}}=i\sqrt{\tfrac{\hbar^2}{4}}=\frac{i\hbar}{2},$$
and the operator part expands using $[a,a]=[a^\dagger,a^\dagger]=0$ and $[a^\dagger,a]=-[a,a^\dagger]$:
$$[a+a^\dagger,\;a^\dagger-a]=[a,a^\dagger]-[a^\dagger,a]=2[a,a^\dagger].$$
Therefore $[\hat x,\hat p]=\tfrac{i\hbar}{2}\cdot2[a,a^\dagger]=i\hbar\,[a,a^\dagger]$, which is $i\hbar$
wherever $[a,a^\dagger]=1$. With $\hbar=1$, `canonical_commutator(8)[:7,:7]`$\approx i\,I_7$ on the interior,
as the check confirms.

### P8.  The truncation artifact — why finite $[\hat x,\hat p]=i\hbar$ is impossible
Prove that no finite matrices satisfy $[\hat x,\hat p]=i\hbar I$, and identify
exactly where the $N$-level number-basis $[\hat x,\hat p]$ deviates from $i\hbar I$.
*(Mathematical theorem — Wintner 1947 / Wielandt 1949; see `../refs.md`.)*
*Answer:* $\mathrm{tr}[\hat x,\hat p]=0$ for any finite matrices, but
$\mathrm{tr}(i\hbar I)=i\hbar N\neq0$ — contradiction. Concretely
$[a,a^\dagger]=I-N|N{-}1\rangle\langle N{-}1|$, so $[\hat x,\hat p]=i\hbar(I-N|N{-}1\rangle\langle N{-}1|)$:
correct on the interior, but the bottom-right corner is $-i\hbar(N-1)$.
*Check:* `C = canonical_commutator(8)`; `abs(np.trace(C)) < 1e-9` (zero), while
`C[7,7]` $=-7i$ (the artifact, $=-i\hbar(N-1)$), and removing that one entry
leaves `C - 1j*np.eye(8)` $\approx0$.
(`test_canonical_commutator_truncation_artifact`.)

**Solution.** Any commutator of finite matrices is traceless, since $\mathrm{tr}(\hat x\hat p)=\mathrm{tr}(\hat p\hat x)$,
so $\mathrm{tr}[\hat x,\hat p]=0$; but $\mathrm{tr}(i\hbar I)=i\hbar N\neq0$ — the two cannot be equal, so
$[\hat x,\hat p]=i\hbar I$ has no finite-dimensional representation. The deviation is localized: $a^\dagger a=\mathrm{diag}(0,\dots,N-1)$
is exact, but $aa^\dagger$ loses the rung $a^\dagger|N-1\rangle$ (it would land on the discarded $|N\rangle$), giving
$$[a,a^\dagger]=I-N\,|N{-}1\rangle\langle N{-}1|\;\Longrightarrow\;[\hat x,\hat p]=i\hbar\big(I-N|N{-}1\rangle\langle N{-}1|\big).$$
So it is $i\hbar$ on the interior but the corner reads $-i\hbar(N-1)$. For $N=8$ the code gives
`np.trace(C)`$\approx0$ and `C[7,7]`$=-7i=-i\hbar(N-1)$; zeroing that one entry makes `C - 1j*np.eye(8)`$\approx0$.

### P9.  Resolution of the identity
For an orthonormal basis $\{|n\rangle\}$ show $\sum_n|n\rangle\langle n|=\hat I$,
and that this is the statement of completeness. *(Griffiths 3e §3.6.2, Eq. 3.93,
p.152.)*
*Answer:* acting on any $|\psi\rangle=\sum_m c_m|m\rangle$,
$\sum_n|n\rangle\langle n|\psi\rangle=\sum_n c_n|n\rangle=|\psi\rangle$.
*Check:* `V = haar_unitary(6, seed=12)`; `sum(projector(V[:,n]) for n in range(6))`
$\approx I_6$. (`test_resolution_of_identity`.)

**Solution.** Let $\{|n\rangle\}$ be orthonormal, $\langle n|m\rangle=\delta_{nm}$, and complete (it spans $\mathcal H$).
Any state expands as $|\psi\rangle=\sum_m c_m|m\rangle$ with $c_m=\langle m|\psi\rangle$. Apply the candidate operator:
$$\Big(\sum_n|n\rangle\langle n|\Big)|\psi\rangle=\sum_n|n\rangle\langle n|\psi\rangle=\sum_n|n\rangle\Big(\sum_m c_m\langle n|m\rangle\Big)=\sum_n c_n|n\rangle=|\psi\rangle.$$
Since this reproduces every $|\psi\rangle$, the operator is the identity: $\sum_n|n\rangle\langle n|=\hat I$. The
content is *completeness* — the projectors leave nothing out only if the basis spans the whole space. Numerically,
summing the projectors onto the 6 columns of a unitary, `sum(projector(V[:,n]) for n in range(6))`, returns $\approx I_6$.
