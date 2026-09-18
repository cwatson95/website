# 09.5 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| air-standard gas turbine, cycle description | §9.5 *Modeling Gas Turbine Power Plants* / §9.6 *Air-Standard Brayton Cycle* | — | 526–527 | 544–545 |
| turbine work `Ẇ_t/ṁ = h₃−h₄` (`turbine_work`) | §9.6.1 *Evaluating Principal Work and Heat Transfers* | **9.15** | 527 | 545 |
| compressor work `Ẇ_c/ṁ = h₂−h₁` (`compressor_work`) | §9.6.1 | **9.16** | 527 | 545 |
| heat added `Q̇_in/ṁ = h₃−h₂` (`heat_added`) | §9.6.1 | **9.17** | 527 | 545 |
| heat rejected `Q̇_out/ṁ = h₄−h₁` (`heat_rejected`) | §9.6.1 | **9.18** | 528 | 546 |
| efficiency, air-table (`brayton_efficiency_air_table`) | §9.6.1 | **9.19** | 528 | 546 |
| back work ratio, 40–80% (`back_work_ratio`) | §9.6.1 | **9.20** | 528 | 546 |
| isentropic legs `p_r2=p_r1·r_p`, `p_r4=p_r3/r_p` (`pr_after_*`) | §9.6.2 *Ideal Air-Standard Brayton Cycle* | **9.21, 9.22** | 529 | 547 |
| cold-air temperatures `T₂`, `T₄` (`temp_after_*`) | §9.6.2 | **9.23, 9.24** | 529 | 547 |
| efficiency, cold air-standard `η=1−1/r_p^((k−1)/k)` (`brayton_efficiency`) | §9.6.2 *Effect of Compressor Pressure Ratio* | **9.25** | 532 | 550 |
| max-net-work pressure ratio (`pressure_ratio_max_work`) | Ex 9.5, Eq. (a) | — | 534 | 552 |
| isentropic η_t, η_c applied to the cycle (`*_work_actual`) | §9.6.3 *Considering Gas Turbine Irreversibilities and Losses* | (6.46, 6.48) | 535 | 553 |
| regenerative heat addition `Q̇_in/ṁ = h₃−h_x` (`heat_added_regenerative`) | §9.7 *Regenerative Gas Turbines* | **9.26** | 538 | 556 |
| regenerator effectiveness (`regenerator_effectiveness`) | §9.7 | **9.27** | 539 | 557 |

## Worked Examples used
| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| **9.4** | Analyzing the Ideal Brayton Cycle (η=0.457, bwr=0.396, 2481 kW; cold 0.482/0.414) | 529–531 | 547–549 |
| **9.5** | Determining Compressor Pressure Ratio for Maximum Net Work (r_p*=(T₃/T₁)^(k/2(k−1)) ≈ 21) | 533–534 | 551–552 |
| **9.6** | Evaluating Performance of a Brayton Cycle with Irreversibilities (η_t=η_c=0.8; η=0.249, bwr=0.618, 1254 kW) | 535–537 | 553–555 |
| **9.7** | Evaluating Thermal Efficiency of a Brayton Cycle with Regeneration (η_reg=0.8; h_x=762.8, η=0.568) | 539–541 | 557–559 |

Ex 9.4's air-table enthalpies (h₁=300.19, h₂=579.9, h₃=1515.4, h₄=808.5 kJ/kg) and its
cold air-standard comparison column (T₂=579.2 K, T₄=725.1 K, η=0.482, bwr=0.414,
2308 kW) are read from the book (p.530–531). Quick-Quiz values: Q̇_in=5432 kW (Ex 9.4),
η=16.8%/bwr=70.65% at η_t=0.70 (Ex 9.6), η=60.4% at η_reg=1 (Ex 9.7). Cold-air `k=1.4`
per Table A-20.

## See also
`09.1` (Carnot ceiling), `09.2`–`09.4` (piston cycles — compression ratio, not pressure
ratio), `09.6` (Rankine — bwr ~1%), `10.2` (Stirling — same Eq. 9.27 regenerator),
`07.1` (η_t/η_c definitions), Topic 5 (air tables), `9.EQ`/`9.EP`/`9.HP`.
