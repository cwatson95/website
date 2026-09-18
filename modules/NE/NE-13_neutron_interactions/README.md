# NE-13 — Neutron interactions: the 1/v law, resonances, activation, fission

Thirteenth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§7.4** (printed pp. 196–205) of Shultis &
Faw, 3rd ed.: why neutron cross sections resist theory, the 1/v law, resonance
structure by nuclide mass, the reactions that matter at each energy, neutron
activation, and fission cross sections.

- **Prerequisites:** `~NE-11` (Σ = σN, mean free path, R = Σφ), `~NE-12` (the
  smooth-photon contrast this module is built against), `~NE-08` (elastic
  kinematics, ξ, the compound nucleus behind every resonance), `~NE-09`
  (fissile vs fissionable), `~NE-07` (decay with production).
- **Cross-links:** `~NE-19` (η is the first of the four factors; resonance
  escape is another), `~NE-20` (¹³⁵Xe poisoning), `~NE-21` (diffusion supplies
  the flux), `~NE-15` (¹⁰B and ⁶Li as detector materials), `~NE-26` (activation
  analysis as a measurement technique).

## Scope
Neutrons interact with the nucleus, not the electrons, so none of NE-12's
scalings survive — cross sections vary erratically between isotopes of the same
element (¹H/²H by 658×, ¹⁰B/¹¹B by 700 000×) and S&F state plainly that no
predictive theory exists. Two regularities carry reactor physics. The **1/v law**
makes absorption rise as neutrons slow: 1 keV → thermal multiplies capture by
199, and ²³⁵U fission by ~600, which is what buys the 115 graphite collisions of
NE-08. **Resonances** are narrow enormous peaks whose character shifts with mass
— keV-wide for light nuclei, sub-eV for heavy ones and unresolvable above a few
keV — and a fission neutron must fall through the heavy-nuclide resonance forest
to reach thermal, which is the resonance-escape problem and the reason fuel is
lumped. Activation follows the saturation law, and the module keeps both the
exact form and the book's stated approximation. Finally η = νσ_f/σ_a, not ν, is
what must exceed 1 for a chain reaction.

## Operations — `code/neutron_interactions.py`

| call | meaning | reference |
|------|---------|-----------|
| `load_thermal_cross_sections()`, `load_activation_data()` | Appendices C.1 and C.2 | Tables C.1, C.2 |
| `absorption_cross_section`, `scattering_cross_section`, `total_cross_section`, `fission_cross_section` | σ_a (all removal channels), σ_s, σ_t, σ_f | Table C.1 |
| `capture_to_fission_ratio(nuc)` | α = σ_γ/σ_f | §7.4.2 |
| `eta_neutrons_per_absorption(nuc, nu)` | η = νσ_f/σ_a — what must exceed 1 | §7.4.2 |
| `neutron_speed(E)`, `neutron_energy_from_speed(v)`, `maxwellian_most_probable_energy(T)` | the 0.0253 eV / 2200 m/s / 293.6 K point | §7.4 |
| `one_over_v_cross_section(σ_ref, E)` | σ ∝ 1/√E ∝ 1/v | Eq. (7.40) |
| `light_nucleus_total_cross_section(σ1, σ2, E)` | σ₁ + σ₂/√E; **raises above 1 keV** | Eq. (7.40) |
| `classify_nuclide(A)`, `resonance_character(A)` | light/intermediate/heavy; where resonances live | §7.4.1 |
| `SECONDARY_NEUTRON_THRESHOLDS` | (n,2n): ~8 MeV typical, D 3.3, Be 1.84 | §7.4.1 |
| `activation_rate`, `activation_activity`, `saturation_activity` | R = (mN_A/A)σφ; R[1−e^{−λt}] | Example 7.5 |
| `atom_density`, `macroscopic_cross_section`, `mean_free_path` | the NE-11 machinery for neutrons | §7.1.6 |
| `is_fissile`, `is_fissionable` | the §7.4.2 classification | §7.4.2 |

## Use
```python
from neutron_interactions import (absorption_cross_section, one_over_v_cross_section,
                                  eta_neutrons_per_absorption, capture_to_fission_ratio,
                                  activation_activity, saturation_activity,
                                  load_thermal_cross_sections, load_activation_data,
                                  resonance_character, E_THERMAL_EV)

xs = load_thermal_cross_sections()
absorption_cross_section("10B", xs) / absorption_cross_section("11B", xs)   # 694485

s0 = absorption_cross_section("1H", xs)
one_over_v_cross_section(s0, 1000.0) / s0        # 0.0050 -- 1 keV is 199x weaker

eta_neutrons_per_absorption("233U", 2.48, xs)    # 2.282  -- highest, despite lowest nu
capture_to_fission_ratio("239Pu", xs)            # 0.362  -- the plutonium penalty

resonance_character(238)["width"]                # '1 eV or less'

mn = load_activation_data()["56Mn"]              # Example 7.5
activation_activity(2.0, 55.0, mn["sigma_b"], 1e13, 120.0, 2.579*3600)   # 2.598e10 Bq
saturation_activity(2.0, 55.0, mn["sigma_b"], 1e13)                      # 2.913e12 Bq
```

## Run
```bash
cd code
python3 neutron_interactions.py        # demo: 1/v, resonances, Example 7.5, eta
python3 test_neutron_interactions.py   # tests  ->  "All 18 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/C1_thermal_neutron_cross_sections.csv` and
`../../data_tables/C2_activation_radionuclides.csv`.

## Files
- `notes.md` — why there is no theory to fit → the 1/v law and what moderation
  buys → resonances by mass and the resonance-escape problem → what happens at
  each energy, with the Be/D (n,2n) anomaly → activation and saturation →
  σ_f, α and η, with a "Where this goes" map.
- `code/neutron_interactions.py`, `code/test_neutron_interactions.py` (stdlib
  only). `light_nucleus_total_cross_section` **raises above 1 keV** rather than
  extrapolating past Eq. (7.40)'s stated range, and `activation_activity`
  requires the half-life explicitly so the short-irradiation approximation is a
  choice rather than a default.
- `problems/problems.md` — 7 worked problems (S&F Ch. 7 Prob. 16, Example 7.5,
  plus five added: what moderation buys, why ¹⁰B is enriched, why η beats ν, the
  moderator trade-off, and why fuel is lumped) with numeric `*Check:*` lines.
- `figures/` — the 1/v law across eight decades, the erratic isotope scatter with
  same-element pairs joined, resonance bands by nuclide class against the thermal
  and fission-spectrum markers, and activation saturation with Example 7.5 marked
  at 0.9% of the way up.
- `refs.md` — page-verified citations; the Example 7.5 approximation kept
  alongside the exact form; the meaningful blank in Table C.2; and the 0.2%
  inconsistency in the thermal reference point.
