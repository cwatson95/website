# 1.3 — Problems

Check with `code/extensive.py`. Citations in `../refs.md`.

### P1.  Additivity of volume  *(Moran 8e §1.3.3, p.9)*
A 3 kg system at specific volume `v = 0.5 m³/kg` is divided into 2 kg and 1 kg
parts (same `v`). Show the volumes add.
*Answer:* `V = m v` gives `1.0 + 0.5 = 1.5 m³ = V(3 kg)`.
*Check:* `volume(2,0.5) + volume(1,0.5) == volume(3,0.5)` → True; `is_additive([1.0,0.5],1.5)` → True.

### P2.  Scaling with extent  *(Moran 8e §1.3.3, p.9)*
If one unit has internal energy `U = 100 kJ`, what is `U` of two identical units?
*Answer:* extensive ⇒ `2 × 100 = 200 kJ = U(2 kg at u=100)`.
*Check:* `scales_with_extent(internal_energy(1,100), 2) == internal_energy(2,100)` → True.

### P3.  Which are extensive?  *(concept — Moran 8e §1.3.3)*
Classify: `V`, `T`, `m`, `p`, `KE`, `ρ`. Then confirm the extensive ones with the
additivity test on two subsystems.
*Answer:* extensive: `V, m, KE`; intensive: `T, p, ρ` (module `1.4`).
*Check:* `kinetic_energy(2,10)+kinetic_energy(2,10)` adds; `density` does not (it
mass-averages — see `1.4`).
