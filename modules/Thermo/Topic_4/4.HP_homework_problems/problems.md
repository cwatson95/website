# 4.HP — Topic 4: Homework Problems (Moran Ch.3/6/7)

8 problems from Moran 8e spanning Properties & State Functions, each solved from its
given data (steam-table values from Tables A-2..A-5). Moran has **no answer key**, so
these are *worked solutions*, reproduced by `code/homework.py` and checked
(`test_homework.py`, 19 checks incl. energy/entropy/exergy-balance consistency).
Citations in `refs.md`.

## Enthalpy & phase change (Ch. 3)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 3.46 | water sat. vapor @4 bar, **rigid**, → 400 °C; find Q/m | rigid ⇒ Q/m = u₂−u₁ = **+407.6 kJ/kg** | `p3_46()` |
| 3.63 | water 20 bar, x₁=0.8, 0.5 m³, **rigid**, cooled → 4 bar; find Q | m=6.26 kg, x₂=0.171, **Q=−8283 kJ** | `p3_63()` |
| 3.70 | water 5 kg, 5 bar, 240 °C, **const-p**, Q=2960 kJ; find T₂, W | h₂=3531.9, **T₂≈522 °C, W=+667 kJ** | `p3_70()` |

## Entropy (Ch. 6)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 6.11 | air 300 K/100 kPa → 500 K/650 kPa; find Δs | **Δs=−0.0197 kJ/kg·K** (same rev. or irrev. — a property) | `p6_11()` |
| 6.37 | 2 m³ air, rigid insulated, +710 kJ paddle, 293 K/200 kPa, cv=0.72 | m=4.76 kg, T₂=500.3 K, **σ=1.83 kJ/K** | `p6_37()` |
| 6.59 | 1 kg metal @1075 K (c=0.5) + 100 kg water @295 K (c=4.2), isolated | Tf=295.93 K, **σ=0.673 kJ/K** | `p6_59()` |

## Exergy (Ch. 7)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 7.21 | concrete slab (16560 kg, c=0.88) 298→301 K, T₀=298 K | **ΔE=218.6 kJ**; could lift 1000 kg by **22.3 m** | `p7_21()` |
| 7.36 | 1 lb metal @2000 °R (c=0.1) + 25 lb water @500 °R, T₀=537 °R | σ=0.1596 Btu/°R, **Ed=85.7 Btu** | `p7_36()` |

**Method.** Rigid (`W=0`) ⇒ `Q=ΔU` (use `u`); constant-`p` ⇒ `Q=ΔH` (use `h`). Δs is a
property (same for any path); σ and Ed measure the path's irreversibility, with
`Ed = T₀σ`.

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 18 tests passed."
```
