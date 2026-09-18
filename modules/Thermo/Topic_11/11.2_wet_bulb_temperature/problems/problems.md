# 11.2 — Problems

Check with `code/wet_bulb.py`. Citations in `../refs.md`. Pressures in kPa, $T$ in $^\circ$C,
enthalpies in kJ/kg, $\omega$ in kg vapor/kg dry air. Steam-table reads from Table A-2.

### P1.  Saturated exit humidity ratio $\omega'$  *(Moran Eq. 12.49, p.763)*
An adiabatic saturator with $T_{as}=25\,^\circ$C, $p=101.325$ kPa, $p_g(25^\circ\text{C})=3.169$ kPa.
Find the saturated exit humidity ratio.
*Answer:* $\omega'=0.622(3.169)/(101.325-3.169)=0.0201$. At saturation $p_v=p_g$, so this
is exactly Eq. 12.43 with $p_v=p_g$. *Check:*
`humidity_ratio_at_saturation(3.169, 101.325)` ≈ 0.02008.

### P2.  Humidity ratio from the adiabatic-saturation (≈ wet-bulb) temperature  *(Moran Eq. 12.48, p.763)*
Moist air at dry-bulb $T=40\,^\circ$C with adiabatic-saturation temperature
$T_{as}=25\,^\circ$C, $p=101.325$ kPa. Using $\omega'$ from P1, $h_a=c_{pa}T$, and
$h_f(25)=104.89$, $h_g(25)=2547.2$, $h_g(40)=2574.3$, find $\omega$.
*Answer:* $\omega=\dfrac{c_{pa}(25-40)+\omega'(2547.2-104.89)}{2574.3-104.89}
=\dfrac{-15.075+49.05}{2469.41}=0.0138$. *Check:*
`humidity_ratio_from_wet_bulb(0.020082, dry_air_enthalpy(40), dry_air_enthalpy(25), 104.89, 2547.2, 2574.3)` ≈ 0.01376.

### P3.  Energy balance is self-consistent  *(Moran Eq. 12.50, p.764)*
Verify that the $\omega$ of P2 makes the adiabatic-saturator energy balance (Eq. 12.50)
balance, i.e. its residual is zero.
*Answer:* $(h_a+\omega h_g)_T + (\omega'-\omega)h_f(T_{as}) - (h_a+\omega' h_g)_{T_{as}} = 0$.
*Check:* `adiabatic_saturator_residual(0.013759, 0.020082, dry_air_enthalpy(40), dry_air_enthalpy(25), 2574.3, 2547.2, 104.89)` ≈ 0.

### P4.  Dew point and adding moisture  *(Moran §12.5.4, p.757; Eq. 12.52, p.768)*
(a) For air with $\omega=0.0138$ at $p=101.325$ kPa, find the dew-point vapor pressure
$p_v$. (b) If steam is sprayed in at $\dot m_w/\dot m_a = 0.004$, find the exit $\omega$.
*Answer:* (a) $p_v=\omega p/(0.622+\omega)=0.0138(101.325)/(0.6358)=2.20$ kPa, dew point
$=T_{sat}(2.20\text{ kPa})\approx19\,^\circ$C. (b) $\omega_2=0.0138+0.004=0.0178$. *Check:*
`dew_point_pressure(0.0138, 101.325)` ≈ 2.20; `exit_humidity_ratio(0.0138, 0.004, 1.0)` ≈ 0.0178.
