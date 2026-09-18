# MA-07 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| separable first-order | Ch.8 §2 *Separable Equations* | 395 | 414 |
| linear first-order | Ch.8 §3 *Linear First-Order Equations* | 401 | 420 |
| 2nd-order const-coeff, homogeneous (oscillator) (`second_order_system`) | Ch.8 §5 *Second-Order Linear Equations…Zero Right-Hand Side* | 408 | 427 |
| forced / inhomogeneous (resonance) | Ch.8 §6 *…Right-Hand Side Not Zero* | 417 | 436 |
| series / Frobenius solutions | Ch.12 §11 *Generalized Power Series or the Method of Frobenius* (also §21 Fuchs) | 585 | 604 |

## Notes
- The **numerical** integrators (Euler, RK4) are standard methods, not a Boas
  section; the citations above are for the analytic ODE theory the code solves.
- `linear_evolve_symmetric` reuses `~MA-04`'s `eig_symmetric`; the constant-coefficient
  linear-system theory is Boas §8.5.

## Further reading (not page-verified)
- Butkov, *Mathematical Physics*, **Ch.3** (linear differential equations of second
  order; the nonhomogeneous case / variation of constants). `MA_Mathematics/MPHY_butkov.pdf`
  is a **scanned, image-only PDF with no text layer**, so its section/page numbers are
  not verifiable here and are deliberately omitted.
