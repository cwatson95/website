# RE-12 — References

Page-level citations **verified by reading the page text** (PyMuPDF) in the PDFs
under `books/library/`. **Printed** = the number on the page; **PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| C. Pope, *Geometry & Group Theory / GR lecture notes* | `RE_Relativity_Cosmology/cpope_notes.pdf` | cite by **PDF page + section** (folios offset, not rendered as the viewer page) |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| geodesics as the shortest distance; variational calculus with several functions (`euler_lagrange_gives_christoffel`) | Zee | §II.2 *The Shortest Distance between Two Points* | 123 | 146 |
| the action principle (`lagrangian`, `action_length`) | Zee | §II.3 *Physics Is Where the Action Is* | 136 | 159 |
| motion in curved spacetime; the geodesic equation `d²X^λ/dτ² + Γ ẊẊ = 0` (`geodesic_rhs`) | Zee | §V.4 *Motion in Curved Spacetime* | 301 | 324 |
| geodesic motion in curved spacetime (`integrate_geodesic`) | cpope | §5 / §5.1 *Geodesic motion in curved spacetime* | — | 57 |
| the **Geodesic Equation** (5.11), `d²x^μ/dτ² + Γ^μ_{νρ}ẋ^νẋ^ρ = 0` (`geodesic_rhs`) | cpope | §5.1 (eq. 5.11) | — | 60 |
| the affine parameter (`integrate_geodesic`'s `dtau`) | cpope | §5.1 (affine parameter) | — | 61 |
| the Euler–Lagrange / Christoffel machinery | — see **MA-13** `variational` (`euler_lagrange_residual`) and **MA-17** `diffgeo` (`christoffel`, `metric_inverse`) | — | — | — |
| maximal proper time (reversed triangle inequality) | — see **RE-05** `minkowski` (`proper_time`) | §3 | — | — |

*All Zee and cpope pages above were re-read with PyMuPDF; cpope's chapter 5 is
titled "Geodesics in General Relativity" (heading on PDF 56, §5.1 on PDF 57), and
the boxed Geodesic Equation (5.11) sits on PDF 60.*

## Cross-module dependency
Imports **MA-17** (`modules/MA/MA-17_differential_geometry/code/diffgeo.py`) for
`christoffel`/`metric_inverse`/`sphere_metric` — the geodesic RHS needs `Γ` — and
**MA-13** (`modules/MA/MA-13_calculus_of_variations/code/variational.py`) for
`euler_lagrange_residual`, used to show the geodesic equation **is** the
Euler–Lagrange equation of the action (the variational ⇔ Christoffel equivalence,
`euler_lagrange_gives_christoffel`). Maximal aging reuses **RE-05**'s
proper-time/reversed-triangle logic via `action_length`. Builds directly on
**RE-11** (the curvature/Christoffel toolkit).

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 6 (geodesics, the geodesic
  equation) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 3 (the geodesic equation, the
  variational principle) — `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
