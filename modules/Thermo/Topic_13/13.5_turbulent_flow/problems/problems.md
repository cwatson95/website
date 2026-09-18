# 13.5 — Problems  *(~CM, not from Moran 8e)*

Check with `code/turbulent_flow.py`. **Cross-trunk fluid mechanics; no Moran citations.**
SI units: `ρ` [kg/m³], `V` [m/s], `D,L,ε` [m], `μ` [Pa·s], `ΔP` [Pa].

### P1.  Reynolds number and regime  *(~CM; Cengel Ch.8)*
Water (`ρ=1000`, `μ=10⁻³ Pa·s`) flows at `V=2 m/s` in a `D=0.05 m` pipe. Find `Re` and
the regime.
*Answer:* `Re = 1000·2·0.05/10⁻³ = 10⁵ > 4000` ⇒ **turbulent**. *Check:*
`reynolds_number(1000, 2, 0.05, 1e-3)` = 1.0e5; `flow_regime(1e5)` = `"turbulent"`;
`is_turbulent(1e5)` = `True`.

### P2.  Blasius smooth-pipe friction factor  *(~CM; White Eq. 6.38)*
For the flow in P1 (smooth wall), estimate the Darcy friction factor with Blasius.
*Answer:* `f = 0.316/Re^{1/4} = 0.316/(10⁵)^{0.25} = 0.0178`. *Check:*
`friction_factor_blasius(1e5)` ≈ 0.01777. (Contrast the laminar `64/Re = 6.4×10⁻⁴` that
`13.4` would give at this `Re` — but the flow is *not* laminar here.)

### P3.  Roughness raises the friction factor (Colebrook/Moody)  *(~CM; White Eq. 6.48)*
For P1, compare the smooth-wall Colebrook `f` with the value at relative roughness
`ε/D = 0.001`.
*Answer:* smooth `f = 0.0180`; rough `f = 0.0222` — roughness raises it ~23%. *Check:*
`friction_factor_colebrook(1e5, 0.0)` ≈ 0.01799; `friction_factor_colebrook(1e5, 0.001)`
≈ 0.02217; `friction_factor_haaland(1e5, 0.001)` ≈ 0.02197 (Haaland ≈ Colebrook).

### P4.  Flatter turbulent profile  *(~CM; White Sec. 6.6)*
For the 1/n power-law profile with `n=7`, give the mean-to-peak velocity ratio and
contrast it with laminar.
*Answer:* `V/u_max = 2n²/((n+1)(2n+1)) = 2·49/(8·15) = 0.817`, vs the laminar `0.5` of
`13.4` — turbulence flattens the profile. *Check:* `mean_velocity_power_law(1.0, 7)` ≈
0.8167; `power_law_velocity_profile(10, 0, 0.05, 7)` = 10 (centerline), `(…, 0.05, …)` = 0 (wall).

### P5.  Pressure drop and head loss  *(~CM; Munson Ch.8)*
For P1 over `L=10 m` with smooth wall, find `ΔP` (Darcy–Weisbach) and confirm
`ΔP = ρg·h_L`.
*Answer:* `f = 0.0180`, `ΔP = f(L/D)(ρV²/2) = 0.0180·200·2000 ≈ 7.2 kPa`; head loss
`h_L = ΔP/ρg ≈ 0.734 m`. *Check:*
`pressure_drop_darcy(friction_factor_colebrook(1e5,0), 10, 0.05, 1000, 2)` ≈ 7196 Pa
`== 1000·9.80665·head_loss_darcy(…)`.
