# 9.EQ — Topic 9: List of Equations (Power & Refrigeration Cycles)

The defining equations of **Topic 9** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks
that all six concept modules (`09.1`–`09.6`) reproduce them. Citations are Moran 8e
(printed pages; PDF = printed + 18; `refs.md`).

## Carnot ceiling & engine terminology (Ch. 5, §9.1)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 5.9 | `η_max = 1 − T_C/T_H` | `carnot_efficiency` | §5.9.1, p.265 |
| 9.1 | `mep = W_cycle/(V₁−V₂)` | `mean_effective_pressure` | §9.1, p.511 |

## Otto cycle (§9.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 9.3 | `η = 1 − (u₄−u₁)/(u₃−u₂)` | `otto_efficiency_air_table` | §9.2, p.514 |
| 9.6 | `T₂ = T₁ r^(k−1)` | `otto_temp_after_compression` | §9.2, p.514 |
| 9.7 | `T₄ = T₃/r^(k−1)` | `otto_temp_after_expansion` | §9.2, p.514 |
| 9.8 | `η = 1 − 1/r^(k−1)` | `otto_efficiency` | §9.2, p.515 |

## Diesel cycle (§9.3)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 9.11 | `η = 1 − (u₄−u₁)/(h₃−h₂)` | `diesel_efficiency_air_table` | §9.3, p.519 |
| 9.13 | `η = 1 − (1/r^(k−1))·(r_c^k−1)/(k(r_c−1))` | `diesel_efficiency` | §9.3, p.519 |

## Dual cycle (§9.4)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 9.14 | `η = 1 − (u₅−u₁)/[(u₃−u₂)+(h₄−h₃)]` | `dual_efficiency_air_table` | §9.4, p.523 |
| — | `η = 1 − (1/r^(k−1))·(r_p r_c^k−1)/[(r_p−1)+k r_p(r_c−1)]` (→ Otto as r_c→1, Diesel as r_p→1) | `dual_efficiency` | §9.4, p.523 |

## Brayton cycle (§9.6–9.7)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 9.15 | `Ẇ_t/ṁ = h₃−h₄` | `brayton_turbine_work` | §9.6.1, p.527 |
| 9.16 | `Ẇ_c/ṁ = h₂−h₁` | `brayton_compressor_work` | §9.6.1, p.527 |
| 9.17 | `Q̇_in/ṁ = h₃−h₂` | `brayton_heat_added` | §9.6.1, p.527 |
| 9.18 | `Q̇_out/ṁ = h₄−h₁` | `brayton_heat_rejected` | §9.6.1, p.528 |
| 9.19 | `η = [(h₃−h₄)−(h₂−h₁)]/(h₃−h₂)` | `brayton_efficiency_air_table` | §9.6.1, p.528 |
| 9.20 | `bwr = (h₂−h₁)/(h₃−h₄)` (40–80%) | `brayton_back_work_ratio` | §9.6.1, p.528 |
| 9.23 | `T₂ = T₁ r_p^((k−1)/k)` | `brayton_temp_after_compression` | §9.6.2, p.529 |
| 9.24 | `T₄ = T₃ (1/r_p)^((k−1)/k)` | `brayton_temp_after_expansion` | §9.6.2, p.529 |
| 9.25 | `η = 1 − 1/r_p^((k−1)/k)` | `brayton_efficiency` | §9.6.2, p.532 |
| 9.27 | `η_reg = (h_x−h₂)/(h₄−h₂)` | `regenerator_effectiveness` | §9.7, p.539 |

## Rankine cycle (§8.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 8.1 | `Ẇ_t/ṁ = h₁−h₂` | `rankine_turbine_work` | §8.2.1, p.446 |
| 8.2 | `Q̇_out/ṁ = h₂−h₃` | `rankine_condenser_heat` | §8.2.1, p.447 |
| 8.3 | `Ẇ_p/ṁ = h₄−h₃` | `rankine_pump_work` | §8.2.1, p.447 |
| 8.4 | `Q̇_in/ṁ = h₁−h₄` | `rankine_boiler_heat` | §8.2.1, p.447 |
| 8.5a | `η = [(h₁−h₂)−(h₄−h₃)]/(h₁−h₄)` | `rankine_efficiency` | §8.2.1, p.447 |
| 8.6 | `bwr = (h₄−h₃)/(h₁−h₂)` (~1–2%) | `rankine_back_work_ratio` | §8.2.1, p.447 |
| 8.7b | `(Ẇ_p/ṁ)_s ≈ v₃(p₄−p₃)` | `rankine_pump_work_approx` | §8.2.2, p.449 |

> `python3 code/test_equations.py` → 27 value checks + 33 cross-module checks =
> `"All 60 tests passed."` (The cross-checks import 09.1–09.6 and assert each computes
> the same formula, including that the dual closed form reduces to the Otto and Diesel
> modules' forms and that every cycle sits below the 09.1 Carnot ceiling.)
