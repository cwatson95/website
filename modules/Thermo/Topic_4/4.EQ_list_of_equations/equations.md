# 4.EQ — Topic 4: List of Equations (Properties & State Functions)

The defining equations of **Topic 4** in canonical Moran 8e form. Each is a function
in `code/equations.py`; `code/test_equations.py` checks every value **and**
cross-checks that the concept modules (4.1–4.5) reproduce them. Citations are Moran 8e
(printed pages; PDF = printed + 18; `refs.md`).

## Enthalpy (Ch. 3 §3.6)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 3.4 | `h = u + pv` | `enthalpy` | §3.6.1, p.111 |
| 3.3 | `H = U + pV` | `enthalpy_total` | §3.6.1, p.111 |

## Quality & mixtures (Ch. 3 §3.3–3.6, Ch. 6 §6.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 3.1 | `x = m_vap/m_tot` | `quality` | §3.3, p.102 |
| 3.2/3.6/3.7/6.4 | `y = yf + x·yfg` (v,u,h,s) | `mixture_property` | §3.5.2, p.108 |

## Entropy (Ch. 6)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 6.13 | `Δs = c·ln(T₂/T₁)` | `entropy_change_incompressible` | §6.4, p.298 |
| 6.22 | `Δs = cp·ln(T₂/T₁) − R·ln(p₂/p₁)` | `entropy_change_ideal_gas_cp` | §6.5.2, p.301 |
| 6.24 | `σ = (S₂−S₁) − ∫δQ/T_b` | `entropy_production_closed` | §6.7, p.305 |

## Exergy (Ch. 7)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 7.2 | `e = (u−u₀)+p₀(v−v₀)−T₀(s−s₀)` | `specific_exergy` | §7.3.2, p.376 |
| 7.5 | `E_q = (1−T₀/T_b)Q` | `exergy_transfer_heat` | §7.4.1, p.380 |
| 7.7 | `E_d = T₀·σ` | `exergy_destruction` | §7.4.1, p.380 |

## Gibbs phase rule (Ch. 14 §14.6)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 14.68 | `F = 2 + N − P` | `gibbs_phase_rule` | §14.6.2, p.913 |

> `python3 code/test_equations.py` → 11 value checks + 9 cross-module checks =
> `"All 20 tests passed."`
