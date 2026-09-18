# QM-13 — Addition of Angular Momenta

Coupling two angular momenta: the coupled $(J^2,J_z)$ basis, the uncoupled
$(j_1 m_1; j_2 m_2)$ basis, and the Clebsch–Gordan coefficients between them
(see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-10` (a single angular momentum — its matrix operators
  `Lz, L_plus, L_minus, Lx, Ly, L_squared` are **imported by this module's code**
  to build $\mathbf J_1,\mathbf J_2$), `~QM-11` (spin: the $\tfrac12\otimes\tfrac12$
  case is two spins), `~MA-04` (linear algebra: tensor products, simultaneous
  eigenvectors, unitary change of basis).
- **Feeds into:** `~QM-17` (spin–orbit coupling / fine structure: $\mathbf J=\mathbf L+\mathbf S$
  *is* this construction, and $\mathbf L\!\cdot\!\mathbf S$ is the cross term made
  diagonal here — forward), `~QM-21` (the singlet $(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)/\sqrt2$
  is the maximally-entangled Bell state — forward), `~QM-14` (identical particles:
  the symmetric-triplet / antisymmetric-singlet split). These bridges connect when
  those modules land.

## Scope
Two angular momenta combine by **re-diagonalizing $J^2$**, and the Clebsch–Gordan
coefficients are the unitary that does it (Griffiths 3e §4.4.3, p.223).

1. **The product space** — each angular momentum lives in a $(2j+1)$-dim space;
   the composite lives in the tensor product, $\dim=(2j_1+1)(2j_2+1)$. $\mathbf J_1,\mathbf J_2$
   act by Kronecker products ($J_{1i}=L_i\otimes\mathbb 1$, $J_{2i}=\mathbb 1\otimes L_i$).
2. **Total operators** — $\mathbf J=\mathbf J_1+\mathbf J_2$; $J_z$ is diagonal
   ($M=m_1+m_2$, "the $z$-components add"), but $J^2=(\mathbf J_1+\mathbf J_2)^2$
   mixes equal-$M$ states (Griffiths p.223).
3. **Multiplet content** — diagonalizing $J^2$ gives $j_1\otimes j_2=\bigoplus_{J=|j_1-j_2|}^{j_1+j_2}J$,
   each $J$ once with $2J+1$ states; the dimensions match, $\sum_J(2J+1)=(2j_1+1)(2j_2+1)$
   (Griffiths p.225).
4. **Clebsch–Gordan** — the unitary coupled↔uncoupled change of basis (Eq. 4.183,
   Table 4.8, p.225–226), built from scratch by the highest-weight + ladder
   recursion in the Condon–Shortley convention.
5. **Two spin-½** — the worked archetype: singlet $J=0$ + triplet $J=1$
   (Griffiths Eqs. 4.175–4.176, p.223–224).

**House rule for this module:** nothing about the coupling is asserted — it is
*built*. $\mathbf J_1,\mathbf J_2$ are assembled from `~QM-10`'s single-$j$
operators by tensor products; $J^2$ is diagonalized to read off the multiplets; the
Clebsch–Gordan matrix is constructed by the ladder recursion and then checked
**three independent ways** — against the explicit Griffiths tables, against
unitarity (CG orthonormality), and against `sympy`'s Clebsch–Gordan routine — so
the construction is never graded only against itself.

## Operations — `code/addition.py` ($\hbar = 1$, natural units)

| call | meaning | result |
|------|---------|--------|
| `multiplet_content(j1,j2)` | the total-$J$ series | `[j1+j2, …, |j1−j2|]` |
| `decomposition(j1,j2)` | readable CG series | e.g. `'1/2 (x) 1/2 = 1 (+) 0'` |
| `dimension_check(j1,j2)` | dimension sum rule | `((2j1+1)(2j2+1), Σ(2J+1))` |
| `uncoupled_labels` / `coupled_labels` | basis labels | `(m1,m2)` / `(J,M)` |
| `embed_1(op,j2)` / `embed_2(op,j1)` | lift to product space | `op⊗I`, `I⊗op` |
| `total_operators(j1,j2)` | all operators (dict) | `J1i,J2i,Ji,J±,J1²,J2²,J²` |
| `Jz_total` / `Jminus_total` / `Jplus_total` | total $J_z,J_\mp,J_\pm$ | matrices |
| `J_squared(j1,j2)` | total Casimir $J^2$ | matrix |
| `J1_squared` / `J2_squared` | the two subsystem Casimirs | matrices |
| `coupled_basis(j1,j2)` | CG transform | `(U, coupled_labels, uncoupled_labels)` |
| `cg_coefficient(j1,m1,j2,m2,J,M)` | one CG coefficient | `⟨j1 m1; j2 m2 | J M⟩` |
| `cg_table(j1,j2)` | full table | `{(J,M): {(m1,m2): coeff}}` |
| `commutator(A,B)` | `AB−BA` | (re-exported from `~QM-10`) |

`HBAR` (= `1.0`) and `dim(j)` (= `2j+1`) are re-exported from `~QM-10`; the $\hbar$
factors are carried symbolically, so $J^2\to\hbar^2J(J+1)$, $J_z\to\hbar M$.

## Use
```python
import numpy as np
from addition import (decomposition, J_squared, coupled_basis,
                      cg_coefficient, cg_table, multiplet_content)

decomposition(1.0, 0.5)                       # '1 (x) 1/2 = 3/2 (+) 1/2'
np.round(np.linalg.eigvalsh(J_squared(0.5,0.5)).real, 3)   # [0, 2, 2, 2] = J(J+1)
U, cl, unc = coupled_basis(0.5, 0.5)          # U unitary; columns are |J,M>
np.allclose(U.conj().T @ U, np.eye(4))        # True  -- CG orthonormality
cg_coefficient(0.5, 0.5, 0.5, -0.5, 0, 0)     # 0.7071  -- singlet amplitude
cg_table(0.5, 0.5)[(0.0, 0.0)]                # {(0.5,-0.5): 0.707, (-0.5,0.5): -0.707}
```

## Run
```bash
cd code
python3 addition.py          # demo: 1/2(x)1/2 and 1(x)1/2 tables; singlet + triplet
python3 test_addition.py     # tests  ->  "All 16 tests passed."
```

## Files
- `notes.md` — tensor product → total $\mathbf J$ → multiplet content → Clebsch–Gordan, with the two-spin-½ archetype
- `code/addition.py` — the library (numpy; single-$j$ operators imported from `~QM-10`)
- `code/test_addition.py` — 16 checks: dimension rule, $J^2$ spectrum, unitarity, singlet/triplet, Griffiths Table 4.8, sympy cross-check
- `problems/problems.md` — worked problems (Griffiths 3e)
- `refs.md` — verified textbook locations (Griffiths §4.4.3; Bethe §6)
