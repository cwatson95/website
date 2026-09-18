# NE-18 — References

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
| Health effects from large acute doses | §9.5 | 288–289 | 311–312 |
| Effects on individual cells; LET, dose rate, mitotic state | §9.5.1 | 289 | 312 |
| Deterministic effects; D₅₀ and D_th | §9.5.2 | 289–292 | 312–315 |
| **Table 9.7** — D₅₀ and D_th by organ (`DETERMINISTIC_EFFECTS`) | Table 9.7 | 290 | 313 |
| Skin, eye lens, blood-forming tissue, GI, gonads, embryo | §9.5.2 | 290–292 | 313–315 |
| Potentially lethal exposure; the three dose conventions | §9.5.3 | 292–294 | 315–317 |
| **Table 9.8** — LD_x/60 (`LETHAL_DOSES`, `lethality_fraction`) | Table 9.8 | 292 | 315 |
| **Table 9.9** — high sublethal doses (`SUBLETHAL_EFFECTS`) | Table 9.9 | 293 | 316 |
| **Table 9.10** — the prodromal syndrome (`PRODROMAL_SYMPTOMS`) | Table 9.10 | 293 | 316 |
| The four stages of radiation illness (`ARS_STAGES`) | §9.5.3 | 294 | 317 |
| Hereditary effects; Muller 1927 | §9.6 | 294–295 | 317–318 |
| Classification of genetic effects | §9.6.1 | 295 | 318 |
| **Table 9.11** — BEIR-VII / UNSCEAR genetic risks (`GENETIC_RISKS`) | Table 9.11 | 296 | 319 |
| Gonad dose vs effective dose | §9.6.2 | 296–297 | 319–320 |
| **Doubling dose**; MC and PRCF (`doubling_dose`, `hereditary_risk`) | Eq. (9.13) | 297 | 320 |
| **Risk for dominant/X-linked disorders** | Eq. (9.14) | 297 | 320 |
| Cancer risks; latency, initiation/promotion/progression | §9.7 | 297–299 | 320–322 |
| **Table 9.12** — U.S. cancer rates 2002 (`CANCER_BASELINE`) | Table 9.12 | 298 | 321 |
| Estimating radiogenic risk; **DDREF** | §9.7.1, Fig. 9.2 | 299 | 322 |
| Dose-response models; the ERR form | §9.7.2 | 300–301 | 323–324 |
| **risk = R₀ × ERR** | Eq. (9.15) | 300 | 323 |
| **ERR = β_s D exp(e*γ)(a/60)^η** (`excess_relative_risk`) | Eq. (9.16) | 300 | 323 |
| Average risks for exposed populations; the 0.057/Gy factor | §9.7.3 | 301 | 324 |
| **Table 9.13** — risk by age at exposure (`LIFETIME_CANCER_RISK`) | Table 9.13 | 302 | 325 |
| **Table 9.14** — three exposure scenarios (`EXPOSURE_SCENARIOS`) | Table 9.14 | 303 | 326 |
| Probability of causation | §9.7.4 | 301–303 | 324–326 |
| **PC = ERR/(1+ERR)** (`probability_of_causation`) | Eq. (9.17) | 303 | 326 |
| **Example 9.6** — a 30-y male at 0.02 Gy | Ex. 9.6 | 303 | 326 |
| Radon and lung cancer | §9.8 | 303–307 | 326–330 |
| **The ²²²Rn chain** (`RN222_CHAIN`) | Eq. (9.18) | 304 | 327 |
| **Potential alpha energy** (`potential_alpha_energy_per_bq`) | Eqs. (9.19)–(9.20) | 304–305 | 327–328 |
| **EEC = F·C₀** (`equilibrium_equivalent_concentration`) | Eq. (9.21) | 305 | 328 |
| Outdoor and indoor concentrations; the EPA 150 Bq/m³ action level | §9.8.1 | 305–306 | 328–329 |
| **Table 9.15** — risk by population (`RADON_RISK_BY_POPULATION`) | Table 9.15 | 306 | 329 |
| **Table 9.16** — risk by age and duration (`RADON_RISK_BY_AGE_DURATION`) | Table 9.16 | 307 | 330 |
| **1 WLM = 629 000 Bq h m⁻³** (`wlm_to_bq_h_per_m3`) | §9.9 fn. 4 | 307 | 330 |
| **Example 9.7** — 10⁶ people at 20 Bq/m³ | Ex. 9.7 | 308 | 331 |
| Radiation protection standards | §9.9 | 307–310 | 330–333 |
| **Risk-related dose limits** (`occupational_limit_sv`, `public_limit_sv`) | §9.9.1 | 308–309 | 331–332 |
| **Table 9.17** — the 1987 NCRP limits (`NCRP_1987_LIMITS`) | Table 9.17 | 310 | 333 |
| 10 CFR 20; TEDE | §9.9.2 | 310–311 | 333–334 |
| Radiation hormesis; the five models | §9.10, Fig. 9.3 | 311–312 | 334–335 |
| A hormetic model; scavengers, repair enzymes, apoptosis | §9.10.1 | 312–313 | 335–336 |
| Evidence for hormesis; Cohen's radon study, worker cohorts | §9.10.2 | 313–314 | 336–337 |
| Is the LNT model doomed? | §9.10.3 | 314–316 | 337–339 |

