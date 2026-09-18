# 5.3 — Problems

Check with `code/liquid_tables.py`. Citations in `../refs.md`. `v` [m³/kg], `u,h` [kJ/kg],
`T` [°C], `p` [bar]. Liquid data read from `steam_tables/` A-5 (and A-2 for `f`).

### P1.  Compressed liquid from A-5  *(Moran 8e §3.5.1, p.105)*
Find `v`, `u`, `h` of water at `100 bar` (10 MPa), `100 °C`.
*Answer (A-5):* `v = 1.0385×10⁻³ m³/kg`, `u = 416.12 kJ/kg`, `h = 426.50 kJ/kg`. *Check:*
`compressed(100,100,"v")` ≈ 1.0385e-3, `compressed(100,100,"u")` ≈ 416.12,
`compressed(100,100,"h")` ≈ 426.50.

### P2.  Saturated-liquid approximation for `v`, `u`  *(Moran 8e Eqs. 3.11–3.12, p.123)*
Approximate the same state with saturated-liquid data at `100 °C`. How close to P1?
*Answer:* `vf(100)=1.0435×10⁻³`, `uf(100)=418.94`; both within `~0.5–0.7 %` of the A-5
values. *Check:* `v_approx(sat_liquid(100)["vf"])` ≈ 1.0435e-3 (≈ `compressed(100,100,"v")`
to <1 %); `u_approx(sat_liquid(100)["uf"])` ≈ 418.94.

### P3.  Pressure-corrected enthalpy  *(Moran 8e Eqs. 3.13–3.14, p.123)*
Approximate `h` at `100 bar`, `100 °C` with Eq. 3.13, then with Eq. 3.14, and compare to
the A-5 value `426.50`.
*Answer:* `psat(100 °C)=1.014 bar`; `h ≈ hf + vf(p − psat) = 419.04 +
1.0435×10⁻³·(10000 − 101.4) = 429.4 kJ/kg` (within ~3 of the table); the bare
`h ≈ hf = 419.0` is ~1.7 % low. *Check:*
`h_approx(419.04, 1.0435e-3, 10000, 101.4)` ≈ 429.4; `h_approx_simple(419.04)` = 419.04.

### P4.  Specific volume of water — Problem 3.13(b,c)  *(Moran 8e Problem 3.13, p.152)*
Find `v` of water at (b) `40 °C, 20 MPa` and (c) `40 °C, 2 MPa`.
*Answer:* (b) A-5 at `200 bar, 40 °C`: `v = 0.9992×10⁻³ m³/kg`. (c) `20 bar` is below the
A-5 grid, so approximate `v ≈ vf(40 °C) = 1.0078×10⁻³ m³/kg`. *Check:*
`compressed(200,40,"v")` ≈ 0.9992e-3; `v_approx(sat_liquid(40)["vf"])` ≈ 1.0078e-3.

### P5.  Weak pressure dependence of liquid `v`  *(Moran 8e §3.10.1, p.123)*
At `40 °C`, compare `v` at `25 bar` and `200 bar` (A-5).
*Answer:* `v(25 bar)=1.0067×10⁻³`, `v(200 bar)=0.9992×10⁻³`; the change is `< 1 %` over an
eightfold pressure rise — the justification for Eq. 3.11. *Check:*
`abs(compressed(200,40,"v") − compressed(25,40,"v"))/compressed(25,40,"v") < 0.01`.
