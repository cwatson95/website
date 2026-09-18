# NE-12 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |
| Shultis & Faw, *Problem Solution Manual*, 3rd ed. (2016) | `NE_Nuclear_Engineering/nuclear_science_sol_shultis_faw.pdf` | indexed by chapter/problem |

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Photon interactions; the three significant mechanisms | §7.3 | 191 | 214 |
| Photoelectric effect; $E_e=E-E_b$ (`photoelectron_energy`) | §7.3.1 | 192 | 215 |
| K-shell binding energies: H 13.6 eV, Fe 7.11 keV, Pb 88 keV, U 116 keV (`K_EDGE_KEV`) | §7.3.1 | 192 | 215 |
| Absorption edges; $n\simeq3$ below 150 keV, $n\simeq1$ above 5 MeV; $m$ = 4–4.6 | §7.3.1 | 192 | 215 |
| **$\sigma_{ph}\propto Z^4/E^3$** (`photoelectric_scaling`) | Eq. (7.32) | 192 | 215 |
| 1.25× the K-shell cross section for heavy nuclei | §7.3.1 | 192 | 215 |
| Fluorescence x-rays, Auger electrons, fluorescent yield 0.005 → 0.965 (`FLUORESCENT_YIELD`) | §7.3.1 + fn. 3 | 192 | 215 |
| Compton scattering; relativistic kinematics | §7.3.2 | 192–193 | 215–216 |
| **$E'=E/[1+(E/m_ec^2)(1-\cos\theta_s)]$** (`compton_scattered_energy`) | Eq. (7.33), from (2.30) | 193 | 216 |
| **Klein–Nishina cross section** (`klein_nishina_per_electron`) | Eq. (7.34) | 193 | 216 |
| Classical electron radius $r_e=2.8179\times10^{-13}$ cm (`R_E_CM`) | Eq. (7.35) | 193 | 216 |
| Bound-electron incoherent scattering; where the free-electron model fails | §7.3.2 | 193 | 216 |
| Coherent (Rayleigh) scattering; 75% within 4° for 1 MeV on iron | §7.3.2 | 193–194 | 216–217 |
| Comparison of all cross sections in lead | Fig. 7.3 | 194 | 217 |
| Pair production; threshold $2m_ec^2$, triplet $4m_ec^2$ (`pair_production_threshold`) | §7.3.3 | 194 | 217 |
| **$E_++E_-=E_\gamma-2m_ec^2$** (`pair_kinetic_energy_shared`) | Eq. (7.36) | 194–195 | 217–218 |
| $\sigma_{pp}\propto Z^2$; emission angles $\simeq m_ec^2/E_\gamma$ | §7.3.3 | 195 | 218 |
| Annihilation into two $m_ec^2$ photons (`annihilation_photon_energy`) | §7.3.3 | 195 | 218 |
| Photon attenuation coefficients | §7.3.4 | 195 | 218 |
| **$\mu=N[\sigma_{ph}+\sigma_{inc}+\sigma_{pp}]$**, Rayleigh excluded | Eq. (7.37) | 195 | 218 |
| **$\mu/\rho=\mu_{ph}/\rho+\mu_c/\rho+\mu_{pp}/\rho$** (`dominant_process`) | Eq. (7.38) | 195 | 218 |
| Total mass coefficients for four shielding materials | Fig. 7.4 | 196 | 219 |
| Correction for secondary radiation; **$\mu_{en}\simeq\mu f$** (`energy_transfer_fraction`) | Eq. (7.39) | 195–196 | 218–219 |
| Relation among $\mu_a$, $\mu_{tr}$, $\mu_{tr}^0$, $\mu_{en}$ | Fig. 7.5 | 196 | 219 |
| Photon mass coefficients (`load_photon_coefficients`) | Table C.3 | 591–595 | 614–618 |

## Problems (verified, S&F 3rd ed. Ch. 7)
Chapter 7's problem set begins on printed **218** (PDF 241). Problems **12, 14
and 15** are worked here; **1–11 and 13** are `~NE-11`, **16** is `~NE-13` and
**17–21** are `~NE-14`.

- **Prob. 12** — interactions and positrons from 3 MeV photons in water — printed 219, PDF 242.
- **Prob. 14** — a 2 mCi ⁶⁰Co source in a water-filled iron tank — printed 219, PDF 242.
- **Prob. 15** — maximum Compton electron and minimum scattered photon at 0.1, 1 and 10 MeV — printed 219, PDF 242.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## A data-extraction bug found while building this module

