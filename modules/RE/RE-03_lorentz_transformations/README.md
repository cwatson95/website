# RE-03 — Lorentz Transformations

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The
computational core of special relativity: how coordinates, velocities and the
metric transform between inertial frames.

- **Prerequisites:** `RE-02` (postulates of SR). Soft: `~CM-03` (inertial /
  Galilean frames — the c→∞ limit recovered here).
- **Feeds into:** `~RE-04` (time dilation & length contraction are corollaries of
  one boost), `~RE-05` (Minkowski 4-vectors & the interval), `~RE-07`
  (Doppler & aberration), `~RE-08` (covariant formulation).

## Scope
The Lorentz boost as the linear map that keeps the speed of light invariant; the
**rapidity** φ = artanh β that turns a boost into a hyperbolic rotation; Einstein
**velocity addition** as rapidity addition; and the **Lorentz group** structure
(closure, inverse, proper/orthochronous subgroup, parity & time reversal).

## Conventions (whole RE trunk)
- Natural units **c = 1**; an event is `x = (ct, x, y, z)` (time component `x⁰=ct`).
- `β = v/c`, `γ = 1/√(1−β²)`.
- Metric **η = diag(−1,+1,+1,+1)** (mostly-plus, GR/Zee/MTW). Interval
  `s² = −(ct)² + x² + y² + z²`; timelike `s²<0`, null `s²=0`, spacelike `s²>0`.
- A boost acts as `x' = Λx`, the **active** boost to a frame moving at +β:
  `x' = γ(x − βct)`, `ct' = γ(ct − βx)`.

## The one idea
A boost along an axis is a **hyperbolic rotation by the rapidity** φ = artanh β
(so γ = cosh φ, γβ = sinh φ). Collinear boosts therefore *add their rapidities*,
and that single fact **is** Einstein's velocity-addition rule:

```
boost(b₁) · boost(b₂) = boost( (b₁+b₂)/(1+b₁b₂) )   ⟺   artanh b₁ + artanh b₂ = artanh( (b₁+b₂)/(1+b₁b₂) )
```

Velocities don't add; rapidities do. `c` is the unreachable rapidity-infinity.

## Operations — `code/lorentz.py`
| call | meaning |
|------|---------|
| `gamma(beta)`, `rapidity(beta)`, `beta_from_rapidity(phi)` | γ, φ=artanh β, β=tanh φ |
| `boost(beta, axis=1)` | 4×4 boost along x/y/z (axis 1/2/3) |
| `general_boost((bx,by,bz))` | 4×4 boost for an arbitrary velocity 3-vector |
| `apply(L, event)`, `compose(*Ls)`, `inverse(L)` | act / multiply / invert |
| `dot4(a,b)`, `interval2(x)`, `classify(x)` | Minkowski product, s², time/null/space |
| `velocity_add(u,v)` | collinear (u⊕v)=(u+v)/(1+uv) |
| `velocity_add_3d(u,v')` | general (non-collinear) addition via 4-velocity |
| `four_velocity(v)`, `three_velocity(U)` | U=γ(1,**v**) ↔ **v**=U/U⁰ |
| `preserves_eta(L)`, `is_proper(L)`, `is_orthochronous(L)` | is L a (proper, orthochronous) Lorentz transf? |

## Use
```python
from lorentz import boost, compose, velocity_add, apply, interval2, preserves_eta

velocity_add(0.7, 0.7)                 # 0.9396…  (NOT 1.4 — capped at c=1)
preserves_eta(boost(0.6))              # True   (ΛᵀηΛ = η)
interval2(apply(boost(0.8), [2,0.5,0,0]))   # = interval2([2,0.5,0,0])  (invariant)
compose(boost(0.5), boost(0.5))        # == boost(velocity_add(0.5,0.5))
```

## Run
```bash
cd code
python3 lorentz.py            # demo: γ table, rapidity additivity, invariance
python3 test_lorentz.py       # 11 property-based tests -> "All 11 tests passed."
```

## Files
- `notes.md` — postulates→boost, rapidity, velocity addition, the group, η-invariance
- `code/lorentz.py` — the library (pure stdlib; 4-vectors are length-4 lists)
- `code/test_lorentz.py` — η-preservation, interval & light-cone invariance, rapidity additivity
- `problems/problems.md` — worked problems (Griffiths Ch.12, Zee III)
- `refs.md` — verified textbook citations
