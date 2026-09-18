# 1.1 — Open Systems / Control Volumes (notes)

A **closed system** is a fixed quantity of matter; only energy crosses its
boundary. An **open system** — a **control volume** (CV) — is instead a fixed
*region* of space whose boundary (the **control surface**) **mass is free to
cross**. Almost every working device (turbine, pump, nozzle, boiler, valve) is
analyzed as a CV. The whole subject is two book-keeping laws — mass and energy —
written for matter flowing through that region.

Citations: **M** = Moran, Shapiro, Boettner & Bailey 8e; page numbers are the
*printed* book pages (PDF = printed + 17; full table in `refs.md`).

## 1. Closed system vs. control volume
A system is whatever we draw the boundary around; everything else is the
surroundings [M §1.2, p.4]. If the boundary admits no mass it is a **closed
system** (a *control mass*); if it admits mass it is a **control volume / open
system** [M §1.2.1–1.2.2, p.6]. Choosing the control surface well — often right
across the inlet and exit pipes of a device — is half the work [M §1.2.3, p.7].
This module *generalizes* the closed-system energy balance of `1.2` to account
for the energy that flowing mass carries in and out.

## 2. Conservation of mass for a control volume
Mass is neither created nor destroyed, so the rate it accumulates in the CV is
what flows in minus what flows out [M §4.1, Eq. 4.2, p.170]:
$$\frac{dm_{cv}}{dt}=\sum_i \dot m_i-\sum_e \dot m_e .$$
For **one-dimensional flow** across a port of area $A$, normal velocity $V$, and
specific volume $v$ (so density $\rho=1/v$) [M §4.2.1, Eq. 4.4b, p.172]:
$$\boxed{\;\dot m=\frac{AV}{v}=\rho A V\;}$$
Code: `mass_flow_rate(A, V, v)`, and `mass_rate_residual(inlets, outlets)` for
the accumulation term. *Check:* $A=0.1\,\mathrm{m^2}$, $V=20\,\mathrm{m/s}$,
$v=0.2\,\mathrm{m^3/kg}\Rightarrow\dot m=10\,\mathrm{kg/s}$.

