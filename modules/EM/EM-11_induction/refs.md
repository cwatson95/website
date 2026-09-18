# EM-11 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was re-confirmed in this range against the page text (e.g. PDF p.330
carries printed "312", the start of §7.2.1 Faraday's Law). Griffiths is the worked
source for the whole EM-01..EM-18 sequence; Jackson 3e and Schwinger sit at a
higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| electromotive force (the EMF concept) | §7.1.2 *Electromotive Force* | 303 | 321 |
| motional emf, EMF = B v L (`motional_emf`) | §7.1.3 *Motional emf* | 305 | 323 |
| the flux rule, EMF = −dΦ/dt | §7.1.3 (flux rule) | 313 | 331 |
| Faraday's law & Lenz (`faraday_emf`, `lenz_sign`, `magnetic_flux`, `flat_loop_surface`) | §7.2.1 *Faraday's Law* | 312 | 330 |
| induced electric field, ∇×**E** = −∂**B**/∂t (Eq. 7.18) | §7.2.2 *The Induced Electric Field* | 317 | 335 |
| inductance, Φ = L I (`solenoid_inductance`, `mutual_inductance_solenoids`) (Eq. 7.27–7.28) | §7.2.3 *Inductance* | 321 | 339 |
| energy in **B** (`energy_in_inductor`, `magnetic_energy_density`, `magnetic_field_energy_solenoid`) (Eq. 7.34–7.35) | §7.2.4 *Energy in Magnetic Fields* | 328 | 346 |

## See also
- `~EM-08` for `MU0` and the **B** field, reused by every flux, inductance, and
  energy formula here.
- `~MA-02` for `surface_flux`, reused verbatim as `magnetic_flux` (and
  `flat_loop_surface` builds the surface it integrates over). Griffiths reviews
  this vector calculus in Ch. 1.
- Downstream: `~EM-12` (AC circuits — `L` in a driven loop), `~EM-13` (Maxwell —
  the induced-**E** law becomes one of the four equations).
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 5
  (magnetostatics, Faraday's law & quasi-static fields); Schwinger, *Classical
  Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
