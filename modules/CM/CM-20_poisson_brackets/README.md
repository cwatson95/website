# CM-20 — Poisson Brackets & Canonical Transformations

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereq:** `~CM-19`.
**Links:** `~QM-05` (the {,} → (1/iℏ)[,] bridge to commutators), `~MA-22`
(Liouville / phase-space flow).

## Scope
The Poisson bracket {f, g}, the fundamental bracket {q, p} = 1, the equation of
motion df/dt = {f, H}, and the test for a **canonical transformation** ({Q, P} = 1).

## Operations — `code/poisson_brackets.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `poisson_bracket(f, g, q, p)` | {f,g} = ∂_q f ∂_p g − ∂_p f ∂_q g | Goldstein §9.5 p.388 |
| `time_derivative(f, H, q, p)` | df/dt = {f, H} | Goldstein §9.6 p.396 |
| `is_canonical(Q, P, q, p)` | {Q, P} = 1 ? | Goldstein §9.5 p.388 |

f, g, Q, P are functions of (q, p).

## Use
```python
from poisson_brackets import poisson_bracket, time_derivative, is_canonical
poisson_bracket(lambda q,p:q, lambda q,p:p, 1.3, 0.7)            # 1   ({q,p}=1)
time_derivative(lambda q,p:q, lambda q,p:0.5*p*p+q*q, 1, 0.5)    # qdot = p
is_canonical(lambda q,p:p, lambda q,p:-q, 1, 1)                  # True
```

## Run
```bash
cd code
python3 poisson_brackets.py        # demo (fundamental brackets, EOM, canonical tests)
python3 test_poisson_brackets.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/poisson_brackets.py` · `code/test_poisson_brackets.py` · `problems/problems.md`
