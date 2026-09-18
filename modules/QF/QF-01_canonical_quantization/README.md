# QF-01 — Canonical Field Quantization

First module of the **QUANTUM FIELD THEORY** trunk (see `modules/topic_network.txt`).
This is the top of **KEY BRIDGE B6**: a free quantum field is *infinitely many
harmonic oscillators*, one per momentum mode — the `~QM-09` oscillator, promoted.

- **Prerequisites:** `~QM-09` (the quantum harmonic oscillator and its $a,a^\dagger$
  algebra — the single mode this whole module repeats), `~QM-22` (the Klein–Gordon
  & Dirac equations being quantized), `~QM-05` (operators & commutators, $[x,p]=i\hbar$),
  `~CM-19` (canonical momentum $\pi=\partial\mathcal L/\partial\dot q$).
- **Cross-links:** `~CM-16` (classical normal modes — what a field mode *is*),
  `~QM-14` (identical particles, Pauli exclusion — the spin–statistics payoff),
  `~QM-19` (path integrals — the alternative quantization route), `~EM-09` (vector
  potential & gauge freedom — the photon's constraint), `~QF-02`/`~QF-03`/`~QF-04`
  (interactions, gauge theories, renormalization), `~QF-05` (curved-spacetime QFT —
  the user's Quantum_Optics work).

## Scope
Canonical quantization turns a classical field into a quantum one by the same rule
that quantizes a particle. From a Lagrangian density $\mathcal L$ one reads off the
**canonical momentum** $\pi=\partial\mathcal L/\partial(\partial_0\phi)$ and imposes
the **equal-time commutator** $[\phi(\mathbf x),\pi(\mathbf y)]=i\hbar\,\delta^3(\mathbf x-\mathbf y)$,
the field analogue of $[x,p]=i\hbar$. Fourier-expanding the **Klein–Gordon field**
into modes with **dispersion** $\omega_{\mathbf p}=\sqrt{\mathbf p^2c^2+m^2c^4}/\hbar
\to\sqrt{\mathbf p^2+m^2}$ (massless $\to|\mathbf p|$) reveals that each mode is an
independent **harmonic oscillator** with ladder operators $a_{\mathbf p},a_{\mathbf p}^\dagger$
and spectrum $(n_{\mathbf p}+\tfrac12)\hbar\omega_{\mathbf p}$ — **KEY BRIDGE B6**.
Stacking quanta with $a^\dagger$ on the vacuum builds the **Fock space** of
multi-particle states (**second quantization**: particle number is now dynamical),
while the leftover $\tfrac12$ per mode sums to the UV-divergent **vacuum / zero-point
energy** $\tfrac12\sum_{\mathbf p}\hbar\omega_{\mathbf p}$, which the code regularizes
with a cutoff and shows growing like $\Lambda^4$ — the divergence that motivates
renormalization (`~QF-04`). The module closes with the two refinements canonical
quantization forces on other fields: the **Dirac field** needs **anticommutators**
$\{b,b^\dagger\}$ (spin–statistics, Pauli exclusion, `~QM-14`), and the **EM field**
carries a **gauge constraint** $\pi^0=0$ that must be fixed before quantizing
(`~QF-03`, `~EM-09`).

## Operations — `code/field_quantization.py`  (natural units $\hbar=c=1$)

| call | meaning | reference |
|------|---------|-----------|
| `kg_dispersion(p, m)` | $\omega_{\mathbf p}=\sqrt{\mathbf p^2+m^2}$ (massless $\to\lvert\mathbf p\rvert$) | PS §2.3 |
| `annihilation(D)` / `creation(D)` | $a,a^\dagger$ in the $D$-level number basis | PS §2.3; `~QM-09` |
| `number(D)` | $N=a^\dagger a=\mathrm{diag}(0,1,\dots,D{-}1)$ | PS §2.3 |
| `commutator(A,B)` | $[A,B]=AB-BA$; $[a,a^\dagger]=1$ on the interior | PS §2.3 |
| `single_mode_spectrum(D, omega)` | diagonalize $\omega(N+\tfrac12)$ → $\omega(n+\tfrac12)$ (B6) | PS §2.3 |
| `mode_energy(p, m, n)` | $E=(n+\tfrac12)\,\omega_{\mathbf p}$ ($n=0$: zero-point) | PS §2.3 |
| `field_modes(cutoff, box_L)` | box-mode magnitudes $\lvert\mathbf p\rvert\le$ cutoff | PS §2.3 |
| `vacuum_energy(masses_or_modes, cutoff)` | $\tfrac12\sum_{\mathbf p}\omega_{\mathbf p}$; grows $\sim\Lambda^4$ | PS §2.3 |
| `anticommutator(A,B)` | $\{A,B\}=AB+BA$ (the Dirac field) | PS §3.5 |
| `fermion_annihilation()` | single fermion mode $b$; $\{b,b^\dagger\}=1$, $b^{\dagger2}=0$ | PS §3.5 |

## Use
```python
import numpy as np
from field_quantization import (kg_dispersion, single_mode_spectrum, mode_energy,
                                vacuum_energy, creation, annihilation, commutator)

kg_dispersion(np.array([0.,1.,5.]), m=0.0)   # [0. 1. 5.]   massless: omega = |p|
kg_dispersion(0.0, m=2.0)                     # 2.0          rest energy at p=0
single_mode_spectrum(6, omega=1.0)            # [0.5 1.5 2.5 3.5 4.5 5.5]  (n+1/2)w  (B6)
mode_energy(3.0, 4.0, n=0)                     # 2.5  = omega/2 (zero-point), omega=5
np.diag(commutator(annihilation(6), creation(6))).real   # [1 1 1 1 1 -5]  [a,a+]=1 interior
vacuum_energy(0.0, 2.0), vacuum_energy(0.0, 4.0)         # 24.4, 379.3  -> ~16x  (UV ~Lambda^4)
```

## Run
```bash
cd code
python3 field_quantization.py        # demo: KG dispersion, oscillator spectrum, cutoff vacuum energy, Pauli
python3 test_field_quantization.py   # tests  ->  "All 13 tests passed."
```

## Files
- `notes.md` — Lagrangian → commutator → mode expansion → Fock space → vacuum
  energy; the Dirac (anticommutator) and EM (gauge) refinements; the B6 bridge
- `code/field_quantization.py`, `code/test_field_quantization.py` (numpy only, self-contained)
- `problems/problems.md` — worked problems (Peskin Ch.2–3; cross-checks to the code)
- `refs.md` — citation table (Peskin primarily; Zee, Weinberg cross-cited, section level)
