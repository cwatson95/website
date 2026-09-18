# CM-16 — References

**Verification:** Fowles & Cassiday has a real **text layer** (text-extracted and
confirmed). Marion & Thornton is a **scanned, image-only PDF**; its pages were read
from **rendered page images** (folio + heading quoted as proof).

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| coupled oscillators; normal coordinates (`normal_modes`) | Fowles | §11.3 *Coupled Harmonic Oscillators: Normal Coordinates* | 472 | 483 |
| dynamics of oscillating systems (overview) | Fowles | Ch.11 *Dynamics of Oscillating Systems* | 465 | 476 |
| normal coordinates | Marion & Thornton *(image)* | §12.6 *Normal Coordinates* (Ch.12 *Coupled Oscillations*) | 483 | 497 |
| coupled oscillations (overview) | Marion & Thornton *(image)* | Ch.12 *Coupled Oscillations* | 468 | 482 |

- `normal_modes` reduces the generalized eigenproblem K v = ω²M v to a symmetric one and
  calls `~MA-04`'s `eig_symmetric`.
