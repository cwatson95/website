# QM-22 — References

Page-level citations **verified by reading the page text** in the PDF (extracted
with `fitz`, not eyeballed off a scan). **Printed** = the number printed on the
page; **PDF** = the page in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this Griffiths scan: the printed folio
> equals the viewer page throughout the body (read printed page `P` with
> `fitz.open(path)[P-1].get_text()`). The whole QM trunk uses this scan; the
> Dirac-equation mentions below were confirmed by extracting the page text.

## ⚠ Weak-coverage module — the verification is the CODE

**Griffiths 3e is a non-relativistic text.** Confirmed by full-text scan of all
644 pages:

- **"Klein–Gordon" → ZERO hits.** Griffiths never treats (or names) the
  Klein–Gordon equation. There is no page to cite, pinned or otherwise.
- **The Dirac equation appears only *in passing*,** in the fine-structure context
  of §7.3 — two verified mentions (below), never a derivation, no gamma matrices,
  no spinors.

So, exactly as `~QM-01_origins` handles black-body/Bohr (which precede Griffiths'
starting point), **the physics in `notes.md` is standard and correct, and the
verification lives in `code/test_relativistic.py`** — 18 checks of the Clifford
algebra, both dispersion relations, the spinor solutions and normalizations, and
the $g=2$ non-relativistic limit, each against a closed form (to machine precision
for the exact matrix identities; to the finite-difference floor $\sim10^{-6}$ for
the Klein–Gordon $\Box$ operator). The unpinned standard sources are Sakurai and
Bjorken–Drell (below).

## Topic → location (Griffiths 3e — the only genuine, verified mentions)

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| "The exact fine-structure formula for hydrogen (obtained **from the Dirac equation** without recourse to perturbation theory)" — Problem 7.22 | Griffiths 3e | §7.3 *Fine Structure of Hydrogen* / Prob. 7.22 | **388** |
| "the exact solution can be obtained by using the **(relativistic) Dirac equation** in place of the (nonrelativistic) Schrödinger equation… (see Problem 7.22)" — footnote | Griffiths 3e | §7.3 (footnote 18) | **415** |
| Fine structure = relativistic correction + spin–orbit (the NR expansion this module derives; `nonrel_energy`, `energy_expansion`) — context for the `~QM-17` bridge | Griffiths 3e | §7.3 *The Fine Structure of Hydrogen* | **378** |

> **Honesty note.** The two Dirac mentions (p.388, p.415) are exactly that —
> *mentions*: Griffiths derives hydrogen's fine structure by perturbation theory
> and points to the Dirac equation only as the rigorous source whose expansion
> reproduces his result. That expansion (relativistic kinetic correction
> $-p^4/8m^3$ + spin–orbit, opening into `~QM-17`) is the §3 limit of this module,
> so these are the *correct* and *honest* places to cite Griffiths. Everything
> else — the Klein–Gordon equation, the gamma/Clifford algebra, 4-spinors, the
> $g=2$ derivation — is **not** in Griffiths and is verified by the code.

## Problems (in `problems/problems.md`)
- **P1** — Klein–Gordon dispersion & negative energies *(code-verified; no Griffiths page)*
- **P2** — the Clifford algebra forces $(\gamma^0)^2=+\mathbb1$, $(\gamma^i)^2=-\mathbb1$ *(code)*
- **P3** — $\det(\not{\!p}-m)=(p\cdot p-m^2)^2$ and $\text{Dirac}^2=\text{KG}$ *(code)*
- **P4** — construct & verify the four plane-wave spinors *(code)*
- **P5** — the $g=2$ magnetic moment from the non-relativistic limit *(code)*
- **P6** — leading relativistic energy correction $-p^4/8m^3$ → fine structure
  *(Griffiths §7.3, p.378; "exact" from the Dirac equation, Prob. 7.22, p.388)*

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern Quantum Mechanics*** — `QM_Quantum_Mechanics/SakuraiQM.pdf`
  is an **image-only scan (no text layer)**; cite **unpinned**: **Ch. 8,
  *Relativistic Quantum Mechanics*** (Klein–Gordon, the Dirac equation, gamma
  matrices, the non-relativistic limit and $g=2$). The standard graduate treatment
  of everything in this module.
- **Bjorken & Drell, *Relativistic Quantum Mechanics*** — the classic dedicated
  text (off-shelf / not in this repo); cite **unpinned**: Ch. 1–3 (Dirac equation,
  Lorentz covariance, plane-wave solutions and the hole theory). Uses the same
  Dirac representation and mostly-minus metric as this module.
- **Peskin & Schroeder, *An Introduction to QFT*** — Ch. 3 for the spinor algebra
  and normalizations $\bar u u=2m$, $\bar v v=-2m$; the forward bridge to `~QF-01`.
- `~MA-18` (this repo) — the Clifford / gamma-matrix algebra; the test cross-checks
  the Pauli matrices against MA-18's `pauli()`.
