# MA-04 — References

Page-level citations **verified by reading the page text/images** in the PDFs.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** (2004) | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** |

## Boas — Chapter 3, Linear Algebra

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| matrix operations & multiplication (`matmul`, `transpose`, `trace`) | §6 *Matrix Operations* | 114 | 133 |
| determinant (`det`) | §3 *Determinants; Cramer's Rule* | 89 | 108 |
| solving systems / inverse (`solve`, `inverse`) | §2 *Matrices; Row Reduction* | 83 | 102 |
| linear vector spaces (basis, dimension, inner product) | §10 *Linear Vector Spaces* | 142 | 161 |
| eigenvalues, eigenvectors, diagonalization (`eig_symmetric`, `eigvals_2x2`) | §11 *Eigenvalues and Eigenvectors; Diagonalizing Matrices* (orth./symm./Herm. pp.152–161) | 148 | 167 |
| diagonalization in practice (`reconstruct`) | §12 *Applications of Diagonalization* | 162 | 181 |

## Marion & Thornton — the physics connection

| Topic | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| matrix operations & multiplication | §1.5 *Matrix Operations* | 9 | 23 |
| eigenvalue problem / diagonalization **via the inertia tensor** | §11.5 *Principal Axes of Inertia* — secular determinant \|I_ij − λδ_ij\| = 0 (eq. 11.39) | 425 | 439 |

## Notes (verified)
- Terminology: Boas uses **"row reduction"**, not "Gaussian elimination" (same procedure).
- M&T has **no standalone determinant section in Ch.1** (the only Ch.1 determinant is
  the cross-product mnemonic, §1.12 p.28). It introduces the **eigenvalue / diagonalization**
  machinery with the inertia tensor in §11.5 (p.425) — precisely the `~CM-13` use of
  `eig_symmetric`. The terms eigenvalue/eigenvector/diagonalization are named near §11.7
  (p.440); the characteristic equation recurs for coupled oscillations (`~CM-16`, p.479).
