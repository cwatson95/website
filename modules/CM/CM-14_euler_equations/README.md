# CM-14 — Euler's Equations

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-13`
(principal moments), `~MA-07`. **Links:** `~CM-09` (angular momentum).

## Scope
**Euler's equations** for rigid-body rotation in the principal-axis body frame,
their torque-free conservation laws (|L| and rotational energy), and the
free-precession of a symmetric top.

## Operations — `code/euler_equations.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `euler_rhs(I, torque)` | RHS of Euler's equations | Fowles §9.3 p.381 |
| `integrate_euler(I, omega0, …)` | integrate the body-frame ω(t) | Fowles §9.4 p.383 |
| `precession_rate(I_perp, I_sym, omega3)` | (I₃−I₁)/I₁ · ω₃ | Fowles §9.5 p.384 |
| `L_magnitude_sq`, `rotational_energy` | conserved quantities (torque-free) | Fowles §9.4 p.383 |

I = (I₁, I₂, I₃) are the principal moments from `~CM-13`.

## Use
```python
from euler_equations import integrate_euler, precession_rate
ts, ws = integrate_euler((1,2,3), (1,1,1), 0, 5, 5000)   # torque-free; |L|, T conserved
precession_rate(1.0, 2.0, 3.0)                            # symmetric-top precession rate
```

## Run
```bash
cd code
python3 euler_equations.py        # demo (conservation, symmetric top, steady spin)
python3 test_euler_equations.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/euler_equations.py` · `code/test_euler_equations.py` · `problems/problems.md`
