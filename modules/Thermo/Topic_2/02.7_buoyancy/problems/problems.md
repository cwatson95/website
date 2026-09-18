# 2.7 — Problems

Check with `code/buoyancy.py`. Citations in `../refs.md`.

### P1.  Buoyant force  *(Moran 8e §1.6.2, p.16)*
Find the buoyant force on a `1 m³` object fully submerged in water (`ρ=1000 kg/m³`).
*Answer:* `F_b = ρgV = 1000·9.81·1 = 9810 N`.
*Check:* `buoyant_force(1000, 1)` = 9810.

### P2.  Tip of the iceberg  *(Moran 8e §1.6.2, p.16–17)*
Ice (`ρ=917`) floats in seawater (`ρ=1025`). What fraction is submerged?
*Answer:* `V_sub/V_tot = ρ_ice/ρ_sea = 917/1025 ≈ 0.895` (≈ 89.5 %).
*Check:* `submerged_fraction(917, 1025)` ≈ 0.895.

### P3.  Apparent weight  *(Moran 8e §1.6.2; cf. Problem 1.54)*
A steel block (`ρ=7850`) weighs 100 N in air. Find its apparent weight fully
submerged in water.
*Answer:* `V = 100/(7850·9.81) = 1.30×10⁻³ m³`; `F_b = 1000·9.81·V ≈ 12.7 N`;
apparent `≈ 87.3 N`.
*Check:* `apparent_weight(100, 1000, 100/(7850*9.81))` ≈ 87.3.
