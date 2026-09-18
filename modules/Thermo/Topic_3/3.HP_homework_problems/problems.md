# 3.HP — Topic 3: Homework Problems (Moran Ch.5, the second law)

7 **second-law problems** from Moran 8e Ch.5 (printed pp.278–286), each solved from
its given data. Moran has **no answer key**, so these are *worked solutions*,
reproduced by `code/homework.py` and checked (`test_homework.py`, 22 checks incl.
energy-balance consistency). Citations in `refs.md`. Carnot temps are **absolute**.

## Power cycles
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 5.2 | cycle takes Q_C=500 kJ from cold, gives Q_H=400 kJ to hot, W=100 kJ; possible? | balance closes (W=100), but **impossible** — net heat cold→hot *with* work violates the 2nd law | `p5_2()` |
| 5.21 | reversible, η=40%, Q_H=50 kJ at T_H=600 K; find T_C, Q_C, W | T_C=360 K; W=20 kJ; Q_C=30 kJ | `p5_21()` |
| 5.31 | Q_H=1000 Btu, T_H=1000 °F, T_C=300 °F, η = 75% of reversible; find η, W, Q_C | η_rev=0.480, η=0.360; W=359.7 Btu; Q_C=640.3 Btu | `p5_31()` |
| 5.34 | power cycle 500/310 K, W=0.1 MW; min theoretical Q̇ rejected | η_max=0.38; Q̇_C,min=0.163 MW | `p5_34()` |
| 5.76 | Carnot cycle T_H=600 K, T_C=300 K; η, and Δη if T_H +15% | η=0.50; η→0.565 (**+13.0%**) | `p5_76()` |

## Refrigeration & heat pumps
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 5.48 | reversible power η=20%; COP of reversible refrig. & heat pump (same reservoirs) | β=4, γ=5 (γ=β+1) | `p5_48()` |
| 5.50 | freezer 20 °F, kitchen 70 °F; claimed COP (a) 10, (b) 9.6, (c) 4 | β_max=9.6 → (a) **impossible**, (b) reversible limit, (c) possible (irreversible) | `p5_50()` |

**Method.** Power cycles use η_max = 1 − T_C/T_H (Eq. 5.9) as the ceiling, W = ηQ_H,
Q_C = Q_H − W (Eq. 2.41). Refrigeration/heat-pump claims are tested against
β_max = T_C/(T_H−T_C) (Eq. 5.10) / γ_max = T_H/(T_H−T_C) (Eq. 5.11). A claim that
*exceeds* the reversible bound is impossible; *equal* means reversible; *below* means
a real (irreversible) cycle.

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 23 tests passed."
```
