# SM-03 — Classical Statistical Mechanics

Third module of the **STATISTICAL MECHANICS & THERMODYNAMICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~SM-01` (`K_B`, the counting picture); `~SM-02` supplies the thermodynamic potentials this produces.
- **Feeds into:** `~SM-04` (quantum statistics replaces the Boltzmann factor with BE/FD).

## Scope
A system in contact with a heat bath at temperature T occupies state i with the
**Boltzmann probability** P_i = e^{−βE_i}/Z. The **partition function**
Z = Σ_i e^{−βE_i} (β = 1/kT) is the master object: every thermodynamic quantity is
a derivative of ln Z —
U = −∂lnZ/∂β, F = −kT ln Z, S = (U−F)/T, and **C = Var(E)/(kT²)** (heat capacity =
energy fluctuations, the simplest fluctuation–dissipation relation). Worked examples:
the two-level **Schottky anomaly**, the harmonic oscillator / **Einstein solid**,
classical **equipartition**, and the **grand canonical** ensemble.

## Operations — `code/classical_statmech.py`

| call | meaning | reference |
|------|---------|-----------|
| `partition_function(energies, T)` | Z = Σ e^{−E_i/kT} | Pa §3.2 p.41 |
| `boltzmann_probability(energies, T)` | P_i = e^{−E_i/kT}/Z | Pa §3.2 p.41 |
| `internal_energy(energies, T)` | U = Σ E_i P_i = −∂lnZ/∂β | Pa §3.3 p.50 |
| `helmholtz_from_partition(Z, T)` | F = −kT ln Z | Pa §3.3 p.50 |
| `entropy_canonical(energies, T)` | S = (U − F)/T | Pa §3.3 p.50 |
| `heat_capacity(energies, T)` | C = Var(E)/(kT²) | Pa §3.3 p.50 |
| `two_level_energy` / `two_level_heat_capacity(eps, T)` | Schottky two-level system | Pa §3.9 p.70 |
| `harmonic_oscillator_energy(omega, T)` | ⟨E⟩ = ℏω(½ + 1/(e^{βℏω}−1)) | Pa §3.8 p.65 |
| `einstein_heat_capacity(omega, T)` | Einstein-solid C (→ k high-T) | Pa §3.8 p.65 |
| `equipartition_energy(dof, N, T)` | U = (f/2)NkT | Pa §3.7 p.61 |
| `grand_partition_function(Z_of_N, z, Nmax)` | Ξ = Σ z^N Z_N | Pa §4.2 p.93 |

Constants: `K_B`, `HBAR` (re-exported).

## Use
```python
from classical_statmech import boltzmann_probability, heat_capacity, two_level_heat_capacity, K_B

boltzmann_probability([0.0, 1e-21], 50.0)        # [0.81, 0.19]: ground state favored when cold
heat_capacity([0.0, 1e-21, 2e-21], 70.0)         # C = Var(E)/(k T^2)
two_level_heat_capacity(1e-21, 30.0) / K_B       # the Schottky bump (peaks near kT ~ 0.42 eps)
```

## Run
```bash
cd code
python3 classical_statmech.py          # demo: Boltzmann weights, Schottky, oscillator, equipartition
python3 test_classical_statmech.py     # tests  ->  "All 9 tests passed."
```

## Files
- `notes.md` — derivations with inline page citations
- `code/classical_statmech.py`, `code/test_classical_statmech.py`
- `problems/problems.md` — worked problems (Pathria Ch.3–4; Schroeder Ch.6)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
