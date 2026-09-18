# RE-09 — Tensor Calculus on Manifolds

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The step
from flat-space tensors to tensors on a **curved manifold**: the position-dependent
metric `g_{μν}(x)`, the Christoffel symbols, the covariant derivative, parallel
transport and holonomy, and the geodesic equation — the differential geometry that
becomes general relativity.

- **Prerequisites:** `RE-08` (covariant formulation — tensors in flat SR);
  **`~MA-17`** (differential geometry — the Christoffel/Riemann machinery). This is
  the dependency flagged in the topic network: RE-09 *uses* MA-17's code.
- **Feeds into:** `~RE-10` (equivalence principle — Γ vanishes in a locally
  inertial frame), `~RE-11` (curvature: Riemann & Ricci, holonomy density),
  `~RE-12` (geodesics & the variational principle).

## The one idea
On a curved manifold the basis vectors vary from point to point, so the plain
partial derivative `∂_i V^k` is **not** a tensor. The fix is the **covariant
derivative**, which adds a Christoffel correction that cancels the basis drift:
```
∇_i V^k = ∂_i V^k + Γ^k_{ij} V^j        (contravariant)
∇_i W_k = ∂_i W_k − Γ^j_{ik} W_j        (covariant)
```
The connection `Γ^k_{ij} = ½ g^{kl}(∂_i g_{jl} + ∂_j g_{il} − ∂_l g_{ij})` is the
**unique** one that is metric-compatible (`∇g = 0`) and torsion-free. Curvature
then shows up as **holonomy**: a vector parallel-transported around a closed loop
comes back rotated by the enclosed curvature.

## Built on MA-17
The Christoffel symbols are **not reimplemented** — `christoffel` here is a thin
re-export of `diffgeo.christoffel`, and the reference metrics (`sphere_metric`,
`plane_polar_metric`) are MA-17's:
```python
import diffgeo                          # MA-17, imported by relative path
christoffel(g, x)  ==  diffgeo.christoffel(g, x)     # Gamma^k_ij = Gam[k][i][j]
```
Everything else (covariant differentiation, parallel transport, geodesic
acceleration, the metric-compatibility check) is built on top by finite
differences. `metric` is a **callable** `x ↦ g`, exactly as in MA-17.

## Operations — `code/covariant_derivative.py`
| call | meaning |
|------|---------|
| `minkowski_metric()` | the flat field `η = diag(−1,+1,+1,+1)` (all Γ ≈ 0) |
| `christoffel(g, x)` | Levi-Civita `Γ^k_{ij}` = `Gam[k][i][j]` (MA-17 re-export) |
| `covariant_derivative_vector(g, Vfield, x)` | `∇_i V^k = ∂_i V^k + Γ^k_{ij}V^j` → `M[i][k]` |
| `covariant_derivative_covector(g, Wfield, x)` | `∇_i W_k = ∂_i W_k − Γ^j_{ik}W_j` → `M[i][k]` |
| `parallel_transport(g, V0, path, steps)` | drag `V0` along `path` (`δV^k = −Γ^k_{ij}V^j dx^i`) |
| `geodesic_acceleration(g, x, xdot)` | `ẍ^k = −Γ^k_{ij} ẋ^i ẋ^j` (geodesic ⇔ this is 0) |
| `metric_compatibility(g, x)` | `max|∇_i g_{jk}|` (≈ 0 for Levi-Civita) |

## Use
```python
import sys; sys.path.insert(0, "code")
from covariant_derivative import christoffel, geodesic_acceleration, parallel_transport
import diffgeo
g = diffgeo.sphere_metric(1.0)                 # unit 2-sphere, g = diag(1, sin^2 th)

christoffel(g, [1.0, 0.4])[0][1][1]            # Gamma^theta_phiphi = -sin cos = -0.4546
geodesic_acceleration(g, [3.14159/2, 0], [0,1])# ~[0,0]  equator is a great circle
geodesic_acceleration(g, [1.0, 0], [0,1])      # [0.4546,0]  a latitude is NOT a geodesic

loop = [[1,0],[1,0.3],[1.3,0.3],[1.3,0],[1,0]] # closed lat-long rectangle
parallel_transport(g, [1.0, 0.0], loop, 400)   # returns ROTATED -> holonomy ~ area
```

## Run
```bash
cd code
python3 covariant_derivative.py        # demo: flat Γ=0, sphere Γ, geodesics, holonomy≈area
python3 test_covariant_derivative.py   # 9 tests -> "All 9 tests passed."
```
*(The module adds `../../../MA/MA-17_differential_geometry/code` to `sys.path`, so
run it in place; no install needed.)*

## Files
- `notes.md` — the metric field, why ∂V isn't a tensor, the connection, ∇, parallel
  transport & holonomy, geodesics, and Γ vanishing in a local inertial frame
- `code/covariant_derivative.py` — the library (imports MA-17; pure stdlib otherwise)
- `code/test_covariant_derivative.py` — flat reduction, sphere Christoffels, `∇g=0`,
  geodesics, holonomy ≈ enclosed area
- `problems/problems.md` — worked problems (Zee §V.5–V.6, cpope §4)
- `refs.md` — verified textbook citations
