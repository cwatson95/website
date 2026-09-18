# RE-01 — References

Page-level citations **verified by reading the page text** (PyMuPDF) in the PDFs
under `books/library/`. **Printed** = the number on the page; **PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| Galilean vs Maxwell; why `c` has no frame | Zee | §III.1 *Galileo versus Maxwell* | 159 | 182 |
| Einstein's postulates; the ether & Michelson–Morley | Griffiths | §12.1.1 *Einstein's Postulates* | 502 | 520 |
| aberration of starlight & the ether (historical) | Griffiths | §12.1.1 (same section) | 505 | 523 |
| Galilean (`c→∞`) limit of the Lorentz transformation | Griffiths | §12.1.3, **Prob. 12.18(a)** (Galilean transformation matrix) | 527 | 545 |
| the Galilean transformation `r'=r−Vt` (`galilean_position`) | — see **CM-03** `reference_frames` (`galilean_position`, `galilean_velocity`) | — | — | — |
| Einstein velocity addition (`relativistic_velocity_add`) | — see **RE-03** `lorentz` (`velocity_add`); Griffiths §12.1.3 Ex. 12.6 | 519 | 537 |

## Problems (verified, Griffiths 4th ed.)
- **Prob. 12.18(a)** — write the matrix of a Galilean transformation (and compare
  to a rotation and a Lorentz boost) — printed **527**, PDF 545.
- (Conceptual) The Michelson–Morley analysis above follows Griffiths §12.1.1 and
  the standard `Δt ≈ (L/c)(v/c)²` ether-wind calculation.

## Cross-module dependencies
- **CM-03** `reference_frames` — the Galilean boost this module contrasts with SR.
- **RE-03** `lorentz` — the Lorentz transformation whose `c→∞` limit is Galilean.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 1–2 (the Michelson–Morley
  experiment, the ether) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 2 — `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
