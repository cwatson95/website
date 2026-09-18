# 1.2 — Problems

Work by hand from `ΔKE+ΔPE+ΔU = Q−W` and `W=∫p dV`, then check with
`code/closed_systems.py`. Citations verified — see `../refs.md`. Sign: `Q` in,
`W` out (work done *by* the system).

### P1.  Polytropic expansion/compression work  *(Moran 8e Example 2.1, p.50)*
Air in a piston–cylinder follows `pV^1.3 = const` from `p₁=100 kPa, V₁=1 m³` to
`V₂=0.5 m³`. Find `p₂` and the work `W = (p₂V₂−p₁V₁)/(1−n)`.
*Answer:* `p₂ = 100(1/0.5)^1.3 = 246.2 kPa`; `W = −77.05 kJ` (work in).
*Check:* `polytropic_pressure(100,1,0.5,1.3)` ≈ 246.2; `polytropic_work(100,1,0.5,1.3)`
≈ −77.05; and `pdv_work_trapz(lambda V:100*(1/V)**1.3, 1, 0.5)` agrees.

### P2.  Cooling a gas in a piston–cylinder  *(Moran 8e Example 2.2, p.64)*
The gas of P1 is compressed (so `W = −77.05 kJ`) while it also rejects
`Q = −50 kJ` of heat. With `ΔKE = ΔPE = 0`, find `ΔU`.
*Answer:* `ΔU = Q − W = −50 − (−77.05) = +27.05 kJ`.
*Check:* `work_done(Q=-50.0, dU=27.05)` ≈ −77.05; `heat_transfer(W=-77.05, dU=27.05)`
≈ −50; `energy_balance_residual(-50, -77.05, 27.05)` ≈ 0.

### P3.  Isothermal expansion of an ideal gas  *(Moran 8e §2.2.5 / Example 2.1(b), p.51)*
An ideal gas expands isothermally (`n=1`) from `100 kPa, 1 m³` to `2 m³`. Find the
work, and the heat (recall `ΔU=0` for an isothermal ideal gas, so `Q=W`).
*Answer:* `W = p₁V₁ ln(V₂/V₁) = 100(1)ln2 = 69.31 kJ`, and `Q = 69.31 kJ`.
*Check:* `polytropic_work(100,1,2,1)` ≈ 69.31; `heat_transfer(W=69.31, dU=0.0)` ≈ 69.31.

### P4.  Constant-pressure heating  *(Moran 8e §2.2.3, Eq. 2.17, p.48)*
A gas is heated at constant `p = 200 kPa`, expanding from `1 m³` to `3 m³`; its
internal energy rises by `ΔU = 300 kJ`. Find `W` and `Q`.
*Answer:* `W = p(V₂−V₁) = 200(2) = 400 kJ`; `Q = ΔU + W = 300 + 400 = 700 kJ`.
*Check:* `constant_pressure_work(200,1,3)` = 400; `heat_transfer(W=400, dU=300)` = 700;
and `polytropic_work(200,1,3,0)` = 400 (n=0 is constant pressure).

### P5.  Kinetic & potential terms  *(Moran 8e §2.1, Eqs. 2.5/2.10, p.43)*
A 2 kg system accelerates from rest to 10 m/s and rises 10 m. Find `ΔKE` and `ΔPE`.
*Answer:* `ΔKE = ½(2)(10²) = 100 J = 0.100 kJ`; `ΔPE = 2(9.81)(10) = 196.2 J = 0.196 kJ`.
*Check:* `delta_KE(2,0,10)` = 0.1; `delta_PE(2,0,10)` ≈ 0.196.
