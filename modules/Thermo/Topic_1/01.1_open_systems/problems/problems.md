# 1.1 — Problems

Work by hand from the steady-flow energy equation, then check with
`code/open_systems.py` (property values come from `../../steam_tables/` via
`steam_lookup.py`). Citations verified against the PDF — sections and pages in
`../refs.md`. Sign convention: $\dot Q$ in, $\dot W$ out.

### P1.  Steam turbine specific work  *(Moran 8e §4.7 "Turbines", p.188)*
Steam enters an adiabatic turbine at $60\,\mathrm{bar}$, $400^\circ\mathrm C$ and
leaves at $0.10\,\mathrm{bar}$ with quality $x_2=0.90$. Neglecting $\Delta ke$
and $\Delta pe$, show $\dot W_{cv}/\dot m=h_1-h_2$ and evaluate it.
Use $h_1$ from Table A‑4 and $h_2=h_f+x_2h_{fg}$ from Table A‑3 at $0.10$ bar.
*Answer:* $3177.2-2345.4=831.8\ \mathrm{kJ/kg}$.
*Check:* `turbine_power(Stream(1, st.h_superheated(60,400)), Stream(1, st.h_two_phase(0.10,0.90)))`
≈ 831.8; and `energy_rate_residual(0, 831.8, [in], [out])` ≈ 0.

### P2.  Steam nozzle exit velocity  *(Moran 8e §4.6 "Nozzles and Diffusers", Eq. 4.21, p.184)*
Steam enters a nozzle at $10\,\mathrm{bar}$, $200^\circ\mathrm C$ ($h_1=2827.9$
kJ/kg) with $V_1=10\,\mathrm{m/s}$ and expands adiabatically to $h_2=2700$ kJ/kg.
Find the exit velocity. (Watch units: $\Delta h$ in kJ/kg → ×1000 for m²/s².)
*Answer:* $V_2=\sqrt{10^2+2(1000)(2827.9-2700)}\approx 505.9\ \mathrm{m/s}$.
*Check:* `nozzle_exit_velocity(2827.9, 2700.0, V_in=10.0)` ≈ 505.9; the inverse
`diffuser_exit_enthalpy(2700.0, 505.9, 10.0)` ≈ 2827.9.

### P3.  Flashing through a throttle  *(Moran 8e §4.10 "Throttling Devices", Eq. 4.22 — Ex. 4.9, p.201)*
Saturated **liquid** water at $30\,\mathrm{bar}$ is throttled to $1\,\mathrm{bar}$.
Using $h_2=h_1$, find the quality (fraction flashed to vapor) downstream.
With $h_1=h_f(30\,\mathrm{bar})=1008.4$ kJ/kg and, at $1$ bar, $h_f=417.46$,
$h_{fg}=2258.0$: $x_2=(h_1-h_f)/h_{fg}$.
*Answer:* $x_2=(1008.4-417.46)/2258.0=0.262$ (≈26% flashes to vapor).
*Check:* `h1 = st.sat_pressure(30)['hf']; h2 = throttle_exit_enthalpy(h1);
s = st.sat_pressure(1.0); x2 = (h2 - s['hf'])/s['hfg']` → ≈ 0.262.

### P4.  Open feedwater heater (adiabatic mixing)  *(Moran 8e §4.9 "Heat Exchangers", p.196)*
In an open feedwater heater, superheated steam at $20\,\mathrm{bar}$,
$320^\circ\mathrm C$ ($h=3069.5$ kJ/kg, $\dot m=1\,\mathrm{kg/s}$) mixes directly
with subcooled liquid water ($h\approx167.6$ kJ/kg, $\dot m=4\,\mathrm{kg/s}$).
For $\dot Q=\dot W=0$, find the exit enthalpy.
*Answer:* $h_e=\dfrac{1(3069.5)+4(167.6)}{5}\approx 748.0\ \mathrm{kJ/kg}$.
*Check:* `mixing_exit_enthalpy([Stream(1.0, st.h_superheated(20,320)), Stream(4.0, 167.6)])`
≈ 748.

### P5.  Heat-exchanger flow ratio  *(Moran 8e §4.9 "Heat Exchangers", p.196)*
A closed (no-mixing) heat exchanger has a hot stream giving up enthalpy
$3000\to500$ kJ/kg and a cold stream taking $100\to400$ kJ/kg. With
$\dot Q_{cv}=\dot W=0$ around both streams, find $\dot m_{cold}/\dot m_{hot}$.
*Answer:* $(3000-500)/(400-100)=2500/300=8.33$.
*Check:* `heat_exchanger_flow_ratio(3000, 500, 100, 400)` ≈ 8.33.

### P6.  Continuity at a junction  *(Moran 8e §4.2 "Forms of the Mass Rate Balance", Eq. 4.4b/4.6, p.172)*
Two inlets feed one outlet at steady state: $\dot m_1=6$, $\dot m_2=4\,\mathrm{kg/s}$.
Find $\dot m_3$. If the outlet pipe has $v=0.5\,\mathrm{m^3/kg}$ and
$V=20\,\mathrm{m/s}$, find its area $A$ from $\dot m=AV/v$.
*Answer:* $\dot m_3=10\,\mathrm{kg/s}$; $A=\dot m v/V=10(0.5)/20=0.25\,\mathrm{m^2}$.
*Check:* `mass_rate_residual([Stream(6,0), Stream(4,0)], [Stream(10,0)])` = 0;
`mass_flow_rate(0.25, 20, 0.5)` = 10.
