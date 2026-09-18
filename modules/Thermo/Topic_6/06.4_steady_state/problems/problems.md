# 6.4 — Problems

Check with `code/steady_state.py`. Citations in `../refs.md`. `Q̇,Ẇ` [kW], `ṁ` [kg/s],
`h` [kJ/kg], `V` [m/s].

### P1.  Steam turbine, steady state (Ex 4.4)  *(Moran 8e §4.7.2, p.188–189)*
Steam enters at `ṁ = 4600 kg/h`, `h₁ = 3177.2 kJ/kg`, `V₁ = 10 m/s`; the turbine
develops `Ẇcv = 1000 kW`. Exit: `h₂ = 2345.4 kJ/kg`, `V₂ = 30 m/s` (`ΔPE ≈ 0`). Find
the heat-transfer rate `Q̇cv`.
*Answer:* `ΔKE = (30²−10²)/2 = 0.4 kJ/kg`; `Q̇cv = Ẇcv + ṁ[(h₂−h₁)+ΔKE] =
1000 + (4600/3600)(−831.4) = −62.3 kW` (heat *from* the turbine). *Check:*
`heat_rate_steady(1000, 4600/3600, 3177.2, 2345.4, V1=10, V2=30)` ≈ −62.3.

### P2.  Does KE matter? (Ex 4.4 Quick Quiz)  *(Moran 8e §4.7.2, p.189)*
Repeat P1 neglecting the kinetic-energy change. Compare.
*Answer:* `Q̇cv = 1000 + (4600/3600)(−831.8) = −62.9 kW` — only 0.6 kW different; KE is
negligible here. *Check:* `heat_rate_steady(1000, 4600/3600, 3177.2, 2345.4)` ≈ −62.9.

### P3.  Steam turbine power (HW 4.42)  *(Moran 8e §4, p.223)*
Steam enters a well-insulated turbine at `h₁ = 3015.4 kJ/kg`, `V₁ = 10 m/s` and exits at
`h₂ = 2431.7 kJ/kg`, `V₂ = 90 m/s`; `ṁ = 11.95 kg/s` (`ΔPE ≈ 0`). Find the power.
*Answer:* well-insulated ⇒ `Q̇ = 0`; `ΔKE = (10²−90²)/2 = −4.0 kJ/kg`;
`Ẇcv = ṁ[(h₁−h₂)+ΔKE] = 11.95(583.7−4.0) = 6927 kW`. *Check:*
`power_rate_steady(0, 11.95, 3015.4, 2431.7, V1=10, V2=90)` ≈ 6927.

### P4.  Air nozzle — area and heat transfer (HW 4.34)  *(Moran 8e §4, p.223)*
Air (`R = 0.287`, `cp = 1.011 kJ/kg·K`) enters a horizontal nozzle at `ṁ = 2.3 kg/s`,
450 K, 350 kPa, `V₁ = 3 m/s`, and exits at 300 K, `V₂ = 460 m/s`. Find inlet area `A₁`
and the heat-transfer rate.
*Answer:* `v₁ = RT₁/p₁ = 0.369 m³/kg`, `A₁ = ṁv₁/V₁ = 0.283 m²`. `ΔKE =
(460²−3²)/2 = 105.8 kJ/kg`; `Q̇ = ṁ[cp(T₂−T₁)+ΔKE] = 2.3(−151.65+105.8) = −105.5 kW`
(heat *from* the air). *Check:* `heat_rate_steady` with `h₂−h₁ → cp(T₂−T₁)`:
`heat_rate_steady(0, 2.3, 1.011*450, 1.011*300, V1=3, V2=460)` ≈ −105.5.
