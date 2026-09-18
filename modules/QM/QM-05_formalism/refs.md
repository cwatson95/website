# QM-05 — References

Page-level citations **verified by extracting the page text** from the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module: the printed folio equals
> the viewer page (folio 119 = §3.1 at viewer 119; folio 152 = §3.6.2 at viewer
> 152; folio 59–60 = the commutator/canonical-commutator at viewer 59–60). To
> read printed page $P$: `fitz.open(path)[P-1].get_text()`.

## Topic → location (all printed pages confirmed by reading the page)

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| States are vectors; "natural language of QM is linear algebra" | Griffiths 3e | §3.1 *Hilbert Space* | 119 |
| Inner product $\langle f\|g\rangle$ (Eq. 3.6); orthonormal & complete sets; $\langle\phi\|\psi\rangle=\langle\psi\|\phi\rangle^{*}$ (`inner_product`, `norm`) | Griffiths 3e | §3.1 | 120 |
| Observables (section head) | Griffiths 3e | §3.2 *Observables* | 122 |
| Hermitian operators: real $\langle Q\rangle$ $\Rightarrow$ $Q=Q^\dagger$ (Eqs. 3.13, 3.16–3.17) (`is_hermitian`, `expectation`) | Griffiths 3e | §3.2.1 *Hermitian Operators* | 123 |
| $\hat x$, $\hat H$ Hermitian; $(AB)^\dagger=B^\dagger A^\dagger$ (`dagger`) | Griffiths 3e | Problems 3.4(d), 3.5(b) | 124 |
| Determinate states = eigenstates; the eigenvalue equation | Griffiths 3e | §3.2.2 *Determinate States* | 125 |
| Eigenfunctions of a Hermitian operator (discrete vs continuous) | Griffiths 3e | §3.3 | 127 |
| **Spectral theorem:** Thm 1 real eigenvalues, Thm 2 orthogonal eigenvectors (`spectral_decomposition`) | Griffiths 3e | §3.3.1 *Discrete Spectra* | 128 |
| Commutator $[A,B]=AB-BA$ (Eq. 2.48) (`commutator`) | Griffiths 3e | §2.3.1 *Algebraic Method* | 59 |
| **Canonical commutation relation** $[\hat x,\hat p]=i\hbar$ (Eq. 2.52) (`canonical_commutator`) | Griffiths 3e | §2.3.1 | 60 |
| Ladder operators (raising/lowering); $a^\mp$ = hermitian conjugate of $a^\pm$ | Griffiths 3e | §2.3.1 | 61, 63 |
| $\hat x,\hat p$ in terms of raising/lowering operators (Eq. 2.48 reused) (`position_operator`, `momentum_operator`) | Griffiths 3e | Example 2.5 | 65 |
| Generalized uncertainty principle; **compatible (commuting) observables share simultaneous eigenfunctions**, incompatible ones do not | Griffiths 3e | §3.5 | 139 |
| Dirac notation: bra, ket, dual space; projector $\|n\rangle\langle n\|$; completeness $\sum_n\|n\rangle\langle n\|=I$ (`projector`, resolution of identity) | Griffiths 3e | §3.6.2 *Dirac Notation* | 152 |
| Operators: sum and product; Dirac form of the Hermitian condition | Griffiths 3e | §3.6.2 | 153 |

> **Honesty notes.**
> 1. Several of Griffiths' *displayed, numbered equations* (e.g. the explicit
>    forms of $\hat x,\hat p$ in terms of $a^\pm$, and $a^\pm|n\rangle=\sqrt{\,}|n\pm1\rangle$)
>    are typeset as embedded images in this scan, so `get_text()` returns the
>    surrounding prose and equation *numbers* but not the formula glyphs. Every
>    page above was confirmed by the **prose that names the result** (e.g. p.60
>    literally reads *"known as the canonical commutation relation"*; p.63 *"is
>    the hermitian conjugate (or adjoint) of"*; p.139 *"compatible (commuting)
>    observables do admit complete sets of simultaneous eigenfunctions"*). The
>    formula *values* are the standard ones, and are themselves **verified
>    numerically in `code/test_formalism.py`**, not taken on faith.
> 2. The finite-dimensional impossibility of $[\hat x,\hat p]=i\hbar I$
>    (zero-trace argument; Wintner 1947 / Wielandt 1949) is a **mathematical
>    theorem, not a Griffiths citation** — it is listed under *Further reading*
>    below and proved in `notes.md` §7 and the test
>    `test_canonical_commutator_truncation_artifact`.

## Problems (verified, Griffiths 3e)
- **Problem 3.4(d)** — show $\hat x$ and $\hat H$ are Hermitian — printed **p.124**.
- **Problem 3.5(b)** — $(\hat Q\hat R)^\dagger=\hat R^\dagger\hat Q^\dagger$, hermitian conjugates — printed **p.124**.
- **Problem 3.16** — incompatible observables cannot share a *complete* set of eigenfunctions (referenced from §3.5) — printed **p.139** (statement); problem itself in the §3.5 problem set.

## Further reading (not page-verified here)
- Sakurai & Napolitano, *Modern Quantum Mechanics*, **Ch. 1** (kets, bras,
  operators; the fundamental commutation relations) — `QM_Quantum_Mechanics/SakuraiQM.pdf` is
  an **image-only scan (no text layer)**; cited unpinned, never by page.
- Cohen-Tannoudji, *Quantum Mechanics* Vol. I, **Ch. II** (the mathematical tools:
  state space, Dirac notation, observables) — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf` is
  likewise **image-only**; cited unpinned.
- **No finite-dimensional representation of the CCR:** A. Wintner, *Phys. Rev.*
  **71**, 738 (1947); H. Wielandt, *Math. Ann.* **121**, 21 (1949). The trace
  argument ($\mathrm{tr}[A,B]=0\neq\mathrm{tr}(i\hbar I)$) is the elementary form
  used in `notes.md` §7.
- `~MA-04` (`modules/MA/MA-04_linear_algebra/`) — vector spaces, the eigenvalue
  problem, diagonalization; its pure-Python real-symmetric Jacobi solver is
  cross-checked against this module's `numpy.linalg.eigh` in
  `test_cross_check_MA04_eigensolver`.
