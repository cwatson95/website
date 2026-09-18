# 6.EQ — Topic 6: List of Equations (Processes & Idealizations)

The defining equations of **Topic 6** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks that
the concept modules (6.1–6.5) reproduce them. Citations are Moran 8e (printed pages;
PDF = printed + 18; `refs.md`).

## 6.1 Reversible / internally reversible (Ch. 6 §6.6)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 6.23 | `Q_int rev = ∫T dS = T(s₂−s₁)` | `heat_int_rev_isothermal` | §6.6.1, p.302 |
| 6.2b | `dS = (δQ/T)_int rev` | `entropy_change_int_rev` | §6.6, p.302 |

## 6.2 Irreversible / entropy production (Ch. 6 §6.7–6.8)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 6.24 | `σ = (S₂−S₁) − ∫(δQ/T)_b` | `entropy_production` | §6.7, p.305 |
| 6.30 | `σ_isol = ΔS_sys + ΔS_surr ≥ 0` | `sigma_isolated` | §6.8.1, p.313 |
| 6.13 | `ΔS = m c ln(T₂/T₁)` (incompr.) | `entropy_change_incompressible` | §6.4, p.298 |

## 6.3 Adiabatic / isentropic (Ch. 6 §6.11–6.12, §3.15)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 6.43 | `T₂/T₁ = (p₂/p₁)^((k−1)/k)` | `final_temp_isentropic` | §6.11.2, p.328 |
| 6.45 | `p₂/p₁ = (v₁/v₂)^k` (`pv^k=const`) | `pressure_ratio_from_volume` | §6.11.2, p.328 |
| 6.46 | `η_t = (h₁−h₂)/(h₁−h₂s)` | `isentropic_turbine_eff` | §6.12.1, p.333 |
| 3.47 | `c_p=kR/(k−1)`, `c_v=R/(k−1)` | `cp_from_k`, `cv_from_k` | §6.11.2, p.328 |

## 6.4 Steady-state control volumes (Ch. 4 §4.5)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 4.20a | `0=Q̇−Ẇ+ṁ[Δh+ΔKE+ΔPE]` | `heat_rate_steady` | §4.5.1, p.181 |

## 6.5 Conservation of mass (Ch. 4 §4.1–4.2)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 4.4b | `ṁ = AV/v` | `mass_flow_rate` | §4.2.1, p.172 |
| 4.6 | `Σṁi = Σṁe` | `steady_mass_residual` | §4.2.2, p.173 |

> `python3 code/test_equations.py` → 13 value checks + 13 cross-module checks =
> `"All 26 tests passed."`
