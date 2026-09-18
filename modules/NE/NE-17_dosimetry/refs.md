# NE-17 — References

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
| Historical roots; ICRP, NCRP, EPA, NRC | §9.1 | 270–272 | 293–295 |
| Dosimetric quantities; why fluence is not enough | §9.2 | 272–273 | 295–296 |
| Energy imparted to the medium | §9.2.1 | 273 | 296 |
| **Absorbed dose**; the gray, the rad | Eq. (9.1), §9.2.2 | 274 | 297 |
| **Kerma**; charged-particle equilibrium (`kerma`) | Eq. (9.2), §9.2.3 | 274 | 297 |
| Calculating kerma and dose | §9.2.4 | 274–277 | 297–300 |
| **K = 1.602e−10 E (μ_tr/ρ) Φ** (`kerma`) | Eq. (9.5) | 275 | 298 |
| **D = 1.602e−10 E (μ_en/ρ) Φ** (`absorbed_dose`) | Eq. (9.6) | 275 | 298 |
| **Example 9.1** — iron kerma & dose from a 5-MeV source in water | Ex. 9.1 | 276 | 299 |
| **f_s = 2A/(A+1)²** (`neutron_recoil_fraction`) | Eq. (9.7) | 276 | 299 |
| **Fast-neutron kerma** (`neutron_kerma`) | Eq. (9.8) | 276 | 299 |
| **Example 9.2** — water kerma rate from 0.1-MeV neutrons | Ex. 9.2 | 277 | 300 |
| **Exposure**; the roentgen; W = 33.85 eV/ion pair | §9.2.5 | 277–278 | 300–301 |
| **X = 1.835e−8 E (μ_en/ρ)_air Φ** (`exposure`) | Eq. (9.9) | 278 | 301 |
| Relative biological effectiveness (RBE) | §9.2.6 | 278–279 | 301–302 |
| **H = QF × D** (`dose_equivalent`); the sievert, the rem | Eq. (9.10), §9.2.7 | 279 | 302 |
| **Table 9.1** — quality factors (`QUALITY_FACTORS`) | Table 9.1 | 279 | 302 |
| Quality factor; U.S. federal values differ for neutrons | §9.2.8 | 279–280 | 302–303 |
| **Example 9.3** — dose equivalent 15 m from a 1-MeV source | Ex. 9.3 | 280 | 303 |
| **Effective dose equivalent** (`effective_dose`) | Eq. (9.11), §9.2.9 | 280 | 303 |
| **Table 9.2** — ICRP [1977] weights (`ICRP77_TISSUE_WEIGHTS`) | Table 9.2 | 281 | 304 |
| **Example 9.4** — HE from natural internal emitters | Ex. 9.4 | 281 | 304 |
| **Effective dose** E = Σ w_T Σ w_R D_{T,R} | Eq. (9.12), §9.2.10 | 281 | 304 |
| **Table 9.3** — ICRP [1991] weights (`ICRP90_TISSUE_WEIGHTS`) | Table 9.3 | 282 | 305 |
| Doses from ingested radionuclides; MIRD vs ICRP | §9.3 | 282–283 | 305–306 |
| Committed dose equivalent; the 50-year cutoff η | §9.3.1 | 283 | 306 |
| The general method; Reference Man | §9.3.2 | 283–284 | 306–307 |
| The ICRP compartment model; f₁, f₂, λ_b | §9.3.3, Fig. 9.1 | 284–285 | 307–308 |
| **Example 9.5** — ingesting 1 mCi ⁵⁹Fe and 50 μCi ⁶⁰Co | Ex. 9.5 | 285 | 308 |
| **Table 9.4** — ingestion dose coefficients (`INGESTION_DOSE_COEFFICIENTS`) | Table 9.4 | 286 | 309 |
| Natural exposures; cosmic, cosmogenic, ⁴⁰K, ⁸⁷Rb, radon | §9.4 | 285–288 | 308–311 |
| **Table 9.5** — world background, 2.4 mSv/y (`NATURAL_BACKGROUND_WORLD`) | Table 9.5 | 287 | 310 |
| **Table 9.6** — U.S. background, 3.0 mSv/y (`NATURAL_BACKGROUND_US`) | Table 9.6 | 288 | 311 |
| U.S. man-made component, 0.65 mSv/y (`US_MANMADE_BREAKDOWN`) | §9.4 | 288 | 311 |

## Problems (verified, S&F 3rd ed. Ch. 9)
Chapter 9's problems begin on printed **318** (PDF 341). Problems **1–6** belong
to this module; **7–20** are health effects, radon and protection standards and
are worked in `~NE-18`.

