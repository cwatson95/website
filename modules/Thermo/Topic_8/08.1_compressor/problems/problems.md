# 08.1 — Problems

Check with `code/compressor.py`. Citations in `../refs.md`. SI energy-balance calls use
`h` [J/kg], `V` [m/s], power [W]; efficiency calls use enthalpy *differences* (kJ/kg ok).

### P1.  Mass flow from inlet data  *(Moran 8e Eq. 4.4b, p.172)*
Air enters a compressor inlet of area `A1 = 0.1 m²` at `p1 = 1 bar`, `T1 = 290 K`,
`V1 = 6 m/s`. Find `ṁ` (air `R = 287 J/kg·K`).
*Answer:* `ṁ = A1V1p1/(RT1) = (0.1)(6)(10⁵)/(287·290) = 0.72 kg/s`. *Check:*
`mass_flow_rate_ideal_gas(0.1, 6, 1.0e5, 8314/28.97, 290)` ≈ 0.72.

### P2.  Air-compressor power (Ex 4.5)  *(Moran 8e Eq. 4.20a, p.191)*
Continue P1: exit at 7 bar, 450 K, 2 m/s; heat transfer `Q̇ = −180 kJ/min`.
`h1 = 290.16`, `h2 = 451.80 kJ/kg` (Table A-22). Find the power input.
*Answer:* `Ẇcv = Q̇ + ṁ[(h1−h2)+(V1²−V2²)/2] = −3 + 0.72(−161.64) + 0.012 = −119.4 kW`;
power **input** = 119.4 kW. *Check:* with the book's `ṁ=0.72`,
`power_input(0.72, 290.16e3, 451.80e3, Qdot=-180e3/60, V1=6, V2=2, g=0)/1e3` ≈ 119.4.

### P3.  Isentropic compressor efficiency (Ex 6.14)  *(Moran 8e Eq. 6.48, p.338)*
R-22 is compressed adiabatically from `h1 = 249.75` to `h2 = 294.17 kJ/kg`; the isentropic
exit at the same pressure is `h2s = 285.58 kJ/kg`. Find `η_c`.
*Answer:* `η_c = (h2s−h1)/(h2−h1) = 35.83/44.42 = 0.81 (81%)`. *Check:*
`isentropic_efficiency(249.75, 294.17, 285.58)` ≈ 0.81.

### P4.  Real exit state from η_c  *(Moran 8e Eq. 6.48 rearranged, p.338)*
A compressor with `η_c = 0.80` takes a refrigerant from `h1 = 241.35 kJ/kg`; the
isentropic exit at the discharge pressure is `h2s = 272.39 kJ/kg`. Find the *actual* exit
enthalpy and the actual specific work.
*Answer:* `h2 = h1 + (h2s−h1)/η_c = 241.35 + 31.04/0.80 = 280.15 kJ/kg`; actual work
`h2−h1 = 38.80 kJ/kg` (vs. isentropic 31.04). *Check:*
`exit_enthalpy_from_efficiency(241.35, 272.39, 0.80)` ≈ 280.15. (These are the state-2
values of Moran Ex 10.3.)
