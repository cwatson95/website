# MA-16 — Tensor Analysis & Index Notation

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-03` (curvilinear
coordinates), `~MA-04` (matrices/linear algebra). **Feeds:** `~RE-08` (tensors in
SR), `~EM-18` (the field tensor F^{μν}), `~CM-13` (the inertia tensor),
`~MA-17` (curvature). Network **bridge B5** (tensors → inertia → field tensor →
curvature).

## Scope
Index notation and the **Einstein summation convention**; **contravariant** vⁱ vs
**covariant** v_i components; the **metric tensor** g_ij that converts between
them and measures length; **raising/lowering** indices; and the two fundamental
symbols — the **Kronecker delta** δⁱ_j and the **Levi-Civita symbol** ε. The
headline facts: a vector's length g_ij vⁱvʲ is a **coordinate invariant**, and the
metric of any curvilinear system is g = JᵀJ from the coordinate map's Jacobian
(so polar → diag(1,r²), spherical → diag(1,r²,r²sin²θ)). Determinant and inverse
are built from ε, keeping everything inside index notation.

## Operations — `code/tensors.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `kronecker_delta(n)`, `levi_civita_symbol`, `levi_civita3` | δⁱ_j and ε | Boas §5 p.508 |
| `det_levi_civita`, `cofactor_matrix`, `inverse` | det/inverse via ε (Cramer) | Boas §5 p.508 |
| `metric_from_map(xmap, q)` | g_ij = JᵀJ from the coordinate map | Boas §8 p.521; §10 p.529 |
| `lower_index(g, v)`, `raise_index(g_inv, v)` | vᵢ=g_ij vʲ, vⁱ=gⁱʲvⱼ | Boas §10 p.529 |
| `inner(g, u, v)` | invariant g_ij uⁱvʲ | Boas §10 p.529 |
| `cross_via_levi_civita(a, b)` | (a×b)ⁱ=εⁱʲᵏaⱼbₖ | Boas §5 p.508 |
| `eps_delta_identity_holds()` | Σε_ijk ε_ilm = δ_jlδ_km−δ_jmδ_kl | Boas §5 p.508 |

## Use
```python
import math
from tensors import metric_from_map, inner, jacobian, matvec, cross_via_levi_civita

polar = lambda q: [q[0]*math.cos(q[1]), q[0]*math.sin(q[1])]
g = metric_from_map(polar, [2.0, 0.7])     # [[1,0],[0,4]]  -> ds^2 = dr^2 + r^2 dtheta^2
v = [0.3, 0.25]
inner(g, v, v) == sum(c*c for c in matvec(jacobian(polar,[2.0,0.7]), v))   # length invariant
cross_via_levi_civita([1,2,3], [4,5,6])    # [-3, 6, -3]
```

## Run
```bash
cd code
python3 tensors.py            # demo (metric from map, length invariance, raise/lower, eps)
python3 test_tensors.py       # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/tensors.py` · `code/test_tensors.py` · `problems/problems.md`
