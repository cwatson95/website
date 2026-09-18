# MA-13 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

All in **Chapter 9, Calculus of Variations** (opens printed p.472 / PDF 491).

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| functionals; the shortest-distance question (`functional`) | §1 *Introduction* | 472 | 491 |
| the Euler equation (`euler_lagrange_residual`) | §2 *The Euler Equation* | 474 | 493 |
| applying it; first integral / no-x shortcut (`minimize_path`, `beltrami`, `catenary`) | §3 *Using the Euler Equation* | 478 | 497 |
| brachistochrone & cycloids (`cycloid_brachistochrone`) | §4 *The Brachistochrone Problem; Cycloids* | 482 | 501 |
| several variables → Lagrange's equations | §5 *Several Dependent Variables; Lagrange's Equations* | 485 | 504 |
| constraints (isoperimetric) | §6 *Isoperimetric Problems* | 491 | 510 |
| δ-notation | §7 *Variational Notation* | 493 | 512 |

## Cross-trunk (the physics this becomes)
| Topic | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| Lagrange's equations from a variational principle (`~CM-17`) | Boas §5 (above) | 485 | 504 |

## Notes (verified)
- Boas's §3 (p.478) is where the "if L has no explicit x" shortcut is used (it
  leads straight to the cycloid and catenary first integrals); the module's
  `beltrami` is that conserved quantity L − y′L_{y′}.
- §5 (p.485) explicitly titles the multi-variable case *Lagrange's Equations* —
  the direct hand-off to `~CM-17` (Lagrangian mechanics) and bridge **B1**.
- Marion & Thornton Ch.6–7 and Goldstein Ch.2 give the same material from the
  mechanics side; pinned there in `~CM-17` when that module is built.
