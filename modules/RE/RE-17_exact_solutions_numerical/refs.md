# RE-17 — References

Page-level citations **verified by reading the page text** (PyMuPDF / `fitz`) in
the PDFs under `books/library/`. **Printed** = the number on the page; **PDF** =
the viewer page index. Offsets for Baumgarte–Shapiro and Stephani were measured
here (printed folios read off six pages each).

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| Baumgarte & Shapiro, *Numerical Relativity* (2010) | `RE_Relativity_Cosmology/NumericalRelativitySolvingEinsteinsEquationsOnTheComputerBaumgarteT.W.ShapiroS.L.Z-lib.org.pdf` | PDF = printed **+ 20** *(verified here)* |
| Stephani, Kramer, MacCallum, Hoenselaers & Herlt, *Exact Solutions of Einstein's Field Equations* (2nd ed., 2003) | `RE_Relativity_Cosmology/StephaniExactSolutionsEinsteinsFieldEquations.pdf` | PDF = printed **+ 31** *(verified here)* |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| Kerr / rotating black holes; frame dragging (printed 460–462), ergosphere (printed 467) (`kerr_metric`, `kerr_ergosphere`) | Zee | §VII.5 *Rotating Black Holes* | 458 | 481 |
| Kerr solution; **Boyer–Lindquist** coordinates named (`kerr_metric`) | Stephani | §20.5 *The Kerr solution and the Tomimatsu–Sato class* | 311 | 342 |
| Reissner–Nordström solution `ds²=r²dΩ²+(1−2m/r+e²/r²)⁻¹dr²−(…)dt²` (`reissner_nordstrom_metric`) | Stephani | §15.4 (explicit metric) | 232 | 264 |
| Schwarzschild solution (the `Q→0,a→0` limit, explicit `ds²`) | Stephani | §15.4 | 231 | 263 |
| de Sitter spacetime; constant-curvature Λ-vacuum (`de_sitter_metric`) | Zee | §IX.10 *De Sitter Spacetime* | 624 | 647 |
| spaces of constant curvature (de Sitter = Lorentzian `K>0`) | Stephani | §8.5 *Spaces of constant curvature* | 101 | 132 |
| numerical relativity; the initial-value / Cauchy problem | Zee | §VI.6 *Initial Value Problems and Numerical Relativity* | 400 | 423 |
| the 3+1 decomposition of Einstein's equations (`adm_decompose`) | Baumgarte–Shapiro | Ch. 2 *The 3+1 decomposition of Einstein's equations* (opener) | 23 | 43 |
| lapse function `α` (`adm_decompose`) | Baumgarte–Shapiro | Ch. 2, "…called the lapse function" | 30 | 50 |
| shift vector `β^a` (`adm_decompose`) | Baumgarte–Shapiro | Ch. 2, "…spatial shift vector βᵃ", Eq. (2.99) | 41 | 61 |
| Hamiltonian constraint `R+K²−K_{ab}K^{ab}=16πρ` (`hamiltonian_constraint_flat`); momentum constraint Eq. (2.96) | Baumgarte–Shapiro | Ch. 2, **Eq. (2.90)** (Hamiltonian), Eq. (2.96) (momentum) | 40 | 60 |
| choosing basis vectors → the ADM equations | Baumgarte–Shapiro | §2.7 *Choosing basis vectors: the ADM equations* | 43 | 63 |
| constructing constraint-satisfying initial data (constraints restated Eq. 2.132) | Baumgarte–Shapiro | Ch. 3 *Constructing initial data* (opener) | 54 | 74 |

## Cross-module dependency
Imports **RE-11** (`modules/RE/RE-11_curvature/code/curvature.py`) for
`ricci` / `einstein_tensor` / `ricci_scalar` (which in turn pull in **MA-17**
`diffgeo` for the finite-difference Riemann tensor and `metric_inverse`). This
module adds only metrics, field-equation validators, and the 3+1/ADM algebra; the
correctness of Kerr/de Sitter/RN is established *by* RE-11's curvature engine
(`verify_vacuum`, `verify_einstein_lambda`).

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Chs. 19 (Kerr), 22 (Reissner–
  Nordström) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 11 §11.7 (Kerr), Ch. 13 (de Sitter)
  — `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
- *(Both PDFs are scanned images with no extractable text, so page numbers are
  not cited — same policy as RE-11/RE-03 and Butkov in the MA trunk.)*
