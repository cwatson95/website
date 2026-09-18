# 09.3 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| constant-p heat addition `Q₂₃/m = h₃−h₂` | §9.3 *Air-Standard Diesel Cycle* | **9.9, 9.10** | 518 | 536 |
| efficiency, air-table `η=1−(u₄−u₁)/(h₃−h₂)` (`diesel_efficiency_air_table`) | §9.3 | **9.11** | 519 | 537 |
| expansion volume ratio `V₄/V₃ = r/rc` (`temp_after_isentropic_expansion`) | §9.3 | **9.12** | 519 | 537 |
| efficiency, cold air-standard `η=1−(1/r^(k−1))(rc^k−1)/(k(rc−1))` (`diesel_efficiency`) | §9.3 *Effect of Compression Ratio on Performance* | **9.13** | 519 | 537 |

## Worked Example used
| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| **9.2** | Analyzing the Diesel Cycle (η = 0.578 air-table; T₂, T₃, T₄, p₂, mep) | 520–521 | 538–539 |

Example 9.2's published `η = 0.578` is the air-table value (Eq. 9.11); the cold
air-standard `η = 0.632` (Eq. 9.13) for the same `r, rc` overpredicts and is noted in
the book as "left as an exercise" (p.521). Cold-air `k = 1.4` per Table A-20.

## See also
`09.2` (Otto — `rc → 1` limit), `09.4` (dual — `r_p → 1` limit gives Eq. 9.13), `09.1`
(Carnot ceiling), `07.1` (efficiency), Topic 5 (air tables), `9.EQ`/`9.EP`/`9.HP`.
