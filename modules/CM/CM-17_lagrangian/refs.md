# CM-17 — References

**Verification:** Fowles & Cassiday has a real **text layer** (text-extracted and
confirmed). Marion & Thornton and Goldstein are **scanned, image-only PDFs**; their
pages were read from **rendered page images** (folio + heading quoted as proof).
**Goldstein offset note (verified):** PDF = printed **+ 10** in Ch.1–5, but the
scan drops ~4 leaves so it drifts to **+ 6** by Ch.8–9 — every page below was
folio-checked individually.

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Goldstein, Poole & Safko, *Classical Mechanics*, **3rd ed.** | `CM_Classical_Mechanics/GoldsteinCM.pdf` | (drifts; see note) | image scan |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| generalized coordinates | Fowles | §10.2 *Generalized Coordinates* | 423 | 434 |
| Lagrange's equations (`el_residual`, `generalized_momentum`) | Fowles | §10.4 *Lagrange's Equations of Motion for Conservative Systems* | 430 | 441 |
| Hamilton's principle | Goldstein *(image)* | §2.1 *Hamilton's Principle* | 34 | 44 |
| Lagrange's equations from Hamilton's principle | Goldstein *(image)* | §2.3 *Derivation of Lagrange's Equations from Hamilton's Principle* | 44 | 54 |
| D'Alembert's principle & Lagrange's equations | Goldstein *(image)* | §1.4 *D'Alembert's Principle and Lagrange's Equations* | 16 | 26 |
| Lagrangian & Hamiltonian dynamics (overview) | Marion & Thornton *(image)* | Ch.7 *Hamilton's Principle—Lagrangian and Hamiltonian Dynamics* | 228 | 242 |

- `el_residual` reuses `~MA-13`'s `euler_lagrange_residual`; `integrate_eom` reuses `~MA-07`.
