# MA-17 — References

Page-level citations **verified by reading the page text** in the PDFs.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Warner, *Foundations of Differentiable Manifolds and Lie Groups* (GTM 94) | `MA_Mathematics/warner_diff_man_lie_groups.pdf` | PDF = printed **+ 10** |
| de Rham, *Differentiable Manifolds* (Grundlehren 266) | `MA_Mathematics/deRhamDiffManifolds.pdf` | PDF = printed **+ 9** |
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

(PDF = 1-based viewer page. For PyMuPDF use `load_page(PDF − 1)`.)

### Forms & the exterior derivative
| Topic (code symbol) | Book — section / title | Printed p. | PDF p. |
|---|---|---|---|
| tangent vectors / tangent space | Warner §1.14 *Tangent Vectors and Differentials* | 13 | 23 |
| tensors & differential forms (`gradient`/`curl`/`divergence` as d) | Warner §2 *Tensors and Differential Forms* | 56 | 66 |
| the exterior derivative (d²=0) | Warner *exterior derivative … d* | 65 | 75 |
| differentiable manifold (definition) | de Rham Ch I §1 | 3 | 12 |
| differential forms | de Rham Ch II §4 *Differential Forms* | 15 | 24 |
| differential (exterior derivative) of a form | de Rham §4 *the differential dα* | 17 | 26 |

### Metric & tensors (the curvature inputs)
| Topic | Book — section / title | Printed p. | PDF p. |
|---|---|---|---|
| the metric tensor; non-Cartesian tensors (`christoffel` input) | Boas Ch.10 §10 *Non-Cartesian Tensors* | 529 | 548 |

## Curvature — honest note
The **Christoffel/Riemann/Ricci** machinery (`christoffel`, `riemann`, `ricci`,
`gaussian_curvature_2d`) is **general-relativity** material; on this shelf its full
treatment lives in the GR texts (Weinberg, d'Inverno) under trunk **`~RE-09`…`~RE-13`**,
not in the differential-geometry math books above (Warner/de Rham develop forms and
manifolds, not Riemannian curvature at this level). The formulas used are the
standard Levi-Civita ones; the **Theorema Egregium** result (sphere K=1/a², plane
K=0) is self-validating against the exact answers, independent of any page citation.

## Notes (verified)
- Warner offset (+9) and de Rham offset (+8) were each cross-checked against an
  index/running-head entry ("exterior derivative, 65"; "§8 Definition of Currents
  / 35").
- de Rham §4 (p.15–17) is the clean source for "a differential form and its
  exterior derivative"; Warner §2 (p.56, with d on p.65) is the tensor-bundle
  version. Both give d²=0.
- The numerical curvature uses nested central differences of a callable metric; the
  sphere/plane checks pin K to ~1 % despite the double differentiation.
