# MA-14 — Green's Functions

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-15` (the delta
source), `~MA-07`/`~MA-08` (ODE/PDE boundary-value problems), `~MA-11`
(eigenfunction expansions). **Feeds:** `~EM-17` (retarded potentials &
Liénard–Wiechert), `~QM-19` (the propagator / Feynman path integral), and the
transient response of `~MA-10`.

## Scope
The Green's function is the **inverse of a differential operator**: G solves
L_x G(x,ξ)=δ(x−ξ), and then the solution of L u = f is just
u(x)=∫G(x,ξ)f(ξ)dξ — superpose the response to a unit point source. Three views:
the closed-form **two-solution construction** for a boundary-value problem, the
**eigenfunction (spectral) expansion** G=Σφ_n(x)φ_n(ξ)/λ_n, and the **causal
propagator** for an initial-value problem. Each is cross-checked against a direct
finite-difference solve or RK4.

## Operations — `code/greens_function.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `green_dirichlet(x, xi)` | G for −u″ on [0,1], = x_<(1−x_>) | Boas §12 p.461 |
| `green_helmholtz(x, xi, k)` | G for −u″+k²u (two-solution build) | Boas §12 p.461 |
| `solve_bvp_greens(f, xs, k)` | u(x)=∫G f dξ | Boas §12 p.461; Ch.13 p.657 |
| `solve_bvp_direct(f, N, k)` | independent finite-difference solve | — |
| `green_series(x, xi, nmax)` | spectral sum Σ φₙφₙ/λₙ | Boas Ch.13 §22 p.657 |
| `causal_green_oscillator(t, tau, omega)` | propagator sin ω(t−τ)/ω · H(t−τ) | Boas §12 p.461 |
| `solve_oscillator_greens(f, t, omega)` | y(t)=∫₀ᵗ G f dτ vs `rk4_oscillator` | Boas §12 p.461 |

## Use
```python
import math
from greens_function import solve_bvp_greens, solve_bvp_direct, green_series, green_dirichlet

# -u'' = sin(pi x), u(0)=u(1)=0  ->  exact u = sin(pi x)/pi^2
solve_bvp_greens(lambda x: math.sin(math.pi*x), [0.25, 0.5, 0.75])

# the spectral sum converges to the closed-form tent:
green_series(0.3, 0.7, 2000), green_dirichlet(0.3, 0.7)     # both 0.09
```

## Run
```bash
cd code
python3 greens_function.py        # demo (BVP vs exact/FD, spectral series, propagator vs RK4)
python3 test_greens_function.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/greens_function.py` · `code/test_greens_function.py` · `problems/problems.md`
