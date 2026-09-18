# CM-10 — Centripetal & Circular Motion

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-01`
(curvature), `~CM-02` (the force). **Links:** `~CM-11` (orbits), `~CM-12`
(rotating frames).

## Scope
Uniform circular motion and the **centripetal acceleration** a = v²/R = ω²R,
period and frequency, and the cross-check against `~CM-01`'s general curvature
(a circle has curvature 1/R and inward acceleration v²/R).

## Operations — `code/circular_motion.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `uniform_circular(R, omega)` | trajectory r(t) on a circle | Fowles §1.11 p.36 |
| `centripetal_acceleration(v, R)` | a_c = v²/R | Fowles §1.11 p.38 |
| `centripetal_force(m, v, R)` | F_c = m v²/R | Fowles §1.11 p.38 |
| `period(omega)`, `frequency(omega)`, `angular_velocity(T)` | T, f, ω | Fowles §3.x |

## Use
```python
from circular_motion import uniform_circular, centripetal_acceleration, period
centripetal_acceleration(6.0, 2.0)        # 18  (= v^2/R = omega^2 R)
period(3.0)                                # 2*pi/3
# cross-check via CM-01:
from kinematics import curvature, normal_acceleration
curvature(uniform_circular(2,3))(0.5)      # 1/R = 0.5
```

## Run
```bash
cd code
python3 circular_motion.py        # demo (centripetal relations, cross-check via CM-01)
python3 test_circular_motion.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/circular_motion.py` · `code/test_circular_motion.py` · `problems/problems.md`
