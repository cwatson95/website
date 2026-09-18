# 5.4 — Problems

Check with `code/pv_diagram.py`. Citations in `../refs.md`. `p` [kPa], `V` [m³],
`W` [kJ] (or `p` [kPa], `v` [m³/kg], `W/m` [kJ/kg]). Keep `p` in kPa so areas come out in kJ.

### P1.  Polytropic expansion work — Moran Ex 2.1  *(Moran 8e Example 2.1, p.51)*
A gas expands from `p₁ = 3 bar`, `V₁ = 0.1 m³` to `V₂ = 0.2 m³` along `pVⁿ = const`. Find
the work for (a) `n = 1.5`, (b) `n = 1.0`, (c) `n = 0`.
*Answer:* (a) `p₂ = p₁(V₁/V₂)¹·⁵ = 1.06 bar`, `W = (p₂V₂ − p₁V₁)/(1 − n) = 17.6 kJ`;
(b) `W = p₁V₁ ln(V₂/V₁) = 20.79 kJ`; (c) `W = p(V₂ − V₁) = 30 kJ`. *Check:*
`work_polytropic(300, 0.1, p_polytropic(300,0.1,0.2,1.5), 0.2, 1.5)` ≈ 17.6;
`work_isothermal_ideal_gas(300,0.1,0.2)` ≈ 20.79; `work_isobaric(300,0.1,0.2)` = 30.

### P2.  Trapezoid rule = closed form  *(Moran 8e Eq. 2.17, p.49)*
Verify the area-under-the-curve (trapezoid) integral over a finely sampled `n=1.5`
polytrope equals the closed-form work of P1(a).
*Answer:* both give `17.6 kJ` (the area interpretation of `∫p dV`). *Check:*
`work_pdV(*_polytropic_path(300,0.1,0.2,1.5))` ≈ `work_polytropic(...)`.

### P3.  Work is path-dependent  *(Moran 8e §2.2.5, p.49)*
Two paths join the same end states `(300 kPa, 0.1 m³) → (100 kPa, 0.2 m³)`: path A expands
at `300 kPa` then drops pressure at `0.2 m³`; path B drops pressure at `0.1 m³` then
expands at `100 kPa`. Compare the work.
*Answer:* `W_A = 300(0.2−0.1) = 30 kJ`, `W_B = 100(0.2−0.1) = 10 kJ`; different areas ⇒
**work is not a property**. *Check:* `work_pdV([300,300,100],[0.1,0.2,0.2])` = 30;
`work_pdV([300,100,100],[0.1,0.1,0.2])` = 10.

### P4.  Isobaric water-work — Moran Ex 3.4 process 1–2  *(Moran 8e Example 3.4, p.119)*
Water is cooled/compressed at constant `10 bar` from `v₁ = 0.3066` to `v₂ = 0.1944 m³/kg`.
Find `W/m`.
*Answer:* `W/m = p(v₂ − v₁) = (1000 kPa)(0.1944 − 0.3066) = −112.2 kJ/kg` (work **on** the
water). *Check:* `work_isobaric(1000, 0.3066, 0.1944)` ≈ −112.2.

### P5.  Vaporization work — Moran Ex 6.1  *(Moran 8e Example 6.1, p.304)*
Water vaporizes at constant `4.758 bar` (`150 °C`) from `vf = 1.0905×10⁻³` to
`vg = 0.3928 m³/kg`. Find `W/m`.
*Answer:* `W/m = p(vg − vf) = (475.8 kPa)(0.3928 − 1.0905×10⁻³) = 186.38 kJ/kg`. *Check:*
`work_isobaric(475.8, 1.0905e-3, 0.3928)` ≈ 186.38.
