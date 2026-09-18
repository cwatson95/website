# 08.3 — Heat Exchanger (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. What a heat exchanger does
A **heat exchanger** moves energy between two (or more) streams. A **recuperator** keeps
the streams apart with a wall (counterflow / parallel / cross-flow tube-in-tube,
shell-and-tube, radiators); a **direct-contact** exchanger mixes them [M §4.9, p.195].
Condensers and evaporators are special single-stream cases (see `08.2`).

## 2. Whole-device energy balance
Draw the control volume around the **entire** exchanger, enclosing *both* streams. The
only work is flow work, so `Wdot_cv = 0`; the inter-stream heat transfer is now *internal*
and does not cross the boundary. With negligible KE/PE the multi-stream balance
[M Eq. 4.18, p.181] gives
$$0=\dot Q_{cv}-\dot W_{cv}+\dot m_h(h_{hi}-h_{ho})+\dot m_c(h_{ci}-h_{co}).$$
If the device is also externally adiabatic (`Qdot_cv = 0`) this becomes the clean statement
that **the hot stream gives up exactly what the cold stream takes up**:
$$\dot m_h\,(h_{hi}-h_{ho})=\dot m_c\,(h_{co}-h_{ci}).$$

## 3. The mass-flow ratio
Rearranging fixes the **mass-flow ratio** from enthalpies alone [M Ex 4.7, p.197]:
$$\frac{\dot m_c}{\dot m_h}=\frac{h_{hi}-h_{ho}}{h_{co}-h_{ci}}.$$
For an ideal-gas or incompressible stream with constant specific heat,
`dh = c(T_out − T_in)` (`code/sensible_enthalpy_change`), so the balance can be written in
temperatures.

*Check (M Ex 4.7, p.197):* condensing steam (hot: `h_hi = 2465.1`, `h_ho = 188.45 kJ/kg`)
against cooling water (cold: `h_co − h_ci = 62.7 kJ/kg`, i.e. 20 → 35 °C). Then
`ṁ_c/ṁ_h = (2465.1−188.45)/62.7 = 36.3`. With the steam-side flow `ṁ_h = 125 kg/s` the
cooling-water flow is `36.3 × 125 ≈ 4538 kg/s` — a lot of water per unit of steam.

`code/energy_balance_residual` evaluates the full balance (with optional `Qcv`, `Wcv`) and
returns ~0 at a consistent solution; `code/mass_flow_other` solves
`ṁ₁Δh₁ = ṁ₂Δh₂` for the unknown flow.

## Bridge
Look at only **one** side of this device and you recover the single-stream **condenser**
(`08.2`, `Q̇cv = ṁΔh`). String an evaporator, compressor, condenser and valve together and
the two heat exchangers become the cold-side and hot-side of the **heat pump / refrigerator**
of module `08.4`.
