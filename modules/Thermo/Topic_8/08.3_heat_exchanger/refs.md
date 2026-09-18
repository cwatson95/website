# 08.3 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| multi-stream energy balance (`energy_balance_residual`) | §4.9.1 *Heat Exchanger Modeling Considerations* | **4.18** | 196 | 214 |
| mass-flow ratio (`mass_flow_ratio_cold_to_hot`, `mass_flow_other`) | §4.9.2 / Ex 4.7 | from 4.18 | 197 | 215 |
| per-stream duty (`heat_duty`) | §4.9.1 | from 4.20a | 196 | 214 |
| constant-cp Δh (`sensible_enthalpy_change`) | §3.14.2 (ideal gas) / §3.10.3 (incompressible) | 3.51 / 3.20b | 140 / 118 | 158 / 136 |
| two-phase enthalpy (`enthalpy_two_phase`) | §3.6 | 3.2/3.6 | 103 | 121 |

Worked example:
- **Ex 4.7** Evaluating Performance of a Power Plant Condenser (two-stream view):
  cooling-water-to-steam mass-flow ratio `ṁ3/ṁ1 = (h1−h2)/(h4−h3) = 36.3`;
  Quick Quiz: at `ṁ1 = 125 kg/s` the cooling water is 4538 kg/s.
  Properties: 0.1 bar `hf=191.83`, `hg=2584.7` (A-3); 45 °C `hf=188.45`, and cooling-water
  `h4−h3 = hf(35)−hf(20) = 146.68−83.96 = 62.7 kJ/kg` (A-2). p.197 / PDF 215.

## See also
`08.1` (compressor), `08.2` (condenser), `08.4` (heat pump), `8.EQ`, `8.EP`, `8.HP`.
