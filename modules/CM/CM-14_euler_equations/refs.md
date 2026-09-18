# CM-14 — References

**Verification:** Fowles & Cassiday has a real **text layer** (text-extracted and
confirmed). Marion & Thornton is a **scanned, image-only PDF**; its page was read
from a **rendered page image** (folio + heading quoted as proof).

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| Euler's equations of motion (`euler_rhs`) | Fowles | §9.3 *Euler's Equations of Motion of a Rigid Body* | 381 | 392 |
| free (torque-free) rotation (`L_magnitude_sq`, `rotational_energy`) | Fowles | §9.4 *Free Rotation of a Rigid Body: Geometric Description* | 383 | 394 |
| free precession of a symmetric top (`precession_rate`) | Fowles | §9.5 *Free Rotation of a Rigid Body with an Axis of Symmetry* | 384 | 395 |
| Euler's equations for a rigid body | Marion & Thornton *(image)* | §11.9 *Euler's Equations for a Rigid Body* | 444 | 458 |

- Integrated with `~MA-07`; principal moments come from `~CM-13`.
