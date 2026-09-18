# MA-14 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

Boas introduces Green functions for ODEs at the end of **Chapter 8** (with the
Dirac delta, `~MA-15`) and applies them to PDEs in **Chapter 13**.

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| ODE Green's function; point-source construction (`green_dirichlet`, `green_helmholtz`, `solve_bvp_greens`, `causal_green_oscillator`) | Ch.8 §12 *A Brief Introduction to Green Functions* | 461 | 480 |
| the delta source L G = δ (`~MA-15`) | Ch.8 §11 *The Dirac Delta Function* | 449 | 468 |
| Green functions for PDEs; spectral use (`green_series`) | Ch.13 *Use of Green Functions* | 657 | 676 |

## Further reading (not page-pinned here)
- **Butkov**, *Mathematical Physics* (`MA_Mathematics/MPHY_butkov.pdf`) has a full
  Green's-functions chapter (Sturm–Liouville inverse, PDE fundamental solutions).
  Scanned image PDF (no text layer), so pages are not pinned here.

## Notes (verified)
- The ODE Green's-function section is titled *A Brief Introduction to Green
  Functions* and runs from printed **p.461** (§12 of Ch.8); it sits immediately
  after the Dirac-delta section (§11, p.449), which is why MA-14 lists MA-15 as a
  prerequisite even though MA-15 has the higher module number.
- "Use of Green Functions" recurs in **Chapter 13** (printed p.657) for partial
  differential equations — the eigenfunction-expansion / fundamental-solution
  viewpoint of `green_series`.
- Symmetry G(x,ξ)=G(ξ,x) follows from self-adjointness of L (`~MA-11` §2); the
  spectral form G=Σφₙφₙ/λₙ is completeness (`~MA-11`) divided by the spectrum.
