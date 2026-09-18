# 13.2 — Problems

Check with `code/supersonic.py`. Citations in `../refs.md`. `A/A*` and ratios
dimensionless; `T` [K], `p` per problem.

### P1.  Area–Mach relation (Table 9.2)  *(Moran 8e Eq. 9.52, p.578)*
For air (`k=1.4`), find `A/A*` at `M = 0.5`, `1.0`, and `2.0`.
*Answer:* `1.3398`, `1.0`, `1.6875` (note the same `A/A*>1` would also admit a subsonic
*and* a supersonic Mach number). *Check:* `area_mach_ratio(0.5, 1.4)` ≈ 1.3398;
`area_mach_ratio(2.0, 1.4)` ≈ 1.6875.

### P2.  Critical pressure & choking (Ex 9.14a)  *(Moran 8e Sec. 9.13.2/9.14.1, p.574/578)*
Air (`k=1.4`) enters a converging nozzle from a tank at `po = 1.0 MPa`. For what back
pressures is the nozzle choked? Is `pB = 500 kPa` choked?
*Answer:* `p* = (2/2.4)^3.5·po = 0.528·1000 = 528 kPa`; choked for `pB ≤ 528 kPa`. Since
`500 < 528`, **yes, choked** (exit `M=1`). *Check:* `critical_pressure_ratio(1.4)` ≈
0.528; `is_choked(500e3, 1.0e6, 1.4)` = `True`.

### P3.  Choked exit conditions and mass flow (Ex 9.14a)  *(Moran 8e §9.14, p.580)*
For the choked nozzle of P2 (`To=360 K`, exit area `A2=0.001 m²`, `R=287 J/kg·K`), find
`T2`, `V2`, and `ṁ`.
*Answer:* `T2 = T* = (2/2.4)·360 = 300 K`; `V2 = √(kRT2) = 347.2 m/s`;
`ṁ = p*A2V2/(RT2) = (528000)(0.001)(347.2)/(287·300) = 2.13 kg/s`. *Check:*
`critical_temperature_ratio(1.4)*360` ≈ 300; `speed_of_sound_ideal_gas(1.4, 287, 300)`
≈ 347.2.

### P4.  Supersonic exit of a C–D nozzle (Ex 9.15c)  *(Moran 8e Eqs. 9.51–9.52, p.584)*
A converging–diverging nozzle has `A2/A* = 2.4` and air (`k=1.4`) with `M=1` at the
throat. Find the supersonic exit Mach number and `p2/po`.
*Answer:* the supersonic root of `A/A*=2.4` is `M2 = 2.4`; `p2/po = 1/(1+0.2·2.4²)^3.5 =
0.0684`. With `po=100 lbf/in²`, `p2 = 6.84 lbf/in²`. *Check:*
`mach_from_area_ratio(2.4, 1.4, supersonic=True)` ≈ 2.4;
`1/stagnation_pressure_ratio(2.4, 1.4)` ≈ 0.0684.
