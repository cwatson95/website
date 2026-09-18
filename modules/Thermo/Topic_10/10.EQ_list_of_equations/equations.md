# 10.EQ — Topic 10: List of Equations (Engines)

The defining equations of **Topic 10** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks that
BOTH concept modules (`10.1` Carnot, `10.2` Stirling) reproduce them. Citations are Moran
8e (printed pages; PDF = printed + 18; `refs.md`).

## Carnot ceilings — two reservoirs (Ch. 5 §5.9)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 5.9 | `η_max = 1 − T_C/T_H` | `carnot_efficiency` | §5.9.1, p.265 |
| 5.10 | `β_max = T_C/(T_H−T_C)` | `carnot_cop_refrigerator` | §5.9.2, p.267 |
| 5.11 | `γ_max = T_H/(T_H−T_C)`  (`γ_max = β_max + 1`) | `carnot_cop_heat_pump` | §5.9.2, p.267 |

## Kelvin-scale ratio (Ch. 5 §5.7)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 5.7 | `(Q_C/Q_H)_rev = T_C/T_H` | `kelvin_heat_ratio` | §5.7, p.262 |

## Isothermal ideal-gas heat/work (Ch. 2 §2.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 2.17 | `Q = W = R T ln(V₂/V₁)` per unit mass (from `W = ∫p dV` with `pV = mRT`, `du = 0`) | `isothermal_heat` | §2.2.3, p.48–49 |

## Stirling cycle & regeneration (Ch. 9 §9.8.4, §9.7)
| Eq. | form | function | source |
|-----|------|----------|--------|
| — | `η = 1 − T_C/T_H` (ideal Stirling **= Carnot** ceiling) | `stirling_efficiency` | §9.8.4, p.552–553 |
| (3.50) | `Q_regen = c_v (T_H − T_C)` (constant-volume legs) | `regenerator_heat` | §9.8.4, p.552 / §3.14.2, p.140 |
| 9.27 | `η_reg = (h_x−h_2)/(h_4−h_2)` | `regenerator_effectiveness` | §9.7, p.539 |

**Coexistence.** Eqs. 5.9–5.11 are also registered in `3.EQ` (second law) and `7.EQ`
(performance metrics) with the same citations — each topic carries its own canonical copy
and cross-checks its own concept modules; here they cross-check the *engines* (`10.1`,
`10.2`). The Stirling row makes the shared ceiling explicit: the ideal Stirling efficiency
**is** the Eq. 5.9 expression (Moran §9.8.4, p.553). `T` absolute (K/°R).

> `python3 code/test_equations.py` → 14 value checks + 14 cross-module checks =
> `"All 28 tests passed."`
