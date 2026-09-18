# SM-01 — References

Page-level citations to **Pathria** were **verified by reading the page text** in
the PDF. **Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Notes |
|---|---|---|
| Pathria & Beale, *Statistical Mechanics*, **3rd ed.** | `SM_Statistical_Mechanics/PathriaStatMech.pdf` | printed↔PDF offset **drifts** (≈ +16 early → +7 late); pairs below read directly off each page |
| Schroeder, *An Introduction to Thermal Physics* | `SM_Statistical_Mechanics/SchroderStatMech.pdf` | **scanned / image-only** — no text layer; cited at **chapter level only** |

> The Pathria PDF accumulates a few unnumbered pages through the book, so a single
> printed→PDF offset is wrong; each pair in the table was confirmed on its own page.
> Schroeder cannot be page-verified (image scan), so it is cited by chapter.

## Topic → location

| Topic (code symbol) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| fundamental postulate, microstates (`multiplicity_two_state`) | Pa | §1.1 *The macroscopic and microscopic states* | 1 | 17 |
| Boltzmann entropy S = k ln Ω (`boltzmann_entropy`) | Pa | §1.2 *Contact between statistics & thermodynamics: the number Ω(N,V,E)* | 3 | 19 |
| Stirling, classical ideal gas (`stirling_ln_factorial`) | Pa | §1.4 *The classical ideal gas* (Sackur–Tetrode) | 10 | 25 |
| entropy of mixing / Gibbs paradox | Pa | §1.5 *The entropy of mixing and the Gibbs paradox* | 16 | 32 |
| phase space (`multiplicity_einstein_solid` context) | Pa | §2.1 *Phase space of a classical system* | 25 | 40 |
| the microcanonical ensemble | Pa | §2.3 *The microcanonical ensemble* | 30 | 45 |
| multiplicity, two-state systems, Stirling | Sch | Ch.2 *The Second Law* (multiplicity, Einstein solid, Stirling) | — (image-only) | — |

## See also
- `~MA-19` for `binomial_pmf` / `normal_pdf`, reused by `two_state_probability` and
  `gaussian_approx_two_state`; the 1/√N sharpening is the central-limit theorem.
- `~SM-02` (entropy → temperature & the laws), `~SM-03` (canonical ensemble) build on S = k ln Ω.
- Higher-level: Pathria Ch.1–2 (rigorous); Schroeder Ch.2 (gentle, image-only locally).
