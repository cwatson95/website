# RE-15 — References

Page-level citations **verified by reading the page text** (PyMuPDF) in the PDFs
under `books/library/`. **Printed** = the number printed on the page; **PDF** = the
viewer page index. Offsets were checked against the page text, not assumed.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| Dodelson, *Modern Cosmology* (1st ed., 2003) | `RE_Relativity_Cosmology/ModernCosmologySD.pdf` | PDF = printed **+ 15** |

The Dodelson offset **+15** was determined here: Ch. 2 *The Smooth, Expanding
Universe* opens on **PDF 38** (printed 23), and the folios "24, 25, 26, …" on the
following pages sit on PDF 39, 40, 41, … (printed + 15). It is consistent at Ch. 5
*Einstein Equations*, which opens **PDF 132** (printed 117), with folio "118" on
PDF 133. (`ModernCosmologySD.pdf` is text-extractable; the scan’s OCR is noisy, so
section titles and equation numbers were read directly off each cited page.)

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| cosmological principle ⇒ universe-as-one-equation (`flrw_metric`) | Zee | §VI.2 *To Cosmology as Quickly as Possible* | 355 | 378 |
| FLRW metric `diag(−1,a²,a²,a²)` (`flrw_metric`) | Dodelson | Eq. (2.4) | 26 | 41 |
| Einstein eqs `G_{μν}=R_{μν}−½g_{μν}R=8πGT_{μν}` (`G00_from_flrw`) | Dodelson | §2.1.3 *Einstein Equations*, Eq. (2.30) | 32 | 47 |
| Friedmann eq. from time–time Einstein `3ȧ²/a²=8πGρ`; critical density `ρ_cr=3H₀²/8πG` (`friedmann_1_residual`, `critical_density`) | Dodelson | Eqs. (2.38)–(2.40) | 33 | 48 |
| cosmological redshift / comoving distance (`redshift`) | Dodelson | §2.2 *Distances*, Eq. (2.41) | 34 | 49 |
| the dynamic universe; Friedmann equations & eras (`friedmann_2_residual`, eras) | Zee | §VIII.1 *The Dynamic Universe* | 489 | 512 |
| "the Friedmann equation (1.2)" named (`friedmann_1_residual`) | Dodelson | Exercise 5 (Ch. 3) | 82 | 97 |
| Einstein tensor `G_{μν}` implementation | — see **RE-11** `curvature` (`einstein_tensor` → MA-17 finite-difference Riemann/Ricci) | — | — | — |

## Cross-module dependency
Imports **RE-11** (`modules/RE/RE-11_curvature/code/curvature.py`) for
`einstein_tensor` (which in turn imports MA-17’s finite-difference curvature). The
**headline result is validated numerically**: handing `flrw_metric` to
`einstein_tensor` reproduces `G₀₀ = 3[(ȧ/a)² + k/a²]` — confirmed for de Sitter
(`G₀₀ → 3H²`), matter (`G₀₀ → 3(2/3t)²`) and both curved cases `k=±1` to ∼1–2%.

## Further reading (not page-verified — image-only scans, no usable text layer)
- d’Inverno, *Introducing Einstein’s Relativity*, Ch. 22–23 (cosmology, FLRW,
  Friedmann models) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Chs. 14–15 (cosmology) —
  `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
