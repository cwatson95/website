# 08.1 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| mass flow rate `ṁ=AV/v` (`mass_flow_rate`) | §4.2.1 *One-Dimensional Flow Form of the Mass Rate Balance* | **4.4b** | 172 | 190 |
| CV energy balance (`power_cv`, `power_input`) | §4.8.1 *Compressor & Pump Modeling* | **4.20a** | 190 | 208 |
| compressor power `Ẇcv=ṁ(h1−h2)` | §4.8.1 | 4.20b form | 190 | 208 |
| isentropic compressor work `h2s−h1` (`isentropic_compressor_work`) | §6.12.3 *Isentropic Compressor & Pump Efficiencies* | — | 337 | 355 |
| isentropic efficiency `η_c=(h2s−h1)/(h2−h1)` (`isentropic_efficiency`) | §6.12.3 | **6.48** | 338 | 356 |

Worked examples:
- **Ex 4.5** Calculating Compressor Power (air): `ṁ=0.72 kg/s`, `Ẇcv=−119.4 kW`.
  Properties `h1=290.16`, `h2=451.80 kJ/kg` (Table A-22). p.191 / PDF 209.
- **Ex 6.14** Evaluating Isentropic Compressor Efficiency (R-22): `Ẇcv=−3.11 kW`,
  `η_c=0.81`. Properties `h1=249.75`, `h2=294.17`, `h2s=285.58 kJ/kg` (Table A-9).
  p.338 / PDF 356.

## See also
`08.2` (condenser), `08.3` (heat exchanger), `08.4` (heat pump), `8.EQ`, `8.EP`, `8.HP`.
