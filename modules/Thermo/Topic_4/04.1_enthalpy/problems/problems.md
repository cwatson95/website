# 4.1 — Problems

Check with `code/enthalpy.py`. Citations in `../refs.md`. Units: `h,u` [kJ/kg],
`p` [kPa], `v` [m³/kg].

### P1.  Enthalpy from u, p, v  *(Moran 8e Eq. 3.4, p.111)*
Water at 0.10 MPa has `u = 2537.3 kJ/kg` and `v = 1.793 m³/kg`. Find `h`.
*Answer:* `h = u + pv = 2537.3 + (100)(1.793) = 2716.6 kJ/kg` (matches Table A-4).
*Check:* `enthalpy(2537.3, 100, 1.793)` ≈ 2716.6.

### P2.  Quality from enthalpy  *(Moran 8e Eq. 3.7, p.112)*
A liquid–vapor mixture has `h = 156.67 kJ/kg` with `hf = 59.35`, `hg = 253.99`. Find
the quality, and the corresponding `u` if `uf = 58.77`, `ug = 230.38`.
*Answer:* `x = (156.67−59.35)/(253.99−59.35) = 0.5`; `u = 58.77 + 0.5(230.38−58.77) =
144.6 kJ/kg`. *Check:* `quality_from_enthalpy(156.67,59.35,253.99)` = 0.5;
`internal_energy_from_quality(58.77,230.38,0.5)` ≈ 144.6.

### P3.  Constant-pressure heating (HW 3.70)  *(Moran 8e §3.6.1, p.111)*
5 kg of water at 5 bar, 240 °C (`h₁ = 2939.9 kJ/kg`) is heated at constant pressure
until `h₂ = 3531.9 kJ/kg`. Find the heat transfer.
*Answer:* at constant `p`, `Q = m(h₂−h₁) = 5(3531.9−2939.9) = 2960 kJ`. *Check:*
`const_pressure_heat(2939.9, 3531.9, 5)` = 2960.

### P4.  Why enthalpy only at constant pressure  *(Moran 8e §3.6.1, p.111; Ex 3.3)*
A rigid (constant-volume) tank of water is stirred/heated. Should you use `Δh` or
`Δu` for the heat transfer? Why?
*Answer:* use `Δu`. At constant volume there is no boundary work (`W=0`), so
`Q = ΔU`; enthalpy's advantage (`Q=ΔH`) applies only when `pΔV` work is present, i.e.
at constant pressure. (This is exactly Moran Ex. 3.3, where `W=−31.3 Btu` comes from
paddle work, and `Q=0`.)
