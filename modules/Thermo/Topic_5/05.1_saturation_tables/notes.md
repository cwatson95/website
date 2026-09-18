# 5.1 — Saturation Tables (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Why one index is enough inside the dome
Within the two-phase liquid–vapor region, pressure and temperature are **not
independent** [M §3.2.2, p.100]: for each saturation temperature `Tsat` there is exactly
one saturation pressure `psat`, traced by the vaporization line. So the saturation tables
need only **one** index:
- **Table A-2** — the *temperature* table (index `T`) [M §3.5.2, p.107].
- **Table A-3** — the *pressure* table (index `p`) [M §3.5.2, p.107].

Each row lists the **saturated-liquid** (subscript `f`) and **saturated-vapor**
(subscript `g`) values of `v, u, h, s`, plus the evaporation differences `vfg, hfg, …`
(`fg = g − f`).

## 2. Quality and the two-phase mixture rule
The **quality** of a two-phase mixture is the vapor mass fraction [M Eq. 3.1, §3.3, p.102]:
$$x=\frac{m_{\text{vap}}}{m_{\text{liq}}+m_{\text{vap}}},\qquad 0\le x\le 1.$$
Averaging the specific volume over both phases (`Vliq=mliq vf`, `Vvap=mvap vg`) gives the
**mixture rule** [M Eq. 3.2, §3.5.2, p.108]:
$$v=(1-x)\,v_f+x\,v_g=v_f+x\,(v_g-v_f).$$
The same `x`-weighting holds for every specific property:
$$u=u_f+x\,(u_g-u_f)\ (3.6),\quad h=h_f+x\,(h_g-h_f)\ (3.7),\quad s=s_f+x\,(s_g-s_f)\ (6.4).$$
Inverting Eq. 3.2 gives the quality from a measured `v`:
$$x=\frac{v-v_f}{v_g-v_f}\quad(\text{equally from }u,h,s).$$
*Check (M p.108):* water at `100 °C`, `x=0.9`: `v = 1.0435×10⁻³ + 0.9(1.673 − 1.0435×10⁻³)
= 1.506 m³/kg`.

## 3. Interpolation
States rarely fall on the table grid, so use **linear interpolation** between adjacent
entries [M §3.5.1, p.105]:
$$y(x)=y_1+\frac{x-x_1}{x_2-x_1}\,(y_2-y_1).$$
Care is needed: the appendix tables are themselves coarse samples of a smooth surface.

## 4. Finding states from `(p, T)` — the decision tree
Given `p` and `T < Tc`, look up `Tsat = Tsat(p)` in A-3 (or `psat(T)` in A-2)
[M "Finding States in the Steam Tables", p.109]:
- `p > psat(T)`  ⇔  `T < Tsat(p)`  → **compressed liquid** (`5.3`).
- `p = psat(T)`  ⇔  `T = Tsat(p)`  → **two-phase**; need a *second* property (e.g. `x` or `v`).
- `p < psat(T)`  ⇔  `T > Tsat(p)`  → **superheated vapor** (`5.2`).

`phase_pT` implements this (with a triple-point floor for `T < 0.01 °C` → solid).

## Bridge
*Check (M Ex 3.2):* rigid tank, water at `p₁=1 bar`, `x₁=0.5`. From A-3,
`v₁ = vf + 0.5(vg − vf) = 0.8475 m³/kg`; `T₁ = Tsat(1 bar) = 99.63 °C`. Heating to
`p₂=1.5 bar` at fixed `v` (`v₂=v₁`) keeps the state two-phase: `T₂ = 111.4 °C`,
`x₂ = (v₁ − vf₂)/(vg₂ − vf₂) = 0.731`. With `m = V/v₁ = 0.59 kg`, the vapor mass is
`mg₂ = x₂m = 0.431 kg`. When heating drives `vg(p₃) = v₁`, the tank holds pure saturated
vapor — interpolating A-3 gives `p₃ = 2.11 bar`. The full example lives in `5.EP`.
