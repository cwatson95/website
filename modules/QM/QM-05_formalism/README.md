# QM-05 — Formalism: Hilbert Space, Dirac Notation, Operators, Commutators

The mathematical spine of the **QUANTUM MECHANICS** trunk (see
`modules/topic_network.txt`). After QM-01–QM-04 built wavefunctions, this module
recasts the theory in its native language — **linear algebra on a Hilbert
space** — so that every later result is a statement about vectors and operators.

- **Prerequisites:** `~MA-04` (vector spaces, matrices, eigenvalues/eigenvectors,
  diagonalization). Helpful: `~QM-02`/`~QM-03` (the wavefunction these vectors
  abstract).
- **Feeds into:** `~QM-06` (measurement — eigenvalues are the outcomes,
  $|\langle n|\psi\rangle|^2$ the probabilities), `~QM-09` (ladder operators),
  and is the quantum end of **bridge B7** to `~CM-20` (Poisson bracket).

## Scope
States are abstract vectors $|\psi\rangle$ in a Hilbert space; the inner product
$\langle\phi|\psi\rangle$; Dirac bra-ket notation; linear operators and their
matrix representation; **Hermitian operators = observables** (real eigenvalues,
orthonormal eigenvectors — the spectral theorem); commutators $[A,B]=AB-BA$; and
the **canonical commutator** $[\hat x,\hat p]=i\hbar$. *(Griffiths 3e, Ch. 3,
with the commutator/ladder material of Ch. 2.)*

**House rule for this module:** nothing about an operator is asserted — it is
*verified numerically against a closed form*. Eigenvalues are checked real,
eigenvectors checked orthonormal, $A=\sum_n\lambda_n|n\rangle\langle n|$ checked
to reconstruct $A$, the Jacobi identity checked to vanish, and the canonical
commutator checked **honestly**: it equals $i\hbar$ only on the *interior* of a
finite truncation (see the caveat below).

## Operations — `code/formalism.py`

| call | meaning | formula |
|------|---------|---------|
| `inner_product(phi, psi)` | Dirac bra-ket $\langle\phi\|\psi\rangle$ (bra conjugated) | $\sum_i \phi_i^{*}\psi_i$ |
| `norm(psi)` / `normalize(psi)` | length / unit state | $\sqrt{\langle\psi\|\psi\rangle}$ |
| `dagger(A)` | Hermitian conjugate (adjoint) | $A^\dagger=\overline{A}^{\mathsf T}$ |
| `projector(psi)` | projector onto a ray | $\|\psi\rangle\langle\psi\|/\langle\psi\|\psi\rangle$ |
| `is_hermitian(A)` | observable test | $A=A^\dagger$ |
| `expectation(A, psi)` | mean value | $\langle\psi\|A\|\psi\rangle/\langle\psi\|\psi\rangle$ |
| `commutator(A, B)` | (non)commutativity | $[A,B]=AB-BA$ |
| `spectral_decomposition(A)` | spectral theorem | real $\lambda_n$, orthonormal $\|n\rangle$ |
| `reconstruct_from_spectrum(w, V)` | rebuild $A$ | $\sum_n\lambda_n\|n\rangle\langle n\|$ |
| `annihilation` / `creation` / `number_operator` | ladder ops | $a$, $a^\dagger$, $\hat N=a^\dagger a$ |
| `position_operator(N)` / `momentum_operator(N)` | $\hat x,\hat p$ in number basis | $\hat x\propto a+a^\dagger,\ \hat p\propto i(a^\dagger-a)$ |
| `canonical_commutator(N)` | $[\hat x,\hat p]$ | $i\hbar$ on the interior |
| `random_hermitian` / `random_matrix` / `haar_unitary` | test fixtures | — |

`HBAR` (default $1$, natural units) is exported; pass the SI value to the
operator builders for physical numbers.

## The finite-dimensional `[x,p]` caveat (read this)
$[\hat x,\hat p]=i\hbar$ **cannot hold exactly in any finite dimension.** The
trace of *any* commutator of finite matrices is zero ($\mathrm{tr}\,AB=\mathrm{tr}\,BA$),
whereas $\mathrm{tr}(i\hbar I)=i\hbar N\neq 0$. Truncating the oscillator to $N$
levels drops the top rung, so $[a,a^\dagger]=I-N|N{-}1\rangle\langle N{-}1|$ and
hence $[\hat x,\hat p]=i\hbar\,(I-N|N{-}1\rangle\langle N{-}1|)$: **exactly
$i\hbar$ on the $(N{-}1)$-dimensional interior block, but $-i\hbar(N{-}1)$ in the
bottom-right corner.** The tests verify the interior *and* verify the corner is
exactly this predicted artifact — they never claim a false exact identity.

## Use
```python
from formalism import (spectral_decomposition, reconstruct_from_spectrum,
                       commutator, canonical_commutator, random_hermitian, dagger)
import numpy as np

A = random_hermitian(4, seed=0)
w, V = spectral_decomposition(A)            # w real, V columns orthonormal
np.allclose(reconstruct_from_spectrum(w, V), A)   # True: A = sum lambda|n><n|
np.allclose(dagger(V) @ V, np.eye(4))             # True: eigenvectors orthonormal

C = canonical_commutator(6)                 # [x,p] in the 6-level number basis
np.round(np.diag(C).imag, 6)                # [1,1,1,1,1,-5]: i on interior, -5 corner
```

## Cross-links
- `~MA-04` — linear algebra. This module uses `numpy.linalg.eigh` (Hermitian =
  *complex*; MA-04's `eig_symmetric` is real-symmetric only), but for a
  real-symmetric observable the two **agree** — verified in
  `test_cross_check_MA04_eigensolver`, which imports MA-04 by relative path.
- `~CM-20` — **bridge B7**, Poisson bracket → commutator. CM-20 is not yet built;
  when it lands, the classical $\{A,B\}$ maps to the quantum
  $\frac{1}{i\hbar}[A,B]$, turning $\{x,p\}=1$ into $[\hat x,\hat p]=i\hbar$.
- `~QM-06` (measurement), `~QM-09` (ladder operators) consume this machinery.

## Run
```bash
cd code
python3 formalism.py          # demo: inner product, spectral theorem, [x,p]
python3 test_formalism.py     # tests  ->  "All 20 tests passed."
```

## Files
- `notes.md` — derivations: Hilbert space, Dirac notation, the spectral theorem,
  compatible observables, and an honest treatment of finite-dim $[x,p]$
- `code/formalism.py` — the library (numpy; observables, commutators, ladder ops)
- `code/test_formalism.py` — 20 checks against closed forms (incl. the MA-04 cross-check)
- `problems/problems.md` — worked problems (Griffiths 3e), each with a code *Check:*
- `refs.md` — verified textbook locations
