# 08.2 — Problems

Check with `code/condenser.py`. Citations in `../refs.md`. `h` [kJ/kg], `ṁ` [kg/s],
`Q̇` in matching power units.

### P1.  Two-phase inlet enthalpy  *(Moran 8e §3.6, p.103)*
Steam enters a condenser at 0.1 bar with quality `x = 0.95`. With `hf = 191.83`,
`hg = 2584.7 kJ/kg` (Table A-3), find `h_in`.
*Answer:* `h_in = 191.83 + 0.95(2584.7−191.83) = 2465.1 kJ/kg`. *Check:*
`enthalpy_two_phase(191.83, 2584.7, 0.95)` ≈ 2465.1.

### P2.  Steam-side heat rejection (Ex 4.7)  *(Moran 8e §4.9.1, p.198)*
The condensate leaves at 45 °C (`h_out ≈ hf = 188.45 kJ/kg`). Find the heat transfer per
kg of steam and state its direction.
*Answer:* `Q̇cv/ṁ = h_out − h_in = 188.45 − 2465.1 = −2276.7 kJ/kg`; the minus sign means
energy is rejected from the steam to the cooling water. *Check:*
`heat_transfer_rate(1, 2465.1, 188.45)` ≈ −2276.7.

### P3.  Heat-pump condenser duty (Ex 10.4)  *(Moran 8e Eq. 10.5, p.632)*
R-134a enters the condenser at `h2 = 280.19` and leaves at `h3 = 105.29 kJ/kg`, with
`ṁ = 0.2 kg/s`. Find the heating rate delivered.
*Answer:* `Q̇out = ṁ(h2−h3) = 0.2(174.90) = 34.98 kW`. *Check:*
`heat_rejected(0.2, 280.19, 105.29)` ≈ 34.98.

### P4.  Exit quality of a partially-condensed stream  *(Moran 8e §3.6, p.103)*
A refrigerant leaves a condenser at `h = 120 kJ/kg` where `hf = 100`, `hg = 280 kJ/kg`.
Is it fully condensed? Find the quality.
*Answer:* `x = (120−100)/(280−100) = 0.111` — still a two-phase mixture (11.1% vapor), so
the condenser has **not** fully condensed the stream. *Check:*
`quality_from_h(120, 100, 280)` ≈ 0.111.
