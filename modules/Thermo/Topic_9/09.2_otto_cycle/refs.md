# 09.2 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| Otto energy transfers `W/m, Q/m = Δu` | §9.2 *Air-Standard Otto Cycle* | **9.2** | 514 | 532 |
| efficiency, air-table `η=1−(u₄−u₁)/(u₃−u₂)` (`otto_efficiency_air_table`) | §9.2 | **9.3** | 514 | 532 |
| isentropic compression `T₂/T₁=r^(k−1)` (`temp_after_isentropic_compression`) | §9.2 *(cold air-standard)* | **9.6** | 514 | 532 |
| isentropic expansion `T₄/T₃=1/r^(k−1)` (`temp_after_isentropic_expansion`) | §9.2 *(cold air-standard)* | **9.7** | 514 | 532 |
| efficiency, cold air-standard `η=1−1/r^(k−1)` (`otto_efficiency`) | §9.2 *Effect of Compression Ratio on Performance* | **9.8** | 515 | 533 |

## Worked Example used
| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| **9.1** | Analyzing the Otto Cycle (η = 0.51 air-table, 0.565 cold; T₂, T₄, mep) | 515–517 | 533–535 |

The two efficiencies (0.51 vs 0.565) and the temperatures 1212/1241 °R and
1878/1567 °R are read directly from Example 9.1's air-standard vs cold air-standard
comparison table (p.517). Cold-air `c_v=0.718`, `c_p=1.005`, `k=1.4` are Moran Table A-20.

## See also
`09.1` (Carnot ceiling), `09.3` (Diesel — constant-p burn), `09.4` (dual),
`07.1` (efficiency), Topic 5 (air tables), `9.EQ`/`9.EP`/`9.HP`.
