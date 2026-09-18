# 08.4 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| Carnot refrigerator COP `β_max=T_C/(T_H−T_C)` (`carnot_cop_refrigeration`) | §10.1 *Vapor Refrigeration Systems* | **10.1** | 611 | 629 |
| refrigerator COP `β=Q_C/W_net`; VC form `(h1−h4)/(h2−h1)` (`cop_refrigeration`, `cop_ref_from_enthalpies`) | §10.2 *Analyzing Vapor-Compression Refrigeration Systems* | **10.7** | 613 | 631 |
| cycle first law `Q_H=Q_C+W_net` (`heat_rejected`) | §10.6 *Vapor-Compression Heat Pump Systems* | **10.8** | 629 | 647 |
| Carnot heat-pump COP `γ_max=T_H/(T_H−T_C)` (`carnot_cop_heat_pump`) | §10.6 | **10.9** | 629 | 647 |
| heat-pump COP `γ=Q_H/W_net`; VC form `(h2−h3)/(h2−h1)` (`cop_heat_pump`, `cop_hp_from_enthalpies`) | §10.6 | **10.10** | 630 | 648 |

## Worked Examples used
| Example | Title | Result | Printed p. | PDF p. |
|---|---|---|---|---|
| **10.1** | Ideal Vapor-Compression Refrigeration Cycle (R-134a) | β = 9.24 (Carnot β_max = 10.5) | 613–615 | 631–633 |
| **10.4** | Vapor-Compression Heat Pump (R-134a) | γ = 4.65 | 630–631 | 648–649 |

The `γ = β + 1` identity (since `Q_H = Q_C + W_net`) makes every heat-pump COP ≥ 1, and both
COPs are capped by the Carnot value `T_H/(T_H−T_C)` (temperatures in **kelvin**). R-134a
enthalpies are read from Tables A-10…A-12.

## See also
`08.1` (compressor), `08.2` (condenser), `08.3` (heat exchanger), Topic 9 (full
vapor-compression / refrigeration *cycles*), `07.1` (efficiency & COP), `8.EQ`/`8.EP`/`8.HP`.
