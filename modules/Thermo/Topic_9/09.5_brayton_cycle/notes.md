# 09.5 — Air-Standard Brayton Cycle (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. From piston to gas turbine
The Otto/Diesel/dual cycles (09.2–09.4) are *closed-system* piston idealizations. The
**Brayton cycle** models the **gas turbine** — compressor, combustor, turbine — as a
*steady-flow* loop of air. In the air-standard idealization combustion becomes external
heat addition, and a second heat exchanger returns the exhaust to the compressor inlet
so the air runs a true cycle [M §9.5–9.6, p.526–527, Fig. 9.9]:

- **1–2** isentropic compression (work **in**);
- **2–3** constant-**pressure** heat addition;
- **3–4** isentropic expansion through the turbine (work **out**);
- **4–1** constant-pressure heat rejection.

## 2. Steady-flow energy transfers — Eqs. 9.15–9.20
Each component is a control volume at steady state ($\Delta$ke = $\Delta$pe = 0), so
per unit of mass flowing [M §9.6.1, p.527–528]:
$$\frac{\dot W_t}{\dot m}=h_3-h_4\ (9.15),\qquad \frac{\dot W_c}{\dot m}=h_2-h_1\ (9.16),$$
$$\frac{\dot Q_{in}}{\dot m}=h_3-h_2\ (9.17),\qquad \frac{\dot Q_{out}}{\dot m}=h_4-h_1\ (9.18),$$
$$\eta=\frac{(h_3-h_4)-(h_2-h_1)}{h_3-h_2}\ (9.19),\qquad
\text{bwr}=\frac{h_2-h_1}{h_3-h_4}\ (9.20).$$
Because the compressor squeezes **gas** (large specific volume), the **back work ratio
is 40–80%** — compare 1–2% for the Rankine pump (09.6) [M p.528]. These balances hold
with or without irreversibilities.

## 3. The ideal cycle and the pressure ratio
With isentropic turbine/compressor and no pressure drops, Table A-22 air data are
linked by $p_{r2}=p_{r1}(p_2/p_1)$ and $p_{r4}=p_{r3}(p_1/p_2)$ (Eqs. 9.21–9.22). On a
**cold air-standard** basis [M §9.6.2, p.529, 532]:
$$T_2=T_1\,r_p^{(k-1)/k}\ (9.23),\qquad T_4=T_3\,(1/r_p)^{(k-1)/k}\ (9.24),$$
$$\boxed{\ \eta=1-\frac{1}{r_p^{\,(k-1)/k}}\ }\quad(9.25),\qquad r_p=\frac{p_2}{p_1}.$$
Efficiency **rises with pressure ratio** — same shape as Otto's Eq. 9.8 with
$r_p^{(k-1)/k}$ in place of $r^{k-1}$. With turbine-inlet temperature capped by
metallurgy, the *net work per unit mass* instead peaks at
$r_p^*=(T_3/T_1)^{k/2(k-1)}$ [Ex 9.5, p.533–534] — about **21** for 300/1700 K — so
vehicle turbines run below the best-efficiency ratio.

## 4. Worked check — Example 9.4 (ideal)
Air at 100 kPa, 300 K, 5 m³/s; $r_p=10$; $T_3=1400$ K. Table A-22: $h_1=300.19$
($p_{r1}=1.386$), $h_2=579.9$, $h_3=1515.4$ ($p_{r3}=450.5$), $h_4=808.5$ kJ/kg.
$$\eta=\frac{706.9-279.7}{935.5}=0.457,\qquad \text{bwr}=\frac{279.7}{706.9}=0.396,$$
$\dot m=5.807$ kg/s, $\dot W_{cycle}=2481$ kW ($\dot Q_{in}=5432$ kW). Cold air-standard,
$k=1.4$: $T_2=579.2$ K, $T_4=725.1$ K, $\eta=0.482$, bwr $=0.414$, $\dot W=2308$ kW —
constant specific heats again **overpredict** [M Ex 9.4, p.529–531].

## 5. Irreversibilities — Example 9.6
Real turbomachines: $\dot W_t/\dot m=\eta_t(\dot W_t/\dot m)_s$ and
$\dot W_c/\dot m=(\dot W_c/\dot m)_s/\eta_c$ ($\eta_t,\eta_c$ per Eqs. 6.46/6.48)
[M §9.6.3, p.535]. With $\eta_t=\eta_c=0.80$ on the Ex 9.4 cycle: $w_t=565.5$,
$w_c=349.6$, $h_2=649.8$, $q_{in}=865.6$ kJ/kg, so $\eta=0.249$, bwr $=0.618$,
$\dot W=1254$ kW — half the ideal output [M Ex 9.6, p.535–537]. The large bwr is why
gas turbines *need* high $\eta_t,\eta_c$; at $\eta_t=0.70$, $\eta$ falls to 16.8%.

## 6. Regeneration pointer — §9.7
Turbine exhaust ($T_4>T_2$) can preheat compressor air in a counterflow **regenerator**:
$\dot Q_{in}/\dot m=h_3-h_x$ (9.26) with effectiveness
$$\eta_{reg}=\frac{h_x-h_2}{h_4-h_2}\quad(9.27),\qquad 60\text{–}80\%\ \text{typical}.$$
Net work is unchanged, heat added drops, so $\eta$ rises: Ex 9.7 ($\eta_{reg}=0.8$)
gives $h_x=762.8$ kJ/kg and $\eta=0.568$ vs 0.457 without [M §9.7, p.537–541]. Module
`10.2` uses the same Eq. 9.27 for the Stirling/Ericsson regenerator.

## Bridge
Carnot (`09.1`) still caps it: 0.457 < 0.786 for 1400/300 K. The piston cycles
(09.2–09.4) trade at *equal compression ratio*; Brayton trades on *pressure ratio* and
loses most to its back work. Next, `09.6` swaps the gas loop for a condensing **vapor**
loop — pumping liquid makes bwr collapse to ~1%. Isentropic device efficiencies live in
`07.1`; air tables in Topic 5.
