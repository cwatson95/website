# NE-17 — Dosimetry: kerma, absorbed dose, equivalent & effective dose

Seventeenth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), opening Chapter 9. Covers **§§9.1–9.4** (printed
pp. 270–288) of Shultis & Faw, 3rd ed.: dosimetric quantities, kerma and absorbed
dose, exposure, quality factors, effective dose, internal dose from ingestion,
and natural background.

- **Prerequisites:** `~NE-11` (fluence and reaction rates), `~NE-12` (μ_tr vs
  μ_en), `~NE-13` (elastic scattering kinematics, reused for neutron kerma).
- **Cross-links:** `~NE-18` (turns effective dose into risk), `~NE-16` (every
  measured dose is a count), `~NE-27` (imaging and therapy dosimetry).

## Scope
It takes four quantities to get from "there is a radiation field" to "this is how
much it matters", and each one is a correction to the last: **kerma** (energy
released to charged particles), **absorbed dose** (energy actually deposited),
**equivalent dose** (weighted by track density), **effective dose** (weighted by
which organ). The gaps between them are the physics — bremsstrahlung separates
the first two by 6.5% in iron at 5 MeV, the quality factor spans a factor of 20,
and the organ weights span 25. The module also closes the conversion S&F leave
open, 1 R = 8.73 mGy in air, which is what turns a survey-meter reading into a
dose.

## Operations — `code/dosimetry.py`

| call | meaning | reference |
|------|---------|-----------|
| `mass_coefficient(mat, E, comp)` | μ/ρ from Appendix C.3; `interpolation=` linear or log-log | App. C.3 |
| `point_source_fluence(S, t, r, mu)` | S t e^{−μr}/4πr² | Eq. (7.25) |
| `kerma(E, mu_tr_over_rho, Φ)` | 1.602e−10 E (μ_tr/ρ) Φ | Eq. (9.5) |
| `absorbed_dose(E, mu_en_over_rho, Φ)` | the same with μ_en | Eq. (9.6) |
| `photon_kerma_rate`, `photon_dose_rate` | the above with the table lookup done | Ex. 9.1 |
| `photon_dose_rate_from_lines(...)` | a discrete spectrum, optionally attenuated | Probs. 4–5 |
| `exposure(E, mu_en_air, Φ)` | 1.835e−8 E (μ_en/ρ)_air Φ, in roentgen | Eq. (9.9) |
| `roentgen_to_air_dose(X)` | **1 R = 8.73 mGy** | added |
| `neutron_recoil_fraction(A)` | 2A/(A+1)² | Eq. (9.7) |
| `neutron_kerma`, `water_neutron_kerma_coefficient` | fast-neutron kerma | Eq. (9.8) |
| `quality_factor(kind, E)` | Table 9.1; **refuses unknown radiations** | Table 9.1 |
| `dose_equivalent(D, QF)` | H = QF·D | Eq. (9.10) |
| `effective_dose(organ_doses, weights)` | Σ w_T H_T; **refuses unweighted organs** | Eqs. (9.11)–(9.12) |
| `ICRP77/90/07_TISSUE_WEIGHTS` | three vintages of w_T | Tables 9.2–9.3 + added |
| `committed_effective_dose(intakes)` | 50-y committed dose, 68 nuclides | Table 9.4 |
| `NATURAL_BACKGROUND_WORLD / _US` | 2.4 and 3.0 mSv/y | Tables 9.5–9.6 |
| `rule_of_thumb_exposure_rate`, `rule_of_thumb_valid_range` | 6CEN/r² and where it holds | Prob. 6 |

## Use
```python
from dosimetry import (point_source_fluence, photon_kerma_rate, photon_dose_rate,
                       linear_coefficient, roentgen_to_air_dose, quality_factor,
                       dose_equivalent, effective_dose, committed_effective_dose,
                       ICRP90_TISSUE_WEIGHTS, BQ_PER_CI)

phi = point_source_fluence(1e8, 1.0, 100.0,            # S&F Example 9.1
                           linear_coefficient("water", 5.0, "total"))
photon_kerma_rate("iron", 5.0, phi) * 3.6e9            # 2.34 uGy/h
photon_dose_rate("iron", 5.0, phi) * 3.6e9             # 2.20 uGy/h -- kerma is 6.5% high

roentgen_to_air_dose(0.010) * 1e6                      # 87.3 uGy/h from 10 mR/h
dose_equivalent(1.0, quality_factor("neutron", 1.0))   # 20 Sv from 1 Gy
quality_factor("muon")                                 # raises: will not assume QF = 1

effective_dose({"lung": 20.0, "thyroid": 5.0}, ICRP90_TISSUE_WEIGHTS)   # 2.65
effective_dose({"lung": 20.0, "pancreas": 5.0})        # raises: no weight for pancreas

committed_effective_dose({"59Fe": 1e-3 * BQ_PER_CI,    # S&F Example 9.5
                          "60Co": 50e-6 * BQ_PER_CI})  # 0.072 Sv = 7.2 rem, NOT 7.1 mrem
```

## Run
```bash
cd code
python3 dosimetry.py        # demo: Examples 9.1-9.5, the R->Gy conversion, the rule of thumb
python3 test_dosimetry.py   # tests  ->  "All 21 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — the four quantities and why each is needed → exposure and the
  missing conversion → neutron kerma → quality factor → effective dose as risk
  arithmetic → internal dose and the natural yardstick, with a "Where this goes"
  map and a note on the module's four corrections.
- `code/dosimetry.py`, `code/test_dosimetry.py` (stdlib only; coefficients read
  from `../../data_tables/`). Two functions **refuse** rather than answering:
  `quality_factor` on an unrecognised radiation (defaulting to 1 understates a
  fast-neutron dose twentyfold) and `effective_dose` on an organ with no
  weighting factor (silent omission always biases toward "safe").
- `problems/problems.md` — 8 worked problems (S&F Ch. 9 problems 1–6, plus two
  added: reading a survey meter, and a mixed n/γ field) with numeric `*Check:*`
  lines.
- `figures/` — dose per unit fluence for four materials beside the kerma/dose
  gap, the 6CEN/r² rule against the exact Eq. (9.9) with its 20% band, the
  quality factor's factor of twenty against the fission spectrum, and what
  natural background is actually made of beside three vintages of tissue weights.
- `refs.md` — page-verified citations; **four printed results this module
  corrects**, each with the evidence; three things the chapter needs and omits
  (the R→Gy conversion, ICRP-103, thermal-neutron kerma); and the two places the
  module refuses.
