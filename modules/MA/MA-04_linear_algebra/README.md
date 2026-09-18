# MA-04 — Linear Algebra

Math trunk (see `modules/topic_network.txt`). **Prereq:** none (root; pairs with `~MA-01`).
**Feeds:** `~CM-13` (inertia tensor → principal axes), `~CM-16` (normal modes),
`~QM-05`/`~QM-06` (observables as Hermitian operators; diagonalization).

## Scope
Matrix operations; determinant, linear solve and inverse by Gaussian elimination
(Boas: "row reduction"); and the **eigenvalue problem** for real symmetric
matrices solved from scratch with **Jacobi rotations** — the algorithm behind
principal axes and the diagonalization of observables. Pure Python; for large or
general/complex problems use `numpy.linalg`.

## Operations — `code/linalg.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `matmul`, `matvec`, `transpose`, `trace`, `identity` | matrix algebra | Boas §6 p.114 |
| `det` | determinant (partial-pivot elimination) | Boas §3 p.89 |
| `solve`, `inverse` | A x = b, A⁻¹ (row reduction) | Boas §2 p.83; §3 p.89 |
| `is_symmetric` | symmetry test | Boas §11 p.148 |
| `eig_symmetric` | eigenvalues & orthonormal eigenvectors (Jacobi) | Boas §11 p.148 |
| `reconstruct` | rebuild A = Q Λ Qᵀ | Boas §11 p.148; §12 p.162 |
| `eigvals_2x2` | 2×2 eigenvalues (may be complex) | Boas §11 p.148 |

Matrices are lists of rows; vectors are lists/tuples.

## Use
```python
from linalg import solve, inverse, eig_symmetric, reconstruct

solve([[4,3],[6,3]], [10,12])          # x with A x = b
inverse([[4,3],[6,3]])

S = [[2,1,0],[1,2,1],[0,1,2]]          # symmetric
vals, vecs = eig_symmetric(S)          # vals sorted; vecs = orthonormal columns
# A v = lambda v for each pair; reconstruct(vals, vecs) == S
```

## Run
```bash
cd code
python3 linalg.py            # demo (solve, invert, Jacobi eigen, complex 2x2)
python3 test_linalg.py       # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/linalg.py` · `code/test_linalg.py` · `problems/problems.md`
