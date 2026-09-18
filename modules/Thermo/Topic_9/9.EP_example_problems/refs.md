# 9.EP — References

Examples read page-by-page from the PDF. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| 9.1 | Analyzing the Otto Cycle | 515–517 | 533–535 |
| 9.2 | Analyzing the Diesel Cycle | 520–521 | 538–539 |
| 9.3 | Analyzing the Dual Cycle | 523–524 | 541–542 |
| 9.4 | Analyzing the Ideal Brayton Cycle | 529–531 | 547–549 |
| 9.5 | Determining Compressor Pressure Ratio for Maximum Net Work | 533–534 | 551–552 |
| 9.6 | Evaluating Performance of a Brayton Cycle with Irreversibilities | 535–537 | 553–555 |
| 9.7 | Evaluating Thermal Efficiency of a Brayton Cycle with Regeneration | 539–541 | 557–559 |
| 8.1 | Analyzing an Ideal Rankine Cycle | 450–452 | 468–470 |
| 8.2 | Analyzing a Rankine Cycle with Irreversibilities | 456–458 | 474–476 |
| 8.3 | Evaluating Performance of an Ideal Reheat Cycle | 461–463 | 479–481 |
| 8.4 | Evaluating Performance of a Reheat Cycle with Turbine Irreversibility | 463–464 | 481–482 |

## Equations used
mep (Eq. 9.1, p.511); Otto η/isentropic legs (Eqs. 9.2–9.8, p.514–515); Diesel
(Eqs. 9.11–9.13, p.519); dual (Eq. 9.14, p.523); Brayton works/heats/η/bwr
(Eqs. 9.15–9.20, p.527–528), `p_r`/cold-air legs (Eqs. 9.21–9.25, p.529–532),
regenerator (Eqs. 9.26–9.27, p.538–539); Rankine balances (Eqs. 8.1–8.6, p.446–447),
pump approximation (Eq. 8.7b, p.449), η_t/η_p (Eqs. 8.9–8.10b, p.455–456). Canonical
implementations in module `9.EQ`.

Embedded property data are the book's own quotes: Table A-22/A-22E air values
(u, h, v_r, p_r at the Example states), Table A-3/A-4 steam values, and Table A-2
`h_f` for the condenser cooling water. The Rankine steam values are additionally
cross-checked against `modules/Thermo/steam_tables/` in module `09.6`.

## See also
`9.EQ` (the equations these use), `9.HP` (end-of-chapter problems), and the concept
modules `09.1`–`09.6`.
