# 13.HP — Topic 13: Homework Problems (Moran Ch.9, compressible flow)

7 **compressible-flow problems** from Moran 8e Ch.9 (printed pp.601–603), each solved
from its given data. Moran has **no answer key** for end-of-chapter problems, so these
are *worked solutions*, reproduced by `code/homework.py` and checked (`test_homework.py`,
37 checks incl. choking-test and across-shock consistency). Citations in `refs.md`.

## Sound, stagnation, critical state
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 9.113 | sonic velocity (ideal gas) of (a) air 1000 K, (b) CO₂ 500 K, (c) He 300 K | c = √(kRT): 633.9, 348.9, 1019 m/s (light gas → fast sound) | `p9_113()` |
| 9.121 | show T*/To=2/(k+1), p*/po=(2/(k+1))^{k/(k−1)}; evaluate for Ex 9.14 | ratios 0.833, 0.528; T*=300 K, p*=528 kPa (= Ex 9.14) | `p9_121()` |

## Converging nozzles (choking)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 9.123 | mixture k=1.31, M=23, po=5 bar, To=700 K → 1 bar, A₂=30 cm²; T₂, V₂, ṁ | p*=2.72 bar>1 ⇒ **choked**; T₂=606 K, V₂=536 m/s, ṁ=2.00 kg/s | `p9_123()` |
| 9.124 | tank 120/600 °R → 60 lbf/in², A₂=1 in²; ṁ for (a) air, (b) CO₂, (c) Ar | (a) p*=63.4>60 choked, ṁ=2.61; (b) p*=66.4 choked, ṁ=3.10; (c) p*=58.5<60 **subsonic** M₂=0.979, ṁ=3.25 lb/s | `p9_124()` |
| 9.125 | air po=1.4 bar, To=280 K → 1 bar, A₂=0.0013 m²; ṁ, and ṁ if po→2 bar | (a) p*=0.74<1 subsonic, M₂=0.71, ṁ=0.404; (b) p*=1.06>1 **choked**, ṁ=0.628 kg/s | `p9_125()` |

## Normal shocks
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 9.136 | air shock px=0.5 bar, Tx=280 K, Mx=1.8; py, pox | My=0.617; py=1.807 bar; pox=2.873 bar | `p9_136()` |
| 9.137 | C–D nozzle, shock at exit, atm 14.7/520 °R, Mx=1.5, A₂=1.8 in²; pox, Tox, ṁ | px=5.98; pox=21.95 lbf/in²; Tox=571 °R (=Toy); ṁ=0.748 lb/s | `p9_137()` |

**Method.** First test **choking** of a converging nozzle: choked when pB ≤ p* =
(2/(k+1))^{k/(k−1)}·po; then the exit is sonic (M=1, p₂=p*, T₂=T*) and ṁ is maximal,
else the exit pressure equals pB and M₂ comes from inverting Eq. 9.51. Mass flow
ṁ = ρ₂A₂V₂ with ρ₂=p₂/(RT₂), V₂=M₂√(kRT₂). For a **normal shock** use Eqs. 9.53–9.55;
the stagnation temperature is unchanged (Tox=Toy) while pox drops (irreversible).

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 37 tests passed."
```
