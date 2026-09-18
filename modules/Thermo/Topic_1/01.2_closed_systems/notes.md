# 1.2 — Closed Systems / Control Mass (notes)

A **closed system** (control mass) always contains the same matter — **no mass
crosses its boundary** — so it interacts with its surroundings only through heat
`Q` and work `W` [M §1.2.1, p.6]. (An **isolated** system exchanges neither.)
This is the control-mass special case of module `1.1`: drop the flow terms
`Σ ṁ(h+V²/2+gz)` from the open-system balance and what remains is below.

Citations: **M** = Moran, Shapiro, Boettner & Bailey 8e; *printed* pages
(PDF = printed + 17; table in `refs.md`).

## 1. The closed-system energy balance
Energy is conserved, so the change in the system's total energy equals the net
energy transferred in as heat and out as work [M §2.5, Eqs. 2.35a–b, p.61]:
$$\underbrace{E_2-E_1}_{\Delta KE+\Delta PE+\Delta U}=Q-W .$$
Spelled out,
$$\boxed{\;\Delta KE+\Delta PE+\Delta U=Q-W\;}$$
with the sign convention $Q>0$ **into** the system, $W>0$ done **by** the system.
The kinetic and potential pieces are
$$\Delta KE=\tfrac12 m\,(V_2^2-V_1^2),\qquad \Delta PE=m g\,(z_2-z_1)$$
[M §2.1, Eqs. 2.5 & 2.10]. Code: `energy_balance_residual` returns
$(Q-W)-(\Delta U+\Delta KE+\Delta PE)$ (zero when satisfied); `heat_transfer`
and `work_done` solve it for $Q$ or $W$; `delta_KE`, `delta_PE` give the
mechanical terms. *Unit care:* $\tfrac12 mV^2$ and $mgz$ come out in J, so the
code divides by 1000 to reach kJ.

The **time-rate** form is [M §2.5.1, Eq. 2.37, p.62]:
$$\frac{dE}{dt}=\dot Q-\dot W .$$
Code: `power_balance_residual`. *Check:* with no kinetic/potential change,
$\Delta U=Q-W$ — heat added at fixed volume ($W=0$) all goes to internal energy.

## 2. Boundary (`∫p dV`) work
When the system boundary moves through a volume change, the work is [M §2.2.3,
Eq. 2.17, p.48]:
$$W=\int_{V_1}^{V_2} p\,dV .$$
This requires the pressure $p$ to be **defined** along the path, i.e. a
**quasiequilibrium** process (module `1.5`); only then is $W$ the area under the
process curve on a $p$–$V$ diagram. Code: `pdv_work_trapz(p_of_V, V1, V2)`
integrates any path numerically.

## 3. Polytropic processes
A common, integrable path is the **polytropic** process $pV^{n}=\text{const}$, so
$p_2=p_1(V_1/V_2)^n$ [M §2.2.5, p.50]. Its work integrates in closed form
[M Example 2.1, Eqs. (a)–(b), p.50–51]:
$$W=\begin{cases}\dfrac{p_2V_2-p_1V_1}{1-n}, & n\neq 1,\\[2mm]
   p_1V_1\,\ln\dfrac{V_2}{V_1}, & n=1 \ \text{(isothermal ideal gas).}\end{cases}$$
Code: `polytropic_work`, `polytropic_pressure`; the special case $n=0$ is
constant pressure, `constant_pressure_work` $=p(V_2-V_1)$. *Checks:* the
closed form agrees with `pdv_work_trapz` to 4 digits; an adiabatic ($Q=0$)
compression with $W<0$ raises $U$ by $|W|$.

## Worked example — polytropic compression
Air is compressed in a piston–cylinder along $pV^{1.3}=\text{const}$ from
$p_1=100\,\mathrm{kPa},\ V_1=1\,\mathrm{m^3}$ to $V_2=0.5\,\mathrm{m^3}$. Then
$p_2=100(1/0.5)^{1.3}=246.2\,\mathrm{kPa}$ and
$$W=\frac{p_2V_2-p_1V_1}{1-n}=\frac{246.2(0.5)-100(1)}{1-1.3}=-77.05\ \mathrm{kJ},$$
work **in** (the surroundings do work on the gas). If the compression is
adiabatic, $\Delta U=Q-W=+77.05\,\mathrm{kJ}$ — the internal energy (and
temperature) rise. Code reproduces both numbers, and `pdv_work_trapz` returns the
same $-77.05$ kJ.

## Bridge
Adding the flow terms to §1 gives module `1.1` (open systems); the gas-power
**cycles** of group `9` (Otto, Diesel, Stirling) are closed-system piston cycles
built from these `∫p dV` legs and the energy balance.
