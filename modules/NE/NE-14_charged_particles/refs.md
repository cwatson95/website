# NE-14 — References

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
| Attenuation of charged particles; why they matter | §7.5 | 205 | 228 |
| Interaction mechanisms; continuous Coulomb interaction | §7.5.1 | 205 | 228 |
| Definite range vs exponential attenuation | §7.5.1 | 205 | 228 |
| Bremsstrahlung introduced | §7.5.1 | 207 | 230 |
| Particle range; heavy charged particles travel straight | §7.5.2 | 207 | 230 |
| The 2.2 keV maximum transfer to one electron (from Eq. 6.22, `~NE-08`) | §7.5.2 | 207 | 230 |
| Straggling; the penetration-fraction curve | Fig. 7.12 | 208 | 231 |
| $R_p$ projected, $R_e$ extrapolated, **CSDA** range $R$ | §7.5.2 | 208 | 231 |
| Electrons: delta rays, tortuous paths | §7.5.2 | 208–209 | 231–232 |
| Electron track pictures (EGS4) | Figs. 7.13–7.14 | 209 | 232 |
| Stopping power defined | §7.5.3 | 209 | 232 |
| **Collisional stopping power** $\rho(Z/A)z^2f(I,\beta)$ | Eq. (7.41) | 210 | 233 |
| **The Bragg curve**; maximum at ~0.7 MeV for alphas in water | §7.5.3, Fig. 7.15 | 210–211 | 233–234 |
| **Radiative stopping power** $\propto(E+m_ec^2)Z^2F(E,Z)$ | Eq. (7.42) | 211 | 234 |
| Stopping power data for protons and electrons | Fig. 7.16 | 212 | 235 |
| **$(dE/ds)_{rad}/(dE/ds)_{coll}\simeq EZ/700\,(m_e/M)^2$** (`radiative_to_collisional`) | Eq. (7.43) | 212 | 235 |
| **Example 7.6** — the 8.9 MeV crossover in gold (`bremsstrahlung_crossover_energy`) | Example 7.6 | 212 | 235 |
| Estimating ranges; the CSDA integral | §7.5.4, Eq. (7.44) | 212–213 | 235–236 |
| CSDA ranges for protons and electrons | Fig. 7.17 | 213 | 236 |
| **Energy-deposition depth fractions** (`energy_deposition_depth_fraction`) | §7.5.4 | 213–214 | 236–237 |
| Mass-thickness range derivation | Eqs. (7.45)–(7.46) | 214 | 237 |
| **The three scaling rules** (`scaled_heavy_range`) | §7.5.4 | 214 | 237 |
| Rules fail below ~1 MeV per amu | §7.5.4 | 214 | 237 |
| **Empirical range formula** $\rho R=10^{a+bx+cx^2}$ (`csda_mass_range`) | Eq. (7.47) | 214 | 237 |
| **Table 7.2** — proton and alpha constants (`RANGE_CONSTANTS_PROTON/ALPHA`) | Table 7.2 | 215 | 238 |
| **Table 7.3** — electron constants (`RANGE_CONSTANTS_ELECTRON`) | Table 7.3 | 216 | 239 |
| **Example 7.7** — a 6 MeV triton by scaling | Example 7.7 | 216 | 239 |
| **Fission-fragment range** $\rho R=CE^{2/3}$ (`fission_fragment_range`) | Eq. (7.48) | 216 | 239 |
| Fission-fragment residual energy vs depth | Figs. 7.18–7.19 | 217 | 240 |

## Problems (verified, S&F 3rd ed. Ch. 7)
Problems **17–21** belong to this module; **1–13** are `~NE-11`, **12/14/15** are
`~NE-12` and **16** is `~NE-13`.

- **Prob. 17** — bremsstrahlung/collision ratio for 5 MeV electrons in air and lead — printed 220, PDF 243.
- **Prob. 18** — aluminium thickness to stop electrons, protons, alphas — printed 220, PDF 243.
- **Prob. 19** — range of a 10 MeV triton in air — printed 220, PDF 243.
- **Prob. 20** — Eq. (7.47) against Janni's proton data — printed 220, PDF 243.
- **Prob. 21** — median heavy fission fragment in air and gold — printed 220, PDF 243.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## Two problems in Table 7.2 and Example 7.7

### The proton/lead row is unusable, and is withheld

Table 7.2 prints, for **protons in lead**, $(a,b,c)=(0.065607,\,0.98751,\,0.0047353)$.
Three independent observations say this cannot be right:

1. **It does not belong to the family.** Every other proton row has
   $a\in[-2.61,-2.13]$, $b\in[1.38,1.51]$, $c\in[0.14,0.25]$. The lead row has
   $a=+0.066$, $b=0.988$, $c=0.0047$.
