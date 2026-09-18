# 1.HP — Topic 1: Homework Problems

Selected **quantitative end-of-chapter problems** from Moran 8e Ch.1–2 ("Problems:
Developing Engineering Skills", printed pp.30–35 and 82–90). Moran publishes **no
answer key**, so the answers below are *my worked solutions*, each reproduced by
`code/homework.py` and checked (`test_homework.py`, 39 checks incl. consistency).
Citations in `refs.md`; PDF = printed + 17.

## Chapter 1 — Getting Started
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 1.8 | m=350 kg; find weight on Mars (g=3.73) and Earth (g=9.81) | 1305.5 N; 3433.5 N | `p1_8()` |
| 1.13 | m=120 lb weighs 119 lbf; find local g, then weight/mass at g=32.05 ft/s² | 31.91 ft/s²; 119.54 lbf, 120 lb | `p1_13()` |
| 1.20 | 0.5 kmol NH₃ in 6 m³; find weight & specific volume | 83.5 N; 12 m³/kmol, 0.7046 m³/kg | `p1_20()` |
| 1.21 | 2 lb liquid in 62.6 in³; find v and ρ | 0.01811 ft³/lb; 55.21 lb/ft³ | `p1_21()` |
| 1.23 | 5 kg vapor, v=0.2160 m³/kg; find V, gram-moles, molecules | 1.08 m³; 277.5 mol; 1.671×10²⁶ | `p1_23()` |
| 1.33 | gas manometer L=1.0 m Hg, p_atm=101 kPa; find gas pressure | 234.3 kPa | `p1_33()` |
| 1.35 | barometer, p_atm=100 kPa; find Hg column | 750.1 mm = 29.53 in | `p1_35()` |
| 1.36 | venturi, kerosene Δh=12 cm (v=0.00122 m³/kg); find Δp | 0.965 kPa | `p1_36()` |
| 1.38 | submarine at 1000 ft, water 62.4 lb/ft³; find pressure | 30.49 atm | `p1_38()` |
| 1.40 | inlet 5.5 psig (atm 14.5), ratio 8; find exit | 160 psia | `p1_40()` |
| 1.42 | 0.5-m piston, gauge 1.2→2.8 kPa; find piston & added mass | 24.0 kg; 32.0 kg | `p1_42()` |
| 1.50 | Toronto 19.5/−4.9 °C → °F, °R | 67.1 °F/526.8 °R; 23.2 °F/482.9 °R | `p1_50()` |
| 1.51 | six °F values → °C, K | e.g. 86 °F=30 °C=303.15 K; −459.67 °F=0 K | `p1_51()` |

## Chapter 2 — Energy and the First Law
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 2.5 | car 2500 lbf, ΔPE=2.25×10⁴ Btu from 5183 ft; find top elevation | 12 186 ft | `p2_5()` |
| 2.6 | m=1000 kg, 100→20 m/s; find ΔKE | −4800 kJ | `p2_6()` |
| 2.7 | 14 000 kg, 0→620 km/h, +10 000 m (g=9.78); find ΔKE, ΔPE | 207 623 kJ; 1 369 200 kJ | `p2_7()` |
| 2.26 | pV²=const, 1 bar/0.1 m³ → 9 bar; find V₂, W | 0.0333 m³; −20 kJ | `p2_26()` |
| 2.28 | pVⁿ, V 0.1→0.04 m³, p₂=2 bar; find p₁ & W for n=0,1,1.3 | p₁=2/0.8/0.61 bar; W=−12/−7.33/−6.41 kJ | `p2_28()` |
| 2.31 | air, 80 psi/4 ft³·lb⁻¹ → 20 psi/11; find polytropic work | n=1.370; W=+724 Btu | `p2_31()` |
| 2.39 | heater 6 A, 220 V, 24 h, $0.08/kWh; find power, energy, cost | 1.32 kW; 31.68 kWh; $2.53 | `p2_39()` |
| 2.58 | 10 kg: W=0.147 kJ/kg, Δz=−50 m, 15→30 m/s, Δu=−5 kJ/kg, g=9.7; find Q | −50.0 kJ | `p2_58()` |
| 2.59 | const-p 2 bar, 0.1→0.12 m³, ΔU=0.25 kJ; find W, Q | 4 kJ; 4.25 kJ | `p2_59()` |
| 2.62 | motor 10 A/110 V, 9.7 N·m @1000 rpm, hA=3.9 W/K, T_f=21 °C; find P_e, P_shaft, T_s | 1.1 kW; 1.016 kW; 42.6 °C | `p2_62()` |
| 2.71 | 25 kg piston (A=0.005 m²), 2.5 g air 2.5→1.0 L, −1 kJ; find Δu | −310.6 kJ/kg | `p2_71()` |
| 2.90 | refrigerator, Ẇ=0.15 kW, Q̇_out=0.6 kW; find Q̇_in, COP | 0.45 kW; COP=3.0 | `p2_90()` |

## Run
```bash
cd code
python3 homework.py          # print a sample of worked answers
python3 test_homework.py     # 39 checks (answers + consistency) -> "All 39 tests passed."
```

*Skipped from extraction (no definite numeric answer): true/false items, design/
open-ended/Internet problems, and a few garbled or under-specified statements
(e.g. 2.18 omits the mass; 2.29's "compression" actually expands).*
