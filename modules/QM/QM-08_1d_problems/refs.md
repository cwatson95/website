# QM-08 — References

Page-level citations **verified by reading the page text** in the PDF (extracting
`get_text()`, not trusting a table of contents). **Printed** = the number on the
page; **PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module: the printed folio equals
> the viewer page (e.g. §2.2 prints "49" at viewer page 49; §2.6 prints "93" at
> viewer 93). The whole QM trunk uses this scan; `fitz.open(path)[P-1]` reads
> printed page `P`.

## Topic → location (all printed pages read and confirmed)

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| Infinite square well, $E_n=n^2\pi^2\hbar^2/2mL^2$ (`infinite_well_energy`, `bound_states`) | Griffiths 3e | §2.2 *The Infinite Square Well* | 49–50 |
| Bound vs scattering states (the dichotomy) | Griffiths 3e | §2.5.1 | 82–83 |
| Free particle, dispersion & wave packets (`free_particle_omega`, `gaussian_packet_sigma`) | Griffiths 3e | §2.4 *The Free Particle* | 74 |
| Delta-function well, one bound state $E=-m\alpha^2/2\hbar^2$ (`delta_well_energy`) | Griffiths 3e | §2.5 *The Delta-Function Potential* (Eq. 2.132) | 81, 85, 87 |
| Reflection & transmission coefficients, $R+T=1$ (`step_RT`, `scatter_piecewise`) | Griffiths 3e | §2.5 (delta scattering) | 89 |
| Tunnelling (delta/finite barrier) | Griffiths 3e | §2.5 | 90 |
| Finite square well, bound-state count & transmission resonances (`finite_square_well_bound_count`) | Griffiths 3e | §2.6 *The Finite Square Well* (Eq. 2.172) | 93, 96 |

## Problems (verified, Griffiths 3e)
- **Problem 2.31** — delta well as the zero-width limit of a finite square well;
  recover $E=-m\alpha^2/2\hbar^2$ — printed **p.97**. *(Checked by
  `test_delta_well_as_finite_square_well_limit`.)*
- **Problem 2.33** — transmission coefficient of a **rectangular barrier**, the
  three cases $E<V_0$, $E=V_0$, $E>V_0$; partial answer $T=[1+\frac{V_0^2
  \sinh^2\kappa a}{4E(V_0-E)}]^{-1}$ — printed **p.97**. *(This is exactly
  `transmission_barrier`.)*
- **Problem 2.34** — the **step potential**: reflection coefficient for
  $E>V_0$ and $E<V_0$, and the current-weighted transmission $T=\frac{k_2}{k_1}
  |F/A|^2$ (part c) — printed **p.97–98**. *(This is `step_RT`.)*
- **Problem 2.35** — a particle meeting an abrupt potential **drop** ("cliff"):
  reflection even when the step goes *down* — printed **p.98**.
- **Problem 2.22** — the spreading free Gaussian wave packet — referenced from
  §2.4 (p.74); the spreading law $\sigma_x(t)$ is `gaussian_packet_sigma`.

> **Honesty note (per the trunk's citation rule).** All page numbers above were
> confirmed by extracting and reading the page text before citing. Griffiths uses
> the symbol $a$ for the infinite-well width (this module's code uses $L$ to avoid
> clashing with the finite well's *half-width* $a$) — same formula, renamed symbol.
> The infinite-well energy and the step/barrier coefficients carry equation
> numbers in the 2.27–2.32 / 2.169–2.175 image blocks that I could **not** pin to
> an individual number from the text layer, so they are cited **by section and
> page** (verified) rather than by equation; Eq. 2.132 (delta energy) and Eq. 2.172
> (finite-well transmission) *are* pinned because their numbers are cross-referenced
> in the verifiable text of Problems 2.31/2.32 (p.97). **The deeper verification is
> the code**, where every spectrum and coefficient is checked against a closed form
> and an independent transfer-matrix solve in `test_one_dim.py`.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; `get_text()` returns nothing, so cite
  unpinned. 1-D potentials/tunnelling are covered in its Ch. 2 (Schrödinger wave
  mechanics) — referenced without a page number by trunk rule.
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. I** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned (Ch. I complements on 1-D square
  potentials, barriers, and bound states).
- **Bethe & Jackiw, *Intermediate QM*** — `QM_Quantum_Mechanics/BetheQM.pdf` has a text layer
  but is pitched past these basics (it opens at the hydrogen atom and beyond); not
  cited here for the elementary 1-D problems.
- WKB tunnelling ($T\sim e^{-2\int\kappa\,dx}$) is deferred to `~QM-15`; the
  partial-wave / Born scattering generalization to `~QM-18`.
