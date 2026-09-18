# 6.3 — Problems

Check with `code/adiabatic.py`. Citations in `../refs.md`. `T` absolute (K/°R);
air `R = 8.314/28.97 kJ/kg·K`. Isentropic ⇒ adiabatic + internally reversible.

### P1.  Isentropic process of air (Ex 6.9)  *(Moran 8e §6.11.3, p.329–330)*
Air undergoes an **isentropic** process from `p₁ = 1 atm`, `T₁ = 540 °R` to `T₂ = 1160 °R`.
Find `p₂`. Solve (a) with `p_r` data and (c) with constant `k = 1.39` (at the mean 850 °R).
*Answer:* (a) `p₂ = p₁·p_r2/p_r1 = 1·(21.18/1.3860) = 15.28 atm`; (c) `p₂ =
p₁(T₂/T₁)^{k/(k−1)} = (1160/540)^{1.39/0.39} = 15.26 atm`. *Check:*
`p2_from_pr(1, 1.3860, 21.18)` ≈ 15.28; `final_pressure_isentropic(540, 1160, 1, 1.39)` ≈ 15.26.

### P2.  Air leaking from a rigid insulated tank (Ex 6.10)  *(Moran 8e §6.11.3, p.330–331)*
A rigid, insulated tank holds 5 kg of air at 5 bar, 500 K. A slow leak drops the pressure
to 1 bar. The air remaining undergoes an **isentropic** process (`Δs = 0`). Find the mass
remaining and its temperature.
*Answer:* `p_r2 = (p₂/p₁)p_r1 = (1/5)(8.411) = 1.6822` ⇒ `T₂ = 317 K` (Table A-22);
`m₂ = (p₂/p₁)(T₁/T₂)m₁ = (1/5)(500/317)(5) = 1.58 kg`. *Check:*
`pr2_isentropic(8.411, 1, 5)` ≈ 1.6822; `m2 = (1/5)(500/317)(5)` ≈ 1.58.

### P3.  Turbine work from isentropic efficiency (Ex 6.11)  *(Moran 8e §6.12.1, p.333–334)*
Steam enters a turbine at `p₁ = 5 bar`, `T₁ = 320 °C` and leaves at 1 bar; adiabatic,
ΔKE/ΔPE ≈ 0, isentropic efficiency 75%. Find the work per unit mass.
*Answer:* `h₁ = 3105.6`, `s₁ = 7.5308`; for the isentropic exit (`s₂s = s₁`, 1 bar)
`h₂s = 2743.0 kJ/kg`. `W/m = η_t(h₁−h₂s) = 0.75(3105.6−2743.0) = 271.95 kJ/kg`. *Check:*
`0.75*(3105.6-2743.0)` ≈ 271.95.

### P4.  Evaluating turbine isentropic efficiency (Ex 6.12)  *(Moran 8e §6.12.1, p.334–335)*
Air enters an adiabatic turbine at `p₁ = 3.0 bar`, `T₁ = 390 K` and exits at `p₂ = 1.0 bar`;
the measured work is 74 kJ/kg. Find `η_t`.
*Answer:* `h₁ = 390.88`, `p_r1 = 3.481`; `p_r(T₂s) = (1/3)(3.481) = 1.1603` ⇒ `h₂s = 285.27
kJ/kg`, so `(W/m)_s = 105.6 kJ/kg` and `η_t = 74/105.6 = 0.70`. *Check:*
`isentropic_turbine_eff(390.88, 390.88-74, 285.27)` ≈ 0.70.
