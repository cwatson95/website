# 10.HP — Topic 10: Homework Problems (Moran Ch.5/9)

8 problems on the Carnot and Stirling engines, each solved from complete given data by
`code/homework.py` and checked (`test_homework.py`, 45 checks incl. balance/consistency
and cross-checks vs `10.1`/`10.2`). Problems **1–3** are Moran 8e Ch.5 *Checking
Understanding* items (p.277); **6–8** build on the Ch.9 end-of-chapter Stirling problems
9.102–9.103 (p.601). Moran has **no worked key**, so all are *worked solutions*.
Citations in `refs.md`. Cycle `Q`, `W` are positive magnitudes (P8 signed per process);
`T` is absolute (K/°R).

## Carnot ceilings, claims, and extrema (Ch. 5)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P1 | (CU #24 + claim) cycle 1000 K↔400 K, Q_H=1000, Q_C=500 kJ; verdict. Inventor: Q_C=300 kJ | η=**0.50**<0.60 ⇒ **irreversible**; claim η=0.70 ⇒ **impossible** | `p1()` |
| P2 | (CU #23) Carnot η at T_H=1225 °C, T_C=298 K (Fig. 5.12 pt. b) | η_max=**0.801 (~80 %)** | `p2()` |
| P3 | (CU #17) Carnot gas cycle: p₁=3 atm, v₁=4.2 ft³/lb, p₄=1 atm; find v₄ | isotherm 4–1 ⇒ v₄=p₁v₁/p₄=**12.6 ft³/lb** | `p3()` |
| P4 | reversible cycle 745 K↔298 K, Q_H=1000 kJ; max W, min Q_C | η_max=0.60 ⇒ W_max=**600 kJ**, Q_C,min=**400 kJ** | `p4()` |
| P5 | freezer 268 K↔295 K removes 8000 kJ/h; min power; judge 800 kJ/h claim (Ex 5.2 QQ) | β_max=9.93 ⇒ Ẇ_min=**806 kJ/h (0.224 kW)**; claim β=10 ⇒ **invalid** | `p5()` |

## Stirling engine (Ch. 9 §9.8.4; Problems 9.102–9.103, p.601)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P6 | (9.102) 36 g air, r=6, p₁=1 bar, V₁=0.03 m³, T_H=1000 K; W_net, η, mep | T_C=290.4 K; W=**13.14 kJ**, η=**0.710**, mep=**5.25 bar** | `p6()` |
| P7 | (9.102 cont.) regenerator duty; η with no / 80 %-effective regenerator | Q_regen=18.34 kJ; η=**0.356 (none)** / **0.592 (80 %)** vs 0.710 ideal | `p7()` |
| P8 | (9.103) helium Stirling: 15→150 lbf/in² at 100 °F; expansion at 1500 °F; per-process W, Q; η vs Carnot | W₁₂=Q₁₂=**−639.4**, W₃₄=Q₃₄=**+2238.7**, Q₂₃=−Q₄₁=**1041.9 Btu/lb**; η=**0.714 = Carnot** | `p8()` |

**Method.** A claimed cycle is judged against η_max = 1 − T_C/T_H (Eq. 5.9): above the
ceiling is impossible, equal is reversible, below is irreversible; the same corollaries
give W_max = η_max·Q_H, Q_C,min = Q_H·T_C/T_H (Eq. 5.7) and Ẇ_min = Q̇_C/β_max
(Eq. 5.10). The Stirling isothermals carry Q = W = mRT ln r (Eq. 2.17 form) and the
constant-volume legs c_v(T_H−T_C) (Eq. 3.50 form): with ideal regeneration those legs
cancel and η = W/Q₃₄ = 1 − T_C/T_H — the Carnot value (§9.8.4) — while without a
regenerator that heat becomes an external input and η collapses (P7); mep = W_net per
displacement volume (Eq. 9.1).

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 45 tests passed."
```
