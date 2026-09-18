# 07.1 — Problems

Check with `code/efficiency.py`. Citations in `../refs.md`. Cycle `Q`, `W` are **positive
magnitudes**; Carnot `T` is **absolute (K/°R)**.

### P1.  Thermal efficiency of a power cycle  *(Moran 8e Eqs. 2.42/2.43, p.74)*
A power cycle receives `Q_in = 1000 kJ` and rejects `Q_out = 200 kJ`. Find the net work
and the thermal efficiency.
*Answer:* `W_cycle = Q_in − Q_out = 800 kJ`, so `η = 800/1000 = 0.80` (80%), equivalently
`1 − 200/1000 = 0.80`. *Check:* `thermal_efficiency(800,1000)` =
`thermal_efficiency_from_heat(1000,200)` = 0.80.

### P2.  Carnot ceiling — is the claim possible?  *(Moran 8e Eq. 5.9, p.265; Ex 5.1)*
The cycle of P1 runs between reservoirs at `T_H = 2000 K` and `T_C = 400 K`. What is the
maximum possible efficiency, and is a claimed 85% achievable?
*Answer:* `η_max = 1 − 400/2000 = 0.80`. The P1 cycle (η = 0.80) is at the reversible
limit; a claimed 85% is **impossible**. *Check:* `carnot_efficiency(400,2000)` = 0.80;
`efficiency_is_possible(0.85,400,2000)` → False.

### P3.  Refrigerator COP vs. its ceiling  *(Moran 8e Eqs. 2.45/5.10, p.75/267; Ex 5.2)*
A freezer pulls `Q_C = 8000 kJ/h` from a compartment at `−5 °C (268 K)` using
`W_cycle = 3200 kJ/h`, rejecting to `22 °C (295 K)` air. Find `β` and the reversible
maximum `β_max`.
*Answer:* `β = 8000/3200 = 2.5`; `β_max = 268/(295−268) = 9.9`. Since 2.5 < 9.9,
irreversibilities are present. *Check:* `cop_refrigerator(8000,3200)` = 2.5;
`carnot_cop_refrigerator(268,295)` ≈ 9.93.

### P4.  Heat pump: `γ = β + 1` and its ceiling  *(Moran 8e Eqs. 2.47/5.11, p.75/267)*
The same machine as P3 viewed as a heat pump delivers `Q_H = Q_C + W = 11200 kJ/h`.
Find `γ` and verify `γ = β + 1`; also give `γ_max` between 268 K and 295 K.
*Answer:* `γ = 11200/3200 = 3.5 = 2.5 + 1`; `γ_max = 295/(295−268) = 10.9 = β_max + 1`.
*Check:* `cop_heat_pump(11200,3200)` = 3.5; `carnot_cop_heat_pump(268,295)` ≈ 10.93.

### P5.  Isentropic turbine work  *(Moran 8e Eq. 6.46, p.333; Ex 6.11)*
Steam enters a turbine at `h_1 = 3105.6 kJ/kg`; for the actual exit pressure the
isentropic exit enthalpy is `h_2s = 2743.0 kJ/kg`. If `η_t = 0.75`, find the actual work
per unit mass.
*Answer:* `w = η_t(h_1 − h_2s) = 0.75(3105.6 − 2743.0) = 271.95 kJ/kg`. *Check:*
`turbine_work_actual(0.75, 3105.6, 2743.0)` ≈ 271.95.

### P6.  Isentropic compressor efficiency  *(Moran 8e Eq. 6.48, p.338; Ex 6.14)*
A compressor takes refrigerant from `h_1 = 249.75` to an actual `h_2 = 294.17 kJ/kg`; the
isentropic exit is `h_2s = 285.58 kJ/kg`. Find `η_c`.
*Answer:* `η_c = (285.58 − 249.75)/(294.17 − 249.75) = 35.83/44.42 = 0.81` (81%). *Check:*
`isentropic_compressor_efficiency(249.75, 294.17, 285.58)` ≈ 0.81.

### P7.  Isentropic nozzle efficiency  *(Moran 8e Eq. 6.47, p.335; Ex 6.13)*
A steam nozzle has actual exit kinetic energy `V_2²/2 = 114.8 Btu/lb` versus an
isentropic `(V_2²/2)_s = 124.3 Btu/lb`. Find the nozzle efficiency.
*Answer:* `η_n = 114.8/124.3 = 0.924` (92.4%). *Check:*
`isentropic_nozzle_efficiency(114.8, 124.3)` ≈ 0.924.
