# RE-05 — Minkowski Spacetime

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). Special
relativity recast as the geometry of a 4-D space with one minus sign in its
metric — the home of 4-vectors, the invariant interval, and the light cone.

- **Prerequisites:** `RE-03` (Lorentz transformations); **`~MA-16`** (tensor
  analysis — the metric, raising/lowering indices, the inner product). This is
  the dependency flagged in the topic network: RE-05 *uses* MA-16's code.
- **Feeds into:** `~RE-06` (4-momentum & dynamics), `~RE-08` (covariant
  formulation), `~RE-09`/`~RE-11` (the curved-spacetime generalisation),
  `~QM-22` (relativistic quantum mechanics).

## Scope
The Minkowski metric η = diag(−1,+1,+1,+1); the invariant interval s² and the
timelike / null / spacelike trichotomy; the **light cone** as the causal
structure (future / past / elsewhere); **proper time** as Minkowski arc length
and the reversed triangle inequality (twin paradox); the standard 4-vectors
(position, velocity, momentum) and their invariants (`U·U = −1`, `p·p = −m²`).

## Built on MA-16
The index gymnastics are **not reimplemented** — they are MA-16's. With η as the
metric `g`:
```python
import tensors                       # MA-16, imported by relative path
mdot(u, v)  = tensors.inner(ETA, u, v)          # u·v = η_{μν}u^μ v^ν
lower(v)    = tensors.lower_index(ETA, v)        # v_μ = η_{μν} v^ν
raise_(vlo) = tensors.raise_index(ETA, vlo)      # v^μ = η^{μν} v_ν
```
Minkowski space **is** MA-16's machinery with an indefinite metric instead of a
positive-definite one. (η is its own inverse, so `ETA_INV = ETA`.)

## Operations — `code/minkowski.py`
| call | meaning |
|------|---------|
| `mdot(u,v)`, `interval2(x)`, `classify(x)` | η-inner product, s²=x·x, time/null/space |
| `lower(v)`, `raise_(v)` | index lowering/raising with η (MA-16) |
| `causal_relation(a,b)`, `is_future_pointing(x)` | future / past / elsewhere |
| `proper_time(events)` | Minkowski arc length Σ√(−s²) along a timelike worldline |
| `four_velocity(v)`, `three_velocity(U)` | U = γ(1,**v**), U·U=−1 |
| `four_momentum(m,v)`, `invariant_mass(p)` | p = mU, m = √(−p·p) (mass shell) |

## Use
```python
from minkowski import interval2, classify, proper_time, four_momentum, invariant_mass

classify([1, 1, 0, 0])                       # 'null'  (a photon)
interval2([3, 1, 0, 0])                      # -8.0    (timelike)
proper_time([[0,0,0,0],[10,0,0,0]])          # 10.0  (inertial: maximal aging)
proper_time([[0,0,0,0],[5,4,0,0],[10,0,0,0]])# 6.0   (out-and-back twin: younger)
invariant_mass(four_momentum(2.0, [0.6,0,0]))# 2.0   (frame-independent)
```

## Run
```bash
cd code
python3 minkowski.py            # demo: light cone, twin paradox, mass shell
python3 test_minkowski.py       # 9 tests -> "All 9 tests passed."
```
*(The module adds `../../../MA/MA-16_tensor_analysis/code` to `sys.path`, so run
it in place; no install needed.)*

## Files
- `notes.md` — the metric, interval, light cone, proper time, 4-vectors
- `code/minkowski.py` — the library (imports MA-16; pure stdlib otherwise)
- `code/test_minkowski.py` — invariance under boosts, causal structure, twin paradox
- `problems/problems.md` — worked problems (Griffiths Ch.12, Zee III.3)
- `refs.md` — verified textbook citations
