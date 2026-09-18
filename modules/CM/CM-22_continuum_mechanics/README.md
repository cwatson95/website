# CM-22 — Continuum Mechanics & the Continuity Equation

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-02`.
**KEY BRIDGE B2** — the same law is mass here, charge in `~EM-13`, probability in
`~QM-04`. **Links:** `~CM-23` (fluids), `~PK-02` (plasma fluid).

## Scope
Local conservation of mass: the **continuity equation** ∂ρ/∂t + ∇·(ρv) = 0, the
**material derivative** D/Dt = ∂/∂t + v·∇, and the equivalence of the Eulerian and
material forms. Reuses MA-02's `divergence`/`gradient`.

## Operations — `code/continuum_mechanics.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `continuity_residual(rho, v, x,y,z,t)` | ∂ρ/∂t + ∇·(ρv) (= 0 if mass conserved) | Boas §6.10 p.317; Griffiths §8.1.1 p.356 |
| `material_derivative(f, v, x,y,z,t)` | Df/Dt = ∂f/∂t + v·∇f | Boas §6.10 p.314 |
| `divergence_of_velocity(v, x,y,z,t)` | ∇·v (local expansion rate) | Boas §6.7 p.296 |

Fields take (x, y, z, t): `rho(...)->scalar`, `v(...)->(vx,vy,vz)`.

## Use
```python
import math
from continuum_mechanics import continuity_residual
c = 0.5
rho = lambda x,y,z,t: math.exp(-(x-c*t)**2)     # density bump advected at speed c
v   = lambda x,y,z,t: (c, 0, 0)
continuity_residual(rho, v, 0.3, 0, 0, 1.0)     # ~0  (mass conserved)
```

## Run
```bash
cd code
python3 continuum_mechanics.py        # demo (travelling wave, Eulerian vs material form)
python3 test_continuum_mechanics.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/continuum_mechanics.py` · `code/test_continuum_mechanics.py` · `problems/problems.md`
