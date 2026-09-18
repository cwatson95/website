# 5.2 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| superheated vapor table A-4 (`superheated`) | §3.5.1 *Vapor and Liquid Tables* | — | 105 | 123 |
| linear / double interpolation (`linear_interp`) | §3.5.1 (Fig. 3.7) | — | 105–106 | 123–124 |
| enthalpy `h = u + pv` (`enthalpy`) | §3.6.1 *Introducing Enthalpy* | **3.4** | 111 | 129 |

In-text checks: `v(10.0 MPa, 600 °C)=0.03837 m³/kg` (p.105); single-interpolation
`v(10 bar, 215 °C)=0.2141` (Fig. 3.7, p.106); `h(0.10 MPa,120 °C)=u+pv=2716.6 kJ/kg`
(p.112). **Problem 3.7** (printed 152) supplies a mini-table at `1.0`/`1.5 MPa` for
interpolation practice: (a) `v(240 °C,1.25 MPa)=0.1879`, (b) `T(1.5 MPa,0.1555)=260 °C`,
(c) `v(220 °C,1.4 MPa)=0.1557` — worked in `5.HP`.

Steam-table data: `modules/Thermo/steam_tables/A4_superheated_water.csv` (24 pressure
blocks 0.06–320 bar, 278 rows; `v` direct m³/kg). Provenance in that folder's `README.md`.

## See also
`5.1` (saturation tables — the `Sat.` rows that start each A-4 block), `5.3` (A-5 shares
this format), `5.EP` (Examples 3.3/3.4), `5.EQ`, `5.HP`.
