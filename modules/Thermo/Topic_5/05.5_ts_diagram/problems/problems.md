# 5.5 — Problems

Check with `code/ts_diagram.py`. Citations in `../refs.md`. `T` [K] (absolute!),
`s` [kJ/kg·K], `Q` [kJ/kg]; `S` [kJ/K], `Q` [kJ]. Entropy data from `steam_tables/`.

### P1.  Reversible isothermal heat — Moran Ex 6.1  *(Moran 8e Eq. 6.23, p.304)*
Water is vaporized reversibly at constant `T = 150 °C` (423.15 K) from saturated liquid
(`sf = 1.8418`) to saturated vapor (`sg = 6.8379 kJ/kg·K`). Find `Q/m`.
*Answer:* `Q/m = T(s₂ − s₁) = 423.15(6.8379 − 1.8418) = 2114.1 kJ/kg` — the rectangular
area under the isotherm. *Check:* `heat_isothermal(423.15, 1.8418, 6.8379)` ≈ 2114.1.

### P2.  Area = trapezoid  *(Moran 8e §6.6.1, p.302)*
A reversible process has `T` linear in `s` from `(300 K, 0)` to `(500 K, 2 kJ/K)`. Find the
heat.
*Answer:* `Q = ½(T₁ + T₂)(S₂ − S₁) = ½(300 + 500)(2) = 800 kJ` (trapezoid area). *Check:*
`heat_linear_TS(300,500,0,2)` = 800 = `heat_TdS([300,500],[0,2])`.

### P3.  Carnot cycle on T–s  *(Moran 8e §6.6.2, p.303)*
A Carnot power cycle runs between `T_H = 600 K` and `T_C = 300 K` with `ΔS = 1 kJ/K`. Find
`Q_in`, `Q_out`, `W_net`, and the efficiency.
*Answer:* `Q_in = T_H ΔS = 600 kJ`, `Q_out = T_C ΔS = 300 kJ`, `W_net = (T_H − T_C)ΔS =
300 kJ` (enclosed rectangle), `η = 1 − T_C/T_H = 0.5`. *Check:* `heat_isothermal(600,0,1)`
= 600; `carnot_net_work(600,300,1)` = 300; `carnot_efficiency(600,300)` = 0.5.

### P4.  Isentropic leg carries no heat  *(Moran 8e §6.6, p.302)*
What is the heat for the adiabatic-reversible (isentropic) legs of the Carnot cycle?
*Answer:* `Q = ∫T dS = 0` because `dS = 0` (constant entropy). *Check:*
`heat_TdS([600,300],[2.0,2.0])` = 0.

### P5.  Mollier (h–s) isentropic expansion  *(Moran 8e §6.2.5, p.296)*
Water at `240 °C`, `0.10 MPa` (state 1) expands isentropically to `0.01 MPa` (state 2).
Read `x₂` and `h₂` (the Mollier-chart construction, cross-checked against the tables).
*Answer:* `s₂ = s₁ = s(240 °C, 1 bar) ≈ 7.99 kJ/kg·K`; at `0.1 bar`,
`x₂ = (s₂ − sf)/(sg − sf) ≈ 0.98` and `h₂ = hf + x₂(hg − hf) ≈ 2537 kJ/kg` (Moran's stated
chart values). *Check:* computed from `5.1` A-3/A-4 reads, `x₂ ≈ 0.979`, `h₂ ≈ 2535 kJ/kg`
(within chart-reading accuracy); see `5.EP` `ex_mollier`.
