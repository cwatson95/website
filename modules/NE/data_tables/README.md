# Nuclear data tables — Shultis & Faw, Appendices A–D

Reference data for the **NE** trunk, extracted from the appendices of

> J.K. Shultis & R.E. Faw, *Fundamentals of Nuclear Science and Engineering*,
> **3rd edition**, CRC Press, 2017 —
> `books/library/NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf`

The numbers here were pulled **programmatically** from the PDF (not hand-typed)
and cross-validated against each other, so they are the canonical source for
masses, abundances, cross sections and attenuation coefficients throughout the
`NE-01 … NE-27` modules. Same role as `Thermo/steam_tables/` plays for the
Thermodynamics trunk.

**Page convention.** The book's printed page numbers run 23 behind the PDF page
index: **PDF page = printed page + 23** (printed 54 = the Chapter 3 opening =
PDF 77; printed 555 = Appendix A = PDF 578). `refs.md` in each module cites
*printed* pages; `_extract.py` works in PDF pages.

---

## Files

| File | Table | What it is | Printed pp. | Rows |
|---|---|---|---|---|
| `A1_physical_constants.csv` | A.1 | Fundamental physical constants (CODATA 2002) | 555 | 20 |
| `A3_element_properties.csv` | A.3 | Atomic weights, densities, melting/boiling points, abundances | 560–561 | 92 |
| `A4_isotopic_abundances.csv` | A.4 | Isotopic abundances + decay data for T½ > 1 h | 562–569 | 916 |
| `B1_atomic_masses.csv` | B.1 | Neutral atomic masses (Audi–Wapstra 1995) | 570–587 | 2931 |
| `C1_thermal_neutron_cross_sections.csv` | C.1 | 2200 m/s (0.0253 eV) cross sections, 27 isotopes | 589–590 | 75 |
| `C2_activation_radionuclides.csv` | C.2 | Thermal-neutron activation products | 591 | 31 |
| `C3_photon_coefficients_{air,water,concrete,iron,lead}.csv` | C.3 | Photon mass coefficients, 5 materials | 591–595 | 40–58 each |
| `D1_decay_radiation.csv` | D | Individual emitted radiations, 127 nuclides | 596–624 | 1276 |
| `D2_decay_group_totals.csv` | D | keV per decay, by radiation group | 596–624 | 338 |
| `data_tables.md` | — | Human-readable rendering of the small tables | — | — |
| `_extract.py` | — | Reproducible extractor + self-validation | — | — |

The CSVs are the canonical data; `data_tables.md` is a rendering for reading.

---

## Units and conventions

| Column | Quantity | Unit |
|---|---|---|
| `atomic_mass_u`, `atomic_weight` | neutral **atomic** mass (electrons included) | u (¹²C ≡ 12 exactly) |
| `abundance_pct` | natural isotopic abundance | atom % |
| `sigma_b`, `activation_sigma_b` | microscopic cross section | barn (10⁻²⁴ cm²) |
| `mu_*_cm2_g` | photon **mass** coefficient μ/ρ | cm²/g |
| `E_MeV` | photon energy | MeV |
| `freq_pct` | emissions per 100 decays | % |
| `E_avg_keV`, `E_max_keV`, `E_keV` | mean / endpoint / discrete energy | keV |
| `keV_per_decay` | group energy yield | keV per decay |
| `half_life` | as printed, value + unit | `ky`/`My`/`Gy`/`Ty`/`Py`/`Ey` = 10³…10¹⁸ y |

**Nuclide naming.** `nuclide` is `<A><symbol>`, e.g. `235U`; metastable states carry
`m`, e.g. `137mBa`. `Z`, `A` and (in B.1) `N` are separate integer columns, and
`A = N + Z` holds for every row.

**Cross-section subscripts** in `C1_...csv` `reaction` column: `gamma` = (n,γ) radiative
capture, `s` = elastic scattering, `f` = fission, `alpha` = (n,α), `p` = (n,p),
`t` = total.

**Photon coefficients** in `C3_...csv`: `mu_c` incoherent (Compton) scattering with
electron binding, `mu_ph` photoelectric, `mu_pp` pair production, `mu` their sum,
`mu_tr` energy transfer, `mu_en` energy absorption. Rows with a non-empty `edge`
column (`K`, `L1`, `L2`, `L3`, `M`) repeat an energy immediately **above** an
absorption edge; the unflagged row at the same energy is the value **below** it.
Interpolating across an edge without noticing the duplicate is the classic way to
get shielding calculations wrong.

**Appendix D groups**: `beta`, `positron`, `conversion_auger_electron`, `gamma_xray`,
`alpha`. `incomplete = yes` reproduces the book's asterisk: the individually listed
lines account for less than 95% of that group's total, so the total is the number to
trust, not the sum of the rows.

---

## How the extraction works

`pdftotext -bbox-layout` gives a bounding box per word. Words are clustered into
visual rows by baseline and into columns by x. Three things make this necessary
rather than optional:

1. **Side-by-side records.** Tables A.4, B.1, C.2 and Appendix D print two or
   three record columns per page. A line-oriented read interleaves them.
