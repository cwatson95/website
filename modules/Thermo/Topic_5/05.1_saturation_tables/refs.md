# 5.1 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| `p`,`T` not independent in dome | §3.2.2 *Projections of the p–v–T Surface* | — | 100 | 118 |
| quality definition (`quality_from_v` inverts) | §3.3 *Studying Phase Change* | **3.1** | 102 | 120 |
| linear interpolation (`linear_interp`) | §3.5.1 *Vapor and Liquid Tables* | — | 105 | 123 |
| saturation tables A-2/A-3 (`sat_T`, `sat_p`) | §3.5.2 *Saturation Tables* | — | 107 | 125 |
| two-phase mixture rule `v=vf+x(vg−vf)` (`mixture`) | §3.5.2 | **3.2** | 108 | 126 |
| mixture rule for `u` | §3.6.2 *Retrieving u and h Data* | **3.6** | 112 | 130 |
| mixture rule for `h` | §3.6.2 | **3.7** | 112 | 130 |
| mixture rule for `s` | §6.2.2 *Saturation Data* | **6.4** | 293 | 311 |
| finding states from `(p,T)` (`phase_pT`) | "Finding States in the Steam Tables" | — | 109 | 127 |

Worked example: **Ex 3.2** *Heating Water at Constant Volume* (rigid two-phase) —
`v₁=0.8475 m³/kg`, `T₁=99.63 °C`, `T₂=111.4 °C`, `m=0.59 kg`, `x₂=0.731`,
`mg₂=0.431 kg`, `p₃=2.11 bar` (printed 109–111 / PDF 127–129; reproduced in `5.EP`).
In-text quality illustration water `100 °C`, `x=0.9` → `v=1.506 m³/kg` (printed 108).

Steam-table data: `modules/Thermo/steam_tables/A2_sat_water_temperature.csv` (70 rows,
0.01–374.14 °C) and `A3_sat_water_pressure.csv` (50 rows, 0.04–220.9 bar); `vf` stored
×10³. See that folder's `README.md` for extraction/validation provenance.

## See also
`5.2` (superheated vapor A-4), `5.3` (compressed liquid A-5 + sat-liquid approximation),
`5.4` (p–v diagram), `5.5` (T–s diagram), `5.EQ`, `5.EP`, `5.HP`.
