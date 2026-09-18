# 6.4 — Steady-State Operation (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. What "steady state" means
A control volume (CV) is at **steady state** when every property is unchanging in time.
The mass and energy in the CV do not accumulate, so the storage (time-derivative) terms
of the rate balances are zero [M §4.5.1, p.181]:
$$\frac{dm_{cv}}{dt}=0,\qquad \frac{dE_{cv}}{dt}=0.$$
The mass flow rates and the rates of heat and work transfer are also constant in time.
(Steady operation excludes startup and shutdown transients.)

## 2. The steady-state rate balances
With `dm_cv/dt = 0` the mass rate balance becomes `Σṁi = Σṁe` (Eq. 4.6, module `6.5`).
With `dE_cv/dt = 0` the energy rate balance (Eq. 4.15) reduces to [M §4.5.1, p.181]:
$$0=\dot Q_{cv}-\dot W_{cv}+\sum_i\dot m_i\!\left(h_i+\tfrac{V_i^2}{2}+gz_i\right)-\sum_e\dot m_e\!\left(h_e+\tfrac{V_e^2}{2}+gz_e\right)\quad(4.18).$$
For the common **one-inlet/one-exit** device (`ṁ₁ = ṁ₂ = ṁ`):
$$0=\dot Q_{cv}-\dot W_{cv}+\dot m\!\left[(h_1-h_2)+\tfrac{V_1^2-V_2^2}{2}+g(z_1-z_2)\right]\quad(4.20a),$$
or, per unit mass, dividing by `ṁ` (Eq. 4.20b). Only boundary transfer quantities
appear — the balance says nothing about, and needs nothing about, the CV interior.

## 3. Modeling notes
- The enthalpy, KE, and PE terms appear as inlet−exit *differences*, so the datums used
  for `h`, `V`, `z` cancel [M §4.5.1, p.182].
- For turbines/compressors the net KE and PE of the stream are usually negligible next
  to `Δh`, leaving `Ẇcv = ṁ(h₁−h₂)` for an adiabatic turbine [M §4.7.1, p.188].

**Steady state collapses storage, not transfer.** *Check (M Ex 4.4, steam turbine):*
`ṁ = 4600 kg/h`, `Ẇcv = 1000 kW`; inlet `h₁ = 3177.2 kJ/kg`, `V₁ = 10 m/s`; exit
`h₂ = 2345.4 kJ/kg`, `V₂ = 30 m/s`. `ΔKE = (30²−10²)/2 = 400 J/kg = 0.4 kJ/kg` (small).
`Q̇cv = Ẇcv + ṁ[(h₂−h₁)+ΔKE] = 1000 + (4600/3600)(−831.8+0.4) = −62.3 kW` — heat *out*,
small next to the power. Neglecting KE gives −62.9 kW.

## Bridge
The steady-state energy balance (Eq 4.20) is the workhorse for every flow device in
Topic 7 (and, combined with the entropy balance, sets isentropic efficiencies in module
`6.3`). The mass side `Σṁi=Σṁe` is module `6.5`.
