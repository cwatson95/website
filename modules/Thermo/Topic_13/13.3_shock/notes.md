# 13.3 — Normal Shock (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. What a shock is
In the diverging part of a C–D nozzle, when the back pressure lies between the
shock-free supersonic design value and the subsonic-diffuser value, a thin
(≈10⁻⁵ cm) **normal shock** stands across the duct [M §9.13.3, p.575]. The control-volume
mass, energy, momentum, and entropy balances (Eqs. 9.46–9.49) give, at steady state with
`Q̇=Ẇ=0`: `ρxVx=ρyVy`, `hox=hoy`, `px+ρxVx²=py+ρyVy²`, and `sy−sx=σ̇/ṁ ≥ 0`. The entropy
condition `sy > sx` means the change can only go supersonic → subsonic.

## 2. The normal-shock functions (ideal gas, constant k)
Combining the balances with the ideal-gas relations gives closed forms in `Mx`
[M §9.14.2, p.581–582]:
$$M_y^2=\frac{M_x^2+\tfrac{2}{k-1}}{\tfrac{2k}{k-1}M_x^2-1}\ (9.55),\qquad
\frac{p_y}{p_x}=\frac{1+kM_x^2}{1+kM_y^2}\ (9.54),$$
$$\frac{T_y}{T_x}=\frac{1+\tfrac{k-1}{2}M_x^2}{1+\tfrac{k-1}{2}M_y^2}\ (9.53),\qquad
\frac{p_{oy}}{p_{ox}}=\frac{M_x}{M_y}\!\left[\frac{1+\tfrac{k-1}{2}M_y^2}{1+\tfrac{k-1}{2}M_x^2}\right]^{\frac{k+1}{2(k-1)}}\ (9.56).$$
Since `Tox=Toy` (energy, Eq. 9.47b) but `sy>sx`, the **stagnation pressure falls**:
`poy/pox < 1`. Because the area is unchanged across the shock, `A*x/A*y = poy/pox`
(Eq. 9.57). *Check (Table 9.3, k=1.4, Mx=2.0):* `My=0.5774`, `py/px=4.500`,
`Ty/Tx=1.6875`, `poy/pox=0.7209`.

## 3. Reading the table
For a given `Mx` and `k`, Eq. 9.55 fixes `My`, then Eqs. 9.53/9.54/9.56 fix the jumps —
exactly how Table 9.3 (k=1.4) is built [M §9.14.2, p.582].

## Bridge
*Check (M Ex 9.15d):* a shock stands at the C–D nozzle exit where the upstream
(supersonic) state is `Mx=2.4`, `px=6.84 lbf/in²`. Then `My=0.52`, `py/px=6.5533`, so
the exit (back) pressure is `py=44.82 lbf/in²`. *Check (M Ex 9.15e):* with the shock
*inside* the diverging section at `Mx=2.2`, the stagnation-pressure ratio
`poy/pox=0.62812` shifts the effective sonic area (`A*x/A*y`), which (with Eq. 9.52)
sets the subsonic exit Mach number — the link back to the area–Mach relation of `13.2`.
