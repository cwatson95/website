# QM-13 — Problems

Work them by hand, then check with `code/addition.py`. Sources in `../refs.md`.
Natural units $\hbar=1$ (as in the code).

### P1.  Why $M=0$ appears twice  *(Griffiths 3e Example 4.5, p.223)*
Two spin-½ particles have four product states. List their $M=m_1+m_2$ values and
explain why the appearance of $M=0$ *twice* signals two different total spins.
*Answer:* $M=+1,0,0,-1$ for $|\!\uparrow\uparrow\rangle,|\!\uparrow\downarrow\rangle,|\!\downarrow\uparrow\rangle,|\!\downarrow\downarrow\rangle$.
A single multiplet of total $J$ has $M$ running once each from $-J$ to $J$ in unit
steps. Here $M=1$ and $M=-1$ occur once, but $M=0$ twice — impossible for one
multiplet, so there must be **two**: a $J=1$ triplet ($M=1,0,-1$) and a $J=0$
singlet ($M=0$). Hence $\tfrac12\otimes\tfrac12=1\oplus0$.
*Check:* `decomposition(0.5,0.5)` → `'1/2 (x) 1/2 = 1 (+) 0'`;
`dimension_check(0.5,0.5)` → `(4,4)`. (`test_multiplet_content_series`,
`test_dimension_sum_rule`.)

**Solution.** The four product states $|\!\uparrow\uparrow\rangle,|\!\uparrow\downarrow\rangle,|\!\downarrow\uparrow\rangle,|\!\downarrow\downarrow\rangle$
carry $M=m_1+m_2=+1,0,0,-1$. A single spin-$J$ multiplet must contain each $M$ from
$-J$ to $J$ exactly once in unit steps; here $M=+1$ and $M=-1$ appear once each, so the
largest multiplet is $J=1$ with $M=1,0,-1$ — and that uses up only *one* of the two
$M=0$ states. The leftover $M=0$, with no partner at $M=\pm1$, can only be a $J=0$
singlet. Hence
$$\tfrac12\otimes\tfrac12=1\oplus0,\qquad \dim:\ 4=3+1.$$
This is exactly `decomposition(0.5,0.5)`→`'1/2 (x) 1/2 = 1 (+) 0'` with
`dimension_check(0.5,0.5)`→`(4,4)`.

### P2.  Build the triplet and singlet by lowering  *(Griffiths 3e Eqs. 4.175–4.176, p.223–224; Prob. 4.37)*
Starting from $|1,1\rangle=|\!\uparrow\uparrow\rangle$, apply $J_-=J_{1-}+J_{2-}$
to generate the rest of the triplet, then write the singlet as the orthogonal
$M=0$ combination.
*Answer:* $J_-|\!\uparrow\uparrow\rangle=|\!\downarrow\uparrow\rangle+|\!\uparrow\downarrow\rangle$,
so $|1,0\rangle=\tfrac1{\sqrt2}(|\!\uparrow\downarrow\rangle+|\!\downarrow\uparrow\rangle)$
and once more $|1,-1\rangle=|\!\downarrow\downarrow\rangle$. The singlet is the
orthogonal one, $|0,0\rangle=\tfrac1{\sqrt2}(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)$
(triplet symmetric, singlet antisymmetric under particle swap).
*Check:* `coupled_basis(0.5,0.5)` columns equal $[1,0,0,0]$, $[0,\tfrac1{\sqrt2},\tfrac1{\sqrt2},0]$,
$[0,0,0,1]$, $[0,\tfrac1{\sqrt2},-\tfrac1{\sqrt2},0]$.
(`test_singlet_and_triplet_half_half`, `test_ladder_normalization_within_a_multiplet`.)

