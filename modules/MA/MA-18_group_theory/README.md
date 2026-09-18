# MA-18 — Group Theory & Symmetry

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-04` (matrices —
representations are matrices). **Feeds:** `~CM-18` (Noether: symmetry →
conservation), `~QF-03` (gauge groups), `~QM-10`/`~QM-11` (rotation group →
angular momentum & spin). Network **bridge B8**.

## Scope
**Finite groups** — cyclic Zₙ, dihedral Dₙ, symmetric Sₙ — defined by their
elements and operation, with the axioms, element orders, and **Lagrange's theorem**
read straight off the Cayley table; **representations** (a homomorphism G →
matrices); and the two **Lie algebras** that run physics: **so(3)** (rotations →
angular momentum) and **su(2)** (the Pauli matrices → spin-½). The recurring
theorem is that representations turn abstract group elements into matrices you can
multiply, and that the *infinitesimal* structure is a commutator algebra.

## Operations — `code/groups.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `FiniteGroup(elements, op)` | axioms, identity, inverses, abelian? | standard (see refs) |
| `cyclic_group(n)`, `symmetric_group(n)`, `dihedral_group(n)` | Zₙ, Sₙ, Dₙ | standard (see refs) |
| `.element_order`, `.subgroup_orders` | orders; Lagrange (divides \|G\|) | standard |
| `cyclic_rep(n)`, `rotation_matrix` | Zₙ → SO(2) representation | Warner §3 p.82 |
| `so3_generators()`, `commutator` | so(3): [Lᵢ,Lⱼ]=εᵢⱼₖLₖ | Warner §3.29 p.102 |
| `pauli()` | su(2): [σᵢ,σⱼ]=2iεᵢⱼₖσₖ | Warner §3 p.85 |

## Use
```python
from groups import cyclic_group, symmetric_group, dihedral_group, so3_generators, commutator, pauli, scalar, matmul

symmetric_group(3).is_abelian()          # False -- smallest non-abelian group
dihedral_group(3).elements == ...        # D_3 = S_3 (6 symmetries of a triangle)
Lx, Ly, Lz = so3_generators()
commutator(Lx, Ly) == Lz                 # the rotation Lie algebra closes
sx, sy, sz = pauli()
commutator(sx, sy) == scalar(2j, sz)     # [sigma_x, sigma_y] = 2 i sigma_z
```

## Run
```bash
cd code
python3 groups.py             # demo (Z_6/S_3/D_3, Lagrange, reps, so(3) & su(2))
python3 test_groups.py        # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/groups.py` · `code/test_groups.py` · `problems/problems.md`
