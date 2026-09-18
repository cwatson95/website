# 2.1 — Problems

Check with `code/work.py`. Citations in `../refs.md`. Sign: `W>0` done BY system.

### P1.  Spring work is quadratic  *(Moran 8e §2.2.6, p.52)*
A linear spring, `k=200 N/m`, is stretched from its natural length to 0.1 m, then
to 0.2 m. Find the work to each, and explain why the second is 4×, not 2×, the first.
*Answer:* `W = ½k x²` → 1 J and 4 J; `W ∝ x²`, so doubling `x` quadruples `W`.
*Check:* `spring_work(200,0,0.1)` = 1.0; `spring_work(200,0,0.2)` = 4.0.

### P2.  Shaft vs electrical work  *(Moran 8e §2.2.6, Eqs. 2.20/2.21, p.53)*
A shaft delivers `τ=18 N·m` at `ω=100 rad/s` for 1 s; separately an element draws
`110 V, 10 A` for 1 s. Find each work.
*Answer:* shaft `W=τω·dt = 1800 J` (out); electrical `|W| = VI·dt = 1100 J` (in).
*Check:* `shaft_work(18,100,1)` = 1800; `electric_work(110,10,1)` = 1100.

### P3.  Work from a variable force  *(Moran 8e §2.2, Eq. 2.12, p.44)*
A force `F(s) = 10 s` (N, s in m) acts over 0 → 2 m. Find the work.
*Answer:* `W = ∫₀² 10s ds = 5s²|₀² = 20 J`.
*Check:* `work_force_displacement(lambda s: 10*s, 0, 2)` ≈ 20.

### P4.  Boundary work, constant pressure  *(Moran 8e Eq. 2.17, p.48)*
A gas at constant 200 kPa expands 1 → 1.5 m³. Find the boundary work.
*Answer:* `W = ∫p dV = 200(0.5) = 100 kJ` (done by the gas).
*Check:* `boundary_work(lambda V: 200, 1, 1.5)` ≈ 100.
