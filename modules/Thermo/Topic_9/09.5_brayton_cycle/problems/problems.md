# 09.5 — Problems

Check with `code/brayton_cycle.py`. Citations in `../refs.md`. Cold air-standard `k = 1.4`.

### P1.  Efficiency from pressure ratio  *(Moran 8e Eq. 9.25, p.532)*
Find the cold air-standard ideal Brayton efficiency at compressor pressure ratios
`r_p = 6, 10, 20`.
*Answer:* `η = 1 − 1/r_p^(0.4/1.4)` = **0.401, 0.482, 0.575**. Efficiency rises with `r_p`.
*Check:* `brayton_efficiency(6)` ≈ 0.401, `brayton_efficiency(10)` ≈ 0.482,
`brayton_efficiency(20)` ≈ 0.575.

### P2.  Ideal cycle, Example 9.4  *(Moran 8e Ex 9.4, Eqs. 9.15–9.20, p.529)*
Air enters the compressor of an ideal Brayton cycle at 100 kPa, 300 K; `r_p = 10`;
turbine inlet `T₃ = 1400 K`. Table A-22 gives `h₁ = 300.19`, `h₂ = 579.9`, `h₃ = 1515.4`,
`h₄ = 808.5 kJ/kg`. Find `η` and the back work ratio.
*Answer:* `w_t = 706.9`, `w_c = 279.7`, `q_in = 935.5 kJ/kg`;
`η = (706.9−279.7)/935.5 = 0.457`; `bwr = 279.7/706.9 = 0.396` — the compressor eats
~40% of the turbine output. *Check:* `brayton_efficiency_air_table(300.19, 579.9, 1515.4, 808.5)` ≈ 0.457;
`back_work_ratio(...)` ≈ 0.396.

### P3.  Cold air-standard states  *(Moran 8e Eqs. 9.23–9.24, p.529)*
For the cycle of P2 on a cold air-standard basis, find `T₂` and `T₄` and compare `η`.
*Answer:* `T₂ = 300·10^(0.4/1.4) = 579.2 K`; `T₄ = 1400/10^(0.4/1.4) = 725.1 K`;
`η = 0.482 > 0.457` — constant specific heats overpredict (Ex 9.4 comparison table).
*Check:* `temp_after_isentropic_compression(300, 10)` ≈ 579.2;
`temp_after_isentropic_expansion(1400, 10)` ≈ 725.1.

### P4.  Irreversible turbomachines, Example 9.6  *(Moran 8e Ex 9.6, §9.6.3, p.535)*
Repeat P2 with `η_t = η_c = 0.80`. Find `η` and `bwr`.
*Answer:* `w_t = 0.8·706.9 = 565.5`; `w_c = 279.7/0.8 = 349.6`; `h₂ = 649.8`;
`q_in = 865.6 kJ/kg`; `η = (565.5−349.6)/865.6 = 0.249`; `bwr = 0.618`. Irreversibility
cuts the efficiency nearly in half because the back work ratio is so large. *Check:*
`turbine_work_actual(706.9, 0.8)` = 565.5; `compressor_work_actual(279.7, 0.8)` ≈ 349.6.

### P5.  Regeneration, Example 9.7  *(Moran 8e Ex 9.7, Eqs. 9.26–9.27, p.539)*
A regenerator with effectiveness 80% is added to the ideal cycle of P2. Find `h_x` and
the new `η`.
*Answer:* `h_x = 579.9 + 0.8(808.5−579.9) = 762.8 kJ/kg`; `q_in = 1515.4 − 762.8 =
752.6 kJ/kg`; net work is unchanged, so `η = 427.2/752.6 = 0.568` (up from 0.457). At
`η_reg = 1` it would reach 0.604. *Check:* `regenerator_exit_enthalpy(579.9, 808.5, 0.8)`
≈ 762.8; `heat_added_regenerative(762.8, 1515.4)` ≈ 752.6.

### P6.  Best pressure ratio for net work  *(Moran 8e Ex 9.5, p.534)*
For fixed `T₁ = 300 K` and `T₃ = 1700 K` (cold air-standard), what pressure ratio
maximizes net work per unit of mass flow? Is that the best-efficiency ratio?
*Answer:* `r_p* = (1700/300)^(1.4/0.8) ≈ 21` (Fig. 9.12). No — `η` keeps rising with
`r_p`, so vehicle engines run near `r_p*` for compactness, not peak efficiency. *Check:*
`pressure_ratio_max_work(300, 1700)` ≈ 20.8; `brayton_efficiency(30) > brayton_efficiency(21)`.
