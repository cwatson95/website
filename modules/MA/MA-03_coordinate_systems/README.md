# MA-03 — Coordinate Systems

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-01`.
**Feeds:** `~MA-02` (operators in curvilinear coords), `~EM-04` (boundary-value
problems), `~QM-12` (central potentials), `~CM-11` (orbits).

## Scope
Cartesian ↔ cylindrical ↔ spherical transforms, the orthonormal curvilinear
**basis vectors**, the **scale factors** h_i, and the **Jacobian** volume
elements. Reuses MA-01's `dot`/`cross`/`norm` to verify the bases are
orthonormal and right-handed.

Conventions: cylindrical (ρ, φ, z); spherical (r, θ, φ) with θ the polar angle
from +z ∈ [0, π] and φ the azimuth ∈ (−π, π].

## Operations — `code/coordinates.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `cart_to_cyl` / `cyl_to_cart` | cylindrical transform | Boas §5.4 p.260; Griffiths §1.4.2 p.43 |
| `cart_to_sph` / `sph_to_cart` | spherical transform | Boas §5.4 p.261; Griffiths §1.4.1 p.38 |
| `cyl_basis(phi)` / `sph_basis(theta, phi)` | unit vectors (Cartesian comps) | Griffiths §1.4.1 p.38 |
| `cyl_scale_factors` / `sph_scale_factors` | (h_ρ,h_φ,h_z), (h_r,h_θ,h_φ) | Boas Ch.10 §8 p.521 |
| `cyl_jacobian` / `sph_jacobian` | dV factor: ρ ; r²sinθ | Boas §5.4 p.258 (Jacobians) |
| `vector_to_spherical` / `vector_from_spherical` | components in the sph basis | Griffiths §1.4.1 p.38 |

Scale factors and the Jacobian are linked: J = h₁h₂h₃ (the dV factor).

## Use
```python
import math
from coordinates import cart_to_sph, sph_basis, sph_jacobian

cart_to_sph(1, 1, 0)            # (sqrt2, pi/2, pi/4)  = (r, theta, phi)
e_r, e_th, e_ph = sph_basis(math.radians(60), math.radians(40))
sph_jacobian(2.0, math.pi/2)   # r^2 sin(theta) = 4.0   (dV = r^2 sinθ dr dθ dφ)
```

## Run
```bash
cd code
python3 coordinates.py          # demo (transforms, orthonormal basis, scale factors)
python3 test_coordinates.py     # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/coordinates.py` · `code/test_coordinates.py` · `problems/problems.md`
