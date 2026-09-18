# MA-20 — Numerical Methods

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-04` (linear
algebra), `~MA-07` (ODEs), `~MA-02` (calculus). **Feeds:** `~PK-01` (Boltzmann/
kinetic solvers), every quadrature/ODE check in `~MA-10`…`~MA-14`, and `~CM-23` (CFD).

## Scope
The core toolkit, organized around the **order of accuracy**: **quadrature**
(trapezoid 2nd-order, Simpson 4th-order, Gauss–Legendre), **root finding**
(bisection, Newton, secant), **ODE integrators** (Euler 1st-order, RK4 4th-order),
the **power iteration** for a dominant eigenvalue, and **Lagrange interpolation**.
The unifying check: a method claiming order *p* must show error ∝ hᵖ, which the
code measures empirically by halving the step and reading the error ratio (→ 2ᵖ).

## Operations — `code/numerical.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `trapezoid`, `simpson` | composite Newton–Cotes quadrature | Schaum's p.109/231 |
| `gauss_legendre(f,a,b,n,panels)` | Gauss quadrature (exact deg 2n−1) | standard (see refs) |
| `quad_order(method,…)` | empirical convergence order | — |
| `bisection`, `newton`, `secant` | root finders | Schaum's (Newton) p.233 |
| `euler`, `rk4` | ODE integrators | Schaum's (RK4) p.236 |
| `ode_order(integrator,…)` | empirical ODE order | Chicone Ch.1 |
| `power_iteration(A)` | dominant eigenvalue/vector | standard (cf. `~MA-04`) |
| `lagrange_interp(xs,ys,x)` | interpolating polynomial | Schaum's p.227 |

## Use
```python
import math
from numerical import simpson, quad_order, newton, rk4, ode_order, power_iteration

simpson(math.exp, 0, 1, 100)                       # ~ e - 1
quad_order(simpson, math.exp, 0, 1, math.e - 1)    # ~ 4.0 (Simpson is 4th order)
newton(lambda x: x*x - 2, lambda x: 2*x, 1.0)[0]   # sqrt 2, quadratic convergence
ode_order(rk4, lambda t, y: y, 1.0, 1.0, math.e)   # ~ 4.0
```

## Run
```bash
cd code
python3 numerical.py          # demo (quadrature, roots, ODE orders, eigenvalue, interp)
python3 test_numerical.py     # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/numerical.py` · `code/test_numerical.py` · `problems/problems.md`
