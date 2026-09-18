# CM-06 — Linear Momentum

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-02`.
**Feeds:** `~CM-07` (centre of mass), `~CM-08` (collisions).

## Scope
Linear momentum **p** = m**v**, total momentum of a system, the **impulse**
**J** = ∫**F** dt (= Δ**p**), and **conservation** of total momentum (Newton's
third law). Pure stdlib.

## Operations — `code/linear_momentum.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `momentum(m, v)` | p = m v | Fowles §2.1 p.58 |
| `total_momentum(masses, vels)` | P = Σ mᵢ vᵢ | Fowles §7.1 p.277 |
| `impulse(force, t0, t1)` | J = ∫ F dt = Δp | Fowles §7.5 p.305 |

`force` is `force(t) -> (Fx, Fy, Fz)`.

## Use
```python
from linear_momentum import momentum, total_momentum, impulse
momentum(2.0, (3,0,-1))                         # [6,0,-2]
total_momentum([2,1], [[1,0,0],[-2,0,0]])       # [0,0,0]
impulse(lambda t:(3,0,0), 0, 2)                 # [6,0,0]  = F * dt
```

## Run
```bash
cd code
python3 linear_momentum.py        # demo (p, total P, impulse, third-law cancellation)
python3 test_linear_momentum.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/linear_momentum.py` · `code/test_linear_momentum.py` · `problems/problems.md`
