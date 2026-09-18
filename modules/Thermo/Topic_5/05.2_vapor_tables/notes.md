# 5.2 — Superheated Vapor Table (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Two independent properties fix the state
In the single-phase **superheated-vapor** region, pressure and temperature are
independent again [M §3.5.1, p.105], so the superheated table (A-4) is two-way: for each
listed pressure it tabulates `v, u, h, s` versus temperature. Each pressure block begins
with the **saturated-vapor** row (`Sat.`, at `Tsat(p)`) and then proceeds to higher
temperatures. The value in parentheses after the pressure in the table heading is the
corresponding saturation temperature.
*Check (M p.105):* A-4 gives `v(10.0 MPa, 600 °C) = 0.03837 m³/kg`.

## 2. Single interpolation
If only one variable is off-grid, interpolate linearly along that variable inside the
on-grid block [M §3.5.1, p.105]:
$$y=y_1+\frac{x-x_1}{x_2-x_1}\,(y_2-y_1).$$
*Check (M Fig. 3.7, p.106):* water vapor at `10 bar`, `215 °C`, between `200 °C`
(`v=0.2060`) and `240 °C` (`v=0.2275`):
`v = 0.2060 + (215−200)/40·(0.2275 − 0.2060) = 0.2141 m³/kg`.

## 3. Double interpolation
When **both** `p` and `T` are off-grid, do it twice [M §3.5.1, p.105]:
1. interpolate in `T` inside the lower-pressure block → `y(p_lo, T)`;
2. interpolate in `T` inside the higher-pressure block → `y(p_hi, T)`;
3. interpolate those two results in `p` → `y(p, T)`.
On a grid pressure step 3 is trivial, so the double routine reduces to the single one.
*Check (Problem 3.7c):* `v(1.4 MPa, 220 °C) = 0.1557 m³/kg` from the `1.0`/`1.5 MPa`
blocks.

## 4. Enthalpy consistency
A-4 lists `u`, `h`, `s` alongside `v`. Because `h ≡ u + pv` [M Eq. 3.4, §3.6.1, p.111],
the tabulated values must satisfy this identity (watch units: `p` in kPa × `v` in m³/kg →
kJ/kg). *Check (M p.112):* water at `0.10 MPa`, `120 °C`: `u=2537.3`, `v=1.793`, so
`h = 2537.3 + 100·1.793 = 2716.6 kJ/kg`, matching the table.

## Bridge
Outside the shaded low-pressure corner of the T–s/Mollier charts (`5.5`), both `T` and
`p` are needed to fix enthalpy; only at low pressure does `h ≈ h(T)` (the ideal-gas
limit). For the *liquid* side of the dome the same two-way table format reappears as the
compressed-liquid table A-5 — see `5.3`, where the saturated-liquid approximation often
replaces it.
