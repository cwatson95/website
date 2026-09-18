# 11.HP — Topic 11: Homework Problems (Moran Ch.12, psychrometrics)

7 **psychrometric problems** from Moran 8e Ch.12 (printed pp.793–799), each solved from
its given data (printed pp.795–799). Moran has **no answer key** for end-of-chapter problems, so these are
*worked solutions*, reproduced by `code/homework.py` and checked (`test_homework.py`, 48
checks = worked values + physical-consistency). Citations in `refs.md`.

## Humidity ratio, dew point, condensation
| # | given → find | worked answer | check |
|---|--------------|---------------|-------|
| 12.51 | moist air 30 °C, 2 bar, 50% RH, 600 kg/h cooled at const p to 20 °C → Q̇ | ω₁=0.00667; dew pt 18.4 °C (< 20 → no condensate); ṁₐ=596 kg/h; **Q̇=−6062 kJ/h** | `p12_51()` |
| 12.52 | 2 lb moist air 100 °F, 1 atm, 40% RH compressed isothermally to 4 atm → condensate | ωₐ would-be pv=1.52 > pg=0.95 ⇒ **condenses**; ω₂=0.01022; **mₓ=0.0124 lb** | `p12_52()` |
| 12.56 | N₂/H₂O mixture 200 °F, 1 atm, 20% (molar) water vapor cooled at const p → onset T | pv=yᵥp=2.94 lbf/in²; dew point **≈140.6 °F** | `p12_56()` |

## Dehumidification (cooling below the dew point)
| # | given → find | worked answer | check |
|---|--------------|---------------|-------|
| 12.60 | 30 °C, 1.05 bar, 80% RH in; exit 15 °C, 1 bar, 95% RH; refrigerant Δh=100 kJ/kg → ṁᵣ/ṁₐ | ω₁=0.0208, ω₂=0.0102; ṁ_w/ṁₐ=0.0106; **ṁᵣ/ṁₐ=0.417** | `p12_60()` |
| 12.78 | 35 °C, 1 atm, 50% RH in; saturated air + condensate exit at 15 °C → Q/ṁₐ, mₓ/ṁₐ | ω₁=0.0178, ω₂=0.0106; condensate 0.00712 kg/kg(a); **Q/ṁₐ=−38.3 kJ/kg(a)** | `p12_78()` |

## Wet-bulb / dry-bulb and evaporative cooling
| # | given → find | worked answer | check |
|---|--------------|---------------|-------|
| 12.77 | 1 atm, T_db=82 °F, T_wb=68 °F, 10 lb/min, cooled at const p to 62 °F → φ₁, Q̇ | ω′=0.0147 (Eq. 12.49), ω₁=0.0114 (Eq. 12.48), **φ₁≈49%**; dew 61 °F (< 62 → no condensate); **Q̇=−48.4 Btu/min** | `p12_77()` |
| 12.92 | 35 °C, 1 bar, 10% RH, 50 m³/min; liquid 20 °C fully evaporates; exit 25 °C (adiabatic) → liquid rate, φ₂ | ω₁=0.00352→ω₂=0.00763; ṁₐ=56.2 kg/min; **liquid 0.231 kg/min**; **φ₂≈38%** | `p12_92()` |

**Method.** Get the vapor pressure from φ (pv=φ·pg) or from the wet-bulb temperature
(Eqs. 12.48–12.49 with T_wb≈T_as), then ω=0.622 pv/(p−pv). The **dew point** is
T_sat(pv): cool at constant p (constant ω) and condensation begins there; for *constant-T*
compression it begins when pv would exceed pg. **Dehumidification** cools below the dew
point so ω₂<ω₁ and condensate mₓ=ṁₐ(ω₁−ω₂); apply the Eq.-12.55 energy balance for Q (or
the refrigerant balance for ṁᵣ). **Evaporative cooling** is an adiabatic humidification:
ω rises, T falls, φ rises, with the injected-water rate = ṁₐ(ω₂−ω₁) (Eq. 12.52).

> **No book key.** These are worked solutions; table values (pg, hf, hg) used are stated
> in each `homework.py` function and in `refs.md`. Dry-air enthalpy uses ha=cpa·T
> (cpa=1.005 kJ/kg·K or 0.24 Btu/lb·°R) and T(K)=T(°C)+273, matching Moran's examples.

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 48 tests passed."
```
