# 12.HP — Topic 12: Homework Problems (Moran Ch.13/14 + ~PK Saha leaf)

9 problems on combustion and reacting mixtures: **P1–P8** are Moran 8e end-of-chapter
problems (printed pp.867–871, 919, 921), each solved from its given data; **P9 is the
~PK Saha extension (NOT in Moran)**. Moran has **no answer key**, so all are *worked
solutions*, reproduced by `code/homework.py` and checked (`test_homework.py`, 64 checks
incl. element-balance closure, Σy = 1, K round-trips, steam-table dew-point brackets,
and the Saha ↔ Eq.-14.35 identity). Citations in `refs.md`. Enthalpies kJ/kmol; air =
O₂ + 3.76 N₂, `M_air = 28.97`; `p_ref = 1 atm`.

## Fuel stoichiometry & products (Ch. 13, §13.1)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P1 (13.2) | ethane C₂H₆ + theoretical air; AF̄, AF | a_O₂=3.5, AF̄=**16.66**, AF=**16.05** | `p1()` |
| P2 (13.7) | butane C₄H₁₀, φ=0.9; balanced eq., % excess air | O₂ supplied=**7.222** ⇒ +0.722 O₂, 27.16 N₂ in products; excess=**11.1%** (lean) | `p2()` |
| P3 (13.30) | hexane C₆H₁₄, dry analysis CO₂ 8.5 / CO 5.2 / O₂ 3 / N₂ 83.3%; balanced eq., % theo air, dew pt | per 100 kmol dry: a=**2.283** fuel, b=**22.09** O₂, c=**15.98** H₂O (N₂ closes to 0.3%); **101.8%** theo; y_v=0.1378 ⇒ dew pt **52.4 °C** | `p3()` |
| P4 (13.17) | dodecane C₁₂H₂₆ + 150% theo air; AF̄, AF, dew pt at 1 atm | AF̄=**132.1**, AF=**22.47** (M=170.33); y_v=0.0938 ⇒ dew pt **44.8 °C** | `p4()` |

## Heating values & adiabatic flame temperature (Ch. 13, §13.2–13.3)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P5 (13.59) | h̄_RP of gaseous pentane C₅H₁₂ at 25 °C, vapor water (+ liquid variant) | LHV form **−3,272,080** kJ/kmol = 45,351 kJ/kg; HHV form **−3,536,140** = 49,011 kJ/kg — regenerate Table A-25's 45,350/49,010 | `p5()` |
| P6 (13.51) | liquid propane (h°_f=−118,900, given) + air, both 25 °C, insulated reactor; T_P for (a) theo air, (b) 300% theo air | RHS=2,028,940 kJ/kmol; (a) **T ≈ 2381 K** (2350–2400 bracket), (b) **T ≈ 1152 K** (1140–1160 bracket); cf. octane 2395 K (Ex 13.8) | `p6()` |

## Chemical & ionization equilibrium (Ch. 14, §14.3–14.4)
| # | given → find | answer | check |
|---|--------------|--------|-------|
| P7 (14.32) | closed vessel, 1 CO + ½ O₂ at 1 atm, 300 K → equilibrium CO₂/CO/O₂ at 2500 K (K=0.0363); final p | Eq. 14.35 coupled to `p₂ = p₁(n₂/n₁)(T₂/T₁)`: z=**0.0741**, p₂=**5.76 atm**, y=(0.071, 0.036, **0.893**) — self-pressurization suppresses dissociation (z<0.129 of Ex 14.2) | `p7()` |
| P8 (14.67) | 1 kmol N at 12,000 K, 6 atm ionizes, 0.95 kmol N left; K for N ⇌ N⁺ + e⁻ | z=0.05, n=1.05: `K = [z²/(1−z²)](p/p_ref)` = **0.0150** (log₁₀K = −1.82) | `p8()` |
| P9 **(~PK, NOT Moran)** | Saha: hydrogen, χ=13.6 eV, g₊/g₀=½, n=10²³ m⁻³; x at 8/12/16 kK; Moran-form K | x = **0.0068 / 0.219 / 0.77** — the missing K(T) of Moran §14.4.3: K(12,000 K)=**0.0101** via `K = S·k_BT/p_ref`, and `z = √(K/(K+p/p_ref))` at `p = n(1+x)k_BT` reproduces x exactly (same order as P8's N-ionization K ≈ 0.015 at 12,000 K) | `p9()` |

**Method.** Balance each element (air = 4.76 kmol per kmol O₂; N₂ inert); AF̄→AF via
Eq. 13.2; a **dry** product analysis hides the water, so back it out from the H balance,
then `p_v = y_v p` and the dew point is `T_sat(p_v)` (Table A-2 rows 40–55 °C embedded).
Heating values are `|h_RP|` (Eq. 13.18) with liquid (HHV) or vapor (LHV) product water.
The adiabatic flame temperature solves `Σ_P n(Δh)_e = Σ_R n h°_f − Σ_P n h°_f`
(Eq. 13.21b) by bracketing with Table A-23 rows. Equilibrium problems use Eq. 14.35 —
in a **closed vessel** the pressure itself depends on the extent, so solve K(z, p₂(z))
self-consistently; ionization (§14.4.3) is the same K machinery with `A ⇌ A⁺ + e⁻`.
**P9 is flagged ~PK:** Moran cites statistical thermodynamics for ionization K values
but gives no formula — the Saha equation supplies it (physical-consistency checks only;
no book key).

## Run
```bash
cd code
python3 homework.py          # worked answers
python3 test_homework.py     # -> "All 64 tests passed."
```
