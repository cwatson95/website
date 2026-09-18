# 3.1 — Zeroth Law & Temperature (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Thermal equilibrium
Two bodies brought into contact through a diathermal (heat-permitting) wall
eventually stop changing — they reach **thermal equilibrium** [M §1.7, p.19].
The single property they then share is **temperature**.

## 2. The zeroth law
> When two objects are in thermal equilibrium with a third object, they are in
> thermal equilibrium with one another. [M §1.7, p.19]

The reusable third object is a **thermometer**: equal thermometer readings ⇒
mutual equilibrium, even for two bodies never placed in contact. Logically this
is *prior* to the first and second laws (hence "zeroth", named after them were
already numbered). Code: `zeroth_law(Ta,Tb,Tc)` returns `True` when the premise
`A~C, B~C` holds (and the law then forces `A~B`), else `None`.

## 3. Temperature scales
Two **absolute** scales put zero at absolute zero:
- **Kelvin** (SI), fixed by the triple point of water $T_{tp}=273.16\,\mathrm{K}$
  [M §1.7.3, p.22].
- **Rankine**: $T(^\circ\mathrm{R})=1.8\,T(\mathrm{K})$ [M Eq. 1.16, §1.7.2, p.21].

Two **shifted** scales put zero at convenient points:
- **Celsius**: $T(^\circ\mathrm{C})=T(\mathrm{K})-273.15$ [M Eq. 1.17, §1.7.3, p.22].
- **Fahrenheit**: $T(^\circ\mathrm{F})=T(^\circ\mathrm{R})-459.67$ [M Eq. 1.18];
  equivalently $T(^\circ\mathrm{F})=1.8\,T(^\circ\mathrm{C})+32$ [M Eq. 1.19, p.22].

*Check:* 300 K = 540 °R = 26.85 °C = 80.33 °F; the steam point 373.15 K = 100 °C
= 212 °F; absolute zero = 0 K = −273.15 °C = −459.67 °F; and °C = °F at −40°.

## 4. Why absolute T matters
Temperature **ratios** drive the second law — Carnot efficiency
$\eta=1-T_C/T_H$ (`3.3`) — and the ideal-gas law $pV=nRT$. A ratio is only
meaningful on an **absolute** scale; e.g. between 27 °C and 327 °C the correct
ratio is $300.15/600.15$ (K), *not* $27/327$. Using °C/°F in a ratio is a classic
and serious error.

## Bridge
The absolute `T` defined here is the temperature appearing in the **first law**
(`3.2`, energy balance), the **second law** (`3.3`, Carnot bounds), and the
**third law** (`3.4`, `S→0` as `T→0`). The thermodynamic (Kelvin) scale is in
fact *defined* by the second law itself — see `3.3`, §Kelvin scale.