**Solution.** For spin $\tfrac12$ the lowering operator gives $J_{i-}|\!\uparrow\rangle=\hbar|\!\downarrow\rangle$
(since $\hbar\sqrt{s(s+1)-m(m-1)}=\hbar$ at $s=m=\tfrac12$), so $J_-=J_{1-}+J_{2-}$ acts as
$$J_-|\!\uparrow\uparrow\rangle=(J_{1-}|\!\uparrow\rangle)|\!\uparrow\rangle+|\!\uparrow\rangle(J_{2-}|\!\uparrow\rangle)
=\hbar\big(|\!\downarrow\uparrow\rangle+|\!\uparrow\downarrow\rangle\big).$$
On the coupled side $J_-|1,1\rangle=\hbar\sqrt2\,|1,0\rangle$, so
$|1,0\rangle=\tfrac1{\sqrt2}(|\!\uparrow\downarrow\rangle+|\!\downarrow\uparrow\rangle)$; one more
lowering gives $|1,-1\rangle=|\!\downarrow\downarrow\rangle$. The singlet is the remaining unit
vector of the $M=0$ sector orthogonal to $|1,0\rangle$,
$|0,0\rangle=\tfrac1{\sqrt2}(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)$. In the
uncoupled order $|\!\uparrow\uparrow\rangle,|\!\uparrow\downarrow\rangle,|\!\downarrow\uparrow\rangle,|\!\downarrow\downarrow\rangle$
these are the columns `coupled_basis(0.5,0.5)` returns: $[1,0,0,0]$,
$[0,\tfrac1{\sqrt2},\tfrac1{\sqrt2},0]$, $[0,0,0,1]$, $[0,\tfrac1{\sqrt2},-\tfrac1{\sqrt2},0]$.

### P3.  The general series and the dimension check  *(Griffiths 3e p.225)*
Couple spin $\tfrac32$ with spin $2$. What total spins are possible, and does the
coupled basis still span the right space?
*Answer:* $J=\tfrac72,\tfrac52,\tfrac32,\tfrac12$ (from $j_1+j_2=\tfrac72$ down to
$|j_1-j_2|=\tfrac12$). Dimension: $(2\cdot\tfrac32+1)(2\cdot2+1)=4\cdot5=20$, and
$\sum(2J+1)=8+6+4+2=20$. ✓
*Check:* `multiplet_content(1.5,2.0)` → `[3.5,2.5,1.5,0.5]`;
`dimension_check(1.5,2.0)` → `(20,20)`. (`test_multiplet_content_series`,
`test_dimension_sum_rule`.)

**Solution.** The series runs from the "parallel" maximum $J=j_1+j_2=\tfrac32+2=\tfrac72$
down to the "antiparallel" minimum $J=|j_1-j_2|=\tfrac12$ in unit steps, each value once:
$$\tfrac32\otimes2=\tfrac72\oplus\tfrac52\oplus\tfrac32\oplus\tfrac12.$$
Coupling only re-labels the same Hilbert space, so the two basis counts must agree:
$$(2\cdot\tfrac32+1)(2\cdot2+1)=4\cdot5=20=\!\!\sum_{J=1/2}^{7/2}\!(2J+1)=8+6+4+2.$$
This is `multiplet_content(1.5,2.0)`→`[3.5,2.5,1.5,0.5]` and
`dimension_check(1.5,2.0)`→`(20,20)`.

### P4.  Why we need Clebsch–Gordan at all  *(Griffiths 3e Problem 4.41, p.227)*
Show that $J^2$ is **not** diagonal in the uncoupled basis (so the product states
are not total-spin eigenstates), even though $J_z$ is. What is the culprit?
*Answer:* $J^2=J_1^2+J_2^2+2J_{1z}J_{2z}+J_{1+}J_{2-}+J_{1-}J_{2+}$. The flip-flop
term $J_{1\pm}J_{2\mp}$ connects $|m_1,m_2\rangle$ to $|m_1{\mp}1,m_2{\pm}1\rangle$
(same $M$), so $[J^2,J_{1z}]\ne0$ and $J^2$ has off-diagonal blocks. To build $J^2$
eigenstates you must take linear combinations of equal-$M$ product states — those
coefficients are the Clebsch–Gordan coefficients. The total $J_z=J_{1z}+J_{2z}$
*does* commute with $J^2$.
*Check:* `J_squared(0.5,0.5)` has nonzero off-diagonal entries; `commutator(`$J^2$`,J1z)` $\ne0$
but `commutator(`$J^2$`,Jz)` $=0$. (`test_J2_not_diagonal_in_uncoupled_basis`.)