## Problems (verified, S&F 3rd ed. Ch. 9)
Chapter 9's problems begin on printed **318** (PDF 341). Problems **7–20** belong
to this module; **1–6** are dosimetry and are worked in `~NE-17`.

- **Prob. 7** — a worker takes 2.3 Gy — printed 319, PDF 342.
- **Prob. 8–9** — collective dose and hereditary illness — printed 319, PDF 342.
- **Prob. 11–13** — cancer risk from background and occupational exposure — printed 319, PDF 342.
- **Prob. 14–18** — radon exposure and lung-cancer risk — printed 320, PDF 343.
- **Prob. 19–20** — the rationale for the limits — printed 320, PDF 343.

### The solution manual is offset by two
For Chapter 9 the authors' solution manual is numbered **+2** relative to the
textbook from problem 7 onwards: its Problems 7 and 8 (the ⁴⁰K in a banana, and
the ²²⁶Ra maximum permissible body burden) do not appear in the textbook's list
at all, so its Prob. 9 is the textbook's Prob. 7, and so on. Several restated
problems also carry different numbers from the textbook's — 900 µCi vs 700 µCi,
330 million vs 320 million, a 40-year-old worker vs a 35-year-old. The manual was
evidently written against a different edition. Where the two disagree, the
problems here follow the **textbook** and the tests cross-check against the
manual's worked arithmetic.

## Five printed results this module corrects

### Table 9.11 — a total that does not match its column (printed p. 296)
The second-generation column reads 1300–2500, 0, 250–1200 and 2400–3000, which
adds to **3950**–6700. The Total row prints **3930**–6700.

Unlike the other four, **this one cannot be resolved from the book alone.** The
"percent of baseline" row prints 0.53, and 3930/738 000 = 0.5325% rounds to 0.53
while 3950/738 000 = 0.5352% rounds to 0.54 — so the printed percentage was
computed from the printed total and the two agree with each other. Either the
total and the percentage are both wrong, or one of the three column entries is 20
lower than printed. The first-generation column adds exactly (3000–4700), which
establishes that the table format is being read correctly.

The published BEIR-VII table gives 3950–6700, which is why the module treats the
column as authoritative — but that is an outside source, so the test pins the
**inconsistency** and not the resolution. *Verified:
`test_table_9_11_does_not_add_up_to_its_own_total`.*

### Example 9.7 — 3116 where its own factors give 3416 (printed p. 308)
The example computes an annual exposure of 0.0876 MBq h m⁻³ and a risk of 0.039
per MBq h m⁻³ for 10⁶ people, and reports "3116 radon-induced deaths".
$0.039\times0.0876\times10^6=3416$. The **next sentence** divides by a 73-year
lifespan and reports 47 deaths per year — which requires 3416 (3116/73 = 42.7).
The book's own following line therefore identifies the typo. *Verified:
`test_reproduces_example_9_7_and_its_two_errors`.*