## 3. Flow work, and why enthalpy appears
To push a unit mass across the boundary against the local pressure $p$, the
surroundings do **flow work** $p v$ on the CV [M §4.4.2, "commonly referred to as
flow work", Eqs. 4.12–4.13, p.179]. Every stream therefore transports its
internal energy *plus* this flow work, and the two always travel together as the
combination we name **enthalpy**:
$$h \equiv u + p v .$$
That is the whole reason $h$ — not $u$ — is the natural energy variable for
open systems (and why the steam tables tabulate $h$).

## 4. The control-volume energy rate balance
Adding the kinetic and potential energy each stream also carries, the
first law for a control volume is [M §4.4.3, Eq. 4.15, p.180]:
$$\boxed{\;\frac{dE_{cv}}{dt}=\dot Q_{cv}-\dot W_{cv}
  +\sum_i \dot m_i\!\left(h_i+\tfrac{V_i^2}{2}+gz_i\right)
  -\sum_e \dot m_e\!\left(h_e+\tfrac{V_e^2}{2}+gz_e\right)\;}$$
Sign convention: $\dot Q_{cv}>0$ **into** the CV, $\dot W_{cv}>0$ **done by** the
CV (the shaft work of a turbine). The per-stream group is the **specific flow
energy**
$$\psi \equiv h+\tfrac{V^2}{2}+gz ,$$
so the balance is $dE_{cv}/dt=\dot Q-\dot W+\sum_i\dot m_i\psi_i-\sum_e\dot m_e\psi_e$.
Code: `flow_energy(h, V, z)` returns $\psi$ and `energy_rate_residual(Qdot, Wdot,
inlets, outlets)` returns $dE_{cv}/dt$. *Unit care:* $h$ is in kJ/kg but $V^2/2$
and $gz$ come out in J/kg, so the code divides them by 1000; then
$\dot m\,[\mathrm{kg/s}]\times\psi\,[\mathrm{kJ/kg}]=\mathrm{kW}$, matching
$\dot Q,\dot W$.

## 5. Steady state
At steady state nothing in the CV changes with time: $dm_{cv}/dt=0$ and
$dE_{cv}/dt=0$ [M §4.5.1, Eqs. 4.6 & 4.18, p.181]. Mass in = mass out, and
$$0=\dot Q_{cv}-\dot W_{cv}
  +\sum_i \dot m_i\,\psi_i-\sum_e \dot m_e\,\psi_e .$$
For a single inlet $1$ and single exit $2$ (so $\dot m_1=\dot m_2=\dot m$) this
is the **steady-flow energy equation** [M Eq. 4.20a]:
$$0=\dot Q_{cv}-\dot W_{cv}
  +\dot m\!\left[(h_1-h_2)+\tfrac{V_1^2-V_2^2}{2}+g(z_1-z_2)\right].$$
Code: `shaft_power(inlet, outlet, Qdot)` solves this for $\dot W_{cv}$;
`turbine_power` / `compressor_power` are its two signs.

## 6. The steady-flow device set
Each common component is just this one equation with terms switched off — these
are the idealizations later modules (`8`, `9`) build on:

- **Nozzle / diffuser** [M §4.6, Eq. 4.21, p.184]: $\dot W=0$, $\dot Q\approx0$,
  $\Delta pe\approx0\Rightarrow h_1+\tfrac{V_1^2}{2}=h_2+\tfrac{V_2^2}{2}$, hence
  $V_2=\sqrt{V_1^2+2\,(h_1-h_2)}$. Code: `nozzle_exit_velocity`,
  `diffuser_exit_enthalpy` (the inverse).
- **Turbine** [M §4.7, p.188] / **compressor, pump** [M §4.8, p.190]:
  $\dot Q\approx0$, $\Delta ke,\Delta pe\approx0\Rightarrow
  \dot W_{cv}=\dot m\,(h_1-h_2)$ — positive out for a turbine, negative (work in)
  for a compressor/pump. Code: `turbine_power`, `compressor_power`.
- **Throttling valve** [M §4.10, Eq. 4.22, p.201]: $\dot W=0$, $\dot Q\approx0$,
  $\Delta ke\approx0\Rightarrow \boxed{h_2=h_1}$ — pressure drops at constant
  enthalpy. Code: `throttle_exit_enthalpy`.
- **Heat exchanger / mixing** [M §4.9, p.196]: $\dot W=0$, and for the CV around
  *both* streams $\dot Q_{cv}\approx0$, giving $\sum_i\dot m_ih_i=\sum_e\dot m_eh_e$.
  Code: `heat_exchanger_flow_ratio` (closed, no mixing) and
  `mixing_exit_enthalpy` (direct contact).

### Worked example — steam turbine (ties to `../../steam_tables/`)
Steam enters at $60\,\mathrm{bar}$, $400^\circ\mathrm C$ and leaves at
$0.10\,\mathrm{bar}$ with quality $x_2=0.90$; neglect $\Delta ke,\Delta pe$ and
take $\dot Q\approx0$. From Table **A‑4**, $h_1=3177.2\,\mathrm{kJ/kg}$; from
Table **A‑3** at $0.10\,\mathrm{bar}$, $h_2=h_f+x_2h_{fg}=191.83+0.90(2392.8)
=2345.4\,\mathrm{kJ/kg}$. Then
$$\frac{\dot W_{cv}}{\dot m}=h_1-h_2=831.8\ \mathrm{kJ/kg}.$$
Code reproduces this from the CSVs:
`turbine_power(Stream(1, st.h_superheated(60,400)), Stream(1, st.h_two_phase(0.10,0.90)))`
$\approx 831.8$, and `energy_rate_residual(0, 831.8, [in], [out])\approx0` — the
balance closes. *Check:* including the kinetic term for $V_1=10$, $V_2=90$ m/s
lowers it by $\tfrac{V_2^2-V_1^2}{2}=4.0\,\mathrm{kJ/kg}$ to $827.8$.

## Bridge
Steady-state mass/energy here *are* leaves `6.4` (steady-state) and `6.5`
(conservation of mass flow); the device idealizations seed the component modules
in group `8` and the **Rankine** (`9.6`) and **Brayton** (`9.5`) cycles, which
chain several control volumes together.
