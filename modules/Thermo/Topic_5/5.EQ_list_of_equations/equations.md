# 5.EQ — Topic 5: List of Equations (Property Data: Tables & Diagrams)

The defining equations of **Topic 5** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks that
the concept modules (5.1–5.5) reproduce them. Citations are Moran 8e (printed pages;
PDF = printed + 18; `refs.md`) — Ch.3 "Evaluating Properties" plus the Ch.6 T–s material.

## Quality & two-phase mixture rule (Moran §3.3, §3.5.2, §3.6.2, §6.2.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 3.1 | `x = m_vap/(m_liq + m_vap)` | `quality` | §3.3, p.102 |
| 3.2 | `v = vf + x(vg − vf)` | `mixture` | §3.5.2, p.108 |
| 3.2′ | `x = (v − vf)/(vg − vf)` | `quality_from_v` | §3.5.2, p.108 |
| 3.6 | `u = uf + x(ug − uf)` | `mixture` | §3.6.2, p.112 |
| 3.7 | `h = hf + x(hg − hf)` | `mixture` | §3.6.2, p.112 |
| 6.4 | `s = sf + x(sg − sf)` | `mixture` | §6.2.2, p.293 |

## Enthalpy & interpolation (Moran §3.6.1, §3.5.1)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 3.3 | `H = U + pV` | `enthalpy_extensive` | §3.6.1, p.111 |
| 3.4 | `h = u + pv` | `enthalpy` | §3.6.1, p.111 |
| — | `y = y₁ + (x−x₁)/(x₂−x₁)(y₂−y₁)` | `linear_interp` | §3.5.1, p.105 |

## Saturated-liquid approximations (Moran §3.10.1, §6.2.3)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 3.11 | `v(T,p) ≈ vf(T)` | `v_approx` | §3.10.1, p.123 |
| 3.12 | `u(T,p) ≈ uf(T)` | `u_approx` | §3.10.1, p.123 |
| 3.13 | `h(T,p) ≈ hf(T) + vf(T)[p − psat(T)]` | `h_approx` | §3.10.1, p.123 |
| 3.14 | `h(T,p) ≈ hf(T)` | `h_approx_simple` | §3.10.1, p.123 |
| 6.5 | `s(T,p) ≈ sf(T)` | `s_approx` | §6.2.3, p.293 |

## Area interpretations: work on p–v, heat on T–s (Moran §2.2.5, §6.6)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 2.17 | `W = ∫p dV` ; isobaric `W = p(V₂−V₁)` | `work_pdV`, `work_isobaric` | §2.2.5, p.49 |
| 6.23 | `Q = ∫T dS` ; isothermal `Q = T(S₂−S₁)` | `heat_TdS`, `heat_isothermal` | §6.6.1, p.302 |
| 5.9 | `η = 1 − T_C/T_H` (Carnot, from T–S areas) | `carnot_efficiency` | §6.6.2, p.303 |

> `python3 code/test_equations.py` → 19 value checks + 17 cross-module checks =
> `"All 36 tests passed."` The cross-checks import 5.1–5.5 and assert each computes the
> same formula — including that 5.4 (`work_pdV`) and 5.5 (`heat_TdS`) share the identical
> "area under a path" trapezoid kernel (work vs heat).
