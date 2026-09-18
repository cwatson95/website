# EM-04 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (e.g. PDF p.137 carries printed
"119", the start of §3.1.5). Everything in this module sits in **Chapter 3**
(*Potentials*), §3.1–3.3; Jackson 3e and Schwinger sit at a higher level (see
*See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| first uniqueness theorem (`solve_laplace_2d`) | §3.1.5 *Boundary Conditions and Uniqueness Theorems* | 119 | 137 |
| first-theorem **proof** ($V_3$ difference, no-extrema squeeze) + Example 3.1 (cavity) | §3.1.5 (proof paragraph) | 120 | 138 |
| **Poisson corollary** ($\nabla^2V_3=-\rho/\varepsilon_0+\rho/\varepsilon_0=0$; $\rho$ + boundary $V$ fix $V$) | §3.1.5 (end) | 121 | 139 |
| second uniqueness theorem (conductors) | §3.1.6 *Conductors and the Second Uniqueness Theorem* | 121 | 139 |
| second-theorem setup: per-conductor Gauss integrals; $\nabla\!\cdot\!\mathbf E_3=0$, $\oint\mathbf E_3\!\cdot d\mathbf a=0$ (Eqs. 3.7–3.8) | §3.1.6 | 122 | 140 |
| second-theorem **proof**: $\nabla\!\cdot\!(V_3\mathbf E_3)=-(E_3)^2$, divergence theorem, $\int(E_3)^2d\tau=0$; Purcell warning example | §3.1.6 (end) | 123 | 141 |
| image potential / field (`image_potential_plane`, `image_field_plane`) | §3.2.1 *The Classic Image Problem* (Eq. 3.9) | 124 | 142 |
| induced surface charge (`induced_surface_charge`, `total_induced_charge`) | §3.2.2 *Induced Surface Charge* (Eq. 3.10) | 125 | 143 |
| image force (`image_force`) | §3.2.3 *Force and Energy* (Eq. 3.12) | 126 | 144 |
| slot: Fourier series + closed form (`slot_potential_series`, `slot_potential_closed`) | §3.3.1 *Separation of Variables — Cartesian* (Eqs. 3.34, 3.36) | 131 | 149 |
| spherical separation, Legendre series (→ `~EM-05`) | §3.3.2 *Separation of Variables — Spherical* (Eqs. 3.65–3.66) | 141 | 159 |

## See also
- `~EM-01` (the field, `coulomb_field`) and `~EM-03` (the potential,
  `potential_point_charges`, and Laplace/Poisson) — `boundary_value.py` imports
  both directly; the image method is built entirely from them.
- `~MA-08` for the Laplace PDE and separation of variables, and `~MA-11` for
  Sturm–Liouville theory — the orthogonal eigenfunctions and completeness that
  fix the Fourier coefficients in §3.3.1.
- Downstream `~EM-05` (multipole expansion): the spherical-separation Legendre
  series of §3.3.2 *is* the multipole series; the special functions are `~MA-12`.
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 2
  (boundary-value problems, images) and Ch. 3 (separation of variables in
  spherical/cylindrical coordinates); Schwinger, *Classical Electrodynamics*
  (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
