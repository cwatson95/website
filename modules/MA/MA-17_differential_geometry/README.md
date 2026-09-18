# MA-17 — Differential Geometry  [adv]

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-16` (tensors & the
metric), `~MA-02` (grad/curl/div), `~MA-03` (coordinates). **Feeds:** `~RE-09`
(tensor calculus on manifolds), `~RE-11`/`~RE-13` (curvature & the Einstein
equations), `~MA-18` (Lie groups are manifolds). Network **bridge B5**.

## Scope
Two pillars of geometry on curved spaces. **Differential forms & the exterior
derivative**: in R³, d acting on a 0/1/2-form *is* grad/curl/div, and the single
identity **d² = 0** is exactly curl(grad)=0 and div(curl)=0. **Riemannian
curvature**: Christoffel symbols → the Riemann tensor → Ricci → scalar/Gaussian
curvature, computed **from the metric alone**. The showcase is Gauss's *Theorema
Egregium*: the 2-sphere has K=1/a² and the (polar) plane has K=0, intrinsic facts
no choice of coordinates can change.

## Operations — `code/diffgeo.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `gradient`, `curl`, `divergence` | d on a 0/1/2-form in R³ | Warner §2 p.56; de Rham §4 p.15 |
| (d²=0) `curl(gradient(f))`, `divergence(curl(V))` | the exterior derivative is nilpotent | Warner *exterior derivative* p.65; de Rham p.17 |
| `christoffel(metric, x)` | Γᵏ_ij = ½gᵏˡ(∂ᵢg_jl+∂ⱼg_il−∂ₗg_ij) | Boas §10 p.529 (metric); `~RE-09` |
| `riemann`, `ricci`, `ricci_scalar` | curvature tensors from the metric | `~RE-11` |
| `gaussian_curvature_2d(metric, x)` | K = R/2 (Theorema Egregium) | `~RE-11` |
| `sphere_metric(a)`, `plane_polar_metric()` | test metrics (K=1/a², K=0) | — |

## Use
```python
import math
from diffgeo import gradient, curl, divergence, gaussian_curvature_2d, sphere_metric, plane_polar_metric

curl(gradient(lambda x: x[0]*x[1]*x[2]))([0.6,-0.4,0.9])   # ~ [0,0,0]  (d^2 = 0)
gaussian_curvature_2d(sphere_metric(2.0), [1.0, 0.3])      # ~ 0.25  = 1/a^2
gaussian_curvature_2d(plane_polar_metric(), [1.5, 0.0])    # ~ 0  (flat)
```

## Run
```bash
cd code
python3 diffgeo.py            # demo (d^2=0; curvature of sphere vs plane)
python3 test_diffgeo.py       # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/diffgeo.py` · `code/test_diffgeo.py` · `problems/problems.md`
