# CM-12 — Non-inertial (Rotating) Frames

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-03`,
`~MA-01` (cross product). **Links:** `~CM-10` (centripetal), `~RE-10`
(equivalence principle).

## Scope
The fictitious accelerations in a frame rotating at angular velocity **ω**: the
**centrifugal** −ω×(ω×r) and the **Coriolis** −2ω×v (plus the Euler term when ω
changes). Reuses MA-01's `cross`.

## Operations — `code/rotating_frames.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `centrifugal_acceleration(omega, r)` | −ω×(ω×r), outward, ω²ρ | Fowles §5.3 p.196 |
| `coriolis_acceleration(omega, v)` | −2ω×v, ⟂ to ω and v | Fowles §5.3 p.196 |
| `euler_acceleration(omega_dot, r)` | −ω̇×r (changing rotation) | Fowles §5.3 p.196 |
| `centrifugal_force`, `coriolis_force` | ×m | Fowles §5.3 p.196 |

## Use
```python
from rotating_frames import centrifugal_acceleration, coriolis_acceleration
centrifugal_acceleration((0,0,2), (3,0,0))     # (12,0,0)  = omega^2 r, outward
coriolis_acceleration((0,0,2), (0,1,0))        # (4,0,0)   perp to omega and v
```

## Run
```bash
cd code
python3 rotating_frames.py        # demo
python3 test_rotating_frames.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/rotating_frames.py` · `code/test_rotating_frames.py` · `problems/problems.md`
