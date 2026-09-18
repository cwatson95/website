# EM-14 — References

Page-level citations taken from the verified Griffiths Ch. 7–12 map (printed pages
confirmed by page text). **Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset (PDF = printed + 18) is the one used across `~EM-01..EM-18`; e.g. printed p.356
(the continuity equation) sits at PDF p.374. Griffiths Ch. 8 is the worked source for this
module; Jackson 3e and Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| continuity equation, ∂ρ/∂t+∇·**J**=0 (KEY BRIDGE B2) | §8.1.1 *The Continuity Equation* (Eq. 8.4) | 356 | 374 |
| energy density u (`energy_density`) | §8.1.2 *Poynting's Theorem* (Eq. 8.13) | 357 | 375 |
| Poynting vector **S** (`poynting_vector`) | §8.1.2 (Eq. 8.10) | 358 | 376 |
| Maxwell stress tensor T_ij (`maxwell_stress_tensor`) | §8.2.2 *Maxwell's Stress Tensor* (Eq. 8.19) | 362 | 380 |
| field momentum **g**, radiation pressure (`momentum_density`, `radiation_pressure`) | §8.2.3 *Conservation of Momentum* (Eq. 8.29–8.30) | 366 | 384 |
| plane wave B₀=E₀/c (`plane_wave_snapshot`) | §9.2.2 *Monochromatic Plane Waves* (Eq. 9.49) — forward ref, `~EM-15` | 394 | 412 |

All §8 pages are from the verified map. The plane-wave constructor `plane_wave_snapshot`
properly belongs to `~EM-15`; it appears here only as the canonical example in which the
densities collapse to $S=cu$ and $g=u/c$.

## See also
- `~EM-01` for `EPS0` (ε₀) and the field convention, `~EM-08` for `MU0` (μ₀); the code
  imports both, and `C` = 1/√(μ₀ε₀) is built from them.
- `~MA-01` for `cross`/`dot`/`norm`, which act on the EM field functions directly
  (`poynting_vector` is just `cross(E, B)/μ₀`).
- `~EM-06` for the electrostatic energy ½ε₀E² — the $u_E$ piece of the energy density here.
- Downstream: `~EM-15` (waves: ⟨S⟩, radiation pressure) and `~EM-17` (radiated power).
- `~CM-22` for the same continuity equation as mass conservation (**KEY BRIDGE B2**).
- Higher level: Jackson, *Classical Electrodynamics* 3e, **Ch. 6** (conservation laws —
  Poynting's theorem, the Maxwell stress tensor, field momentum); Schwinger, *Classical
  Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
