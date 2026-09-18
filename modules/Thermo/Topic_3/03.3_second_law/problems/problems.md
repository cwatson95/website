# 3.3 — Problems

Check with `code/second_law.py`. Citations in `../refs.md`. **`T` absolute (K/°R)**.

### P1.  Carnot efficiency ceiling  *(Moran 8e Eq. 5.9, p.265)*
A power cycle receives heat at `T_H = 745 K` and rejects to `T_C = 298 K`. Find the
maximum possible thermal efficiency.
*Answer:* `η_max = 1 − 298/745 = 0.60` (60%). No cycle between these reservoirs can
exceed this. *Check:* `carnot_efficiency(298, 745)` = 0.60.

### P2.  Spotting an impossible claim  *(Moran 8e §5.5, p.257)*
An inventor claims a power cycle that is 65% efficient between 745 K and 298 K. Is it
possible?
*Answer:* **No** — it exceeds the Carnot ceiling 0.60 (corollary 1). At most a
*reversible* cycle reaches 0.60. *Check:* `efficiency_is_possible(0.65, 298, 745)` → False.

### P3.  Refrigerator vs heat pump COP  *(Moran 8e Eqs. 5.10–5.11, p.267)*
A reversible cycle runs between `T_C = 250 K` and `T_H = 300 K`. Find the maximum COP
as a refrigerator and as a heat pump, and verify `γ = β + 1`.
*Answer:* `β_max = 250/50 = 5`, `γ_max = 300/50 = 6`, and `6 = 5 + 1`. *Check:*
`carnot_cop_refrigerator(250,300)` = 5; `carnot_cop_heat_pump(250,300)` = 6.

### P4.  Kelvin–Planck with one reservoir  *(Moran 8e Eqs. 5.1/5.3, p.246/254)*
Can a cycle exchanging heat with a *single* reservoir produce `W_cycle = +50 kJ`?
What about `−50 kJ`?
*Answer:* `+50` is **forbidden** (`W_cycle ≤ 0` for a single reservoir); `−50` (net
work *in*, e.g. a stirring process) is allowed. *Check:*
`kelvin_planck_allows(50)` → False; `kelvin_planck_allows(-50)` → True.

### P5.  Maximum work from a heat source  *(Moran 8e Eq. 5.9, p.265)*
A reservoir at `T_H = 745 K` supplies `Q_H = 1000 kJ`; the environment is `T_C = 298 K`.
What is the most work any cycle can extract?
*Answer:* `W_max = η_max · Q_H = 0.60 · 1000 = 600 kJ`. *Check:*
`max_work_from_heat(1000, 298, 745)` = 600.
