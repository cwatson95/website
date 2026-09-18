# CM-03 — Reference Frames

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereq:** `~CM-01`.
**Links:** `~RE-01` (where the Galilean rule breaks down), `~CM-07`/`~CM-08`
(the centre-of-mass frame for collisions), `~CM-12` (rotating frames).

## Scope
Galilean transformations between inertial frames (r′ = r − Vt, v′ = v − V) and
the **centre-of-mass (C) frame**, in which the total momentum is zero. Pure
vector arithmetic.

## Operations — `code/reference_frames.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `galilean_position(r, V, t)` | r′ = r − V t | Fowles §5.1 p.184 |
| `galilean_velocity(v, V)` | v′ = v − V | Fowles §5.1 p.184 |
| `relative_velocity(va, vb)` | vₐ − v_b (frame-independent) | Fowles §2.1 p.54 |
| `cm_velocity(masses, vels)` | V_cm = Σmᵢvᵢ / Σmᵢ | Fowles §7.1 p.275 |
| `to_cm_frame(masses, vels)` | velocities in the C-frame (ΣP = 0) | Fowles §7.6 p.306 |
| `total_momentum(masses, vels)` | Σ mᵢ vᵢ | Fowles §7.1 p.277 |

## Use
```python
from reference_frames import galilean_velocity, cm_velocity, to_cm_frame, total_momentum
galilean_velocity([3,0,0], [1,0,0])                 # [2,0,0]
cm_velocity([2,1], [[1,0,0],[-2,0,0]])              # [0,0,0]
total_momentum([2,1], to_cm_frame([2,1], [[1,0,0],[-2,0,0]]))   # [0,0,0]
```

## Run
```bash
cd code
python3 reference_frames.py        # demo
python3 test_reference_frames.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/reference_frames.py` · `code/test_reference_frames.py` · `problems/problems.md`
