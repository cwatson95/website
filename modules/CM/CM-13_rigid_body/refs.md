# CM-13 — References

**Verification:** Fowles & Cassiday has a real **text layer** (text-extracted and
confirmed). Marion & Thornton is a **scanned, image-only PDF**; its pages were
read from **rendered page images** (folio + heading quoted as proof).

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Fowles & Cassiday, *Analytical Mechanics*, **7th ed.** | `CM_Classical_Mechanics/FowlesCassiday.pdf` | PDF = printed **+ 11** | text-verified |
| Marion & Thornton, *Classical Dynamics*, **5th ed.** | `CM_Classical_Mechanics/marionThorton.pdf` | PDF = printed **+ 14** | image scan |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| inertia tensor; L=Iω, T=½ω·Iω (`inertia_tensor`, `angular_momentum`, `rotational_kinetic_energy`) | Fowles | §9.1 *Rotation of a Rigid Body about an Arbitrary Axis: Moments and Products of Inertia…* | 361 | 372 |
| principal axes of a rigid body (`principal_axes`) | Fowles | §9.2 *Principal Axes of a Rigid Body* | 371 | 382 |
| inertia tensor | Marion & Thornton *(image)* | §11.3 *Inertia Tensor* | 415 | 429 |
| principal axes of inertia | Marion & Thornton *(image)* | §11.5 *Principal Axes of Inertia* | 424 | 438 |

- `principal_axes` reuses `~MA-04`'s `eig_symmetric` (the Jacobi eigensolver) — the
  inertia tensor is the canonical real-symmetric eigenproblem of mechanics.
