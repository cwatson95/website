# 5.4 — The p–v Diagram (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The p–v projection of the p–v–T surface
A pure substance has a single-valued p–v–T surface [M §3.2.1, p.97]. Projecting it onto
the pressure–volume plane gives the **p–v diagram**: single-phase solid/liquid/vapor
regions separated by the two-phase **dome**, whose left and right borders are the
**saturated-liquid** and **saturated-vapor** lines. They meet at the **critical point**
`(pc, Tc, vc)` [M §3.2.2, p.99]. Isotherms run nearly flat across the dome (where `p` and
`T` are locked together) and steepen in the liquid region. The dome is exactly the region
the saturation tables of `5.1` describe.

## 2. Boundary work is the area under the path
For a closed system the only work mode of a simple compressible substance is boundary
(`pdV`) work. In an **internally reversible** (quasiequilibrium) process the pressure is
uniform, so [M Eq. 2.16–2.17, §2.2.3–2.2.5, pp.48–49]:
$$\delta W=p\,dV,\qquad W=\int_1^2 p\,dV .$$
Geometrically this integral is the **area under the process path** on the `p–V` diagram.
Because the area depends on the path joining the two end states, **work is not a property**
— different paths give different areas.

## 3. Closed forms for common reversible paths
[M Example 2.1, §2.2.5, pp.50–51]
- **isobaric** (`p` const): `W = p(V₂ − V₁)` — a rectangle.
- **polytropic** `pVⁿ = const`, `n ≠ 1`: `W = (p₂V₂ − p₁V₁)/(1 − n)`, with
  `p₂ = p₁(V₁/V₂)ⁿ`.
- **isothermal ideal gas** (`n = 1`, `pV = const`): `W = p₁V₁ ln(V₂/V₁)`.

*Check (M Ex 2.1):* gas from `p₁=3 bar`, `V₁=0.1 m³` to `V₂=0.2 m³`: (a) `n=1.5` →
`p₂=1.06 bar`, `W=17.6 kJ`; (b) `n=1.0` → `W=20.79 kJ`; (c) `n=0` → `W=30 kJ`. The
trapezoid rule on a finely sampled polytrope reproduces the closed form.

*Units:* `p` in kPa with `V` in m³ gives `W` in kJ (`1 kPa·m³ = 1 kJ`; `1 bar·m³ = 100 kJ`).

## Bridge
The water examples of `5.EP` use the isobaric form directly: Ex 3.4 process 1–2 (cool at
`10 bar` from `v=0.3066` to `0.1944 m³/kg`) gives `W/m = p(v₂−v₁) = −112.2 kJ/kg`; Ex 6.1
(vaporize at `4.758 bar`, `150 °C`) gives `W/m = 186.38 kJ/kg`. The exact dual of this
module is `5.5`: on the **T–s** diagram the area under a reversible path is the **heat**.
