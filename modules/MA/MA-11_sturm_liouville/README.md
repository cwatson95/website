# MA-11 — Sturm–Liouville Theory

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-04` (matrix
eigenproblem), `~MA-07` (ODEs), `~MA-08` (separation of variables).
**Feeds:** `~MA-12` (Legendre/Bessel/Hermite/Laguerre are SL eigenfunctions),
`~MA-14` (Green's function = Σ eigenfunctions / λₙ), `~QM-05` (observables as
self-adjoint operators; eigenfunctions as a basis).

## Scope
The self-adjoint eigenvalue problem **−(p y′)′ + q y = λ w y** on [a,b] with
homogeneous boundary conditions: its **real, ordered eigenvalues**, its
**w-orthogonal eigenfunctions**, their **completeness** (any function expands in
them — the abstraction of Fourier series), and the **Rayleigh quotient**
variational bound λ_min ≤ R[y]. The operator is finite-differenced to a symmetric
tridiagonal matrix; eigenvalues come from a **Sturm sequence** — the object the
theory is named after — and bisection.

## Operations — `code/sturm_liouville.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `sl_tridiagonal(p,q,w,a,b,N)` | finite-difference −(p y′)′+q y = λ w y | Boas §6 p.575 |
| `sturm_count(d,e,mu)` | # eigenvalues below μ (Sturm sequence) | Boas Ch.12 misc. p.617 |
| `tridiag_eigenvalues(d,e)` | eigenvalues by Sturm bisection | Boas §6 p.575 |
| `tridiag_eigenvector(d,e,lam)` | eigenvector by inverse iteration | — |
| `sl_eigenpairs(p,q,w,a,b,N,k)` | lowest k SL eigenpairs (weight scaled) | Boas §6–9 pp.575–582 |
| `inner_w(f,g,w,h)` | weighted inner product ∫ f g w dx | Boas §7 p.577 |
| `rayleigh_quotient(p,q,w,y,a,b)` | R[y] ≥ λ_min variational bound | Boas §6 p.575 |
| `expand` / `reconstruct` | eigenfunction expansion (completeness) | Boas §9 p.580 |

## Use
```python
import math
from sturm_liouville import sl_eigenpairs, rayleigh_quotient

# -y'' = lambda y on [0, pi], Dirichlet  ->  eigenvalues n^2, eigenfunctions sin(n x)
lams, ys, xs, w, h = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, math.pi, 200, 5)
lams            # ~ [1, 4, 9, 16, 25]

trial = [x*(math.pi - x) for x in xs]
rayleigh_quotient(1.0, 0.0, 1.0, trial, 0.0, math.pi)   # 10/pi^2 ~ 1.013 >= lam_min
```

## Run
```bash
cd code
python3 sturm_liouville.py        # demo (eigenvalues -> n^2, sines, Rayleigh, Parseval)
python3 test_sturm_liouville.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/sturm_liouville.py` · `code/test_sturm_liouville.py` · `problems/problems.md`
