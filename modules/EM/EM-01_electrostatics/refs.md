# EM-01 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (e.g. PDF p.77 carries printed "59",
the start of Chapter 2). Griffiths is the worked source for the whole EM-01..EM-10
sequence; Jackson 3e and Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| Coulomb's law (`K_E`, `EPS0`) | §2.1.2 *Coulomb's Law* (Eq. 2.1) | 60 | 78 |
| electric field, **F**=Q**E** (`force_on_charge`) | §2.1.3 *The Electric Field* (Eq. 2.3) | 61 | 79 |
| field of point charges, superposition (`point_charge_field`, `coulomb_field`) | §2.1.3 (Eq. 2.4) | 61 | 79 |
| field magnitude / direction (`field_magnitude`, `field_line_direction`) | §2.1.2–2.1.3 | 60–61 | 78–79 |
| continuous distributions (`field_of_distribution`) | §2.1.4 *Continuous Charge Distributions* (Eq. 2.8) | 63 | 81 |
| curl-free / divergence structure (bridge to ~EM-02) | §2.2.2 *The Divergence of E*, §2.2.4 *The Curl of E* | 71, 77 | 89, 95 |

## See also
- `~MA-01` for `norm`/`unit`/`dot`, reused by `field_magnitude`, `field_line_direction`.
- `~MA-02` for `curl`/`divergence`, which act on the EM field functions directly
  (the §2.2 structure checks). Griffiths reviews this vector calculus in Ch. 1.
- `~EM-02` (Gauss), `~EM-03` (potential), `~EM-05` (multipole), `~EM-06` (energy)
  all build on this field.
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 1
  (`EM/Jackson…SolutionManual…pdf` holds solutions only locally); Schwinger,
  *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
