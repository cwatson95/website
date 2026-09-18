# 2.5 — Kinetic Energy

Topic 2 (*Energy & Work*) module; see `modules/Thermo/list.txt`.

Energy of bulk motion, `KE = ½mV²`, introduced from the work–energy idea: the net
work of the resultant force equals the change in kinetic energy (Moran §2.1.1).
The thermo modules `1.2`/`1.EQ` use the same `ΔKE` term (in kJ) inside the energy
balance; here it is in joules.

| call | meaning |
|------|---------|
| `kinetic_energy(m, V)` | `½mV²` |
| `delta_KE(m, V1, V2)` | `½m(V₂²−V₁²)` |
| `work_from_KE(m, V1, V2)` | net work = `ΔKE` |
| `speed_after_work(m, V1, W)` | `√(V₁²+2W/m)` |

```bash
cd code && python3 kinetic_energy.py
python3 test_kinetic_energy.py        # "All 5 tests passed."
```

Files: `notes.md`, `code/kinetic_energy.py`, `code/test_kinetic_energy.py`,
`problems/problems.md`, `refs.md`.
