# 9.HP — Topic 9: Homework Problems (Moran Ch.5/8/9)

12 problems across the six Topic-9 cycles, each solved from complete given data by
`code/homework.py` and checked (`test_homework.py`, 66 checks incl. balance/consistency).
Moran has **no worked key** for its end-of-chapter sets, so all are *worked solutions*
in the style of the Ch.8–9 problems. Citations in `refs.md`. Cold air-standard `k = 1.4`,
`c_v = 0.718`, `c_p = k·c_v`; Rankine states read at runtime from
`../../steam_tables/` (Table A-3).

## Carnot ceiling (Ch. 5)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P1 | cycle 1400 K↔300 K claims η=0.75 / 0.80; verdicts | η_max=**0.786** ⇒ 0.75 irreversible, 0.80 **impossible** | `p1()` |

## Otto cycle (§9.2)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P2 | r=9.5, T₁=300 K, p₁=100 kPa, T₃=2000 K; T₂, T₄, η, w, mep | T₂=**738.3 K**, T₄=**812.7 K**, η=**0.594**, w=**537.8 kJ/kg**, mep=**698 kPa** | `p2()` |
| P3 | required r for η=0.60 | r=**9.88** (`(1−η)^(−1/(k−1))`) | `p3()` |

## Diesel cycle (§9.3)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P4 | r=16, r_c=2.5, T₁=310 K; T₂–T₄, η | T₂=**939.7**, T₃=**2349.4**, T₄=**1118.1 K**, η=**0.590** | `p4()` |
| P5 | r=18, r_c=1.5/2/3; η trend vs Otto | η=**0.657/0.632/0.589**, all < Otto **0.685** — longer burn costs efficiency | `p5()` |

## Dual cycle (§9.4)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P6 | r=16, r_p=1.3, r_c=1.5, T₁=300 K; T₂–T₅, η | T₅=**688.0 K**, η=**0.647**, bracketed: Diesel 0.640 < dual < Otto 0.670 | `p6()` |

## Brayton cycle (§9.6–9.7)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P7 | ideal, r_p=12, T₁=300 K, T₃=1400 K; T₂, T₄, η, w, bwr | T₂=**610.2**, T₄=**688.3 K**, η=**0.508**, w=**403.5 kJ/kg**, bwr=**0.436** | `p7()` |
| P8 | P7 with η_t=η_c=0.85; η, bwr | η=**0.327** (halved), bwr=**0.603** | `p8()` |
| P9 | P7 + regenerator η_reg=0.75; T_x, η | T_x=**668.8 K**, η=**0.549** (w unchanged) | `p9()` |

## Rankine cycle (§8.2)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P10 | ideal, sat vapor 60 bar → 0.10 bar; x₂, η, bwr | x₂=**0.699**, η=**0.354**, bwr=**0.0066** | `p10()` |
| P11 | boiler 80 bar; condenser 0.08 vs 1.0 bar | η=**0.371 > 0.290** — lower p_cond wins (but exits wetter) | `p11()` |
| P12 | condenser 0.08 bar; boiler 40 vs 80 bar; Carnot | η=**0.343 < 0.371**, both below Carnot **0.399/0.446** at T_sat extremes | `p12()` |

**Method.** Piston cycles: cold air-standard closed forms (Eqs. 9.8, 9.13, dual §9.4)
with `T` chains `T₁→r^(k−1)→r_p/r_c` and mep = w/(v₁(1−1/r)) (Eq. 9.1). Brayton:
Eqs. 9.23–9.25 with `w = c_p[(T₃−T₄)−(T₂−T₁)]`, η_t/η_c per §9.6.3, `T_x` per Eq. 9.27.
Rankine: Eqs. 8.1–8.7b with `s₂ = s₁` and Table A-3 saturation rows. Every cycle's
energy balance closes (`q_in − q_out = w_net`) and sits below its Carnot ceiling.

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 66 tests passed."
```
