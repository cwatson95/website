# CM-18 — Symmetries & Noether's Theorem

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-17`.
**Links:** `~MA-18` (groups), `~CM-06`/`~CM-09` (the conservation laws), `~QF-03`
(gauge symmetry).

## Scope
The link between **continuous symmetries** of the Lagrangian and **conserved
quantities**: translation → momentum, rotation → angular momentum, time-translation
→ energy. Reuses CM-17's machinery.

## Operations — `code/noether.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `noether_charge(L, f, t, q, qdot)` | Q = (∂L/∂q̇) f(q), conserved for δq = εf | Goldstein §2.6 p.54 |
| `symmetry_defect(L, f, …)` | first-order change in L under the flow (~0 ⇒ symmetry) | Goldstein §2.6 p.54 |
| `energy(L, t, q, qdot)` | Jacobi energy; conserved if ∂L/∂t = 0 | Goldstein §2.6 p.54 |

## Use
```python
from noether import noether_charge, symmetry_defect, energy, integrate_eom
free = lambda t,q,p: 0.5*p*p                       # free particle
symmetry_defect(free, lambda q: 1.0, 0, 1, 2)      # ~0  (translation is a symmetry)
# noether_charge(free, lambda q:1.0, ...) = momentum, conserved
```

## Run
```bash
cd code
python3 noether.py        # demo (translation->momentum, time->energy)
python3 test_noether.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/noether.py` · `code/test_noether.py` · `problems/problems.md`
