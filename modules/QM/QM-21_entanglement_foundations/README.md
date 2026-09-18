# QM-21 — Entanglement & Foundations

Part of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-11` (two spin-½ qubits, the Pauli/spin toolkit),
  `~QM-20` (the reduced density matrix — the entanglement diagnostic used here),
  `~QM-06` (measurement / collapse). Helpful: `~MA-04` (eigen/SVD),
  `~MA-18` (SU(2)).
- **Feeds into:** `~QO-05` (entangled photons & squeezing — the optical
  realization of these Bell tests; **not built yet**, bridge noted below).
- **Sideways links:** `~QM-13` (the singlet is the total-spin $J=0$ state);
  `~RE-06` / special relativity (the no-signaling discussion).

## Scope
What it means for a quantum state to be **entangled**, and why Bell's theorem
rules out local hidden variables — as evaluable linear algebra (Griffiths 3e
Ch. 12, "Afterword"):

1. **EPR paradox.** The spin-0 pion decays into the **singlet**
   $|\Psi^-\rangle=(|01\rangle-|10\rangle)/\sqrt2$ (Eq. 12.1, p.567). Measuring
   one spin instantly fixes the other — "spooky action at a distance." EPR
   concluded QM must be incomplete (a hidden variable $\lambda$).
2. **Entangled (non-separable) states.** The singlet **cannot** be written as a
   product $|a\rangle\otimes|b\rangle$ (Problem 12.1, p.568). Diagnostic: the
   reduced state of one qubit is **pure** for a product state but **maximally
   mixed** ($=\mathbb I/2$) for a Bell state.
3. **The four Bell states** $|\Phi^\pm\rangle,|\Psi^\pm\rangle$ — a maximally
   entangled orthonormal basis.
4. **Local hidden variables & Bell.** The singlet correlation is
   $E(\mathbf a,\mathbf b)=-\mathbf a\!\cdot\!\mathbf b$ (Eq. 12.4, p.570). The
   **CHSH** combination $S=E(a,b)-E(a,b')+E(a',b)+E(a',b')$ obeys the **classical
   bound $|S|\le2$** for any local theory, but the singlet reaches **$|S|=2\sqrt2$**
   (the **Tsirelson** bound) at optimal angles — and never exceeds it. Griffiths'
   own 3-setting form $|P(a,b)-P(a,c)|\le1+P(b,c)$ (Eq. 12.12, p.571) is built
   too, with his 45° violation reproduced.
5. **What it means / doesn't.** Violation ⇒ **no local hidden variables** (nature
   is nonlocal). But **no faster-than-light signaling**: Alice's marginal
   statistics ($\rho_A$) are independent of Bob's choice of measurement (p.571–572).

**House rule:** nothing is asserted, everything is *checked*. Separability
(purity / Schmidt rank / concurrence), $E=-\mathbf a\!\cdot\!\mathbf b$, the
classical bound (exhaustively over all 16 local strategies), the $2\sqrt2$
Tsirelson maximum, and no-signaling are all verified numerically in
`test_entanglement.py`. **Self-contained:** the qubit/Bell tools are built here
(numpy) — the concurrent `~QM-11`/`~QM-20` code is *not* imported.

## Operations — `code/entanglement.py`

| call | meaning | formula |
|------|---------|---------|
| `bell_state(name)` / `singlet()` | the four Bell states | $|\Phi^\pm\rangle,|\Psi^\pm\rangle=(|00\rangle\pm|11\rangle),(|01\rangle\pm|10\rangle)$ over $\sqrt2$ |
| `product_state(a, b)` | separable state | $|a\rangle\otimes|b\rangle$ |
| `partial_trace(rho, keep, dims)` | reduced density matrix | $\rho_A=\mathrm{Tr}_B\rho$, $\rho_B=\mathrm{Tr}_A\rho$ |
| `purity(rho)` / `is_pure` | mixedness | $\mathrm{Tr}(\rho^2)\in[\tfrac12,1]$ (qubit) |
| `schmidt_coeffs` / `schmidt_rank` | entanglement rank | SVD of $\psi$ reshaped; rank 1 ⇔ product |
| `is_product_state(psi)` | separability test | Schmidt rank $=1$ |
| `concurrence(psi)` | entanglement measure | $C=2|ad-bc|\in[0,1]$ |
| `concurrence_spinflip(psi)` | Wootters cross-check | $|\langle\psi|\sigma_y\!\otimes\!\sigma_y|\psi^*\rangle|$ |
| `measure_op(n)` | spin observable along $\hat{\mathbf n}$ | $\hat{\mathbf n}\!\cdot\!\boldsymbol\sigma$ (eigenvalues $\pm1$) |
| `correlation(state, a, b)` / `E_singlet(a,b)` | spin–spin correlation | $\langle\psi|(\mathbf a\!\cdot\!\boldsymbol\sigma)\!\otimes\!(\mathbf b\!\cdot\!\boldsymbol\sigma)|\psi\rangle$ |
| `chsh_value(state,a,a',b,b')` / `chsh_from_angles` | CHSH $S$ | $E(a,b)-E(a,b')+E(a',b)+E(a',b')$ |
| `chsh_operator(...)` | the CHSH operator | $\lVert\hat B\rVert\le2\sqrt2$ (Tsirelson) |
| `tsirelson_bound()` | quantum max of $|S|$ | $2\sqrt2$ |
| `bell_3setting(a,b,c)` | Griffiths' inequality | returns $(\,|P_{ab}-P_{ac}|,\;1+P_{bc}\,)$ |
| `lhv_deterministic_strategies()` | the 16 local vertices | $|S|=2$ for each (classical bound) |
| `no_signaling_unitary` / `no_signaling_measurement` | Bob can't signal | $\rho_A$ unchanged by Bob's $U$ / measurement |
| `su2(theta, axis)` | SU(2) rotation | $\cos\tfrac\theta2\,\mathbb I-i\sin\tfrac\theta2\,(\hat{\mathbf n}\!\cdot\!\boldsymbol\sigma)$ |

Also exported: Pauli matrices `sigma_x/y/z`, `I2`, basis kets `ket0/ket1`,
`bloch_ket(theta,phi)`, `ndir(theta,phi)` (planar direction vector), `kron`,
`density_matrix`, `normalize`.

## Use
```python
import numpy as np
from entanglement import (singlet, product_state, ket0, ket1, partial_trace,
                         density_matrix, purity, concurrence, E_singlet, ndir,
                         chsh_from_angles, tsirelson_bound)

