# 2.7 — Buoyancy

Topic 2 (*Energy & Work*) module; see `modules/Thermo/list.txt`. A **fluid-statics**
cross-link (`~CM`) that uses the hydrostatic pressure of `1.4`/§1.6.

- **Builds on:** pressure & the pressure–depth relation (`1.4`, Moran §1.6).
- **Cross-trunk:** belongs to fluid mechanics (Classical Mechanics trunk); kept
  here for completeness — wire to a fluids module when networking.

## Scope
**Archimedes' principle:** a submerged (or floating) body feels an upward buoyant
force equal to the **weight of the fluid it displaces**,
$$F_b=\rho_\text{fluid}\,g\,V_\text{displaced}.$$
Moran derives it in §1.6.2 from the pressure–depth relation. Consequences: a body
floats iff its mean density is below the fluid's, and a freely floating body
submerges a fraction `ρ_object/ρ_fluid` of its volume.

| call | meaning |
|------|---------|
| `buoyant_force(ρ_fluid, V, g)` | `F_b = ρgV` |
| `apparent_weight(W, ρ_fluid, V)` | `W − F_b` |
| `floats(ρ_object, ρ_fluid)` | `ρ_object < ρ_fluid` |
| `submerged_fraction(ρ_object, ρ_fluid)` | `ρ_object/ρ_fluid` |

## Run
```bash
cd code && python3 buoyancy.py       # F_b, iceberg fraction, apparent weight
python3 test_buoyancy.py             # "All 7 tests passed."
```

## Files
`notes.md`, `code/buoyancy.py`, `code/test_buoyancy.py`, `problems/problems.md`, `refs.md`.
