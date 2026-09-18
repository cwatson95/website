# 5.HP — Topic 5: Homework Problems (Moran Ch.3 property data)

6 **property-evaluation** problems from Moran 8e Ch.3 (printed pp.152–153), each solved from
its given data with the Topic-5 steam-table tools (concept modules `5.1`–`5.3`). Moran has
**no answer key**, so these are *worked solutions*, reproduced by `code/homework.py` and
checked (`test_homework.py`, 26 checks incl. quality bounds and phase recovery). Citations in
`refs.md`. All problems use **water** and the project SI steam tables.

## Phase / state determination
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 3.6  | phase of H₂O at (a)10 bar,179.9 °C (b)10 bar,150 °C (c)0.5 bar,100 °C (d)50 bar,20 °C (e)1 bar,−6 °C | (a) two-phase (b) compressed liquid (c) superheated vapor (d) compressed liquid (e) solid | `p3_6()` |
| 3.14 | locate H₂O at 120 °C: (a)5 bar (b)v=0.6 m³/kg (c)1 bar; p_sat(120 °C)=1.985 bar | (a) compressed liquid (b) two-phase (c) superheated vapor | `p3_14()` |

## Table interpolation
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 3.7  | superheated vapor: (a) v at 240 °C, 1.25 MPa; (b) T at 1.5 MPa, v=0.1555; (c) v at 220 °C, 1.4 MPa | (a) **0.1879 m³/kg** (b) **260 °C** (c) **0.1557 m³/kg** | `p3_7()` |
| 3.13 | specific volume: (a) 400 °C, 20 MPa; (b) 40 °C, 20 MPa (A-5); (c) 40 °C, 2 MPa (approx) | (a) **9.940×10⁻³** (b) **9.992×10⁻⁴** (c) **1.0078×10⁻³ m³/kg** | `p3_13()` |

## Two-phase quality & rigid process
| # | given → find | answer | check |
|---|--------------|--------|-------|
| 3.15(a) | 4 kg water in a closed 1 m³ container at 100 °C; if two-phase, find quality | v=0.250 m³/kg → two-phase, **x=0.149** | `p3_15a()` |
| 3.23 | rigid tank, sat. vapor at 200 °C cooled to 100 °C; find p₁, p₂ | p₁=p_sat(200 °C)=**15.54 bar**; v₂=v₁ → two-phase, p₂=**1.014 bar**, x₂=0.076 | `p3_23()` |

**Method.** Phase at (p, T) compares T against T_sat(p) (Table A-2/A-3): T < T_sat → compressed
liquid, T > T_sat → superheated vapor, T = T_sat → two-phase; below the triple point → solid.
Phase at (T, v) compares v against v_f(T), v_g(T). Quality `x = (v − v_f)/(v_g − v_f)`.
Superheated values come from linear interpolation in Table A-4 (in p and T); compressed-liquid
v from Table A-5, or the approximation `v(T,p) ≈ v_f(T)` when off the A-5 grid. A rigid tank
holds v constant, so cooling at fixed v slides the state down a vertical line on the T–v diagram.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 26 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
