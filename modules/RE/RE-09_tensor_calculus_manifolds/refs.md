# RE-09 — References

Page-level citations **verified by reading the page text** in the PDFs under
`books/library/`. **Printed** = the number on the page; **PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| C. Pope, *Geometry and Group Theory* lecture notes (GR chapters) | `RE_Relativity_Cosmology/cpope_notes.pdf` | cite by **PDF page + section** (folios not cleanly rendered) |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| tensors on a curved manifold, "the mother of all vectors" (`christoffel`, context) | Zee | §V.5 *Tensors in General Relativity* | 312 | 335 |
| why ∂V is not a tensor; the covariant derivative `D_λ W^μ = ∂_λ W^μ + Γ^μ_{λν}W^ν` (`covariant_derivative_*`) | Zee | §V.6 *Covariant Differentiation* | 320 | 343 |
| "classical" differential geometry of curves and surfaces (background) | Zee | §I.7 *Differential Geometry Made Easy* | 96 | 119 |
| covariant derivative def. `∇_μ V^ν = ∂_μ V^ν + Γ^ν_{μρ}V^ρ` (Eq. 4.31) (`covariant_derivative_vector`) | cpope | §4.3 *Covariant differentiation* | — | 39–40 |
| Christoffel from the metric `2Γ_{αμν}g_{αρ}=∂_μ g_{νρ}+∂_ν g_{μρ}−∂_ρ g_{μν}` (Eq. 4.47); metric compatibility (`christoffel`, `metric_compatibility`) | cpope | §4.3→§4.4 *Some properties of the covariant derivative* | — | 41–43 |
| parallel transport `dV^μ/dλ = 0` (Eq. 4.99) (`parallel_transport`) | cpope | §4.5 *Riemann curvature tensor* | — | 52–53 |
| holonomy `ΔV^μ = −½ R^μ_{νρσ}V^ν ΔA^{ρσ}` (Eq. 4.117) — curvature from transport round a loop (→ RE-11) | cpope | §4.5 / §4.6 | — | 55 |
| the 2-sphere worked example: `R_{1212}=sin²θ` (Eq. 4.122) — cross-check of sphere curvature | cpope | §4.6 *An example: The 2-sphere* | — | 55–56 |
| the geodesic equation `ẍ^μ + Γ^μ_{νρ}ẋ^ν ẋ^ρ = 0` (`geodesic_acceleration`, → RE-12) | cpope | §5 *Geodesics in General Relativity* / §5.1 | — | 56–57 |
| the Christoffel symbol itself `Γ^k_{ij} = ½ g^{kl}(∂_i g_{jl}+∂_j g_{il}−∂_l g_{ij})` (implementation) | — see **MA-17** `differential_geometry` (`diffgeo.christoffel`, `riemann`, `sphere_metric`, `plane_polar_metric`) | — | — | — |

## Problems
The problems in `problems/problems.md` are worked exercises drawn from the verified
Zee and cpope sections above (no separately-numbered end-of-chapter problems are
cited — Zee's exercises are embedded in the running text of §V.5–V.6, and the
cpope notes are lecture notes without a numbered problem set in these chapters).

## Cross-module dependency
This module imports **MA-17** (`modules/MA/MA-17_differential_geometry/code/diffgeo.py`)
for `christoffel` (the Levi-Civita connection), the reference metrics
`sphere_metric` / `plane_polar_metric`, and (downstream, RE-11) `riemann` / `ricci`.
See that module's `refs.md` for the underlying differential-geometry citations.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 6 (parallel transport,
  covariant differentiation) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 4 (the affine connection, covariant
  differentiation) — `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
