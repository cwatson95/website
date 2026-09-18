# 11.EQ — Topic 11: List of Equations (Psychrometrics — Moist Air)

The defining equations of **Topic 11** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks
that the concept modules (11.1 dry-bulb, 11.2 wet-bulb) reproduce them. Citations are
Moran 8e Ch.12 (printed pages; PDF = printed + 18; `refs.md`).

## Composition (Moran §12.5.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 12.42 | `ω = mv/ma` | `humidity_ratio` | §12.5.2, p.754 |
| 12.43 | `ω = 0.622 pv/(p−pv)` | `humidity_ratio_from_pressures` | §12.5.2, p.755 |
| 12.44 | `φ = pv/pg(T)` | `relative_humidity` | §12.5.2, p.755 |
| 12.43i | `pv = ωp/(0.622+ω)` (dew-point pv) | `vapor_pressure_from_ratio` | §12.5.2/12.5.4, p.755/757 |
| 12.44i | `pv = φ pg` | `vapor_pressure_from_phi` | §12.5.2, p.755 |

## Energy of moist air (Moran §12.5.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 12.45 | `H = ma ha + mv hv` | `mixture_enthalpy_total` | §12.5.2, p.755 |
| 12.46 | `h = ha + ω hv` (per unit dry air) | `mixture_enthalpy_per_dry_air` | §12.5.2, p.755 |
| 12.47 | `hv ≈ hg(T)` | `vapor_enthalpy_approx` | §12.5.2, p.755 |

## Wet-bulb / adiabatic saturation (Moran §12.5.5, §12.7)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 12.48 | `ω = [ha(Tas)−ha(T)+ω′(hg(Tas)−hf(Tas))]/(hg(T)−hf(Tas))` | `humidity_ratio_from_wet_bulb` | §12.5.5, p.763 |
| 12.49 | `ω′ = 0.622 pg(Tas)/(p−pg(Tas))` | `humidity_ratio_at_saturation` | §12.5.5, p.763 |
| 12.50 | `(ha+ωhg)_T+(ω′−ω)hf(Tas)−(ha+ω′hg)_Tas = 0` | `adiabatic_saturator_residual` | §12.5.5, p.764 |
| 12.51 | `ha = cpa T(°C)` (chart datum) | `dry_air_enthalpy` | §12.7, p.767 |

## Air-conditioning balance (Moran §12.8.1)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 12.52 | `ṁw = ṁa(ω2 − ω1)` (water added/removed) | `water_mass_balance` | §12.8.1, p.768 |

> `python3 code/test_equations.py` → 15 value checks + 16 cross-module checks =
> `"All 31 tests passed."` The cross-checks import 11.1 and 11.2 and assert each computes
> the same formula, including that the two modules agree on the shared `pv↔ω` inversion
> (12.43i) and that 11.2's `exit_humidity_ratio` inverts the 12.52 mass balance.
