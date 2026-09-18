# NE-18 — Radiation health effects: deterministic & stochastic risk, LNT, standards

Eighteenth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), and the last of Chapter 9. Covers **§§9.5–9.10**
(printed pp. 288–316) of Shultis & Faw, 3rd ed.: acute effects, hereditary risk,
radiogenic cancer, radon, protection standards, and radiation hormesis.

- **Prerequisites:** `~NE-17` (the dose quantities this consumes), `~NE-16`
  (counting statistics — the 0.2 Gy observability floor is a power statement),
  `~NE-07` (secular equilibrium, for the radon chain).
- **Cross-links:** `~NE-22`/`~NE-23` (limits as design constraints), `~NE-27`
  (therapy drives deterministic effects deliberately), `~ST-12`.

## Scope
Two kinds of effect that behave oppositely. **Deterministic** effects have a
threshold below which nobody is affected, and above it the *severity* grows with
dose — 60-day lethality goes from 5% to 99% over a factor of 2.2 in dose.
**Stochastic** effects (cancer, hereditary illness) have no established threshold
and change only the *probability*; they are invisible below ~0.2 Gy, which is
exactly where every regulation is written. Everything in §§9.7–9.9 is therefore
an extrapolation, LNT is the extrapolation regulation uses, and §9.10 is the
book's own account of why that is contested. The module carries all five
candidate dose-effect shapes and fits none.

## Operations — `code/health_effects.py`

| call | meaning | reference |
|------|---------|-----------|
| `deterministic_effects_at(dose)` | which endpoints are possible at all | Table 9.7 |
| `lethality_fraction(dose)` | 60-day lethality, untreated | Table 9.8 |
| `midline_from_free_field(R)` | the ⅔ rule between dose conventions | §9.5.3 |
| `doubling_dose()` | R_human/R_mice = 0.82 Gy | §9.6.2 |
| `hereditary_risk(P, DD, MC, PRCF)` | risk per Gy | Eq. (9.13) |
| `GENETIC_RISKS` | baselines and per-Gy cases | Table 9.11 |
| `cancer_risk_at_age(sex, age, ...)` | excess lifetime risk per 10⁵ per 0.1 Gy | Table 9.13 |
| `scaled_cancer_risk(...)` | the same, scaled linearly — the LNT step, explicit | Ex. 9.6 |
| `cancer_risk_per_gy()` | 0.057 /Gy, the environmental risk factor | §9.7.3 |
| `radiogenic_cancer_deaths(N, D)` | N·D·0.057; **refuses trivial individual doses** | §9.10 |
| `excess_relative_risk(D, sex, a₀, a)` | BEIR-VII solid-cancer ERR | Eq. (9.16) |
| `probability_of_causation(ERR)` | ERR/(1+ERR) | Eq. (9.17) |
| `potential_alpha_energy_per_bq()` | 34 689 MeV/m³ per Bq/m³ EEC | Eqs. (9.19)–(9.20) |
| `equilibrium_equivalent_concentration(C, F)` | EEC = F·C₀ | Eq. (9.21) |
| `annual_radon_exposure(EEC)`, `radon_lung_cancer_risk(...)` | MBq h/m³ and its risk | Tables 9.15–9.16 |
| `wlm_to_bq_h_per_m3` | 1 WLM = 629 000 Bq h/m³ | §9.9 fn. 4 |
| `occupational_limit_sv()`, `public_limit_sv()` | re-derive 50 and 5.7 mSv/y | §9.9.1 |
| `NCRP_1987_LIMITS` | the whole limit table | Table 9.17 |
| `lnt`, `linear_with_threshold`, `quadratic`, `linear_quadratic`, `hormetic` | the five shapes | Fig. 9.3 |

## Use
```python
from health_effects import (deterministic_effects_at, lethality_fraction,
                            scaled_cancer_risk, radiogenic_cancer_deaths,
                            annual_radon_exposure, radon_lung_cancer_risk,
                            equilibrium_equivalent_concentration,
                            occupational_limit_sv, doubling_dose)

deterministic_effects_at(0.2)               # []  -- below every threshold, nobody
deterministic_effects_at(2.3)               # 6 endpoints, incl. marrow death
lethality_fraction(3.25)                    # 0.50  -- LD50/60

scaled_cancer_risk("male", 30, 0.02)        # 6.3e-4 -- S&F Example 9.6
radiogenic_cancer_deaths(1000, 0.1)         # 5.7 deaths
radiogenic_cancer_deaths(1e7, 1e-5)         # raises: same product, no support

eec = equilibrium_equivalent_concentration(46.0, 0.5)      # U.S. average home
radon_lung_cancer_risk(annual_radon_exposure(eec), "smoking male")   # 0.032
radon_lung_cancer_risk(annual_radon_exposure(eec), "nonsmoking male")# 0.0032

occupational_limit_sv() * 1000              # 50 mSv/y, re-derived from Table 9.17's logic
doubling_dose()                             # 0.82 Gy -- a mouse measurement
```

## Run
```bash
cd code
python3 health_effects.py        # demo: thresholds, lethality, Ex. 9.6-9.7, radon, limits
python3 test_health_effects.py   # tests  ->  "All 20 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — deterministic effects and the dose-convention trap → hereditary
  risk and the mouse in the middle → cancer and the region where measurement
  stops → radon's potential alpha energy → what a dose limit actually is →
  hormesis, with a "Where this goes" map and a note on the module's five
  corrections.
- `code/health_effects.py`, `code/test_health_effects.py` (stdlib only). One
  function **refuses**: `radiogenic_cancer_deaths` on an individual dose below a
  tenth of natural background, because LNT will return a confident number from a
  collective dose assembled out of doses nothing has ever been observed at, and
  ICRP-103 advises against exactly that.
- `problems/problems.md` — 8 worked problems (S&F Ch. 9 problems 7, 8, 9, 11, 13,
  14, 16, plus the 1987 Goiânia accident from the solution manual) with numeric
  `*Check:*` lines.
- `figures/` — Table 9.7's thresholds beside the lethality curve, the five
  dose-effect models and the log-axis panel showing where they stop being
  distinguishable, cancer risk against age at exposure for solid cancer and
  leukemia, and where radon's potential alpha energy actually sits.
- `refs.md` — page-verified citations; **five printed results this module
  corrects**, one of them explicitly *unresolvable from the book alone*; the
  solution manual's problem-numbering drift; and the place the module refuses.
