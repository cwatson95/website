# MA-21 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

The **asymptotics** are Boas **Chapter 11, Special Functions**:

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| asymptotic series; optimal truncation (`exp_integral_scaled_*`, `optimal_truncation`) | §10 *Asymptotic Series* | 549 | 568 |
| Stirling's formula (`ln_factorial_stirling`) | §11 *Stirling's Formula* | 552 | 571 |
| the error function & related integrals | §9 *The Error Function* | 547 | 566 |
| the Gamma function (factorials → continuous) | §3 *Definition of the Gamma Function* | 538 | 557 |

## Dimensional analysis — honest note
**Buckingham's Pi theorem / dimensional analysis is NOT covered in the
text-extractable books on the `Mathematics/` shelf.** Verified by full-text search:
neither Boas, nor *Schaum's Mathematical Handbook of Formulas and Tables*
(`schaums_equation_book.pdf`), contains "Buckingham", "pi theorem", or
"dimensional analysis". The `buckingham_pi`/`nullspace` code is therefore presented
on its own mathematical footing (the Pi groups are literally the null space of the
dimension matrix, `~MA-04`); it is standard material in fluids/transport texts
(e.g. Barenblatt, *Scaling*; any Reynolds-number treatment, `~CM-23`/`~PK-03`) which
are not on this shelf. No page is cited rather than guess one.

## Notes (verified)
- Boas §10 (p.549) is explicit that an asymptotic series "may diverge" yet be
  useful, with the error bounded by the first omitted term — exactly the
  optimal-truncation behavior the code demonstrates.
- §11 (p.552) gives Stirling's formula with the 1/(12n) correction; the module's
  `terms` argument toggles successive corrections.
- Regular perturbation is the elementary face of the asymptotic methods of §10;
  the full physics treatment is `~QM-15` (Rayleigh–Schrödinger, WKB).
