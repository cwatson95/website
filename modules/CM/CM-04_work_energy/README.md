# CM-04 — Work & Energy

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-01`,
`~MA-02` (the work integral IS a line integral), `~MA-01`. **Feeds:** `~CM-05`
(potential energy), `~CM-08` (collision energetics).

## Scope
Kinetic energy T = ½m|v|², the **work integral** W = ∫F·dl (reusing MA-02's
`line_integral`), and the **work–energy theorem** W = ΔT.

## Operations — `code/work_energy.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `kinetic_energy(m, v)` | T = ½ m (v·v) | Fowles §2.3 p.63 |
| `work(force_field, path, a, b)` | W = ∫ F·dl (= MA-02 line integral) | Fowles §4.1 p.145 |
| `power(F, v)` | P = F·v | Fowles §4.1 p.145 |

A force field is `F(x,y,z) -> (Fx,Fy,Fz)`; a path is `gamma(t) -> (x,y,z)`.

## Use
```python
from work_energy import kinetic_energy, work
kinetic_energy(2.0, (3,0,4))                       # 25
work(lambda x,y,z:(0,0,-9.81*3), lambda s:(0,0,4*(1-s)), 0, 1)   # m g h, lowering 3 kg by 4 m
```

## Run
```bash
cd code
python3 work_energy.py        # demo (T, work of a constant force, work-energy theorem)
python3 test_work_energy.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/work_energy.py` · `code/test_work_energy.py` · `problems/problems.md`
