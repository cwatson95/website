# 6.2 — Problems

Check with `code/irreversible.py`. Citations in `../refs.md`. `T` absolute (K/°R);
`σ` [kJ/K or Btu/°R]; ideal-gas air `R = 0.287 kJ/kg·K`, incompressible/ideal-gas `c` as given.

### P1.  Quenching a smaller bar (Ex 6.5 Quick Quiz)  *(Moran 8e §6.8.1, p.315)*
A **0.45-lb** metal bar at 1900 °R is quenched in 20 lb of water at 530 °R; `c_w = 1.0`,
`c_m = 0.1 Btu/lb·°R`, tank adiabatic. Find `T_f` and the entropy produced.
*Answer:* energy balance `m_w c_w(T_f−T_wi) + m_m c_m(T_f−T_mi) = 0` ⇒ `T_f = 533 °R`;
`σ = m_w c_w ln(T_f/T_wi) + m_m c_m ln(T_f/T_mi) = 0.1129 − 0.0572 = 0.0557 Btu/°R > 0`
(book answer). *Check:* `sigma_isolated(entropy_change_incompressible(20,1.0,533,530),
entropy_change_incompressible(0.45,0.1,533,1900))` ≈ 0.0557.

### P2.  Air stirred in a rigid insulated tank (HW 6.37)  *(Moran 8e §6, p.350)*
2 m³ of air, initially 293 K, 200 kPa, in a **rigid, insulated** tank with a paddle wheel
receives 710 kJ of paddle work; `c_v = 0.72 kJ/kg·K`. Find (a) mass, (b) `T₂`, (c) σ.
*Answer:* `m = p₁V₁/(RT₁) = (200)(2)/(0.287·293) = 4.76 kg`. Adiabatic, rigid:
`ΔU = −W = 710 kJ = m c_v(T₂−T₁)` ⇒ `T₂ = 293 + 710/(4.76·0.72) ≈ 500 K`. Rigid ⇒ v const,
so `σ = ΔS = m c_v ln(T₂/T₁) = 3.425·ln(500.3/293) ≈ 1.83 kJ/K > 0`. *Check:* with `m=4.757`,
`entropy_change_incompressible(4.757, 0.72, 500.3, 293)` ≈ 1.83 (same form `m c ln(T₂/T₁)`).

### P3.  Heat across a finite ΔT (HW 6.53)  *(Moran 8e §6, p.351)*
10 lb of air in a **rigid** tank at 1 atm, 600 °R is heated by a reservoir at 900 °R until
the air reaches 800 °R; the boundary where heat crosses is at 900 °R. Air `c_v = 0.171
Btu/lb·°R`. Find `Q` and σ.
*Answer:* `Q = ΔU = m c_v(T₂−T₁) = 10(0.171)(200) = 342 Btu`. Rigid ⇒
`ΔS = m c_v ln(T₂/T₁) = 1.71·ln(800/600) = 0.4919 Btu/°R`; entropy transfer `= Q/T_b =
342/900 = 0.380`; `σ = ΔS − Q/T_b = 0.4919 − 0.380 = 0.112 Btu/°R > 0` (finite-ΔT heat
transfer is irreversible). *Check:* `entropy_production(entropy_change_incompressible(10,
0.171,800,600), 342/900)` ≈ 0.112.

**Method.** Build the energy balance for `Q`/`W`, the entropy balance for σ. For a rigid
(constant-volume) ideal gas `ΔS = m c_v ln(T₂/T₁)`; the entropy transfer is `∫δQ/T_b`. A
positive σ confirms the process is possible and irreversible; σ < 0 would be impossible.
