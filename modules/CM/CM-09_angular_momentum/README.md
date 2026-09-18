# CM-09 — Angular Momentum & Torque

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-01`,
`~MA-01` (cross product). **Feeds:** `~CM-11` (central forces / Kepler),
`~CM-13` (rigid bodies), `~QM-10` (quantum angular momentum).

## Scope
Angular momentum **L** = **r** × **p**, torque **N** = **r** × **F**, the rotational
equation of motion d**L**/dt = **N**, and the central-force conservation law
(**N** = 0 when **F** ∥ **r**). Reuses MA-01's `cross` and CM-01's
`velocity`/`acceleration`.

## Operations — `code/angular_momentum.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `angular_momentum(m, r, v)` | L = m (r × v) | Fowles §7.2 p.278 |
| `torque(r, F)` | N = r × F | Fowles §7.2 p.278 |
| `angular_momentum_of(m, traj)` | L(t) along a trajectory r(t) | Goldstein §1.2 p.6 |
| `torque_rate(m, traj)` | N = r × (m a) = dL/dt | Fowles §7.2 p.278 |

## Use
```python
from angular_momentum import angular_momentum, torque
angular_momentum(2, (1,0,0), (0,3,0))     # (0,0,6)
torque((2,0,0), (0,5,0))                   # (0,0,10)
torque((2,1,0), (-4,-2,0))                 # (0,0,0)  central force -> no torque
```

## Run
```bash
cd code
python3 angular_momentum.py        # demo (L, N, circular motion, dL/dt = N)
python3 test_angular_momentum.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/angular_momentum.py` · `code/test_angular_momentum.py` · `problems/problems.md`
