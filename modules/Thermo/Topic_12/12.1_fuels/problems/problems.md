# 12.1 — Problems

Check with `code/fuels.py`. Citations in `../refs.md`. Enthalpies `kJ/kmol` (molar) or
`kJ/kg`; molecular weights `kg/kmol`; mole fractions and ratios dimensionless.

### P1.  Theoretical air for methane  *(Moran 8e §13.1.2, Eq. 13.4, p.808)*
Balance `CH₄ + a(O₂ + 3.76N₂) → CO₂ + 2H₂O + dN₂` and give the molar and mass air–fuel
ratios.
*Answer:* `a = a_O₂ = 1 + 4/4 = 2`, `AF̄ = 2·4.76 = 9.52`; `AF = 9.52(28.97/16.04) = 17.2`
kg air/kg fuel. *Check:* `theoretical_air_molar(1,4)` = 9.52; `afr_molar_to_mass(9.52,16.04)`
≈ 17.2.

### P2.  Octane with excess air  *(Moran 8e Ex 13.1, p.809)*
Octane `C₈H₁₈` burns with (a) theoretical air, (b) 150% theoretical air. Find `AF̄`, `AF`,
and the equivalence ratio in (b).
*Answer:* (a) `a_O₂ = 12.5`, `AF̄ = 59.5`, `AF = 15.1`. (b) `AF̄ = 89.25`, `AF = 22.6`,
`φ = 59.5/89.25 = 0.67` (lean). *Check:* `theoretical_air_molar(8,18)` = 59.5;
`equivalence_ratio(89.25, 59.5)` ≈ 0.67.

### P3.  Dew point of products  *(Moran 8e Ex 13.2(c), p.812)*
Methane products contain 20.4 lbmol H₂O per 100 lbmol dry products at 1 atm. Find the
water-vapor mole fraction and its partial pressure (the dew point is `T_sat(p_v)`).
*Answer:* `y_v = 20.4/120.4 = 0.169`, `p_v = 0.169 atm = 2.48 lbf/in²` ⇒ dew point ≈
134 °F (Table A-2E). *Check:* `water_vapor_mole_fraction(20.4,100)` ≈ 0.169;
`dew_point_partial_pressure(0.169, 1.0)` = 0.169.

### P4.  Percent theoretical air from a dry analysis  *(Moran 8e Ex 13.2(b), p.812)*
The methane combustion of P3 has actual `AF̄ = 10.78`. State the percent of theoretical
air.
*Answer:* `% theo = 10.78/9.52 = 1.13 = 113%` (13% excess air). *Check:*
`percent_theoretical_air(10.78, 9.52)` ≈ 1.13; `percent_excess_air(10.78, 9.52)` ≈ 0.13.

### P5.  Heating values of methane  *(Moran 8e Ex 13.7, p.826)*
Using `h°_f` (kJ/kmol): CO₂ −393,520; H₂O(l) −285,830; H₂O(g) −241,820; CH₄(g) −74,850,
find the HHV and LHV of methane (per kmol and per kg).
*Answer:* HHV (liquid water) `= −393,520 + 2(−285,830) − (−74,850) = −890,330 kJ/kmol =
−55,507 kJ/kg`; LHV (vapor) `= −802,310 kJ/kmol = −50,019 kJ/kg`. *Check:*
`enthalpy_of_combustion([(1,-393520,0),(2,-285830,0)], [(1,-74850,0)])` = −890,330;
`heating_value_mass(-890330, 16.04)` ≈ 55,507.

### P6.  Steady-flow energy balance  *(Moran 8e Ex 13.5, Eqs. 13.12b/13.15b, p.819)*
A methane gas-turbine combustor burns CH₄ with 400% theoretical air; products exit at
730 K (`Δh` from Table A-23). With `h̄_R = −74,850` and the product `Δh` terms, find
`h̄_P` and `h̄_P − h̄_R`.
*Answer:* `h̄_P = −359,475 kJ/kmol fuel`, so `h̄_P − h̄_R = −284,625 kJ/kmol` (energy
released per mole of fuel). *Check:*
`stream_enthalpy([(1,-393520,19258),(2,-241820,15314),(6,0,13495),(30.08,0,12860)])`
≈ −359,475.