- **Prob. 1** — tritium in air; the air-kerma rate — printed 318, PDF 341.
- **Prob. 2–3** — a ¹³⁷Cs point source in air and in water — printed 318, PDF 341.
- **Prob. 4–5** — ¹⁶N and ⁴³K dose rates in air and in iron — printed 318, PDF 341.
- **Prob. 6** — the 6CEN/r² rule of thumb — printed 319, PDF 342.

## Four printed results this module corrects

The pattern is the one this trunk keeps finding: a printed number contradicted by
the book's own adjacent numbers. Each is kept in a `*_ERRATA`-style constant and
pinned by a test.

### Example 9.3 — a factor of 100 (printed p. 280)
The example computes a fluence of $2.122\times10^4$ cm⁻² and then writes
$$H=(1)(1.602\times10^{-10})(1)(0.03103)(2.122\times10^4)=10.5\ \mu\text{Sv}.$$
That product is $1.055\times10^{-7}$ Sv = **0.105 µSv**. The inputs are not in
doubt: 0.03103 cm²/g is Appendix C.3's μ_en/ρ for water at 1 MeV, and
$2.122\times10^4$ is the example's own preceding line. For what it is worth,
10.5 µSv *is* the right answer at $r=1.5$ m — a lost factor of ten in the
distance, squared. *Verified: `test_example_9_3_is_wrong_by_a_factor_of_one_hundred`.*

A **second, independent** slip sits in the same example: the text says the source
emitted "for 5 minutes" while the fluence line uses 600 s. The fluence line is
internally consistent (it shows $4\pi(1500\ \text{cm})^2$ and gets
$2.122\times10^4$), so the prose is the half that is wrong.

### Example 9.5 — the right number in the wrong unit (printed p. 285)
Ingesting 1 mCi ⁵⁹Fe and 50 µCi ⁶⁰Co. Table 9.4 gives 6.6×10³ and 1.0×10⁴ rem/Ci,
so the committed effective dose equivalent is
$$(10^{-3})(6.6\times10^3)+(5\times10^{-5})(1.0\times10^4)=6.6+0.5=7.1\ \textbf{rem},$$
and the example prints "7.1 **mrem**". Three things went wrong in one line: the
⁵⁹Fe coefficient is printed as 6.6 rather than 6.6×10³ rem/Ci, the ⁶⁰Co intake as
10⁻⁶ rather than 5×10⁻⁵ Ci, and the answer's prefix as milli. What makes it
unambiguous rather than arguable is that **the printed intermediates do not
reproduce the printed answer** — they give 16.6 mrem.

It matters. 7.1 rem is 71 mSv: thirty times a year's natural background and a
reportable overexposure. 7.1 mrem is a transatlantic flight. *Verified:
`test_example_9_5_number_is_right_and_the_unit_is_not`.*

### Problem 9.1 — tritium's beta energy is in keV (printed p. 318)
The problem gives ³H's average beta energy as "5.37 **MeV**". Tritium's entire
decay energy is 18.6 keV, so no tritium beta can carry 5.37 MeV, and the book's
own **Appendix D lists 5.67 keV/decay**. The authors' solution manual restates
the problem with "keV" — and then substitutes MeV in the arithmetic anyway,
finally reporting $2.196\times10^{-7}$ Gy/h as "22.0 µGy/h", which is 0.2196
µGy/h. The correct answer from Appendix D is **0.232 nGy/h**. *Verified:
`test_problem_9_1_tritium_average_beta_energy_is_keV_not_MeV`.*

### Solution manual, Problem 9.4(a) — proved wrong by Problem 9.5(a)
The ¹⁶N table lists $f E (\mu_{en}/\rho)=0.08931$ for the 6.129 MeV line, but
$0.690\times6.129\times0.01639=0.06931$. The **same product** appears one problem
later multiplied by $e^{-2.403}$, where it is printed as 0.006269 — and
$0.006269/e^{-2.403}=0.06931$. So 0.08931 is a 6 transcribed as an 8, and
Problem 4(a)'s answer is **1.27 mGy/h**, not 1.611. *Verified:
`test_reproduces_problems_4_and_5_and_finds_the_typo_between_them`.*

The same test records a smaller, separate discrepancy: for ⁴³K's 617.5 keV line
the solution manual uses $(\mu_{en}/\rho)_{\rm air}=0.02880$ and
$\mu^{\rm Fe}=0.5174$ cm⁻¹, which are the table's **0.8 MeV** row, not the
interpolation to 0.6175 MeV (0.02947 and 0.5905). Every one of the other eleven
coefficients in those two tables is reproduced exactly from the extracted
Appendix C.3, which is what isolates this one as a row-lookup slip. It costs 1.2%
in air and a factor of 1.73 in iron, where it sits inside an exponential.

