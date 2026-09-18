# CM-11 — References

**Verification:** Fowles & Cassiday has a real **text layer** (text-extracted and
confirmed). Marion & Thornton is a **scanned, image-only PDF**; its page was read
from a **rendered page image** (folio + heading quoted as proof).

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| gravitation & central forces (overview) | Fowles | Ch.6 *Gravitation and Central Forces* | 218 | 229 |
| Kepler's laws; T² ∝ a³ (`kepler_period`) | Fowles | §6.3 *Kepler's Laws of Planetary Motion* | 225 | 236 |
| inverse-square orbit; ellipses (`kepler_potential`, `orbit`, `circular_orbit_radius`) | Fowles | §6.5 *Kepler's First Law: The Law of Ellipses* | 229 | 240 |
| energy equation of an orbit (`effective_potential`) | Fowles | §6.9 *Energy Equation of an Orbit in a Central Field* | 251 | 262 |
| central-force motion | Marion & Thornton *(image)* | Ch.8 *Central-Force Motion* | 287 | 301 |

- `reduced_mass` is reused from `~CM-07`; the orbit integrator is `~MA-07`.
