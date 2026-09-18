# 08.4 — Heat Pump / Refrigerator (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

This module is the **device / COP** view: how to *rate* a reversed cycle. The detailed
**cycle** analysis (state-by-state vapor-compression and Brayton cycles) lives in Topic 9.

## 1. Reversed cycle and the first law
A refrigerator / heat pump uses a net work input `W_net` to pump heat `Q_C` out of a cold
region and dump `Q_H = Q_C + W_net` into a warm region [M Eq. 10.8, p.629]. Same hardware,
different *purpose*: a **refrigerator** wants `Q_C` (cooling); a **heat pump** wants `Q_H`
(heating).

## 2. Coefficients of performance
The COP is the *wanted effect ÷ work paid* [M §10.1, §10.6.1]:
$$\beta=\frac{Q_C}{W_{net}}\ (10.7\text{ form}),\qquad
\gamma=\frac{Q_H}{W_{net}}\ (10.10\text{ form}).$$
Since `Q_H = Q_C + W_net`, dividing by `W_net` gives the identity
$$\boxed{\gamma=\beta+1}$$
so a heat pump's COP is **always ≥ 1** — you always get out at least the work you put in,
plus the free heat scavenged from the cold side. (`code/cop_refrigeration`,
`cop_heat_pump`, `heat_rejected`.)

## 3. Carnot (reversible) ceilings
The best possible COPs between reservoirs at `T_C`, `T_H` (kelvin) are [M Eqs. 10.1, 10.9]:
$$\beta_{max}=\frac{T_C}{T_H-T_C}\ (10.1),\qquad
\gamma_{max}=\frac{T_H}{T_H-T_C}\ (10.9),$$
which also satisfy `γ_max = β_max + 1`. COP falls as the temperature lift `T_H − T_C`
grows — which is why air-source heat pumps struggle on the coldest days.
(`code/carnot_cop_refrigeration`, `carnot_cop_heat_pump`.)

## 4. Vapor-compression COP from enthalpies
For the real cycle (1 compressor in, 2 compressor out, 3 condenser out, 4 valve out; the
throttle gives `h4 = h3`) the net work is the compressor work, so [M Eqs. 10.7, 10.10]:
$$\beta=\frac{h_1-h_4}{h_2-h_1},\qquad \gamma=\frac{h_2-h_3}{h_2-h_1}.$$
(`code/cop_ref_from_enthalpies`, `cop_hp_from_enthalpies`.)

*Check (M Ex 10.1, p.614):* ideal R-134a refrigerator, `h1=247.23`, `h2s=264.7`,
`h3=h4=85.75 kJ/kg` ⇒ `β = 161.48/17.47 = 9.24`, well below the Carnot limit
`β_max = 273/(299−273) = 10.5` for the 0 °C / 26 °C reservoirs (throttling + desuperheat
irreversibilities).

*Check (M Ex 10.4, p.632):* R-134a heat pump, `h1=242.54`, `h2=280.19`, `h3=h4=105.29 kJ/kg`
⇒ `γ = 174.9/37.65 = 4.65`; with `ṁ=0.2 kg/s`, `Ẇc = 7.53 kW` and `Q̇out = 34.98 kW`
(heating a building). The same cycle's refrigeration COP is `β = γ − 1 = 3.65`.

## Bridge
The work input `W_net` is the **compressor** of `08.1`; the heat-rejection `Q_H` is the
**condenser** of `08.2`; the cold- and warm-side exchangers are instances of `08.3`. The
full cycle (T–s diagram, isentropic-efficiency effects, p–h plane) is Topic 9.
