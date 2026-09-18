# CM-02 — References

**Verification:** Fowles & Cassiday has a real **text layer** — citations were
text-extracted and confirmed. Marion & Thornton is a **scanned, image-only PDF**;
its pages were read from **rendered page images** (the mining agent quoted the
visible printed folio + heading as proof) — reliable, but not text-extractable.

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| Newton's laws of motion (`newton_rhs`, `sum_forces`) | Fowles | §2.1 *Newton's Laws of Motion: Historical Introduction* (2nd/3rd law p.57) | 47 | 58 |
| equation of motion F = dp/dt = ma (`trajectory`) | Fowles | §4.1 *Introduction: General Principles* (Eq. 4.1.1–4.1.2) | 144 | 155 |
| forces depending on position (`spring_force` etc.) | Fowles | §2.4 *Forces that Depend on Position* | 63 | 74 |
| Newton's laws | Marion & Thornton *(image)* | §2.2 *Newton's Laws* | 49 | 63 |
| equation of motion for a particle | Marion & Thornton *(image)* | §2.4 *The Equation of Motion for a Particle* | 55 | 69 |

- The **RK4 integrator** is `~MA-07` (a standard numerical method, not a textbook section).
