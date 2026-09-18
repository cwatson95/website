# 09.4 — Problems

Check with `code/dual_cycle.py`. Citations in `../refs.md`. Cold air-standard `k = 1.4`.

### P1.  Air-table efficiency, Example 9.3  *(Moran 8e Ex 9.3, Eq. 9.14, p.523)*
A dual cycle has `r = 18`, `r_p = 1.5`, `r_c = 1.2`, `T₁ = 300 K`. Air-table properties:
`u₁ = 214.07`, `u₂ = 673.2`, `u₃ = 1065.8`, `h₃ = 1452.6`, `h₄ = 1778.3`, `u₅ = 475.96 kJ/kg`.
Find `η`.
*Answer:* `η = 1 − (475.96−214.07)/[(1065.8−673.2)+(1778.3−1452.6)] = 0.635` (63.5%).
*Check:* `dual_efficiency_air_table(214.07, 673.2, 1065.8, 1452.6, 1778.3, 475.96)` ≈ 0.635.

### P2.  Net work and mep, Example 9.3  *(Moran 8e Ex 9.3, p.524)*
For the same cycle with `v₁ = 0.861 m³/kg`, find the net work per unit mass and the mean
effective pressure.
*Answer:* `w_net = (u₃−u₂)+(h₄−h₃)−(u₅−u₁) = 392.6 + 325.7 − 261.89 = 456.4 kJ/kg`;
`mep = w_net/[v₁(1−1/r)] = 456.4/[0.861(1−1/18)] = 561 kPa ≈ 0.56 MPa`. *Check:*
`mean_effective_pressure(456.4, 0.861, 18)` ≈ 561.3 kPa.

### P3.  Otto limit `r_c → 1`  *(Moran 8e Eq. 9.14 → 9.8, p.523)*
Show that with no constant-pressure burn the dual cycle reduces to Otto at the same `r`.
*Answer:* As `r_c → 1`, `dual_efficiency(18, 1.5, 1+ε) → 1 − 1/18^0.4 = 0.6853` = Otto.
*Check:* `dual_efficiency(18, 1.5, 1.000000001)` ≈ `1 − 1/18**0.4` ≈ 0.6853.

### P4.  Diesel limit `r_p → 1`  *(Moran 8e Eq. 9.14 → 9.13, p.523)*
Show that with no constant-volume burn the dual cycle reduces to Diesel at the same `r`.
*Answer:* As `r_p → 1`, `dual_efficiency(18, 1+ε, 2) → 1 − (1/18^0.4)(2^1.4−1)/(1.4·1) = 0.6316`
= Diesel. *Check:* `dual_efficiency(18, 1.000000001, 2)` ≈ 0.6316.

### P5.  State temperatures (cold air-standard)  *(Moran 8e §9.4, p.523–524)*
For `r = 18`, `r_p = 1.5`, `r_c = 1.2`, `T₁ = 300 K`, find `T₂`–`T₅` on the cold air-standard.
*Answer:* `T₂ = 300·18^0.4 = 953.3 K`; `T₃ = r_p T₂ = 1430.0 K`; `T₄ = r_c T₃ = 1715.9 K`;
`T₅ = T₄(r_c/r)^0.4 = 580.9 K`. (Cold-air values run above the book's air-table 898.3/1347.5/1617 K
because constant `c_p` overpredicts temperatures.) *Check:*
`temp_after_isentropic_compression(300,18)` ≈ 953.3;
`temp_after_constant_volume_heat(953.3,1.5)` ≈ 1430.0;
`temp_after_constant_pressure_heat(1430.0,1.2)` ≈ 1715.9;
`temp_after_isentropic_expansion(1715.9,18,1.2)` ≈ 580.9.