2. **It gives an absurd answer.** At 4 MeV the ten sound rows give 0.024–0.062
   g/cm²; the lead row gives **4.59 g/cm²** — 74× the largest, against an accepted
   PSTAR value near 0.065 g/cm².
3. **Its $b$ matches the lead *alpha* row's $b$ to 1 part in $10^4$**
   (0.98751 vs 0.98740). No other material pair does this, which points at
   contamination between adjacent rows during typesetting.

Offered as conjecture rather than fact: the printed $a$ of **0.065607** is
suspiciously close to the correct 4 MeV mass range of ~0.0656 g/cm², so a range
*value* may have been set into a constant column.

Because the correct constants cannot be recovered from the printed row,
`csda_mass_range("proton", "Pb", …)` **raises** rather than returning a number.
Inventing a replacement would be fabricating data. The printed values are kept in
`SUSPECT_RANGE_CONSTANTS` and `test_the_lead_proton_row_is_withheld` pins all
three observations.

### Example 7.7 uses the wrong row's $b$

Example 7.7 (printed 216) computes the 2 MeV proton range in **water** as
$$\rho R=10^{-2.6144+1.4501x+0.23219x^2}=0.00697\ \text{g/cm}^2,$$
but Table 7.2's H₂O proton row is $(-2.6144,\,\mathbf{1.4975},\,0.23219)$.
**1.4501 is the LiF row's $b$**, two lines below.

The table is right and the example is wrong:

| | $b$ | $\rho R$(2 MeV) | vs PSTAR's 7.178e-3 |
|---|---|---|---|
| Table 7.2 H₂O | 1.4975 | 7.202e-3 | **+0.3%** |
| Example 7.7 text | 1.4501 | 6.969e-3 | −2.9% |

The example's final answer for the triton range, 0.021 cm, is therefore ~3% low;
this module gets 0.0216 cm. `EXAMPLE_7_7_B_DISCREPANCY` records both and
`test_example_7_7_uses_the_wrong_b` checks that PSTAR picks the table.

## How accurate is Eq. (7.47), really?

S&F give the formula and its 0.1–10 MeV validity window but **no error
estimate**. Checked against the NIST STAR codes the fits were made from
(`test_ranges_match_the_NIST_star_codes`), the answer is a few percent in the
middle and considerably worse at the ends:

| | deviation from NIST |
|---|---|
| protons, H₂O, 1–10 MeV | −1.1% to +6.0% |
| electrons, water, 1–10 MeV | −0.4% to −3.6% |
| electrons, lead, 1 MeV | −7.4% |
| **protons, Al, 0.1 MeV** (the lower bound) | **−27.5%** |

The last is the book's own Problem 20, and it is the reason `csda_mass_range`
refuses to evaluate outside the window by default: if the fit is already 27% low
*at* the boundary, nothing it returns beyond the boundary means anything. An
explicit `strict=False` is available for callers who want the extrapolation
knowingly.

**A note on the test itself.** The first draft of
`test_ranges_match_the_NIST_star_codes` used the module-wide `_approx` helper,
which falls back to an *absolute* tolerance for values below 1 — so assertions on
quantities like 3.8e-3 g/cm² were passing for any candidate whatsoever. The test
now uses a strictly relative `_rel`, and additionally asserts that the worst
deviation *exceeds* 2%, so a future change that accidentally makes the comparison
vacuous again will fail rather than pass.

## Cross-module dependencies
- **`~NE-08`** — Eq. (6.22)'s 2.2 keV maximum transfer to one electron, the
  microscopic fact behind "thousands of interactions".
- **`~NE-12`** — the photoelectrons, Compton electrons and pairs whose subsequent
  fate this module describes; photons damage tissue only through them.
- **`~NE-09`** — fission fragments and their 168 MeV, deposited within microns.
- **`~NE-17`, `~NE-18`** — dose and its biological weighting; stopping power is
  LET under another name, and the Bragg peak is why $w_R(\alpha)=20$.
- **`~NE-05`** — beta endpoints, which set the energies that matter for §4.

## Further reading
- Berger, M.J., *ESTAR / PSTAR / ASTAR*, NIST — the codes S&F's Tables 7.2–7.3
  are fitted to, and the right source for any serious range calculation.
- ICRU Report 37, *Stopping Powers for Electrons and Positrons* (1984) — S&F's
  cited source for Eqs. (7.41)–(7.42).
- Janni, J.F., *At. Data Nucl. Data Tables* **27** (1982) 147 — the proton range
  tables of Problem 20.
- Evans, R.D., *The Atomic Nucleus* (1955), Ch. 18–22 — the Bethe formula in
  full, which S&F deliberately do not write out.
- Alexander & Gazdik, *Phys. Rev.* **120** (1960) 874 — the fission-fragment
  range fit of Eq. (7.48).
- Cross, Freedman & Wong, AECL-10521 (1992) — the beta depth-dose distributions
  behind the §7.5.4 deposition fractions.
