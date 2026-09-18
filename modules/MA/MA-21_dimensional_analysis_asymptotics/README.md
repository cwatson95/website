# MA-21 — Dimensional Analysis & Asymptotics

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-04` (null spaces),
`~MA-01` (series). **Feeds:** `~QM-15` (perturbation theory & WKB), `~CM-23`/`~PK-03`
(Reynolds/Knudsen scaling), and order-of-magnitude estimation everywhere.

## Scope
Two complementary "without solving it exactly" tools. **Dimensional analysis**:
the Buckingham Pi theorem builds the dimensionless groups of a problem as the
**null space of the dimension matrix** (so a pendulum's period must be √(L/g) on
dimensional grounds alone). **Asymptotics**: divergent **asymptotic series** and
their *optimal truncation* (the error shrinks to ~the smallest term near N≈x, then
diverges), **Stirling's** approximation, and **regular perturbation** series.

## Operations — `code/asymptotics.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `nullspace(M)` | basis of {x : Mx=0} (RREF) | — (cf. `~MA-04`) |
| `buckingham_pi(dim_matrix)` | dimensionless groups = null space | standard method (see refs) |
| `is_dimensionless(dim_matrix, exps)` | net dimension = 0 check | standard method |
| `exp_integral_scaled_true/_asymptotic` | g(x)=x eˣE₁(x): exact vs series | Boas §10 p.549 |
| `optimal_truncation(x)` | best N (~x) and its error | Boas §10 p.549 |
| `ln_factorial_stirling(n, terms)` | n ln n − n + ½ln(2πn) + … | Boas §11 p.552 |
| `perturbed_root(eps, order)` | root of x²+εx−1=0 as a series | Boas §10 p.549 (asymptotic/perturbative) |

## Use
```python
from asymptotics import buckingham_pi, is_dimensionless, optimal_truncation, ln_factorial_stirling
import math

# pendulum {T_period, L, g, m} over (M,L,T):
D = [[0,0,0,1],[0,1,1,0],[1,0,-2,0]]
g = buckingham_pi(D)               # one group, exponents ~ (2,-1,1,0) = g T^2 / L
is_dimensionless(D, g[0])          # True

optimal_truncation(8.0)[0]         # best truncation N ~ 8 (= x)
ln_factorial_stirling(100, 3) - math.lgamma(101)   # ~ 1e-9
```

## Run
```bash
cd code
python3 asymptotics.py            # demo (Pi groups, optimal truncation, Stirling, perturbation)
python3 test_asymptotics.py       # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/asymptotics.py` · `code/test_asymptotics.py` · `problems/problems.md`
