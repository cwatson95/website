# RE-08 — References

Page-level citations **verified by reading the page text** in the PDFs under
`books/library/` (each checked with PyMuPDF, not inferred from a table of
contents). **Printed** = the number on the page; **PDF** = the page index in the
viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| "a tensor transforms like a tensor" — the transformation-law definition | Zee | §I.4 *Who Is Afraid of Tensors?* | 52 | 75 |
| contra/covariant 4-vectors, the metric, index notation (`transform_vector`, `lower`, `raise_`, `mdot`) | Griffiths | §12.1.4 *The Structure of Spacetime* | 525 | 543 |
| Minkowski geometry / the metric as fixed background (`ETA`) | Zee | §III.3 *Minkowski and the Geometry of Spacetime* | 174 | 197 |
| rank-2 transformation law `t̄^{μν}=Λ^μ_λΛ^ν_σ t^{λσ}` + symmetric tensors (`transform_tensor2`, `symmetric_part`) | Griffiths | §12.3 *Relativistic Electrodynamics*, **Eq. 12.115** | 563 | 581 |
| symmetry/antisymmetry preserved by Λ (`symmetry_type_preserved` test) | Griffiths | §12.3, **Prob. 12.50** | 564 | 582 |
| covariant 4-vector by lowering the 0-component; invariants `F^{μν}F_{μν}` (`lower`, `double_contract`, `trace`) | Griffiths | §12.3, **Prob. 12.51** | 565 | 583 |
| the 4-gradient `∂/∂x^μ` and the d'Alembertian `□ = ∂_ν∂^ν = ∇²−∂_t²/c²` (`four_gradient`, `dalembertian`) | Griffiths | §12.3.5 *Relativistic Potentials*, **Eq. 12.133, 12.138** | 569–570 | 587–588 |

## Downstream application (NOT a prerequisite of this module)
- The field tensor `F^{μν}` (built from the antisymmetric-tensor + 4-gradient
  machinery here) — Griffiths §12.3.3 *The Field Tensor*, printed **562**, PDF 580;
  the explicit `F^{μν}` array is **Eq. 12.119**, printed 564, PDF 582. This is the
  content of module **~EM-18** (relativistic electrodynamics / covariant Maxwell).

## Cross-module dependencies
- Imports **MA-16** (`modules/MA/MA-16_tensor_analysis/code/tensors.py`) for
  `inner`, `lower_index`, `raise_index`, `kronecker_delta`. See that module's
  `refs.md` for the underlying index-notation citations.
- Imports **RE-03** (`modules/RE/RE-03_lorentz_transformations/code/lorentz.py`)
  for the boosts Λ (`general_boost`, `boost`, `inverse`, `apply`). The
  inverse-transpose used by `transform_covector` is RE-03's
  `inverse(L) = η Λᵀ η`.
- Builds directly on **RE-05** (Minkowski spacetime) for η and the invariant
  interval.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 5 (tensor calculus) —
  `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 2 §§2.6–2.12 (Lorentz tensors) —
  `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
- *(Both PDFs are scanned images with no extractable text, so page numbers are not
  cited — same policy as the rest of the RE/MA trunks.)*
