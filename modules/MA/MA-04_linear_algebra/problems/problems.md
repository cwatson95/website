# MA-04 — Problems

Work by hand, then check with `code/linalg.py`. Citations in `../refs.md`.

### P1.  Solve and invert  *(Boas 3e §2 p.83; §3 p.89)*
Solve the system  4x+3y=10, 6x+3y=12  by row reduction, then find the inverse of
[[4,3],[6,3]] and confirm A·A⁻¹ = I.
*Check:* `solve([[4,3],[6,3]], [10,12])`, `inverse(...)`, `matmul(A, inverse(A))`.

**Solution.** Row-reduce the augmented matrix; subtracting the equations ($R_2-R_1$) gives
$2x=2$, so $x=1$, and back-substitution $4(1)+3y=10$ gives $y=2$. For the inverse, the
determinant is $\det A=4\cdot3-3\cdot6=-6\neq0$, and for a $2\times2$ matrix
$A^{-1}=\frac1{\det A}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$:
$$A^{-1}=\frac1{-6}\begin{pmatrix}3&-3\\-6&4\end{pmatrix}=\begin{pmatrix}-\tfrac12&\tfrac12\\[2pt]1&-\tfrac23\end{pmatrix},\qquad
A\,A^{-1}=\begin{pmatrix}1&0\\0&1\end{pmatrix}.$$
So $(x,y)=(1,2)$ — exactly `solve(...)` $=[1,2]$, `inverse(...)` $=[[-0.5,0.5],[1,-0.667]]$, and `matmul(A, inverse(A))` $=I$.

### P2.  Determinant and singularity  *(Boas 3e §3, p.89)*
Show det[[1,2],[2,4]] = 0 (rows dependent ⇒ no inverse), and det of a diagonal
matrix is the product of the diagonal. *Check:* `det(...)`.

**Solution.** Directly, $\det\begin{pmatrix}1&2\\2&4\end{pmatrix}=1\cdot4-2\cdot2=0$, because row 2 is
$2\times$ row 1 — the rows are linearly dependent, so the matrix collapses volume to zero and
cannot be inverted. For a diagonal matrix the off-diagonal entries are already zero, so
Gaussian elimination touches nothing and the determinant is just the product of pivots:
$$\det\operatorname{diag}(d_1,\dots,d_n)=\prod_{i=1}^{n}d_i,\qquad
\det\operatorname{diag}(2,3,5)=2\cdot3\cdot5=30.$$
This matches `det([[1,2],[2,4]])` $=0$ and `det([[2,0,0],[0,3,0],[0,0,5]])` $=30$.

### P3.  Eigenvalues by characteristic polynomial  *(Boas 3e §11, p.148)*
For S = [[2,1],[1,2]] solve det(S−λI)=0 → λ=1,3, find the eigenvectors, and verify
they are orthogonal. *Check:* `eig_symmetric([[2,1],[1,2]])`; confirm S·v = λv.

**Solution.** The characteristic equation is $\det(S-\lambda I)=(2-\lambda)^2-1=\lambda^2-4\lambda+3=0$,
i.e. $(\lambda-1)(\lambda-3)=0$, so $\lambda=1,3$. For $\lambda=1$, $(S-I)\mathbf v=\begin{pmatrix}1&1\\1&1\end{pmatrix}\mathbf v=0$
gives $\mathbf v\propto(1,-1)$; for $\lambda=3$, $(S-3I)\mathbf v=\begin{pmatrix}-1&1\\1&-1\end{pmatrix}\mathbf v=0$
gives $\mathbf v\propto(1,1)$. Normalizing,
$$\mathbf v_1=\tfrac1{\sqrt2}(1,-1),\qquad \mathbf v_3=\tfrac1{\sqrt2}(1,1),\qquad \mathbf v_1\cdot\mathbf v_3=\tfrac12(1-1)=0.$$
Orthogonality is guaranteed because $S$ is symmetric. `eig_symmetric` returns eigenvalues
$\approx[1,3]$ with these orthonormal columns (dot product $0$), and $S\mathbf v=\lambda\mathbf v$ holds.

### P4.  Principal axes of an inertia tensor  *(Marion & Thornton 5e §11.5, p.425; Boas 3e §12, p.162)*
Given a symmetric inertia tensor (e.g. I = [[2,−1,0],[−1,2,0],[0,0,3]]),
diagonalize it: the eigenvalues are the **principal moments** and the
eigenvectors are the **principal axes**. Confirm A = QΛQᵀ with Q orthogonal.
This is exactly the eigenproblem `~CM-13` will use. *Check:* `eig_symmetric(I)`,
`reconstruct(vals, vecs)`.

**Solution.** The tensor is block-diagonal: the $z$-axis decouples (eigenvalue $3$, axis
$(0,0,1)$), while the $xy$-block $\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$ has eigenvalues $2\pm1=1,3$
with axes $\tfrac1{\sqrt2}(1,1)$ and $\tfrac1{\sqrt2}(1,-1)$. So the principal moments are
$\{1,3,3\}$, and as a check $\sum\lambda_i=1+3+3=7=\operatorname{tr}I$ and $\prod\lambda_i=1\cdot3\cdot3=9=\det I$.
Stacking the orthonormal axes as columns of $Q$ ($Q^{\mathsf T}Q=I$),
$$I=Q\,\Lambda\,Q^{\mathsf T},\qquad \Lambda=\operatorname{diag}(1,3,3).$$
`eig_symmetric(I)` returns eigenvalues $\approx[1,3,3]$ and `reconstruct(vals, vecs)` rebuilds $I$ exactly.

### P5.  Complex eigenvalues of a rotation  *(Boas 3e §11, p.148)*
The 90° rotation [[0,−1],[1,0]] has no real eigenvectors. Solve λ²+1=0 → λ=±i.
*Check:* `eigvals_2x2([[0,-1],[1,0]])` → (i, −i). (Contrast: a *symmetric* matrix
always has real eigenvalues — P3.)

**Solution.** Here $\operatorname{tr}A=0$ and $\det A=(0)(0)-(-1)(1)=1$, so the characteristic
polynomial $\lambda^2-(\operatorname{tr}A)\lambda+\det A$ becomes
$$\lambda^2+1=0\ \Longrightarrow\ \lambda=\pm i.$$
The eigenvalues are pure imaginary because a real $90^\circ$ rotation sends every real direction
to a perpendicular one — no real vector maps to a scalar multiple of itself. `eigvals_2x2([[0,-1],[1,0]])`
returns $(i,-i)$. Contrast P3: a real *symmetric* matrix always has real eigenvalues and a real
orthonormal eigenbasis.
