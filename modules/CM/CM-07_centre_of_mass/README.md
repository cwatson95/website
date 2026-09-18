# CM-07 — Centre of Mass

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-06`.
**Feeds:** `~CM-08` (collisions in the CM frame), `~CM-11` (two-body → one-body).

## Scope
The centre of mass of a system, its velocity, the **reduced mass** of a two-body
problem, and the CM/relative decomposition. Pure stdlib.

## Operations — `code/centre_of_mass.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `centre_of_mass(masses, positions)` | R = Σmᵢrᵢ / Σmᵢ | Fowles §7.1 p.275 |
| `cm_velocity(masses, velocities)` | V = Σmᵢvᵢ / Σmᵢ | Fowles §7.1 p.275 |
| `reduced_mass(m1, m2)` | μ = m₁m₂/(m₁+m₂) | Fowles §7.3 p.283 |
| `relative_coordinate(r1, r2)` | r = r₁ − r₂ | Fowles §7.3 p.283 |
| `two_body_decompose(m1, m2, r1, r2)` | (R, r) | Fowles §7.3 p.283 |

## Use
```python
from centre_of_mass import centre_of_mass, reduced_mass, two_body_decompose
centre_of_mass([3,1], [[0,0,0],[4,0,0]])      # [1,0,0]  (toward the heavy mass)
reduced_mass(2.0, 2.0)                         # 1.0  (= m/2)
two_body_decompose(1, 1, [0,0,0], [2,0,0])    # (R=[1,0,0], r=[-2,0,0])
```

## Run
```bash
cd code
python3 centre_of_mass.py        # demo
python3 test_centre_of_mass.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/centre_of_mass.py` · `code/test_centre_of_mass.py` · `problems/problems.md`
