# 2.HP — Topic 2: Homework Problems

17 **quantitative work/energy problems** from Moran 8e Ch.2 (printed pp.82–90),
chosen to **not overlap** Topic_1/1.HP's 12. Moran has no answer key, so these are
*my worked solutions*, reproduced by `code/homework.py` and checked
(`test_homework.py`, 30 checks incl. consistency). Citations in `refs.md`.

## Kinetic & potential energy
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 2.10 | 300 lb, work on it 140 Btu, +100 ft, V₂=200 ft/s; find V₁ | 151.9 ft/s | `p2_10()` |
| 2.14 | 100 lb free-fall from 600 ft, V₁=50 ft/s down, g=31.5; find impact V | 200.7 ft/s | `p2_14()` |
| 2.16 | 200 kg down 10 m ramp at 40°, frictionless; find V at bottom | 11.23 m/s | `p2_16()` |

## Work from a resultant force / power
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 2.19 | 10 kg, a=4 m/s² for 20 s from rest; find work | 32 kJ | `p2_19()` |
| 2.22 | truck 322.5 kN at 110 km/h, f=0.0069 (Fr=fw); find power | 68.0 kW | `p2_22()` |

## Expansion / compression (∫p dV) work
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 2.27 | CO₂, p=23.75−7.5V (psi,ft³), 2.5→0.5 ft³; find W | −4.63 Btu | `p2_27()` |
| 2.29 | N₂, pV¹·³⁵, 20 bar/0.5 m³ → 2.75 m³; find p₂, W | 2.00 bar; +1284 kJ¹ | `p2_29()` |
| 2.30 | O₂, p=A/V+B (A=0.06,B=3.0), 0.01→0.03 m³; find p₁,p₂,W | 9, 5 bar; 12.59 kJ | `p2_30()` |
| 2.35 | air cycle: pV=c (10 psi/4 ft³→50), const-V, const-p back; find V₂, W each | 0.8 ft³; −11.91/0/+5.92 Btu | `p2_35()` |

## Spring / shaft / electrical
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 2.36 | belt sander, 1500 ft/min, μ=0.2, N=15 lbf; find power, work/min | 0.136 hp; 5.78 Btu | `p2_36()` |
| 2.37 | pulley r=0.075 m, τ=200 N·m, 7 kW; find belt force, rpm | 2.67 kN; 334 rpm | `p2_37()` |
| 2.38 | 10 V, 0.5 A, 30 min; find R, energy | 20 Ω; 9 kJ | `p2_38()` |
| 2.45 | spring k=10⁴, ℓ₀=3 cm, 6→10 cm; find work | 20 J | `p2_45()` |

## Closed-system energy balance
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 2.65 | piston A=40 in², 100 lbf, atm 14.7; paddle +3 Btu, rises 1 ft, adiabatic; find ΔU | +2.12 Btu | `p2_65()` |
| 2.66 | 0.4 lb gas, pv¹·², 160 psi/1 ft³ → 390 psi, Q=−2.1 Btu; find Δu | +54.0 Btu/lb | `p2_66()` |
| 2.70 | air adiabatic n=1.4, 100 psi/1000 °R → 50 psi; find T₂ | 820 °R | `p2_70()` |
| 2.64 | R22 rigid tank 1 kg, u 232.92→276.67, paddle 0.1 kW 20 min, Q̇=K·t; find W, Q, K | −120 kJ; −76.25 kJ; 0.00635 kW/min | `p2_64()` |

¹ Problem 2.29's printed text says "compression," but the data (`p₂≈2 bar`, `V`
increasing 0.5→2.75 m³) describe an **expansion** with `W>0` — flagged by the
extraction. Solved as stated by the numbers.

## Run
```bash
cd code
python3 homework.py          # sample of worked answers
python3 test_homework.py     # -> "All 30 tests passed."
```