2. **Superscripts.** Mass numbers, scientific-notation exponents, cross-section
   subscripts and footnote markers are separate, smaller glyphs whose vertical
   centres sit *between* two baselines, so a naive row clustering drops them into
   the neighbouring line. `banded_rows()` defines baselines from body glyphs only,
   then attaches each small glyph to the nearest one. Without this, `1.08×10⁵`
   silently becomes `1.08×10⁰`.
3. **Drifting margins.** The left margin of a table shifts by several points
   between pages, so Tables A.4 and C.1/C.2 are parsed as *token sequences* keyed
   on structure (superscript mass number followed by an element symbol) rather
   than on absolute x positions.

Run it with:

```bash
python3 _extract.py            # validate, then write the CSVs and data_tables.md
python3 _extract.py --check    # validate only, write nothing
```

It needs poppler's `pdftotext` on `$PATH` and the book PDF. The PDF is found via
`$NE_BOOK_PDF`, else `<repo>/books/library/NE_Nuclear_Engineering/`; when run from
a git worktree it also looks in the main checkout, since `books/` is untracked.

---

## Validation

Nothing is written until every check passes. Per table: row counts, monotonic
energy grids, and anchors checked against independently known values (¹²C = 12 u
*exactly*; ²³⁵U = 0.7204%; σ_f(²³⁵U) = 587 b; σ_α(¹⁰B) = 3840 b; the ⁶⁰Co
1173.2/1332.5 keV pair; the ¹³¹I 364.5 keV line; ³H's 18.6 keV beta endpoint).
Internal identities: `A = N + Z` for all 2931 nuclides; `μ = μ_c + μ_ph + μ_pp`
and `μ_en ≤ μ_tr` for every photon row, with `μ_pp = 0` below the 1.022 MeV
threshold; `σ_t ≥` every partial cross section; `⟨E⟩ ≤ E_max` for every beta group.

The strongest test spans three tables. Each element's standard atomic weight is
rebuilt from Table A.4's abundances and Table B.1's nuclidic masses and compared
with Table A.3:

$$M(Z) \;=\; \sum_i \frac{a_i}{100}\, M(N_i, Z)$$

**81 elements agree to better than 3×10⁻⁴** (worst 2.9×10⁻⁴). That cannot happen
unless all three tables were read correctly, and it is what turned up the errata
below.

---

## Errata and book-internal inconsistencies

Found by the cross-check, not by eye. The CSVs keep the **printed** value and flag
it in a `note` column; only the validator uses the correction.

| Table | Entry | Printed | Should be | Evidence |
|---|---|---|---|---|
| A.4 | ³²S abundance | `95.02` | `94.93` | sum over S isotopes → 100.09%, not 100%; the corrected value reproduces A.3's 32.066 |
| A.4 | ¹⁹⁴Pt abundance | `32.67` | `32.967` | sum over Pt isotopes → 99.70%; the corrected value reproduces A.3's 195.078 |

Two further elements do not reconcile to a single typo — their printed abundances
simply do not sum to 100%, so the abundances and the atomic weights come from
different evaluations: **Yb** (sums to 99.94%) and **Os** (sums to 100.14%).

Table C.1 and Table A.4 also disagree on six light isotopes, because C.1 quotes
ENDF/B-VI (1995) abundances and A.4 quotes NuBase. Largest is deuterium:

| Nuclide | C.1 | A.4 |
|---|---|---|
| ²H | 0.015 | 0.0115 |
| ¹³C | 1.11 | 1.07 |
| ¹⁷O | 0.039 | 0.038 |
| ¹⁵N | 0.36 | 0.368 |
| ¹⁰B | 19.6 | 19.9 |
| ⁶Li | 7.5 | 7.59 |

**Use A.4 for abundances.** C.1's are carried along only because they label its
cross sections.

**Transactinide symbols.** Appendix B predates the settled IUPAC names and uses
`Db`=104, `Jl`=105, `Rf`=106, `Hn`=108 — so `Db` and `Rf` there mean *different
elements* than they do today (and Table A.2 in the same book uses `Ha`=105,
`Ns`=107). `symbol` in `B1_atomic_masses.csv` is the modern IUPAC symbol derived
from `Z`; `book_symbol` preserves what the book printed where the two differ.

One PDF text-layer artifact is worth knowing about: ²¹²Pb's mass renders as
`211.991 887.5`, where the final digit group is separated by a period rather than
a space. It is parsed as 211.9918875.

---

## See also

- `../list_NE.txt` — the trunk index.
- `NE-03` (binding energy) and `NE-04` (Q-values) consume `B1_atomic_masses.csv`;
  `NE-06`/`NE-07` (decay kinetics, chains) consume `A4_isotopic_abundances.csv`
  and Appendix D; `NE-11`–`NE-13` (attenuation, photon and neutron interactions)
  consume `C1`/`C3`; `NE-17` (dosimetry) consumes `C3` (μ_en/ρ) and Appendix D.
- `Thermo/steam_tables/` — the same pattern for water properties.
