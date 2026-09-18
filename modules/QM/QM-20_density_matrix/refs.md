# QM-20 — References

Page-level citations **verified by extracting the page text** from the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module: the printed folio equals
> the viewer page. The Chapter 12 "Afterword" opens on viewer page 566; §12.3
> *Mixed States and the Density Matrix* heading reads on viewer page 575; §12.3.2
> *Mixed States* on 579; §12.3.3 *Subsystems* on 582 — each confirmed by
> extracting the page text before citing. To read printed page $P$:
> `fitz.open(path)[P-1].get_text()`. Same scan as the rest of the QM trunk.

## Topic → location (all printed pages confirmed by reading the page)

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| **§12.3 *Mixed States and the Density Matrix*** (chapter "Afterword" begins p.566) | Griffiths 3e | §12.3 (heading) | **575** |
| Density operator $\rho=\|\psi\rangle\langle\psi\|$ defined; matrix elements $\rho_{ij}$; pure-state properties (Hermitian, $\mathrm{Tr}\,\rho=1$, $\rho^2=\rho$, $\mathrm{Tr}\,\rho^2=1$); $\langle A\rangle=\mathrm{Tr}(\rho A)$ (`density_matrix_pure`, `expectation`, `is_density_matrix`) | Griffiths 3e | §12.3.1 *Pure States* (Eqs. 12.16–12.21) | 576 |
| Example 12.1 (spin-up-$x$): "$\rho$ is hermitian, its trace is 1, and $\mathrm{Tr}\,\rho^2=1$"; **von Neumann equation** $i\hbar\dot\rho=[H,\rho]$ (`von_neumann_rhs`, `evolve`) | Griffiths 3e | Example 12.1; **Prob. 12.4(b)** | 577 |
| Mixed state $\rho=\sum_i p_i\|\psi_i\rangle\langle\psi_i\|$; populations sum to 1; "$\rho$ is idempotent only if it represents a pure state… a quick way to test whether the state is pure" (`density_matrix_mixed`, `is_pure`) | Griffiths 3e | §12.3.2 *Mixed States* (Eqs. 12.30–12.34) | 579 |
| Example 12.2 (50/50 mixture): "$\rho$ is hermitian, trace is 1, but $\mathrm{Tr}\,\rho^2<1$… not a pure state"; **purity** $\mathrm{Tr}(\rho^2)\le1$, $=1$ iff pure; $\rho^2=\rho$ iff pure (`purity`) | Griffiths 3e | Example 12.2; **Prob. 12.6(b),(c)** | 580 |
| Bloch-vector form of a qubit $\rho=\tfrac12(I+\mathbf a\!\cdot\!\boldsymbol\sigma)$; pure iff $\|\mathbf a\|=1$, mixed iff $\|\mathbf a\|<1$ (Bloch sphere) | Griffiths 3e | Prob. 12.8 | 580 |
| **Subsystems / reduced density matrix** ("subsystem density matrix"): a part of an entangled pure state is mixed; the singlet's positron reduces to a 50/50 mixture (`partial_trace`) | Griffiths 3e | §12.3.3 *Subsystems* (Eqs. 12.39–12.40) | 582 |
| **Decoherence** as the quantum→classical mechanism (off-diagonal collapse from environmental "measurement") | Griffiths 3e | §12.5 *Schrödinger's Cat* | 586 |

## Problems (verified, Griffiths 3e)
- **Problem 12.4** — (a) prove the pure-state density-matrix properties
  (Eqs. 12.17–12.20); (b) show the time evolution is $i\hbar\dot\rho=[H,\rho]$
  (the von Neumann equation) — printed **p.577**.
- **Problem 12.5** — repeat Example 12.1 for spin-down along $y$ — printed **p.577**.
- **Problem 12.6** — (a) prove the mixed-state properties; (b) **show
  $\mathrm{Tr}(\rho^2)\le1$, equal to 1 only if $\rho$ is pure**; (c) **$\rho^2=\rho$
  iff pure** — printed **p.580**.
