# 8.HP — Topic 8: Homework Problems (Moran Ch.4/6/10 devices)

8 problems spanning the four Topic-8 devices, each solved from complete given data by
`code/homework.py` and checked (`test_homework.py`, 34 checks incl. balance/consistency).
Moran has **no worked key**, so all are *worked solutions*; the property values are the
book-verified ones from the Topic-8 worked Examples (`8.EP`, `refs.md`). `h` in kJ/kg,
rates in kW; Carnot `T` is absolute (K).

## Compressor (Ch. 4 §4.8, Ch. 6 §6.12.3)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P1 | air 1 bar, 290 K, 6 m/s in A=0.1 m²; find v and ṁ two ways | v=**0.832 m³/kg**, ṁ=**0.72 kg/s** (AV/v = AVp/RT) | `p1()` |
| P2 | + exit h₂=451.80, h₁=290.16 kJ/kg, V₂=2 m/s, Q̇=−3 kW; find power input | Ẇcv=**−119.4 kW** (input 119.4; KE term 0.012 kW) | `p2()` |
| P3 | R-22, ṁ=0.07 kg/s, h₁=249.75, h₂=294.17, h₂ₛ=285.58 (adiabatic); find Ẇcv, η_c | Ẇcv=**−3.11 kW**, η_c=**0.81** (w 44.42 ≥ min 35.83) | `p3()` |
| P4 | h₁=241.35, h₂ₛ=272.39, η_c=0.80; find actual exit state | h₂=**280.15 kJ/kg**, w=**38.80 kJ/kg** (ideal 31.04) | `p4()` |

## Condenser & heat exchanger (Ch. 4 §4.9)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P5 | steam 0.1 bar, x=0.95 (hf=191.83, hg=2584.7) → 45 °C liquid (188.45); ṁ=125 kg/s | h_in=**2465.1**, q=**−2276.7 kJ/kg**, Q̇=**−284.6 MW** | `p5()` |
| P6 | hot 2465.1→188.45 kJ/kg vs cold Δh=62.7 kJ/kg; find ṁ_c/ṁ_h and ṁ_c at 125 kg/s | ratio=**36.3**, ṁ_c=**4539 kg/s** (balance closes) | `p6()` |
| P7 | air ṁ=4 kg/s, cp=1.005, 500→300 K heats water ṁ=8 kg/s, c=4.18, in 20 °C; find exit T | duty=**804 kW**, T_out=**44.0 °C** | `p7()` |

## Heat pump (Ch. 10)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P8 | Ex 10.4 cycle (h₁=242.54, h₂=280.19, h₃=h₄=105.29, ṁ=0.2 kg/s), 295 K in / 278 K out; find γ, rates, ceiling | Ẇ=**7.53**, Q̇_out=**34.98 kW**, γ=**4.65** < γ_max=**17.35** (γ=β+1) | `p8()` |

**Method.** Every device is the one-inlet/one-exit steady CV balance (Eq. 4.20a) with the
right terms kept: compressor → `Ẇcv = ṁ(h₁−h₂) < 0` (+ KE/heat-loss terms if given);
condenser / one exchanger side → `Q̇cv = ṁ(h_out−h_in)`; whole exchanger → Eq. 4.18 with
`Q̇cv = Ẇcv = 0`, fixing `ṁ_c/ṁ_h`. Real compressors are rated by `η_c = (h₂ₛ−h₁)/(h₂−h₁)`
(Eq. 6.48), whose inverse fixes the actual exit state. The heat-pump COP `γ = (h₂−h₃)/(h₂−h₁)`
obeys `γ = β + 1` and sits below the Carnot ceiling `γ_max = T_H/(T_H−T_C)`.

**Consistency checks** (in `test_homework.py`): the two ṁ forms agree (P1); the KE term is
negligible next to Δh (P2); `w_s ≤ w` and `0 < η_c ≤ 1` (P3); Eq. 6.48 round-trips (P4);
`hf ≤ h_in ≤ hg` and `q < 0` (P5); the whole-exchanger residual ≈ 0 (P6, P7); the first law
`Q̇_C + Ẇ = Q̇_H` closes, `γ = β + 1`, and `γ < γ_max` (P8).

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 34 tests passed."
```
