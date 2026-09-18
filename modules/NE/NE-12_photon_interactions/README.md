# NE-12 — Photon interactions: photoelectric, Compton, pair production

Twelfth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§7.3** (printed pp. 191–196) of Shultis &
Faw, 3rd ed.: the photoelectric effect and absorption edges, Compton scattering
and the Klein–Nishina cross section, coherent scattering, pair and triplet
production, the composition of the total attenuation coefficient, and the
distinction between interaction and energy deposition.

- **Prerequisites:** `~NE-11` (the μ this module opens up), `~NE-08` (the
  inverse-mass energy split), `~NE-05` (positron annihilation, ⁶⁰Co's two
  gammas), `~NE-01`/`~NE-02` (shell binding energies; why heavy nuclei have low
  Z/A).
- **Cross-links:** `~NE-14` (the electrons and pairs created here are what
  stopping power then deals with), `~NE-15` (a gamma spectrum is this module read
  off an oscilloscope), `~NE-17` (dose is μ_en φ E/ρ), `~NE-27` (K-edge contrast
  agents; 511 keV and PET).

## Scope
Three processes carry essentially all of μ between 10 eV and 20 MeV, and their Z
exponents decide everything. **Photoelectric** (σ ~ Z⁴/E³) absorbs the photon
outright and carries the absorption edges — lead's K edge at 88 keV multiplies
μ_ph by 4.7 across zero energy difference, which is why iodine and barium are
contrast agents. **Compton** (σ ~ Z per atom, so ~Z/A ≈ ½ per gram) is
material-independent in its kinematics: E′ depends on angle and energy only, so
the ¹³⁷Cs Compton edge sits at 477 keV in every detector, with the 184 keV
backscatter peak as its complement. **Pair production** (σ ~ Z²) is forbidden
below 1.022 MeV — a conservation law, not a trend — and returns two 0.511 MeV
annihilation photons. Because only the photoelectric effect truly absorbs,
μ counts interactions while μ_en counts deposition; in water at 100 keV only 15%
of the interacting energy stays put.

## Operations — `code/photon_interactions.py`

| call | meaning | reference |
|------|---------|-----------|
| `load_photon_coefficients(m)`, `mass_coefficient(m, E, comp)`, `linear_coefficient` | Appendix C.3, edge-aware log-log interpolation | Table C.3 |
| `photoelectron_energy(E, E_b)` | $E-E_b$ | §7.3.1 |
| `photoelectric_scaling(Z, E, n, m)` | the crude $Z^m/E^n$ trend, for ratios only | Eq. (7.32) |
| `K_EDGE_KEV`, `FLUORESCENT_YIELD` | H → U binding energies; yield 0.005 → 0.965 | §7.3.1 |
| `compton_scattered_energy(E, θ)`, `compton_electron_energy` | $E/[1+(E/m_ec^2)(1-\cos\theta)]$ | Eq. (7.33) |
| `compton_edge(E)`, `backscatter_energy(E)` | 477 and 184 keV for ¹³⁷Cs | §7.3.2 |
| `compton_wavelength_shift_A(θ)` | $(h/m_ec)(1-\cos\theta)$ — a universal constant | §7.3.2 |
| `klein_nishina_per_electron(E)`, `..._per_atom(E, Z)`, `..._mass_coefficient(E, Z/A)` | the full cross section | Eq. (7.34) |
| `pair_production_threshold()`, `triplet_production_threshold()` | 1.022 and 2.044 MeV | §7.3.3 |
| `pair_kinetic_energy_shared(E)`, `annihilation_photon_energy()` | $E_\gamma-2m_ec^2$; 0.511 MeV | Eq. (7.36) |
| `dominant_process(m, E)`, `crossover_energies(m)` | which process leads, and where they swap | Eq. (7.38) |
| `energy_transfer_fraction(m, E)` | $f=\mu_{en}/\mu$ | Eq. (7.39) |
| `MATERIALS`, `Z_OVER_A_NIST_ORDINARY_CONCRETE` | Z/A and densities; the concrete caveat | see `refs.md` |

## Use
```python
from photon_interactions import (mass_coefficient, compton_edge, backscatter_energy,
                                 compton_scattered_energy, klein_nishina_per_electron,
                                 klein_nishina_mass_coefficient, crossover_energies,
                                 energy_transfer_fraction, dominant_process, MATERIALS)

compton_edge(0.6617), backscatter_energy(0.6617)     # 0.4774, 0.1843 MeV  -- 137Cs
compton_scattered_energy(1.0, 3.14159)               # 0.2035 MeV at 180 deg

# Klein-Nishina reproduces the tabulated Compton column to 0.1%
klein_nishina_mass_coefficient(1.0, MATERIALS["water"]["z_over_a"])   # 0.07060
mass_coefficient("water", 1.0, "c")                                   # 0.07066

mass_coefficient("lead", 0.088, "ph")    # 1.547  -- below the K edge
mass_coefficient("lead", 0.0881, "ph")   # 7.298  -- above it: x4.7

crossover_energies("lead")               # (0.556, 4.76) -- a narrow Compton window
crossover_energies("water")              # (0.028, None) -- a wide one
energy_transfer_fraction("water", 0.1)   # 0.154 -- interacting is not depositing
dominant_process("lead", 10.0)           # 'pp'
```

## Run
```bash
cd code
python3 photon_interactions.py        # demo: domains, Klein-Nishina vs table, spectra
python3 test_photon_interactions.py   # tests  ->  "All 22 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/C3_photon_coefficients_*.csv`.

## Files
- `notes.md` — the three processes and their Z exponents → photoelectric and
  absorption edges, with K-fluorescence escape → Compton kinematics, the edge and
  the backscatter peak, Klein–Nishina and exactly where it fails → pair
  production and annihilation → the Compton window and μ_en vs μ, with a
  "Where this goes" map.
- `code/photon_interactions.py`, `code/test_photon_interactions.py` (stdlib
  only). The central test computes Klein–Nishina independently and reproduces
  the tabulated Compton column to **0.1%** above 0.5 MeV; a second test asserts
  the free-electron approximation's failure below the K edge as *physics*
  (ordered in energy and in Z) rather than loosening a tolerance; a third solves
  the table for Z/A and recovers the NIST values.
- `problems/problems.md` — 8 worked problems (S&F Ch. 7 problems 12, 14, 15 plus
  five added: lead as two different shields, K-edge contrast agents,
  Klein–Nishina vs the table, fluorescence escape, and reading a gamma spectrum)
  with numeric `*Check:*` lines.
- `figures/` — the three processes with their domains shaded, lead's nine
  absorption edges with the K-edge deposition collapse, Compton kinematics with
  the ¹³⁷Cs edge and backscatter peak, and f = μ_en/μ across three materials.
- `refs.md` — page-verified citations; **an extraction bug this module exposed**
  (the lead K edge was missing from the Appendix C.3 CSVs — found because the
  tests compare the data against an analytic formula); the ANSI/ANS concrete
  composition taken from the book rather than NIST; and the two table
  conventions (coherent scattering excluded, edge energies duplicated).
