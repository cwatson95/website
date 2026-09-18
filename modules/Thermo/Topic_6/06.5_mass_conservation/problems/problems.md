# 6.5 — Problems

Check with `code/mass_conservation.py`. Citations in `../refs.md`. `ṁ` [kg/s], `A` [m²],
`V` [m/s], `v` [m³/kg].

### P1.  Feedwater heater, steady state (Ex 4.1)  *(Moran 8e §4.3.1, p.174–175)*
A feedwater heater (2 inlets, 1 exit) operates at steady state. Inlet 1: water vapor,
`ṁ₁ = 40 kg/s`. Exit 3: saturated liquid at 7 bar with `(AV)₃ = 0.06 m³/s`
(`v₃ = 1.108×10⁻³ m³/kg`). Inlet 2: `A₂ = 25 cm²`, `v₂ ≈ vf(40 °C) = 1.0078×10⁻³`.
Find `ṁ₃`, `ṁ₂`, and `V₂`.
*Answer:* `ṁ₃ = (AV)₃/v₃ = 54.15 kg/s`; steady ⇒ `ṁ₂ = ṁ₃ − ṁ₁ = 14.15 kg/s`;
`V₂ = ṁ₂v₂/A₂ = 5.7 m/s`. *Check:* `mdot_from_volumetric(0.06, 1.108e-3)` ≈ 54.15;
`velocity_from_mdot(14.15, 1.0078e-3, 25e-4)` ≈ 5.7.

### P2.  Barrel filling — transient to steady (Ex 4.2)  *(Moran 8e §4.3.2, p.175–176)*
Water enters an open barrel at `ṁi = 30 lb/s`; it drains at `ṁe = 9L` (L = liquid
height, ft). Find the steady height.
*Answer:* `dm_cv/dt = ṁi − ṁe` (Eq 4.2). At steady state `dL/dt = 0 ⇒ 9L = 30 ⇒
L = 3.33 ft`. *Check:* `30.0/9.0` ≈ 3.333; `dmcv_dt([30.0],[9*3.333])` ≈ 0.

### P3.  Liquid-water duct (HW 4.15)  *(Moran 8e §4, p.221)*
Liquid water at 20 °C flows steadily through a one-inlet/one-exit duct. Inlet
`D₁ = 0.02 m`, `V₁ = 40 m/s`; exit `D₂ = 0.04 m`. `v ≈ vf(20 °C) = 1.0018×10⁻³ m³/kg`.
Find `ṁ` and the exit velocity `V₂`.
*Answer:* `A₁ = πD₁²/4 = 3.1416×10⁻⁴ m²`, `ṁ = A₁V₁/v = 12.54 kg/s`. Incompressible
+ steady ⇒ `A₂V₂ = A₁V₁`; with `A₂ = 4A₁`, `V₂ = V₁/4 = 10.0 m/s`. *Check:*
`mass_flow_rate(3.1416e-4, 40, 1.0018e-3)` ≈ 12.54.

### P4.  Air control volume — exit area (HW 4.16)  *(Moran 8e §4, p.221)*
Air (ideal gas, `R = 0.287 kJ/kg·K`) enters a 1-inlet/1-exit CV at 6 bar, 500 K,
30 m/s through `A₁ = 28 cm²`. It exits at 3 bar, 456.5 K, 300 m/s. Steady state. Find
`ṁ` and the exit area `A₂`.
*Answer:* `v₁ = RT₁/p₁ = 0.2392 m³/kg`, `ṁ = A₁V₁/v₁ = 0.351 kg/s`;
`v₂ = RT₂/p₂ = 0.4367 m³/kg`, `A₂ = ṁv₂/V₂ = 5.11×10⁻⁴ m² = 5.11 cm²`. *Check:*
`mass_flow_rate(28e-4, 30, 0.2392)` ≈ 0.351; `velocity` inversion gives `A₂` via `ṁv₂/V₂`.
