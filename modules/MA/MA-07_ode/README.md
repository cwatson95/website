# MA-07 — Ordinary Differential Equations

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-04` (linear systems).
**Feeds:** `~CM-02` (Newton's 2nd law is an ODE), `~CM-15`/`~CM-16` (oscillations
& normal modes), `~QM-03` (Schrödinger equation).

## Scope
Numerical integrators — **Euler** and **RK4** — for scalar, vector and
second-order systems, plus the **exact** evolution of a linear system
dx/dt = A x by **diagonalization** (reusing `~MA-04`'s eigensolver). The analytic
solution families (separable, linear first-order, constant-coefficient second
order, forced) are documented with citations in `notes.md`.

## Operations — `code/ode.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `integrate(f, y0, t0, t1, n)` | solve dy/dt = f(t,y) (RK4 default) | (numerical method; theory below) |
| `euler_step`, `rk4_step` | one step of each scheme | — |
| `second_order_system(g)` | y″=g(t,y,y′) → first-order system | Boas §8.5 p.408 |
| `linear_rhs(A)` | RHS of dx/dt = A x | Boas §8.5 p.408 |
| `linear_evolve_symmetric(A, x0, t)` | exact e^{At}x0 for symmetric A (via MA-04) | Boas §8.5 p.408 |

State `y` is a list; a scalar ODE uses a length-1 list. `integrate` returns `(ts, ys)`.

## Use
```python
import math
from ode import integrate, second_order_system, linear_rhs, linear_evolve_symmetric

ts, ys = integrate(lambda t, y: [y[0]], [1.0], 0, 1, 1000)   # y'=y -> y(1)=e
f = second_order_system(lambda t, y, v: -y)                  # SHO  y''=-y
ts, ys = integrate(f, [1.0, 0.0], 0, 2*math.pi, 4000)        # -> cos t

A = [[0.0, 1.0], [1.0, 0.0]]
linear_evolve_symmetric(A, [1, 0], 0.7)                      # exact e^{At}x0 (= cosh,sinh)
```

## Run
```bash
cd code
python3 ode.py            # demo (exp, SHO, damped, linear system: eigen vs RK4)
python3 test_ode.py       # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/ode.py` · `code/test_ode.py` · `problems/problems.md`
