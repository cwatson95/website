# RE-14 — References

Page-level citations **verified by reading the page text** (PyMuPDF) in the PDFs
under `books/library/`. **Printed** = the number on the page; **PDF** = the
viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| C. Pope, *General Relativity lecture notes* | `RE_Relativity_Cosmology/cpope_notes.pdf` | cite by **PDF page + section** (folios not rendered) |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| Schwarzschild metric; vacuum (Ricci-flat) exterior (`schwarzschild_metric`, `lapse`) | Zee | §VI.3 *The Schwarzschild-Droste Metric and Solar System Tests of Einstein Gravity* | 362 | 385 |
| " — derivation of the static, spherically-symmetric solution | cpope | §6.2 *The Schwarzschild solution* | — | 71 |
| horizon `r=2M` = coordinate singularity; causal structure; `K` finite there (`horizon_radius`, `kretschmann_formula`) | Zee | §VII.2 *Black Holes and the Causal Structure of Spacetime* | 419 | 442 |
| massive effective potential; ISCO `r = 3r_S = 6M` (`effective_potential`, `isco`) | Zee | §VII.1 *Particles and Light around a Black Hole*, Eq. 8 | 414 | 437 |
| massless effective potential `U=1/r²−r_S/r³`, max at `3r_S/2 = 3M` → photon sphere (`effective_potential_massless`, `photon_sphere`) | Zee | §VII.1, Eq. 12 | 415 | 438 |
| orbits & perihelion precession `Δφ = 6π(M/l)²` (`perihelion_precession`) | Zee | §VI.3 *Solar System Tests* (Mercury, 43″/century) | 368–369, 372 | 391–392, 395 |
| " (effective-potential treatment of orbits) | cpope | §6.3.1 *Orbits around a star or black hole* | — | 75 |
| light deflection `4M/b` (`light_deflection`) | Zee | §VI.3 *Solar System Tests* (bending of light) | 370 | 393 |
| " (photon orbits & bending of light by the Sun) | cpope | §6.3.2 *Photon orbits, and bending of light by the Sun* | — | 79 |
| Shapiro radar echo delay (`shapiro_delay`) | Zee | §VI.3, *Appendix 2: Radar echo delay* | 372 | 395 |
| infall: finite proper, infinite coordinate time (radial geodesics) | cpope | §10.2 *Radial geodesics in Schwarzschild* | — | 139 |
| the event horizon (one-way surface) | cpope | §10.3 *The event horizon* (ch. §10 *Global Structure of Schwarzschild Black holes*, from PDF 133) | — | 140 |
| Kretschmann scalar `K = 48M²/r⁶`; the Riemann/Ricci machinery | — see **RE-11** `curvature` (and **MA-17** `diffgeo`) | — | — | — |

## Cross-module dependency
Imports **RE-11** (`modules/RE/RE-11_curvature/code/curvature.py`) for
`schwarzschild_metric`, `ricci`, and `kretschmann` (RE-11 in turn imports MA-17).
The tests reuse RE-11 to confirm the exterior is Ricci-flat and that
`kretschmann` reproduces `48M²/r⁶`. The Newtonian central-force comparison
(Kepler ellipses, no precession) forward-references **~CM-11** (not yet built); the
orbit integrator here is a self-contained RK4, not an import.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 16–17 (the Schwarzschild
  solution & black holes) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 8 (the Schwarzschild solution) —
  `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
- *(Both PDFs are scanned images with no extractable text, so page numbers are not
  cited — same policy as the MA/RE trunks.)*
- Griffiths' *Introduction to Electrodynamics* does **not** cover general
  relativity, so unlike the SR modules (RE-02–RE-08) there is no Griffiths cite here.
