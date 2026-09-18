# EM-18 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was re-confirmed against the page text across Ch. 12 (e.g. PDF p.568
carries printed "550", the start of §12.3.1). Griffiths is the worked source for
the whole EM-01..EM-18 sequence; Jackson 3e and Schwinger sit at a higher level
(see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| magnetism as relativity (motivation) | §12.3.1 *Magnetism as a Relativistic Phenomenon* | 550 | 568 |
| field transformation (`boost_fields`) | §12.3.2 *How the Fields Transform* (Eq. 12.108–12.109) | 553 | 571 |
| the field tensor (`field_tensor`, `fields_from_tensor`, `is_antisymmetric`) | §12.3.3 *The Field Tensor* (Eq. 12.118–12.119) | 562 | 580 |
| Lorentz invariants (`field_invariants`) | §12.3.3, Prob. 12.47 | 562 | 580 |
| covariant Maxwell ∂_μF^{μν} = μ₀J^ν | §12.3.4 *Electrodynamics in Tensor Notation* (Eq. 12.127–12.128) | 565 | 583 |
| Lorentz factor γ (`gamma`), c = 1/√(μ₀ε₀) (`C`) | §12.1 *The Special Theory of Relativity* | — | — |

The γ / c row lives in §12.1 (the relativity primer); the citation map for this
module covers §12.3 only, so it is cited at section level without a verified page.

## See also
- `~EM-01` (`EPS0`) and `~EM-08` (`MU0`) supply `C` = 1/√(μ₀ε₀); `~MA-01` (`dot`)
  is reused by `field_invariants`.
- `~MA-16` for tensor / index notation (covariant vs contravariant, the metric
  η_{μν} that lowers F^{μν}); `~RE-08` for the covariant formulation of special
  relativity, which re-derives this module's tensors from the relativity side.
- `~QF-03` (gauge theories / QED), where F^{μν} = ∂^μA^ν − ∂^νA^μ is the field
  strength of the `~EM-09` four-potential.
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 11
  (*Special Theory of Relativity*) — the field tensor and covariant Maxwell are
  §11.9–11.10; Schwinger, *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
