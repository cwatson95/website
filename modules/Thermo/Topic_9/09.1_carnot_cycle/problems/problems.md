# 09.1 — Problems

Check with `code/carnot_cycle.py`. Citations in `../refs.md`. **`T` absolute (K/°R)**.

### P1.  Carnot efficiency ceiling  *(Moran 8e Ex 5.1, Eq. 5.9, p.266)*
A power cycle operates between reservoirs at `T_H = 2000 K` and `T_C = 400 K`. What is
the maximum possible thermal efficiency?
*Answer:* `η_max = 1 − 400/2000 = 0.80` (80%). No cycle between these reservoirs can
exceed this. *Check:* `carnot_efficiency(400, 2000)` = 0.80.

### P2.  Carnot bounds a real engine  *(Moran 8e §5.10.3, p.273)*
The cold air-standard Otto cycle at compression ratio 8 has `η = 0.565` (module `09.2`)
and its hot/cold extremes are about 2000 K / 400 K. Is that efficiency allowed?
*Answer:* **Yes** — 0.565 < 0.80, so it is below the Carnot ceiling (a real,
irreversible cycle). A claimed 0.85 would be **impossible**. *Check:*
`efficiency_is_possible(0.565, 400, 2000)` → True; `efficiency_is_possible(0.85, 400, 2000)` → False.

### P3.  Carnot refrigerator COP  *(Moran 8e Ex 5.2, Eq. 5.10, p.268)*
A Carnot refrigeration cycle keeps a freezer at `T_C = 268 K` while rejecting heat to
`T_H = 295 K` air. Find the maximum COP.
*Answer:* `β_max = 268/(295−268) = 268/27 = 9.93 ≈ 9.9`. *Check:*
`carnot_cop_refrigerator(268, 295)` ≈ 9.93.

### P4.  Carnot heat-pump COP and minimum work  *(Moran 8e Ex 5.3, Eq. 5.11, p.269)*
A Carnot heat pump holds a dwelling at `T_H = 530 °R` using `T_C = 492 °R` outdoor air
and must deliver `Q_H = 5×10⁵ Btu/day`. Find `γ_max` and the least work input.
*Answer:* `γ_max = 530/(530−492) = 530/38 = 13.95`; `W_min = Q_H/γ_max =
5×10⁵/13.95 = 3.58×10⁴ Btu/day`. *Check:* `carnot_cop_heat_pump(492, 530)` = 13.95;
`min_work_heat_pump(5e5, 492, 530)` ≈ 3.58×10⁴.

### P5.  Most work from a heat source  *(Moran 8e Eq. 5.9, p.271)*
A reservoir at `T_H = 2000 K` supplies `Q_H = 1000 kJ`; the surroundings are at
`T_C = 400 K`. What is the most work any cycle can extract?
*Answer:* `W_max = η_max·Q_H = 0.80·1000 = 800 kJ`. *Check:*
`max_work_from_heat(1000, 400, 2000)` = 800.
