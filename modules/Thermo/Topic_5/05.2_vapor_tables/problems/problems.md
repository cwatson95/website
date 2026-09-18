# 5.2 — Problems

Check with `code/vapor_tables.py`. Citations in `../refs.md`. `v` [m³/kg], `T` [°C],
`p` [bar]. Superheated data read from `steam_tables/` A-4.

### P1.  Single interpolation (Moran Fig. 3.7)  *(Moran 8e §3.5.1, p.106)*
Find the specific volume of superheated water vapor at `10 bar`, `215 °C`.
*Answer:* between `200 °C` (`v=0.2060`) and `240 °C` (`v=0.2275`),
`v = 0.2060 + (215−200)/40·(0.2275 − 0.2060) = 0.2141 m³/kg`. *Check:*
`superheated(10, 215, "v")` ≈ 0.2141.

### P2.  Interpolating in pressure — Problem 3.7(a)  *(Moran 8e §3.5.1, p.152)*
Estimate `v` at `T = 240 °C`, `p = 1.25 MPa` (12.5 bar).
*Answer:* between `1.0 MPa` (`v=0.2275`) and `1.5 MPa` (`v=0.1483`) at `240 °C`,
`v = 0.2275 + (12.5−10)/5·(0.1483 − 0.2275) = 0.1879 m³/kg`. *Check:*
`superheated(12.5, 240, "v")` ≈ 0.1879.

### P3.  Inverse interpolation — Problem 3.7(b)  *(Moran 8e §3.5.1, p.152)*
Find the temperature at `p = 1.5 MPa`, `v = 0.1555 m³/kg`.
*Answer:* between `240 °C` (`v=0.1483`) and `280 °C` (`v=0.1627`),
`T = 240 + (0.1555 − 0.1483)/(0.1627 − 0.1483)·40 = 260 °C`. *Check:*
`linear_interp(0.1555, 0.1483, 0.1627, 240, 280)` ≈ 260.

### P4.  Double interpolation — Problem 3.7(c)  *(Moran 8e §3.5.1, p.152)*
Estimate `v` at `T = 220 °C`, `p = 1.4 MPa` (14 bar) — both off-grid.
*Answer:* interpolate in `T` first: at `1.0 MPa`, `v(220)=0.2168`; at `1.5 MPa`,
`v(220)=0.1404`. Then in `p` at `1.4 MPa`: `v = 0.2168 + (14−10)/5·(0.1404 − 0.2168)
= 0.1557 m³/kg`. *Check:* `superheated(14, 220, "v")` ≈ 0.1557.

### P5.  Enthalpy consistency  *(Moran 8e Eq. 3.4, p.112)*
At `0.10 MPa` (1 bar), `120 °C`, A-4 gives `u = 2537.3 kJ/kg`, `v = 1.793 m³/kg`. Verify
the tabulated `h = 2716.6 kJ/kg`.
*Answer:* `h = u + pv = 2537.3 + (100 kPa)(1.793) = 2716.6 kJ/kg`. *Check:*
`enthalpy(superheated(1,120,"u"), 100, superheated(1,120,"v"))` ≈ 2716.6 ≈ `superheated(1,120,"h")`.
