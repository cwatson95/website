# 12.1 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| combustion, air model (`theoretical_air_molar`) | §13.1, §13.1.2 *Introducing Combustion / Modeling Combustion Air* | 13.1, 13.3–13.5 | 806–809 | 824–827 |
| theoretical O₂ `C+H/4+S−O/2` (`theoretical_O2`) | §13.1.2 *Theoretical Air* | (from 13.4) | 808 | 826 |
| air–fuel ratio mass↔molar (`afr_molar_to_mass`) | §13.1.2 *Air–Fuel Ratio* | **13.2** | 808 | 826 |
| % theoretical / excess air, φ (`equivalence_ratio`) | §13.1.2 | (from 13.5) | 808–809 | 826–827 |
| products & dew point `p_v=y_v p` (`dew_point_partial_pressure`) | §13.1.3 *Determining Products of Combustion* | — | 811–812 | 829–830 |
| enthalpy `h=h°_f+Δh` (`enthalpy`) | §13.2.1 *Evaluating Enthalpy for Reacting Systems* | **13.9** | 817 | 835 |
| enthalpy of combustion (`enthalpy_of_combustion`) | §13.2.3 *Enthalpy of Combustion and Heating Values* | **13.18** | 825 | 843 |
| heating values HHV/LHV (`heating_value_mass`) | §13.2.3 | — | 825–826 | 843–844 |
| energy balance `(Q̇−Ẇ)/ṅ_F = h̄_P−h̄_R` (`energy_balance_per_mole_fuel`) | §13.2.2 *Energy Balances for Reacting Systems* | **13.12b, 13.15b** | 818–819 | 836–837 |

Worked anchors reproduced in `code/fuels.py`: **Ex 13.1** octane AFR (`a_O₂=12.5`,
`AF̄=59.5`, `AF=15.1`; 150% air `AF̄=89.25`, `φ=0.67`) p.809–810 / PDF 827–828; **Ex 13.2**
methane dry-product analysis (`%theo=113%`, `AF=19.47`, `y_v=0.169`, dew pt 134 °F,
vapor 0.489) p.811–812 / PDF 829–830; **Ex 13.7** methane heating values
(HHV 890,330 kJ/kmol = 55,507 kJ/kg; LHV 802,310 = 50,019; `h_RP@1000K = −800,552`)
p.826–827 / PDF 844–845. Thermochemical data: **Table A-25** (p.970 / PDF 988).

## See also
`12.2` (dissociation & ionization), `12.EP` (Examples 13.1–13.8, 14.1–14.2),
`12.EQ` (equation registry), `12.HP` (homework).
