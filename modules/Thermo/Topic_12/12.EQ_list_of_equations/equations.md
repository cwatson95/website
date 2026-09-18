# 12.EQ — Topic 12: List of Equations (Combustion & Reacting Mixtures)

The defining equations of **Topic 12** in canonical Moran 8e form. Each is a function in
`code/equations.py`; `code/test_equations.py` checks every value **and** cross-checks
that the concept modules (`12.1`, `12.2`) and the worked-examples module (`12.EP`)
reproduce them. Citations are Moran 8e (printed pages; PDF = printed + 18; `refs.md`)
for the Ch.13–14 trunks, and cross-trunk plasma physics (**~PK, NOT Moran**) for the
Saha rows.

## Combustion stoichiometry & air (Moran §13.1)
| Eq. | form | function | source |
|-----|------|----------|--------|
| from 13.3–13.4 | `a_O₂ = C + H/4 + S − O/2` | `theoretical_O2` | §13.1.2, p.808 |
| 13.4 | `AF̄_theo = 4.76 a_O₂` (air = O₂ + 3.76 N₂) | `theoretical_air_molar` | §13.1.2, p.807–808 |
| 13.2 | `AF = AF̄ (M_air/M_fuel)` | `air_fuel_mass_from_molar` | §13.1.2, p.808 |
| (13.5) | `% theo = AF/AF_theo`; `% excess = AF/AF_theo − 1` | `percent_theoretical_air`, `percent_excess_air` | §13.1.2, p.808–809 |
| — | `φ = AF_theo/AF_actual` (<1 lean, >1 rich) | `equivalence_ratio` | §13.1.2, p.809 |
| — | `p_v = y_v p`, dew point = `T_sat(p_v)` | `dew_point_partial_pressure` | §13.1.3, p.811–812 |

## First law for reacting systems (Moran §13.2–13.3)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 13.9 | `h = h°_f + Δh` | `enthalpy_formation_plus_dh` | §13.2.1, p.817 |
| 13.15b | `Σ n (h°_f + Δh)` per stream | `stream_enthalpy` | §13.2.2, p.819 |
| 13.12b/13.15b | `(Q̇cv−Ẇcv)/ṅ_F = h̄_P − h̄_R` | `energy_balance_steady` | §13.2.2, p.818–819 |
| 13.17b | `Q−W = Σ_P n(h°_f+Δh) − Σ_R n(h°_f+Δh) − R̄T_P Σ_P n + R̄T_R Σ_R n` | `energy_balance_closed` | §13.2.2, p.823 |
| 13.18 | `h_RP = Σ_P n_e h_e − Σ_R n_i h_i` | `enthalpy_of_combustion` | §13.2.3, p.825 |
| — | HHV/LHV `= |h_RP|` (liquid/vapor product water); ÷M per kg | `heating_value_molar`, `heating_value_mass` | §13.2.3, p.825–826 |
| 13.21b | `Σ_P n_e(Δh)_e = Σ_R n_i h°_f,i − Σ_P n_e h°_f,e` (adiabatic, reactants at T_ref) | `adiabatic_flame_rhs`, `interpolate_flame_temperature` | §13.3.1, p.829 |

## Chemical & ionization equilibrium (Moran §14.1–14.4)
| Eq. | form | function | source |
|-----|------|----------|--------|
| 14.17 | `μ_i = g°_i + R̄T ln(y_i p/p_ref)` | `chemical_potential_ideal_gas` | §14.1, p.886 |
| 14.26 | `ν_Aμ_A + ν_Bμ_B = ν_Cμ_C + ν_Dμ_D` | `reaction_equilibrium_residual` | §14.2, p.889 |
| 14.29b | `ΔG° = Σ_P ν(h̄−Ts̄°) − Σ_R ν(h̄−Ts̄°)` | `gibbs_of_reaction` | §14.3.1, p.890 |
| 14.31 | `ln K = −ΔG°/(R̄T)` (Table A-27 tabulates log₁₀K) | `lnK_from_gibbs`, `log10K_from_gibbs` | §14.3.1, p.890 |
| 14.32 | `K = Π y^ν (p/p_ref)^Δν` | `equilibrium_constant_composition` | §14.3.1, p.890 |
| 14.34 | `log₁₀K* = −log₁₀K` (inverse reaction) | `log10K_inverse` | §14.3.1, p.890 |
| 14.35 | `K = Π n^ν ((p/p_ref)/n)^Δν`, n incl. inerts | `equilibrium_constant_moles` | §14.3.2, p.892 |
| 14.45 / Ex 14.8 | `A ⇌ A⁺ + e⁻`: `K = [z²/(1−z²)](p/p_ref)`; `z = √(K/(K+p/p_ref))` | `ionization_K_from_extent`, `ionization_extent_from_K` | §14.4.3, p.904–905 |

> **Adjacent, not included:** the van't Hoff equation `d ln K/dT = ΔH/R̄T²`
> (Eq. 14.43b, §14.4.2, p.903; integrated form Eq. 14.44, p.904) — neither `12.1` nor
> `12.2` uses it, so it has no registry row.

## Saha ionization rows (**~PK, NOT Moran**; `12.2` part B)
| form | function | source |
|------|----------|--------|
| `n_Q = (2πm_e k_B T/h²)^{3/2} = 1/λ³` | `quantum_concentration` | ~PK (Reif; Rybicki & Lightman §9.5) |
| `S = n₊n_e/n₀ = 2(g₊/g₀) n_Q e^{−χ/k_BT}` | `saha_rhs` | ~PK (Saha 1920; Chen) |
| `K(T) = S·k_B T/p_ref` (Moran-form ionization K) | `saha_ionization_K` | ~PK (bridge to Eq. 14.35) |

> Moran §14.4.3 treats ionization equilibrium with the *same* K machinery but says the
> ionization K "can be calculated … by using the procedures of statistical
> thermodynamics" **without giving the formula** (p.904). The Saha equation *is* that
> formula — hence the ~PK flag. The bridge row converts Saha's number-density form to
> Moran's dimensionless K; `test_equations.py` verifies the two give identical
> ionization fractions (exact algebra: `x²/(1−x) = S/n` ⇔ `K = z²/(1−z²)·p/p_ref` with
> `p = n(1+x)k_BT`).

> `python3 code/test_equations.py` → 37 value checks + 30 cross-module checks =
> `"All 67 tests passed."` (The cross-checks import `12.1`, `12.2`, and `12.EP` and
> assert each computes the same formula, including that `12.2`'s dissociation extents
> round-trip through Eq. 14.35 and that the Saha fraction matches Moran's Eq.-14.35
> ionization form.)
