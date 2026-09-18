# 5.3 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| compressed-liquid table A-5 (`compressed`) | §3.5.1 *Vapor and Liquid Tables* | — | 105 | 123 |
| saturated-liquid reference from A-2 (`sat_liquid`) | §3.5.2 *Saturation Tables* | — | 107 | 125 |
| `v(T,p) ≈ vf(T)` (`v_approx`) | §3.10.1 *Approximations for Liquids Using Saturated Liquid Data* | **3.11** | 123 | 141 |
| `u(T,p) ≈ uf(T)` (`u_approx`) | §3.10.1 | **3.12** | 123 | 141 |
| `h(T,p) ≈ hf(T)+vf(T)[p−psat(T)]` (`h_approx`) | §3.10.1 | **3.13** | 123 | 141 |
| `h(T,p) ≈ hf(T)` (`h_approx_simple`) | §3.10.1 | **3.14** | 123 | 141 |
| `s(T,p) ≈ sf(T)` (used in `5.5`) | §6.2.3 *Liquid Data* | **6.5** | 293 | 311 |

In-text check: `v(10.0 MPa, 100 °C) = 1.0385×10⁻³ m³/kg` (p.105). **Problem 3.13**
(printed 152) specific volume of water: (a) `400 °C, 20 MPa` superheated; (b)
`40 °C, 20 MPa` A-5 → `0.9992×10⁻³`; (c) `40 °C, 2 MPa` approx `v≈vf(40 °C)=1.0078×10⁻³`
— worked in `5.HP`.

Steam-table data: `modules/Thermo/steam_tables/A5_compressed_liquid_water.csv` (8 pressure
blocks 25–300 bar, 66 rows; `v` ×10³) and `A2_sat_water_temperature.csv` for the `f`
reference. Provenance in that folder's `README.md`.

## See also
`5.1` (saturated-liquid `f` data), `5.2` (A-4 shares the two-way table format),
`5.5` (the analogous `s ≈ sf` entropy approximation), `5.EQ`, `5.EP`, `5.HP`.
