# MA-16 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

All in **Chapter 10, Tensor Analysis** (opens printed p.496 / PDF 515).

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| index notation; the summation convention (`matvec`, contractions) | §3 *Tensor Notation and Operations* | 502 | 521 |
| inertia tensor (the rank-2 example, `~CM-13`) | §4 *Inertia Tensor* | 505 | 524 |
| Kronecker δ, Levi-Civita ε, ε–δ identity (`levi_civita_symbol`, `cross_via_levi_civita`, `det_levi_civita`) | §5 *Kronecker Delta and Levi-Civita Symbol* | 508 | 527 |
| pseudovectors / pseudotensors | §6 *Pseudovectors and Pseudotensors* | 514 | 533 |
| the metric in curvilinear coordinates (`metric_from_map`) | §8 *Curvilinear Coordinates* | 521 | 540 |
| non-Cartesian tensors; covariant/contravariant & the metric (`lower_index`, `raise_index`, `inner`) | §10 *Non-Cartesian Tensors* | 529 | 548 |

## Notes (verified)
- Boas's Ch.10 is the natural home of MA-16: §5 (p.508) gives δ and ε; §10 (p.529)
  introduces non-Cartesian tensors and the **metric** that distinguishes
  covariant from contravariant components — the conceptual core of the module.
- The ε–δ identity is stated within §5 (printed p.508–513); the exact sub-page is
  not pinned here because Boas's subscript glyphs do not extract cleanly as text.
- The metric-from-Jacobian construction g=JᵀJ is the tensor-analysis restatement
  of the scale factors / line element of `~MA-03` (Boas §8, p.521).
- Marion & Thornton Ch.11 (inertia tensor) and any SR text (Minkowski metric) give
  the physics applications; pinned in `~CM-13` / `~RE-08` when built.
