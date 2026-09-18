# 2.6 — Problems

Check with `code/potential_energy.py`. Citations in `../refs.md`.

### P1.  Lifting a mass  *(Moran 8e §2.1.2, Eq. 2.10, p.42)*
Find the change in potential energy when 10 kg is raised 50 m (`g=9.81`).
*Answer:* `ΔPE = mg(z₂−z₁) = 10·9.81·50 = 4905 J`.
*Check:* `delta_PE(10,0,50)` = 4905.

### P2.  Work done by gravity  *(Moran 8e §2.1.2, p.42)*
The same mass now falls 50 m. How much work does gravity do?
*Answer:* `W_grav = −ΔPE = +4905 J` (gravity does positive work on the falling mass).
*Check:* `work_by_gravity(10,50,0)` = 4905.
