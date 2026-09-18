# CM-08 — Collisions & Scattering

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-06`,
`~CM-07`. **Links:** `~CM-11` (central-force orbits), `~QM-18` (quantum scattering).

## Scope
One-dimensional **elastic** and **inelastic** collisions (conserving momentum, and
— for elastic — kinetic energy), the centre-of-mass connection, and **Rutherford
scattering** (the angle–impact-parameter relation and the differential
cross-section). Reuses `~CM-07` (`cm_velocity`, `reduced_mass`).

## Operations — `code/collisions.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `elastic_collision_1d(m1,v1,m2,v2)` | final velocities (conserves p & T) | Fowles §7.5 p.303 |
| `inelastic_collision(m1,v1,m2,v2)` | common (= CM) velocity | Fowles §7.5 p.303 |
| `rutherford_angle(b, E, k)` | θ = 2 arctan(k/2Eb) | Fowles §6.14 p.264 |
| `rutherford_cross_section(θ, E, k)` | (k/4E)²/sin⁴(θ/2) | Goldstein §3.10 p.110 |

## Use
```python
from collisions import elastic_collision_1d, inelastic_collision, rutherford_angle
elastic_collision_1d(1, 3, 1, -1)        # (-1, 3)  equal masses swap velocities
inelastic_collision(2, [4,0,0], 1, [0,0,0])   # [8/3,0,0]  (the CM velocity)
rutherford_angle(0.5, 1.0, 1.0)          # pi/2  (90 deg)
```

## Run
```bash
cd code
python3 collisions.py        # demo (elastic/inelastic, Rutherford)
python3 test_collisions.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/collisions.py` · `code/test_collisions.py` · `problems/problems.md`
