# RE-13 — References

Page-level citations **verified by reading the page text** (PyMuPDF) in the PDFs
under `books/library/`. **Printed** = the number on the page; **PDF** = the viewer
page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| C. Pope, *Geometry & General Relativity lecture notes* | `RE_Relativity_Cosmology/cpope_notes.pdf` | cite by **PDF page + section** (folios not rendered) |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| the metric *is* the gravitational field; curved spacetime | Zee | §V.3 *The Universe as a Curved Spacetime* | 288 | 311 |
| weak-field geodesics → Newton; `g_00=−(1+2Φ)` (`newtonian_poisson_residual`) | Zee | §V.4 *Motion in Curved Spacetime* (`Γ^i_{00}≈½∂_ih_{00}`) | 303 | 326 |
| perfect-fluid energy-momentum tensor `ρ,p` (`stress_energy_perfect_fluid`) | Zee | §III.6 *Completion, Promotion, and the Nature of the Gravitational Field* (Eq. 18) | 231 | 254 |
| the field equation `G_μν=8πT_μν`; curvature from `[D_μ,D_ν]`; the Einstein tensor as LHS (`field_equation_residual`) | Zee | §VI.1 *To Einstein's Field Equation as Quickly as Possible* (weak field `g=η+h`, p. 339) | 337 | 360 |
| `T_μν` as the source that "tells spacetime how to curve" (`einstein_tensor`) | Zee | §VI.4 *Energy Momentum Distribution Tells Spacetime How to Curve* | 378 | 401 |
| the Newtonian limit **fixes the coupling** (`G_N`/`8π`) (`newtonian_poisson_residual`) | Zee | §VI.5 *Gravity Goes Live* — "The Newtonian limit" | 391 | 414 |
| construction of the stress-energy tensor `T^{μν}` | cpope | §2 (momentum density/current → 2-tensor) | — | 25 |
| geodesic Newtonian limit `d²x^i/dt²=½∂_ih_{00}`, `h_{00}=−2Φ` | cpope | §5.5 *Geodesic motion in the Newtonian limit* | — | 66–67 |
| derivation of `G_μν=8πT_μν`; `∇_μT^{μν}=0` ↔ charge conservation analogy (`trace_reversed_ricci`) | cpope | §6.1 *Derivation of the Einstein equations* | — | 68–69 |
| cosmological constant `R_μν−½Rg_μν+Λg_μν=0` from the Λ-action (`field_equation_residual`, `Lambda`) | cpope | §7 (Einstein–Hilbert + Λ), **Eq. 7.15** | — | 88 |

## Cross-module dependency
**Imports RE-11** (`modules/RE/RE-11_curvature/code/curvature.py`) for the geometry
side — `einstein_tensor`, `ricci`, and the `minkowski`/`schwarzschild` reference
metrics (RE-11 in turn imports MA-17 for the finite-difference Riemann/Ricci). This
module adds the **matter** side: the stress-energy tensor, the trace-reversed
equation, the field-equation residual (with `Λ`), the de Sitter Λ-vacuum, and the
Newtonian limit. Validated by reproducing `G_μν=0` for Schwarzschild, `G_μν+Λg_μν=0`
for de Sitter (`Λ=3/L²`), and `G_{00}=2∇²Φ` in the weak field.

The canonical **field** stress-energy tensor (electromagnetic
`T_{μν}=F_{μα}F_ν{}^α−¼g_{μν}F²`) is the subject of **~EM-14** — forward-referenced
in `notes.md` §4, **not** imported.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 10–11 (the field equations,
  the energy-momentum tensor) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 7 (Einstein's field equations) —
  `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
- *(Both PDFs are scanned images with no extractable text, so page numbers are not
  cited — same policy as RE-11.)*
