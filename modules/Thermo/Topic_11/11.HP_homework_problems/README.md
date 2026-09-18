# 11.HP — Homework Problems (Topic 11)

Support module for **Topic 11 (Psychrometrics — Moist Air)**: 7 **psychrometric problems**
from Moran 8e Ch.12, solved and code-checked. Parallels the other topics' `HP` modules.

## Contents
- `problems.md` — the 7 problems (given → find → worked answer), grouped by type, each
  with its check call.
- `code/homework.py` — one function per problem, solved from the given data.
- `code/test_homework.py` — 48 checks: worked-solution values + physical consistency
  (dew point vs dry bulb, ω ordering for humidification vs dehumidification, mass-balance
  closure ṁ_w=ṁₐ(ω₂−ω₁), sign of Q).

## Note
Moran provides **no answer key** for these end-of-chapter problems; the answers are
*worked solutions* (checked-but-unofficial). Coverage: humidity ratio and dew point,
condensation by constant-pressure cooling and by isothermal compression, dew point of a
non-air carrier gas, two dehumidifiers (one refrigerant-coupled), a wet-bulb/dry-bulb
state determination via the adiabatic-saturation equation, and an adiabatic evaporative
cooler (humidification).

> Saturation pressures and h_f/h_g are Table A-2 (SI) / A-2E (English) reads, stated in
> each `homework.py` function. Dry-air enthalpy uses ha=cpa·T (cpa=1.005 kJ/kg·K or
> 0.24 Btu/lb·°R); T(K)=T(°C)+273, matching Moran's worked examples.

## Run
```bash
cd code
python3 homework.py
python3 test_homework.py     # -> "All 48 tests passed."
```

## Files
`problems.md`, `code/homework.py`, `code/test_homework.py`, `refs.md`.