**Solution.** Expand $J^2=(\mathbf J_1+\mathbf J_2)^2=J_1^2+J_2^2+2J_{1z}J_{2z}+J_{1+}J_{2-}+J_{1-}J_{2+}$.
The flip-flop term $J_{1\pm}J_{2\mp}$ sends $|m_1,m_2\rangle\to|m_1{\mp}1,m_2{\pm}1\rangle$ —
same $M=m_1+m_2$, but a *different* product state — so $J^2$ picks up off-diagonal entries
inside each equal-$M$ block. For $\tfrac12\otimes\tfrac12$ (order
$|\!\uparrow\uparrow\rangle,|\!\uparrow\downarrow\rangle,|\!\downarrow\uparrow\rangle,|\!\downarrow\downarrow\rangle$),
$$J^2=\begin{pmatrix}2&0&0&0\\0&1&1&0\\0&1&1&0\\0&0&0&2\end{pmatrix},$$
whose central ($M=0$) block is non-diagonal. Thus $[J^2,J_{1z}]\ne0$, while the *total*
$[J^2,J_z]=0$. Numerically `J_squared(0.5,0.5)` shows the off-diagonal $1$'s,
`commutator(`$J^2$`,J1z)` has largest entry $1\ne0$, and `commutator(`$J^2$`,Jz)`$=0$.

### P5.  Read a Clebsch–Gordan table  *(Griffiths 3e Table 4.8, p.226)*
For $1\otimes\tfrac12$, write $|\tfrac32,\tfrac12\rangle$ and $|\tfrac12,\tfrac12\rangle$
in the uncoupled basis from the table.
*Answer:* $|\tfrac32,\tfrac12\rangle=\sqrt{\tfrac13}\,|1,-\tfrac12\rangle+\sqrt{\tfrac23}\,|0,\tfrac12\rangle$
and $|\tfrac12,\tfrac12\rangle=\sqrt{\tfrac23}\,|1,-\tfrac12\rangle-\sqrt{\tfrac13}\,|0,\tfrac12\rangle$
(orthogonal, as they must be; Condon–Shortley sign on the largest-$m_1$ term).
*Check:* `cg_coefficient(1,1,0.5,-0.5,1.5,0.5)` $=\sqrt{1/3}$;
`cg_coefficient(1,0,0.5,0.5,0.5,0.5)` $=-\sqrt{1/3}$; `cg_table(1,0.5)`.
(`test_one_times_half_table`, `test_cg_selection_rules_and_lookup`.)

**Solution.** In $1\otimes\tfrac12$ the $M=\tfrac12$ sector holds exactly two product
states, $|1,-\tfrac12\rangle$ and $|0,\tfrac12\rangle$ (both with $m_1+m_2=\tfrac12$); they
split one each into the $J=\tfrac32$ and $J=\tfrac12$ multiplets. Reading Table 4.8,
$$|\tfrac32,\tfrac12\rangle=\sqrt{\tfrac13}\,|1,-\tfrac12\rangle+\sqrt{\tfrac23}\,|0,\tfrac12\rangle,
\qquad
|\tfrac12,\tfrac12\rangle=\sqrt{\tfrac23}\,|1,-\tfrac12\rangle-\sqrt{\tfrac13}\,|0,\tfrac12\rangle,$$
orthogonal unit vectors, the Condon–Shortley sign making the largest-$m_1$ amplitude
positive. Thus `cg_coefficient(1,1,0.5,-0.5,1.5,0.5)`$=\sqrt{1/3}=0.5774$ and the
$|0,\tfrac12\rangle$ amplitude of $|\tfrac12,\tfrac12\rangle$,
`cg_coefficient(1,0,0.5,0.5,0.5,0.5)`$=-\sqrt{1/3}=-0.5774$, both entries of `cg_table(1,0.5)`.

### P6.  Coupled states are simultaneous eigenstates  *(Griffiths 3e p.224–225)*
Confirm that each $|J,M\rangle$ is a simultaneous eigenstate of $J^2,J_z,J_1^2,J_2^2$
— i.e. that $\{J^2,J_z,J_1^2,J_2^2\}$ is a complete set of commuting observables.
*Answer:* By construction $|J,M\rangle$ has $J^2\to J(J+1)$, $J_z\to M$,
$J_1^2\to j_1(j_1+1)$, $J_2^2\to j_2(j_2+1)$. These four operators commute, so a
common eigenbasis exists; the change of basis $U$ from the uncoupled basis
diagonalizes $J^2$ and $J_z$ together: $U^\dagger J^2 U=\mathrm{diag}\,J(J+1)$.
*Check:* `coupled_states_...`: each column of `coupled_basis(...)` is an eigenvector
of all four; `U.conj().T @ J_squared @ U` is diagonal.
(`test_coupled_states_are_simultaneous_eigenstates`, `test_U_block_diagonalizes_J2_and_Jz`.)

