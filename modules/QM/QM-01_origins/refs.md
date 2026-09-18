# QM-01 — References

Page-level citations **verified by reading the page text** in the PDF (not a
table of contents). **Printed** = the number on the page; **PDF** = the page in
the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |
| Bethe & Jackiw, *Intermediate Quantum Mechanics*, 3rd ed. | `QM_Quantum_Mechanics/BetheQM.pdf` | text-extractable; cite by §/p. |

> **Offset note.** Verified empirically: the printed folio equals the viewer
> page throughout the body (folio 16 = §1.1 at viewer 16; folio 301 = §6 at
> viewer 301; linear and constant in between). The whole QM trunk uses this scan.

## Topic → location

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| de Broglie wavelength λ=h/p (`de_broglie_wavelength`) | Griffiths 3e | §1.6 *The Uncertainty Principle* (wave/wavelength trade-off) | 35 |
| de Broglie & the classical↔quantum boundary | Griffiths 3e | **Problem 1.18** | 40 |
| Planck's constant introduced | Griffiths 3e | §1.1, footnote | 16 |
| black body & photoelectric (as *applications*, not derivations) | Griffiths 3e | radiation chapter / Afterword | 530–541, 566 |

> **Honesty note (per the trunk's citation rule).** Griffiths 3e is a *quantum
> mechanics* text: it starts from the wavefunction and does **not** derive the
> black-body spectrum, the photoelectric equation or the Bohr model (these are
> the "old quantum theory" that precedes its starting point). It mentions Planck
> (p.16) and revisits black-body/photoelectric as applications later (pp.530–541)
> and in the Afterword (p.566) — those locations are verified, but they are
> mentions, not first-principles treatments. The derivations in `notes.md` are
> standard results; **the verification here is the code**, where σ, the Wien
> constant, the Rydberg constant and λ_C are rederived from h, c, k_B, e, mₑ and
> checked to CODATA in `test_origins.py`.

## Problems (verified, Griffiths 3e)
- **Problem 1.18** — de Broglie wavelength vs system size; which systems must be
  treated quantum-mechanically — printed **p.40**.

## Further reading (not page-verified here)
- Sakurai & Napolitano, *Modern QM* — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an **image-only
  scan (no text layer)**; cite unpinned (intro/ch.1 historical remarks).
- Cohen-Tannoudji, *Quantum Mechanics* Vol. I — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned (Ch. I & complements on wave-particle
  duality).
- The old quantum theory (Planck, Einstein, Bohr, Sommerfeld) is the subject of
  modern-physics texts; not on this shelf.
