# 6.5 — Conservation of Mass Flow (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The mass rate balance
For a control volume (CV) the conservation-of-mass principle is the **mass rate
balance** [M §4.1.1, p.170]:
$$\frac{dm_{cv}}{dt}=\sum_i \dot m_i-\sum_e \dot m_e\quad(4.2),$$
the rate of change of mass inside the CV equals the total inlet rate minus the total
exit rate. For a single inlet and single exit it is `dm_cv/dt = ṁi − ṁe` (Eq. 4.1).
The dots denote time rates of transfer (kg/s).

## 2. Evaluating the mass flow rate
For a **one-dimensional** stream (flow normal to the boundary; uniform intensive
properties over the area) the mass flow rate is [M §4.2.1, p.172]:
$$\dot m=\rho\,A\,V\quad(4.4a),\qquad \dot m=\frac{A\,V}{v}\quad(4.4b),$$
with `A` the flow area, `V` the velocity normal to `A`, `v` the specific volume
(`ρ=1/v`). The product `AV` is the **volumetric flow rate** (m³/s). Inverting Eq. 4.4b
gives the velocity `V = ṁv/A`. (The general definition is `ṁ = ∫_A ρVn dA`, Eq. 4.3.)

## 3. Steady state
Many systems are idealized as being at **steady state**: every property is unchanging
in time, so there is no accumulation, `dm_cv/dt = 0`, and Eq. 4.2 reduces to
[M §4.2.2, p.173]:
$$\sum_i \dot m_i=\sum_e \dot m_e\quad(4.6)$$
— total incoming and outgoing mass rates are equal. Note: equality of total in/out
rates does **not** by itself prove steady state (other properties could vary), and
steady state does **not** imply one-dimensional flow — these are independent
idealizations.

**`ṁ = AV/v` is a property–geometry coupling.** *Check (M Ex 4.1, feedwater heater,
steady, 2 inlets + 1 exit):* saturated liquid exits at `7 bar` with `(AV)₃ = 0.06 m³/s`,
`v₃ = 1.108×10⁻³ m³/kg`, so `ṁ₃ = 0.06/1.108e-3 = 54.15 kg/s`. With `ṁ₁ = 40 kg/s`,
the steady balance gives `ṁ₂ = ṁ₃ − ṁ₁ = 14.15 kg/s`, and `V₂ = ṁ₂v₂/A₂ =
14.15(1.0078e-3)/(25 cm²) = 5.7 m/s`. *Transient (M Ex 4.2, barrel):* `ṁi = 30 lb/s`,
`ṁe = 9L`, so `dL/dt → 0` gives the steady height `9L = 30 ⇒ L = 3.33 ft`.

## Bridge
The steady mass balance `Σṁi=Σṁe` (Eq 4.6) is reused verbatim by the steady-state
**energy** rate balance (module `6.4`, Eq 4.20), and `ṁ=AV/v` sizes every nozzle,
turbine, compressor, and heat-exchanger duct analyzed in Topics 7–9.
