# 13.4 — Problems  *(~CM, not from Moran 8e)*

Check with `code/laminar_flow.py`. **Cross-trunk fluid mechanics; no Moran citations.**
SI units: `ρ` [kg/m³], `V` [m/s], `D,L` [m], `μ` [Pa·s], `ΔP` [Pa].

### P1.  Reynolds number and regime  *(~CM; White Ch.6)*
Oil (`ρ=900`, `μ=0.4 Pa·s`) flows at `V=2 m/s` in a `D=0.05 m` pipe. Find `Re` and the
regime.
*Answer:* `Re = 900·2·0.05/0.4 = 225 < 2300` ⇒ **laminar**. *Check:*
`reynolds_number(900, 2, 0.05, 0.4)` = 225; `is_laminar(225)` = `True`.

### P2.  Laminar friction factor  *(~CM; White Eq. 6.12)*
For the flow in P1, find the Darcy friction factor.
*Answer:* `f = 64/Re = 64/225 = 0.2844`. *Check:* `friction_factor_laminar(225)` ≈ 0.2844.

### P3.  Pressure drop two ways  *(~CM; White Ch.6 / Munson Ch.8)*
For P1 over `L=10 m`, find `ΔP` from (a) Darcy–Weisbach with `f=64/Re` and (b) the
Hagen–Poiseuille law, and confirm they agree.
*Answer:* (a) `ΔP = f(L/D)(ρV²/2) = 0.2844·200·1800 = 102.4 kPa`; (b)
`ΔP = 32μLV/D² = 32·0.4·10·2/0.0025 = 102.4 kPa`. **Equal.** *Check:*
`pressure_drop_darcy(64/225, 10, 0.05, 900, 2)` ≈ `pressure_drop_hagen_poiseuille(0.4, 10, 2, 0.05)`
≈ 102400.

### P4.  Parabolic profile and mean velocity  *(~CM; White Sec. 6.4)*
For laminar pipe flow with centerline speed `u_max = 4 m/s`, give `u` at the wall and at
`r = R/2`, and the mean velocity.
*Answer:* `u(R) = 0`; `u(R/2) = 4(1−0.25) = 3 m/s`; `V = u_max/2 = 2 m/s`. *Check:*
`velocity_profile_parabolic(4, 0.0125, 0.025)` = 3.0; `mean_velocity_from_max(4)` = 2.0.
