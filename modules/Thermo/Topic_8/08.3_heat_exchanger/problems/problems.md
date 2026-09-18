# 08.3 — Problems

Check with `code/heat_exchanger.py`. Citations in `../refs.md`. `h` [kJ/kg], `c` [kJ/kg·K],
`T` [K or °C consistently], `ṁ` [kg/s].

### P1.  Mass-flow ratio in a condenser (Ex 4.7)  *(Moran 8e §4.9.2, p.197)*
Condensing steam goes from `h_hi = 2465.1` to `h_ho = 188.45 kJ/kg`; cooling water rises
by `h_co − h_ci = 62.7 kJ/kg`. Find `ṁ_water/ṁ_steam`.
*Answer:* `ṁ_c/ṁ_h = (2465.1−188.45)/62.7 = 36.3`. *Check:*
`mass_flow_ratio_cold_to_hot(2465.1, 188.45, 0, 62.7)` ≈ 36.3.

### P2.  Cooling-water flow rate  *(Moran 8e Ex 4.7 Quick Quiz, p.198)*
If the condensing steam flows at `ṁ_steam = 125 kg/s`, find the cooling-water flow.
*Answer:* `ṁ_water = ṁ_steam(h_hi−h_ho)/(h_co−h_ci) = 125 × 36.3 ≈ 4538 kg/s`. *Check:*
`mass_flow_other(125, 2465.1−188.45, 62.7)` ≈ 4538.

### P3.  Energy balance closes  *(Moran 8e Eq. 4.18, p.196)*
Verify that, with `Q̇cv = Ẇcv = 0`, the whole-exchanger balance is satisfied for P1's
ratio (take `ṁ_h = 1`, `ṁ_c = 36.3`).
*Answer:* `ṁ_h(h_hi−h_ho) + ṁ_c(h_ci−h_co) = 1(2276.65) + 36.3(−62.7) ≈ 0`. *Check:*
`energy_balance_residual(1, 2465.1, 188.45, 36.31, 0, 62.7)` ≈ 0.

### P4.  Oil-cooled-by-water (constant cp)  *(Moran 8e §3.13.2, p.130)*
Oil (`c = 2 kJ/kg·K`) enters at 450 K and leaves at 350 K with `ṁ_oil = 10 kg/s`. Cooling
water (`c = 4.18 kJ/kg·K`) enters at 20 °C and leaves at 60 °C. Find the water flow rate
(adiabatic device).
*Answer:* hot duty `= 10·2·(450−350) = 2000 kW`; water `Δh = 4.18·40 = 167.2 kJ/kg`, so
`ṁ_water = 2000/167.2 = 11.96 kg/s`. *Check:* `mass_flow_other(10, 200, 167.2)` ≈ 11.96.
