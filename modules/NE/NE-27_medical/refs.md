# NE-27 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |

Nuclear data cross-checks use the trunk's shared tables in
`modules/NE/data_tables/` (`D1_decay_radiation.csv`, `A4_isotopic_abundances.csv`),
extracted from the same book's Appendix D.

## Topic → location

| Topic (code symbol) | Section | Printed p. | PDF p. |
|---|---|---|---|
| **Table 14.1** — global use of medical radiology (1991–96) | Table 14.1 | 512 | 535 |
| Diagnostic imaging — overview | §14.1 | 513 | 536 |
| **X-ray projection imaging; the tube** (`xray_energy`) | §14.1.1 | 513–518 | 536–541 |
| **Table 14.2** — anode/filter characteristic lines (`ANODE_LINES`) | Table 14.2 | 515 | 538 |
| Fluoroscopy | §14.1.2 | 518 | 541 |
| **Mammography** — the Mo anode (`moseley_k_alpha`) | §14.1.3 | 519 | 542 |
| Bone densitometry (DXA) | §14.1.4 | 519–520 | 542–543 |
| **X-ray computed tomography** (`hounsfield_unit`) | §14.1.5 | 520–526 | 543–549 |
| Radon transform, Eq. (14.8) | §14.1.5 | 521 | 544 |
| **Hounsfield/Cormack Nobel** — *erratum*, see below (`CT_NOBEL`) | §14.1.5 | 521 | 544 |
| Fourier transforms, Eqs. (14.9)–(14.12); filtered backprojection | §14.1.5 | 521–523 | 544–546 |
| CT detector technology | §14.1.6 | 526 | 549 |
| **SPECT; the gamma camera** (`SPECT_TRACERS`) | §14.1.7 | 526–529 | 549–552 |
| Intrinsic resolution R_I = 2.5–4.5 mm; collimators | §14.1.7 | 528 | 551 |
| **Pinhole point-spread; Fig. 14.16** — *erratum* (`pinhole_resolution`) | §14.1.7 | 528 | 551 |
| **System resolution, Eq. (14.19)** (`spect_system_resolution`) | §14.1.7 | 528 | 551 |
| **Positron emission tomography** (`annihilation_photon_energy`) | §14.1.8 | 529–534 | 552–557 |
| **Table 14.3** — PET radionuclides (`PET_NUCLIDES`) | Table 14.3 | 530 | 553 |
| Coincidence timing window, 10–25 ns (`coincidence_window_length`) | §14.1.8 | 530–531 | 553–554 |
| Positron range; "only ¹⁸F … permit transport" (`usable_transport_time`) | §14.1.8 | 530–531 | 553–554 |
| **Table 14.4** — PET scanner comparison (Siemens ECAT) | Table 14.4 | 532 | 555 |
| Magnetic resonance imaging | §14.1.9 | 534–536 | 557–559 |
| Radioimmunoassay | §14.2 | 536–538 | 559–561 |
| Diagnostic radiotracers; ⁹⁹ᵐTc "most commonly used" | §14.3 | 538–539 | 561–562 |
| **Table 14.5** — tracers by process (no quantitative data) | Table 14.5 | 539 | 562 |
| Radioimmunoscintigraphy | §14.4 | 539–540 | 562–563 |
| **Radiation therapy** (`THERAPY_MODALITIES`) | §14.5 | 540–550 | 563–573 |
| "1.37 million new cases … 564 thousand deaths"; fractionation | §14.5 | 540 | 563 |
| **Table 14.6** — U.S. 2004 cases and deaths (`CANCER_2004`) | Table 14.6 | 541 | 564 |
| **Table 14.7** — lifetime cancer risk (`CANCER_LIFETIME_RISK`) | Table 14.7 | 541 | 564 |
| Early applications; early teletherapy; ⁶⁰Co | §§14.5.1–14.5.2 | 540–542 | 563–565 |
| Accelerator-based teletherapy | §14.5.3 | 542 | 565 |
| 3-D conformal radiation therapy (CRT) | §14.5.4 | 542–544 | 565–567 |
| Intensity-modulated radiation therapy (IMRT) | §14.5.5 | 544 | 567 |
| Electron beam therapy | §14.5.6 | 544–545 | 567–568 |
| **Proton beam therapy; the Bragg peak** (`~NE-14`) | §14.5.7 | 545–547 | 568–570 |
| Stereotactic radiation therapy (Gamma Knife) | §14.5.8 | 547 | 570 |
| **Clinical brachytherapy** (`brachytherapy_dose_rate`) | §14.5.9 | 547–549 | 570–572 |
| Radionuclide therapy (¹³¹I) | §14.5.10 | 549 | 572 |
| Boron neutron capture therapy | §14.5.11 | 549–550 | 572–573 |

## Errata — established, not asserted

