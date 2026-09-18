# CM-05 — Conservative Forces & Potential Energy

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-04`,
`~MA-02` (gradient & curl). **Feeds:** `~CM-11` (effective potential / orbits),
`~CM-15` (oscillations about a minimum).

## Scope
The conservative force **F = −∇U**, the curl test for conservativeness, the total
mechanical energy E = T + U, and the **stability of equilibria** (minima of U).
Reuses MA-02's `gradient`/`curl` and MA-01's `dot`.

## Operations — `code/potential_energy.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `force_from_potential(U)` | F = −∇U | Fowles §4.2 p.151 |
| `is_conservative(F)` | curl F = 0 ? | Fowles §4.1 p.146 |
| `total_energy(m, v, U, r)` | E = ½m|v|² + U | Fowles §4.2 p.152 |
| `is_equilibrium(U1d, x)` | U′(x) = 0 ? | Fowles §2.3 p.63 |
| `is_stable(U1d, x)` | U″(x) > 0 ? (a minimum) | Fowles §2.3 p.63 |

## Use
```python
from potential_energy import force_from_potential, is_conservative, total_energy
U = lambda x,y,z: 0.5*3*(x*x+y*y+z*z)         # isotropic spring
F = force_from_potential(U)                    # -> F = -3 r
is_conservative(F)                             # True (gradient field, curl 0)
is_conservative(lambda x,y,z:(-y,x,0))         # False (rotational)
```

## Run
```bash
cd code
python3 potential_energy.py        # demo (F=-grad U, conservativeness, energy, double well)
python3 test_potential_energy.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/potential_energy.py` · `code/test_potential_energy.py` · `problems/problems.md`
