# MA-20 — References

Page-level citations **verified by reading the page text** in the PDFs.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Schaum's *Mathematical Handbook of Formulas and Tables* (Spiegel/Lipschutz/Liu) | `MA_Mathematics/schaums_equation_book.pdf` | PDF = printed **+ 12** |
| Chicone, *Ordinary Differential Equations with Applications*, **2nd ed.** | `MA_Mathematics/ode_with_applications_chicone.pdf` | PDF = printed **+ 20** |

(PDF = 1-based viewer page. For PyMuPDF use `load_page(PDF − 1)`.)

| Topic (code symbol) | Book — section / title | Printed p. | PDF p. |
|---|---|---|---|
| Simpson's (parabolic) rule (`simpson`) | Schaum's *Simpson's formula* (and §*Simpson's Rule*) | 109 / 231 | 121 / 243 |
| Newton's method (`newton`) | Schaum's *Newton's Method* | 233 | 245 |
| interpolation (forward differences / Lagrange) (`lagrange_interp`) | Schaum's *Newton's Forward-Difference Formula* & interpolation | 227 | 239 |
| Runge–Kutta (`rk4`) | Schaum's *Fourth-order Runge–Kutta method* | 236 | 248 |
| existence/uniqueness of the integrated ODE | Chicone §1.1 *Existence and Uniqueness* | 3 | 23 |

## Standard methods not page-pinned here
- **Gauss–Legendre quadrature**, **bisection**, **secant**, and the **power
  iteration** are textbook-standard but were not located as titled sections in the
  two text-extractable books above; they are presented on their own footing
  (Gauss nodes are the Legendre roots of `~MA-12`; power iteration complements the
  Jacobi/Sturm eigensolvers of `~MA-04`/`~MA-11`). No page is cited rather than
  guess one. (A dedicated numerical-analysis text — Press *Numerical Recipes*,
  Burden & Faires — is not on this shelf.)

## Notes (verified)
- Schaum's offset (+11) was cross-checked against its index ("Simpson's formula,
  109, 231"; "Runge–Kutta, 236") and the body tables.
- Chicone is used here only for the existence/uniqueness theorem (§1.1, p.3) that
  underwrites integrating an IVP; its dynamics content anchors `~MA-22`.
- Boas has **no** dedicated numerical-methods chapter (verified by full-text
  search for "Simpson"/"Numerical Methods"), which is why MA-20 leans on Schaum's.
