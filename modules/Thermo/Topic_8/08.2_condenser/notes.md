# 08.2 — Condenser (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. What a condenser does
A **condenser** is a heat exchanger whose job is to **reject heat** from a working fluid,
typically condensing a vapor to liquid at (nearly) constant pressure. Condensers are found
in power plants and in refrigeration / heat-pump systems [M §4.9.2, p.196].

## 2. Single-stream energy balance
Take a control volume around the **working-fluid side** only (one inlet, one exit). The
only work is flow work, so `Wdot_cv = 0`, and kinetic / potential energy changes are
negligible. The steady energy rate balance [M Eq. 4.20a, p.181] collapses to
$$\dot Q_{cv}=\dot m\,(h_\text{out}-h_\text{in}).$$
Since the fluid loses energy (`h_out < h_in`), **`Qdot_cv < 0`** — heat flows *out*. The
heat-rejection **magnitude** is `ṁ(h_in − h_out)` (`code/heat_rejected`).

For a two-phase inlet, fix the enthalpy from the quality
`h = hf + x(hg − hf)` (`code/enthalpy_two_phase`); invert with
`x = (h − hf)/(hg − hf)` (`code/quality_from_h`).

*Check (M Ex 4.7 steam side, p.198):* steam enters at 0.1 bar, `x = 0.95`
(`h1 = 191.83 + 0.95(2584.7−191.83) = 2465.1 kJ/kg`) and leaves as condensate at 45 °C
(`h2 ≈ hf = 188.45 kJ/kg`). Then per kg of steam
`Qdot_cv/ṁ = h2 − h1 = 188.45 − 2465.1 = −2276.7 kJ/kg` — energy rejected to the cooling
water. (At `ṁ = 125 kg/s` this is −284.6 MW.)

## 3. The condenser in a cycle
In a vapor-compression refrigerator / heat pump the condenser sits between the compressor
exit (state 2) and the expansion valve (state 3). Per unit mass of refrigerant the heat
rejected is [M Eq. 10.5, p.613]
$$\frac{\dot Q_{out}}{\dot m}=h_2-h_3,$$
the working basis of `code/condenser_heat_per_mass`.

*Check (M Ex 10.4 heat-pump condenser, p.632):* `h2 = 280.19`, `h3 = 105.29 kJ/kg`,
`ṁ = 0.2 kg/s` ⇒ `Qdot_out = 0.2(280.19−105.29) = 34.98 kW` delivered to the building.

## Bridge
Viewed with the **cooling stream** included, the condenser is a *two-stream* heat exchanger
— that whole-device balance and the mass-flow ratio it fixes are module `08.3`. The heat
rejected here is the `Q_H` that defines the heat-pump COP in module `08.4`.
