# 2.4 — Problems

Check with `code/power.py`. Citations in `../refs.md`.

### P1.  Shaft power of a motor  *(Moran 8e §2.2.6, Eq. 2.20, p.53; cf. Ex 2.6)*
A motor output shaft delivers `τ = 9.7 N·m` at `1000 rpm`. Find the shaft power (kW).
*Answer:* `ω = 1000·2π/60 = 104.7 rad/s`; `Ẇ = τω ≈ 1016 W ≈ 1.016 kW`.
*Check:* `shaft_power(9.7, rpm_to_rad_s(1000))` ≈ 1015.8.

### P2.  Electric heater energy  *(Moran 8e §2.2.6, Eq. 2.21, p.53; cf. HW 2.39)*
A heater draws `6 A` at `220 V`. Find its power and the energy used in 24 h.
*Answer:* `Ẇ = VI = 1320 W = 1.32 kW`; `E = 1.32·24 = 31.68 kW·h`.
*Check:* `electric_power(220,6)/1000` = 1.32; `energy_from_power(1320, 24*3600)/3.6e6` = 31.68.

### P3.  Tractive power  *(Moran 8e §2.2.2, Eq. 2.13, p.46)*
A vehicle pushes with a steady `500 N` at `4 m/s`. Find the power delivered.
*Answer:* `Ẇ = F·V = 2000 W = 2 kW`.
*Check:* `power_force_velocity(500, 4)` = 2000.
