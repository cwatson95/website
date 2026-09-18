# 4.2 — Problems

Check with `code/entropy.py`. Citations in `../refs.md`. `s,c,cp,cv,R` [kJ/kg·K], `T` [K].

### P1.  Entropy is a property, σ is not (Ex 6.1 vs 6.2)  *(Moran 8e §6.7, p.303–309)*
Water goes from saturated liquid to saturated vapor at 150 °C (`s₁=1.8418`,
`s₂=6.8379`). Compare (a) an internally reversible isothermal path and (b) an
adiabatic paddle-wheel path.
*Answer:* `Δs = 4.9961 kJ/kg·K` for **both**. (a) `Q/m = T·Δs = 423.15(4.9961) =
2114.1 kJ/kg`, `σ = 0`. (b) `Q = 0` ⇒ `σ/m = Δs = 4.9961 kJ/kg·K`, `W/m = −1927.82`.
Same Δs, different σ. *Check:* `heat_isothermal_rev(423.15, 4.9961)` ≈ 2114.1;
`entropy_production_closed(6.8379, 1.8418, 0)` ≈ 4.9961.

### P2.  Ideal-gas entropy change is a property (HW 6.11)  *(Moran 8e Eq. 6.20a, p.300)*
Air goes from 300 K, 100 kPa to 500 K, 650 kPa. Find Δs for a reversible vs an
irreversible path (`s°(300)=1.70203`, `s°(500)=2.21952`, `R=0.287`).
*Answer:* `Δs = 2.21952 − 1.70203 − 0.287·ln(6.5) = −0.0197 kJ/kg·K`, **identical**
both ways (Δs is a property; only σ differs). *Check:*
`entropy_change_ideal_gas_tables(1.70203, 2.21952, 0.287, 100, 650)` ≈ −0.0197.

### P3.  Rigid insulated tank with a paddle (HW 6.37)  *(Moran 8e §6.7, p.350)*
2 m³ of air at 293 K, 200 kPa (rigid, insulated) receives 710 kJ of paddle work;
`cv = 0.72 kJ/kg·K`. Find the mass, `T₂`, and the entropy produced.
*Answer:* `m = pV/RT = 400/(0.287·293) = 4.757 kg`; adiabatic rigid ⇒ `ΔU = −W =
+710 = m·cv(T₂−293)` ⇒ `T₂ = 500.3 K`; `σ = m·cv·ln(T₂/T₁) = 1.83 kJ/K`. *Check:*
`4.757·entropy_change_ideal_gas_cv(0.72,0.287,293,500.3,1,1)` ≈ 1.83.

### P4.  Entropy produced by thermal mixing (HW 6.59)  *(Moran 8e §6.7, p.352)*
A 1 kg metal block at 1075 K (`c=0.5`) is quenched in 100 kg of water at 295 K
(`c=4.2`); the pair is isolated. Find the final temperature and σ.
*Answer:* `T_f = (0.5·1075 + 420·295)/(420.5) = 295.93 K`;
`σ = 0.5·ln(T_f/1075) + 420·ln(T_f/295) = −0.645 + 1.318 = 0.673 kJ/K > 0`. *Check:*
`entropy_change_incompressible(0.5,1075,295.93) + 100·entropy_change_incompressible(4.2,295,295.93)` ≈ 0.673.
