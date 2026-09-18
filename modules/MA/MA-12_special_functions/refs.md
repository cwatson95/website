# MA-12 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

Chapter 12 is titled *Series Solutions of Differential Equations; Legendre,
Bessel, Hermite, and Laguerre Functions* (opens printed p.562 / PDF 581);
spherical harmonics appear in **Chapter 13** (PDEs).

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| Legendre's equation & recurrence (`legendre`) | Ch.12 §2 *Legendre's Equation* | 564 | 583 |
| Rodrigues' formula | Ch.12 §4 *Rodrigues' Formula* | 568 | 587 |
| generating function (`legendre_generating`) | Ch.12 §5 *Generating Function for Legendre Polynomials* | 569 | 588 |
| complete orthogonal sets | Ch.12 §6 *Complete Sets of Orthogonal Functions* | 575 | 594 |
| Legendre orthogonality (`orthogonality_legendre`) | Ch.12 §7 *Orthogonality of the Legendre Polynomials* | 577 | 596 |
| Legendre series | Ch.12 §9 *Legendre Series* | 580 | 599 |
| associated Legendre (`assoc_legendre`) | Ch.12 §10 *The Associated Legendre Functions* | 583 | 602 |
| Bessel's equation (`bessel_j`) | Ch.12 §12 *Bessel's Equation* | 587 | 606 |
| Bessel orthogonality | Ch.12 §19 *Orthogonality of Bessel Functions* | 601 | 620 |
| Hermite & Laguerre; ladder operators (`hermite`, `laguerre`) | Ch.12 §22 *Hermite Functions; Laguerre Functions; Ladder Operators* | 607 | 626 |
| spherical harmonics Y_l^m | Ch.13 *Partial Differential Equations* ("are the spherical harmonics Y_l^m") | 651 | 670 |

## Further reading (not page-pinned here)
- **Butkov**, *Mathematical Physics* (`MA_Mathematics/MPHY_butkov.pdf`) — full
  chapters on each family with contour-integral generating functions. Scanned
  image PDF (no text layer), so pages are not pinned here.

## Notes (verified)
- §22 (printed p.607) carries **both** Hermite *and* Laguerre functions and the
  ladder-operator viewpoint — the exact bridge to `~QM-09` (the algebraic oscillator).
- "spherical harmonics Y_l^m" is verified on printed **p.651** (Ch.13); the
  associated Legendre machinery they rest on is Ch.12 §10 (p.583).
- Bessel orthogonality (§19, p.601) uses weight **w = r** on [0,a] with the zeros
  α_k as the eigenvalue labels — the cylindrical Sturm–Liouville problem (`~MA-11`).
