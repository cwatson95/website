# 10.2 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| Stirling cycle (2 isothermals + 2 const-V, regenerated); `η = 1 − T_C/T_H` (`stirling_efficiency`) | §9.8.4 *Ericsson and Stirling Cycles* | — | 552–553 | 570–571 |
| Carnot efficiency identity `η_max = 1 − T_C/T_H` | §5.9.1 *Power Cycles* | **5.9** | 265 | 283 |
| isothermal ideal-gas heat `Q = W = R T ln(V₂/V₁)` (`isothermal_heat`) | §2.2 *Broadening Our Understanding of Work* | **2.17** | 49 | 67 |
| constant-volume Δu `c_v(T_H−T_C)` regenerator heat (`regenerator_heat`) | §3.14.2 *Using Constant Specific Heats* | **3.50** | 140 | 158 |
| regenerator effectiveness `(h_x−h_2)/(h_4−h_2)` (`regenerator_effectiveness`) | §9.7 *Regenerative Gas Turbines* | **9.27** | 539 | 557 |

The ideal (100 %-regeneration) Stirling efficiency equals the Carnot value `1 − T_C/T_H`
(Moran p.552–553); without regeneration the constant-volume heating must be supplied
externally and the efficiency drops far below it. `T` absolute.

## See also
`10.1` (Carnot engine — the shared `1 − T_C/T_H` ceiling), Topic 9 (`09.5` Brayton uses the
same regenerator idea), `07.1` (efficiency), `10.EQ`/`10.EP`/`10.HP`.
