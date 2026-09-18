# 7.EP — Topic 7 Example Problems (Moran Ch.5/6)

Seven Moran 8e worked **Examples** spanning the performance metrics, reproduced from their
*given* data and verified in `code/examples.py` (`test_examples.py`). Each regenerates the
book's published answer. Citations in `refs.md`.

| Moran Ex. | concept (module) | given → find | book answer | function |
|-----------|------------------|--------------|-------------|----------|
| **5.1** Evaluating Power Cycle Performance | thermal η + Carnot (`07.1`) | T_H=2000 K, T_C=400 K; (a) η=60% (b) W=850 kJ (c) Q_C=200 kJ, all Q_H=1000 kJ | η_max=80%; (a) irreversible (b) impossible (c) reversible | `ex_5_1` |
| **5.2** Evaluating Refrigerator Performance | COP β (`07.1`) | freezer 268 K in 295 K air; Q̇_C=8000, Ẇ=3200 kJ/h | β=2.5, β_max=9.9 | `ex_5_2` |
| **5.3** Evaluating Heat Pump Performance | COP γ_max (`07.1`) | 530 °R from 492 °R; Q_H=5×10⁵ Btu/day; 0.13 $/kWh | γ_max=13.95, W_min=3.58×10⁴ Btu/day, cost=$1.36/day | `ex_5_3` |
| **6.11** Determining Turbine Work | isentropic turbine (`07.1`) | steam 5 bar/320 °C → 1 bar, η_t=75%; h₁=3105.6, h₂s=2743.0 | W/m=271.95 kJ/kg | `ex_6_11` |
| **6.12** Evaluating Isentropic Turbine Efficiency | isentropic turbine (`07.1`) | air 3 bar/390 K → 1 bar, w=74 kJ/kg; h₁=390.88, p_r1=3.481 | h₂s=285.27, (W/m)_s=105.6, η_t=0.70 | `ex_6_12` |
| **6.13** Evaluating Isentropic Nozzle Efficiency | isentropic nozzle (`07.1`) | steam 140 lbf/in², 600 °F, 100 ft/s → 40 lbf/in², 350 °F; h₂s=1202.3 | ke₂=114.8, ke₂s=124.3, η_n=0.924 | `ex_6_13` |
| **6.14** Evaluating Isentropic Compressor Efficiency | isentropic compressor (`07.1`) | R-22, ṁ=0.07 kg/s; h₁=249.75, h₂=294.17, h₂s=285.58 | Ẇ=−3.11 kW, η_c=0.81 | `ex_6_14` |

**Key thread:** Examples 5.1–5.3 measure whole **cycles** against the *Carnot* ceiling
(η_max, β_max, γ_max); Examples 6.11–6.14 measure single **devices** against the
*isentropic* ideal (state 2s with s₂s=s₁). Ex 6.11/6.12 are the two directions of the same
turbine relation (Eq. 6.46): work-from-efficiency and efficiency-from-work.

## Run
```bash
cd code
python3 examples.py          # all seven examples vs the book answers
python3 test_examples.py     # -> "All 18 tests passed."
```
