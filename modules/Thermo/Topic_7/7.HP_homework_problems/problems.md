# 7.HP — Topic 7: Homework Problems (Moran Ch.2/5/6)

8 problems on performance metrics, each solved from complete given data by
`code/homework.py` and checked (`test_homework.py`, 18 checks incl. balance/consistency).
Problems **2–5** are Moran 8e *Checking Understanding* items (p.277) whose answer is fixed
by the physics; Moran has **no worked key**, so all are *worked solutions*. Citations in
`refs.md`. Cycle `Q`, `W` are positive magnitudes; Carnot `T` is absolute (K/°R).

## Thermal efficiency & Carnot ceilings (Ch. 2, 5)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P1 | power cycle, Q_in=1000 kJ, W=400 kJ; find η, Q_out | η=**0.40**, Q_out=**600 kJ** | `p1()` |
| P2 | (CU #6) cycle 2000 °F↔1000 °F claims η=45%; verdict | η_max=0.407 ⇒ **impossible** | `p2()` |
| P3 | (CU #15) max η between 1000 °C and 500 °C | η_max=**0.393 (39.3%)** | `p3()` |
| P4 | (CU #16) cycle 500 K↔300 K, Q_H=1000 kJ; min Q_C | η_max=0.40 ⇒ Q_C ≥ **600 kJ** | `p4()` |

## Coefficients of performance (Ch. 2, 5)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P5 | (CU #11) max COP heat pump 40 °F↔80 °F | γ_max=**13.49** | `p5()` |
| P6 | refrigerator Q_C=2000 kJ, W=500 kJ, 250 K↔300 K | β=**4.0**, β_max=**5.0** (irreversible) | `p6()` |

## Isentropic (device) efficiencies (Ch. 6)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P7 | turbine h₁=3000, h₂=2680, h₂s=2600 kJ/kg | η_t=**0.80**, w=**320** (ideal 400) | `p7()` |
| P8 | pump h₁=200, h₂=212.5, h₂s=210 kJ/kg | η_p=**0.80**, w_in=**12.5 kJ/kg** | `p8()` |

**Method.** For a power cycle η = W/Q_in = 1 − Q_out/Q_in, capped by η_max = 1 − T_C/T_H;
a claim above the ceiling is impossible, equal to it is reversible, below it is
irreversible. COPs β = Q_C/W and γ = Q_H/W are capped by β_max = T_C/(T_H−T_C) and
γ_max = T_H/(T_H−T_C). A device's isentropic efficiency compares it to the reversible-
adiabatic ideal (state 2s, s₂s=s₁) at the same inlet state and exit pressure.

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 18 tests passed."
```
