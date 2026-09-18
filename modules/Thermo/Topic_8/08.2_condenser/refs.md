# 08.2 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| HX energy balance (`heat_transfer_rate`, `heat_rejected`) | §4.9.1 *Heat Exchanger Modeling Considerations* | from 4.20a/4.18 | 196 | 214 |
| cycle condenser `Q̇out/ṁ=h2−h3` (`condenser_heat_per_mass`) | §10.2.1 *Evaluating Principal Work & Heat Transfers* | **10.5** | 613 | 631 |
| two-phase enthalpy `h=hf+x(hg−hf)` (`enthalpy_two_phase`, `quality_from_h`) | §3.6 *Evaluating Properties Using the Steam Tables* | 3.2/3.6 | 103 | 121 |

Worked examples:
- **Ex 4.7** Evaluating Performance of a Power Plant Condenser — steam side:
  `Q̇cv/ṁ = h2 − h1 = −2276.7 kJ/kg`. Properties: 0.1 bar `hf=191.83`, `hg=2584.7`
  (Table A-3); 45 °C `hf=188.45` (Table A-2). p.197–198 / PDF 215–216.
- **Ex 10.4** Analyzing an Actual Vapor-Compression Heat Pump Cycle — condenser:
  `Q̇out = ṁ(h2−h3) = 34.98 kW`. Properties `h2=280.19`, `h3=105.29 kJ/kg` (R-134a,
  Tables A-12/A-11). p.632 / PDF 650.

Supporting table values verified against the local `steam_tables/` CSVs (Moran A-2/A-3).

## See also
`08.1` (compressor), `08.3` (heat exchanger), `08.4` (heat pump), `8.EQ`, `8.EP`, `8.HP`.
