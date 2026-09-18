# QM-10 — References

Page-level citations **verified by reading the page text** in the PDF (extracted,
not eyeballed off a scan). **Printed** = the number printed on the page; **PDF** =
the page in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |
| Bethe & Jackiw, *Intermediate Quantum Mechanics*, 3rd ed. | `QM_Quantum_Mechanics/BetheQM.pdf` | PDF = printed **+ 19** |

> **Offset notes.**
> *Griffiths:* the printed folio equals the viewer page throughout the body (the
> whole QM trunk uses this scan; read printed page `P` with `fitz.open(path)[P-1]`).
> *Bethe:* verified empirically — fitz index 30/31/32 carry printed folios
> 12/13/14, so `fitz_index = printed + 18` (equivalently PDF viewer page =
> printed + 19); read printed page `P` with `fitz.open(path)[P+18]`. Confirmed on
> three consecutive folios.

## Topic → location (Griffiths 3e — the primary source)

| Topic (code symbol) | Section | Printed p. |
|---|---|---|
| Classical $\mathbf L=\mathbf r\times\mathbf p$; operators via $\mathbf p\to-i\hbar\nabla$ (`Lx`,`Ly`,`Lz`) | §4.3 *Angular Momentum* | 201 |
| $[L_x,L_y]=i\hbar L_z$ and cyclic (Eq. 4.99) (`commutator`) | §4.3.1 *Eigenvalues* | 202 |
| $L^2=L_x^2+L_y^2+L_z^2$; $[L^2,L_i]=0$ (Eq. 4.101–4.103) (`L_squared`) | §4.3.1 | 202 |
| Ladder operators $L_\pm=L_x\pm iL_y$; $[L_z,L_\pm]=\pm\hbar L_\pm$ (Eq. 4.105) (`L_plus`,`L_minus`) | §4.3.1 | 203 |
| Top/bottom rung terminate the ladder | §4.3.1 | 203–204 |
| Spectrum $L^2\to\hbar^2 l(l+1)$, $L_z\to\hbar m$, $m=-l..l$ ($2l+1$ states); $l$ integer **or half-integer**; Fig. 4.12 for $l=2$ (Eq. 4.118–4.119) (`casimir_eigenvalue`,`m_values`) | §4.3.1 | 205 |
| Ladder matrix element $\hbar\sqrt{l(l+1)-m(m\pm1)}$ (`ladder_coeff`) (Problem 4.21) | §4.3.1 / Prob. 4.21 | 206 |
| "The eigenfunctions of $L^2$ and $L_z$ are the spherical harmonics" (the §4.1↔§4.3 link) | §4.3.1 (end) | 206 |
| The angular equation; $\Phi=e^{im\phi}$, $m$ integer from single-valuedness (Eq. 4.21–4.22) | §4.1.2 *The Angular Equation* | 176 |
| Associated Legendre $P_l^m(\cos\theta)$ (Eq. 4.27) (← `~MA-12` `assoc_legendre`) | §4.1.2 | 177 |
| Spherical harmonics $Y_l^m$ (Eq. 4.32); orthonormality (Eq. 4.33); Table 4.3 (`spherical_harmonic`,`sphere_inner_product`) | §4.1.2 | 178 |
| $L_z=-i\hbar\,\partial/\partial\phi$ in spherical coordinates (Eq. 4.129) (`Lz_on_Y`) | §4.3.2 *Eigenfunctions* | 208 |

## Topic → location (Bethe & Jackiw — verified extra source)

| Topic | Section | Printed p. |
|---|---|---|
| $[J_a,J_b]=i\,\epsilon_{abc}J_c$ (Eq. 1-27); $[J_a,J^2]=0$, $J^2=J_x^2+J_y^2+J_z^2$ (1-28); simultaneous $J^2,J_z$ with $m=-j..j$ in unit steps, $J^2=j(j+1)$; $J_+=J_x+iJ_y$ with element $\sqrt{(j-m)(j+m+1)}$ (1-29) | §1 *Quantum Mechanical Results / Constants of Motion* | 13 |
| Half-integer angular momentum = spin ("$J_z$ no longer $-i\,\partial/\partial\phi$"); $S^2=s(s+1)$, $S_z=m_s$; integer/half-integer forced by commutators + Hermiticity (1-31) | §1 | 14 |

> **Honesty note (per the trunk's citation rule).** Unlike the old-quantum-theory
> topics of `QM-01`, angular momentum is *core* Griffiths and is treated from
> first principles there: §4.3.1 derives the eigenvalues algebraically and
> §4.1.2/§4.3.2 the spherical harmonics — every formula in `notes.md` is on a
> page verified above. The one thing Griffiths does **not** print is the explicit
> $(2l+1)\times(2l+1)$ matrices for general $l$ that `angular_momentum.py` builds
> (it writes matrices out only for spin-$\tfrac12$ in §4.4); those are the
> standard representation assembled from the ladder matrix element of Problem 4.21
> (p.206) and the spectrum of Eq. 4.119 (p.205), and the code **verifies** the
> algebra they must satisfy to machine precision. The Bethe citations are an
> independent confirmation of the same algebra (note Bethe's
> $\sqrt{(j-m)(j+m+1)}=\sqrt{j(j+1)-m(m+1)}$, identical to `ladder_coeff`).

## Problems (verified, Griffiths 3e)
- **Problem 4.4** — construct spherical harmonics from Eqs. 4.27/4.28/4.32; check
  normalized and orthogonal — printed **p.179**.
- **Problem 4.5** — the "unacceptable second solution" of the $\theta$ equation —
  printed **p.179**.
- **Problem 4.7** — find specific $Y_l^m$ and verify they satisfy the angular
  equation — printed **p.179**.
- **Problem 4.8** — derive the Legendre orthonormality condition from the
  Rodrigues formula — printed **p.179**.
- **Problem 4.21** — the raising/lowering normalization constants
  $A_l^m=\hbar\sqrt{l(l+1)-m(m\pm1)}$ — printed **p.206**.
- **Problem 4.22** — commutators $[L_z,x]$, …; obtain $[L_x,L_y]$ from the
  canonical relations; show $H=p^2/2m+V(r)$ commutes with all of $\mathbf L$ —
  printed **p.206–207**.
- **Problem 4.23** — rate of change of $\langle\mathbf L\rangle$ = expectation of
  the torque (rotational Ehrenfest); conservation for spherically symmetric $V$ —
  printed **p.207** (the quantum face of `~CM-09`).

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned: Ch. 3, *Theory of Angular
  Momentum* (the same algebra, with rotations and $D$-matrices).
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. I** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned: Ch. VI (general theory of angular
  momentum) and the complements on spherical harmonics.
- `~MA-12` (this repo) — associated Legendre functions and the spherical
  harmonics, the mathematical prerequisite imported by the code.
