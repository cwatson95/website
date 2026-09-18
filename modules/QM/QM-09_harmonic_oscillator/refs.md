# QM-09 — References

Page-level citations **verified by extracting the page text** in the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified for this module by reading the page text: printed
> p.57 begins "2.3 The Harmonic Oscillator", printed p.59 carries the "2.3.1
> Algebraic Method" heading, printed p.67 carries "2.3.2 Analytic Method" — each
> at viewer page = printed page. Consistent with the QM-trunk offset (folio =
> fitz index + 1).

## Topic → location (Griffiths 3e, all page-text-confirmed)

| Topic (code symbol) | Section | Printed p. |
|---|---|---|
| The harmonic oscillator: $V=\frac12 m\omega^2x^2$, TISE to solve | §2.3 | **57** |
| Two approaches announced (power series vs ladder operators) | §2.3 | **58** |
| **§2.3.1 Algebraic Method** heading; factoring $H$; ladder operators $a,a^\dagger$ defined (`annihilation`, `creation`) | §2.3.1 | **59** |
| Canonical commutation relation $[x,p]=i\hbar$; $H=\hbar\omega(a^\dagger a+\tfrac12)$ (`commutator`, `hamiltonian_matrix`) | §2.3.1 | **60** |
| Ladder operators raise/lower energy by $\hbar\omega$ | §2.3.1 | **61** |
| Lowest rung $a|0\rangle=0$; ground state $\psi_0$, $E_0=\tfrac12\hbar\omega$; allowed energies $E_n=\hbar\omega(n+\tfrac12)$ (`energy`, `zero_point_energy`) | §2.3.1 | **62** |
| $a^\dagger$ = adjoint of $a$; first excited state (Example 2.4) | §2.3.1 | **63** |
| $a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$, $a|n\rangle=\sqrt{n}\,|n-1\rangle$ (Eq. 2.66); orthonormality (Eq. 2.67) (`basis_vector`, `overlap`) | §2.3.1 | **64** |
| **§2.3.2 Analytic Method** heading; dimensionless $\xi=\sqrt{m\omega/\hbar}\,x$, $K=2E/\hbar\omega$ (`xi`) | §2.3.2 | **67** |
| Power-series solution; recursion formula (Eq. 2.82) | §2.3.2 | **68** |
| Series must terminate ⇒ $E_n=\hbar\omega(n+\tfrac12)$ recovered | §2.3.2 | **69** |
| Hermite polynomials $H_n$, Table 2.1; normalized $\psi_n$ (Eq. 2.85), "identical to the algebraic ones" (`psi`, `ground_state`) | §2.3.2 | **71** |

> **Note on the §2.3.1 page.** The dispatch listed the Algebraic Method at
> printed p.58; p.58 is where Griffiths *announces* the two approaches, and the
> numbered heading "2.3.1 Algebraic Method" together with the factoring of $H$
> actually begins on **p.59**. Both pages were read and are cited at their true
> locations above (a verified p.59 is better than an approximate p.58).

## Problems (verified, Griffiths 3e)
- **Problem 2.10** — construct $\psi_2$; sketch $\psi_0,\psi_1,\psi_2$; check their
  orthogonality by explicit integration — printed **p.65**.
- **Problem 2.11** — compute $\langle x\rangle,\langle p\rangle,\dots$ for
  $\psi_0,\psi_1$ by explicit integration — printed **p.65**.
- **Problem 2.12** — $\langle x\rangle,\langle p\rangle,\langle x^2\rangle,\langle
  p^2\rangle,\langle T\rangle,\langle V\rangle$ for the $n$th state via the ladder
  trick (Example 2.5); check the uncertainty principle — printed **p.66**.
- **Problem 2.14** — ground state: probability of finding the particle outside the
  classically allowed region (to 3 sig figs) — printed **p.72**.
- **Problem 2.15** — use the recursion (Eq. 2.85) to work out higher $H_n$ — printed **p.73**.
- **Problem 2.16** — Hermite-polynomial theorems: Rodrigues formula, the recursion
  $H_{n+1}=2\xi H_n-2nH_{n-1}$, the derivative relation, the generating function — printed **p.73**.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned. The oscillator via
  $a,a^\dagger$ is in **Ch. 2** (Quantum Dynamics).
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. I** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned (**Ch. V**, the one-dimensional
  harmonic oscillator, and its complements).
- **MA-12** (`modules/MA/MA-12_special_functions/`) — the physicists' Hermite
  polynomials $H_n$ this module imports, with their recurrence, weight
  $e^{-x^2}$, orthogonality $\int H_mH_n e^{-x^2}dx=2^n n!\sqrt\pi\,\delta_{mn}$,
  and ODE residual checks.
