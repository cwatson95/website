# 5.1 — Problems

Check with `code/sat_tables.py`. Citations in `../refs.md`. `v` [m³/kg], `T` [°C],
`p` [bar], `x` dimensionless. Saturation data read from `steam_tables/` A-2/A-3.

### P1.  Quality and specific volume  *(Moran 8e Eq. 3.2, p.108)*
A two-phase liquid–vapor mixture of water at `100 °C` has quality `x = 0.9`. Find `v`.
*Answer:* `v = vf + x(vg − vf) = 1.0435×10⁻³ + 0.9(1.673 − 1.0435×10⁻³) = 1.506 m³/kg`
(Moran's in-text value, p.108). *Check:*
`mixture(sat_T(100,"vf"), sat_T(100,"vg"), 0.9)` ≈ 1.506.

### P2.  Quality from specific volume  *(Moran 8e Eq. 3.2 inverted, p.108)*
Water at `150 °C` has `v = 0.1944 m³/kg`. Find the quality.
*Answer:* `vf=1.0905×10⁻³`, `vg=0.3928`; `x = (0.1944 − vf)/(vg − vf) = 0.494`
(this is state 3 of Moran Ex 3.4). *Check:*
`quality_from_v(0.1944, sat_T(150,"vf"), sat_T(150,"vg"))` ≈ 0.494.

### P3.  Interpolating a saturation property  *(Moran 8e §3.5.1, p.105)*
Estimate the saturated-vapor specific volume `vg` of water at `145 °C`.
*Answer:* between A-2 entries `vg(140)=0.5089` and `vg(150)=0.3928`,
`vg(145) = 0.5089 + (145−140)/10·(0.3928 − 0.5089) = 0.4509 m³/kg`. *Check:*
`sat_T(145, "vg")` ≈ 0.4509 (= `linear_interp(145,140,150,0.5089,0.3928)`).

### P4.  Rigid two-phase tank — Moran Ex 3.2  *(Moran 8e Eqs. 3.1–3.2, p.109)*
A rigid tank holds `V = 0.5 m³` of water, two-phase at `p₁ = 1 bar`, `x₁ = 0.5`. Heating
raises the pressure to `p₂ = 1.5 bar` (constant `v`). Find `T₁`, `T₂`, the total mass, and
the vapor mass at each state.
*Answer:* `v₁ = vf + 0.5(vg − vf) = 0.8475 m³/kg`; `T₁ = Tsat(1) = 99.63 °C`,
`T₂ = Tsat(1.5) = 111.4 °C`; `m = V/v₁ = 0.59 kg`; `mg₁ = x₁m = 0.295 kg`;
`x₂ = (v₁ − vf₂)/(vg₂ − vf₂) = 0.731`, `mg₂ = x₂m = 0.431 kg`. *Check:* see `code/sat_tables.py`
`_demo()` and `5.EP` `ex_3_2`.

### P5.  Phase determination from `(p, T)`  *(Moran Problem 3.6, p.152; decision tree p.109)*
Classify the phase of H₂O at: (a) `10 bar, 179.9 °C`; (b) `10 bar, 150 °C`;
(c) `0.5 bar, 100 °C`; (d) `50 bar, 20 °C`; (e) `1 bar, −6 °C`.
*Answer:* (a) two-phase (`Tsat(10)=179.9 °C`); (b) compressed liquid; (c) superheated
vapor (`Tsat(0.5)=81.3 °C < 100`); (d) compressed liquid; (e) solid (below triple point).
*Check:* `phase_pT(10,179.9)` = `"two-phase"`, `phase_pT(10,150)` = `"compressed liquid"`,
`phase_pT(0.5,100)` = `"superheated vapor"`, `phase_pT(50,20)` = `"compressed liquid"`,
`phase_pT(1,-6)` = `"solid"`.
