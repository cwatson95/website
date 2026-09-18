# QM-13 — References

Page-level citations **verified by reading the page text** in the PDF (extracted,
not eyeballed off a scan). **Printed** = the number printed on the page; **PDF** =
the page in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |
| Bethe & Jackiw, *Intermediate Quantum Mechanics*, 3rd ed. | `QM_Quantum_Mechanics/BetheQM.pdf` | PDF = printed **+ 19** |

> **Offset notes.**
> *Griffiths:* printed folio equals the viewer page throughout the body (read
> printed page `P` with `fitz.open(path)[P-1]`). Confirmed on every page cited
> below (the §4.4.3 heading prints on folio 223 at fitz index 222, etc.).
> *Bethe:* verified empirically here — fitz indices 122/123/124/125 carry printed
> folios 104/105/106/107, so `fitz_index = printed + 18` (PDF viewer page =
> printed + 19). Read printed page `P` with `fitz.open(path)[P+18]`. (Same offset
> as `~QM-10`.)

## Topic → location (Griffiths 3e — the primary source)

| Topic (code symbol) | Section | Printed p. |
|---|---|---|
| §4.4.3 *Addition of Angular Momenta* heading; total $\mathbf J=\mathbf J_1+\mathbf J_2$; "$z$-components add", $M=m_1+m_2$ (`Jz_total`, `total_operators`) | §4.4.3 | 223 |
| Example 4.5: two spin-½; the four product states; building the triplet with $S_-$ (Eq. 4.175) (`coupled_basis`, `Jminus_total`) | §4.4.3 | 223–224 |
| The singlet $\tfrac1{\sqrt2}(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)$ (Eq. 4.176) (`test_singlet_and_triplet_half_half`) | §4.4.3 | 224 |
| Proof: triplet are $S^2$ eigenstates with $2\hbar^2$ ($s{=}1$), singlet with $0$ ($s{=}0$) (`test_coupled_states_are_simultaneous_eigenstates`) | §4.4.3 | 224–225 |
| General series $J=j_1{+}j_2,\dots,|j_1{-}j_2|$ in integer steps (`multiplet_content`, `decomposition`) | §4.4.3 | 225 |
| CG expansion $|s\,m\rangle=\sum C^{\,s\,m}_{m_1 m_2}|s_1 m_1\rangle|s_2 m_2\rangle$, $m_1{+}m_2{=}m$ (Eq. 4.183); the term "Clebsch–Gordan coefficients" (`cg_coefficient`, `coupled_basis`) | §4.4.3 | 225 |
| **Table 4.8** Clebsch–Gordan coefficients; "sum of the squares of each row …is 1"; the direct-product → direct-sum (group-theory) remark (`cg_table`, `test_coupled_basis_is_unitary`) | §4.4.3 | 226 |
| Triangle/dimension counting via the $M$ ladder doubling at $M{=}0$ (`dimension_check`, `test_dimension_sum_rule`) | §4.4.3 | 223, 225 |

## Topic → location (Bethe & Jackiw — verified secondary source, §6)

| Topic | Section | Printed p. |
|---|---|---|
| $|\ell_1 m_1,\ell_2 m_2\rangle$ is an $L_z=L_{1z}+L_{2z}$ eigenfunction, $M_L=m_1+m_2$; "$L^2=(\mathbf L_1+\mathbf L_2)^2$ is **not in general diagonal**"; diagonalize by linear combinations within fixed $M_L$ (Table 6-1) (`test_J2_not_diagonal_in_uncoupled_basis`) | §6 *Addition of Angular Momenta* | 105 |
| Allowed totals $L=\ell_1{+}\ell_2,\dots,|\ell_1{-}\ell_2|$ (Eq. 6-14), "vector addition of angular momenta" (`multiplet_content`) | §6 | 106 |
| $C(\ell_1 m_1,\ell_2 m_2,LM)=0$ unless $M=m_1+m_2$; the **step-down method** for Clebsch–Gordan coefficients — start at $L=\ell_1{+}\ell_2,M{=}L$ (Eq. 6-17) and apply $L_-=L_{1-}+L_{2-}$ (Eq. 6-18) (`coupled_basis`) | §6 | 107 |

> **Honesty note (per the trunk's citation rule).** Addition of angular momenta is
> *core* Griffiths and is treated from first principles in §4.4.3 (pp.223–227):
> the two-spin-½ example is worked explicitly, the general series is stated, and
> the Clebsch–Gordan coefficients are defined (Eq. 4.183) and tabulated (Table
> 4.8). Every formula in `notes.md` sits on a page verified above. The one thing
> Griffiths does **not** print is the *general* $(2j_1{+}1)(2j_2{+}1)$-dimensional
> matrices and the recursive CG construction for arbitrary $j_1,j_2$ that
> `addition.py` builds — but Bethe §6 (p.107, verified) gives exactly that
> algorithm (the "step-down method," Eqs. 6-17/6-18), and the code is graded
> against the explicit Griffiths tables, against unitarity, **and against an
> independent library** (`sympy.physics.wigner.clebsch_gordan`,
> `test_cg_matches_sympy`). So the verification is both textual and computational.

## Problems (verified, Griffiths 3e)
- **Problem 4.37** — apply $S_-$ to the top triplet state and recover the next
  (a); $S_\pm$ annihilates the singlet (b); triplet/singlet are $S^2$ eigenstates
  (c) — printed **p.226**.
- **Problem 4.38** — quark spins: possible spins of baryons (3 quarks) and mesons
  (quark + antiquark) — printed **p.226–227**.
- **Problem 4.39** — verify Eqs. 4.175–4.176 directly from the Clebsch–Gordan
  table — printed **p.227**.
- **Problem 4.40** — spin-1 ⊗ spin-2 with total spin 3: measure the spin-2 $z$
  component, probabilities; total-$J^2$ of an electron in a hydrogen state —
  printed **p.227**.
- **Problem 4.41** — $[J^2,J_{1z}]\ne0$, so the uncoupled states are not $J^2$
  eigenstates and CG combinations are required; the total $J_z=J_{1z}+J_{2z}$ does
  commute with $J^2$ (Eq. 4.185) — printed **p.227**.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned: Ch. 3, *Theory of Angular
  Momentum* (addition of angular momenta, Clebsch–Gordan coefficients and their
  recursion relations, the Wigner–Eckart theorem).
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. II** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned: Ch. X, *Addition of Angular Momenta*
  (the general theory and CG coefficients).
- `~QM-10` (this repo) — a single angular momentum; its matrix operators
  (`Lz`, `L_plus`, `L_minus`, `Lx`, `Ly`, `L_squared`) are **imported** by
  `addition.py` to build $\mathbf J_1,\mathbf J_2$ in the product space.
