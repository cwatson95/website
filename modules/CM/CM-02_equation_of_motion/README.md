# CM-02 — Equation of Motion

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-01`
(kinematics), `~MA-07` (ODE integrator). **Feeds:** `~CM-04` (work–energy),
`~CM-05` (potential energy), `~CM-06` (momentum).

## Scope
Newton's second law as the **equation of motion** m d²r/dt² = F(t, r, v),
integrated to get the trajectory. The state [r, v] is handed to **MA-07's RK4
integrator**; a small library of forces (constant, gravity, spring, drag) plus
`sum_forces` for free-body superposition.

## Operations — `code/equation_of_motion.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `trajectory(force, m, r0, v0, t0, t1, n)` | integrate m r″ = F → (ts, rs, vs) | Fowles §4.1 p.144 |
| `newton_rhs(force, m)` | the first-order RHS [v, F/m] | Fowles §2.1 p.47 |
| `constant_force`, `uniform_gravity`, `spring_force`, `linear_drag` | force builders | Fowles §2.4 p.63 |
| `sum_forces(*forces)` | net force (free-body) | Fowles §2.1 p.47 |

A `force` is `force(t, r, v) -> (Fx, Fy, Fz)`.

## Use
```python
from equation_of_motion import trajectory, uniform_gravity, spring_force
ts, rs, vs = trajectory(uniform_gravity(2.0), 2.0, (0,0,0), (10,0,10), 0, 2, 1000)  # projectile
ts, rs, vs = trajectory(spring_force(8.0), 0.5, (1,0,0), (0,0,0), 0, 5, 4000)        # SHO
```

## Run
```bash
cd code
python3 equation_of_motion.py        # demo (projectile, spring/SHO, terminal velocity)
python3 test_equation_of_motion.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/equation_of_motion.py` · `code/test_equation_of_motion.py` · `problems/problems.md`
