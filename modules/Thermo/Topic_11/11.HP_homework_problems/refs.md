# 11.HP — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Problem | Topic | Printed p. | PDF p. |
|---|---|---|---|
| 12.51 | cooling moist air at constant pressure, Q̇ | 795 | 813 |
| 12.52 | isothermal compression → condensation | 795 | 813 |
| 12.56 | dew point of an N₂/water-vapor mixture | 795 | 813 |
| 12.60 | dehumidifier with refrigerant coil | 796 | 814 |
| 12.77 | wet-bulb/dry-bulb state, then cooling | 797 | 815 |
| 12.78 | dehumidifier (Q and condensate per kg dry air) | 797 | 815 |
| 12.92 | adiabatic evaporative cooler | 799 | 817 |

Equations used: 12.43 (ω from pv), 12.44 (φ), 12.46 (mixture enthalpy), 12.48–12.49
(wet-bulb/adiabatic-saturation ω), 12.52 (water mass balance), 12.55 (air-conditioning
energy balance). Steam-table reads (Table A-2, PDF 945 / A-2E, PDF 993):
- SI: pg(15/20/25/30/35 °C)=0.01705/0.02339/0.03169/0.04246/0.05628 bar;
  hg(15/25/30/35)=2528.9/2547.2/2556.3/2565.3; hf(15)=62.99, hf(20)=83.96 kJ/kg.
- English: pg(62/68/82/100 °F)=0.2751/0.3391/0.5414/0.9503; pg(140/150)=2.892/3.722;
  hf(68)=36.09, hg(62/68/82)=1088.6/1091.2/1097.3 Btu/lb.

> **Unverifiable against the book:** Moran prints no answers for these problems, so the
> tabulated numbers are this module's *worked solutions*, cross-checked only for physical
> consistency. Where a dew-point/onset temperature is reported (12.51, 12.56, 12.77) it is
> a **linear interpolation** between the two bracketing Table A-2 / A-2E rows. The "10 lb/min"
> in 12.77 is taken as the moist-air (total) mass flow; ṁₐ is derived from it.

## See also
`11.1`, `11.2` (the relations these problems apply), `11.EP` (the Ch.12 *examples*),
`11.EQ` (equation registry).
