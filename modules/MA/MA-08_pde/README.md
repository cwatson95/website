# MA-08 — Partial Differential Equations

Math trunk (see `modules/topic_network.txt`). **Prereqs:** `~MA-02` (the Laplacian),
`~MA-07` (time stepping). **Feeds:** `~MA-09` (separation → Fourier modes),
`~EM-04` (boundary-value problems), `~QM-03` (Schrödinger equation).

## Scope
The three classic linear PDEs solved by **finite differences**, each checkable
against its **separation-of-variables** (Fourier-mode) solution:
- **heat / diffusion** u_t = α u_xx (explicit FTCS),
- **wave** u_tt = c² u_xx (leapfrog),
- **Laplace** u_xx + u_yy = 0 (Gauss–Seidel relaxation).

## Operations — `code/pde.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `heat_1d(u0, alpha, dx, dt, n)` | diffuse a 1-D field | Boas §13.3 p.628 |
| `wave_1d(u0, v0, c, dx, dt, n)` | propagate a 1-D wave | Boas §13.4 p.633 |
| `laplace_2d(grid)` | solve ∇²u=0 (Dirichlet) | Boas §13.2 p.621; Griffiths §3.1 p.113 |
| `heat_mode(L, alpha, n)` | analytic mode sin(nπx/L)e^{−α(nπ/L)²t} | Griffiths §3.3 p.130 (separation of variables) |
| `wave_mode(L, c, n)` | standing wave sin(nπx/L)cos(cnπt/L) | Boas §13.4 p.633 |

## Use
```python
import math
from pde import heat_1d, laplace_2d, heat_mode

xs = [i/40 for i in range(41)]
u0 = [math.sin(math.pi*x) for x in xs]
uf = heat_1d(u0, 1.0, 1/40, 1e-4, 1000)        # matches heat_mode(1,1,1) at t=0.1

grid = [[0.0]*11 for _ in range(11)]            # set boundary, relax interior
sol, iters = laplace_2d(grid)
```

## Run
```bash
cd code
python3 pde.py            # demo (heat & wave vs separation-of-vars; Laplace on a square)
python3 test_pde.py       # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/pde.py` · `code/test_pde.py` · `problems/problems.md`
