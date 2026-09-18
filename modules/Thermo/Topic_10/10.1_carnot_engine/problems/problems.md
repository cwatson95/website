# 10.1 — Problems

Check with `code/carnot_engine.py`. Citations in `../refs.md`. **`T` absolute (K/°R)**.

### P1.  Carnot efficiency  *(Moran 8e Eq. 5.9, p.265; Example 5.1)*
A Carnot engine receives heat at `T_H = 2000 K` and rejects to `T_C = 400 K`. Find the
thermal efficiency.
*Answer:* `η_max = 1 − 400/2000 = 0.80` (80%). *Check:* `carnot_efficiency(400, 2000)` = 0.80.

### P2.  Carnot heats and work  *(Moran 8e Eqs. 5.7/5.9, p.262/265)*
The engine of P1 receives `Q_H = 1000 kJ`. How much heat does it reject, and what net
work does it deliver?
*Answer:* reversible ⇒ `Q_C = Q_H·T_C/T_H = 1000·(400/2000) = 200 kJ`, so
`W = Q_H − Q_C = 800 kJ` ( = `η_max·Q_H`). *Check:* `carnot_heat_rejected(1000,400,2000)` = 200;
`carnot_work(1000,400,2000)` = 800.

### P3.  Reversible / irreversible / impossible  *(Moran 8e Example 5.1, p.266)*
For the reservoirs of P1 (`η_max = 0.80`), classify three claimed power cycles:
(a) `η = 60%`; (b) `W_cycle = 850 kJ` from `Q_H = 1000 kJ`; (c) `Q_C = 200 kJ` from
`Q_H = 1000 kJ`.
*Answer:* (a) `0.60 < 0.80` → **irreversible**; (b) `η = 0.85 > 0.80` → **impossible**;
(c) `η = 0.80 = η_max` → **reversible**. *Check:* `cycle_status(0.60,400,2000)` →
`"irreversible"`; `cycle_status(0.85,400,2000)` → `"impossible"`;
`cycle_status(0.80,400,2000)` → `"reversible"`.

### P4.  Inventor's claim  *(Moran 8e Example 5.1 Quick Quiz, p.267)*
A cycle between 2000 K and 400 K is claimed to reject `Q_C = 300 kJ` while producing
`W_cycle = 2700 kJ`. Possible?
*Answer:* `Q_H = W + Q_C = 3000 kJ`, so `η = 2700/3000 = 0.90 > 0.80` → **impossible**.
*Check:* `cycle_status(0.90, 400, 2000)` → `"impossible"`.

### P5.  Reversed Carnot cycle — COPs  *(Moran 8e Eqs. 5.10–5.11, p.267; §5.10.2)*
The Carnot cycle of P1 is run **in reverse** between `T_C = 268 K` and `T_H = 295 K`.
Find the COP as a refrigerator and as a heat pump, and verify `γ = β + 1`.
*Answer:* `β_max = 268/(295−268) = 9.93`, `γ_max = 295/27 = 10.93`, and
`10.93 = 9.93 + 1`. *Check:* `carnot_cop_refrigerator(268,295)` ≈ 9.93;
`carnot_cop_heat_pump(268,295)` ≈ 10.93.
