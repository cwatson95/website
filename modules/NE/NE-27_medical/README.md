# NE-27 — Medical applications: imaging, PET/SPECT, radiation therapy

Twenty-seventh and **final** module of the **NUCLEAR SCIENCE & ENGINEERING** trunk
(see `modules/NE/list_NE.txt`). Covers **Chapter 14** (printed pp. 511–554) of
Shultis & Faw, 3rd ed.: x-ray projection imaging, mammography, CT, SPECT, PET,
MRI, radioimmunoassay, diagnostic tracers, and radiation therapy.

- **Prerequisites:** `~NE-11`/`~NE-12` (attenuation and photon interactions),
  `~NE-14` (the Bragg peak), `~NE-15` (detectors), `~NE-18` (dose and effect),
  `~NE-26` (production routes and generators).
- **Cross-links:** `~NE-16` (why sensitivity limits SPECT), `~NE-06` (decay
  during delivery).

## Scope
The chapter divides on a single axis, and it is the module's organising thesis:
**diagnosis wants the smallest dose that still forms an image; therapy wants the
largest dose the tumour can take and the tissue beside it cannot.** Opposite
optimisations of the same quantity. Nearly every technique in Chapter 14 is an
attempt to sharpen one of them spatially, and §14.5's eleven subsections collapse
into three ways of doing it — geometrically, physically, or biochemically.

The module supplies the quantitative spine the chapter leaves out: the Hounsfield
unit (§14.1.5 never defines it), Moseley's law as the reason anode choice *is*
energy choice, the transport calculation behind S&F's remark that only ¹⁸F
travels, and the two floors on PET resolution that no detector can beat.

## Operations — `code/medical.py`

| call | meaning | reference |
|------|---------|-----------|
| `xray_energy(λ)`, `xray_wavelength(E)` | E = hc/λ; reproduces all of Table 14.2 | Table 14.2 |
| `moseley_k_alpha(Z)` | 10.2 eV (Z−1)²; 2% for Mo/Rh, 8% for W | added |
| `ANODE_LINES`, `ATOMIC_NUMBER` | W/Mo/Rh lines, energies, excitation kV | Table 14.2 |
| **`hounsfield_unit(µ)`, `mu_from_hounsfield(HU)`** | **the CT number; refuses HU < −1000** | added |
| `contrast_ratio(µa, µb, t)` | why 20 keV images and 100 keV does not | §14.1.1 |
| `pinhole_resolution(d, f, b)` | object-referred; the caption is dimensionally wrong | §14.1.7 |
| `spect_system_resolution(Rph, RI, M)` | Eq. (14.19), in quadrature | Eq. 14.19 |
| `annihilation_photon_energy()` | 511 keV, two of them, back to back | §14.1.8 |
| `beta_mean_fraction(n)` | Ē/Emax ≈ 0.40 — the β⁺ signature | Table 14.3 |
| `positron_range_mm(Ē)` | the resolution floor: 0.50 mm for ¹⁸F | §14.1.8 |
| `coincidence_window_length(τ)` | cτ/2 = 150 cm at 10 ns | §14.1.8 |
| `activity_after_transport(n, t)`, `usable_transport_time(n)` | 6.1 h for ¹⁸F, 6.8 min for ¹⁵O | §14.1.8 |
| `therapeutic_ratio(Dt, Dn)` | **refuses ratio ≤ 1** — that is not therapy | §14.5 |
| `brachytherapy_dose_rate(S, r)` | 1/r²; a factor of 400 over 0.5–10 cm | §14.5.9 |
| `PET_NUCLIDES`, `SPECT_TRACERS`, `THERAPY_MODALITIES` | the data, sourced separately | Table 14.3 + `data_tables/` |
| `CANCER_2004`, `CANCER_LIFETIME_RISK`, `CT_NOBEL` | Tables 14.6/14.7; the Nobel erratum | Tables 14.6–14.7 |

## Use
```python
from medical import (xray_energy, moseley_k_alpha, hounsfield_unit,
                     mu_from_hounsfield, beta_mean_fraction, positron_range_mm,
                     coincidence_window_length, usable_transport_time,
                     therapeutic_ratio, spect_system_resolution)

xray_energy(0.7093)             # 17.48 keV -- Mo Ka1, the mammography line
moseley_k_alpha(42)             # 17.1 keV  -- from Z alone, within 2%

hounsfield_unit(0.206)          # 0.0    -- water, by construction
mu_from_hounsfield(-1200)       # raises: below air is a negative mu

beta_mean_fraction("18F")       # 0.394  -- the beta-plus signature, not 0.33
positron_range_mm(0.250)        # 0.50 mm for 18F; 2.52 mm for 15O
coincidence_window_length(10.0) # 150 cm -- timing does not localise

usable_transport_time("18F")    # 6.09 h -- the only one you can ship
usable_transport_time("15O")    # 0.11 h -- 6.8 minutes

spect_system_resolution(3.0, 4.5, 2.0)   # 3.75 mm; a better crystal buys 25%
therapeutic_ratio(30.0, 60.0)   # raises: that is not therapy, it is harm
```

## Run
```bash
cd code
python3 medical.py        # demo: anodes, CT numbers, PET transport, therapy, the tables
python3 test_medical.py   # tests  ->  "All 13 tests passed."
cd ../figures && python3 make_figures.py
```

## Findings
Two errata and two gaps, each pinned by a test so a later reader cannot quietly
re-absorb them:

- **§14.1.5, p. 521** — "shared the Nobel prize in **1972**". The prize was
  **1979**; 1972 is the year of the first published CT images. Verified against
  nobelprize.org.
- **Fig. 14.16 caption, p. 528** — "R_ph = (d/b)/(f+b)" has units of 1/length.
  The intended product d(f+b)/b is the *image*-plane blur; the body text's
  (d/f)(f+b) is the object-referred one, and only that form closes Eq. (14.19).
- **The Hounsfield unit is never defined**, though §14.1.5 develops the Radon
  transform and filtered backprojection in full and names Hounsfield.
- **Table 14.5 carries no quantitative data** (process → tracer only), so the
  module's SPECT energies and half-lives come from `../data_tables/`, and the
  tests re-read that CSV rather than trusting the dict.

Confirmed by recomputation: Table 14.2 (E = hc/λ, worst error 1.6 × 10⁻⁴);
Table 14.3 (Ē/Emax = 0.402/0.410/0.424/0.394, and every entry reproduced from
`D1_decay_radiation.csv` to 0.5%, with the 511 keV yield exactly twice the
positron branch); Table 14.6 (all four columns sum exactly to the printed
totals, giving the text's 1.37 M and 564 k); Table 14.7 (46.6% "nearly half",
49%/48% "about half survive").

## Files
- `notes.md` — the anode fixes the energy → contrast is spent by 100 keV → the
  unit the chapter never defines → SPECT is a collimator problem → PET's two
  floors → why ¹⁸F alone travels → nine ways of sharpening one ratio → the
  numbers therapy is aimed at, with a "Where this goes" map.
- `code/medical.py`, `code/test_medical.py` (stdlib only; the tests read
  `../../data_tables/D1_decay_radiation.csv`). `mu_from_hounsfield` **refuses**
  below −1000 HU; `therapeutic_ratio` **refuses** a ratio of 1 or less.
- `problems/problems.md` — 6 worked problems with numeric `*Check:*` lines.
- `figures/` — the anode's fixed lines against Moseley, the CT-number scale,
  PET decay during delivery, and PET's two irreducible resolution limits.
- `refs.md` — page-verified citations, the relations the chapter omits, and the
  two errata with the reasoning that establishes them.
