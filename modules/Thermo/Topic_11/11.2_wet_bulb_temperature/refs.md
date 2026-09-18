# 11.2 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| humidity ratio from $T_{as}$ (`humidity_ratio_from_wet_bulb`) | §12.5.5 *Evaluating Humidity Ratio Using the Adiabatic-Saturation Temperature* | **12.48** | 763 | 781 |
| saturated exit ratio $\omega'$ (`humidity_ratio_at_saturation`) | §12.5.5 | **12.49** | 763 | 781 |
| adiabatic-saturator energy balance (`adiabatic_saturator_residual`) | §12.5.5 *Modeling an Adiabatic Saturator* | **12.50** | 764 | 782 |
| wet-bulb / dry-bulb temperatures, psychrometer | §12.6 *Psychrometers: Measuring the Wet-Bulb and Dry-Bulb Temperatures* | — | 764–765 | 782–783 |
| chart dry-air enthalpy datum (`dry_air_enthalpy`) | §12.7 *Psychrometric Charts* | **12.51** | 767 | 785 |
| mixture enthalpy at a chart point (`state_enthalpy`) | §12.7 (≈ const along $T_{wb}$) | from 12.46 | 766–767 | 784–785 |
| dew-point vapor pressure (`dew_point_pressure`) | §12.5.4 (invert Eq. 12.43) | — | 757 | 775 |
| add moisture to a stream (`exit_humidity_ratio`) | §12.8.1 *Mass Balance* (applied §12.8.4) | **12.52** | 768 | 786 |

In-text anchor: psychrometer reading dry-bulb $68\,^\circ$F + wet-bulb $60\,^\circ$F gives
$\omega=0.0092$ lb/lb, $\phi=63\%$ from Fig. A-9E (p.767 / PDF 785). Steam-table reads:
$p_g(10^\circ\text{C})=1.228$ kPa, $h_f/h_g(10^\circ\text{C})=42.01/2519.8$;
$p_g(25^\circ\text{C})=3.169$ kPa, $h_f/h_g(25^\circ\text{C})=104.89/2547.2$;
$h_g(40^\circ\text{C})=2574.3$ kJ/kg (Table A-2, PDF 945). $c_{pa}=1.005$ kJ/kg·K.

## See also
`11.1` (dry-bulb, humidity ratio, dew point), `11.EQ` (equation registry), `11.EP`
(Example 12.12 at a dry/wet-bulb point), `11.HP` (wet-bulb problem 12.77).
