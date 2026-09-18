# NE-07 — References

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
| Decay dynamics; decay with production | §5.6.1 | 117 | 140 |
| $dN/dt = -\lambda N + Q(t)$ | Eqs. (5.50)–(5.51) | 117 | 140 |
| General solution with an arbitrary source | Eq. (5.52) | 118 | 141 |
| **Constant production** $N(t)=N_oe^{-\lambda t}+(Q_o/\lambda)(1-e^{-\lambda t})$ (`decay_with_production`) | Eq. (5.53) | 118 | 141 |
| Equilibrium value $N_e=Q_o/\lambda$ (`equilibrium_number`, `approach_fraction`) | §5.6.1 | 118 | 141 |
| Three-component decay chains (`two_component_chain`, `daughter_maximum_time`) | §5.6.2 | 118–122 | 141–145 |
| **General decay chain**, the coupled ODE system | Eq. (5.68) | 122 | 145 |
| **Bateman solution** $A_j(t)=N_1(0)\sum_m C_me^{-\lambda_mt}$ (`bateman_activity`) | Eq. (5.69) | 122 | 145 |
| Bateman coefficients $C_m$ (`bateman_coefficients`) | Eq. (5.70) | 123 | 146 |
| Naturally occurring radionuclides; cosmogenic and primordial | §§5.7–5.7.2 | 123–124 | 146–147 |
| Decay series of primordial origin — the four series (`series_of`, `NATURAL_SERIES`) | §5.7.3 | 124 | 147 |
| **Secular equilibrium** (`is_secular`, `secular_equilibrium_activities`) | §5.7.4 | 125 | 148 |
| $\lambda_1N_1=\lambda_2N_2=\cdots$ | Eq. (5.71) | 125 | 148 |
| $A_o=A_1=A_2=\cdots=A_{n-1}$ | Eq. (5.72) | 125 | 148 |
| Radiodating overview | §5.8 | 128 | 151 |
| Dating by the surviving parent (`age_from_parent_fraction`, `carbon14_age`) | §5.8.1 | 128–129 | 151–152 |
| Dating by the accumulated stable daughter (`age_from_daughter_ratio`) | §5.8.2 | 129–131 | 152–154 |
| Radioactive decay data — the source of Appendix D | §5.9 | 131 | 154 |
| Half-lives and abundances (`load_half_lives`) | Table A.4 | 562–569 | 585–592 |

## Problems (verified, S&F 3rd ed. Ch. 5)
Chapter 5's problem set begins on printed **132** (PDF 155). The chain,
equilibrium and dating problems run from **16** onward:

- **Prob. 18** — 6.2 mg of $^{90}$Sr in secular equilibrium with $^{90}$Y — printed 134, PDF 157.
- **Prob. 19** — a sample holding 1.0 GBq $^{90}$Sr and 0.62 GBq $^{90}$Y — printed 134, PDF 157.
- **Probs. 20–21** — the three-component chain of §5.6.2 — printed 134, PDF 157.
- **Prob. 22** — a $\beta^-$ chain with given half-lives — printed 134, PDF 157.
- **Prob. 23** — an encapsulated 40 mg $^{226}$Ra sample — printed 134, PDF 157.
- **Prob. 25** — the global $^{14}$C inventory of 8.5 EBq — printed 135, PDF 158.
- **Prob. 26** — $^{40}$K activity from the 140 g of potassium in the body — printed 135, PDF 158.
- **Prob. 28** — dating charcoal with a $^{14}$C activity of 1.8 dpm/g — printed 135, PDF 158.
- **Probs. 30–31** — $^{238}$Pu as a thermal power source; $^{90}$Sr/$^{90}$Y in equilibrium — printed 135, PDF 158.

Problems 1–7 concern decay energetics (`~NE-05`) and 8–15 concern single-nuclide
kinetics (`~NE-06`).

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## A caution the book does not spell out

**Daughter-ratio dating needs the branching fraction.** S&F §5.8.2 derives
$t=(1/\lambda)\ln(1+N_D/N_P)$ for a parent decaying to a stable daughter. That is
exact for $^{238}$U $\to$ $^{206}$Pb, where every decay eventually reaches lead.
It is **wrong** for K/Ar dating, because only 10.72% of $^{40}$K decays give
$^{40}$Ar and the other 89.28% give $^{40}$Ca (`~NE-05`). The argon accumulates as
$f N_P(e^{\lambda t}-1)$, so the ratio must be divided by $f$ before taking the
logarithm; omitting it makes a rock look 3.4 times younger.
`age_from_daughter_ratio` takes a `branch_fraction` argument for this, defaulting
to 1.0, and `test_potassium_argon_needs_the_branching_correction` pins the factor.

## Cross-module dependencies
- **`~NE-06`** — single-nuclide kinetics; this module adds the source term.
- **`~NE-05`** — decay modes and branching ratios, needed for the K/Ar correction.
- **`~MA-11`** — coupled linear ODE systems; the Bateman equations are the
  canonical triangular example.
- **`../data_tables/`** — `A4_isotopic_abundances.csv` for all half-lives.

## Further reading
- Bateman, H., *Proc. Cambridge Phil. Soc.* **15** (1910) 423 — the original
  solution of the chain equations.
- Krane, *Introductory Nuclear Physics*, §6.4 — chains and equilibria, with the
  degenerate (equal decay constant) case worked out.
- Faure, *Principles of Isotope Geology* — the dating methods of §5 in full,
  including isochron techniques that remove the no-initial-daughter assumption.
