# EM-10 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (e.g. PDF p.291 carries printed
"273", the start of §6.1.4 *Magnetization*). Griffiths is the worked source for
the whole EM-01..EM-10 sequence; Jackson 3e and Schwinger sit at a higher level
(see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| magnetization **M** | §6.1.4 *Magnetization* | 273 | 291 |
| bound currents (`bound_volume_current`, `bound_surface_current`) | §6.2.1 *Bound Currents* (Eq. 6.13–6.14) | 274 | 292 |
| uniformly magnetized sphere (`magnetized_sphere_inner_B`, `magnetized_sphere_inner_H`) | §6.2.1 *The Field of a Magnetized Object* (Ex. 6.1, Eq. 6.16) | 274 † | 292 † |
| auxiliary field **H**, Ampère in matter (`auxiliary_field_H`) | §6.3.1 *Ampère's Law in Magnetized Materials* (Eq. 6.18, 6.20) | 279 | 297 |
| susceptibility & permeability (`magnetization_linear`, `permeability`, `B_linear`, `classify_material`) | §6.4.1 *Magnetic Susceptibility and Permeability* (Eq. 6.29, 6.31, 6.33) | 284 | 302 |
| ferromagnetism & hysteresis (`hysteresis_branches`, `remanence`, `coercivity`) | §6.4.2 *Ferromagnetism* | 288 | 306 |

† The uniformly magnetized-sphere example (Ex. 6.1, **B**_in = ⅔μ₀**M**, the code's
Eq. 6.16; **H**_in = −**M**/3 follows from Eq. 6.18) sits within §6.2 just past the
p.274 heading. The citation map verifies the **section anchor** (§6.2.1, p.274),
not the example's own page — cited at section level.

## See also
- `~EM-08` for `MU0` and the magnetostatic laws (∇×**B** = μ₀**J**, Ampère),
  reused throughout; the H-form ∮**H**·d**l** = I_f,enc is the in-matter version.
- `~MA-01` for `cross` (used by `bound_surface_current` = **M**×n̂) and `norm`;
  `~MA-02` for `curl` (used by `bound_volume_current` = ∇×**M**). Griffiths reviews
  this vector calculus in Ch. 1.
- `~EM-07` (dielectrics / the **D** field) — the electric analogue, developed
  section-for-section: **P** ↔ **M**, bound charge ↔ bound current, **D** ↔ **H**
  (Griffiths Ch. 4 ↔ Ch. 6).
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, **Ch. 5**
  (*Magnetostatics, Faraday's Law, Quasi-Static Fields* — incl. magnetic materials
  and **H**; `EM/Jackson…SolutionManual…pdf` holds solutions only locally);
  Schwinger, *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
