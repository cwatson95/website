# QM-07 — References

Page-level citations **verified by reading the page text** in the PDF (not a
table of contents). **Printed** = the number on the page; **PDF** = the page in
the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module: printed folio equals the
> viewer page — read printed page $P$ with `fitz.open(path)[P-1].get_text()`.
> Confirmed on pp.33–36 (§1.5–1.6), pp.137–142 (§3.5), and pp.120 / 594 (§3.1
> inner products / §A.2 & Problem A.5, the Schwarz inequality), each containing
> the heading/equation cited below. The whole QM trunk uses this scan.

## Topic → location

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| $\sigma_x\sigma_p\ge\hbar/2$, the position–momentum trade-off (`uncertainty_product`) | Griffiths 3e | §1.6 *The Uncertainty Principle* | 35 |
| Generalized uncertainty principle, statement & motivation | Griffiths 3e | §3.5 *The Uncertainty Principle* | 137 |
| **Proof** of $\sigma_A\sigma_B\ge\tfrac12\lvert\langle[\hat A,\hat B]\rangle\rvert$ (`generalized_bound`, `commutator`) | Griffiths 3e | §3.5.1 *Proof of the Generalized Uncertainty Principle* | 138 |
| **Schwarz inequality** stated (integral form, Eq. 3.7; inner-product axioms Eqs. 3.6–3.9) (`schwarz_gap`) | Griffiths 3e | §3.1 *Hilbert Space* | 120 |
| Schwarz inequality, abstract statement (Eq. A.27) and the **proof by projection** — "Let $h=g-\frac{\langle f\vert g\rangle}{\langle f\vert f\rangle}f$ and use $\langle h\vert h\rangle\ge0$" (`schwarz_residual_identity`) | Griffiths 3e | §A.2 *Inner Products*, **Problem A.5** (Gram–Schmidt projection: Problem A.4) | 594 |
| Endnote to Ch. 3: the finite-dimensional Schwarz proof deferred to Problem A.5 (footnote 5) | Griffiths 3e | Ch. 3 endnotes | 167 |
| $\sigma_x\sigma_p\ge\hbar/2$ recovered as an application; incompatible/compatible observables | Griffiths 3e | §3.5 (cont., Eq. 3.62–3.63) | 139 |
| Minimum-uncertainty wave packet is a **Gaussian** (`gaussian_packet`) | Griffiths 3e | §3.5.2 *The Minimum-Uncertainty Wave Packet* | 141 |
| Ehrenfest rate $d\langle x\rangle/dt=\langle p\rangle/m$ (`split_step_evolve`) | Griffiths 3e | §1.5 *Momentum* (Eq. 1.33) | 33 |
| **Ehrenfest's theorem** named; $d\langle p\rangle/dt=-\langle V'\rangle$ ("expectation values obey the classical laws") | Griffiths 3e | §1.5, **Problem 1.7** | 34 |
| Energy–time uncertainty $\Delta t\,\Delta E\ge\hbar/2$ (further reading) | Griffiths 3e | §3.5.3 *The Energy-Time Uncertainty Principle* | 142 |

> **Note (per the trunk's citation rule).** Griffiths gives the *physics* (the
> bound, its proof, the Gaussian, Ehrenfest's theorem) but no numerical
> demonstration; the **verification here is the code**, where the Gaussian's
> $\hbar/2$, the oscillator's $(n+\tfrac12)\hbar$, the spin bound
> $(\hbar/2)\lvert\langle S_z\rangle\rvert$, and the two Ehrenfest rates are all
> checked against closed forms in `test_uncertainty.py`. The split-step Fourier
> evolution and the spin-$\tfrac12$ example are standard but are not in Griffiths
> as such.

## Problems (verified, Griffiths 3e)
- **Problem A.5** — prove the Schwarz inequality (Eq. A.27); the hint *is* the
  projection construction our P8 and `schwarz_residual_identity` implement —
  printed **p.594**.
- **Problem 1.7** — compute $d\langle p\rangle/dt$; "an instance of Ehrenfest's
  theorem" — printed **p.34**.
- **Problem 1.9** — for a given $\psi$, find $\sigma_x,\sigma_p$ and check their
  product against the uncertainty principle — printed **p.36**.
- **Problem 3.14** — commutator identities, $[\hat x^n,\hat p]$, $[f(\hat x),\hat p]$,
  and the SHO relations (the algebra behind both the bound and Ehrenfest) —
  starts printed **p.139**, continues **p.140**.
- **Problem 3.15** — the energy–time ("(your name)") uncertainty principle —
  printed **p.140**.
- **Problem 3.16** — two noncommuting operators cannot share a complete set of
  eigenfunctions — printed **p.140**.
- **Problem 3.17** — solve the minimum-uncertainty ODE; the solution is a
  Gaussian — printed **p.141**.

## Further reading (not page-verified here)
- Sakurai & Napolitano, *Modern QM* — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an **image-only
  scan (no text layer)**; cite unpinned (Ch. 1: the generalized uncertainty
  relation and the Schwarz-inequality proof; the spin-$\tfrac12$ examples).
- Cohen-Tannoudji, *Quantum Mechanics* Vol. I — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned (Ch. III: observables, the mean value
  and root-mean-square deviation; the Ehrenfest theorem complement).
- Bethe & Jackiw, *Intermediate Quantum Mechanics* — `QM_Quantum_Mechanics/BetheQM.pdf` (has a
  text layer) is intermediate-level and assumes these basics rather than
  re-deriving them; cite by section if used.
- The Schrödinger uncertainty relation (the stronger form with the covariance /
  anticommutator term that makes Robertson strict) is beyond Griffiths; see the
  spin example in `code` for a state where the Robertson bound is *not* saturated.
