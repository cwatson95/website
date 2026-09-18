# 13.3 — Problems

Check with `code/shock.py`. Citations in `../refs.md`. All ratios dimensionless;
`k = 1.4` (air) unless noted.

### P1.  Normal-shock functions at Mx = 2.0 (Table 9.3)  *(Moran 8e Eqs. 9.53–9.56, p.581)*
Air at `Mx = 2.0` passes through a normal shock. Find `My`, `py/px`, `Ty/Tx`, `poy/pox`.
*Answer:* `My = √((4+5)/(28−1)) = 0.5774`; `py/px = (1+1.4·4)/(1+1.4·0.333) = 4.500`;
`Ty/Tx = 1.6875`; `poy/pox = 0.7209`. *Check:* `mach_after_shock(2.0, 1.4)` ≈ 0.5774;
`shock_pressure_ratio(2.0, 1.4)` ≈ 4.500; `stagnation_pressure_ratio_across_shock(2.0, 1.4)`
≈ 0.7209.

### P2.  A shock always loses stagnation pressure  *(Moran 8e Sec. 9.14.2, p.581)*
Show that `poy/pox < 1` and `My < 1` for `Mx = 1.5` and `Mx = 2.0` (the second law forces
`sy > sx`, hence supersonic → subsonic and a stagnation-pressure drop).
*Answer:* `Mx=1.5`: `My=0.701`, `poy/pox=0.9298`; `Mx=2.0`: `My=0.577`, `poy/pox=0.7209`
— both `<1`, both subsonic downstream. *Check:* `mach_after_shock(1.5, 1.4) < 1` and
`stagnation_pressure_ratio_across_shock(1.5, 1.4)` ≈ 0.9298.

### P3.  Shock standing at the nozzle exit (Ex 9.15d)  *(Moran 8e §9.14.2, p.584)*
In a C–D nozzle the supersonic flow just upstream of an exit-plane shock is `Mx = 2.4`,
`px = 6.84 lbf/in²`. Find `My` and the exit (downstream) pressure `py`.
*Answer:* `My = 0.52`; `py/px = 6.5533`, so `py = 6.84·6.5533 = 44.82 lbf/in²`. *Check:*
`mach_after_shock(2.4, 1.4)` ≈ 0.523; `6.84*shock_pressure_ratio(2.4, 1.4)` ≈ 44.82.

### P4.  Shock inside the diverging section (Ex 9.15e)  *(Moran 8e §9.14.2, p.584)*
A shock stands where `Mx = 2.2`. Find `poy/pox` (which rescales the sonic area via
`A*x/A*y = poy/pox`).
*Answer:* `poy/pox = 0.62812`; the downstream sonic area grows by `1/0.62812`, so a
larger subsonic `A2/A*y` and exit Mach number result (Eq. 9.52, module `13.2`). *Check:*
`stagnation_pressure_ratio_across_shock(2.2, 1.4)` ≈ 0.62812;
`sonic_area_ratio_across_shock(2.2, 1.4)` ≈ 0.62812.
