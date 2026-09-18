# MA-16 — Tensor Analysis & Index Notation (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. All in **Chapter 10, Tensor Analysis**.

## 1. Index notation and the summation convention
Write components with indices and **sum over any index that appears twice** (once
up, once down) [B §3 *Tensor Notation and Operations* p.502]:
$$a_i b_i\equiv\sum_i a_i b_i,\qquad (A\mathbf x)_i=A_{ij}x_j,\qquad
\operatorname{tr}A=A_{ii}.$$
A tensor is an object whose components transform in a definite way under a change
of coordinates; rank = number of indices (scalar 0, vector 1, matrix 2). Code:
`matvec`, and the contraction sums throughout.

## 2. The two fundamental symbols
[B §5 *Kronecker Delta and Levi-Civita Symbol* p.508]
- **Kronecker delta** δ_ij = 1 if i=j else 0 — the identity; it *renames/contracts*
  an index: δ_ij a_j = a_i.
- **Levi-Civita symbol** ε_{ijk…} = +1/−1 for an even/odd permutation, 0 if any
  index repeats — totally antisymmetric. In 3-D it builds the cross product and
  the curl: (a×b)_i = ε_{ijk} a_j b_k.
The single most useful identity (the engine behind every "BAC–CAB" vector
identity) [B §5 p.508]:
$$\sum_i \varepsilon_{ijk}\,\varepsilon_{ilm}=\delta_{jl}\delta_{km}-\delta_{jm}\delta_{kl}.$$
Code: `levi_civita_symbol`, `levi_civita3`, `cross_via_levi_civita`,
`eps_delta_identity_holds`. The determinant is the antisymmetric contraction
det A = ε_{i₁…iₙ} A_{1i₁}…A_{niₙ}, and the inverse follows as adj/det (Cramer) —
`det_levi_civita`, `inverse`.

## 3. Contravariant vs covariant — and why we need both
Under a coordinate change qⁱ → q′ⁱ, a **contravariant** vector (upper index, like a
displacement dxⁱ) transforms with ∂q′ⁱ/∂qʲ, while a **covariant** vector (lower
index, like a gradient ∂φ/∂xⁱ) transforms with the *inverse*, ∂qʲ/∂q′ⁱ [B §10
*Non-Cartesian Tensors* p.529]. In an orthonormal Cartesian frame the two coincide,
which is why elementary vector algebra never distinguishes them; in curvilinear or
relativistic settings they differ and the bookkeeping matters.

## 4. The metric tensor
The **metric** g_ij sets lengths and angles and converts between the two index
types [B §10 p.529; §8 *Curvilinear Coordinates* p.521]:
$$ds^2=g_{ij}\,dx^i dx^j,\qquad v_i=g_{ij}v^j,\qquad v^i=g^{ij}v_j,\qquad g^{ik}g_{kj}=\delta^i_j.$$
For coordinates q with Cartesian embedding x(q), the induced metric is
$$g_{ij}=\sum_k\frac{\partial x^k}{\partial q^i}\frac{\partial x^k}{\partial q^j}=(J^{\mathsf T}J)_{ij}.$$
Polar → diag(1, r²) (ds²=dr²+r²dθ²); spherical → diag(1, r², r²sin²θ) — exactly the
line elements of `~MA-03`. Code: `metric_from_map`, `lower_index`, `raise_index`,
`inverse` (gives g^{ij}).

## 5. The invariant
The whole point of the up/down machinery: a fully contracted expression is a
**scalar**, the same in every coordinate system. The cleanest case is length,
$$\lvert v\rvert^2=g_{ij}v^iv^j,$$
which the code checks by comparing the polar-coordinate value g_ij vⁱvʲ to the
Cartesian sum Σ_k(Vᵏ)² of the *same* vector (V = J v). Code: `inner`; the test
confirms invariance for several vectors.

## Where this goes
- `~CM-13`: the inertia tensor I_ij is a rank-2 Cartesian tensor; diagonalizing it
  (`~MA-04`) gives the principal axes [B §4 *Inertia Tensor* p.505].
- `~RE-08`: 4-vectors and the Minkowski metric η = diag(−1,1,1,1); raising/lowering
  with η is §4 above with an indefinite metric.
- `~EM-18`: the field tensor F^{μν} packs E and B; Maxwell's equations become
  ∂_μ F^{μν}=μ₀ Jⁿ — index notation doing real work.
- `~MA-17`: differentiating tensors on a curved space needs the connection
  (Christoffel symbols); the metric of §4 is the starting datum.
