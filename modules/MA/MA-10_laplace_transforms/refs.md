# MA-10 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

All in **Chapter 8, Ordinary Differential Equations**. In the 3rd edition Boas
*moved* the Laplace transform, convolution and Dirac-delta material back into
Ch.8 (her preface: "abandon that [integral transforms] chapter and move the
Laplace transform and Dirac delta function material back to … Chapter 8").

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| the transform; operational rules (`laplace_numeric`, shift, derivative) | §8 *The Laplace Transform* | 437 | 456 |
| solving ODE IVPs (`solve_ivp_laplace`, `invert_quadratic`) | §9 *Solution of Differential Equations by Laplace Transforms* | 440 | 459 |
| convolution (`convolve`) | §10 *Convolution* (definition p.446) | 445 | 464 |
| the inverse pairs (`F_const … F_sin`) | *Table of Laplace Transforms* | 469 | 488 |

## Further reading (not page-pinned here)
- **Butkov**, *Mathematical Physics* (`MA_Mathematics/MPHY_butkov.pdf`) — integral
  transforms chapter (Laplace, Fourier, the Bromwich inversion contour). This PDF
  is a **scanned image with no text layer**, so its page numbers are not pinned
  in this file.
- The **Bromwich integral** (general inversion by residues) belongs to complex
  analysis, `~MA-06` (Boas Ch.14).

## Notes (verified)
- The Laplace section §8 opens on printed p.437 ("8. THE LAPLACE TRANSFORM"); §9
  ("SOLUTION OF DIFFERENTIAL EQUATIONS BY LAPLACE TRANSFORMS") on p.440; the
  *Table of Laplace Transforms* spans printed pp.469–471.
- §10 is titled *Convolution* (printed p.445), with "Definition of Convolution"
  on p.446 — matches the `convolve` integral ∫₀ᵗ f(τ)g(t−τ)dτ.
