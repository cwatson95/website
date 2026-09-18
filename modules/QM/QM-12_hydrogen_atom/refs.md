# QM-12 — References

Page-level citations **verified by reading the page text** in the PDF (extracted
with `fitz`, not eyeballed off a scan). **Printed** = the number printed on the
page; **PDF** = the page in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this scan: the printed folio equals
> the viewer page throughout the body (read printed page `P` with
> `fitz.open(path)[P-1].get_text()`). Confirmed on every page cited below.

> **Anchor corrections (per the trunk's "a wrong page is worse than none" rule).**
> The dispatch's anchor *"§4.2.1 The Radial Equation, ~p.180–186"* mixes two
> sections. Reading the pages shows: the general **radial equation** is **§4.1.3
> The Radial Equation, p.180** (NOT §4.2.1); **§4.2 The Hydrogen Atom** opens on
> **p.185**; and **§4.2.1 The Radial Wave Function** (the κ/ρ asymptotic solution)
> is **p.187**. The $E_n$ "Bohr formula" is **Eq. 4.70, p.189** (named on p.190).
> The Spectrum-of-Hydrogen anchor "p.199" is right for Fig. 4.10; the section
> heading **§4.2.2 The Spectrum of Hydrogen is p.198**. Pages below are the
> corrected, verified ones.

## Topic → location (Griffiths 3e — the primary source)

| Topic (code symbol) | Section / Eq. | Printed p. |
|---|---|---|
| 3-D Schrödinger eq.; separation of variables begins | §4.1 *The Schrödinger Equation* | 171 |
| $\psi=R(r)Y_l^m$; angular part same for all central $V$; **the radial equation**; effective potential + **centrifugal term** $l(l+1)\hbar^2/2mr^2$; $u=rR$, $u(0)=0$ (`effective_potential`,`radial_solve`) | §4.1.3 *The Radial Equation*, Eq. 4.37–4.38 | 180 |
| Infinite spherical well; "radial wave function has $N$ nodes" | §4.1.3 | 181 |
| **§4.2 The Hydrogen Atom**; Coulomb potential $V=-e^2/4\pi\varepsilon_0 r$ (Eq. 4.52); effective potential (Fig. 4.5) | §4.2 | 185 |
| Radial wave function: $\kappa=\sqrt{-2mE}/\hbar$, $\rho=\kappa r$, asymptotics | §4.2.1 *The Radial Wave Function*, Eq. 4.54–4.60 | 187 |
| Power-series solution; recursion formula | §4.2.1, Eq. 4.61–4.76 | 188 |
| Series **must terminate** $\Rightarrow$ quantized $\kappa$; **allowed energies $E_n$** (`coulomb_energy`) | §4.2.1, **Eq. 4.70** | 189 |
| "the famous Bohr formula"; **Bohr radius $a_0$** (Eq. 4.72); three quantum numbers $(n,l,m)$, $R_{nl}$ a polynomial of degree $n-l-1$ (Eq. 4.75); ground state, **13.6 eV** binding energy (`BOHR_RADIUS`,`radial_wavefunction`) | §4.2.1, Eq. 4.70–4.75 | 190 |
| **$l=0..n-1$**, $2l+1$ values of $m$, **degeneracy $=n^2$**; Fig. 4.6 (`allowed_l`,`m_values`,`degeneracy`,`count_states`) | §4.2.1, Eq. 4.84–4.85 | 191 |
| $R_{nl}$ via **associated Laguerre** $L_{n-l-1}^{2l+1}$ (Eq. 4.87–4.88); normalized $R_{nl}$ (Eq. 4.89); Fig. 4.6 "accidental" degeneracy (`generalized_laguerre`,`radial_wavefunction`) | §4.2.1 | 192 |
| Orthogonality $\int R_{nl}R_{n'l}r^2dr=\delta$ (Eq. 4.90); Tables 4.5–4.7 (Laguerre, assoc. Laguerre, $R_{nl}$) | §4.2.1, Eq. 4.90 | 193 |
| Quantum numbers from the nodes; **radial nodes $=n-l-1$** (`count_radial_nodes`) | §4.2.1 | 195 |
| **§4.2.2 The Spectrum of Hydrogen**; $E_\gamma=E_i-E_f$; **Rydberg formula** (Eq. 4.93) & constant (Eq. 4.94) | §4.2.2, Eq. 4.91–4.94 | 198 |
| Fig. 4.10 energy levels & transitions; Bohr energies / hydrogenic scaling (Problem 4.19) | §4.2.2 | 199 |

## Problems (verified, Griffiths 3e)
- **Problem 4.12** — work out $v(\rho)$ for $R_{20},R_{21},R_{31}$ from the
  recursion formula — printed **p.196**.
- **Problem 4.13** — normalize $R_{20}$ and $R_{21}$; construct $\psi_{200}$ etc. —
  printed **p.196**.
- **Problem 4.14** — first four Laguerre polynomials; build $R_{nl}$ two ways
  (Eq. 4.88 vs the recursion) — printed **p.196**.
- **Problem 4.15(a)** — find $\langle r\rangle$ and $\langle r^2\rangle$ in the
  ground state; express in Bohr radii ($\langle r\rangle=\tfrac32 a_0$) — printed
  **p.197** (the `expectation_r` check).
- **Problem 4.16** — most probable value of $r$ in the ground state ($=a_0$, not
  zero) — printed **p.197** (the `radial_probability` peak).
- **Problem 4.19** — hydrogenic atom (nuclear charge $Ze$): scale the Bohr
  energies, radius, and Rydberg constant — printed **p.199**.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned: the central-potential /
  Coulomb problem and the SO(4) symmetry behind the accidental degeneracy.
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. I** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned: Ch. VII (particle in a central
  potential; the hydrogen atom) and its complements.
- `~MA-12` (this repo) — Laguerre and associated Legendre polynomials, the
  special-function prerequisite; `code/test_hydrogen.py` imports its `laguerre`
  to verify that scipy's generalized Laguerre at $\alpha=0$ matches it.
- `~QM-10` (this repo) — the spherical harmonics $Y_l^m$, the angular factor.

> **Honesty note.** The hydrogen atom is *core* Griffiths and is derived there
> from first principles (§4.1.3, §4.2) — every formula in `notes.md` sits on a
> page verified above. The one construction Griffiths does **not** print is the
> finite-difference radial eigensolver `radial_solve`; that is a standard
> numerical method (the symmetric-tridiagonal scheme of `~QM-08`/`~MA-20`), and
> the code **verifies** it by reproducing the analytic $E_n$ (Eq. 4.70) and
> $rR_{nl}$ (Eq. 4.89). The $\langle r\rangle$ closed form is the result of
> Griffiths Problem 4.15a, confirmed numerically in the tests.
