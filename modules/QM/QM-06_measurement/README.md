# QM-06 — Measurement Postulates

Part of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-02` (Born rule — $|\Psi|^2$ as probability), `~QM-05`
  (Hilbert space, Dirac notation, Hermitian operators, commutators). Helpful:
  `~MA-04` (eigenvalues/eigenvectors, the spectral theorem).
- **Feeds into:** `~QM-07` (the disturbance between incompatible observables,
  sharpened into the uncertainty principle), `~QM-11` (the spin example in full),
  `~QM-20` (collapse and ensembles reformulated with the density matrix / mixed
  states).

## Scope
What a **measurement** is, as evaluable linear algebra — the postulates of
Griffiths 3e Ch. 3:

1. **Observable ↔ Hermitian operator.** Every measurable $A$ is a Hermitian
   $\hat A$; its real eigenvalues are the only possible readings; its
   eigenvectors form an orthonormal complete basis.
2. **Generalized statistical interpretation.** Measuring $A$ on $|\psi\rangle$
   yields eigenvalue $a_n$ with $P(a_n)=|\langle a_n|\psi\rangle|^2$ (and the
   $P(a_n)$ sum to 1) — Born in the eigenbasis of the measured operator.
3. **Expectation value.** $\langle A\rangle=\sum_n a_nP(a_n)=\langle\psi|\hat
   A|\psi\rangle$ — two routes to one number.
4. **Collapse.** After reading $a_n$ the state jumps to the normalized
   projection onto that eigenspace; a re-measurement then returns $a_n$ for sure.
5. **Compatible vs incompatible.** Commuting observables share an eigenbasis and
   don't disturb each other; non-commuting ones (e.g. $\sigma_x$, $\sigma_z$) do.

**House rule for this module:** nothing is asserted, everything is *checked*. Σ P
= 1, the two expectation routes, collapse idempotence, and the
commuting/non-commuting disturbance are all verified numerically against closed
forms in `test_measurement.py` — the spin-½ Stern-Gerlach cascade is the worked
example.

## Operations — `code/measurement.py`

| call | meaning | formula |
|------|---------|---------|
| `is_hermitian(A)` | is `A` a valid observable? | $\hat A=\hat A^\dagger$ |
| `eigensystem(A)` | spectrum + eigenbasis | $\hat A\|a_n\rangle=a_n\|a_n\rangle$ (real $a_n$, orthonormal) |
| `eigenspaces(A)` | distinct eigenvalues + projectors | $(a_n,\hat P_n)$, $\sum_n\hat P_n=\mathbb 1$ |
| `outcome_probabilities(psi, A)` | the measurement outcomes | $P(a_n)=\|\langle a_n\|\psi\rangle\|^2=\|\hat P_n\psi\|^2$ |
| `expectation(psi, A)` | mean reading (both ways) | $\sum_n a_nP(a_n)=\langle\psi\|\hat A\|\psi\rangle$ |
| `variance(psi, A)` / `standard_deviation` | spread | $\sigma_A^2=\langle A^2\rangle-\langle A\rangle^2$ |
| `collapse(psi, A, n)` | post-measurement state | $\hat P_n\|\psi\rangle/\|\hat P_n\|\psi\rangle\|$ |
| `measure(psi, A)` | sample an outcome + collapse | returns $(a_n,\|\psi'\rangle)$ |
| `commutator(A, B)` / `commute(A, B)` | (in)compatibility test | $[\hat A,\hat B]=\hat A\hat B-\hat B\hat A$ |
| `spin_state(theta, phi)` | Bloch-sphere spin-½ ket | $(\cos\tfrac\theta2,\,e^{i\phi}\sin\tfrac\theta2)$ |
| `spin_operator(nx, ny, nz)` | SG magnet along **n** | $\tfrac\hbar2\,\hat{\mathbf n}\!\cdot\!\boldsymbol\sigma$ |

Also exported: the Pauli matrices `sigma_x/y/z`, spin operators `Sx/Sy/Sz =
(ħ/2)σ`, `I2`, `HBAR`, `normalize`, and `index_of(A, value)` (the eigenspace
index of a target eigenvalue). Convention: **state first, observable second.**

## Use
```python
import numpy as np
from measurement import (outcome_probabilities, expectation, collapse,
                         sigma_x, sigma_z, spin_state, commute, index_of)

up_z = spin_state(0.0)                       # spin-up along z, |0> = (1, 0)
outcome_probabilities(up_z, sigma_z)         # ([-1, 1], [0., 1.])  -> +1 for sure
outcome_probabilities(up_z, sigma_x)         # ([-1, 1], [.5, .5])  -> 50/50 (incompatible)
expectation(spin_state(np.pi/3), sigma_z)    # 0.5  == cos(60 deg)

commute(sigma_x, sigma_z)                    # False -> incompatible observables
s = collapse(up_z, sigma_x, index_of(sigma_x, +1))   # collapses to |+x>
outcome_probabilities(s, sigma_x)            # ([-1, 1], [0., 1.])  -> now +1 for sure
```

## Run
```bash
cd code
python3 measurement.py          # demo: a spin-½ Stern-Gerlach cascade
python3 test_measurement.py     # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — the five postulates, each derived and tied to its code + test
- `code/measurement.py` — the library (numpy; Pauli/spin toolkit + a `_demo()`)
- `code/test_measurement.py` — 15 checks: Σ P=1, expectation two ways, collapse
  idempotence, compatible vs incompatible disturbance, spin projection law
- `problems/problems.md` — worked problems (Griffiths 3e)
- `refs.md` — verified textbook locations
