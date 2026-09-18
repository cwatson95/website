# 3.2 — Problems

Check with `code/first_law.py`. Citations in `../refs.md`. Signs: `Q>0` in, `W>0` by system.

### P1.  Closed-system energy balance  *(Moran 8e Eq. 2.35, p.61)*
A closed system receives `Q = +50 kJ` of heat and does `W = +30 kJ` of work, with
negligible ΔKE, ΔPE. Find ΔU.
*Answer:* `ΔU = Q − W = 50 − 30 = +20 kJ`.
*Check:* `closed_system_dU(50, 30)` = 20.

### P2.  Cooling a gas (Moran Ex. 2.2)  *(Moran 8e §2.5, p.64)*
A gas is compressed/cooled with boundary work `W = +17.6 kJ` and internal-energy
change `ΔU = −22 kJ`. Find the heat transfer and its direction.
*Answer:* `Q = ΔU + W = −22 + 17.6 = −4.4 kJ` → heat is **out** of the gas.
*Check:* `heat_transfer(-22, 17.6)` = −4.4.

### P3.  Steady-state device  *(Moran 8e Eq. 2.37, p.62)*
A gearbox at steady state rejects heat at `Q̇ = −1.2 kW`. What is the net power, and
why must `Ẇ = Q̇`?
*Answer:* steady state ⇒ `dE/dt = 0` ⇒ `Ẇ = Q̇ = −1.2 kW` (net power out is −1.2 kW,
i.e. 1.2 kW supplied as the input shaft exceeds the output by the heat loss).
*Check:* `rate_energy_balance(-1.2, -1.2)` = 0.

### P4.  First law around a cycle  *(Moran 8e Eqs. 2.40–2.41, p.73)*
A power cycle absorbs `Q_in = 1000 kJ` and rejects `Q_out = 600 kJ` per cycle. Find
the net work, and verify `W_cycle = Q_cycle`.
*Answer:* `W_cycle = Q_in − Q_out = 400 kJ`; and `Q_cycle = 1000 − 600 = 400 kJ`, so
`W_cycle = Q_cycle` (since `ΔE_cycle = 0`).
*Check:* `power_cycle_work(1000, 600)` = 400; `cycle_net_work(400)` = 400.

### P5.  Path independence of ΔU  *(Moran 8e §2.5, p.61)*
Between the same two states, path A has `(Q,W) = (80, 30) kJ` and path B has
`(Q,W) = (50, 0) kJ`. Show both give the same ΔU (as they must, U being a property).
*Answer:* `ΔU_A = 80 − 30 = 50 kJ`; `ΔU_B = 50 − 0 = 50 kJ`. Equal — only `Q − W`
is fixed; the split is path-dependent.
*Check:* `closed_system_dU(80, 30)` = `closed_system_dU(50, 0)` = 50.
