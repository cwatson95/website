# MA-22 — Topology & Dynamical Systems  [adv]

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-04` (eigenvalues),
`~MA-07` (ODEs), `~MA-14`/`~MA-17` (d²=0 → de Rham, for the topology side).
**Feeds:** `~CM-24` (nonlinear dynamics & chaos), `~CM-15` (oscillator stability),
`~PK-03` (plasma instabilities).

## Scope
**Dynamical systems**: the linear-stability **classification of equilibria** from
the Jacobian's eigenvalues (saddle / node / spiral / center), and the **logistic
map's** route to chaos — period-doubling, the **Lyapunov exponent** λ=⟨ln|f′|⟩
(negative on stable cycles, positive in chaos, exactly ln 2 at r=4), and a
period-3 window. **Topology**: the **Euler characteristic** χ=V−E+F, a *topological
invariant* — 2 for every convex polyhedron (a sphere), 0 for the torus, 2−2g for
genus g.

## Operations — `code/topo_dynamics.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `eigenvalues_2x2(J)` | the two eigenvalues of J | Chicone §1.6 p.20 |
| `classify_equilibrium(J)` | saddle/node/spiral/center | Chicone §1.6 pp.20–23 |
| `logistic(r, x)`, `logistic_orbit` | the map x→rx(1−x) and its orbit | Chicone Ch.6 p.449 |
| `lyapunov_logistic(r)` | Lyapunov exponent ⟨ln\|f′\|⟩ | Chicone p.28 (Lyapunov) |
| `period_of_orbit(r)` | period of the attracting cycle | Chicone Ch.8 p.545 (bifurcation) |
| `euler_characteristic(V,E,F)` | χ = V−E+F (topological invariant) | Hatcher p.6 / p.146 |
| `PLATONIC` | (V,E,F) of the five solids (all χ=2) | Hatcher p.6 |

## Use
```python
import math
from topo_dynamics import classify_equilibrium, lyapunov_logistic, period_of_orbit, euler_characteristic

classify_equilibrium([[-1, -2], [2, -1]])   # 'stable spiral' (eigenvalues -1 +/- 2i)
period_of_orbit(3.5)                          # 4  (period-doubled)
lyapunov_logistic(4.0)                        # ~ ln 2 = 0.693  (chaos)
euler_characteristic(*(8, 12, 6))             # 2  (the cube is a sphere)
```

## Run
```bash
cd code
python3 topo_dynamics.py          # demo (equilibria, logistic chaos, Euler characteristic)
python3 test_topo_dynamics.py     # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/topo_dynamics.py` · `code/test_topo_dynamics.py` · `problems/problems.md`
