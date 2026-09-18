# EM-08 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (e.g. PDF p.228 carries printed "210", the
start of Chapter 5). Griffiths is the worked source for the whole EM-01..EM-10 sequence;
Jackson 3e and Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| magnetic fields (intro) | §5.1.1 *Magnetic Fields* | 210 | 228 |
| Lorentz force **F**=Q(**v**×**B**) (`lorentz_force`) | §5.1.2 *Magnetic Forces* (Eq. 5.1) | 212 | 230 |
| force on a wire **F**=∫I d**l**×**B** (`force_on_wire`) | §5.1.3 *Currents* (Eq. 5.16) | 216 | 234 |
| Biot–Savart law (`biot_savart`, `circular_loop_field`) | §5.2.2 *Magnetic Field of a Steady Current* (Eq. 5.39) | 224 | 242 |
| infinite wire B=μ₀I/2πs (`infinite_wire_field`) | §5.2.2 (Eq. 5.36) | 224 | 242 |
| on-axis loop field (`loop_axis_field_closed`) | §5.2.2 (Ex. 5.6, Eq. 5.41) | 224 † | 242 † |
| ∇·**B** = 0 (`div_B_residual`) | §5.3.2 *The Divergence and Curl of B* (Eq. 5.50) | 231 | 249 |
| ∇×**B** = μ₀**J** | §5.3.2 (Eq. 5.56) | 231 | 249 |
| Ampère's law ∮**B**·d**l**=μ₀I_enc (`ampere_circulation`) | §5.3.3 *Ampère's Law* (Eq. 5.57) | 233 | 251 |

† Eq. 5.41 (on-axis loop, Ex. 5.6) sits inside §5.2.2; the citation map fixes that section
at printed p.224 (PDF 242) but does not separately verify the example's own page.

## See also
- `~MA-01` for `cross`/`dot`/`norm` — `cross` is the engine of `lorentz_force`,
  `force_on_wire`, and `biot_savart`.
- `~MA-02` for `line_integral` (the Ampère circulation) and `divergence` (the ∇·**B** = 0
  check), which act on the **B** field functions directly. Griffiths reviews this vector
  calculus in Ch. 1.
- `~EM-09` (vector potential) and `~EM-10` (magnetic materials, **H**) build on this
  field; `~EM-11`/`~EM-13` add time dependence.
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 5 *Magnetostatics*
  (`EM/Jackson…SolutionManual…pdf` holds solutions only locally); Schwinger, *Classical
  Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
