# NE-06 — References

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
| Characteristics of radioactive decay | §5.5 | 111 | 134 |
| Definition of the decay constant $\lambda$ | Eq. (5.32) | 112 | 135 |
| $dN/dt=-\lambda N$ | Eq. (5.33) | 113 | 136 |
| **Exponential decay** $N(t)=N_oe^{-\lambda t}$ (`number_remaining`) | Eq. (5.34) | 113 | 136 |
| Half-life definition and $T_{1/2}=\ln2/\lambda$ (`decay_constant`, `half_life`) | Eqs. (5.35)–(5.36) | 113 | 136 |
| Number of half-lives $n=-1.44\ln(N/N_o)$ (`half_lives_elapsed`) | Eq. (5.38) | 114 | 137 |
| $N(t)=N_o(1/2)^{t/T_{1/2}}$ | Eq. (5.39) | 114 | 137 |
| Survival probability $e^{-\lambda t}$ (`survival_probability`) | Eq. (5.40) | 114 | 137 |
| Decay probability in a finite interval (`decay_probability`) | Eqs. (5.41)–(5.42) | 114 | 137 |
| Decay-time density $p(t)=\lambda e^{-\lambda t}$ (`decay_time_pdf`) | Eq. (5.43) | 114 | 137 |
| **Mean lifetime** $T_{av}=1/\lambda$ (`mean_lifetime`) | Eq. (5.44) | 114 | 137 |
| **Activity** $A(t)=\lambda N(t)=A_oe^{-\lambda t}$ (`activity`, `activity_at_time`) | Eq. (5.45) | 115 | 138 |
| Half-life measurement from a decay curve | §5.5.7 | 115 | 138 |
| Decay by competing processes; rates add (`total_decay_constant`) | Eqs. (5.47)–(5.48) | 116 | 139 |
| Branching fractions $f_i=\lambda_i/\lambda$ (`branching_fractions`) | Eq. (5.49) | 116 | 139 |
| Physical constants ($N_A$) | Table A.1 | 555 | 578 |
| Half-lives of 918 nuclides (`load_half_lives`, `parse_half_life`) | Table A.4 | 562–569 | 585–592 |

## Problems (verified, S&F 3rd ed. Ch. 5)
Chapter 5's problem set begins on printed **132** (PDF 155). The kinetics
problems run from **8** onward, on printed 133–134 (PDF 156–157):

- **Prob. 8** — decay constant and mean lifetime of $^{40}$K (half-life 1.29 Gy) — printed 133, PDF 156.
- **Prob. 9** — decay constants from the level diagram of Fig. 5.12 — printed 133, PDF 156.
- **Prob. 10** — half-life from an activity that falls 30% in one week — printed 133, PDF 156.
- **Prob. 11** — $^{132}$I ($\beta^-$ to $^{132}$Xe, 2.3 h) — printed 133, PDF 156.
- **Prob. 12** — mass of $^{32}$P in a 5 mCi source — printed 133, PDF 156.
- **Prob. 13** — number of atoms in a 1.20 MBq source of $^{24}$Na and of $^{238}$U — printed 133, PDF 156.
- **Prob. 14** — a specimen holding $10^{12}$ atoms of $^{14}$C — printed 133, PDF 156.
- **Prob. 15** — half-life from a table of count-rate data — printed 133–134, PDF 156–157.

Problems 1–7 concern decay energetics and belong to `~NE-05`; problems from 16
onward concern chains, equilibrium and dating and belong to `~NE-07`.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## A note on the curie

The curie is now **defined** as exactly $3.7\times10^{10}$ Bq. Historically it
was intended to be the activity of one gram of $^{226}$Ra. Computing that from
the half-life tabulated in Appendix A.4 gives $3.658\times10^{10}$ Bq/g, i.e.
**0.9886 Ci/g** rather than 1.0000. The 1.1% shortfall is not an error in either
the code or the table: the curie was fixed by convention before radium's
half-life was revised to its present 1600 y value.
`test_one_gram_of_radium_is_about_one_curie` asserts the modern number.

## A note on the year

Half-lives in Appendix A.4 are printed in years with SI prefixes (ky, My, Gy,
Ty, Py, Ey). `SECONDS_PER["y"]` uses the **Julian year**, 365.25 days
$=3.15576\times10^{7}$ s. The tropical year differs by about 0.003%, which is
far below the precision of any tabulated half-life but worth stating, since
half-life comparisons across texts occasionally differ in the last digit for
exactly this reason.

## Cross-module dependencies
- **`~NE-05`** — which decay mode, and how much energy; this module supplies the rate.
- **`~ST-11`** — the exponential distribution; `decay_time_pdf` *is* that density.
- **`~ST-09`** — decays are a Poisson process, which is what makes `~NE-16`'s
  counting statistics work.
- **`../data_tables/`** — `A4_isotopic_abundances.csv` supplies every half-life used here.

## Further reading
- Krane, *Introductory Nuclear Physics*, §6.3 — the same material with the
  statistical derivation of the exponential law spelled out.
- Knoll, *Radiation Detection and Measurement*, Ch. 3 — activity, counting
  statistics and the practicalities of measuring a half-life.