**Solution.** Each coupled vector is built inside a single $(j_1,j_2)$ product space, so it
is automatically an eigenstate of the Casimirs $J_1^2\to\hbar^2j_1(j_1+1)$ and
$J_2^2\to\hbar^2j_2(j_2+1)$. It is assembled within one $M$-sector (eigenstate of
$J_z\to\hbar M$) and forced to be an eigenstate of $J^2\to\hbar^2J(J+1)$ by the
highest-weight$+$ladder construction. Since $\{J^2,J_z,J_1^2,J_2^2\}$ mutually commute a
common eigenbasis exists, and the change of basis diagonalizes the mixed operator:
$U^\dagger J^2U=\mathrm{diag}\,\hbar^2J(J+1)$. For $1\otimes\tfrac12$ this returns
$\mathrm{diag}(3.75,3.75,3.75,3.75,0.75,0.75)$ — $J(J+1)=3.75$ for the $J=\tfrac32$ quartet
and $0.75$ for the $J=\tfrac12$ doublet — exactly what `U.conj().T @ J_squared @ U` gives.

### P7.  Orthonormality = probabilities sum to one  *(Griffiths 3e p.226)*
The Clebsch–Gordan transform is unitary. State what "the sum of the squares of each
row (and column) of the CG table is 1" means physically.
*Answer:* Unitarity says $U^\dagger U=UU^\dagger=\mathbb 1$. Column sum $=1$:
each coupled state $|J,M\rangle$ is normalized. Row sum $=1$: an uncoupled state
$|m_1,m_2\rangle$, if you measure total $(J,M)$, yields a probability
$|\langle j_1 m_1 j_2 m_2|JM\rangle|^2$ for each outcome, and these probabilities
sum to 1.
*Check:* `U.conj().T @ U` $=I$; row/column sums of $|U|^2$ are all $1$.
(`test_coupled_basis_is_unitary`.)

**Solution.** Both bases are orthonormal, so the change of basis $U$ (entries the CG
coefficients) is unitary: $U^\dagger U=UU^\dagger=\mathbb1$. The **column** condition
$\sum_{m_1,m_2}|\langle j_1m_1;j_2m_2|JM\rangle|^2=1$ just says each coupled state
$|J,M\rangle$ is normalized. The **row** condition
$\sum_{J,M}|\langle j_1m_1;j_2m_2|JM\rangle|^2=1$ is the probabilistic statement: prepare the
product state $|m_1,m_2\rangle$, measure total $(J,M)$, and the possible outcomes occur with
probabilities $|\langle j_1m_1;j_2m_2|JM\rangle|^2$ that must sum to one. Hence
`U.conj().T @ U`$=I$ and every row (and column) sum of $|U|^2$ equals $1$ (e.g. $[1,1,1,1]$
for $\tfrac12\otimes\tfrac12$).

### P8.  Independent check + the forward bridges  *(Griffiths 3e Table 4.8, p.226; ~QM-17, ~QM-21)*
Verify the whole $1\otimes1$ Clebsch–Gordan table against an independent source,
and name where this construction reappears.
*Answer:* Every coefficient matches `sympy.physics.wigner.clebsch_gordan` to
machine precision (same Condon–Shortley convention). The construction reappears as
$\mathbf J=\mathbf L+\mathbf S$ in **spin–orbit / fine structure** (`~QM-17`,
where $\mathbf L\!\cdot\!\mathbf S$ is the §2 cross term, diagonal in the coupled
basis) and as the maximally-entangled **Bell singlet** $(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)/\sqrt2$
in **entanglement** (`~QM-21`).
*Check:* `cg_table(1,1)` vs `sympy.physics.wigner.clebsch_gordan`.
(`test_cg_matches_sympy`.)

**Solution.** The highest-weight$+$ladder recursion that builds $U$ is never graded against
itself: every entry of `cg_table(1,1)` is compared to `sympy.physics.wigner.clebsch_gordan`
(the same Condon–Shortley convention) and agrees to machine precision. For instance the
$1\otimes1$ singlet comes out as
$$|0,0\rangle=\tfrac1{\sqrt3}\big(|1,-1\rangle-|0,0\rangle+|{-1},1\rangle\big),$$
each coefficient $\pm1/\sqrt3=\pm0.57735$ matching sympy. The identical coupling reappears as
$\mathbf J=\mathbf L+\mathbf S$ in fine structure (`~QM-17`, where $\mathbf L\!\cdot\!\mathbf S$
is diagonal in the coupled basis) and as the maximally entangled Bell singlet
$(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)/\sqrt2$ in `~QM-21`.
