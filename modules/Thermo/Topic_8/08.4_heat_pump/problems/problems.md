# 08.4 — Problems

Check with `code/heat_pump.py`. Citations in `../refs.md`. COPs are dimensionless; Carnot
limits need **absolute** temperatures (K).

### P1.  Ideal refrigerator COP, Example 10.1  *(Moran 8e Ex 10.1, Eq. 10.7, p.613)*
An ideal vapor-compression R-134a refrigerator has `h1 = 247.23`, `h2 = 264.7`,
`h3 = h4 = 85.75 kJ/kg`. Find the refrigerator COP `β`.
*Answer:* `β = (h1−h4)/(h2−h1) = (247.23−85.75)/(264.7−247.23) = 9.24`. *Check:*
`cop_ref_from_enthalpies(247.23, 264.7, 85.75)` ≈ 9.24.

### P2.  Carnot ceiling for the same reservoirs  *(Moran 8e Eq. 10.1, p.611)*
The cold region is at `T_C = 273 K` and the warm region at `T_H = 299 K`. Find the maximum
(Carnot) refrigerator COP and compare to P1.
*Answer:* `β_max = T_C/(T_H−T_C) = 273/26 = 10.5 > 9.24`. *Check:*
`carnot_cop_refrigeration(299, 273)` ≈ 10.5.

### P3.  Heat-pump COP, Example 10.4  *(Moran 8e Ex 10.4, Eq. 10.10, p.630)*
An R-134a heat pump has `h1 = 242.54`, `h2 = 280.19`, `h3 = h4 = 105.29 kJ/kg`. Find the
heat-pump COP `γ`.
*Answer:* `γ = (h2−h3)/(h2−h1) = (280.19−105.29)/(280.19−242.54) = 4.65`. *Check:*
`cop_hp_from_enthalpies(242.54, 280.19, 105.29)` ≈ 4.65.

### P4.  The `γ = β + 1` identity  *(Moran 8e Eq. 10.8, p.629)*
For the Example 10.4 cycle, compute the refrigeration COP `β` of the same hardware and
verify `γ = β + 1`.
*Answer:* `β = (h1−h4)/(h2−h1) = (242.54−105.29)/37.65 = 3.645`, so `γ = 4.645 = 3.645 + 1`.
*Check:* `cop_hp_from_enthalpies(242.54,280.19,105.29) − cop_ref_from_enthalpies(242.54,280.19,105.29)` ≈ 1.0.

### P5.  Cycle first law (rates)  *(Moran 8e Eq. 10.8, p.629)*
A heat pump draws `Q̇_C = 27.45 kW` from outside with `Ẇ_net = 7.53 kW` of compressor power.
Find the heating delivered `Q̇_H`.
*Answer:* `Q̇_H = Q̇_C + Ẇ_net = 27.45 + 7.53 = 34.98 kW`. *Check:* `heat_rejected(27.45, 7.53)` ≈ 34.98.
