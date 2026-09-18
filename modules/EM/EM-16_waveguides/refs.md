# EM-16 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was re-confirmed in the Ch. 9 range by the page text (PDF p.443 carries
printed "425", the start of §9.5 *Wave Guides*). Griffiths is the worked source for
the whole EM-01..EM-18 sequence; Jackson 3e and Schwinger sit at a higher level
(see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| guided waves, boundary conditions, TE/TM/TEM | §9.5.1 *Wave Guides* | 425 | 443 |
| TE_mn cutoff ω_mn (`cutoff_angular_frequency`, `cutoff_frequency`, `dominant_mode_cutoff`) | §9.5.2 *TE Waves in a Rectangular Wave Guide* (Eq. 9.186) | 428 | 446 |
| guide wavenumber & evanescence (`guide_wavenumber`, `evanescent_decay`, `is_propagating`) | §9.5.2 (Eq. 9.186) | 428 | 446 |
| phase / group velocity, v_p·v_g = c² (`phase_velocity_guide`, `group_velocity_guide`) | §9.5.2 | 428 | 446 |
| coaxial TEM line (`tem_line_speed`) | §9.5.3 *The Coaxial Transmission Line* | 431 | 449 |

Note: the dispersion and $v_p,v_g$ results occupy the back half of §9.5.2, running
to just before §9.5.3 (p.431); the verified anchor for the section is p.428
(Eq. 9.186). Only the cutoff equation page is page-verified — the velocity
discussion is cited at section level against that anchor.

## See also
- `~EM-15` for the free-space wave and the speed `C` (`em_waves`), reused by every
  velocity here — a guide is `~EM-15` plus a cutoff.
- `~MA-08` (PDE / separation of variables): the transverse mode pattern is a 2-D
  Helmholtz eigenvalue problem on the guide cross-section; the cutoffs are its
  eigenvalues.
- `~QO-01` reuses the guide/cavity **mode** idea when it counts and quantizes the
  electromagnetic modes of a box.
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 8
  *Waveguides, Resonant Cavities, and Optical Fibers* (`EM/Jackson…SolutionManual…pdf`
  holds solutions only locally); Schwinger, *Classical Electrodynamics*
  (`EM_Electricity_Magnetism/SchwingerEM.pdf`), waveguides & cavities.
