# QM-03 — The Schrödinger Equation

Module of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-02` (the wavefunction $\Psi$ and the Born rule $|\Psi|^2$
  — the object this module evolves) and `~MA-08` (PDEs / separation of variables,
  the analytic engine). Light contact with `~MA-04` (matrix eigenproblems) helps.
- **Feeds into:** `~QM-04` (probability current — *why* the norm is conserved),
  `~QM-05`/`~QM-06` (the eigenproblem and $|c_n|^2$ as formalism/measurement),
  `~QM-08` (1-D wells, steps, barriers) and `~QM-09` (harmonic oscillator) — both
  built on the machine here.

## Scope
The central equation of quantum mechanics and the anatomy of its solutions, as
objects you **build and evolve on a grid**:

1. **Time-dependent Schrödinger equation (TDSE)** $i\hbar\,\partial_t\Psi=\hat H\Psi$
   — the dynamical law, with $\hat H=-\frac{\hbar^2}{2m}\partial_x^2+V(x)$.
2. **Separation of variables** $\Rightarrow$ the **time-independent** equation
   (TISE) $\hat H\psi=E\psi$ — an eigenvalue problem for the energies $E_n$.
3. **Stationary states** $\Psi_n=\psi_n e^{-iE_nt/\hbar}$ — why $|\Psi|^2$ is then
   frozen in time even though the phase rotates.
4. **The general solution** $\Psi=\sum_n c_n\psi_n e^{-iE_nt/\hbar}$ — the rôle of
   the $c_n$ (Fourier's trick; $|c_n|^2$ = energy probability) and the **beat** at
   $\omega=(E_2-E_1)/\hbar$ that makes a superposition move.

**House rule for this module:** nothing is asserted that the code does not
*recover*. The Hamiltonian is built by finite differences and diagonalised
(`numpy.linalg.eigh`); the well spectrum $E_n=n^2\pi^2\hbar^2/2mL^2$, the
frozen-in-time $|\Psi|^2$ of a stationary state, the Bohr beat period, $\sum|c_n|^2
=1$, and (same solver, different $V$) the oscillator ladder $E_n=(n+\tfrac12)
\hbar\omega$ are all checked against their closed forms in the tests.

## Operations — `code/schrodinger.py`

| call | meaning | formula |
|------|---------|---------|
| `make_grid(a, b, N)` | N interior points; endpoints = Dirichlet walls | $x_i=a+i\,\Delta x$ |
| `second_derivative_matrix(N, dx)` | 3-point Laplacian | tridiag$(1,-2,1)/\Delta x^2$ |
| `hamiltonian(x, V, hbar, m)` | $\hat H$ as a matrix | $-\frac{\hbar^2}{2m}\partial_x^2+V$ |
| `solve(x, V, hbar, m)` | TISE eigenproblem | $\hat H\psi=E\psi$ → $(E_n,\psi_n)$ |
| `stationary_state(psi, E, t)` | evolve one eigenstate | $\psi\,e^{-iEt/\hbar}$ |
| `evolve(E, psi, c, t)` | general solution | $\sum_n c_n\psi_n e^{-iE_nt/\hbar}$ |
| `coefficients(psi, Psi0, dx)` | Fourier's trick | $c_n=\langle\psi_n|\Psi_0\rangle$ |
| `inner_product / normalize / prob_density / expectation_position` | $L^2$ tools | $\langle f|g\rangle,\ |\Psi|^2,\ \langle x\rangle$ |
| `superposition_period(Em, En)` | beat period | $2\pi\hbar/(E_m-E_n)$ |
| `measure_period(ts, signal)` | period from a time series | upward zero-crossings |

Closed-form cross-checks are exported too: `infinite_well_energy`,
`infinite_well_eigenfunction`, `harmonic_oscillator_energy`, `bohr_frequency`.

## Use
```python
import numpy as np
from schrodinger import (make_grid, solve, infinite_well_energy,
                         stationary_state, evolve, prob_density,
                         superposition_period, expectation_position)

x = make_grid(0.0, 1.0, 400)          # infinite well, width L = 1 (ħ = m = 1)
E, psi = solve(x, V=0.0)              # TISE:  H ψ = E ψ
E[0], infinite_well_energy(1, 1.0)    # 4.9348, 4.9348  (= π²/2, to <1e-5)

# a stationary state: |Ψ|² does not move
d0 = prob_density(stationary_state(psi[:,0], E[0], 0.0))
d9 = prob_density(stationary_state(psi[:,0], E[0], 9.0))
np.max(np.abs(d9 - d0))               # ~1e-16  (frozen)

# a superposition does move, beating at ω = (E₂−E₁)/ħ
c = np.zeros(psi.shape[1]); c[0] = c[1] = 1/np.sqrt(2)
superposition_period(E[1], E[0])      # 0.4244 = 2π/(E₂−E₁)
expectation_position(evolve(E, psi, c, 0.0), x)  # ⟨x⟩ oscillates about L/2
```

## Run
```bash
cd code
python3 schrodinger.py          # demo: well spectrum, frozen |Ψ|², beat period, c_n, oscillator
python3 test_schrodinger.py     # tests  ->  "All 13 tests passed."
```

## Files
- `notes.md` — TDSE → separation of variables → TISE; stationary states;
  superposition and the $c_n$; the grid method
- `code/schrodinger.py` — the library (finite-difference $\hat H$, `eigh`, time
  evolution; pure `numpy`)
- `code/test_schrodinger.py` — 13 checks against closed forms (well energies &
  eigenfunctions, stationarity, Bohr period, conservation, Fourier's trick, SHO)
- `problems/problems.md` — worked problems (Griffiths 3e)
- `refs.md` — verified textbook locations
