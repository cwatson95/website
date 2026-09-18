# MA-04 — Linear Algebra (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages.

## 1. Matrices and their algebra
A matrix is a linear map. Addition, scalar multiples, and the product
(AB)_{ik} = Σ_j A_{ij}B_{jk} [B §6 *Matrix Operations* p.114]; the transpose Aᵀ,
trace tr A = ΣA_{ii}, and identity I. Code: `matmul`, `matvec`, `transpose`,
`trace`, `identity`.

## 2. Determinant, solving, inverse
The determinant measures the volume scaling and signals invertibility (det = 0 ⇔
singular) [B §3 *Determinants; Cramer's Rule* p.89]. A linear system A**x** = **b**
is solved by **row reduction** (Gaussian elimination) [B §2 *Matrices; Row
Reduction* p.83]; the inverse solves A**x** = **e**_j column by column. Code:
`det` (partial-pivot elimination), `solve` (Gauss–Jordan), `inverse`.
*(Boas's term is "row reduction"; "Gaussian elimination" is the same procedure.)*

## 3. The eigenvalue problem
A**v** = λ**v** with **v** ≠ 0 means the characteristic equation det(A − λI) = 0
holds [B §11 *Eigenvalues and Eigenvectors; Diagonalizing Matrices* p.148]. For a
2×2 this is λ² − (tr A)λ + det A = 0, with roots that may be complex (a rotation
gives ±i). Code: `eigvals_2x2`.

## 4. Symmetric matrices diagonalize orthogonally
A **real symmetric** matrix (A = Aᵀ) has **real eigenvalues** and a full set of
**orthonormal eigenvectors**, so with Q = [**v**₁ … **v**_n] (eigenvectors as
columns) [B §11 pp.152–161; applications §12 p.162]:
$$A=Q\,\Lambda\,Q^{\mathsf T},\qquad \Lambda=\operatorname{diag}(\lambda_1,\dots,\lambda_n),\qquad Q^{\mathsf T}Q=I.$$
Code: `eig_symmetric` returns (eigenvalues, orthonormal eigenvectors);
`reconstruct` rebuilds QΛQᵀ. Two invariants the tests check: Σλ_i = tr A and Πλ_i = det A.

## 5. How `eig_symmetric` works — Jacobi rotations
Repeatedly apply a plane rotation that zeroes the largest off-diagonal pair (p,q):
choose the angle from θ = (a_qq − a_pp)/(2a_pq), giving t = tanφ from t² + 2θt − 1 = 0,
then c = 1/√(t²+1), s = tc. Each rotation A → GᵀAG shrinks the off-diagonal norm;
accumulating the rotations in Q yields the eigenvectors. It converges quadratically
for symmetric matrices — a clean, self-contained diagonalizer.

## Where this goes
- `~CM-13`: the inertia tensor is symmetric ⇒ its eigenvectors are the **principal
  axes** and its eigenvalues the principal moments — exactly `eig_symmetric`.
- `~CM-16`: small-oscillation normal modes are a (generalized) eigenproblem.
- `~QM-05`/`~QM-06`: observables are Hermitian operators; measurement values are
  eigenvalues and states diagonalize them (the complex analogue of §4).
