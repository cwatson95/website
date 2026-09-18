# CM-15 — References

**Verification:** Fowles & Cassiday has a real **text layer** (text-extracted and
confirmed). Marion & Thornton is a **scanned, image-only PDF**; its pages were read
from **rendered page images** (folio + heading quoted as proof).

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| simple harmonic motion (`integrate_oscillator`) | Fowles | §3.2 *Linear Restoring Force: Harmonic Motion* | 84 | 95 |
| damped harmonic motion (`damped_frequency`, `underdamped_solution`) | Fowles | §3.4 *Damped Harmonic Motion* | 96 | 107 |
| forced motion; resonance (`driven_amplitude`, `resonance_frequency`, `quality_factor`) | Fowles | §3.6 *Forced Harmonic Motion: Resonance* | 113 | 124 |
| damped oscillations | Marion & Thornton *(image)* | §3.5 *Damped Oscillations* | 108 | 122 |
| sinusoidal driving forces | Marion & Thornton *(image)* | §3.6 *Sinusoidal Driving Forces* | 117 | 131 |

- Integrated with `~MA-07` (RK4); the constant-coefficient ODE theory is Boas §8.5/8.6 (see `~MA-07`).
