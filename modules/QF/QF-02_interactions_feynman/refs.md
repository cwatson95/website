# QF-02 — References

| Book (edition) | File | Notes |
|---|---|---|
| Peskin & Schroeder, *An Introduction to Quantum Field Theory* (1995) | `QF_Quantum_Field_Theory/QFTPeskin.pdf` | **primary.** Cited at **section level** (Ch. 4 + §2.4). Section titles read from the PDF table of contents; printed↔PDF page offset **not** verified, so no page numbers are given. |
| Zee, *Quantum Field Theory in a Nutshell* (2nd ed.) | `QF_Quantum_Field_Theory/Zee_QFT.pdf` | cross-reference, cited at **section level** (Part I). Section titles (I.3, I.4, I.7) read from the PDF TOC; no page numbers. |

> **Granularity.** This module cites by **chapter/section title**, not page. The
> Peskin Ch. 4 and §2.4 section headings below were read directly from the book's
> table of contents in `QFTPeskin.pdf`; the Zee §I.x titles likewise from
> `Zee_QFT.pdf`. Page-level pinning (à la `~SM-06`/`~QM-18`) was deliberately not
> attempted here — tighten to pages by opening the PDFs if needed.

## Topic → location (Peskin & Schroeder — primary, Chapter 4)

| Topic (code symbol) | Section / title |
|---|---|
| Interaction picture; the Dyson series / time-ordered exponential | §4.2 *Perturbation Expansion of Correlation Functions* |
| Wick's theorem; contractions → propagators (`propagator`) | §4.3 *Wick's Theorem* |
| Feynman propagator $\widetilde D_F(p)=i/(p^2-m^2+i\epsilon)$ — derivation (`propagator`) | §2.4 *The Klein–Gordon Field in Space-Time* |
| Feynman diagrams; the $\phi^4$ vertex $-i\lambda$ (`phi4_amplitude_squared`) | §4.4 *Feynman Diagrams* |
| Cross sections & the S-matrix; the 2→2 phase space; $d\sigma/d\Omega=|\mathcal{M}|^2/(64\pi^2 s)$ (Eq. 4.84); the $\phi^4$ total $\sigma=\lambda^2/(32\pi s)$ (`phi4_cross_section`, `phi4_differential_cross_section`) | §4.5 *Cross Sections and the S-Matrix* |
| Computing S-matrix elements from diagrams (the procedure behind the amplitude) | §4.6 *Computing S-Matrix Elements from Feynman Diagrams* |
| Mandelstam variables $s,t,u$ and $s+t+u=\sum_i m_i^2$ (`mandelstam`, `mandelstam_sum`, `cm_energy`, `cm_momentum`) | §4.5 (2→2 kinematics) and §5.4 *Crossing Symmetry* (where $s,t,u$ are named) |
| Loop diagrams diverge → renormalization | §4.4–4.5 (the $O(\lambda^2)$ loop), continued in Ch. 6–7 → `~QF-04` |

> **Honesty note.** Mandelstam $s,t,u$ are *used* in the Ch. 4 cross-section
> kinematics but are formally **named and tabulated** by Peskin in §5.4 (*Crossing
> Symmetry*); the sum rule $s+t+u=\sum_i m_i^2$ is standard 2→2 kinematics. The
> identity, the CM relations, and the $\phi^4$ cross section are all **verified in
> the code** (`test_feynman.py`): $s+t+u=4m^2$, $s=E_{\mathrm{cm}}^2$, $\sigma>0$,
> $\sigma\propto\lambda^2$, threshold at $\sqrt{s}=2m$, and the on-shell propagator
> pole $|\widetilde D_F|\sim1/\epsilon$.

## Topic → location (Zee — cross-reference, Part I)

| Topic | Section / title |
|---|---|
| From fields to particles and forces; the propagator as the force-carrier line | §I.3 *From Mattress to Field*; §I.4 *From Field to Particle to Force* |
| Feynman diagrams; the $\phi^4$ interaction, the vertex, and reading amplitudes off diagrams | §I.7 *Feynman Diagrams* |

## See also
- `~QF-01` (this trunk) — canonical quantization: the free fields and propagators
  contracted here; the oscillator bridge **B6** (`CM-15 → CM-16 → QM-09 → QF-01`).
- `~QM-16` — time-dependent perturbation theory, the non-relativistic ancestor of
  the Dyson series ($S=T\exp(-i\int H_I\,dt)$).
- `~QM-18` — non-relativistic scattering: the Born approximation is tree-level
  perturbation theory, with $d\sigma/d\Omega=|f(\theta)|^2$ the QM analogue of the
  field-theory cross section here.
- `~QF-04` — renormalization & the RG: makes sense of the divergent $\phi^4$ loops.
- `~QF-03` — gauge theories / QED: the same Feynman-rule machinery with spin and
  polarization.
- Peskin & Schroeder Ch. 4 (the canonical treatment); Zee Part I (intuitive,
  path-integral flavoured); both on the shelf `books/library/QF_Quantum_Field_Theory/`.
