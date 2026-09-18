# QM-14 — References

Page-level citations **verified by extracting the page text** from the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module: the printed folio equals
> the viewer page. Folio 251 is the "5 Identical Particles" chapter-title page;
> folio 256 carries the "5.1.1 Bosons and Fermions" head and the Pauli paragraph;
> folio 259 carries "5.1.2 Exchange Forces"; folio 264 carries "5.1.4 Generalized
> Symmetrization Principle." To read printed page $P$:
> `fitz.open(path)[P-1].get_text()`.

## Topic → location (all printed pages confirmed by reading the page)

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| Identical Particles (chapter) | Griffiths 3e | **Ch. 5** (title page) | 251 |
| Two-particle systems; product state $\psi_a(1)\psi_b(2)$ (Eq. 5.9); entanglement; the helium Hamiltonian | Griffiths 3e | §5.1 *Two-Particle Systems* | 252–253 |
| Indistinguishability; **bosons (+) symmetric vs fermions (−) antisymmetric** (Eqs. 5.16–5.18); spin–statistics axiom (`symmetrize`, `antisymmetrize`) | Griffiths 3e | §5.1.1 *Bosons and Fermions* | 256 |
| **Pauli exclusion principle** — $\psi_a=\psi_b\Rightarrow\Psi_-=0$ (`antisymmetrize(a,a)=0`) | Griffiths 3e | §5.1.1 | 256 |
| Example 5.1 — two noninteracting particles in the infinite square well | Griffiths 3e | §5.1.1 | 256–257 |
| **Exchange forces** — $\langle(x_1-x_2)^2\rangle$ for dist./boson/fermion (Eqs. 5.19–5.23) (`exchange_dx2`) | Griffiths 3e | §5.1.2 *Exchange Forces* | 259 |
| Exchange term $\mp2\,\lvert\langle x\rangle_{ab}\rvert^2$ and $\langle x\rangle_{ab}=\int x\,\psi_a^*\psi_b$ (Eqs. 5.24–5.26); "no overlap → no effect"; "not really a force" (`position_moments`) | Griffiths 3e | §5.1.2 | 260–261 |
| **Slater determinant** for totally antisymmetric $N$-particle states ("works for any number of particles") (`slater_determinant`) | Griffiths 3e | **Problem 5.8** | 262 |
| Spin; singlet (antisymmetric) ↔ symmetric spatial, triplet (symmetric) ↔ antisymmetric spatial; **helium $1s^2$ needs the singlet** (`singlet`, `triplet`) | Griffiths 3e | §5.1.3 *Spin* | 263 |
| **Exchange operator** $P$, $P^2=1$, eigenvalues $\pm1$; symmetrization axiom $P\Psi=\pm\Psi$ (Eqs. 5.30–5.34) (`swap_operator`, `apply_pair_swap`) | Griffiths 3e | §5.1.4 *Generalized Symmetrization Principle* | 264 |
| Atoms: $Z$-electron Hamiltonian (Eq. 5.36); helium & higher atoms | Griffiths 3e | §5.2 *Atoms* | 267 |
| **Periodic table**; carbon ground state $^3P_0$; Hund's rules; Table 5.1 | Griffiths 3e | §5.2.2 *The Periodic Table* | 272 |

> **Honesty note (per the trunk's citation rule).** Several of Griffiths'
> *displayed, numbered equations* in this chapter (e.g. the explicit symmetric/
> antisymmetric forms $\Psi_\pm$ of Eq. 5.17, and the exchange operator action of
> Eq. 5.30) are typeset as **embedded images** in this scan, so `get_text()`
> returns the surrounding prose and the equation *numbers* but not the formula
> glyphs. Every page above was confirmed by the **prose that names the result** —
> e.g. p.256 literally reads *"bosons (the plus sign), and fermions (the minus
> sign)… Boson states are symmetric under interchange… fermion states are
> antisymmetric"* and *"This is the famous Pauli exclusion principle"*; p.260
> *"identical bosons… tend to be somewhat closer together, and identical fermions…
> somewhat farther apart"*; p.262 *"Form the Slater determinant… this device works
> for any number of particles."* The formula *values* are the standard ones and
> are **verified numerically in `code/test_identical.py`**, not taken on faith
> (the exchange-force numbers against the closed forms of Problems 5.6 & 5.7).

## Problems (verified, Griffiths 3e)
- **Problem 5.4** — the normalization constant $A$ for the symmetric/antisymmetric
  pair (orthonormal case, and the boson $a=b$ case) — printed **p.257**.
- **Problem 5.5** — Hamiltonian and excited states for two identical particles in
  the infinite well (distinguishable / boson / fermion) — printed **p.257**.
- **Problem 5.6** — $\langle(x_1-x_2)^2\rangle$ in the infinite well for one
  particle in $\psi_1$ and one in $\psi_2$, for the three cases — printed
  **p.261**. *(Closed form checked in `test_exchange_force_infinite_well_closed_form`.)*
- **Problem 5.7** — two particles in a shared harmonic oscillator (ground + first
  excited); $\langle(x_1-x_2)^2\rangle$ for the three cases — printed **p.261**.
  *(Closed form checked in `test_exchange_force_harmonic_oscillator_closed_form`.)*
- **Problem 5.8** — three particles; construct the distinguishable/boson/fermion
  states and the **Slater determinant** — printed **p.262**.
- **Problem 5.10** — three spin-1/2 particles: no totally antisymmetric spatial
  state; the well ground state via a Slater determinant — printed **pp.264–265**.

## Further reading (not page-verified here)
- Sakurai & Napolitano, *Modern Quantum Mechanics*, **Ch. 7** (Identical
  Particles; permutation symmetry, Young tableaux) — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cited unpinned, never by page.
- Cohen-Tannoudji, *Quantum Mechanics* Vol. II, **Ch. XIV** (systems of identical
  particles; the symmetrization postulate) — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf` is
  likewise **image-only**; cited unpinned.
- **Spin–statistics theorem** (integer spin ↔ boson, half-integer ↔ fermion): a
  result of relativistic QFT (`~QF-01`), *assumed* in nonrelativistic QM
  (Griffiths p.256). Quantum statistics of the resulting gases is `~SM-04`
  (Bose–Einstein & Fermi–Dirac), *not yet built*.
