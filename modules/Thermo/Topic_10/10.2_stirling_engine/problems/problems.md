# 10.2 — Problems

Check with `code/stirling_engine.py`. Citations in `../refs.md`. Air `R = 0.287`,
`c_v = 0.718 kJ/kg·K`; temperatures **absolute**; `r = V_max/V_min`.

### P1.  Ideal Stirling efficiency = Carnot  *(Moran 8e §9.8.4, p.552; Eq. 5.9, p.265)*
A Stirling engine with 100 % regeneration runs between `T_H = 1000 K` and `T_C = 300 K`.
Find the thermal efficiency.
*Answer:* `η = 1 − T_C/T_H = 1 − 300/1000 = 0.70` — the Carnot ceiling. *Check:*
`stirling_efficiency(300, 1000)` ≈ 0.70.

### P2.  Per-process isothermal heats  *(Moran 8e §9.8.4, p.552; Eq. 2.17, p.49)*
For air with `r = 2`, find the external heat added (3–4 at `T_H`), the heat rejected (1–2 at
`T_C`), and the net work, per unit mass.
*Answer:* `Q_34 = R T_H ln r = 0.287·1000·ln2 = 198.9 kJ/kg`; `Q_12 = R T_C ln r = 59.7 kJ/kg`;
`W = R(T_H−T_C) ln r = 139.3 kJ/kg`, and `W/Q_34 = 0.70` recovers P1. *Check:*
`stirling_heat_added(0.287,1000,2)` ≈ 198.9; `stirling_heat_rejected(0.287,300,2)` ≈ 59.7;
`stirling_net_work(0.287,1000,300,2)` ≈ 139.3.

### P3.  The regenerator's internal duty  *(Moran 8e §9.8.4, p.552; Eq. 3.50, p.140)*
How much heat does the ideal regenerator shuttle between processes 4–1 and 2–3?
*Answer:* `Q_regen = c_v(T_H−T_C) = 0.718·700 = 502.6 kJ/kg` (stored in 4–1, returned in 2–3).
*Check:* `regenerator_heat(0.718, 1000, 300)` ≈ 502.6.

### P4.  Efficiency with NO regenerator  *(Moran 8e §9.8.4, p.552)*
If the regenerator is removed, the constant-volume heating 2–3 must be supplied externally.
Find the efficiency (air, `r = 2`).
*Answer:* `η = W/(Q_34 + c_v(T_H−T_C)) = 139.3/(198.9 + 502.6) = 0.198` — far below the 0.70
Carnot value; the regenerator is what makes the Stirling engine competitive. *Check:*
`stirling_efficiency_no_regen(0.287, 0.718, 1000, 300, 2)` ≈ 0.198.

### P5.  Regenerator effectiveness  *(Moran 8e Eq. 9.27, §9.7, p.539)*
A regenerator raises the cold-stream enthalpy from `h_2 = 300` toward the hot-stream
`h_4 = 800 kJ/kg`. Find the effectiveness if the actual exit enthalpy is `h_x = 700`, and for
ideal regeneration (`h_x = h_4`).
*Answer:* `η_reg = (h_x−h_2)/(h_4−h_2) = (700−300)/(800−300) = 0.80`; ideal `→ 1.00`. *Check:*
`regenerator_effectiveness(700,300,800)` ≈ 0.80; `regenerator_effectiveness(800,300,800)` ≈ 1.0.
