# QM-13 — Addition of Angular Momenta (notes)

A single angular momentum (`~QM-10`) lives in a $(2j+1)$-dimensional space spanned
by $|j,m\rangle$, $m=-j,\dots,j$. The new question here is what happens when a
system carries **two** angular momenta at once — an electron's spin *and* orbit
($\mathbf J=\mathbf L+\mathbf S$, `~QM-17`), two spins (`~QM-11`/`~QM-21`), or a
whole atom's electrons. Classically you just add the vectors; quantum-mechanically
the *magnitude* of the sum is quantized, and the bookkeeping that tracks how is the
**Clebsch–Gordan** machinery (Griffiths 3e §4.4.3, p.223).

Throughout, $\hbar$ is written explicitly; the code uses $\hbar=1$ (documented in
`addition.py`), so $J^2\to J(J+1)$ and $J_z\to M$.

## 1. Two angular momenta: the tensor-product space

If angular momentum 1 has basis $\{|j_1,m_1\rangle\}$ and angular momentum 2 has
$\{|j_2,m_2\rangle\}$, the composite system lives in the **tensor product** of the
two spaces, with basis the products
$$|j_1 m_1\rangle\,|j_2 m_2\rangle\equiv|j_1 m_1; j_2 m_2\rangle,\qquad
\dim = (2j_1+1)(2j_2+1).$$
This is the **uncoupled basis**. Each operator of subsystem 1 acts as the identity
on subsystem 2 and vice versa, i.e. in matrices $J_{1i}=L_i^{(1)}\otimes\mathbb 1_2$
and $J_{2i}=\mathbb 1_1\otimes L_i^{(2)}$ (the code builds these with `np.kron`).
Because they act on different factors, **all of subsystem 1 commutes with all of
subsystem 2**: $[J_{1i},J_{2k}]=0$.

## 2. The total angular momentum

Define the total angular momentum componentwise (Griffiths 3e §4.4.3, p.223):
$$\boxed{\,\mathbf J=\mathbf J_1+\mathbf J_2\,},\qquad J_i=J_{1i}+J_{2i}.$$
Since $\mathbf J_1$ and $\mathbf J_2$ commute and each separately obeys the angular
-momentum algebra, $\mathbf J$ does too: $[J_x,J_y]=i\hbar J_z$ and cyclic. So
$\mathbf J$ is a *bona fide* angular momentum with its own Casimir $J^2$ and ladder
$J_\pm=J_{1\pm}+J_{2\pm}$.

