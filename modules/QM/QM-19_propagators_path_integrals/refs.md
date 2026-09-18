# QM-19 — References

Page-level citations **verified by extracting the page text** from the PDF (not a
table of contents). **Printed** = the number printed on the page; **PDF** = the
page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically (`fitz.open(path)[P-1].get_text()` returns
> printed page $P$): the printed folio equals the viewer page throughout the body.
> Same scan the rest of the QM trunk uses.

## Topic → location (verified)

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| **Propagator defined**; $\Psi(x,t)=\int K\,\Psi(x',0)dx'$; eigen-sum $K=\sum\psi_n\psi_n^*e^{-iE_nt/\hbar}$ (Eq. 6.79); $|K|^2$ = travel probability (`box_propagator`, `free_propagator`) | Griffiths 3e | §6.8.2 *Time-Translation Invariance*, **Problem 6.30** | **342** |
| Harmonic-oscillator propagator $K$ (Mehler) (`harmonic_propagator`) | Griffiths 3e | Problem 6.30(b) | 342 |
| Free-particle propagator $K_0$ (`free_propagator`) | Griffiths 3e | Problem 6.30(d) | 342 |
| Propagator **= Green's function**; inspiration for Feynman's formulation (`free_retarded_propagator`, `box_resolvent_static`) | Griffiths 3e | §10 Born series (scattering) | **503** |
| General solution as a superposition $\sum_n c_n\psi_n e^{-iE_nt/\hbar}$ (the seed of the eigen-sum) | Griffiths 3e | §2.1 *Stationary States* | 43 |
| Infinite-square-well eigenfunctions $\psi_n=\sqrt{2/a}\sin(n\pi x/a)$, $E_n$ (`box_eigenfunction`, `box_energy`) | Griffiths 3e | §2.2 *The Infinite Square Well* | 49–52 |
| Free particle; Gaussian wavepacket & spreading (`gaussian_packet`, spreading test) | Griffiths 3e | §2.4 *The Free Particle*; **Problem 2.21** | 74; 76 |

> **Honesty note (WEAK-COVERAGE module, per the trunk's citation rule).**
> Griffiths 3e contains **no path-integral treatment** — searching the full text,
> "path integral" / "sum over paths" return **zero** hits, and "propagator"
> appears on only three pages (342, 503, and the index, p.635). Those two body
> pages are, however, genuinely on-topic and verified above: **Problem 6.30
> (p.342)** *defines* the propagator and asks for its eigen-sum, free, and
> harmonic forms — i.e. most of this module's content — and **p.503** identifies
> the propagator with the Green's function and names it Feynman's inspiration.
> The path-integral derivation in `notes.md §4` is standard material taken from
> the unpinned sources below; **the verification of every formula is the code**
> (`test_propagator.py`, 15 checks against closed forms, an independent split-step
> FFT integrator, and an imported `~MA-14` Green's function) — exactly how
> `QM-01_origins` handles black-body/Bohr, which Griffiths likewise does not derive.

## Imported module (code reuse, API verified)
- **`~MA-14` Green's functions** — `modules/MA/MA-14_greens_functions/code/greens_function.py`.
  Imported `green_series(x, xi, nmax)` (spectral sum $\sum 2\sin n\pi x\,\sin n\pi\xi/(n\pi)^2$),
  `green_dirichlet(x, xi)` ($=x_<(1-x_>)$), and `causal_green_oscillator` (the
  causal/retarded structural analogue). `test_ma14_resolvent_link` verifies the
  box static resolvent $\sum_n\psi_n\psi_n/E_n = 2\,\texttt{green\_series}\to2\,\texttt{green\_dirichlet}$.

## Problems (verified, Griffiths 3e)
- **Problem 6.30** — the propagator: eigen-sum (a), harmonic (b), free (d) —
  printed **p.342**. The spine of this module.
- **Problem 2.21** — free Gaussian wavepacket and its spreading — printed **p.76**.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite **unpinned**. The propagator and the
  Feynman path integral are developed in **Ch. 2** (*Quantum Dynamics*) — the
  standard textbook treatment this module follows. (Left unpinned deliberately:
  no text layer means a page number cannot be verified, and a wrong page is worse
  than none.)
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. I** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite **unpinned** (the propagator / evolution
  operator and its complements).
- **Feynman & Hibbs, *Quantum Mechanics and Path Integrals*** — the original
  text; not on this shelf.
- `~CM-17` (Lagrangian mechanics / Hamilton's principle) is the **classical**
  partner reached by the stationary-phase $\hbar\to0$ limit (bridge **B1**); it is
  **not built yet**, so it is referenced by id only — the bridge connects when it
  lands. Same for `~QF-01` (path integral → field theory, forward link).
