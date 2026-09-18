# QM-03 — References

Page-level citations **verified by reading the page text** in the PDF (not a
table of contents). **Printed** = the number on the page; **PDF** = the page in
the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified for every page cited below: the printed folio equals
> the viewer page (e.g. §1.1 heading on printed 16 = viewer 16; §2.1 on printed
> 43 = viewer 43; §2.3 on printed 57 = viewer 57). The whole QM trunk uses this
> scan. To read printed page $P$: `fitz.open(path)[P-1].get_text()`.

## Topic → location (all verified by extracting the page text)

| Topic (code symbol) | Section | Printed p. |
|---|---|---|
| TDSE $i\hbar\,\partial_t\Psi=\hat H\Psi$, Eq. 1.1 (`hamiltonian`) | Gr §1.1 *The Schrödinger Equation* | **16** |
| Separation of variables; TISE $\hat H\psi=E\psi$ (`solve`) | Gr §2.1 *Stationary States* | **43** |
| Separable $\langle H\rangle=E$, $\sigma_H=0$; "general solution = linear combination of separable solutions" | Gr §2.1 | **45** |
| $\Psi=\sum c_n\psi_n e^{-iE_nt/\hbar}$ (the "wiggle factor"); stationary states have time-independent probabilities (`evolve`, `stationary_state`) | Gr §2.1 | **46** |
| $\|c_n\|^2$ = probability of energy $E_n$; $\sum\|c_n\|^2=1$; $\langle H\rangle=\sum\|c_n\|^2E_n$ (energy conservation) (`coefficients`) | Gr §2.1 | **47** |
| Infinite square well — setup (`make_grid` Dirichlet walls) | Gr §2.2 *The Infinite Square Well* | **49** |
| Well energies $E_n=n^2\pi^2\hbar^2/2ma^2$ (Eq. 2.30) & eigenfunctions $\psi_n=\sqrt{2/a}\,\sin(n\pi x/a)$ (Eq. 2.31) (`infinite_well_energy`, `infinite_well_eigenfunction`) | Gr §2.2 | **50** |
| Orthonormality $\langle\psi_m\|\psi_n\rangle=\delta_{mn}$, completeness, **Fourier's trick** (`inner_product`, `coefficients`) | Gr §2.2 | **51** |
| Harmonic oscillator $E_n=(n+\tfrac12)\hbar\omega$ (`harmonic_oscillator_energy`, cross-link `~QM-09`) | Gr §2.3 *The Harmonic Oscillator* | **57** |

## Problems (verified, Griffiths 3e)
- **Problem 2.1** — three theorems: the separation constant $E$ must be real, and
  the time-independent $\psi$ can always be taken real — printed **p.47**.
- **Problem 2.5** — a particle in the infinite well started as an even mixture of
  the first two stationary states $\Psi(x,0)=A[\psi_1+\psi_2]$: normalize, find
  $\Psi(x,t)$ and $|\Psi(x,t)|^2$, show $\langle x\rangle$ oscillates and give its
  **angular frequency**, and find the energy probabilities $|c_n|^2$ and
  $\langle H\rangle$ — printed **p.55**. (This is exactly the superposition the
  code builds and times.)

## Further reading (not page-verified here)
- Sakurai & Napolitano, *Modern QM* — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an **image-only
  scan (no text layer)**; cite unpinned (Ch. 2, *Quantum Dynamics* — the
  Schrödinger vs Heisenberg pictures and time evolution).
- Cohen-Tannoudji, *Quantum Mechanics* Vol. I — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned (Ch. III, the postulates and the
  Schrödinger equation; Complement $G_{III}$ on stationary states).

> **Honesty note (per the trunk's citation rule).** Every printed page in the
> tables above was confirmed by extracting its text from the Griffiths 3e PDF
> before citing. Sakurai and Cohen-Tannoudji are image-only on this shelf, so
> they are cited at chapter level **without** page numbers. The numerical
> claims (well spectrum, frozen $|\Psi|^2$, beat period, $\sum|c_n|^2=1$, the SHO
> ladder) are not page-citations at all — **the verification is the code**, where
> each is reproduced from the finite-difference Hamiltonian and checked against
> its closed form in `test_schrodinger.py`.
