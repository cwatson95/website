# NE-15 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |
| Shultis & Faw, *Problem Solution Manual*, 3rd ed. (2016) | `NE_Nuclear_Engineering/nuclear_science_sol_shultis_faw.pdf` | indexed by chapter/problem |

Chapter 8 is by **Douglas S. McGregor** (Kansas State University), credited on
the chapter title page — the only guest-authored chapter in the book.

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| The three requirements of a detector | Ch. 8 opening | 221 | 244 |
| Gas-filled detectors; the six operating regions | §8.1, §8.1.1 | 222–224 | 245–247 |
| Ion chambers | §8.1.2 | 226 | 249 |
| Field in a cylindrical counter, $E(r)$ | Eqs. (8.1)–(8.2) | 231 | 254 |
| Avalanche onset | Eqs. (8.3)–(8.5) | 231–232 | 254–255 |
| **Townsend series** $M=\sum\delta^{i-1}f^i$ (`townsend_series_terms`) | Eq. (8.6) | 232 | 255 |
| **$M=f/(1-\delta f)$** (`gas_multiplication`) | Eq. (8.7) | 232 | 255 |
| Proportional counters | §8.1.3 | 230 | 253 |
| Geiger–Müller counters; the self-sustaining avalanche | §8.1.4 | 236 | 259 |
| Scintillation detectors | §8.2 | 237 | 260 |
| **Table 8.1** — scintillator properties (`SCINTILLATORS_*`) | Table 8.1 | 238 | 261 |
| Inorganic scintillators | §8.2.1 | 239 | 262 |
| Organic scintillators; anthracene reference | §8.2.2 | 243 | 266 |
| Light collection | §8.2.3 | 245 | 268 |
| Semiconductor detectors | §8.3 | 247 | 270 |
| **Table 8.2** — semiconductor properties (`SEMICONDUCTORS`) | Table 8.2 | 244 | 267 |
| Ge detectors; the cooling requirement | §8.3.1 | 249 | 272 |
| Si detectors | §8.3.2 | 251 | 274 |
| Compound semiconductors (CdTe, CZT, HgI₂) | §8.3.3 | 252 | 275 |
| Personal dosimeters: film, pocket chambers, TLD/OSL | §8.4 | 253–255 | 276–278 |
| Cloud/bubble chambers, cryogenic detectors, IceCube | §8.5 | 255–258 | 278–281 |
| FWHM = 2.355σ; resolution = 235.5σ/E | §8.6.2 | 262 | 285 |

## Problems (verified, S&F 3rd ed. Ch. 8)
Chapter 8's problems begin on printed **268** (PDF 291). Problems **1, 3, 4, 5,
6, 8, 9** belong to this module; **2** (dead time) and **7** (counting
statistics) are `~NE-16`.

- **Prob. 1** — three changes to a proportional counter — printed 268, PDF 291.
- **Prob. 3** — collecting 90% of NaI(Tl) light — printed 269, PDF 292.
- **Prob. 4** — scintillation efficiency of anthracene — printed 269, PDF 292.
- **Prob. 5** — air in an ion chamber but not a proportional counter — printed 269, PDF 292.
- **Prob. 6** — FWHM from an 8% resolution — printed 269, PDF 292.
- **Prob. 8** — choosing a scintillator by radiation type — printed 269, PDF 292.
- **Prob. 9** — HPGe against Si(Li) — printed 269, PDF 292.

## Two things this module adds, because the arithmetic needs them

S&F's Chapter 8 is descriptive where the rest of the book is quantitative: it
tabulates detector properties thoroughly but never assembles them into a
resolution calculation. Two standard quantities are required to do so, and
neither appears in the book.

### The Fano factor

**S&F never mention it.** Section 8.6.2 gives σ = √x for *counting* statistics,
which is correct for counting independent events, and the full-energy peak is
described as Gaussian "arising from the statistical fluctuations in the number of
free charge carriers" — but the variance of that carrier count is left as
Poisson by implication.

It is not Poisson. Carrier production is **sub-Poisson**, because the deposited
energy is fixed: a quantum spent creating one electron–hole pair is unavailable
to create another, so the events are anti-correlated and the variance is
suppressed to σ² = FN. Using √N instead of √(FN) overestimates a germanium
photopeak width by √(1/0.13) = 2.8 — it predicts 0.50% where detectors measure
~0.16%.

`FANO_FACTORS` carries the standard values (Ge 0.13, Si 0.115, gas ~0.20,
scintillators 1.0), and `test_the_fano_factor_matters_by_a_factor_of_three` pins
the size of the effect. Sources: Knoll, *Radiation Detection and Measurement*,
4th ed., §4.II.B; ICRU Report 31.

### Gas W-values

§8.1 describes ion-pair creation at length but tabulates no W-values, so the
resolution of a gas detector cannot be computed from the book alone.
`GAS_W_VALUES` carries the standard figures (air 33.97, Ar 26.4, He 41.3,
Xe 21.9, CH₄ 27.3, P-10 26.0 eV per ion pair) from ICRU Report 31.

Both additions are flagged in the source and in `notes.md` rather than being
folded in silently.

## A caution about the numbers this module produces

Everything computed here is a **lower bound from carrier statistics alone**.
Real detectors add electronic noise, incomplete or position-dependent charge
collection, and — for scintillators — light-yield non-proportionality and
non-uniform collection, all adding in quadrature.

The gap is small for germanium (1.2 keV floor against ~1.4 keV measured at 662
keV: the technology nearly attains its limit) and large for NaI(Tl) (3.6% floor
against ~6.5% measured: **more than half the observed width is not carrier
statistics**). `test_these_are_lower_bounds_not_predictions` asserts both
relations, so the module cannot be mistaken for a performance predictor.

## Cross-module dependencies
- **`~NE-16`** — the counting statistics behind √N, and the dead time that limits
  how fast these detectors can be read.
- **`~NE-12`** — the photopeak, Compton edge, backscatter and escape peaks that
  populate a spectrum; the Z⁴ that decides detector and wall material.
- **`~NE-14`** — ranges set window thicknesses and detector depths.
- **`~NE-13`** — ¹⁰B and ⁶Li in neutron detectors, for their 1/v cross sections
  and charged products.
- **`~NE-08`** — the elastic recoil fraction that makes hydrogen-rich organics
  the fast-neutron detector.

## Further reading
- Knoll, G.F., *Radiation Detection and Measurement*, 4th ed. (2010) — the
  standard reference, and the source for Fano factors and the resolution
  decomposition this module uses.
- ICRU Report 31, *Average Energy Required to Produce an Ion Pair* (1979) — the
  W-values.
- Birks, J.B., *The Theory and Practice of Scintillation Counting* (1964) — light
  yield, non-proportionality and Birks' law.
- Spieler, H., *Semiconductor Detector Systems* (2005) — noise, charge
  collection, and the electronics that set the rest of the resolution budget.
