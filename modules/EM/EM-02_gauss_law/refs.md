# EM-02 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (e.g. PDF p.77 carries printed "59", the
start of Chapter 2); §2.2 then runs printed pp.66–77 = PDF pp.84–95. Griffiths is the
worked source for the whole EM-01..EM-10 sequence; Jackson 3e and Schwinger sit at a
higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| flux & integral Gauss's law (`flux_through_sphere`, `enclosed_charge`, `sphere_surface`) | §2.2.1 *Field Lines, Flux, and Gauss's Law* (Eq. 2.13) | 66 | 84 |
| divergence / local form (`gauss_residual`) | §2.2.2 *The Divergence of E* (Eq. 2.16) | 71 | 89 |
| symmetry fields — sphere/line/plane (`uniform_sphere_field`, `line_charge_field`, `plane_sheet_field`) | §2.2.3 *Applications of Gauss's Law* | 71 | 89 |
| curl of **E** (bridge to `~EM-03`) | §2.2.4 *The Curl of E* (Eq. 2.19) | 77 | 95 |

## See also
- `~MA-02` supplies `surface_flux` (the flux integral ∮**E**·d**a**) and `divergence`
  (the local form ∇·**E**), used directly by `flux_through_sphere` and `gauss_residual`;
  Griffiths reviews the divergence theorem and this vector calculus in Ch. 1.
- `~EM-01` provides the field **E** that is integrated here.
- Downstream: `~EM-03` (potential, Poisson/Laplace), `~EM-06` (conductors &
  electrostatic energy), `~EM-07` (Gauss's law for the **D** field in dielectrics) all
  build on Gauss's law.
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 1
  (`EM/Jackson…SolutionManual…pdf` holds solutions only locally); Schwinger,
  *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
