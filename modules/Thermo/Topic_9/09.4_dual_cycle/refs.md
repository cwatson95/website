# 09.4 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| dual-cycle p–V description (1-2-3-4-5) | §9.4 *Air-Standard Dual Cycle* | — | 522 | 540 |
| efficiency, air-table `η=1−(u₅−u₁)/[(u₃−u₂)+(h₄−h₃)]` (`dual_efficiency_air_table`) | §9.4 | **9.14** | 523 | 541 |
| state relations `T₃=r_pT₂`, `T₄=r_cT₃`, `T₅=T₄(r_c/r)^(k−1)` (`temp_after_*`) | §9.4 | — | 523–524 | 541–542 |
| efficiency, cold air-standard closed form (`dual_efficiency`) | §9.4 (constant-`c_p` extension) | — | 523 | 541 |

## Worked Example used
| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| **9.3** | Analyzing the Dual Cycle (r=18, r_p=1.5, r_c=1.2; η=0.635, w_net=456 kJ/kg, mep=0.56 MPa) | 523–524 | 541–542 |

Example 9.3 shares states 1–2 with the Diesel Example 9.2; its published `η = 0.635` is the
air-table value (Eq. 9.14). The cold air-standard closed form (`dual_efficiency`) gives `0.68`
for the same `r, r_p, r_c` — constant `c_p` **overpredicts**, exactly as in Otto/Diesel.
Cold-air `k = 1.4` per Table A-20.

## See also
`09.2` (Otto — `r_c → 1` limit), `09.3` (Diesel — `r_p → 1` limit), `09.1` (Carnot ceiling),
`07.1` (efficiency), Topic 5 (air tables A-22), `9.EQ`/`9.EP`/`9.HP`.
