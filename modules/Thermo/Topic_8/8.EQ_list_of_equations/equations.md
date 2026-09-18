# 8.EQ — Topic 8: List of Equations (Components & Devices)

The defining equations of **Topic 8** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks that
all four concept modules (`08.1`–`08.4`) reproduce them. Citations are Moran 8e (printed
pages; PDF = printed + 18; `refs.md`).

## Mass flow (Ch. 4 §4.2.1)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 4.4b | `ṁ = A·V/v` | `mass_flow_rate` | §4.2.1, p.172 |
| 4.4b | `ṁ = A·V·p/(R·T)` (ideal gas) | `mass_flow_rate_ideal_gas` | Ex 4.5, p.191 |

## Steady CV energy balance & device forms (Ch. 4 §4.5, §4.8, §4.9)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 4.20a | `Ẇcv = Q̇cv + ṁ[(h1−h2)+(V1²−V2²)/2+g(z1−z2)]` | `power_cv` | §4.5.1, p.181 |
| 4.20a | compressor: `Ẇcv = ṁ(h1−h2)` (< 0) | `compressor_power` | §4.8.1, p.190 |
| 4.20a | condenser / one stream: `Q̇cv = ṁ(h_out−h_in)` | `single_stream_heat_rate` | Ex 4.7(b), p.198 |
| 4.18 | exchanger: `0 = ṁ_h(h_hi−h_ho) + ṁ_c(h_ci−h_co)` | `two_stream_balance_residual` | §4.5.1, p.181 |
| 4.18 | `ṁ_c/ṁ_h = (h_hi−h_ho)/(h_co−h_ci)` | `mass_flow_ratio_cold_to_hot` | Ex 4.7(a), p.197 |

## Isentropic compressor efficiency (Ch. 6 §6.12.3)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 6.48 | `η_c = (h2s−h1)/(h2−h1)` | `isentropic_compressor_efficiency` | §6.12.3, p.338 |

## Vapor-compression cycle (Ch. 10; states 1→2 compressor, 2→3 condenser, 3→4 valve, 4→1 evaporator)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 10.3 | `Q̇in/ṁ = h1−h4` (refrigeration capacity) | `refrigeration_capacity_per_mass` | §10.2.1, p.612 |
| 10.4 | `Ẇc/ṁ = h2−h1` | `vc_compressor_work_per_mass` | §10.2.1, p.613 |
| 10.5 | `Q̇out/ṁ = h2−h3` | `vc_condenser_heat_per_mass` | §10.2.1, p.613 |
| 10.6 | `h4 = h3` (throttling valve) | `throttling_exit_enthalpy` | §10.2.1, p.613 |
| 10.7 | `β = (h1−h4)/(h2−h1)` | `cop_refrigeration_vc` | §10.2.1, p.613 |
| 10.8 | `Q̇out = Q̇in + Ẇnet` | `heat_pump_first_law` | §10.6.1, p.629 |
| 10.1 | `β_max = T_C/(T_H−T_C)` | `carnot_cop_refrigeration` | §10.1.1, p.611 |
| 10.9 | `γ_max = T_H/(T_H−T_C)` | `carnot_cop_heat_pump` | §10.6.1, p.629 |
| 10.10 | `γ = (h2−h3)/(h2−h1)` (`γ = β + 1`) | `cop_heat_pump_vc` | §10.6.2, p.630 |

**Units.** `power_cv` is strict SI (`h` [J/kg], `V` [m/s], `Q̇`/`Ẇ` [W]); the
enthalpy-difference forms take any consistent energy unit (kJ/kg is fine); the Carnot
limits need absolute temperature (K).

> `python3 code/test_equations.py` → 18 value checks + 18 cross-module checks =
> `"All 36 tests passed."`
