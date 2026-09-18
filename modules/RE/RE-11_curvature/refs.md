# RE-11 — References

Page-level citations **verified by reading the page text** (PyMuPDF) in the PDFs
under `books/library/`. **Printed** = the number on the page; **PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| C. Pope, *Geometry & Group Theory / GR lecture notes* | `RE_Relativity_Cosmology/cpope_notes.pdf` | cite by **PDF page + section** (folios not rendered) |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| curvature: Gauss → Riemann; R=0 ⇔ flat (`riemann`) | Zee | §I.6 *Curved Spaces: Gauss and Riemann* | 82 | 105 |
| the Riemann tensor & its symmetries (`riemann`) | cpope | §4.5 *Riemann curvature tensor* | — | 52–55 |
| 2-sphere worked example `R_{1212}=sin²θ` (cross-check) | cpope | §4.6 *An example: the 2-sphere* | — | 55–56 |
| Ricci/scalar/Einstein tensor in GR (`ricci`, `einstein_tensor`) | Zee | §V.5 *Tensors in General Relativity* | 312 | 335 |
| geodesic deviation = tidal forces (`geodesic_deviation`) | Zee | §IX.3 *Geodesic Deviation* | 552 | 575 |
| Kretschmann / curvature singularity vs horizon (`kretschmann`) | Zee | §VII.2 *Black Holes and the Causal Structure of Spacetime* | 419 | 442 |
| the Christoffel/Riemann implementation | — see **MA-17** `differential_geometry` (`riemann`, `ricci`, `ricci_scalar`, `metric_inverse`) | — | — | — |

## Cross-module dependency
Imports **MA-17** (`modules/MA/MA-17_differential_geometry/code/diffgeo.py`) for
`riemann`/`ricci`/`ricci_scalar`/`metric_inverse`; this module adds the GR
contractions (`einstein_tensor`, `kretschmann`, `geodesic_deviation`) and the
reference metrics. Validated in 4-D by reproducing Schwarzschild's `R_{μν}=0` and
`K = 48M²/r⁶`.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 6 (curvature, the Riemann
  tensor) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 6 (curvature) — `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
