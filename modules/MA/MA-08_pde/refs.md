# MA-08 — References

Page-level citations **verified by reading the page text** in the PDFs.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

| Topic (code symbol) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| Laplace's equation (`laplace_2d`) | Boas | §13.2 *Laplace's Equation; Steady-State Temperature in a Rectangular Plate* | 621 | 640 |
| " | Griffiths | §3.1 *Laplace's Equation* | 113 | 131 |
| heat / diffusion equation (`heat_1d`, `heat_mode`) | Boas | §13.3 *The Diffusion or Heat Flow Equation; the Schrödinger Equation* | 628 | 647 |
| wave equation (`wave_1d`, `wave_mode`) | Boas | §13.4 *The Wave Equation; the Vibrating String* | 633 | 652 |
| separation of variables (the analytic method) | Griffiths | §3.3 *Separation of Variables* (Cartesian §3.3.1 p.131; "Fourier's trick" p.136; spherical §3.3.2 p.141) | 130 | 148 |
| Schrödinger equation (separation-of-variables BVP) | Boas | §13.3 subsection "The Schrödinger Equation" (eq. 3.22) | 631 | 650 |

## Notes (verified)
- Griffiths correction: separation of variables is **§3.3** (p.130), *not* §3.2 (that
  is the *Method of Images*). "Fourier's trick" is named on p.136 (Cartesian) and
  recurs for Legendre on p.144.
- The **finite-difference** solvers here are standard numerical schemes (FTCS, leapfrog,
  Gauss–Seidel), not a textbook section; the citations are for the PDEs and the
  separation-of-variables solutions the code is checked against.

## Further reading (not page-verified)
- Butkov, *Mathematical Physics*, **Ch.8** (partial differential equations — the
  stretched string / wave equation, separation of variables, Laplace & Poisson, the
  diffusion equation). `MA_Mathematics/MPHY_butkov.pdf` is a **scanned, image-only PDF
  with no text layer**, so its section/page numbers are not verifiable here.
