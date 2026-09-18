# QM-06 — References

Page-level citations **verified by reading the page text** in the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module: printed folio == viewer
> page. Spot-checks used below — §3.4 "Generalized Statistical Interpretation"
> reads on viewer page 133, §1.5 "Momentum" on 32, §3.5.1 on 138 — each
> confirmed by extracting the page text before citing. Same scan as the rest of
> the QM trunk.

## Topic → location

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| Observable ↔ Hermitian operator; real-expectation argument forces $\hat A=\hat A^\dagger$ (`is_hermitian`) | Griffiths 3e | §3.2 Observables / §3.2.1 Hermitian Operators | 122–123 |
| Determinate state ⇒ eigenstate; $\sigma_A=0\Leftrightarrow\hat A\psi=q\psi$ (`variance`) | Griffiths 3e | §3.2.2 Determinate States | 125 |
| Eigenfunctions of a Hermitian operator: real eigenvalues, orthonormal & complete (discrete) (`eigensystem`, `eigenspaces`) | Griffiths 3e | §3.3 | 127 |
| **Generalized statistical interpretation** $P(a_n)=|\langle a_n\|\psi\rangle|^2$; collapse to the eigenstate (`outcome_probabilities`, `collapse`) | Griffiths 3e | §3.4 (Eq. 3.43) | **133** |
| Expectation two ways $\langle A\rangle=\sum a_nP(a_n)=\langle\psi\|\hat A\|\psi\rangle$ (`expectation`) | Griffiths 3e | §3.4 (Eqs. 3.48–3.51) | 134 |
| Expectation value first defined; ensemble caveat; operator "sandwich" $\langle Q\rangle=\int\Psi^*\hat Q\Psi$ | Griffiths 3e | §1.4 Normalization (p.29); §1.5 Momentum, Eqs. 1.28 & 1.36 | 29, 32–33 |
| Compatible vs incompatible observables; commuting ⇒ simultaneous eigenbasis (`commute`, `commutator`) | Griffiths 3e | §3.5 The Uncertainty Principle / §3.5.1 | 137–139 |

## Problems (verified, Griffiths 3e)
- **Problem 3.8** — show the eigenvalues of a Hermitian operator are real and its
  eigenfunctions (distinct eigenvalues) orthogonal — printed **p.129**.
- **Problem 3.16** — two noncommuting operators cannot have a *complete* set of
  common eigenfunctions (the incompatibility theorem) — printed **p.140**.
- **Problem 3.23** — projection operators are idempotent, $\hat P^2=\hat P$;
  find their eigenvalues/eigenvectors (underpins collapse) — printed **p.154**.
- **Problem 3.25** — a two-level-system Hamiltonian: find eigenvalues and
  eigenvectors (the spin-½ template) — printed **p.154**.
- **Problem 3.27** — spectral decomposition $\hat A=\sum_n a_n|a_n\rangle\langle
  a_n|$ — printed **p.154**.
- **Problem 3.33** — *Sequential measurements*: measure A, then B, then A again;
  probability of recovering the first A-value (the canonical disturbance
  problem) — printed **p.160**.

> **Honesty note (per the trunk's citation rule).** Every Griffiths page above
> was confirmed by extracting its text; the *content* of the page matches the
> claim it supports. Griffiths states the measurement postulates physically
> rather than as a numbered axiom list — the "postulate" framing in `notes.md`
> is the standard reading of §3.2–§3.4, with collapse stated verbatim on p.133
> ("the wave function collapses to the corresponding eigenstate"). The
> spin-½/Stern-Gerlach example used in the code lives in Griffiths Ch. 4 (Spin),
> developed in `~QM-11`; here it is used only as the cleanest finite-dimensional
> illustration, and the **verification is the code** — `test_measurement.py`
> checks $\sum P=1$, the two expectation routes, collapse idempotence, and the
> commuting/non-commuting disturbance against closed forms.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer**; confirmed `get_text()` returns nothing).
  Cite unpinned: Ch. 1 (kets, bras, operators; measurements, observables, and
  the uncertainty relations) — Sakurai's "Measurements" discussion (selective
  measurements / projection) is the natural companion to §5–§6 here.
- **Cohen-Tannoudji, Diu & Laloë, *Quantum Mechanics* Vol. I** —
  `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf` is likewise **image-only** (confirmed).
  Cite unpinned: Ch. III, "The postulates of quantum mechanics" (measurement
  postulates, reduction of the wave packet, compatible observables).
- Bethe & Jackiw, *Intermediate QM* (`QM_Quantum_Mechanics/BetheQM.pdf`, text-extractable) is
  an *applications* text and does not restate the measurement postulates; not
  cited here.
