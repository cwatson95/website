# 6.1 — Problems

Check with `code/reversible.py`. Citations in `../refs.md`. `T` absolute (K/°R);
`s` [kJ/kg·K]; `Q,W` [kJ or kJ/kg as noted].

### P1.  Water, internally reversible at 150 °C (Ex 6.1)  *(Moran 8e §6.6.3, p.303–304)*
Water (closed system) goes from saturated liquid to saturated vapor at 150 °C
(423.15 K) by an **internally reversible**, constant-`p`, constant-`T` heating. From
Table A-2: `p = 4.758 bar`, `v₁ = 1.0905×10⁻³`, `v₂ = 0.3928 m³/kg`, `s₁ = 1.8418`,
`s₂ = 6.8379 kJ/kg·K`. Find `W/m` and `Q/m`.
*Answer:* `W/m = p(v₂−v₁) = 475.8(0.3917) = 186.38 kJ/kg`;
`Q/m = T(s₂−s₁) = 423.15(4.9961) = 2114.1 kJ/kg` (area under the T–s line). *Check:*
`work_const_pressure(475.8, 0.3928, 1.0905e-3)` ≈ 186.38; `heat_int_rev_isothermal(423.15, 6.8379, 1.8418)` ≈ 2114.1.

### P2.  Same change at 100 °C (Ex 6.1 Quick Quiz)  *(Moran 8e §6.6.3, p.304)*
Repeat P1 for saturation states at 100 °C (373.15 K): `s₁ = 1.3069`, `s₂ = 7.3549 kJ/kg·K`.
*Answer (book):* `W/m ≈ 170 kJ/kg`, `Q/m ≈ 2257 kJ/kg`. *Check:*
`heat_int_rev_isothermal(373.15, 7.3549, 1.3069)` ≈ 2257.

### P3.  Isothermal reversible work of an ideal gas (HW 6.24)  *(Moran 8e §6, p.348)*
A gas in a piston–cylinder undergoes an **internally reversible isothermal** process at
`T = 400 K` during which `ΔS = −0.3 kJ/K`. Ideal gas, KE/PE negligible. Find the work.
*Answer:* `Q = ∫T dS = T·ΔS = 400(−0.3) = −120 kJ`; for an ideal gas `ΔU = 0` (isothermal),
so `W = Q − ΔU = −120 kJ` (work *on* the gas). *Check:*
`heat_int_rev_isothermal(400, -0.3, 0.0)` = −120; then `W = Q`.

### P4.  Carnot power cycle from a T–s rectangle (HW 6.30)  *(Moran 8e §6, p.349)*
0.1 kg of gas runs a **Carnot power cycle**; isothermal expansion at 800 K, isothermal
compression at 400 K with specific-entropy change `−25 kJ/kg·K`. Find (a) net work per
cycle and (b) thermal efficiency.
*Answer:* the two isothermals are equal-and-opposite on T–s, so `|Δs| = 25 kJ/kg·K`. Net
work = enclosed rectangle = `(T_H−T_C)|Δs|·m = (800−400)(25)(0.1) = 1000 kJ`; `η = 1 −
T_C/T_H = 1 − 400/800 = 0.50`. *Check:* `heat_int_rev_isothermal(800,25,0)*0.1` = 2000 kJ
in; `carnot_eff_ts(800,400)` = 0.50 → `W = 0.50·2000·... ` net 1000 kJ.
