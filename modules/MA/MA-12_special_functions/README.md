# MA-12 — Special Functions

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-07` (series
solutions of ODEs), `~MA-11` (Sturm–Liouville — these *are* its eigenfunctions).
**Feeds:** `~QM-09` (Hermite ↔ harmonic oscillator), `~QM-12` (Laguerre ↔
hydrogen radial, Legendre ↔ angular), `~QM-10` (Y_l^m ↔ angular momentum),
`~EM-05` (Legendre ↔ multipole expansion).

## Scope
The four families that solve the separated equations of physics: **Legendre** P_n
(and associated P_l^m → spherical harmonics), **Hermite** H_n, **Laguerre** L_n,
and **Bessel** J_n. For each: a stable recurrence to evaluate it, the weight that
makes it orthogonal, the ODE it satisfies, and (Legendre) its generating
function. Every evaluator is checked three independent ways — closed-form low
orders, the orthogonality integral, and the residual of its own ODE.

## Operations — `code/special_functions.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `legendre(n, x)`, `legendre_deriv` | P_n(x) by recurrence | Boas §2 p.564 |
| `assoc_legendre(l, m, x)` | P_l^m(x) → spherical harmonics | Boas §10 p.583; Ch.13 p.651 |
| `hermite(n, x)` | H_n(x), weight e^{−x²} | Boas §22 p.607 |
| `laguerre(n, x)` | L_n(x), weight e^{−x} | Boas §22 p.609 |
| `bessel_j(n, x)` | J_n(x) by integral representation | Boas §12 p.587 |
| `legendre_generating(x, t)` | Σ P_n tⁿ = 1/√(1−2xt+t²) | Boas §5 p.569 |
| `orthogonality_{legendre,hermite,laguerre}` | weighted ∫, gives δ_mn | Boas §7 p.577; §19 p.601 |
| `ode_residual(family, n, x)` | plug back into the defining ODE | Boas §2 p.564; §12 p.587 |

## Use
```python
from special_functions import legendre, hermite, laguerre, bessel_j, orthogonality_legendre

legendre(3, 0.4)              # = (5x^3 - 3x)/2
bessel_j(0, 1.0)             # ~ 0.765198  (matches tables)
orthogonality_legendre(2, 2) # ~ 2/(2*2+1) = 0.4
```

## Run
```bash
cd code
python3 special_functions.py        # demo (values, orthogonality, ODE residuals, gen. fn.)
python3 test_special_functions.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/special_functions.py` · `code/test_special_functions.py` · `problems/problems.md`
