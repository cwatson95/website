# QO-02 — Atom–Field Interaction — Rabi Oscillations & Jaynes–Cummings

Second module of the **QUANTUM & NONLINEAR OPTICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-11` (the two-level system / qubit: the Pauli operators
  $\sigma_z,\sigma^+,\sigma^-$ and the driven-spin Rabi flop reused verbatim here),
  `~QM-16` (time-dependent perturbation theory: the dipole drive $-\mathbf d\!\cdot\!\mathbf E$
  and its weak-field limit), `~QO-01` (the quantized field mode, number states
  $|n\rangle$, and coherent states $|\alpha\rangle$).
- **Cross-links:** `~QO-03` (spontaneous & stimulated emission, laser physics — the
  JCM with a *lossy* mode), `~QO-04` (open systems / master equations — damped Rabi,
  the strong-coupling condition behind the vacuum Rabi splitting), `~QM-09` (the
  oscillator ladder $a,a^\dagger$, bridge **B6**).

## Scope
One atom, one mode. A **two-level atom** ($\sigma_z=|e\rangle\langle e|-|g\rangle\langle g|$,
$\sigma^\pm$) driven by a **classical** field undergoes **Rabi oscillations**: in the
rotating-wave approximation the excited population is
$P_e(t)=(\Omega^2/\Omega_R^2)\sin^2(\Omega_R t/2)$ with generalized Rabi frequency
$\Omega_R=\sqrt{\Omega^2+\delta^2}$ — a complete inversion on resonance every
$\Omega t=\pi$, returning at $\Omega t=2\pi$, but only a partial flop
$\Omega^2/(\Omega^2+\delta^2)$ off resonance. **Quantizing** the field promotes this
to the **Jaynes–Cummings model** $H=\hbar\omega_c a^\dagger a+\tfrac12\hbar\omega_a\sigma_z
+\hbar g(a\sigma^++a^\dagger\sigma^-)$, whose conserved excitation number splits it
into $2\times2$ blocks $\{|e,n\rangle,|g,n+1\rangle\}$. Their **dressed states** have
energies $E_{n,\pm}=\hbar\omega_c(n+\tfrac12)\pm\tfrac12\hbar\sqrt{\delta^2+4g^2(n+1)}$,
split by $2g\sqrt{n+1}$ — for $n=0$ the **vacuum Rabi splitting** $2g$, the
cavity-QED hallmark in which even the vacuum lifts a degeneracy. Over a **coherent**
field the atomic inversion $\langle\sigma_z\rangle(t)=\sum_n P_n\cos(2g\sqrt{n+1}\,t)$
**collapses** ($t_c\sim\sqrt2/g$) and then **revives** ($t_r\sim2\pi\sqrt{\bar n}/g$) —
a purely quantum signature, absent for any classical field. Everything is built from
$2\times2$ atom $\otimes$ $N$-level field matrices and **checked**: the closed-form
Rabi formula against direct evolution, the dressed energies against `eigh`, and the
collapse/revival against the Poisson sum.

## Operations — `code/atom_field.py`  (natural units $\hbar=1$)

| call | meaning | reference |
|------|---------|-----------|
| `sigma_z`, `sigma_plus`, `sigma_minus` | two-level operators σ_z, σ⁺=\|e⟩⟨g\|, σ⁻=\|g⟩⟨e\| | ~QM-11; SZ §5.1 |
| `generalized_rabi(Omega, detuning)` | Ω_R = √(Ω²+δ²) | SZ §5.2 |
| `rabi_excited_population(t, Omega, detuning)` | P_e = (Ω²/Ω_R²) sin²(Ω_R t/2) | SZ §5.2 |
| `two_level_hamiltonian(Omega, detuning)` | RWA H = ½(δ σ_z + Ω σ_x) | SZ §5.2 |
| `annihilation(N)`, `number_operator(N)` | field operators a, a†a | ~QO-01; SZ §6.1 |
| `coherent_state(alpha, N)` | \|α⟩, Poissonian P_n, n̄=\|α\|² | ~QO-01; SZ Ch.2 |
| `jcm_hamiltonian(omega_c, omega_a, g, N)` | H = ω_c a†a + ½ω_a σ_z + g(aσ⁺+a†σ⁻) | SZ §6.1–6.2 |
| `dressed_energies(n, detuning, g, omega_c)` | E_{n,±} = ω_c(n+½) ± ½√(δ²+4g²(n+1)) | SZ §6.2 |
| `vacuum_rabi_splitting(g)` | 2g (the n=0 resonant gap) | SZ §6.2 |
| `jcm_inversion(times, omega_c, omega_a, g, alpha, N)` | ⟨σ_z⟩(t): collapse & revival | SZ §6.2 |
| `resonant_inversion_series(times, g, alpha, N)` | Σ_n P_n cos(2g√(n+1) t) | SZ §6.2 |
| `collapse_time(g)`, `revival_time(g, nbar)` | t_c ≈ √2/g, t_r ≈ 2π√n̄/g | SZ §6.2 |

Constant `HBAR` (= 1.0) is re-exported; the ℏ factors are carried symbolically.

## Use
```python
import numpy as np
from atom_field import (rabi_excited_population, generalized_rabi, dressed_energies,
                        vacuum_rabi_splitting, jcm_inversion, revival_time)

rabi_excited_population(np.pi, 1.0, 0.0)        # 1.0  -- resonant pi-pulse fully inverts
rabi_excited_population(2*np.pi, 1.0, 0.0)      # ~0   -- and returns at Om t = 2 pi
generalized_rabi(1.0, 1.5)                       # 1.803  = sqrt(1 + 1.5^2)
Em, Ep = dressed_energies(0, 0.0, 1.0, 5.0)      # resonant vacuum doublet
Ep - Em                                          # 2.0  = vacuum_rabi_splitting(1.0) = 2g
jcm_inversion(0.0, 5, 5, 1.0, 4.0, 60)           # +1.0  -- atom starts excited
jcm_inversion(revival_time(1.0, 16.0)/2, 5, 5, 1.0, 4.0, 60)   # ~0  -- collapsed
```

## Run
```bash
cd code
python3 atom_field.py          # demo: resonant Rabi return, vacuum Rabi splitting 2g, collapse/revival times
python3 test_atom_field.py     # tests  ->  "All 12 tests passed."
```

## Files
- `notes.md` — semiclassical → quantized: RWA, the Rabi formula, the JCM, dressed
  states, the vacuum Rabi splitting, collapse & revival (10 display equations)
- `code/atom_field.py`, `code/test_atom_field.py`
- `problems/problems.md` — worked problems (Scully & Zubairy Ch. 5–6)
- `refs.md` — citation table (Scully & Zubairy, section-level; cross-links)
