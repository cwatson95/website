# NE-14 — Charged-particle stopping: range, stopping power, the Bragg peak

Fourteenth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), and the last of Chapter 7. Covers **§7.5** (printed
pp. 205–217) of Shultis & Faw, 3rd ed.: why charged particles have a definite
range, straggling and the three range definitions, collisional and radiative
stopping power, the Bragg curve, the CSDA range and its scaling rules,
bremsstrahlung, and fission-fragment ranges.

- **Prerequisites:** `~NE-11`–`~NE-13` (the neutral-particle picture this
  inverts), `~NE-08` (the 2.2 keV maximum transfer to one electron), `~NE-12`
  (the electrons and pairs that photons set in motion), `~NE-09` (fission
  fragments).
- **Cross-links:** `~NE-15` (a detector must stop the particle to measure it),
  `~NE-17` (dose is deposited energy; these ranges decide external vs internal
  hazard), `~NE-18` (the Bragg peak is why w_R(α) = 20), `~NE-27` (proton
  therapy).

## Scope
Neutral particles interact a handful of times and attenuate exponentially, with
no range. Charged particles interact continuously with many electrons at once,
lose very little each time, and so slow down almost deterministically and **stop
at a definite range** — a beam is unattenuated until the end, then falls off a
cliff. Stopping power goes as z²(Z/A) and *rises* as the particle slows, so
energy deposition peaks just before the stop: the **Bragg peak**, which is why a
proton beam can put its dose maximum inside a tumour and nothing beyond. Ranges
follow S&F's empirical fit over 0.1–10 MeV, with three scaling rules (ρR is
density-independent; ρR ∝ m/z² at matched speed). Bremsstrahlung is an
electron-only problem — the (m_e/M)² makes a proton's radiative loss 3×10⁶ times
smaller — and its linear Z is why beta shields are plastic first, lead second.

## Operations — `code/charged_particles.py`

| call | meaning | reference |
|------|---------|-----------|
| `csda_mass_range(particle, material, E)` | ρR (g/cm²); **raises outside 0.1–10 MeV** | Eq. (7.47) |
| `csda_range(..., density)` | the same as a length | §7.5.4 |
| `range_energy_valid(E)` | is E inside the fit's stated window | §7.5.4 |
| `RANGE_CONSTANTS_PROTON / _ALPHA / _ELECTRON` | Tables 7.2 and 7.3 | Tables 7.2–7.3 |
| `SUSPECT_RANGE_CONSTANTS` | the withheld proton/Pb row | see `refs.md` |
| `EXAMPLE_7_7_B_DISCREPANCY` | the example's wrong b | see `refs.md` |
| `equivalent_proton_energy(E, m)` | proton energy at matched speed | Example 7.7 |
| `scaled_heavy_range(ρR_p, m, z)` | ρR ∝ m/z² | Eq. (7.46) |
| `radiative_to_collisional(E, Z, m_e/M)` | EZ/700 (m_e/M)² | Eq. (7.43) |
| `bremsstrahlung_crossover_energy(Z)` | 700/Z MeV | Example 7.6 |
| `fission_fragment_range(E, material)` | C E^(2/3) mg/cm² | Eq. (7.48) |
| `energy_deposition_depth_fraction(f)` | range is a path length, not a depth | §7.5.4 |

## Use
```python
from charged_particles import (csda_mass_range, csda_range, scaled_heavy_range,
                               equivalent_proton_energy, radiative_to_collisional,
                               bremsstrahlung_crossover_energy, fission_fragment_range,
                               energy_deposition_depth_fraction)

csda_range("alpha", "H2O", 4.0, 1.0) * 1e4        # 27.9 um  -- stops in the skin
csda_range("proton", "H2O", 4.0, 1.0) * 1e4       # 235 um
csda_range("electron", "water", 1.0, 1.0) * 10    # 4.35 mm

# Example 7.7: a 6 MeV triton, via a proton at the same speed
ep = equivalent_proton_energy(6.0, 3.0160492)     # 2.00 MeV
scaled_heavy_range(csda_mass_range("proton", "H2O", ep), 3.0160492, 1)   # 0.0216 g/cm2

bremsstrahlung_crossover_energy(79)               # 8.9 MeV in gold (Example 7.6)
radiative_to_collisional(2.0, 82)                 # 0.234 -- 23% of a 2 MeV beta
radiative_to_collisional(2.0, 6)                  # 0.017 -- so shield with plastic

fission_fragment_range(99.9, "aluminum")          # 4.09 mg/cm2 = 15 um
energy_deposition_depth_fraction(0.90)            # 0.70 -- depth < range

csda_mass_range("proton", "H2O", 0.05)            # raises: outside the fit's window
csda_mass_range("proton", "Pb", 4.0)              # raises: Table 7.2's row is corrupt
```

## Run
```bash
cd code
python3 charged_particles.py        # demo: ranges, scaling, bremsstrahlung, fragments
python3 test_charged_particles.py   # tests  ->  "All 14 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — why charged particles differ from neutral ones → stopping power
  and the Bragg peak → the range fit and its three scaling rules →
  bremsstrahlung and the low-Z-first shield → range is a path length, not a
  depth, with a "Where this goes" map.
- `code/charged_particles.py`, `code/test_charged_particles.py` (stdlib only).
  Ranges are checked against the **NIST STAR codes** the book's tables were
  fitted to — an independent source — and the module refuses to evaluate outside
  the fit's stated window or to use the corrupt lead row.
- `problems/problems.md` — 7 worked problems (S&F Ch. 7 problems 17–21 plus two
  added: why an alpha emitter is safe outside and lethal inside, and how to
  layer a beta shield) with numeric `*Check:*` lines.
- `figures/` — range vs energy for the three particles, the range-vs-exponential
  contrast that defines the module, Bragg curves reconstructed by
  differentiating the range–energy relation, and the bremsstrahlung crossover.
- `refs.md` — page-verified citations; **two errors in Table 7.2 / Example 7.7**
  (the proton/Pb row is withheld as unusable; the example uses the LiF row's b);
  a quantitative accuracy assessment of Eq. (7.47) that the book omits; and a
  note on a test that was initially passing vacuously.
