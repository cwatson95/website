# EM-17 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was re-confirmed against the page text across Ch. 10–11 (e.g. printed 444 → PDF
462, 451 → 469, 467 → 485, 482 → 500). Griffiths is the worked source for the whole
EM-01..EM-18 sequence; Jackson 3e and Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| retarded potentials, retarded time (`retarded_time`, `retarded_potential_static`) | §10.2.1 *Retarded Potentials* (Eq. 10.26; $t_r=t-\eta/c$, Eq. 10.19) | 444 | 462 |
| Liénard-Wiechert potentials (`lienard_wiechert`) | §10.3.1 *Liénard-Wiechert Potentials* (Eq. 10.46–10.47) | 451 | 469 |
| electric dipole radiation (`dipole_radiated_power`, `dipole_angular_power`, `total_power_from_pattern`) | §11.1.2 *Electric Dipole Radiation* (Eq. 11.21 pattern, Eq. 11.22 total) | 467 | 485 |
| Larmor formula (`larmor_power`) | §11.2.1 *Power Radiated by a Point Charge* (Eq. 11.70 = 11.61, on p.484/PDF 502) | 482 | 500 |

## See also
- `~EM-01` / `~EM-08` for the constants reused here: `EPS0`, `K_E` = 1/4πε₀ (EM-01) and
  `MU0` (EM-08), which combine into `C` = 1/√(μ₀ε₀), and EM-08's vector potential **A**.
- `~MA-01` for `norm`/`unit`/`dot`, used by `retarded_time` and `lienard_wiechert`.
- `~MA-14` (Green's functions) — the retarded potential is the **retarded Green's function /
  propagator** of the wave operator $\Box$ convolved with the source; Griffiths derives it
  via the retarded-time argument rather than the propagator formalism.
- `~EM-05` (multipole / dipole) — the oscillating electric dipole of §11.1 is the EM-05
  dipole set in motion.
- `~EM-18` (relativistic electrodynamics) for the covariant form of the moving-charge fields.
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, **Ch. 9–11** (radiating
  systems, the Liénard-Wiechert fields, and radiation by accelerated charges); Schwinger
  *et al.*, *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`) for the source-theory / Green's-
  function route to the same potentials.
