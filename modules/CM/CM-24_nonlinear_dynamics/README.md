# CM-24 — Nonlinear Dynamics & Chaos

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~MA-22`
(dynamical systems), `~MA-07`. **Links:** `~CM-19` (phase space), `~CM-15`.

## Scope
The physics application of dynamical systems: **fixed points and their stability**
(via the Jacobian, reusing MA-22's classifier), **limit cycles** (the van der Pol
oscillator), and **chaos** with a positive Lyapunov exponent (the logistic map,
reusing MA-22).

## Operations — `code/nonlinear_dynamics.py`
| call | meaning | references |
|------|---------|-----------|
| `jacobian(f, point)` | 2×2 Jacobian of a planar flow | (MA-22 Chicone §1.6) |
| `classify_fixed_point(f, point)` | stability type (reuses MA-22) | MA-22 / Chicone §1.6 |
| `integrate_flow(f, p0, …)` | integrate dx/dt = f(x,y) (MA-07) | — |
| `pendulum_flow(gamma)`, `van_der_pol(mu)` | example flows | — |
| `lyapunov_logistic(r)` | logistic-map Lyapunov exponent (MA-22) | MA-22 |

## Use
```python
import math
from nonlinear_dynamics import classify_fixed_point, pendulum_flow, lyapunov_logistic
classify_fixed_point(pendulum_flow(0.5), (0,0))      # 'stable spiral' (damped pendulum bottom)
classify_fixed_point(pendulum_flow(0.0), (math.pi,0))# 'saddle' (inverted pendulum)
lyapunov_logistic(4.0)                                # ~ ln 2 (chaotic)
```

## Run
```bash
cd code
python3 nonlinear_dynamics.py        # demo (pendulum fixed points, van der Pol, logistic chaos)
python3 test_nonlinear_dynamics.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/nonlinear_dynamics.py` · `code/test_nonlinear_dynamics.py` · `problems/problems.md`
