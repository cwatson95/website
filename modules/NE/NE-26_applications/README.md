# NE-26 — Industrial & research applications: tracers, radiography, NAA, gauges

Twenty-sixth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **Chapter 13** (printed pp. 476–510) of Shultis
& Faw, 3rd ed.: radioisotope production, tracer applications, radiography and
gauging, neutron activation analysis, and radiation processing.

- **Prerequisites:** `~NE-06`/`~NE-07` (decay and Bateman), `~NE-11`/`~NE-12`
  (attenuation), `~NE-16` (counting statistics).
- **Cross-links:** `~NE-27` (medical applications), `~NE-18` (the dose scale),
  `~NE-23` (where fission-product sources come from).

## Scope
A catalogue of three dozen applications, organised by what is physically
happening: radiation as a **label** (tracers), materials affecting radiation
(**gauges**, radiography, NAA), and radiation affecting materials
(**sterilisation**, food, polymers). Almost none of it needs new physics — it
needs the earlier chapters applied with an eye on *sensitivity*, which is where
the chapter stops short. The module supplies the three relations that convert a
description into a design, chief among them the transmission-gauge optimum
**µt = 2**.

## Operations — `code/applications.py`

| call | meaning | reference |
|------|---------|-----------|
| `activation_activity(R, T½, t)`, `saturation_fraction(t, T½)` | A = R(1−e^{−λt}) | §13.1 |
| `irradiation_time_for(f, T½)` | **refuses f ≥ 1** — saturation is asymptotic | §13.1 |
| `generator_daughter_activity(t)`, `optimal_milking_time()` | the ⁹⁹Mo cow; 48.5 h | §13.1 + added |
| `tracer_dilution_volume(V₀, C₀, C)` | V = V₀(C₀/C); only the ratio matters | §13.3.6 |
| `flow_rate_from_tracer(Q₀, C)` | q = Q₀/C, with no cross-section | §13.3.4 |
| `transit_flow_rate(d, t, A)` | the peak-to-peak method | §13.3.4 |
| `radiodate(ratio, T½)` | the decaying clock | §13.3.12 |
| `transmission(µ, t)`, `thickness_from_transmission(I/I₀, µ)` | the gauge, both ways | §13.4.2 |
| **`gauge_precision(µ, t, N₀)`, `optimal_gauge_thickness()`** | **σ_t/t, and µt = 2** | added |
| `geometric_unsharpness(F, d, D)` | the radiographic penumbra | added |
| `naa_detectable_mass(element, h, φ)` | Table 13.3, scaled | Table 13.3 |
| `PRODUCTION_ROUTES`, `GENERATORS`, `RADIOGRAPHY_SOURCES`, `NAA_SENSITIVITY`, `PROCESS_DOSES` | the chapter's data | Tables 13.1–13.3 |

## Use
```python
from applications import (saturation_fraction, optimal_milking_time,
                          generator_daughter_activity, tracer_dilution_volume,
                          flow_rate_from_tracer, gauge_precision,
                          optimal_gauge_thickness, naa_detectable_mass,
                          irradiation_time_for)

saturation_fraction(3.0, 1.0)          # 0.875 -- three half-lives
irradiation_time_for(1.0, 1.0)         # raises: saturation is never reached

optimal_milking_time("99Mo")           # 48.5 h -- why generators are eluted daily
generator_daughter_activity(24.0)      # 95% of the peak already

tracer_dilution_volume(10.0, 1e6, 2.5) # 4.0e6 cm3 -- no calibration needed
flow_rate_from_tracer(1e7, 50.0)       # 2e5 m3/s -- no cross-section needed

optimal_gauge_thickness()              # 2.0 mean free paths, exactly
optimal_gauge_thickness(mu=0.4)        # t = 5 cm for that material
gauge_precision(0.5, 1.0, 1e6) / gauge_precision(2.0, 1.0, 1e6)   # 1.89x worse

naa_detectable_mass("Eu")              # 9e-7 ug -- four billion atoms
naa_detectable_mass("Fe")              # 10 ug -- seven decades worse
```

## Run
```bash
cd code
python3 applications.py        # demo: production, the cow, tracers, the gauge optimum, NAA
python3 test_applications.py   # tests  ->  "All 9 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — the production route decides the decay mode → the ⁹⁹Mo cow → why
  tracers need no calibration → the gauge optimum and why it does *not* describe
  radiography → NAA's seven decades → the dose ladder, with a "Where this goes"
  map and a note on what the module adds.
- `code/applications.py`, `code/test_applications.py` (stdlib only).
  `irradiation_time_for` **refuses** a saturation fraction of 1 or more, which is
  asymptotic and unreachable; `tracer_dilution_volume` refuses a mixed
  concentration above the injected one, which a dilution cannot produce.
- `problems/problems.md` — 6 worked problems with numeric `*Check:*` lines.
- `figures/` — activation saturation beside the generator ingrowth curve, the
  gauge optimum with its tolerance band, NAA's seven decades sorted, and the
  process-dose ladder against a human LD50.
- `refs.md` — page-verified citations; the three relations the chapter needs and
  omits; and why the µt = 2 rule must be kept away from Table 13.2.
