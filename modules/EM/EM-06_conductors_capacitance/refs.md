# EM-06 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (e.g. PDF p.109 carries printed "91",
the start of §2.4.1). Griffiths is the worked source for the whole EM-01..EM-10
sequence; Jackson 3e and Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| work to move a charge (notes §1) | §2.4.1 *The Work It Takes to Move a Charge* (Eq. 2.39, W = QV) | 91 | 109 |
| assembly energy, charge picture (`work_to_assemble`) | §2.4.2 *Energy of a Point Charge Distribution* (Eq. 2.42) | 92 | 110 |
| field energy (`field_energy`, `field_energy_density`, `field_energy_spherical`, `self_energy_uniform_sphere`) | §2.4.3 *Energy of a Continuous Charge Distribution* (Eq. 2.45; uniform sphere, Ex. 2.9) | 94 | 112 |
| conductor properties (notes §4) | §2.5.1 *Basic Properties* | 97 | 115 |
| surface charge & pressure (`surface_pressure`) | §2.5.3 *Surface Charge and the Force on a Conductor* (Eq. 2.51) | 103 | 121 |
| capacitance & stored energy (`capacitance_parallel_plate`, `capacitance_isolated_sphere`, `capacitance_spherical`, `capacitance_cylindrical`, `energy_stored`) | §2.5.4 *Capacitors* (Eq. 2.53 C = Q/V; Eq. 2.54 C = ε₀A/d; Eq. 2.55 W = ½CV²; geometries, Ex. 2.11) | 105 | 123 |

Example-level pages (Ex. 2.9, Ex. 2.11) are quoted at their section's verified
printed page; the citation map fixes section starts, not individual examples.

## See also
- `~EM-01` for `field_magnitude`, `EPS0`, `K_E`; `~EM-02` for `uniform_sphere_field`,
  the worked test distribution. Both supply the **E** that the field-energy integral
  $\tfrac{\varepsilon_0}{2}\int|\mathbf E|^2\,d\tau$ reuses with no glue code.
- `~EM-07` (dielectrics) carries capacitance into matter: $C\to\kappa C$ and energy
  density $\tfrac12\mathbf D\cdot\mathbf E$.
- Downstream, the energy density $\tfrac{\varepsilon_0}{2}E^2$ and surface pressure
  reappear as the field energy and Maxwell stress of `~EM-14`.
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 1–2
  (electrostatic energy and capacitance; `EM/Jackson…SolutionManual…pdf` holds
  solutions only locally); Schwinger, *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
