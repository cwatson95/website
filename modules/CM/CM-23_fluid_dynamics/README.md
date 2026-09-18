# CM-23 — Fluid Dynamics

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~MA-02`,
`~CM-22` (continuity). **Links:** `~PK-03` (plasma fluid description), `~CM-25`
(waves in media).

## Scope
The kinematic descriptors of a flow: **vorticity** ω = ∇×v, the
**incompressibility** test ∇·v = 0, the **irrotationality** test ∇×v = 0, and
**Bernoulli's** constant ½v² + p/ρ + gz. Reuses MA-02's `curl`/`divergence`.

## Operations — `code/fluid_dynamics.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `vorticity(v)` | ω = ∇×v (curl field) | Boas §6.10 p.314 |
| `is_incompressible(v)` | ∇·v = 0 ? | Boas §6.10 p.316 |
| `is_irrotational(v)` | ∇×v = 0 ? | Boas §6.10 p.314 |
| `bernoulli_constant(speed, p, rho, z, g)` | ½v² + p/ρ + gz | (standard result) |

A steady velocity field is `v(x, y, z) -> (vx, vy, vz)`.

## Use
```python
from fluid_dynamics import vorticity, is_incompressible, is_irrotational
rigid = lambda x,y,z: (-1.5*y, 1.5*x, 0)        # rigid rotation
vorticity(rigid)(1,0,0)                          # (0,0,3) = 2*Omega
is_incompressible(rigid)                         # True;  is_irrotational(rigid) -> False
```

## Run
```bash
cd code
python3 fluid_dynamics.py        # demo (vorticity, incompressible/irrotational, Bernoulli)
python3 test_fluid_dynamics.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/fluid_dynamics.py` · `code/test_fluid_dynamics.py` · `problems/problems.md`
