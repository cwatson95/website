# 4.1 — Enthalpy (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Defining enthalpy
The sum of internal energy and the `pV` product appears repeatedly, so it is given
its own name and symbol [M §3.6.1, p.111]:
$$H=U+pV\quad(3.3),\qquad h=u+pv\quad(3.4),\qquad \bar h=\bar u+p\bar v\quad(3.5).$$
Because `U`, `p`, `V` are properties, so is `H`. Units here: `u,h` [kJ/kg], `p` [kPa],
`v` [m³/kg] (so `pv` is in kJ/kg).

## 2. Why it matters: constant-pressure heat & flow work
For a closed system at **constant pressure**, the energy balance gives
$$Q=\Delta U+W=\Delta U+p\,\Delta V=\Delta(U+pV)=\Delta H,$$
so `Q = m(h₂−h₁)`. Enthalpy is therefore the natural "heat content" for
constant-pressure processes. (At constant *volume*, `W=0` and `Q=ΔU` — use `u`, not
`h`; cf. Moran Ex. 3.3, a rigid tank.) The same `h` also accounts for the energy
carried by **flowing** mass across a control volume (Topic 6), where the `pv` term
is the *flow work*.

## 3. Enthalpy (and u) in the two-phase region
Inside the vapor dome a liquid–vapor mixture's properties are `x`-weighted
(`x` = quality, module `4.4`) [M §3.6.2, p.112]:
$$u=u_f+x\,u_{fg}\quad(3.6),\qquad h=h_f+x\,h_{fg}\quad(3.7),$$
with `u_fg = u_g − u_f`, `h_fg = h_g − h_f`. Solve for `x` to read quality from a
measured `h`: `x = (h−h_f)/h_{fg}`.

*Check 1:* water at 0.10 MPa with `u=2537.3` kJ/kg, `v=1.793` m³/kg gives
`h = 2537.3 + (100 kPa)(1.793) = 2716.6` kJ/kg, matching Table A-4.
*Check 2:* R-22 at 12 °C with `u=144.58` → `x=(144.58−58.77)/(230.38−58.77)=0.5`,
then `h = 59.35 + 0.5(253.99−59.35) = 156.67` kJ/kg.

## Bridge
`h` is the energy variable for control-volume / steady-flow analysis (Topic 6),
appears in the **2nd T dS equation** `T ds = dh − v dp` (module `4.2`), and its `pV`
structure recurs in the **exergy** transfer-with-work term (module `4.3`). The
`hf/hfg/hg` columns come from the saturation tables (Topic 5).