**The $z$-component is easy.** $J_z=J_{1z}+J_{2z}$ is diagonal in the uncoupled
basis, and its eigenvalue is just the sum (Griffiths p.223, "the $z$-components
add"):
$$J_z\,|j_1 m_1; j_2 m_2\rangle=\hbar(m_1+m_2)\,|j_1 m_1; j_2 m_2\rangle,\qquad
M\equiv m_1+m_2.$$
**The total magnitude is subtle.** $J^2=(\mathbf J_1+\mathbf J_2)^2$ is *not*
diagonal in the uncoupled basis. Expanding,
$$\boxed{\,J^2=J_1^2+J_2^2+2\,\mathbf J_1\!\cdot\!\mathbf J_2,\qquad
\mathbf J_1\!\cdot\!\mathbf J_2=J_{1z}J_{2z}+\tfrac12\big(J_{1+}J_{2-}+J_{1-}J_{2+}\big)\,}$$
The cross term $J_{1\pm}J_{2\mp}$ moves one quantum from subsystem 1 to subsystem 2
(keeping $M$ fixed), so $J^2$ **mixes** uncoupled states of equal $M$. The two
forms of $J^2$ — the literal $J_x^2+J_y^2+J_z^2$ and the expansion above — are
verified equal in `test_J_squared_two_equivalent_forms`.

## 3. Coupled vs. uncoupled — two bases for one space

The same $(2j_1+1)(2j_2+1)$-dimensional space has two natural orthonormal bases:

| basis | labels | diagonalizes |
|---|---|---|
| **uncoupled** | $|j_1 m_1; j_2 m_2\rangle$ | $J_1^2,\,J_2^2,\,J_{1z},\,J_{2z}$ |
| **coupled** | $|J,M\rangle$ (with $j_1,j_2$ fixed) | $J_1^2,\,J_2^2,\,J^2,\,J_z$ |

Both are eigenbases of the two Casimirs $J_1^2,J_2^2$ (which are constants on the
whole space). They differ in the last pair: the uncoupled basis resolves the
*individual* $z$-components $J_{1z},J_{2z}$; the coupled basis resolves the *total*
$J^2,J_z$. You cannot have all four of $J_{1z},J_{2z},J^2$ simultaneously, because
$$[J^2,J_{1z}]\ne 0$$
(Griffiths Problem 4.41, p.227) — the cross term in §2 is the obstruction. The set
$\{J^2,J_z,J_1^2,J_2^2\}$ *does* commute (a complete commuting set), which is why
the coupled labels $|J,M\rangle$ are well defined (verified in
`test_total_operators_hermitian_and_commuting`). Note the **total** $J_z$ still
commutes with $J^2$, since $[J^2,J_{1z}+J_{2z}]=0$ (Griffiths p.227 footnote).

## 4. The archetype: two spin-½ → triplet + singlet

Take $j_1=j_2=\tfrac12$ (Griffiths Example 4.5, p.223): the electron and proton in
ground-state hydrogen, or any two spin-$\tfrac12$'s. The four uncoupled states are
$|\!\uparrow\uparrow\rangle,|\!\uparrow\downarrow\rangle,|\!\downarrow\uparrow\rangle,|\!\downarrow\downarrow\rangle$ (first slot = particle 1, $\uparrow=m=+\tfrac12$).
Their $M=m_1+m_2$ values are $+1,0,0,-1$ — but $M$ for a single angular momentum
must run in integer steps from $-J$ to $J$, so the doubled $M=0$ signals **two**
multiplets. Starting from the unique top state $|J{=}1,M{=}1\rangle=|\!\uparrow\uparrow\rangle$
and applying $J_-=J_{1-}+J_{2-}$ (Griffiths Eq. 4.175, p.223):
$$|1,1\rangle=|\!\uparrow\uparrow\rangle,\quad
|1,0\rangle=\tfrac{1}{\sqrt2}\big(|\!\uparrow\downarrow\rangle+|\!\downarrow\uparrow\rangle\big),\quad
|1,-1\rangle=|\!\downarrow\downarrow\rangle\qquad(\text{the \textbf{triplet}, }J=1).$$
The remaining combination, orthogonal to $|1,0\rangle$, is the **singlet**
(Griffiths Eq. 4.176, p.224):
$$\boxed{\,|0,0\rangle=\tfrac{1}{\sqrt2}\big(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle\big)\,}$$
Griffiths then *proves* (p.224–225) that the three triplet states are eigenstates
of $J^2$ with eigenvalue $\hbar^2\,1(1{+}1)=2\hbar^2$, and the singlet has $J^2=0$;
the code verifies this in `test_coupled_states_are_simultaneous_eigenstates` and
reproduces the exact vectors in `test_singlet_and_triplet_half_half`. The triplet
is **symmetric** under particle exchange, the singlet **antisymmetric** — the seed
of `~QM-14` (identical particles) and exactly the maximally-entangled **Bell
state** of `~QM-21`.

## 5. The general rule and a dimension check

Coupling spin $j_1$ with spin $j_2$ produces every total from $j_1+j_2$ down to
$|j_1-j_2|$ in integer steps (Griffiths 3e p.225):
$$\boxed{\,j_1\otimes j_2=\bigoplus_{J=|j_1-j_2|}^{\,j_1+j_2}J\,},\qquad
J=j_1+j_2,\ j_1+j_2-1,\ \dots,\ |j_1-j_2|,$$
each value appearing exactly once. (Griffiths' own example: spin $\tfrac32$ with
spin $2$ gives $\tfrac72,\tfrac52,\tfrac32,\tfrac12$.) The highest total occurs
when the two are "parallel," the lowest when "antiparallel." A clean consistency
check is that the coupled basis spans the same space:
$$\sum_{J=|j_1-j_2|}^{\,j_1+j_2}(2J+1)=(2j_1+1)(2j_2+1).$$
The code reads the multiplet content straight off the spectrum of $J^2$
(eigenvalue $\hbar^2J(J+1)$ with multiplicity $2J+1$) in
`test_J2_eigenvalues_and_multiplicities`, and checks the dimension identity in
`test_dimension_sum_rule`. In group-theory language this is the decomposition of
the direct product of two irreducible representations of the rotation group into a
direct sum of irreducibles (Griffiths p.226).

## 6. Clebsch–Gordan coefficients

Because $J_z=J_{1z}+J_{2z}$, a coupled state $|J,M\rangle$ can only contain
uncoupled states with $m_1+m_2=M$. Expanding one basis in the other defines the
**Clebsch–Gordan coefficients** (Griffiths Eq. 4.183, p.225):
$$\boxed{\,|J,M\rangle=\!\!\sum_{m_1+m_2=M}\!\!\langle j_1 m_1; j_2 m_2\,|\,J M\rangle\;
|j_1 m_1; j_2 m_2\rangle\,}$$
Collected as a matrix $U$ (columns = coupled states, rows = uncoupled states),
$U_{(m_1m_2),(JM)}=\langle j_1 m_1; j_2 m_2|JM\rangle$, this is a **unitary change
of basis** between two orthonormal bases — so the CG coefficients are orthonormal:
$$\sum_{m_1,m_2}\langle j_1 m_1; j_2 m_2|JM\rangle\langle j_1 m_1; j_2 m_2|J'M'\rangle
=\delta_{JJ'}\delta_{MM'},$$
i.e. "the sum of the squares of each row (and column) of the CG table is $1$"
(Griffiths p.226). A few cases are tabulated in Griffiths' **Table 4.8** (p.226).
The conventions, all reproduced by the code:
- **Real** coefficients in the **Condon–Shortley** convention.
- **Selection rules:** nonzero only if $m_1+m_2=M$ *and* $|j_1-j_2|\le J\le j_1+j_2$
  (the triangle rule).
- **Sign fixing:** for each multiplet, the top state $|J,J\rangle$ has a real,
  *positive* amplitude on the product state with the largest $m_1$ ($m_1=j_1$).

### How the code builds them (no table lookup)
`addition.py` constructs $U$ from scratch by the **highest-weight + ladder**
recursion (`coupled_basis`):
1. For each $J$ (largest first), the top state $|J,J\rangle$ is the unit vector in
   the $M=J$ sector orthogonal to all higher $|J',J\rangle$ already built — there
   is exactly one such direction — with the Condon–Shortley sign imposed.
2. The rest of the multiplet follows by repeated lowering,
   $|J,M-1\rangle=J_-|J,M\rangle/\hbar\sqrt{J(J+1)-M(M-1)}$.

This is graded three independent ways: against the explicit Griffiths tables
(`test_singlet_and_triplet_half_half`, `test_one_times_half_table`), against
unitarity (`test_coupled_basis_is_unitary`), and against `sympy`'s
Clebsch–Gordan routine (`test_cg_matches_sympy`) so the recursion is never checked
only against itself.

## 7. The coupled basis = simultaneous eigenstates

Rotating $J^2$ and $J_z$ into the coupled basis makes them **diagonal**
($U^\dagger J^2 U=\operatorname{diag}\,\hbar^2J(J+1)$,
$U^\dagger J_z U=\operatorname{diag}\,\hbar M$ — `test_U_block_diagonalizes_J2_and_Jz`),
while each $|J,M\rangle$ is *also* an eigenstate of $J_1^2,J_2^2$. That is exactly
why CG coefficients are needed: $J^2$ is non-diagonal in the uncoupled basis
(`test_J2_not_diagonal_in_uncoupled_basis`), and "in order to form eigenstates of
$J^2$ we need linear combinations of eigenstates of $J_{1z}$ — this is precisely
what the Clebsch–Gordan coefficients do for us" (Griffiths Problem 4.41, p.227).

---
### Why this is a hinge of the QM trunk
Addition of angular momenta is the structural step from one quantized rotor to
composite quantum systems:
- **Spin–orbit / fine structure** (`~QM-17`): an electron's $\mathbf J=\mathbf L+\mathbf S$
  is this construction; the good quantum numbers become $(n,\ell,j,m_j)$ and the
  $\mathbf L\!\cdot\!\mathbf S$ in the Hamiltonian is the §2 cross term, diagonal
  in the coupled basis.
- **Entanglement / Bell states** (`~QM-21`): the singlet
  $(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)/\sqrt2$ is a
  maximally entangled two-qubit state — the resource for `~QO-04/05`.
- **Identical particles** (`~QM-14`): the symmetric triplet / antisymmetric singlet
  split feeds spin–statistics and exchange energy.
- Built directly on **`~QM-10`** (one angular momentum: its operators are imported)
  and **`~QM-11`** (spin-$\tfrac12$, the $\tfrac12\otimes\tfrac12$ case).
The lesson: *two angular momenta combine by re-diagonalizing $J^2$, and the
Clebsch–Gordan coefficients are the unitary that does it.*