### Example 9.7 — a natural mortality rate that is not in the table it cites
The same example states "the annual natural mortality from respiratory cancer is,
**from Table 9.12**, 71.9 per 10⁵ for males and 25.2 per 10⁵ for females", and
gets 486 deaths per year. Table 9.12 gives **76.2 and 42.2** — and all four of
that table's columns add correctly to its own Total row, so the table is
self-consistent and the example is not. Using the table gives **592** deaths per
year. The printed 71.9/25.2 pair appears to be carried over from an older
edition's table. *Verified: same test.*

### Solution manual, ²²⁶Ra body burden — a ²²⁰Rn alpha in a ²²²Rn chain
The solution lists the alpha energies of ²²⁶Ra, ²²²Rn, ²¹⁸Po and ²¹⁴Po as 4.774,
**6.288**, 6.001 and 7.687 MeV, summing to 24.75 MeV. But 6.288 MeV is
**²²⁰Rn's** alpha; the book's own Appendix D gives ²²²Rn 5.4897 MeV and ²²⁰Rn
6.2884 MeV. (The 4.774 MeV for ²²⁶Ra is right, and non-obviously so — it is the
frequency-weighted mean of Appendix D's 4601.8 keV at 5.55% and 4784.5 keV at
94.44%, which is what confirms the extraction and the reading.) The correct sum
is 23.95 MeV and the dose rate is **4.99 rad/y**, not 5.15. *Verified: the alpha
energies in `../data_tables/D1_decay_radiation.csv`.*

### Solution manual, the banana — two errors that partly cancel
The ⁴⁰K problem computes the decay constant as
$\ln2/[(1.27\times10^9\ \mathrm{y})(365.24\ \mathrm{d/y})(\mathbf{3600}\ \mathrm{s/d})]$
— seconds per **hour**, not per day, making λ 24× too large — and then a ⁴⁰K atom
count ten times too small. The product comes out 2.4× high: **30.9 Bq** per
banana where natural potassium's specific activity (31.0 Bq per gram of K) gives
$0.422\ \mathrm{g}\times31.0=13.1$ Bq, and the module's own arithmetic with the
book's own inputs gives 12.9 Bq. The committed dose is therefore 0.066 µSv per
banana, not 0.157 µSv.

Worth adding, since the problem invites it: **eating bananas does not raise your
⁴⁰K burden at all.** Body potassium is homeostatically regulated, so the excess is
excreted and the "banana equivalent dose" is a unit of exposition, not of dose.

## Where the module refuses rather than answering

**A trivial individual dose.** `radiogenic_cancer_deaths` raises below a tenth of
natural background. Linearity makes $N\times D$ the only input, so the model
happily reports deaths from a collective dose assembled out of individual doses
far below anything ever observed to do anything — S&F state this property
explicitly ($10^7$ people at 0.01 mSv "equals" 1000 at 100 mSv), and ICRP-103
states that computing deaths that way "is not reasonable and should be avoided".
The arithmetic is not wrong; the extrapolation underneath it has no support, and
a function that returns a confident number hides exactly that.

## Two numbers in the same chapter that disagree
§9.7.3 derives a sex-averaged fatal-cancer risk of **0.057 Gy⁻¹** from Table 9.14
and rounds it to 0.05/Gy. §9.9.2 quotes NCRP's **10⁻² Sv⁻¹** for the same
quantity — a factor of 5.7 smaller — and uses it to derive the dose limits.
Neither is an erratum: they are different committees' fits (BEIR-VII vs NCRP-116)
made a decade apart, and the spread is an honest measure of how well this quantity
is known. `test_the_environmental_risk_factor` pins both and the ratio.

## Further reading
- NAS/NRC, *Health Risks from Exposure to Low Levels of Ionizing Radiation*
  (BEIR VII Phase 2, 2006) — the source of Tables 9.11, 9.13, 9.14 and Eq. (9.16).
- ICRP Publication 103 (2007), §(k) and Annex A — the current framework, and the
  explicit warning against collective-dose death counting.
- UNSCEAR 2000 and 2001 reports — the other half of Table 9.11's provenance.
- Cohen, B.L., *Health Physics* **68** (1995) 157 — the county-level radon study
  §9.10.2 leans on, and the ecological-fallacy critiques that followed it.
- Preston et al., *Radiat. Res.* **168** (2007) 1 — the Life Span Study solid-cancer
  incidence analysis behind the modern risk coefficients.
