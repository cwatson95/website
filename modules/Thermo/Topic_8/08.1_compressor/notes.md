# 08.1 — Compressor (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. What a compressor does
A **compressor** does work *on* a gas (vapor) to raise its pressure (a **pump** does the
same for a liquid) [M §4.8, p.190]. Because a shaft delivers power to the fluid, the
control-volume work term `Wdot_cv` is **negative** — the magnitude `-Wdot_cv` is the
**power input**.

## 2. Steady control-volume energy balance
For one inlet (1) and one exit (2) at steady state [M Eq. 4.20a, p.181]:
$$0=\dot Q_{cv}-\dot W_{cv}+\dot m\Big[(h_1-h_2)+\frac{V_1^2-V_2^2}{2}+g(z_1-z_2)\Big].$$
For a compressor the potential-energy change is negligible. Solving for the power,
$$\dot W_{cv}=\dot Q_{cv}+\dot m\Big[(h_1-h_2)+\frac{V_1^2-V_2^2}{2}\Big].$$
When stray heat transfer is also a secondary effect [M §4.8.1, p.190]:
$$\dot W_{cv}=\dot m(h_1-h_2)\quad(4.20b\text{ form}).$$
The mass flow rate uses `code/mass_flow_rate`: $\dot m=AV/v$ (Eq. 4.4b), or for an ideal
gas $\dot m=AVp/(RT)$.

*Check (M Ex 4.5, p.191):* air in at 1 bar, 290 K, 6 m/s, `A1=0.1 m²`; out at 7 bar,
450 K, 2 m/s; `Qdot=-180 kJ/min`. Then `ṁ=0.72 kg/s`, with `h1=290.16`, `h2=451.80 kJ/kg`
(Table A-22), giving `Wdot_cv = -3 + 0.72(290.16-451.80) + tiny KE = -119.4 kW`
(power **input** 119.4 kW). The kinetic-energy term contributes < 0.02 kW.

## 3. Isentropic compressor work & efficiency
For fixed inlet state and exit pressure, the **least** work input is the adiabatic,
internally reversible (**isentropic**) compression to the same exit pressure
[M §6.12.3, p.337]:
$$\Big(\tfrac{-\dot W_{cv}}{\dot m}\Big)_s=h_{2s}-h_1\le h_2-h_1.$$
The **isentropic compressor efficiency** is the ratio of this minimum work to the actual
work [M Eq. 6.48, p.338]:
$$\eta_c=\frac{(-\dot W_{cv}/\dot m)_s}{-\dot W_{cv}/\dot m}=\frac{h_{2s}-h_1}{h_2-h_1},
\qquad \eta_c\approx 0.75\text{–}0.85 .$$
Given `η_c`, the actual exit enthalpy is `h2 = h1 + (h2s − h1)/η_c`
(`code/exit_enthalpy_from_efficiency`).

*Check (M Ex 6.14, p.338):* R-22 compressed adiabatically from −5 °C (`h1=249.75`) to
14 bar, 75 °C (`h2=294.17`); the isentropic exit at 14 bar is `h2s=285.58 kJ/kg`. Then
`η_c = (285.58−249.75)/(294.17−249.75) = 35.83/44.42 = 0.81`, and with `ṁ=0.07 kg/s`,
`Wdot_cv = 0.07(249.75−294.17) = −3.11 kW`.

## Bridge
The same balance, with the sign of the work flipped, describes a **turbine**
(`Wdot_cv = ṁ(h1−h2) > 0`). The compressor is the work-input heart of the
**vapor-compression heat pump / refrigerator** of module `08.4`, where `η_c` sets how
far the real cycle falls below the ideal. The condenser that receives the hot compressed
vapor is module `08.2`.
