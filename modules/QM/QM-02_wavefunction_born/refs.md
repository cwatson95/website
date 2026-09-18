# QM-02 — References

Page-level citations **verified by extracting the page text** from the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module: the printed folio equals
> the viewer page. The folio printed at the foot of each page I cite matched its
> 1-based index exactly — e.g. index 16 → "17" (§1.2), index 28 → "29" (§1.4),
> index 31 → "32" (§1.5), index 133 → "134" (momentum space). So to read printed
> page $P$: `fitz.open(path)[P-1].get_text()`.

## Topic → location (all verified)

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| The wavefunction $\Psi(x,t)$ introduced | Griffiths 3e | §1.1 *The Schrödinger Equation* | 16 |
| Born's rule: $|\Psi|^2$ is a probability density (`prob_density`) | Griffiths 3e | §1.2 *The Statistical Interpretation* | 17 |
| Probability (theory digression) | Griffiths 3e | §1.3 *Probability* (header) | 21 |
| Mean / expectation of a discrete variable $\langle j\rangle$ | Griffiths 3e | §1.3.1 *Discrete Variables* | 22 |
| Variance & standard deviation $\sigma^2=\langle x^2\rangle-\langle x\rangle^2$ (`sigma_x`) | Griffiths 3e | §1.3.1, Eqs.1.11–1.13 | 24 |
| Continuous density; $P(a\le x\le b)=\int_a^b\!\rho\,dx$ (`prob_between`) | Griffiths 3e | §1.3.2 *Continuous Variables*, Eq.1.16 | 26 |
| Normalization $\int|\Psi|^2dx=1$; square-integrable; $\Psi\to0$ at $\infty$ (`normalize`) | Griffiths 3e | §1.4 *Normalization*, Eq.1.20 | 29 |
| Norm preserved in time ($d/dt\int|\Psi|^2=0$) | Griffiths 3e | §1.4, Eq.1.27 ("…QED") | 30 |
| $\langle x\rangle=\int x|\Psi|^2dx$; ensemble (not repeated) average (`expectation_x`) | Griffiths 3e | §1.5 *Momentum*, Eq.1.28 | 32 |
| Momentum operator $\hat p=-i\hbar\partial_x$; $\langle p\rangle$ "sandwich" (`expectation_p`) | Griffiths 3e | §1.5, Eqs.1.33–1.35; recipe Eq.1.36 | 33 |
| Momentum-space wavefunction $\Phi(p)$ = Fourier transform of $\Psi$ (Plancherel) (`momentum_space`) | Griffiths 3e | §3.4 *Generalized Statistical Interpretation* | 134 |

## Problems (verified, Griffiths 3e)
- **Problem 1.4** — normalize a triangular $\Psi$; probability to the left of a
  point; expectation value of $x$ — printed **p.30**.
- **Problem 1.5** — normalize $\Psi=Ae^{-\lambda|x|}e^{-i\omega t}$; find
  $\langle x\rangle,\langle x^2\rangle$ and the standard deviation $\sigma_x$;
  probability of being found outside $\langle x\rangle\pm\sigma$ — printed **p.30**.
- **Problem 1.7** — $d\langle p\rangle/dt=\langle -\partial V/\partial x\rangle$
  (Ehrenfest's theorem) — printed **p.34**.
- **Problem 2.21** — *the Gaussian wave packet*: normalize a free Gaussian and
  watch it spread in time (the closed form `free_propagate` reproduces) —
  printed **p.80**.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**, so `get_text()` returns nothing; cited
  **unpinned**: Ch. 1 (state kets, position/momentum representations,
  $\langle x|\alpha\rangle$ as the wavefunction; Gaussian wave packets).
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. I** —
  `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf` is likewise **image-only**; cited unpinned:
  Ch. I (the wave function and Schrödinger equation; probabilistic interpretation)
  and the complement on the Fourier/momentum-space description.

> **Honesty note.** Unlike `~QM-01` (old quantum theory, which Griffiths only
> *mentions*), every topic in QM-02 is treated head-on in Griffiths 3e Chapter 1,
> and the pages above were each confirmed by reading their text. The only
> cross-chapter pin is the momentum-space wavefunction $\Phi(p)$ (§3.4, p.134),
> which Griffiths develops fully only after the formalism of `~QM-05`; in Chapter 1
> momentum enters solely through the operator $-i\hbar\partial_x$ (p.33). The
> physics verification, as always in this trunk, is the code: every closed-form
> Gaussian moment in `notes.md` is checked numerically in `test_wavefunction.py`.
