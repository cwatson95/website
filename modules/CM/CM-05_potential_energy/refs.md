# CM-05 — References

**Verification:** Fowles & Cassiday has a real **text layer** (text-extracted and
confirmed). Marion & Thornton is a **scanned, image-only PDF**; its page was read
from a **rendered page image** (folio + heading quoted as proof).

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| conservative forces & force fields (`is_conservative`) | Fowles | §4.1 *Introduction: General Principles* — "Conservative Forces and Force Fields" | 146 | 157 |
| potential energy; F = −∇V (`force_from_potential`) | Fowles | §4.2 *The Potential Energy Function in Three-Dimensional Motion: The Del Operator* (Eq. 4.2.4) | 151 | 162 |
| energy conservation T + V = E (`total_energy`) | Fowles | §4.2 (continued) | 152 | 163 |
| equilibria & stability, 1-D potential (`is_equilibrium`, `is_stable`) | Fowles | §2.3 *Forces that Depend on Position: Kinetic and Potential Energy* | 63 | 74 |
| conservative forces, potential energy, turning points | Marion & Thornton *(image)* | §2.6 *Energy* | 82 | 96 |

- `force_from_potential` and `is_conservative` reuse `~MA-02`'s `gradient`/`curl`.
