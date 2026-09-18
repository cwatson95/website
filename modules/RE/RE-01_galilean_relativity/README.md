# RE-01 — Galilean Relativity & Its Failure

Root module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). Where
the pre-relativistic picture — absolute time, velocities that just add — works,
and the one place it breaks: light.

- **Prerequisites:** `~CM-03` (reference frames / Galilean boosts). This module
  *imports* CM-03 and RE-03.
- **Feeds into:** `RE-02` (the postulates that replace Galilean kinematics),
  `RE-03` (the Lorentz transformation — Galilean is its `c→∞` limit).

## Scope
The Galilean transformation `r' = r − Vt`, `t' = t`; its invariance for Newton's
laws (acceleration, hence `F=ma`, is unchanged) but **not** for Maxwell's
equations (which carry a fixed `c`); the consequent ether hypothesis; and the
**Michelson–Morley** experiment, whose predicted ~0.4-fringe shift was never
seen — the empirical death of Galilean relativity for light.

## The one idea
Velocities adding as `u+v` is exactly right for mechanics and exactly wrong for
light. Maxwell's `c = 1/√(ε₀μ₀)` names no frame, so Galilean addition would make
light travel at `c−v` in a moving frame; Michelson–Morley looked for that `v` and
found nothing. The fix isn't a patch — it's new kinematics: the Galilean
transformation is the **`c→∞` limit** of the Lorentz transformation (RE-03), and
Einstein's velocity rule `(u+v)/(1+uv/c²)` reduces to `u+v` in the same limit.

## Operations — `code/galilean.py` (c is explicit)
| call | meaning |
|------|---------|
| `galilean_position(r,V,t)`, `galilean_velocity(v,V)` | the Galilean boost (from CM-03) |
| `galilean_velocity_add(u,v)` = `u+v` | the rule that fails for light |
| `relativistic_velocity_add(u,v,c)` | Einstein's rule (from RE-03), `→ u+v` as `c→∞` |
| `galilean_limit_error(u,v,c)` | `|relativistic − Galilean|`, `∝1/c²` |
| `galilean_invariant_acceleration`, `light_speed_galilean` | Newton invariant; light isn't (`c+v≠c`) |
| `michelson_morley_shift(v,L,λ,c)` | predicted fringe shift `(2L/λ)(v/c)²` |
| `ether_wind_dt(v,L,c)` | exact parallel-vs-perpendicular arm time difference |

## Use
```python
from galilean import galilean_velocity_add, relativistic_velocity_add, michelson_morley_shift, C_LIGHT
c = C_LIGHT
galilean_velocity_add(0.7*c, 0.7*c) / c      # 1.4   (overshoots c!)
relativistic_velocity_add(0.7*c, 0.7*c, c)/c # 0.9396 (Einstein: capped at c)
michelson_morley_shift(30e3, 11.0, 500e-9)   # 0.44 fringes predicted; ~0 observed
```

## Run
```bash
cd code
python3 galilean.py          # demo: u+v vs Einstein, the c→∞ limit, Michelson–Morley
python3 test_galilean.py     # 8 tests -> "All 8 tests passed."
```
*(Adds CM-03 and RE-03 `code/` dirs to `sys.path`; run in place.)*

## Files
- `notes.md` — Galilean transformation, Newton vs Maxwell, the ether, Michelson–Morley, the resolution
- `code/galilean.py` — the library (imports CM-03 + RE-03)
- `code/test_galilean.py` — Galilean=limit of Einstein, c-respecting, the MM shift
- `problems/problems.md` — worked problems (Griffiths Ch.12, Zee III.1)
- `refs.md` — verified citations
