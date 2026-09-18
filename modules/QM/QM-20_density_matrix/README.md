# QM-20 — Density Matrix & Open Systems

Part of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-05` (Hilbert space, Hermitian operators, the trace),
  `~QM-06` (measurement statistics — a *mixed* state is an ensemble of outcomes).
  Helpful: `~MA-04` (eigenvalues, the spectral theorem).
- **Feeds into:** `~QM-21` (entanglement & foundations — the **partial trace**
  here is its operational signature; built concurrently, referenced by id only),
  and the unbuilt `~QO-04` (open quantum systems — where the von Neumann equation
  $i\hbar\dot\rho=[H,\rho]$ is generalized to a Lindblad master equation).

## Scope
The state of a quantum system when you **don't fully know it** — as evaluable
linear algebra. The objects of Griffiths 3e Ch. 12 ("Afterword"), §12.3:

1. **Pure vs mixed; the density operator.** A *pure* state is a known ket,
   $\rho=|\psi\rangle\langle\psi|$; a *mixed* state is a classical mixture
   $\rho=\sum_i p_i|\psi_i\rangle\langle\psi_i|$. Every density operator is
   **Hermitian**, has **unit trace**, and is **positive semidefinite** (its
   eigenvalues are probabilities $\ge 0$).
2. **Purity.** $\mathrm{Tr}(\rho^2)\le 1$, with equality **iff** the state is
   pure ($\rho^2=\rho$) — the one-number test for pure vs mixed.
3. **Expectation.** $\langle A\rangle=\mathrm{Tr}(\rho A)$ reproduces
   $\langle\psi|A|\psi\rangle$ for a pure state and the ensemble average
   $\sum_i p_i\langle\psi_i|A|\psi_i\rangle$ for a mixed one.
4. **Reduced density matrix (partial trace).** A subsystem of an **entangled**
   pure state is itself **mixed**: tracing one qubit of the Bell state
   $|\Phi^+\rangle$ leaves the other in $I/2$ (maximally mixed, $S=\ln 2$), while
   a *product* state's subsystem stays pure ($S=0$). This is the operational
   signature of entanglement.
5. **von Neumann entropy.** $S=-\mathrm{Tr}(\rho\ln\rho)=-\sum_k\lambda_k\ln\lambda_k$;
   $S=0$ iff pure, $S=\ln d$ for the maximally mixed state in $d$ dimensions.
6. **Time evolution.** $i\hbar\dot\rho=[H,\rho]$ (the von Neumann equation). Its
   solution is unitary, $\rho(t)=U\rho U^\dagger$, conserving the spectrum (hence
   purity *and* entropy); a $\rho$ that commutes with $H$ is stationary. Decay of
   the off-diagonal coherences is **decoherence**.

**House rule for this module:** nothing is asserted, everything is *checked*.
$\mathrm{Tr}\,\rho=1$, $\mathrm{Tr}(\rho^2)\!\le\!1$, the two expectation routes,
the Bell-subsystem $=I/2$ result, $S=\ln 2$, spectrum/purity conservation under
unitary flow, and the stationarity $\Leftrightarrow[H,\rho]=0$ criterion are all
verified numerically against closed forms in `test_density_matrix.py`.

## Operations — `code/density_matrix.py`

| call | meaning | formula |
|------|---------|---------|
| `density_matrix_pure(psi)` | pure-state operator | $\rho=\|\psi\rangle\langle\psi\|$ |
| `density_matrix_mixed(states, probs)` | statistical mixture | $\rho=\sum_i p_i\|\psi_i\rangle\langle\psi_i\|$ |
| `is_hermitian` / `trace_is_one` / `is_positive_semidefinite` | the 3 defining tests | $\rho=\rho^\dagger$, $\mathrm{Tr}\,\rho=1$, $\lambda_k\ge0$ |
| `is_density_matrix(rho)` | all three at once | valid state |
| `purity(rho)` | purity | $\mathrm{Tr}(\rho^2)\in[1/d,\,1]$ |
| `is_pure(rho)` | pure-state test | $\mathrm{Tr}(\rho^2)=1\Leftrightarrow\rho^2=\rho$ |
| `expectation(rho, A)` | mean reading | $\langle A\rangle=\mathrm{Tr}(\rho A)$ |
| `partial_trace(rho, dims, keep)` | reduced subsystem state | $\rho_A=\mathrm{Tr}_B\,\rho_{AB}$ |
| `von_neumann_entropy(rho, base=None)` | entropy (nats; `base=2`→bits) | $S=-\mathrm{Tr}(\rho\ln\rho)$ |
| `commutator(A, B)` | (non)commutativity | $[A,B]=AB-BA$ |
| `von_neumann_rhs(rho, H, hbar)` | $\dot\rho$ | $-\tfrac{i}{\hbar}[H,\rho]$ |
| `evolve(rho, H, t, hbar)` | unitary evolution | $U\rho U^\dagger,\ U=e^{-iHt/\hbar}$ |

Also exported: Pauli matrices `sigma_x/y/z`, `I2`; kets `ket0, ket1, plus,
minus`; `tensor(*ops)` (Kronecker product), `bell_phi_plus()`,
`maximally_mixed(d)`, and `random_density_matrix(d, rank, seed)`. Natural units
$\hbar=1$ by default; pass `hbar=...` to the evolution routines for SI numbers.
Convention: **state `rho` first, operator second.**

## Use
```python
import numpy as np
from density_matrix import (density_matrix_pure, density_matrix_mixed, purity,
    expectation, partial_trace, von_neumann_entropy, bell_phi_plus, tensor,
    ket0, plus, sigma_x, maximally_mixed)

purity(density_matrix_pure(plus))                 # 1.0   -> pure
purity(density_matrix_mixed([ket0, plus],[.5,.5]))# < 1   -> mixed
expectation(density_matrix_pure(plus), sigma_x)   # 1.0   == <+|sigma_x|+>

bell = density_matrix_pure(bell_phi_plus())       # entangled, pure (S=0)
rhoA = partial_trace(bell, [2, 2], keep=0)        # one qubit of the pair
np.allclose(rhoA, maximally_mixed(2))             # True  -> I/2
von_neumann_entropy(rhoA)                         # 0.6931... = ln2
```

## Run
```bash
cd code
python3 density_matrix.py          # demo: pure vs mixed, entanglement, evolution
python3 test_density_matrix.py     # tests  ->  "All 17 tests passed."
```

## Files
- `notes.md` — the six topics, each derived and tied to its code + test
- `code/density_matrix.py` — the library (numpy/scipy; qubit toolkit + a `_demo()`)
- `code/test_density_matrix.py` — 17 checks: validity, purity, expectation two
  ways, the partial-trace entanglement signature, entropy, von Neumann evolution
- `problems/problems.md` — worked problems (Griffiths 3e Ch. 12)
- `refs.md` — verified textbook locations
