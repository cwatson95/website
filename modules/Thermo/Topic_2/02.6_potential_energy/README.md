# 2.6 — Potential Energy

Topic 2 (*Energy & Work*) module; see `modules/Thermo/list.txt`.

Energy of position in a uniform gravity field, `PE = mgz`, introduced from the
work done against gravity (Moran §2.1.2). The work done BY gravity is `−ΔPE`. The
thermo modules `1.2`/`1.EQ` carry the same `ΔPE` term (in kJ) in the energy
balance; here it is in joules.

| call | meaning |
|------|---------|
| `potential_energy(m, z, g)` | `mgz` |
| `delta_PE(m, z1, z2, g)` | `mg(z₂−z₁)` |
| `work_by_gravity(m, z1, z2, g)` | `−ΔPE` |

```bash
cd code && python3 potential_energy.py
python3 test_potential_energy.py      # "All 5 tests passed."
```

Files: `notes.md`, `code/potential_energy.py`, `code/test_potential_energy.py`,
`problems/problems.md`, `refs.md`.
