# 4.4 — Phase change & quality (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The two-phase region needs a second property
Along the liquid–vapor saturation line, `T` and `p` are **not independent** — fixing
one fixes the other (the Gibbs phase rule gives `F=1` here, module `4.5`). So a
single `T` or `p` does not pin down the state inside the dome. The missing intensive
property is the **quality** [M §3.3, p.102]:
$$x=\frac{m_{vapor}}{m_{liquid}+m_{vapor}}\quad(3.1),\qquad 0\le x\le 1,$$
with `x=0` at saturated liquid and `x=1` at saturated vapor.

## 2. The universal mixture relation
Any specific property of the mixture is the saturated-liquid value plus `x` times the
evaporation increment (subscript `fg`) [M §3.5.2/3.6.2, p.108/112; §6.2.2, p.294]:
$$v=v_f+x\,v_{fg},\quad u=u_f+x\,u_{fg},\quad h=h_f+x\,h_{fg},\quad s=s_f+x\,s_{fg},$$
all "identical in form" (Moran's phrasing). One function, `mixture_property(yf,yg,x)`,
serves all four; invert it to **find** quality from a measured property,
`x = (y−y_f)/y_{fg}`.

## 3. Latent heat
`h_{fg} = h_g − h_f` is the **latent heat of vaporization** — the heat per unit mass to
convert saturated liquid to saturated vapor at fixed `T,p`. It shrinks as pressure
rises toward the critical point (where `h_{fg}→0`).

*Check 1:* water at 100 °C, `x=0.9`: `v = 1.0435×10⁻³ + 0.9(1.673−1.0435×10⁻³) =
1.506 m³/kg`. `h_{fg}(100 °C) = 2676.1 − 419.04 = 2257 kJ/kg`.
*Check 2 (HW 3.16):* a 1 m³ tank of CO₂ at `x=0.7` (`vf=0.983×10⁻³`, `vg=1.756×10⁻²`):
`v=0.01259`, `m=79.4 kg`, of which 30 % (23.8 kg) is liquid — yet the liquid fills only
**2.34 %** of the volume, because `vg ≫ vf`.

## Bridge
Quality threads through the vapor-power and refrigeration cycles (Topic 9 — turbine
exit, condenser) and supplies `s = sf + x·sfg` to the entropy module (`4.2`). The
`f/g` data come from the saturation tables (Topic 5).
