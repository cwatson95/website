# 10.2 — Stirling Engine (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The Stirling cycle
The **Stirling cycle** is a *reversible* power cycle of **four internally reversible
processes** executed by a fixed mass of ideal gas (typically air, helium, or
hydrogen) in a piston–cylinder assembly fitted with a **regenerator** — a porous
matrix that stores and returns heat [M §9.8.4, p.552–553]. Using the numbering of
`code/stirling_engine.py` (consistent with Fig. 9.21):

| Process | type | what happens |
|---|---|---|
| 1–2 | isothermal compression at $T_C$ | gas discharges $Q_{12}$ to the cold surroundings |
| 2–3 | constant-volume heating $T_C\to T_H$ | gas receives heat **from the regenerator** |
| 3–4 | isothermal expansion at $T_H$ | gas receives $Q_{34}$ from the hot source |
| 4–1 | constant-volume cooling $T_H\to T_C$ | gas gives heat **to the regenerator** |

So the cycle is **two isothermals (at $T_H$ and $T_C$) alternating with two
constant-volume regenerative processes**. On a **p–v diagram** the two isotherms are
hyperbolas and the two constant-volume legs are vertical; on a **T–s diagram** the
two isotherms are horizontal and the constant-volume legs curve between them
(Fig. 9.21) [M §9.8.4, p.553].

## 2. The regenerator — why $\eta = \eta_{Carnot}$
The constant-volume cooling 4–1 rejects exactly $Q = c_v(T_H-T_C)$ per unit mass, and
the constant-volume heating 2–3 requires exactly the same amount. An **ideal
regenerator (100% effectiveness)** stores the heat shed in 4–1 and returns it in 2–3,
so these two internal transfers **cancel** and never cross the system boundary
[M §9.8.4, p.552]. All external heat addition then occurs in the isothermal expansion
at $T_H$ and all external heat rejection in the isothermal compression at $T_C$ — the
cycle is thermodynamically equivalent to one exchanging heat with just two reservoirs.
Moran concludes that *"the thermal efficiency of the Stirling cycle is given by the
same expression as for the Carnot and Ericsson cycles"* [M p.553]:
$$\eta = 1 - \frac{T_C}{T_H}\qquad(\text{same form as Eq. 5.9}),$$
with $T$ **absolute**. The Stirling and Ericsson cycles are thus *other* reversible
cycles that reach the **Carnot ceiling** (module `10.1`).

## 3. Per-process heats, work, and mean effective pressure
For an ideal gas the internally reversible **isothermal** process has $du=0$, so
$Q = W = mRT\ln(V_2/V_1)$ [M Eq. 2.17 with $pV=mRT$]. With the **volume (compression)
ratio** $r = V_{max}/V_{min}$:
$$Q_{34}=mRT_H\ln r\ \ (\text{in}),\qquad |Q_{12}|=mRT_C\ln r\ \ (\text{out}),$$
$$W_{net}=Q_{34}-|Q_{12}|=mR\,(T_H-T_C)\ln r .$$
A regenerator changes neither $W_{net}$ nor the boundary heats $Q_{34},Q_{12}$ — it
only recycles the constant-volume heat $Q_{regen}=c_v(T_H-T_C)$ [M Eq. 3.50]. Dividing
$W_{net}$ by $\eta=1-T_C/T_H$ confirms $\eta = W_{net}/Q_{34}$ (the $mR\ln r$ cancels).
The **mean effective pressure** (work per unit displacement) is
$$\text{mep}=\frac{W_{net}}{V_{max}-V_{min}} .$$

## 4. Without regeneration — the penalty
Drop the regenerator and the constant-volume heating 2–3 must be supplied
*externally*, so the heat input becomes $Q_{34}+c_v(T_H-T_C)$ and
$$\eta_{no\,regen}=\frac{mR(T_H-T_C)\ln r}{mRT_H\ln r + mc_v(T_H-T_C)}\ \ll\ 1-\frac{T_C}{T_H}.$$
For air ($R=0.287$, $c_v=0.718$ kJ/kg·K), $T_H=1000$ K, $T_C=300$ K, $r=2$ this gives
$\eta\approx0.20$ versus the ideal $0.70$ — regeneration is *essential* to the
Stirling engine's promise. Real regenerator **effectiveness** is
$\eta_{reg}=(h_x-h_2)/(h_4-h_2)$, $\to 1$ as $h_x\to h_4$ [M Eq. 9.27, §9.7, p.539];
in practice 60–80%.

## 5. The Stirling *engine* (vs. the cycle)
The Ericsson and Stirling **cycles** are "principally of theoretical interest as
examples of cycles that exhibit the same thermal efficiency as the Carnot cycle"
[M p.553]. The **Stirling engine** is the practical piston–cylinder machine built on
those ideas: a closed regenerative cycle whose combustion occurs **externally**, so it
offers high efficiency with low emissions and fuel flexibility — an *external
combustion engine* [M p.553].

## Bridge
The Stirling engine reaches the **same ceiling** $1-T_C/T_H$ as the Carnot engine of
`10.1`, by ideal regeneration rather than by isentropic processes. The corollaries
that make this expression a ceiling are in `3.3`; the gas-turbine **regenerator** it
borrows is `09` (Brayton with regeneration, Eq. 9.27). Worked Stirling/Ericsson
end-of-chapter problems are in `10.HP`; the equation registry is `10.EQ`.
