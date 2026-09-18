# CM-01 — Kinematics

First module of the **CLASSICAL MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~MA-01` (vector algebra) — used directly.
- **Feeds into:** `~CM-09` (angular momentum **L** = **r**×**p**, torque), `~CM-10`
  (centripetal motion), `~CM-11` (central-force orbits), `~CM-03` (frames).

## Scope
Description of *motion* (no forces yet): position, velocity and acceleration of a
particle as vector-valued **functions of time**, the tangential/normal split of
the acceleration, curvature, projectile motion, and the plane-polar
decomposition (centripetal + Coriolis terms).

This is the first **consumer of MA-01**: a trajectory is a function `r(t)`, and
`velocity`/`acceleration` differentiate it while MA-01's `dot`/`cross`/`norm`
act on the resulting functions. Citations with page numbers are in `refs.md`
and inline in `notes.md`, so every formula is checkable against the books in
`books/library/CM_Classical_Mechanics/`.

## Operations — `code/kinematics.py`

| call | meaning | reference |
|------|---------|-----------|
| `velocity(r)` | **v** = d**r**/dt (central difference) | Fowles §1.10 p.31; M&T §1.14 p.30; Goldstein §1.1 p.1 |
| `acceleration(r)` | **a** = d²**r**/dt² | M&T Eq.1.88 p.30 |
| `speed(r)` | \|**v**(t)\| | — |
| `tangent(r)` | unit tangent **T** = **v**/\|**v**\| | Fowles Prob. 1.25 p.46 |
| `tangential_acceleration(r)` | a_T = (**a**·**v**)/\|**v**\| = d\|**v**\|/dt | Fowles Prob. 1.25 p.46 |
| `normal_acceleration(r)` | a_N = \|**v**×**a**\|/\|**v**\| = v²/ρ | Fowles Prob. 1.26 p.46 |
| `curvature(r)` / `radius_of_curvature(r)` | κ = \|**v**×**a**\|/\|**v**\|³, ρ = 1/κ | Fowles Prob. 1.27 p.46 |
| `projectile(speed0, angle, g)` | **r**(t) under uniform gravity | Fowles §4.3 p.156; M&T Ex.2.6 p.63 |
| `time_of_flight`, `range_`, `max_height` | analytic projectile results | Fowles §4.3 p.156 |
| `uniform_acceleration(r0,v0,a)` | **r** = **r₀** + **v₀**t + ½**a**t² | M&T §2.4 p.55 |
| `polar_position(rho, theta)` | planar **r**(t) from ρ(t), θ(t) | Fowles §1.11 p.36 |
| `polar_acceleration_components(rho, theta)` | (a_r, a_θ) = (ρ̈−ρθ̇², ρθ̈+2ρ̇θ̇) | Fowles §1.11 p.36; M&T Eq.1.97–98 p.32 |

Everything returns a **function of t** (built on MA-01's `lift`), so results compose.

## Use
```python
import math
from kinematics import projectile, acceleration, speed, curvature, range_

r = projectile(20.0, math.radians(40.0))   # r(t), a vector function
acceleration(r)(0.3)                        # ~ (0, 0, -9.81)
range_(20.0, math.radians(40.0))            # 40.16 m

circ = lambda t: (2*math.cos(3*t), 2*math.sin(3*t), 0.0)
speed(circ)(0.6), curvature(circ)(0.6)      # 6.0 (=Rω),  0.5 (=1/R)

# bridge to CM-09: specific angular momentum, reusing MA-01's cross
from vector_algebra import cross
from kinematics import velocity
L = cross(r, velocity(r))                    # a function of t
```

## Run
```bash
cd code
python3 kinematics.py            # demo: projectile, circular motion, polar split
python3 test_kinematics.py       # tests  ->  "All N tests passed."
```
(`kinematics.py` imports MA-01's `vector_algebra` by relative path; this becomes
`from physkit.vector_algebra import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/kinematics.py`, `code/test_kinematics.py`
- `problems/problems.md` — worked problems (Fowles, Marion & Thornton)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