# separability: reduced state pure (product) vs maximally mixed (entangled)
purity(partial_trace(density_matrix(product_state(ket0, ket1)), keep=0))  # 1.0
purity(partial_trace(density_matrix(singlet()),               keep=0))    # 0.5
concurrence(singlet())                       # 1.0  (maximally entangled)

E_singlet(ndir(0.0), ndir(0.0))              # -1.0  ( = -a.b, perfect anti-corr)
chsh_from_angles(singlet(), 0, 90, 45, 135)  # -2.8284  ( = -2*sqrt2, violates |S|<=2 )
tsirelson_bound()                            #  2.8284
```

## Run
```bash
cd code
python3 entanglement.py          # demo: the CHSH violation table
python3 test_entanglement.py     # tests  ->  "All 17 tests passed."
```

## Files
- `notes.md` — EPR → entanglement → Bell/CHSH → Tsirelson → no-signaling, each
  derivation tied to its code + test
- `code/entanglement.py` — the library (numpy; qubit/Bell toolkit + a `_demo()`)
- `code/test_entanglement.py` — 17 checks: separability (purity/Schmidt/
  concurrence), $E=-\mathbf a\!\cdot\!\mathbf b$, classical bound (exhaustive),
  Tsirelson $2\sqrt2$, Griffiths' 3-setting violation, no-signaling
- `problems/problems.md` — worked problems (Griffiths 3e Ch. 12)
- `refs.md` — verified textbook locations

> **Bridge to `~QO-05` (not built).** The famous Aspect experiments used
> entangled *photon polarization*, not spins. The polarization correlation goes
> as $\cos2\theta$, so the optimal analyzer angles are *halved* to
> $0°,22.5°,45°,67.5°$ — the same $2\sqrt2$ violation in a different physical
> skin. `~QO-05` builds that optical version (and squeezing) when it lands.
