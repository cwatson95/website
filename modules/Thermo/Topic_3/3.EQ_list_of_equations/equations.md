# 3.EQ — Topic 3: List of Equations (The Laws)

The defining equations of **Topic 3** in canonical Moran 8e form. Each is a function
in `code/equations.py`; `code/test_equations.py` checks every value **and**
cross-checks that the concept modules (3.1–3.4) reproduce them. Citations are Moran
8e (printed pages; PDF = printed + 18; `refs.md`).

## Zeroth law — temperature (Ch. 1 §1.7)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 1.16 | `T_R = 1.8 T_K` | `rankine_from_kelvin` | §1.7.2, p.21 |
| 1.17 | `T_C = T_K − 273.15` | `celsius_from_kelvin` | §1.7.3, p.22 |
| 1.19 | `T_F = 1.8 T_C + 32` | `fahrenheit_from_celsius` | §1.7.3, p.22 |

## First law — energy balance (Ch. 2 §2.5–2.6)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 2.35a | `E₂−E₁ = Q − W` | `delta_E` | §2.5, p.61 |
| 2.41 | `W_cycle = Q_in − Q_out` | `power_cycle_work` | §2.6, p.73 |

## Second law — Carnot bounds (Ch. 5 §5.4–5.9)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 5.4 | `η = 1 − Q_C/Q_H` | `efficiency_from_heat` | §5.4, p.256 |
| 5.7 | `(Q_C/Q_H)_rev = T_C/T_H` | `kelvin_ratio` | §5.7, p.262 |
| 5.9 | `η_max = 1 − T_C/T_H` | `carnot_efficiency` | §5.9.1, p.265 |
| 5.10 | `β_max = T_C/(T_H−T_C)` | `carnot_cop_refrigerator` | §5.9.2, p.267 |
| 5.11 | `γ_max = T_H/(T_H−T_C)` | `carnot_cop_heat_pump` | §5.9.2, p.267 |

## Third law — entropy datum (Ch. 13 §13.5)
| Eq. | form | function | source |
|-----|------|----------|--------|
| — | `S(0 K) = 0` (pure crystal) | `standard_entropy_at_zero` | §13.5.1, p.837 |
| — | `S(T) = a T³/3` (Debye `c_p=aT³`) | `absolute_entropy_debye` | §13.5, p.837 |

> `python3 code/test_equations.py` → 13 value checks + 12 cross-module checks =
> `"All 25 tests passed."`