**A forensic aside that explains a third oddity.** The solution manual's
Problem 2 solves 900 µCi at 2.5 m while the textbook states 700 µCi at 2 m, and
part (a) of the solution carries a stray flux of 43.54 cm⁻²s⁻¹ that matches
neither its own header (35.83) nor its own answer. 43.54 is *exactly* the flux
for 700 µCi at 2 m — the textbook's version. The problem was renumbered between
editions and one line was left behind. Documented, not corrected.

## Three things this module adds

### The roentgen-to-gray conversion
S&F define absorbed dose (§9.2.2) and exposure (§9.2.5) in adjacent sections and
never connect them, yet every survey meter reads in mR/h and every dose limit is
written in mSv. The connection is forced by the two definitions:
$1\ \mathrm{R}=(2.58\times10^{-4}\ \mathrm{C/kg})(33.85\ \mathrm{J/C})=8.73$ mGy
in air, which is also the ratio of the Eq. (9.6) and Eq. (9.9) prefactors.
`roentgen_to_air_dose`.

### ICRP Publication 103 (2007)
The book stops at the 1991 weighting factors. The set in current regulatory use
is ICRP-103, and the *direction of travel* is the point: the gonad weight fell
0.25 → 0.20 → 0.08 as the hereditary-risk estimate came down (`~NE-18` §2), while
breast rose to 0.12. `ICRP07_TISSUE_WEIGHTS`, with a test that all three sets sum
to one.

### Where the fast-neutron formula stops
Eq. (9.8) is elastic scattering only. S&F note in one sentence that slow-neutron
kerma "is more difficult" and leave it; the reason is that thermal kerma in tissue
is dominated by ¹⁴N(n,p)¹⁴C and ¹H(n,γ)²H, i.e. by capture rather than recoil.
`neutron_kerma`'s docstring says so rather than letting the formula be
extrapolated into a regime where it is simply the wrong physics.

## Two places the module refuses rather than answering

**An unrecognised radiation.** `quality_factor` raises instead of returning 1.
QF spans a factor of twenty, so 1 is not a safe default — it is a twentyfold
understatement for fast neutrons and alphas, in the direction that says an
exposure was harmless.

**An organ with no tissue weighting factor.** `effective_dose` raises rather than
dropping the term. A dropped organ still yields a plausible-looking effective
dose, and it is always too *low*. The two ICRP vintages even spell the same organ
differently ("red marrow" in 1977, "bone marrow" in 1991), so mixing a dose list
with the wrong weight set is an easy mistake that would otherwise silently discard
12% of the answer.

## Interpolating Appendix C.3
S&F's solutions say "linearly interpolating between tabulated values", and
reproducing the book's numbers requires exactly that. `~NE-11` and `~NE-12` use
**log-log**, which is the better choice because the coefficients are close to
power laws between grid points. The two agree to 0.08% on μ_en — irrelevant for
dose — and differ by 0.6% on the total μ, which becomes 2% in a flux after 40 cm
of water. `mass_coefficient` offers both and defaults to log-log;
`test_linear_vs_loglog_interpolation` measures the gap rather than asserting one
is right.

## Cross-module dependencies
- **`~NE-11`, `~NE-12`** — fluence, and the μ_tr/μ_en distinction this module
  spends; the same Appendix C.3 tables.
- **`~NE-13`** — Eq. (6.28)'s elastic-scattering mean energy loss, reused here as
  Eq. (9.7).
- **`~NE-16`** — every measured dose is a count with propagated error.
- **`~NE-18`** — takes effective dose and returns a probability of harm.
- **`~NE-26`, `~NE-27`** — applications where these quantities are the design
  variables.

## Further reading
- Attix, F.H., *Introduction to Radiological Physics and Radiation Dosimetry* —
  the standard treatment; Ch. 2–3 make the kerma/dose distinction properly,
  including the cavity theory this module does not touch.
- ICRP Publication 103 (2007), *Ann. ICRP* **37** (2–4) — the current weighting
  factors and the reasoning behind the changes.
- ICRU Report 85, *Fundamental Quantities and Units for Ionizing Radiation* — the
  authoritative definitions, and the source of the vocabulary S&F use.
- NCRP Report 160, *Ionizing Radiation Exposure of the Population of the United
  States* (2009) — the modern successor to Table 9.6; medical exposure has since
  risen to roughly half the U.S. total, which changes the picture in §9.4
  materially.
