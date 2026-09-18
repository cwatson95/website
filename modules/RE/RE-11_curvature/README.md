# RE-11 — Curvature

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The
intrinsic curvature of spacetime: the Riemann tensor and its contractions, and
the physical signature of curvature — geodesic deviation (tidal forces).

- **Prerequisites:** `RE-09` (tensor calculus on manifolds); **`~MA-17`**
  (differential geometry — Riemann/Ricci). This module *imports* MA-17.
- **Feeds into:** `~RE-12` (geodesics), `~RE-13` (Einstein field equations — the
  Einstein tensor built here is their LHS), `~RE-14` (Schwarzschild — verified
  vacuum here), `~RE-16` (gravitational waves). It is the **curvature toolkit**
  the later GR modules import.

## Scope
The Riemann tensor `R^ρ_σμν` as the irreducible gravitational field (the part of
the connection that *cannot* be transformed away); its contractions — Ricci
`R_μν`, scalar `R`, and the **Einstein tensor** `G_μν = R_μν − ½R g_μν`; the
coordinate-invariant **Kretschmann scalar** `K = R_μνρσR^μνρσ`; and **geodesic
deviation**, `D²ξ/dτ² = −R(u,ξ,u)`, which makes tidal forces literally equal to
the Riemann tensor.

## The one idea
The connection `Γ` (RE-09) vanishes at any point in a freely-falling frame (the
equivalence principle, RE-10) — so `Γ` is **not** the gravitational field. Its
*derivative*, the Riemann tensor, cannot be removed: `R = 0` everywhere ⇔ flat ⇔
gravity is a coordinate artefact. Curvature shows up physically as the **relative
acceleration of neighbouring free-fallers** — tidal forces *are* `R^a_{bcd}`.

## Operations — `code/curvature.py` (G = c = 1; metric is a callable `x→g`)
| call | meaning |
|------|---------|
| `riemann/ricci/ricci_scalar` | re-exported from MA-17 (`R^ρ_σμν`, `R_μν`, `R`) |
| `einstein_tensor(metric,x)` | `G_μν = R_μν − ½R g_μν` — LHS of the field equations |
| `kretschmann(metric,x)` | `K = R_μνρσR^μνρσ` (Schwarzschild: `48M²/r⁶`) |
| `geodesic_deviation(metric,x,u,xi)` | tidal 4-accel `−R^a_{bcd}u^b ξ^c u^d` |
| `gaussian_curvature_2d` | `K = R/2` for a 2-surface |
| `minkowski_metric()`, `schwarzschild_metric(M)`, `sphere_metric(a)` | reference metrics |

## Use
```python
from curvature import schwarzschild_metric, ricci, kretschmann, sphere_metric, ricci_scalar

sch = schwarzschild_metric(1.0)
ricci(sch, [0, 10, 1.2, 0.7])          # ≈ 0 (vacuum: Schwarzschild is Ricci-flat)
kretschmann(sch, [0, 10, 1.2, 0.7])    # ≈ 48/10⁶ = 4.8e-5  (curvature is real!)
ricci_scalar(sphere_metric(2.0), [1,0])# 0.5  = 2/a²
```

## Run
```bash
cd code
python3 curvature.py          # demo: flat=0, sphere R=2/a², Schwarzschild vacuum, focusing
python3 test_curvature.py     # 7 tests -> "All 7 tests passed."
```
*(Adds `../../../MA/MA-17_differential_geometry/code` to `sys.path`; run in place.)*

## Files
- `notes.md` — Riemann, its symmetries, Bianchi, Ricci/Einstein, geodesic deviation, singularities
- `code/curvature.py` — the toolkit (imports MA-17)
- `code/test_curvature.py` — flat=0, sphere constancy, Schwarzschild vacuum + Kretschmann, focusing
- `problems/problems.md` — worked problems (Zee, cpope)
- `refs.md` — verified citations