- **Problem 12.7** — construct $\rho$ for a $\tfrac13$/$\tfrac23$ mixture of
  spin-up-$x$ and spin-down-$y$; find $\mathrm{Tr}(\rho^2)$ — printed **p.580**.
- **Problem 12.8** — the **Bloch vector**: most general spin-$\tfrac12$ $\rho$,
  pure iff on the Bloch sphere ($\|\mathbf a\|=1$), mixed inside — printed
  **p.580** (continues p.581).

> **Honesty notes (per the trunk's citation rule).**
> 1. **Equation glyphs are images in this scan.** Griffiths' *displayed, numbered*
>    equations in Ch. 12 (e.g. the explicit $\rho$ matrices, $\mathrm{Tr}\,\rho^2$,
>    the von Neumann equation) are typeset as embedded images, so `get_text()`
>    returns the surrounding prose and equation *numbers* but not the formula
>    glyphs. Every page above was confirmed by the **prose that names the result**
>    — e.g. p.577 literally reads *"Note that $\rho$ is hermitian, its trace is 1,
>    and …"* and *"Show that the time evolution of the density operator is governed
>    by the equation … (This is the Schrödinger equation, expressed in terms of
>    $\rho$)"*; p.579 *"$\rho$ is idempotent only if it represents a pure state
>    (indeed, this is a quick way to test whether the state is pure)"*; p.582
>    *"the subsystem … by itself does not occupy a pure state"*; p.586 *"This
>    phenomenon is called decoherence."* The formula *values* are the standard
>    ones and are themselves **verified numerically in
>    `code/test_density_matrix.py`**, not taken on faith.
> 2. **Anchor refinement.** The dispatch anchor was §12.3 / p.575 for the heading
>    *and* the purity statement. The heading is indeed on p.575, but the
>    purity/$\mathrm{Tr}\,\rho^2=1$ statements live on **p.576** (pure-state
>    property), **p.577** (Example 12.1) and **p.580** (Prob. 12.6(b) for the
>    general $\le1$ bound) — cited at their true pages above.
> 3. **"Partial trace" terminology.** Griffiths covers the *concept* (§12.3.3, the
>    "subsystem density matrix") but does **not** use the words "partial trace" or
>    develop the general $\mathrm{Tr}_B$ machinery; that formal operation is
>    standard quantum-information material, verified by its defining property in
>    `test_partial_trace_defining_property`.
> 4. **von Neumann entropy is not in Griffiths 3e** (the word "entropy" does not
>    appear in Ch. 12). $S=-\mathrm{Tr}(\rho\ln\rho)$ is standard (von Neumann
>    1927); cited unpinned to Sakurai below, and **the verification is the code**
>    ($S=0$ pure, $S=\ln d$ for $I/d$, unitary invariance).

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern Quantum Mechanics*, §3.4** *Density Operators
  and Pure Versus Mixed Ensembles* (and the entropy/Bloch-vector discussion) —
  `QM_Quantum_Mechanics/SakuraiQM.pdf` is an **image-only scan (no text layer**; confirmed
  `get_text()` returns nothing). Cited **unpinned**, never by page. This is the
  natural companion that *does* define the von Neumann entropy.
- **Cohen-Tannoudji, Diu & Laloë, *Quantum Mechanics* Vol. I, Complement E_III**
  (the density operator) — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf` is likewise
  **image-only** (confirmed). Cited **unpinned**.
- **`~QO-04` Open quantum systems** (`modules/QO/`, not yet built) — the Lindblad
  master equation generalizes §6's $i\hbar\dot\rho=[H,\rho]$ with dissipators that
  make decoherence irreversible. Bridge connects when QO-04 lands.
- **`~QM-21` Entanglement & foundations** (concurrent in this batch) — builds Bell
  inequalities and entanglement measures on §4's reduced-state mixedness;
  referenced by id only (no code import).
