# 2.2 — Problems

Check with `code/expansion_work.py`. Citations in `../refs.md`.

### P1.  Constant-pressure expansion  *(Moran 8e Eq. 2.17, p.48)*
A gas at constant 200 kPa expands 1 → 1.5 m³. Find the work.
*Answer:* `W = p(V₂−V₁) = 200(0.5) = 100 kJ`.
*Check:* `constant_pressure_expansion(200,1,1.5)` = 100.

### P2.  Isothermal expansion  *(Moran 8e Example 2.1b, p.51)*
An ideal gas expands isothermally from 100 kPa, 1 m³ to 2 m³. Find the work.
*Answer:* `W = p₁V₁ ln(V₂/V₁) = 100·ln2 = 69.31 kJ`.
*Check:* `isothermal_expansion(100,1,2)` ≈ 69.31.
