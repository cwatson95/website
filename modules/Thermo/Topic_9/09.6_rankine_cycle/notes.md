# 09.6 — Rankine Cycle (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The vapor power cycle
The **Rankine cycle** is the thermodynamic cycle of steam power plants — coal, nuclear,
biomass, geothermal, solar-concentrating all run it (Table 8.2) [M Ch.8 intro/§8.2,
p.439, 445]. Water circulates through four steady-flow components (Fig. 8.2, Moran's
state numbering):

- **1–2** turbine: high-pressure vapor expands, producing work;
- **2–3** condenser: heat rejected to cooling water; exit is (saturated) liquid;
- **3–4** pump: liquid pushed to boiler pressure (small work input);
- **4–1** boiler: feedwater heated and vaporized at pressure.

## 2. Component balances — Eqs. 8.1–8.6
Each component is a control volume at steady state ($\Delta$ke = $\Delta$pe = 0, no
stray heat loss) [M §8.2.1, p.446–447]:
$$\frac{\dot W_t}{\dot m}=h_1-h_2\ (8.1),\quad \frac{\dot Q_{out}}{\dot m}=h_2-h_3\ (8.2),\quad
\frac{\dot W_p}{\dot m}=h_4-h_3\ (8.3),\quad \frac{\dot Q_{in}}{\dot m}=h_1-h_4\ (8.4),$$
$$\eta=\frac{(h_1-h_2)-(h_4-h_3)}{h_1-h_4}\ (8.5a)=1-\frac{h_2-h_3}{h_1-h_4}\ (8.5b),\qquad
\text{bwr}=\frac{h_4-h_3}{h_1-h_2}\ (8.6).$$
These hold with or without irreversibilities. Because the pump handles **liquid**, the
bwr is only **1–2%** — against 40–80% for the Brayton compressor (09.5) [M p.448, 528].

## 3. Ideal cycle and the pump-work shortcut — Eq. 8.7b
In the **ideal Rankine cycle** the turbine and pump are isentropic and the heat
exchangers isobaric; state 1 is saturated (or superheated) vapor, state 3 saturated
liquid [M §8.2.2, p.449]. The incompressible-liquid pump work is
$$\left(\frac{\dot W_p}{\dot m}\right)_s\approx v_3\,(p_4-p_3)\quad(8.7b).$$
Turbine-exit states are fixed by $s_2=s_1$: $x_2=(s_1-s_f)/(s_g-s_f)$, $h_2=h_f+x_2h_{fg}$.

## 4. Worked check — Example 8.1 (ideal)
Sat. vapor at 8.0 MPa → condenser 0.008 MPa, 100 MW net. Table A-3: $h_1=2758.0$,
$s_1=5.7432$; at 0.008 MPa $s_f=0.5926$, $s_g=8.2287$, $h_f=173.88$, $h_{fg}=2403.1$,
$v_f=1.0084\times10^{-3}$:
$$x_2=\frac{5.7432-0.5926}{7.6361}=0.6745,\quad h_2=1794.8,\quad
w_p=8.06,\quad h_4=181.94\ \text{kJ/kg},$$
$$\eta=\frac{963.2-8.06}{2576.06}=0.371,\qquad \text{bwr}=8.37\times10^{-3}\ (0.84\%),$$
$\dot m=3.77\times10^5$ kg/h, $\dot Q_{in}=269.77$ MW, $\dot Q_{out}=169.75$ MW,
cooling water $7.3\times10^6$ kg/h (15→35 °C) [M Ex 8.1, p.450–452].

## 5. Pressure effects and the Carnot comparison
Internally reversible heat transfers give $\eta_{ideal}=1-\bar T_{out}/\bar T_{in}$
(Eq. 8.8): **boiler pressure up** or **condenser pressure down** raises η — the
condenser runs *below atmospheric* for exactly this reason [M §8.2.3, p.453–454]. The
ideal Rankine η still sits **below Carnot** at the same extremes (0.371 < 0.446 for
295.1/41.51 °C) because heat is added over a temperature ramp; Carnot is nevertheless a
poor plant model (combustion products must cool; a 2-phase pump is impractical) [M p.454].

## 6. Irreversibilities — Example 8.2
$$\eta_t=\frac{h_1-h_2}{h_1-h_{2s}}\ (8.9),\qquad
\eta_p=\frac{v_3(p_4-p_3)}{h_4-h_3}\ (8.10b).$$
With $\eta_t=\eta_p=0.85$ on the Ex 8.1 cycle: $h_2=1939.3$, $w_p=9.48$, $h_4=183.36$
kJ/kg → $\eta=0.314$, $\dot m=4.449\times10^5$ kg/h, $\dot Q_{in}=318.2$ MW,
$\dot Q_{out}=218.2$ MW [M Ex 8.2, p.456–458]. The turbine loss dominates; the pump
barely matters (bwr → 0.0116).

## 7. Superheat & reheat — §8.3
Higher boiler / lower condenser pressure drags turbine-exit quality down; droplets
erode blades, so plants keep $x\gtrsim0.9$ [M §8.3, p.459]. **Superheat** (boiler +
superheater = steam generator) and **reheat** (expand → reheat → expand again) raise
$\bar T_{in}$ *and* dry the exhaust. Ex 8.3 (8.0 MPa/480 °C, reheat at 0.7 MPa to
440 °C, condense at 0.008 MPa): $x_2=0.9895$, $x_4=0.9382$, $\eta=0.403$ vs 0.371,
$\dot m=2.363\times10^5$ kg/h, $\dot Q_{out}=148$ MW [M Ex 8.3, p.461–463]. With
$\eta_t=0.85$ per stage it drops to 0.351 (Ex 8.4). Supercritical plants (>22.1 MPa)
push η toward 47% [M p.460].

## Bridge
The Rankine cycle closes Topic 9's tour: Carnot (`09.1`) is the ceiling, the piston
cycles (`09.2`–`09.4`) and the Brayton (`09.5`) burn *in* the gas, Rankine boils *outside*
the loop and wins on back work ratio. Steam-table machinery lives in Topic 5
(`05.1`, `steam_tables/`); η_t/η_p come from `07.1`; the turbine/condenser/pump hardware
has its own Topic-8 modules.
