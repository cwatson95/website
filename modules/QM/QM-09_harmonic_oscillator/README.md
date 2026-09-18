# QM-09 — The Quantum Harmonic Oscillator

A node of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`). The
most important exactly solvable system in physics, solved **two independent
ways** that are then shown to agree.

- **Prerequisites:** `~QM-05` (Hilbert space, operators, commutators — the
  algebra of `[x,p]=iℏ`) and `~MA-12` (Hermite polynomials, **imported** here).
  Helpful: `~QM-03` (the time-independent Schrödinger equation being solved).
- **Feeds into:** `~QM-10` (angular momentum — the same ladder-operator trick),
  `~QM-12` (hydrogen atom — the same power-series/special-function trick), and
  forward across bridge **B6** to `~QF-01` (a quantum field = infinitely many
  harmonic oscillators; the `a, a†` here become particle creation/annihilation
  operators).

## Scope
Both standard solutions of $H=\frac{p^2}{2m}+\frac12 m\omega^2x^2$, as code you
can run and check:

1. **Algebraic method** (ladder operators, Griffiths §2.3.1). Build $a$ and
   $a^\dagger$ as matrices; get $[a,a^\dagger]=1$, $N=a^\dagger a=
   \mathrm{diag}(0,1,2,\dots)$, $H=\hbar\omega(N+\tfrac12)$ with
   $E_n=\hbar\omega(n+\tfrac12)$ and zero-point energy $\tfrac12\hbar\omega$, and
   the ladder relations $a^\dagger|n\rangle=\sqrt{n+1}\,|n{+}1\rangle$,
   $a|n\rangle=\sqrt{n}\,|n{-}1\rangle$, $a|0\rangle=0$.
2. **Analytic method** (Hermite–Gaussians, Griffiths §2.3.2). The eigenfunctions
   $\psi_n(x)\propto H_n(\xi)\,e^{-\xi^2/2}$; verify orthonormality and that each
   solves the finite-difference TISE.
3. **Cross-check:** both methods give the identical spectrum
   $E_n=\hbar\omega(n+\tfrac12)$.

**House rule for this module:** nothing about the spectrum is asserted — it is
*derived twice*. The ladder route diagonalises a matrix Hamiltonian; the Hermite
route diagonalises a finite-difference Hamiltonian built with no knowledge of
ladder operators. The tests confirm both equal $\hbar\omega(n+\tfrac12)$, and
the truncation artifact of finite ladder matrices is exposed, not hidden.

> **Units.** Natural oscillator units $\hbar=m=\omega=1$ throughout (documented
> in `oscillator.py`): energies in units of $\hbar\omega$, lengths in
> $\sqrt{\hbar/m\omega}$, so $E_n=n+\tfrac12$ and $\xi=x$.

## Operations — `code/oscillator.py`

| call | meaning | result |
|------|---------|--------|
| **Algebraic** | | |
| `annihilation(D)` / `creation(D)` | $a$, $a^\dagger$ in the $D$-level number basis | superdiagonal $\sqrt n$ matrices |
| `number_operator(D)` | $N=a^\dagger a$ | $\mathrm{diag}(0,1,\dots,D{-}1)$ |
| `hamiltonian_matrix(D)` | $H=\hbar\omega(N+\tfrac12)$ | diagonal, $E_n=\hbar\omega(n{+}\tfrac12)$ |
| `position_operator` / `momentum_operator(D)` | $x,p$ from $a,a^\dagger$ | $[x,p]=i\hbar$ (interior) |
| `hamiltonian_from_xp(D)` | $H=p^2/2m+\tfrac12 m\omega^2x^2$ | $=$ ladder form on interior |
| `commutator(A,B)` | $[A,B]=AB-BA$ | $[a,a^\dagger]=\mathrm{diag}(1,\dots,1,-(D{-}1))$ |
| `basis_vector(n,D)` | number state $\lvert n\rangle$ | unit column |
| `algebraic_spectrum(D)` | diagonalise $H$ | sorted $E_n$ |
| **Analytic** | | |
| `psi(n,x)` | $\psi_n(x)=(\tfrac{m\omega}{\pi\hbar})^{1/4}\frac{H_n(\xi)}{\sqrt{2^n n!}}e^{-\xi^2/2}$ | scalar or array |
| `ground_state(x)` | $\psi_0$ (pure Gaussian) | closed form |
| `xi(x)` | $\xi=\sqrt{m\omega/\hbar}\,x$ | dimensionless coord |
| `overlap(m,n)` | $\int\psi_m\psi_n\,dx$ (Simpson) | $\delta_{mn}$ |
| `fd_hamiltonian(x)` | finite-difference $H$ on a grid | matrix |
| `fd_spectrum(L,N,k)` | lowest $k$ FD eigenvalues | $\to E_n=\hbar\omega(n{+}\tfrac12)$ |
| `fd_residual(n)` | $\lVert H_\text{fd}\psi_n-E_n\psi_n\rVert/\lVert\psi_n\rVert$ | $\sim10^{-4}$ |
| `energy(n)` / `zero_point_energy()` | $\hbar\omega(n+\tfrac12)$ / $\tfrac12\hbar\omega$ | exact |

Hermite polynomials $H_n$ are **imported from `~MA-12`**
(`special_functions.hermite`); `numpy.polynomial.hermite` is an equivalent
fallback.

## Use
```python
from oscillator import (algebraic_spectrum, creation, basis_vector,
                        commutator, annihilation, overlap, fd_spectrum)
import numpy as np

algebraic_spectrum(6)                       # [0.5 1.5 2.5 3.5 4.5 5.5]  (E_n=n+1/2)
creation(6) @ basis_vector(2, 6)            # sqrt(3)|3>  -> a+|n>=sqrt(n+1)|n+1>
np.diag(commutator(annihilation(6), creation(6))).real   # [1 1 1 1 1 -5]  (truncation)
overlap(2, 2), overlap(2, 3)                # 1.0, ~0.0   (orthonormality)
fd_spectrum(k=4)                            # ~[0.5 1.5 2.5 3.5]  (same, analytic route)
```

## Run
```bash
cd code
python3 oscillator.py          # demo: both methods + the cross-check, side by side
python3 test_oscillator.py     # tests  ->  "All 13 tests passed."
```

## Files
- `notes.md` — the two derivations (ladder algebra; power series → Hermite), the
  truncation artifact, and the bridge to fields (B6)
- `code/oscillator.py` — the library (numpy + scipy; imports `~MA-12` Hermite)
- `code/test_oscillator.py` — 13 checks: commutator, ladder relations, spectrum,
  orthonormality, FD-TISE residual, two-method agreement
- `problems/problems.md` — worked problems (Griffiths 3e §2.3)
- `refs.md` — verified textbook locations
