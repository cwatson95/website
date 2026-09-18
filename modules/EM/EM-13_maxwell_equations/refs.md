# EM-13 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was re-confirmed in the Ch. 7–12 range against the page text (e.g. PDF p.352
carries printed "334", the displacement-current page; PDF p.374 carries printed "356", the
continuity equation). Griffiths is the worked source for the whole EM-11..EM-18 sequence;
Jackson 3e and Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| displacement current (`displacement_current_density`) | §7.3.2 *How Maxwell Fixed Ampère's Law* (Eq. 7.38) | 334 | 352 |
| the four equations (`gauss_E_residual`, `gauss_B_residual`, `faraday_residual`, `ampere_maxwell_residual`, `verify_vacuum_plane_wave`) | §7.3.3 *Maxwell's Equations* (Eqs. 7.39–7.42) | 337 | 355 |
| Maxwell's equations in matter (**D**, **H**) | §7.3.5 *Maxwell's Equations in Matter* | 340 | 358 |
| boundary conditions | §7.3.6 *Boundary Conditions* | 342 | 360 |
| speed of light from constants (`C_SI`) | §7.3.3 → vacuum wave, $c=1/\sqrt{\mu_0\varepsilon_0}$ | 337 | 355 |
| vacuum plane wave (`plane_wave_fields`) | §9.2.2 *Monochromatic Plane Waves* (test vehicle, `~EM-15`) | 394 | 412 |
| continuity ∂ρ/∂t + ∇·**J** = 0 (bridge to `~EM-14`) | §8.1.1 *The Continuity Equation* (Eq. 8.4) | 356 | 374 |

## See also
- `~EM-01` for `EPS0` (ε₀) and `~EM-08` for `MU0` (μ₀) — the two constants whose product is
  $1/c^2$; their measured values are what make `C_SI` come out to the speed of light.
- `~MA-02` for `divergence`/`curl`, which the four residual functions call on the time-slices
  of the fields (the §7.3.3 structure checks). Griffiths reviews this vector calculus in Ch. 1.
- `~EM-11` (Faraday's law, ∇×**E** = −∂**B**/∂t) supplies the third equation; `~EM-14`
  (Poynting / conservation) and `~EM-15` (EM waves) build directly on the four; `~EM-18`
  recasts them covariantly as $\partial_\mu F^{\mu\nu}=\mu_0 J^\nu$.
- `~CM-22` for the continuity equation as **mass** conservation (**KEY BRIDGE B2**).
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, **Ch. 6** (Maxwell
  equations, macroscopic electromagnetism, conservation laws, gauge); Schwinger,
  *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
