# EM-09 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (PDF p.261 carries printed "243",
the start of §5.4 *The Vector Potential*). Griffiths is the worked source for the
whole EM-01..EM-10 sequence; Jackson 3e and Schwinger sit at a higher level (see
*See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| vector potential, **B** = ∇×**A** (`B_from_A`) | §5.4.1 *The Vector Potential* (Eq. 5.59) | 243 | 261 |
| Coulomb gauge ∇·**A**=0, ∇²**A**=−μ₀**J** (`coulomb_gauge_residual`) | §5.4.1 (Eqs. 5.59–5.63) | 243 | 261 |
| infinite-wire potential (`wire_vector_potential`) | §5.4.1 (worked example) | 243 | 261 |
| boundary conditions on **A** | §5.4.2 *Boundary Conditions* | 249 | 267 |
| magnetic moment **m** = I∫d**a** (`magnetic_dipole_moment`) | §5.4.3 *Multipole Expansion of the Vector Potential* (Eq. 5.86) | 252 | 270 |
| dipole potential A_dip (`dipole_vector_potential`) | §5.4.3 (Eq. 5.85) | 252 | 270 |
| dipole field B_dip (`dipole_B_field_closed`) | §5.4.3 (curl of Eq. 5.85) | 252 | 270 |

The explicit dipole **field** B_dip = (μ₀/4π)(1/r³)[3(**m**·**r̂**)**r̂** − **m**] is
the curl of Eq. 5.85, derived in the same subsection (§5.4.3); only the §5.4.3
section start (p.252) is page-verified here. Its electric counterpart is `~EM-05`
Eq. 3.104 (printed p.158) — the same formula under (1/4πε₀, **p**) → (μ₀/4π, **m**).

## See also
- `~EM-08` for `MU0` and `infinite_wire_field` — the wire **B** that
  `wire_vector_potential` must curl back to — and the ∇·**B** = 0 result that makes
  a vector potential possible in the first place.
- `~MA-02` for `curl`/`divergence`, applied straight to the potential functions
  (`B_from_A`, `coulomb_gauge_residual`). Griffiths reviews this vector calculus in
  Ch. 1.
- `~EM-05` the electric-dipole analogue: A_dip ↔ V_dip and B_dip ↔ E_dip under
  (1/4πε₀, **p**) → (μ₀/4π, **m**).
- `~QF-03` gauge invariance — the field-theory descendant of the **A** → **A** + ∇λ
  freedom (KEY BRIDGE B8: MA-18 → CM-18 → QF-03).
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 5
  (vector potential & magnetic dipole; `EM/Jackson…SolutionManual…pdf` holds
  solutions only locally); Schwinger, *Classical Electrodynamics*
  (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
