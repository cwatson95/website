# 13.EQ — Topic 13: List of Equations (Compressible Flow & Gas Dynamics)

The defining equations of **Topic 13** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks
that the concept modules (13.1–13.5) reproduce them. Citations are Moran 8e (printed
pages; PDF = printed + 18; `refs.md`) for the Ch.9 compressible-flow trunk, and
cross-trunk fluid mechanics (~CM) for the pipe-flow leaves.

## Sound, Mach number, stagnation (Moran §9.12)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 9.37 | `c = √(kRT)` | `speed_of_sound_ideal_gas` | §9.12.2, p.570 |
| 9.38 | `M = V/c` | `mach_number` | §9.12.2, p.570 |
| 9.39 | `ho = h + V²/2` | `stagnation_enthalpy` | §9.12.3, p.571 |

## Area change & isentropic flow functions (Moran §9.13–9.14.1)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 9.45 | `dA/A = −(dV/V)(1−M²)` | `area_change_ratio` | §9.13.1, p.573 |
| 9.50 | `To/T = 1 + (k−1)/2·M²` | `stagnation_temperature_ratio` | §9.14.1, p.578 |
| 9.51 | `po/p = (1+(k−1)/2·M²)^{k/(k−1)}` | `stagnation_pressure_ratio` | §9.14.1, p.578 |
| 9.52 | `A/A* = (1/M)[(2/(k+1))(1+(k−1)/2·M²)]^{(k+1)/2(k−1)}` | `area_mach_ratio` | §9.14.1, p.578 |
| 9.51@M=1 | `p*/po = (2/(k+1))^{k/(k−1)}` (=0.528, k=1.4) | `critical_pressure_ratio` | §9.13.2, p.574 |
| 9.50@M=1 | `T*/To = 2/(k+1)` | `critical_temperature_ratio` | §9.14.1, p.578 |

## Normal-shock functions (Moran §9.14.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 9.55 | `My² = (Mx²+2/(k−1))/((2k/(k−1))Mx²−1)` | `mach_after_shock` | §9.14.2, p.581 |
| 9.54 | `py/px = (1+kMx²)/(1+kMy²)` | `shock_pressure_ratio` | §9.14.2, p.581 |
| 9.53 | `Ty/Tx = (1+(k−1)/2·Mx²)/(1+(k−1)/2·My²)` | `shock_temperature_ratio` | §9.14.2, p.581 |
| 9.56 | `poy/pox = (Mx/My)[(1+(k−1)/2·My²)/(1+(k−1)/2·Mx²)]^{(k+1)/2(k−1)}` | `stagnation_pressure_ratio_across_shock` | §9.14.2, p.581 |

## Cross-trunk pipe-flow leaves (~CM, **NOT Moran**; 13.4 / 13.5)
| form | function | source |
|------|----------|--------|
| `Re = ρVD/μ` | `reynolds_number` | ~CM (White §6.3) |
| `f = 64/Re` (laminar, exact) | `friction_factor_laminar` | ~CM (White Eq. 6.12) |
| `f = 0.316/Re^{1/4}` (turbulent, Blasius) | `friction_factor_blasius` | ~CM (White Eq. 6.38) |

> `python3 code/test_equations.py` → 16 value checks + 17 cross-module checks =
> `"All 33 tests passed."` (The cross-checks import 13.1–13.5 and assert each computes
> the same formula, including that 13.4 and 13.5 agree on the shared Reynolds number.)
