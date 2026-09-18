# 7.EQ — Topic 7: List of Equations (Performance Metrics)

The defining equations of **Topic 7** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks that
the concept module (`07.1`) reproduces them. Citations are Moran 8e (printed pages; PDF =
printed + 18; `refs.md`).

## Thermal efficiency — power cycle (Ch. 2 §2.6.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 2.42 | `η = W_cycle/Q_in` | `thermal_efficiency` | §2.6.2, p.74 |
| 2.43 | `η = 1 − Q_out/Q_in` | `thermal_efficiency_alt` | §2.6.2, p.74 |

## Coefficients of performance (Ch. 2 §2.6.3)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 2.45 | `β = Q_C/W_cycle` | `cop_refrigerator` | §2.6.3, p.75 |
| 2.47 | `γ = Q_H/W_cycle`  (`γ = β + 1`) | `cop_heat_pump` | §2.6.3, p.75 |

## Carnot ceilings — two reservoirs (Ch. 5 §5.9)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 5.9 | `η_max = 1 − T_C/T_H` | `carnot_efficiency` | §5.9.1, p.265 |
| 5.10 | `β_max = T_C/(T_H−T_C)` | `carnot_cop_refrigerator` | §5.9.2, p.267 |
| 5.11 | `γ_max = T_H/(T_H−T_C)` | `carnot_cop_heat_pump` | §5.9.2, p.267 |

## Isentropic (device) efficiencies (Ch. 6 §6.12)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 6.46 | `η_t = (h1−h2)/(h1−h2s)` | `isentropic_turbine_efficiency` | §6.12.1, p.333 |
| 6.47 | `η_n = (V₂²/2)/(V₂²/2)_s` | `isentropic_nozzle_efficiency` | §6.12.2, p.335 |
| 6.48 | `η_c = (h2s−h1)/(h2−h1)` | `isentropic_compressor_efficiency` | §6.12.3, p.338 |

> `python3 code/test_equations.py` → 10 value checks + 10 cross-module checks =
> `"All 20 tests passed."`
