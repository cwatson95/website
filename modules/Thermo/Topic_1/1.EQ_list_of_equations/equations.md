# 1.EQ — Topic 1: List of Equations

The key equations of **Topic 1 (Foundations)**, in canonical Moran 8e form. Each
is implemented as a function in `code/equations.py`; `code/test_equations.py`
checks every value **and** cross-checks that the concept modules (1.1, 1.2, 1.4,
1.5) reproduce these forms — so the list is verified, not just asserted.

Citations are Moran 8e (*printed* pages; PDF = +17; see `refs.md`).

## Properties & state (Ch. 1)
| # | Eq. | form | function | source |
|---|-----|------|----------|--------|
| 1 | — | `v = V/m` | `specific_volume(V,m)` | §1.5, p.13 |
| 2 | 1.6 | `ρ = m/V = 1/v` | `density(m,V)` | §1.5, p.13 |
| 3 | 1.14 | `p_abs = p_gauge + p_atm` | `gauge_to_absolute(pg,patm)` | §1.6.3, p.17 |
| 4 | 1.16 | `T(°R) = 1.8·T(K)` | `kelvin_to_rankine(T_K)` | §1.7.2, p.18 |
| 5 | 1.17 | `T(K) = T(°C) + 273.15` | `celsius_to_kelvin(T_C)` | §1.7.3, p.20 |

## Energy & the first law — closed systems (Ch. 2)
| # | Eq. | form | function | source |
|---|-----|------|----------|--------|
| 6 | 2.5 | `ΔKE = ½m(V₂²−V₁²)` | `delta_KE(m,V1,V2)` | §2.1.1, p.41 |
| 7 | 2.10 | `ΔPE = mg(z₂−z₁)` | `delta_PE(m,z1,z2)` | §2.1.2, p.42 |
| 8 | 2.35b | `ΔKE + ΔPE + ΔU = Q − W` | `closed_system_heat(W,dU,…)` | §2.5, p.61 |
| 9 | 2.17 | `W = ∫p dV` (quasiequilibrium) | `boundary_work(p_of_V,V1,V2)` | §2.2.3, p.48 |
| 10 | 2.1(a) | `W = (p₂V₂−p₁V₁)/(1−n)`, n≠1 | `polytropic_work(p1,V1,V2,n)` | Ex 2.1, p.50 |
| 11 | 2.1(b) | `W = p₁V₁ ln(V₂/V₁)`, n=1 | `polytropic_work(…,1)` | Ex 2.1, p.51 |
| — | — | `p₂ = p₁(V₁/V₂)ⁿ` (polytropic) | `polytropic_pressure(…)` | §2.2.5, p.50 |

## Mass & energy — control volumes / open systems (Ch. 4)
| # | Eq. | form | function | source |
|---|-----|------|----------|--------|
| 12 | 4.2 | `dm_cv/dt = Σṁᵢ − Σṁₑ` | `mass_rate_residual(in,out)` | §4.1, p.170 |
| 13 | 4.4b | `ṁ = AV/v = ρAV` | `mass_flow_rate(A,V,v)` | §4.2.1, p.172 |
| 14 | — | `h = u + pv` (enthalpy) | `enthalpy(u,p,v)` | §4.4.2, p.179 |
| 15 | 4.15 | `dE_cv/dt = Q̇ − Ẇ + Σṁ(h+V²/2+gz)ᵢ − Σṁ(…)ₑ` | `flow_energy(h,V,z)` (the ψ term) | §4.4.3, p.180 |

## Constants used
Standard gravity `g = 9.81 m/s²`. (Substance gas constants `R` and the universal
`R̄ = 8.314 kJ/kmol·K` live in the cross-cutting **Constants** module / Table 3.1.)

> Run `python3 code/equations.py` to print this registry, or
> `python3 code/test_equations.py` to verify every equation and its cross-module
> agreement (`"All 26 tests passed."`).
