# 5.5 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| T–s diagram (Fig. 6.2) | §6.2.5 *Using Graphical Entropy Data* | — | 295 | 313 |
| Mollier h–s diagram (Fig. 6.3) | §6.2.5 | — | 296 | 314 |
| entropy mixture `s = sf + x(sg − sf)` | §6.2.2 *Saturation Data* | **6.4** | 293 | 311 |
| `dS = (δQ/T)_int,rev` | §6.6 *Entropy Change in Internally Reversible Processes* | **6.2b** | 302 | 320 |
| heat `Q = ∫T dS` (area on T–s) (`heat_TdS`, `heat_isothermal`) | §6.6.1 *Area Representation of Heat Transfer* | **6.23** | 302 | 320 |
| Carnot on T–s; `η = 1 − T_C/T_H` (`carnot_net_work`, `carnot_efficiency`) | §6.6.2 *Carnot Cycle Application* (cf. Eq. 5.9) | — | 303 | 321 |

Worked example: **Ex 6.1** *Evaluating Work and Heat Transfer for an Internally Reversible
Process of Water* — water vaporized at `150 °C`: `Q/m = T(s₂ − s₁) = 2114.1 kJ/kg`
(`s` from A-2: `sf=1.8418`, `sg=6.8379`); the companion `W/m=186.38 kJ/kg` is in `5.4`.
Printed 303–304 / PDF 321–322; reproduced in `5.EP`. Mollier in-text illustration water
`240 °C, 0.10 MPa` → isentropic to `0.01 MPa`: `x₂≈0.98`, `h₂≈2537 kJ/kg` (p.296).

Entropy data for the worked numbers: `modules/Thermo/steam_tables/` A-2/A-3/A-4
(`s` columns). The Carnot relations use only temperatures (no table data).

## See also
`5.1` (entropy `sf, sg` from the steam tables), `5.4` (the p–v diagram — area = work),
`5.EP` (Example 6.1), `5.EQ`.
