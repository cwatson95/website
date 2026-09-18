# NE-15 — Radiation detectors: gas-filled, scintillation, semiconductor

Fifteenth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§§8.1–8.5** (printed pp. 221–259) of Shultis
& Faw, 3rd ed. — Chapter 8 is guest-written by Douglas S. McGregor: gas-filled
detectors and their operating regions, scintillators inorganic and organic,
semiconductor detectors, personal dosimeters, and a survey of exotic detectors.

- **Prerequisites:** `~NE-12` (what a spectrum's features are, and the Z⁴ that
  picks detector materials), `~NE-14` (a detector must stop the particle),
  `~NE-13` (¹⁰B and ⁶Li for neutrons), `~NE-08` (elastic recoil, for fast-neutron
  detection).
- **Cross-links:** `~NE-16` (counting statistics and dead time), `~NE-17`
  (dosimeters), `~NE-27` (PET's demand for fast dense scintillators).

## Scope
One quantity organises the whole chapter: the number of information carriers per
event, N = E/w. Resolution is 2.355√(F/N), so it improves as 1/√N and **the only
lever is w**. Germanium spends 2.98 eV per electron–hole pair, argon 26 eV per
ion pair, NaI(Tl) ~150 eV per *usable photoelectron* — and that ladder is the
entire ranking of detector families. Gas detectors are four instruments from one
equation, M = f/(1−δf), whose divergence at δf = 1 *is* the proportional-to-Geiger
transition. Scintillators trade brightness against speed, with the caveat that the
photon yield is not the carrier count: NaI's 38 000 photons/MeV become ~6 600
photoelectrons. Semiconductors win on w but trade band gap against thermal noise
(Ge needs cooling) and Z against resolution (CdTe stops better, resolves worse).

## Operations — `code/detectors.py`

| call | meaning | reference |
|------|---------|-----------|
| `carriers_produced(E, w)` | N = E/w | §8.6.2 |
| `carrier_sigma(N, F)` | √(FN) — Fano-suppressed | added, see `refs.md` |
| `intrinsic_resolution_percent(E, w, F)` | 2.355√(F/N) as a percentage | §8.6.2 |
| `fwhm_energy(E, w, F)` | absolute peak width | §8.6.2 |
| `gas_multiplication(f, δ)` | f/(1−δf); **raises past δf = 1** | Eq. (8.7) |
| `townsend_series_terms(f, δ, n)` | the series it sums | Eq. (8.6) |
| `scintillator_photoelectrons(E, s, ...)` | photons → collected → photoelectrons | §8.2.3 |
| `photopeak_resolution_percent(E, s, ...)` | from the photoelectron count | §8.2 |
| `compare_resolution(E)` | all families ranked, best first | §§8.1–8.3 |
| `SEMICONDUCTORS`, `SCINTILLATORS_INORGANIC`, `SCINTILLATORS_ORGANIC` | Tables 8.2 and 8.1 | Tables 8.1–8.2 |
| `GAS_W_VALUES`, `FANO_FACTORS` | added — S&F tabulate neither | see `refs.md` |

## Use
```python
from detectors import (carriers_produced, intrinsic_resolution_percent,
                       gas_multiplication, scintillator_photoelectrons,
                       photopeak_resolution_percent, compare_resolution,
                       SEMICONDUCTORS, FANO_FACTORS)

carriers_produced(0.6617, 2.98)                       # 222 000 pairs in Ge
intrinsic_resolution_percent(0.6617, 2.98, 0.13)      # 0.18%  -- germanium
photopeak_resolution_percent(0.6617, "NaI(Tl)")       # 3.55%  -- sodium iodide

scintillator_photoelectrons(1.0, "NaI(Tl)")           # 6650, not 38000
intrinsic_resolution_percent(0.6617, 2.98, 1.0)       # 0.50% -- Poisson, 2.8x too wide

gas_multiplication(10.0, 0.09)                        # 100 -- proportional
gas_multiplication(10.0, 0.15)                        # raises: Geiger-Mueller regime

for lab, w, n, r in compare_resolution():             # every family, ranked
    print(lab, w, n, r)
```

## Run
```bash
cd code
python3 detectors.py        # demo: family comparison, Tables 8.1-8.2, multiplication
python3 test_detectors.py   # tests  ->  "All 14 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — why the carrier count is everything → gas detectors as one
  equation with four regimes → scintillators and the photon-vs-photoelectron
  trap → semiconductors, the band-gap trade-off and the Fano factor → what the
  ⁶⁰Co doublet looks like in each, with a "Where this goes" map.
- `code/detectors.py`, `code/test_detectors.py` (stdlib only). Tests check the
  resolution ladder, both of Table 8.1's traps (the "relative response" column is
  not the light yield; the photon count is not the carrier count), the Townsend
  series against its closed form, and that the divergence is refused rather than
  returned. One test asserts the computed values sit **below** measured detector
  performance, so the module cannot be mistaken for a predictor.
- `problems/problems.md` — 7 worked problems (S&F Ch. 8 problems 1, 3, 4, 5, 6, 8,
  9) with numeric `*Check:*` lines.
- `figures/` — resolution against carrier count with every family placed on it,
  the gas-multiplication curve with the four operating regions shaded, the
  scintillator brightness–speed trade-off, and the ⁶⁰Co doublet as germanium and
  NaI each see it.
- `refs.md` — page-verified citations; **two quantities this module adds**
  (the Fano factor, which S&F never mention and without which germanium's
  resolution is wrong by 2.8×, and gas W-values); and an explicit statement that
  every number here is a lower bound.
