# RE-06 — References

Page-level citations **verified by reading the page text** (PyMuPDF) in the PDFs
under `books/library/`. **Printed** = the number on the page; **PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| relativistic mechanics; proper velocity → 4-velocity | Griffiths | §12.2.1 *Proper Time and Proper Velocity* | 532 | 550 |
| `E=γmc²`, `𝐩=γm𝐯`, the mass shell (`energy`, `momentum`, `four_momentum`) | Griffiths | §12.2.2 *Relativistic Energy and Momentum* | 535 | 553 |
| collisions, thresholds, invariant mass (`is_conserved`, `system_invariant_mass`, `threshold_kinetic_energy`) | Griffiths | §12.2.3 *Relativistic Kinematics* | 537 | 555 |
| relativistic force / dynamics (`kinetic_energy`) | Griffiths | §12.2.4 *Relativistic Dynamics* | 540 | 558 |
| the worldline action `S=−m∫dτ` (geometric origin of `p=mU`) | Zee | §III.5 *The Worldline Action…* | 207 | 230 |
| 4-velocity, mass shell `p·p=−m²` (`four_momentum`) | — see **RE-05** `minkowski` (`four_momentum`, `invariant_mass`) | — | — | — |
| Newtonian momentum `p=m𝐯` it reduces to | — see **CM-06** `linear_momentum` (`momentum`, `total_momentum`) | — | — | — |

## Problems (verified, Griffiths 4th ed.)
- **Prob. 12.30** — a particle whose kinetic energy is `n` times its rest energy: find its speed — printed **537**, PDF 555.
- **Prob. 12.31** — a collection of particles; total energy, momentum, and invariant mass — printed **537**, PDF 555.
- **Prob. 12.33** — a particle of total energy twice its rest energy collides with an identical one at rest — printed **541**, PDF 559.
- **Prob. 12.34** — a neutral pion of mass `m` decays into two photons — printed **541**, PDF 559.
- **Prob. 12.36** — pair annihilation `e⁺e⁻ → 2γ` — printed **542**, PDF 560.

## Cross-module dependencies
- **RE-05** `minkowski` — the 4-momentum and mass shell this module computes with.
- **CM-06** `linear_momentum` — the Newtonian momentum conservation it generalizes.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 4 (relativistic mechanics) —
  `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 2 — `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
