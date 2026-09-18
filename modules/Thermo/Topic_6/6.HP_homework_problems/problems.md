# 6.HP — Topic 6: Homework Problems (Moran Ch.4 & Ch.6)

8 **processes & idealizations** problems from Moran 8e Ch.4 (flow devices) and Ch.6
(entropy / reversibility / isentropic), each solved from its given data. Moran has **no
answer key**, so these are *worked solutions*, reproduced by `code/homework.py` and checked
(`test_homework.py`, 28 checks incl. energy/entropy-balance consistency). Citations in
`refs.md`. Temperatures in ratios are **absolute** (K/°R).

## Steady-flow control volumes (Ch.4)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 4.34 | air nozzle, ṁ=2.3 kg/s, 450 K/350 kPa/3 m/s → 300 K/460 m/s; cp=1.011 | v₁=0.369 m³/kg, **A₁=0.283 m²**, Q̇=**−105.5 kW** | `p4_34()` |
| 4.42 | insulated turbine, h₁=3015.4, h₂=2431.7, V₁=10, V₂=90, ṁ=11.95 | ΔKE=−4.0 kJ/kg, **Ẇ=6927 kW** | `p4_42()` |

## Reversible & isentropic (Ch.6)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 6.17 | argon, k=1.67, 300 K/1 m³ → 200 K, Δs=−0.27 kJ/kg·K; find V₂ | **V₂≈0.50 m³** | `p6_17()` |
| 6.24 | ideal gas, int. rev. isothermal at 400 K, ΔS=−0.3 kJ/K; find W | Q=−120 kJ, **W=−120 kJ** | `p6_24()` |
| 6.43 | air adiabatic 1 bar/300 K → 10 bar/600 K (cold-air k=1.4); σ/m and min work | **σ/m=0.0358 kJ/kg·K**, T₂s=579 K, **min work≈200.5 kJ/kg** (< actual 215.4) | `p6_43()` |

## Entropy production (Ch.6)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 6.37 | air, rigid insulated tank, 2 m³/293 K/200 kPa, paddle work 710 kJ, cv=0.72 | m=4.76 kg, T₂≈500 K, **σ=1.83 kJ/K** | `p6_37()` |
| 6.40 | air, rigid insulated tank, k=1.4, 4 bar/40 °C/0.2 m³ → 353 °C | p₂=8.0 bar, W=−200 kJ, **σ=0.443 kJ/K** | `p6_40()` |
| 6.53 | 10 lb air, rigid, 600 °R → 800 °R via reservoir at 900 °R (boundary 900 °R), cv=0.171 | Q=342 Btu, **σ=0.112 Btu/°R** | `p6_53()` |

**Method.** Flow devices use the steady-state mass/energy balances (modules `6.4`/`6.5`).
Closed-system problems pair the energy balance (for `Q`/`W`) with the entropy balance
`σ = ΔS − ∫δQ/T` (module `6.2`). Rigid (constant-volume) ideal gas: `ΔS = m c_v ln(T₂/T₁)`,
`p₂/p₁ = T₂/T₁`. Isentropic limits use `T₂/T₁ = (p₂/p₁)^((k−1)/k)` (module `6.3`). A positive
σ confirms the process is possible **and** irreversible; the min-work case (σ = 0) bounds the
actual work — irreversibility always exacts a penalty.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 28 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
