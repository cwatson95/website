# RE-05 — References

Page-level citations **verified by reading the page text** in the PDFs under
`books/library/`. **Printed** = the number on the page; **PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| invariant interval, 4-vectors, the metric (`interval2`, `mdot`) | Griffiths | §12.1.4 *The Structure of Spacetime* | 525 | 543 |
| Minkowski geometry, light cones, spacetime diagrams (`classify`, `causal_relation`) | Zee | §III.3 *Minkowski and the Geometry of Spacetime* | 174 | 197 |
| proper time / the invariant interval ds² | Griffiths | §12.2.1 *Proper Time and Proper Velocity* | 532 | 550 |
| 4-velocity, mass shell `p·p = −m²` (`four_momentum`, `invariant_mass`) | Griffiths | §12.2.2 *Relativistic Energy and Momentum* | 535 | 553 |
| raising/lowering indices with the metric (`lower`, `raise_`) | — see **MA-16** `tensor_analysis` (`lower_index`, `raise_index`, `inner`) | — | — | — |

## Problems (verified, Griffiths 4th ed.)
- **Prob. 12.20** — events, coordinates, and the invariant interval — printed **529**, PDF 547.
- **Prob. 12.21** — coordinates of an event in two frames — printed **529**, PDF 547.
- **Prob. 12.26** — find the invariant product of the 4-velocity with itself (`U·U = −1` ⇒ `= −c²`) — printed **535**, PDF 553.

## Cross-module dependency
This module imports **MA-16** (`modules/MA/MA-16_tensor_analysis/code/tensors.py`)
for `inner`, `lower_index`, `raise_index`. See that module's `refs.md` (Boas Ch.10
tensor analysis) for the underlying index-notation citations.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 3 (the spacetime of SR) —
  `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 2 — `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
