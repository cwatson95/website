# 11.1 — Problems

Check with `code/dry_bulb.py`. Citations in `../refs.md`. Pressures in consistent units
(here lbf/in.² or bar), $\omega$ in kg(or lb) vapor per kg(lb) dry air, $h$ in
kJ/kg(dry air). $p_g$ values are Table A-2 / A-2E reads.

### P1.  Humidity ratio from $\phi$ (Ex 12.7a)  *(Moran Eqs. 12.43–12.44, p.755)*
Moist air at $70\,^\circ$F, $14.7\;\text{lbf/in.}^2$, relative humidity $\phi=70\%$.
With $p_g(70^\circ\text{F})=0.3632\;\text{lbf/in.}^2$ find $p_{v1}$ and $\omega_1$.
*Answer:* $p_{v1}=\phi p_g=0.70(0.3632)=0.2542\;\text{lbf/in.}^2$; then
$\omega_1=0.622(0.2542)/(14.7-0.2542)=0.011$. *Check:*
`vapor_pressure_from_phi(0.70, 0.3632)` ≈ 0.2542;
`humidity_ratio_from_pressures(0.2542, 14.7)` ≈ 0.011.

### P2.  Dew point and mass split (Ex 12.7b,c)  *(Moran §12.5.4, p.757)*
For the P1 sample (1 lb total), find the masses of dry air and vapor, and the dew point.
*Answer:* $m_a=1/(1+\omega_1)=0.9891$ lb, $m_v=\omega_1 m_a=0.0109$ lb. Cooling at
constant $p$, the vapor saturates when $p_g=p_{v1}=0.2542$, i.e. at $T_{sat}=60\,^\circ$F
(Table A-2E). *Check:* `dry_air_mass(1.0, 0.011)` ≈ 0.9891;
`vapor_mass(1.0, 0.011)` ≈ 0.0109.

### P3.  Saturated state sets the maximum $\omega$  *(Moran Eq. 12.43, p.755)*
Cooling the P1 air to $40\,^\circ$F ($p_g(40^\circ\text{F})=0.1217$) leaves it saturated
($p_v=p_g$). Find $\omega_2$ and the vapor condensed per lb sample.
*Answer:* $\omega_2=0.622(0.1217)/(14.7-0.1217)=0.0052$; condensate
$m_w=m_a(\omega_1-\omega_2)=0.9891(0.011-0.0052)\approx 0.0058$ lb. *Check:*
`humidity_ratio_from_pressures(0.1217, 14.7)` ≈ 0.0052.

### P4.  Mixture enthalpy per unit dry air  *(Moran Eqs. 12.46–12.47, p.755)*
A chart point has dry-bulb $22\,^\circ$C, $\omega=0.002$. Using $h_a=c_{pa}T=1.005(22)$
and $h_v\approx h_g(22^\circ\text{C})=2541.7$ kJ/kg, find the mixture enthalpy per kg dry
air. *Answer:* $h=h_a+\omega h_v=22.11+0.002(2541.7)=27.2$ kJ/kg(dry air) — the chart
value at the Example 12.12 inlet. *Check:*
`mixture_enthalpy_per_dry_air(1.005*22, 0.002, 2541.7)` ≈ 27.2.
