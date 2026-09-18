# SM-04 — Quantum Statistics

Fourth module of the **STATISTICAL MECHANICS & THERMODYNAMICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~SM-03` (`K_B`, `HBAR`, the grand canonical ensemble); `~QM-14` (identical particles / symmetrization).
- **Feeds into:** condensed-matter and astrophysics applications (electron gas, white dwarfs, BEC).

## Scope
Identical quantum particles fill single-particle states with mean occupation
⟨n⟩ = 1/(e^{β(ε−µ)} ∓ 1): the lower sign (−1) for **bosons** (Bose–Einstein), the
upper (+1) for **fermions** (Fermi–Dirac). When e^{β(ε−µ)} ≫ 1 both collapse to the
classical **Maxwell–Boltzmann** factor. Fermions obey ⟨n⟩ ≤ 1 (**Pauli**) and at
T = 0 fill every state up to the **Fermi energy**. Bosons with µ = 0 are the
**photon gas**, giving Planck's blackbody spectrum, the Wien displacement peak
(ℏω_max = 2.8214 kT), and the **Stefan–Boltzmann** T⁴ law.

## Operations — `code/quantum_statistics.py`

| call | meaning | reference |
|------|---------|-----------|
| `bose_einstein(eps, mu, T)` | ⟨n⟩ = 1/(e^{(ε−µ)/kT} − 1) | Pa §6.3 p.149 |
| `fermi_dirac(eps, mu, T)` | ⟨n⟩ = 1/(e^{(ε−µ)/kT} + 1), in [0,1] | Pa §6.3 p.149 |
| `maxwell_boltzmann(eps, mu, T)` | ⟨n⟩ = e^{−(ε−µ)/kT} (classical limit) | Pa §6.3 p.149 |
| `fermi_dirac_T0(eps, e_fermi)` | T = 0 step (1 below e_F, 0 above) | Pa §8.1 p.231 |
| `planck_energy_density(omega, T)` | u(ω) = (ℏω³/π²c³)/(e^{ℏω/kT}−1) | Pa §7.3 p.200 |
| `rayleigh_jeans(omega, T)` | (ω²/π²c³)kT (low-ω limit) | Pa §7.3 p.200 |
| `wien_peak_x()` | dimensionless peak x = ℏω_max/kT ≈ 2.8214 | Pa §7.3 p.200 |
| `radiation_energy_density(T)` | U/V = a T⁴, a = π²k⁴/15ℏ³c³ | Pa §7.3 p.200 |
| `stefan_boltzmann_constant()` | σ = π²k⁴/60ℏ³c² = ac/4 | Pa §7.3 p.200 |

Constants: `K_B`, `HBAR`, `C_LIGHT`.

## Use
```python
from quantum_statistics import fermi_dirac, bose_einstein, wien_peak_x, stefan_boltzmann_constant, K_B

fermi_dirac(mu, mu, 300.0)               # 0.5 exactly at the Fermi level
bose_einstein(mu + 0.01*K_B*300, mu, 300.0)   # large: bosons pile into low states
wien_peak_x()                            # 2.8214393... (root of 3(1 - e^-x) = x)
stefan_boltzmann_constant()              # 5.670e-8 W/m^2/K^4 (CODATA)
```

## Run
```bash
cd code
python3 quantum_statistics.py          # demo: BE/FD/MB occupations, Fermi sea, Planck/Wien/Stefan-Boltzmann
python3 test_quantum_statistics.py     # tests  ->  "All 8 tests passed."
```

## Files
- `notes.md` — derivations with inline page citations
- `code/quantum_statistics.py`, `code/test_quantum_statistics.py`
- `problems/problems.md` — worked problems (Pathria Ch.5–8; Schroeder Ch.7)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
