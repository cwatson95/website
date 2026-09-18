# RE-08 — Covariant Formulation of Special Relativity

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The index
machinery — 4-tensors and their Lorentz transformation laws — that turns "the
interval is invariant" into a working language: *a tensor equation true in one
inertial frame is true in all of them.*

- **Prerequisites:** `RE-03` (Lorentz transformations — supplies the boosts Λ),
  `RE-05` (Minkowski spacetime — the metric η and the invariant interval);
  **`~MA-16`** (tensor analysis — the inner product, raising/lowering indices,
  the Kronecker δ). MA-16 and RE-03 are the dependencies flagged in the topic
  network: RE-08 *uses* their code, it does not re-derive it.
- **Feeds into:** `~EM-18` (the field tensor `F^{μν}` and covariant Maxwell —
  the headline downstream application), `~RE-09`/`~RE-11` (the curved-spacetime
  generalisation, where η becomes a position-dependent `g_{μν}(x)`).

## Scope
The transformation laws by rank — scalar (invariant), contravariant `V^μ`,
covariant `V_μ` (the inverse-transpose law), rank-2 `T^{μν}`; raising/lowering
with η; **Lorentz invariants** from full contraction (`V^μV_μ`, the trace
`T^μ_μ`, `S_{μν}T^{μν}`); the symmetric/antisymmetric split and its invariance
under boosts; the **invariant tensors** η, `δ^μ_ν`; the naturally **covariant**
4-gradient `∂_μ` and the scalar **d'Alembertian** `□ = ∂^μ∂_μ = −∂_t² + ∇²`.

## Built on MA-16 and RE-03
The index gymnastics are MA-16's; the boosts Λ are RE-03's. Neither is
reimplemented:
```python
import tensors    # MA-16, by relative path
import lorentz    # RE-03, by relative path
mdot(u, v)              = tensors.inner(ETA, u, v)       # u·v = η_{μν}u^μ v^ν
lower(V)               = tensors.lower_index(ETA, V)     # V_μ = η_{μν} V^ν
transform_covector(L,W) uses lorentz.inverse(L) = η Λᵀ η # the inverse-transpose law
```

## Operations — `code/covariant_sr.py`
| call | meaning |
|------|---------|
| `transform_vector(L, V)` | contravariant `V'^μ = Λ^μ_ν V^ν` (= `lorentz.apply`) |
| `transform_covector(L, V)` | covariant `V'_μ = (Λ⁻¹)^ν_μ V_ν` (inverse-transpose) |
| `transform_tensor2(L, T)` | rank-2 `T'^{μν} = Λ^μ_α Λ^ν_β T^{αβ}` |
| `lower(V)`, `raise_(V)` | index lowering/raising with η (MA-16) |
| `mdot(u,v)`, `double_contract(S,T)` | invariants `u^μv_μ`, `S_{μν}T^{μν}` |
| `trace(T)` | invariant trace `T^μ_μ = η_{μν}T^{μν}` |
| `symmetric_part(T)`, `antisymmetric_part(T)` | `½(T ± Tᵀ)` |
| `four_gradient(f, x)` | covariant `∂_μ f` (numerical, index down) |
| `dalembertian(f, x)` | scalar `□f = −∂_t²f + ∇²f` (numerical) |

## Use
```python
from covariant_sr import (transform_vector, transform_covector, lower,
                          trace, transform_tensor2, ETA, four_gradient,
                          dalembertian, mdot)
import lorentz

L = lorentz.general_boost((0.3, -0.4, 0.5))
V, Wlo = [2,5,-1,3], lower([1,0,2,-2])
# V^μ W_μ is invariant — the inverse-transpose law at work:
sum(a*b for a,b in zip(transform_vector(L,V), transform_covector(L,Wlo)))  # = V·W

transform_tensor2(L, ETA)                 # == ETA  (η is an invariant tensor)
four_gradient(lambda x: mdot(x,x), [1,2,-1,0.5])    # = 2·lower(x)  (covariant)
dalembertian(lambda x: mdot(x,x), [1,2,-1,0.5])     # = 8.0  (a Lorentz scalar)
```

## Run
```bash
cd code
python3 covariant_sr.py         # demo: invariant contraction, η & δ, gradient, □
python3 test_covariant_sr.py    # 16 tests -> "All 16 tests passed."
```
*(The module adds `../../../MA/MA-16_tensor_analysis/code` and
`../../RE-03_lorentz_transformations/code` to `sys.path`, so run it in place; no
install needed.)*

## Files
- `notes.md` — transformation laws by rank, invariants, the covariant ∂_μ and □
- `code/covariant_sr.py` — the library (imports MA-16 + RE-03; pure stdlib otherwise)
- `code/test_covariant_sr.py` — invariance under real RE-03 boosts; η, δ, trace; the wave operator
- `problems/problems.md` — worked problems (Griffiths Ch.12, Zee I.4/III.3)
- `refs.md` — verified textbook citations
