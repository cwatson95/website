# 09.6 — Problems

Check with `code/rankine_cycle.py`. Citations in `../refs.md`. Steam states: Tables
A-2/A-3/A-4 (`../../steam_tables/`), values as Moran quotes them.

### P1.  Ideal Rankine cycle, Example 8.1  *(Moran 8e Ex 8.1, Eqs. 8.1–8.6, p.450)*
Saturated vapor enters the turbine at 8.0 MPa (`h₁ = 2758.0`, `s₁ = 5.7432`); saturated
liquid leaves the condenser at 0.008 MPa (`s_f = 0.5926`, `s_g = 8.2287`, `h_f = 173.88`,
`h_fg = 2403.1`). Find `x₂`, `h₂`, and `η`.
*Answer:* `x₂ = (5.7432−0.5926)/7.6361 = 0.6745`; `h₂ = 173.88 + 0.6745·2403.1 =
1794.8 kJ/kg`; with `h₄ = 181.94`, `η = (963.2−8.06)/2576.06 = 0.371` (37.1%). *Check:*
`quality_from_entropy(5.7432, 0.5926, 8.2287)` ≈ 0.6745;
`rankine_efficiency(2758.0, 1794.8, 173.88, 181.94)` ≈ 0.371.

### P2.  Pump work and back work ratio  *(Moran 8e Eqs. 8.7b, 8.6, p.449, 447)*
For the cycle of P1, `v₃ = 1.0084×10⁻³ m³/kg`. Approximate the pump work and the bwr.
*Answer:* `w_p ≈ v₃(p₄−p₃) = 1.0084×10⁻³·(8000−8) = 8.06 kJ/kg`;
`bwr = 8.06/963.2 = 8.37×10⁻³` — under 1%, vs ~40% for the Brayton compressor (09.5).
*Check:* `pump_work_approx(1.0084e-3, 8.0, 8000.0)` ≈ 8.06;
`back_work_ratio(2758.0, 1794.8, 173.88, 181.94)` ≈ 0.00837.

### P3.  Mass flow and heat rates  *(Moran 8e Ex 8.1(c)–(f), p.451–452)*
The cycle of P1 delivers 100 MW net. Find `ṁ`, `Q̇_in`, `Q̇_out`, and the cooling-water
flow for a 15→35 °C rise (`h_f = 62.99, 146.68 kJ/kg`).
*Answer:* `ṁ = 100×10³·3600/955.14 = 3.77×10⁵ kg/h`; `Q̇_in = 269.77 MW`;
`Q̇_out = 169.75 MW` (62.9% of the input is rejected); `ṁ_cw = 169.75×10³·3600/83.69 =
7.3×10⁶ kg/h`. *Check:* `boiler_heat(181.94, 2758.0)·3.77e5/3600/1e3` ≈ 269.77.

### P4.  Irreversibilities, Example 8.2  *(Moran 8e Ex 8.2, Eqs. 8.9–8.10, p.456)*
Repeat P1 with `η_t = η_p = 0.85`. Find `h₂`, `w_p`, and `η`.
*Answer:* `h₂ = 2758 − 0.85(963.2) = 1939.3 kJ/kg`; `w_p = 8.06/0.85 = 9.48 kJ/kg`
(`h₄ = 183.36`); `η = (818.7−9.48)/2574.64 = 0.314` — the turbine loss dominates.
*Check:* `turbine_exit_actual(2758.0, 1794.8, 0.85)` ≈ 1939.3;
`pump_work_actual(8.06, 0.85)` ≈ 9.48.

### P5.  Superheat + reheat, Example 8.3  *(Moran 8e Ex 8.3, §8.3, p.461)*
Steam at 8.0 MPa, 480 °C (`h₁ = 3348.4`, `s₁ = 6.6586`) expands to 0.7 MPa
(`s_f = 1.9922`, `s_g = 6.708`, `h_f = 697.22`, `h_fg = 2066.3`), is reheated to 440 °C
(`h₃ = 3353.3`, `s₃ = 7.7571`), then expands to 0.008 MPa. Find the exit qualities and `η`.
*Answer:* `x₂ = 0.9895` (`h₂ = 2741.8`); `x₄ = 0.9382 > 0.9` (`h₄ = 2428.5`) — reheat
keeps the exhaust dry; `η = 1523.3/3778 = 0.403`, up from 0.371. *Check:*
`reheat_efficiency(3348.4, 2741.8, 3353.3, 2428.5, 173.88, 181.94)` ≈ 0.403.

### P6.  Carnot comparison  *(Moran 8e §8.2.3, Eq. 8.8, p.453–454; cross-ref `09.1`)*
The cycle of P1 runs between saturation temperatures 295.1 °C (8.0 MPa) and 41.51 °C
(0.008 MPa). Compare `η = 0.371` with the Carnot ceiling, and state the Eq. 8.8 trends.
*Answer:* `η_max = 1 − 314.66/568.25 = 0.446 > 0.371` — heat addition along the
feedwater ramp lowers `T̄_in` below `T_H`. Raising boiler pressure (higher `T̄_in`) or
lowering condenser pressure (lower `T_out`) raises `η`. *Check (in `09.1`):*
`carnot_efficiency(314.66, 568.25)` ≈ 0.446; `ideal_efficiency_avg_temps(568.25, 314.66)` ≈ 0.446.
