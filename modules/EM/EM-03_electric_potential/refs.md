# EM-03 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (PDF p.96 carries printed "78", the start
of §2.3, *Electric Potential*). Griffiths §2.3 is the worked source for this module;
Jackson 3e and Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| V from the field (`potential_from_field`); E from V (`field_from_potential`) | §2.3.1 *Introduction to Potential* (Eq. 2.21, 2.23) | 78 | 96 |
| reference point / additive constant, units (volts) | §2.3.2 *Comments on Potential* | 80 | 98 |
| Poisson & Laplace (`poisson_residual`) | §2.3.3 *Poisson's & Laplace's Equation* (Eq. 2.24–2.25) | 83 | 101 |
| potential of charges (`potential_of_charge`, `potential_point_charges`) | §2.3.4 *Potential of a Localized Charge Distribution* (Eq. 2.29) | 84 | 102 |
| boundary conditions (bridge to ~EM-04) | §2.3.5 *Boundary Conditions* (Eq. 2.31–2.33) | 88 | 106 |

## See also
- `~MA-02` for `gradient`/`line_integral`/`laplacian` — the three operators that connect
  V and **E** (**E** = −∇V, V = −∫**E**·d**l**, ∇²V). Griffiths reviews this vector
  calculus in Ch. 1.
- `~EM-01` for `point_charge_field`/`coulomb_field`, the fields this module integrates
  and reproduces, and for `EPS0`/`K_E`.
- `~MA-08` (PDEs: wave/heat/Laplace, separation of variables) and `~MA-14` (Green's
  functions) — the math behind Poisson/Laplace and the boundary-value problems of
  `~EM-04`.
- Downstream: `~EM-04` (boundary-value problems), `~EM-05` (multipole expansion of V),
  `~EM-06` (electrostatic energy).
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 1–2
  (`EM/Jackson…SolutionManual…pdf` holds solutions only locally); Schwinger,
  *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