**1. The CT Nobel year (§14.1.5, printed p. 521).** S&F: "Implementation of a
practical CT scanner dates from the efforts of Hounsfield and Cormack, working
independently, who shared the Nobel prize in 1972." The Nobel Prize in Physiology
or Medicine was awarded to Allan M. Cormack and Godfrey N. Hounsfield in **1979**,
"for the development of computer assisted tomography". 1972 is a real date in the
same story — Hounsfield's first published CT images and EMI's first clinical
scanner — so the sentence has collapsed the demonstration into the prize. This is
a fact check against nobelprize.org (2026-08-01), not a recomputation; it is
recorded as such. Pinned by `test_the_ct_nobel_year_is_wrong_in_the_book`.

**2. The pinhole point-spread (§14.1.7, printed p. 528).** Fig. 14.16's caption:
"The resolution R_ph of a pin-hole collimator is given by R_ph/(f + b) = d/b or
R_ph = (d/b)/(f + b)." Three observations settle it:

- **Dimensions.** (d/b)/(f+b) is length/length², i.e. 1/length. It cannot be a
  resolution. The caption's own first equality, R_ph/(f+b) = d/b, gives the
  *product* d(f+b)/b, so the printed slash is a typo for a multiplication.
- **Geometry.** A point source at distance b below an aperture of diameter d
  projects, by similar triangles, a spot of diameter d(b+f)/b at an image plane
  distance f above — so the product is right, **in the image plane**.
- **Consistency with Eq. (14.19).** The body text on the same page gives
  R_ph = (d/f)(f+b), which is the image-plane spot divided by the magnification
  M = f/b: the same blur referred to the **object** plane. Eq. (14.19),
  R_sys = √(R_ph² + (R_I/M)²), adds it to R_I/M, which is object-referred. Only
  the body's form makes the equation dimensionally and physically coherent.

So the body text is correct, the caption describes a different plane, and the
caption's division is a typesetting slip. `pinhole_resolution` implements the
body's form; `test_the_pinhole_caption_cannot_be_right_as_printed` asserts all
three statements against each other, including that the two forms differ by
exactly M and that the printed version is off by (f+b)².

## Verified correct — checks that could have failed and did not

| claim | check | result |
|---|---|---|
| **Table 14.2**, all 10 lines | E = hc/λ with hc = 12.39842 keV·Å | mean 5.7 × 10⁻⁵, worst 1.6 × 10⁻⁴ (Rh Kα₁) |
| **Table 14.2**, excitation voltages | must exceed every line they excite | holds for all 10 |
| **Table 14.3**, Ē/Emax | 0.402 / 0.410 / 0.424 / 0.394 | all ≈ 0.40, the β⁺ signature |
| **Table 14.3** vs Appendix D | re-read from `D1_decay_radiation.csv` | Emax, Ē, branch all < 0.5% |
| annihilation yield | 511 keV frequency vs positron branch | **exactly 2×** for all four |
| **Table 14.6** | column sums vs printed totals | **exact**, all four columns |
| Table 14.6 → text | "1.37 million"; "564 thousand" | 1,368,030; 563,700 |
| **Table 14.7** → "nearly half" | male lifetime incidence | 46.6% (female 38.0%) |
| Table 14.7 → "about half survive" | mortality / incidence | 49% M, 48% F die |

## Relations the chapter needs and omits

| relation | why it is needed | where it is |
|---|---|---|
| **HU = 1000(µ − µ_w)/µ_w** | §14.1.5 develops the reconstruction but never states the unit the image is displayed in; two fixed points are what make CT numbers portable | `hounsfield_unit` |
| **E_Kα ≈ 10.2 eV (Z−1)²** | makes the mammography/radiography anode choice a consequence of Z rather than a convention | `moseley_k_alpha` |
| **t(10%) = T₁/₂ log₂10** | turns "only ¹⁸F … permits transport" into 6.1 h vs 6.8 min, a factor of 54 | `usable_transport_time` |
| **R ≈ 4 mm × Ē^1.5** | scales S&F's own 1 MeV → 4 mm into a per-nuclide resolution floor | `positron_range_mm` |
| **cτ/2** | converts the stated 10–25 ns window into 150–375 cm, showing timing cannot localise | `coincidence_window_length` |

## A note on the SPECT data

`SPECT_TRACERS` is **not** from Chapter 14. Table 14.5 (p. 539) lists process →
tracer and gives no energies or half-lives; §14.1.7 (p. 527) names ⁹⁹ᵐTc, ¹²⁵I and
¹³¹I in prose only. The principal imaging gamma and half-life for each tracer come
from `modules/NE/data_tables/D1_decay_radiation.csv` and
`A4_isotopic_abundances.csv`. This is flagged in the source and in
`test_spect_tracers_and_the_99mtc_dominance` so the numbers are never mistaken
for the chapter's.

## Beyond the book

- **Time-of-flight PET.** S&F's 10–25 ns window gives 150–375 cm. Scanners at
  ~400 ps reach 6 cm, finally shorter than a patient. It improves signal-to-noise
  rather than spatial resolution, and is noted as post-book in the source.
- The tissue CT numbers in `figures/fig2_hounsfield_scale.svg` are
  representative clinical values, not S&F's; the caption says so, and the µ(HU)
  curve beside them is exact.
