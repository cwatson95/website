# CM-23 — References

**Verification:** Boas has a real **text layer** (text-extracted and confirmed).

**Shelf-gap note (honest):** the user's *ClassicalMechanics* shelf (Fowles,
Marion & Thornton, Goldstein) covers **particle and rigid-body** mechanics — there
is **no fluid-dynamics text on the shelf**. The flow operators (divergence, curl,
the velocity field) are cited to Boas's vector analysis, where they are derived
with an explicit fluid-flow example; the **Euler equation** and **Bernoulli's
equation** are standard results stated in `notes.md` without a verified shelf page
(not fabricated to one).

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** | text-verified |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| velocity field, streamlines, flux (`vorticity`, `is_irrotational`) | Boas | Ch.6 §10 *The Divergence and the Divergence Theorem* ("Consider a region in which water is flowing… stream lines") | 314 | 333 |
| divergence as net outflow per volume (`is_incompressible`) | Boas | Ch.6 §10 ("the net rate of outflow per unit volume… at a point") | 316 | 335 |
| the curl operator (vorticity) | Boas | Ch.6 §11 *The Curl and Stokes' Theorem* | 324 | 343 |

- `vorticity`/`is_incompressible`/`is_irrotational` reuse `~MA-02`'s `curl`/`divergence`.
- `Bernoulli_constant`: standard (no shelf source) — flagged above.
