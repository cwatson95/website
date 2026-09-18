# CM-19 — References

**Verification:** Fowles & Cassiday has a real **text layer** (text-extracted and
confirmed). Goldstein is a **scanned, image-only PDF**; its page was read from a
**rendered page image** (folio + heading quoted as proof). **Goldstein offset
(verified):** this section is in Ch.8, where the scan has drifted to PDF = printed
**+ 6** (folio-checked; not the +10 of the early chapters).

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Goldstein, Poole & Safko, *Classical Mechanics*, **3rd ed.** | `CM_Classical_Mechanics/GoldsteinCM.pdf` | PDF = printed **+ 6** (Ch.8) | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| the Hamiltonian function; Hamilton's equations (`hamilton_rhs`, `integrate_hamilton`) | Fowles | §10.9 *The Hamiltonian Function: Hamilton's Equations* | 455 | 466 |
| Legendre transformation & Hamilton's equations (`hamiltonian_from_potential`) | Goldstein *(image)* | §8.1 *Legendre Transformations and the Hamilton Equations of Motion* | 334 | 340 |

- Integrated with `~MA-07`; the conjugate momentum / Legendre transform comes from `~CM-17`.
