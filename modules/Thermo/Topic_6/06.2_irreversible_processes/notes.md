# 6.2 — Irreversible Processes & Entropy Production (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. What makes a process irreversible
A process is **irreversible** if the system *and* its surroundings cannot both be returned
to their initial states [M §5.3.1, p.249]. **All actual processes are irreversible.** The
common **irreversibilities** are:

1. Heat transfer through a finite temperature difference  
2. Unrestrained expansion of a gas/liquid to a lower pressure  
3. Spontaneous chemical reaction  
4. Spontaneous mixing of matter at different compositions/states  
5. Friction (sliding and fluid friction)  
6. Electric current flow through a resistance  
7. Magnetization/polarization with hysteresis  
8. Inelastic deformation

**Internal** irreversibilities occur *within* the system; **external** ones occur in the
surroundings. The split depends only on where you draw the boundary [M §5.3.1, p.249–250].

## 2. The closed-system entropy balance
Entropy is *produced*, never destroyed. The closed-system **entropy balance** [M §6.7, p.305]:
$$S_2-S_1=\underbrace{\int_1^2\!\Big(\tfrac{\delta Q}{T}\Big)_{\!b}}_{\text{entropy transfer}}+\underbrace{\sigma}_{\text{production}}\quad(6.24),$$
and on a time-rate basis `dS/dt = Σ_j Q̇_j/T_j + σ̇` (Eq. 6.28). The second law fixes the
**sign of σ** [M §6.7, p.307]:
$$\sigma:\;\begin{cases}>0&\text{irreversibilities present}\\[-2pt]=0&\text{none (internally reversible)}\\[-2pt]<0&\textbf{impossible}\end{cases}\;(6.26),
\qquad S_2-S_1\;\gtrless\;0\;(6.27).$$
σ is **not a property** — it depends on the path. (Same end states, different paths ⇒
different σ: cf. internally-reversible Ex 6.1 with σ = 0 vs. paddle-stirred Ex 6.2 with σ > 0.)

## 3. Increase-of-entropy principle
Enclose the system *and* the affected surroundings to form an **isolated** system. Its
entropy transfer is zero, so [M §6.8.1, p.313]:
$$\Delta S_{\text{isol}}=\Delta S_{\text{system}}+\Delta S_{\text{surr}}=\sigma_{\text{isol}}\ge 0\quad(6.30).$$
**Processes proceed only in the direction that increases the total entropy of system +
surroundings.** One side may *decrease* (e.g. a cooling bar) provided the sum rises.

**σ flags possibility & ranks waste.** *Check (M Ex 6.2, adiabatic paddle-stir of water,
sat-liquid→sat-vapor at 150 °C):* `W/m = −(u₂−u₁) = −(2559.5−631.68) = −1927.82 kJ/kg`;
`σ/m = s₂−s₁ = 6.8379−1.8418 = 4.9961 kJ/kg·K > 0`. *Check (M Ex 6.4, gearbox, steady,
Q̇ = −1.2 kW):* `σ̇ = −Q̇/T_b = 1.2/300 = 4.0×10⁻³ kW/K` (at T_b), `4.1×10⁻³` at T_f = 293 K.
*Check (M Ex 6.5, 0.8-lb bar at 1900 °R quenched in 20-lb water at 530 °R):* `T_f = 535 °R`,
`σ = 20(1.0)ln(535/530) + 0.8(0.1)ln(535/1900) = 0.1878 − 0.1014 = 0.0864 Btu/°R > 0`.

## Bridge
σ = 0 is the reversible limit (module `6.1`); the adiabatic σ-test underlies isentropic
efficiency and "minimum work" arguments in module `6.3`. The CV form of the entropy
balance (`6.4`/`6.5` flows) rank-orders component losses in Topics 7–9.