The Appendix C.3 tables were extracted in an earlier commit on this branch. **The
lead table was missing its K edge**, along with the entire 0.05–0.15 MeV decade
and all five M edges; water, concrete and iron were each missing 3–4 rows.

Two parser bugs, both in `data_tables/_extract.py`:

- the coefficient token regex required an explicit exponent, but Appendix C
  prints values of order unity with none (lead's photoelectric column reads
  `7.291`, not `7.291+0`), so any row containing such a value was skipped;
- the edge-suffix pattern was `(K|L1|L2|L3|M)`, and lead's M edges are `M1..M5`,
  so the trailing digit broke the match.

Both are fixed, the extractor's validators now require every printed edge to
survive parsing, and the row counts rose (lead 52 → 64). This matters for
NE-12 specifically because the K edge is the single sharpest feature in the
photon data and the module is largely about it. It also changed some NE-11
interpolated values slightly; all 250 tests pass against the corrected tables.

The general lesson, and the reason the fix was found at all: the module's tests
compare the tabulated data against an *independent analytic formula*
(Klein–Nishina). A missing row is invisible to a row-count check and obvious to a
physics check.

## A composition constant taken from the book rather than from NIST

`MATERIALS["concrete"]["z_over_a"] = 0.50150`, **not** NIST's 0.50932 for
"ordinary concrete". S&F's Appendix C.3 table is captioned *"ANSI/ANS-6.4.3
standard concrete"*, a different specified composition (the caption lists it:
H 0.005599, O 0.498250, Si 0.315768, Ca 0.082592, …).

Using the NIST value leaves a **1.5% offset in the Compton coefficient that is
constant with energy** — the signature of a composition error rather than a
physics one, since bound-electron effects vanish at high energy. Solving the
tabulated Compton column for $Z/A$ at 3 and 10 MeV, where the free-electron
formula is exact to 0.3%, gives 0.5013 and 0.5019. The adopted 0.5015 is the
book's own value, recovered from its own data.
`test_z_over_a_is_recoverable_from_the_tables` re-derives all five materials and
explicitly pins concrete *against* the NIST figure, which is kept in
`Z_OVER_A_NIST_ORDINARY_CONCRETE` so the distinction is not lost.

## Two conventions worth stating

**Coherent scattering is deliberately excluded from the total.** S&F define
$\mu$ by Eq. (7.37) as photoelectric + incoherent + pair, noting that "Rayleigh
coherent scattering and other minor effects are specifically excluded". The
justification [§7.3.2] is that coherent scattering barely changes photon energy
or direction, and that where it is large (low energy, high $Z$) the photoelectric
effect dominates anyway. `test_components_sum_to_the_total` checks that the three
tabulated components do sum to the tabulated total, confirming the convention
holds in the data.

**Edge energies appear twice in the tables.** Each absorption edge is listed at
the same energy with the shell closed and open. `mass_coefficient` returns the
**lower, below-edge** branch when asked for exactly the edge energy, takes the
upper branch just above, and never uses the duplicated pair as an interpolation
bracket (it raises rather than dividing by zero). Documented in the function and
checked by `test_edge_energies_return_the_below_edge_branch`.

## Cross-module dependencies
- **`~NE-11`** — the $\mu$ this module decomposes, and the flux/reaction-rate
  machinery the problems use.
- **`~NE-08`** — the inverse-mass energy split, which is why the recoiling atom
  in a photoelectric event takes no energy.
- **`~NE-05`** — positron annihilation and the 511 keV line; ⁶⁰Co's two gammas.
- **`~NE-02`** — why lead's $Z/A$ is the lowest of the five materials (heavy
  nuclei are neutron-rich).
- **`../data_tables/`** — `C3_photon_coefficients_*.csv`.

## Further reading
- Evans, R.D., *The Atomic Nucleus* (1955), Ch. 23–25 — S&F's cited source for
  Klein–Nishina; still the most complete elementary derivation.
- Hubbell, J.H., *Photon Cross Sections, Attenuation Coefficients and Energy
  Absorption Coefficients*, NSRDS-NBS 29 (1969) — S&F's cited source for the
  coherent-scattering angular data.
- Cullen, D.E. et al., *EPDL/EPIC* data library (1994) — the source of S&F's
  Fig. 7.3.
- Berger & Hubbell, *XCOM*, NIST — the modern successor to Appendix C.3, with
  arbitrary compositions and energies.
- Knoll, G.F., *Radiation Detection and Measurement*, Ch. 2 and 10 — the same
  three processes read as the features of a pulse-height spectrum (`~NE-15`).
