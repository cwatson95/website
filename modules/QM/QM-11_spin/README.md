# QM-11 — Spin & Two-Level Systems

Pauli matrices, the qubit, and Stern–Gerlach (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-10` (angular momentum: spin is the **same algebra**
  $[J_i,J_j]=i\hbar\varepsilon_{ijk}J_k$ at the half-integer $s=\tfrac12$ rung that
  `~QM-10` builds but cannot give a $Y_l^m$), `~QM-06` (measurement: eigenvalues,
  collapse, Born probabilities — Stern–Gerlach is the canonical example),
  `~MA-04` (linear algebra: Hermitian $2\times2$ matrices, eigenspinors), and
  `~MA-18` (su(2): the Pauli matrices are its generators). The classical object
  has **no** counterpart — that is the point — but the rotation lineage is
  **bridge B3** from `~CM-09`.
- **Feeds into:** `~QM-13` (addition of angular momenta — combine two spins into
  singlet/triplet via Clebsch–Gordan), `~QM-17` (fine structure: spin–orbit
  $\mathbf S\cdot\mathbf L$, Zeeman, hyperfine), and the `~QO`/quantum-information
  modules (every qubit is a spin-$\tfrac12$). The driven two-level system here is
  the seed of `~QO-04`/`~QO-05` (these bridges connect when those modules land).

## Scope
Spin is **intrinsic angular momentum**: an internal degree of freedom with the
full angular-momentum algebra but no $\mathbf r\times\mathbf p$ and no spatial
wavefunction — only a finite matrix (Griffiths 3e §4.4, p.212). The spin-$\tfrac12$
case is the simplest nontrivial quantum system, a **two-level system / qubit**.

1. **The algebra, again** — $[S_i,S_j]=i\hbar\varepsilon_{ijk}S_k$, copied from
   `~QM-10` with the differential operators thrown away (Griffiths §4.4, p.212).
2. **Pauli matrices** — $\mathbf S=\tfrac{\hbar}{2}\boldsymbol\sigma$; the single
   identity $\sigma_i\sigma_j=\delta_{ij}\mathbb 1+i\varepsilon_{ijk}\sigma_k$
   contains $\sigma^2=\mathbb 1$, $\{\sigma_i,\sigma_j\}=2\delta_{ij}$ and the
   commutators; $S^2=\tfrac34\hbar^2\mathbb 1$ (Griffiths §4.4.1, p.214–215).
3. **Spin along $\hat{\mathbf n}$** — eigenspinor $\chi_+=(\cos\tfrac\theta2,
   \sin\tfrac\theta2 e^{i\phi})$; $\langle\mathbf S\rangle=\tfrac\hbar2\hat{\mathbf n}$
   (Bloch sphere); the $\cos^2(\theta/2)$ measurement rule (Griffiths Prob. 4.33,
   p.218).
4. **Stern–Gerlach** — measuring $S_z$ splits a beam into $2s+1=2$ spots:
   quantization made visible (Griffiths Example 4.4, p.221), the `~QM-06`
   postulate in hardware.
5. **Larmor precession** — $H=-\gamma\,\mathbf B\cdot\mathbf S$; for $\mathbf B\parallel
   \hat{\mathbf z}$, $\langle S_x\rangle,\langle S_y\rangle$ rotate at $\omega=\gamma
   B_0$ while $\langle S_z\rangle$ is fixed (Griffiths §4.4.2, p.219–220).
6. **Rabi flop** — a driven two-level system: $P_\uparrow=(\Omega^2/\Omega_R^2)
   \sin^2(\Omega_R t/2)$ — complete inversion on resonance (Griffiths Prob. 4.36).

**House rule for this module:** nothing is asserted — it is *built and checked*.
The Pauli identities and the spin algebra are finite-dimensional and therefore
verified to **machine precision**; the $\hat{\mathbf n}\cdot\mathbf S$ eigenstate,
the precession, and the Rabi formula are checked against their closed forms, and
the time evolution is confirmed **two independent ways** (matrix exponential vs.
ODE integration of $i\hbar\,\dot\chi=H\chi$). One test imports `~QM-10` and
`~MA-18` to prove spin-$\tfrac12$ *is* their $l=\tfrac12$ / su(2) object.

## Operations — `code/spin.py` (ħ = 1, natural units)

| call | meaning | formula |
|------|---------|---------|
| `sigma_x/y/z`, `sigma` | Pauli matrices | the su(2) generators |
| `Sx, Sy, Sz`, `S` | spin-½ operators | $S_i=\tfrac\hbar2\sigma_i$ |
| `S_squared()` | Casimir | $S^2=\tfrac34\hbar^2\mathbb 1=\hbar^2 s(s{+}1)\mathbb 1$ |
| `commutator/anticommutator(A,B)` | $[A,B]$ / $\{A,B\}$ | checks the σ algebra |
| `levi_civita(i,j,k)` | $\varepsilon_{ijk}$ | structure constants |
| `n_hat(θ,φ)` | unit vector | $(\sin\theta\cos\phi,\dots,\cos\theta)$ |
| `spin_operator_along(θ,φ)` | $\hat{\mathbf n}\cdot\mathbf S$ | $\tfrac\hbar2\hat{\mathbf n}\cdot\boldsymbol\sigma$ |
| `spin_eigenstate(θ,φ,sign)` | eigenspinor of $\hat{\mathbf n}\cdot\mathbf S$ | $(\cos\tfrac\theta2,\sin\tfrac\theta2 e^{i\phi})$ |
| `up_z`, `down_z` | $S_z$ eigenspinors | $(1,0)$, $(0,1)$ |
| `expectation(op,χ)` | $\langle\chi|op|\chi\rangle$ | real |
| `prob_up_z(χ)` / `born_probabilities(op,χ)` | Born rule | $\cos^2(\theta/2)$ ; SG split |
| `hamiltonian_field(γ,B)` | spin in a field | $H=-\gamma\,\mathbf B\cdot\mathbf S$ |
| `larmor_frequency(γ,B0)` | precession rate | $\omega=\gamma B_0$ |
| `propagator(H,t)` / `evolve(H,χ,t)` | unitary evolution | $e^{-iHt/\hbar}$ |
| `spin_expectations(H,χ,t)` | $(\langle S_x\rangle,\langle S_y\rangle,\langle S_z\rangle)(t)$ | precession |
| `schrodinger_solve(H,χ,t)` | ODE integrator | $i\hbar\dot\chi=H\chi$ (cross-check) |
| `rabi_hamiltonian/frequency/probability` | driven 2-level | $\Omega_R$, Rabi formula |
| `rotation(θ,n)` | spin-½ rotation | $e^{-i\theta\hat{\mathbf n}\cdot\boldsymbol\sigma/2}$ |

`HBAR` (set to `1.0`) is exported; the ħ factors are carried symbolically, so
restoring SI is a one-line change.

## Use
```python
import numpy as np
from spin import (sigma_x, sigma_y, sigma_z, commutator, Sx, Sy, Sz, S_squared,
                  spin_eigenstate, spin_operator_along, expectation, prob_up_z,
                  hamiltonian_field, spin_expectations, rabi_probability, rotation, I2)

np.allclose(sigma_x @ sigma_y, 1j*sigma_z)             # True  -- sigma_i sigma_j = i eps sigma_k
np.allclose(commutator(Sx, Sy), 1j*Sz)                  # True  -- [Sx,Sy]=i hbar Sz
np.allclose(S_squared(), 0.75*I2)                        # True  -- S^2 = 3/4 hbar^2
chi = spin_eigenstate(np.pi/3, np.pi/5)                  # spin up along (60deg,36deg)
expectation(spin_operator_along(np.pi/3, np.pi/5), chi)  # 0.5   -- <n.S> = +hbar/2
prob_up_z(chi)                                            # 0.75  = cos^2(30deg)
H = hamiltonian_field(2.0, [0,0,3.0])                     # gamma=2, B=3 z-hat
spin_expectations(H, spin_eigenstate(0.9,0), 0.25)       # <S>(t): precesses at omega=6
rabi_probability(np.pi, 1.0, 0.0)                        # 1.0   -- resonant pi-pulse inverts
np.allclose(rotation(2*np.pi), -I2)                      # True  -- 360deg flips the spinor
```

## Run
```bash
cd code
python3 spin.py            # demo: Pauli algebra, n.S, Larmor, Rabi, double cover
python3 test_spin.py       # tests  ->  "All 19 tests passed."
```

## Files
- `notes.md` — the algebra-first derivation: spin → Pauli → $\hat{\mathbf n}\cdot
  \mathbf S$ → Stern–Gerlach → Larmor → Rabi → the $720^\circ$ double cover
- `code/spin.py` — the library (numpy/scipy; self-contained)
- `code/test_spin.py` — 19 checks: exact Pauli/spin algebra, eigenstates,
  $\cos^2(\theta/2)$, Larmor precession (two ways), Rabi, $SU(2)$ double cover,
  and a cross-import of `~QM-10` + `~MA-18`
- `problems/problems.md` — worked problems (Griffiths 3e)
- `refs.md` — verified textbook locations
