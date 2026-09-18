# RE-10 — References

Page-level citations **verified by reading the page text** in the PDFs under
`books/library/` (via PyMuPDF), not inferred from a table of contents.
**Printed** = the number on the page; **PDF** = the page index in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| C. M. Will, *Theory and Experiment in Gravitational Physics* (rev. ed.) | `RE_Relativity_Cosmology/Grav_physics_Clifford_Will.pdf` | PDF = printed **+ 17** |
| C. Pope, *Geometry & Group Theory / GR lecture notes* | `RE_Relativity_Cosmology/cpope_notes.pdf` | folios not rendered — cite by **PDF page + section** |

## Topic → location

| Topic (code symbol) | Source | Section / item | Printed p. | PDF p. |
|---|---|---|---|---|
| "The happiest thought" (Einstein 1907; free fall ⇒ no weight) | Zee | *Prologue to Book Two: The Happiest Thought* | 265 | **288** |
| Free fall is locally inertial; gravity ↔ acceleration (§2) | Zee | §V.1 *Spacetime Becomes Curved* | 275 | **298** |
| Redshift, light bending, geometry from the EP (§3–4, 7) (`grav_redshift`) | Zee | §V.2 *The Power of the Equivalence Principle* | 280 | **303** |
| Local free-fall frame; why "local" is essential (§2, §6) | C. Pope | *Equivalence Principle*, §1–2 | — | **10** |
| Einstein EP stated; local Lorentz frame (§2, §7) | Will | Ch. 2 §2.3 *The Einstein Equivalence Principle* | 22 | **39** |
| Eötvös ratio `η = 2|a₁−a₂|/(a₁+a₂)` (`eotvos_parameter`, §1) | Will | Ch. 2, WEP-tests section, "Eötvös ratio" | 25 | **42** |
| Torsion-balance Eötvös experiment (`eotvos_parameter`, §1) | Will | Ch. 2, **Fig. 2.2** (schematic of the balance) | 26 | **43** |
| Bounds on WEP violation (Newton → Eötvös → Braginsky → satellite) | Will | Ch. 2, **Table 2.2** *Tests of the weak equivalence principle* | 27 | **44** |

## Notes on the sources
- **Zee** develops the EP heuristically through parables before any field
  equations — exactly the logic of this module (redshift and bending "for free").
  The *Prologue to Book Two* (PDF 288) is Einstein's own "happiest thought" quote.
- **Will Ch. 2** is the standard rigorous reference for the *experimental* status of
  the EP: the Eötvös ratio `η` (PDF 42) is the quantity coded as `eotvos_parameter`,
  Fig. 2.2 (PDF 43) is the torsion balance, and Table 2.2 (PDF 44) lists the
  historical bounds quoted in `notes.md` §1.
- **Pope's notes** (PDF 10) give the clean statement that a free-fall frame is
  inertial *only locally* — the seed of the §6 tidal/curvature distinction.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 9 (the principle of
  equivalence) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 3 (the principle of equivalence) —
  `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
- *(Both PDFs are scanned images with no extractable text, so page numbers are not
  cited — same policy as Butkov in the MA trunk.)*
