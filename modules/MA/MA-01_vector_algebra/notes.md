# MA-01 — Vector Algebra (notes)

A vector in 3-space is written by its components in an orthonormal right-handed
basis (x̂, ŷ, ẑ):  **a** = (a₀, a₁, a₂).  All four products below are built from
components, so the same formulas hold whether the components are numbers, symbols,
or functions of a parameter.

## 1. Dot (scalar) product
$$\mathbf a\cdot\mathbf b = a_0b_0+a_1b_1+a_2b_2 = |\mathbf a|\,|\mathbf b|\cos\theta.$$

- **Commutative, distributive, bilinear.**  a·a = |a|².
- **Geometry:** projection length. The scalar projection of **a** on **b** is
  a·b̂, and the vector projection is (a·b/ b·b) **b** (`projection`); what's left,
  **a** − proj, is the `rejection`, perpendicular to **b**.
- **Test:** a·b = 0  ⇔  a ⟂ b.

## 2. Cross (vector) product
$$(\mathbf a\times\mathbf b)_i=\varepsilon_{ijk}a_jb_k,\qquad
\mathbf a\times\mathbf b=
\begin{vmatrix}\hat x&\hat y&\hat z\\ a_0&a_1&a_2\\ b_0&b_1&b_2\end{vmatrix}.$$

- **Anticommutative:** a×b = −b×a;  a×a = 0.  Distributive, **not** associative.
- **Geometry:** a×b = |a||b|sinθ n̂, with n̂ the right-hand-rule normal. Its
  magnitude is the area of the parallelogram on **a**, **b** (triangle area = ½|a×b|).
- **Test:** a×b = 0  ⇔  a ∥ b.

## 3. Scalar triple product  (box product)
$$\mathbf a\cdot(\mathbf b\times\mathbf c)=\det[\mathbf a\ \mathbf b\ \mathbf c].$$

- **Signed volume** of the parallelepiped spanned by a, b, c.
- **Cyclic symmetry:** a·(b×c) = b·(c×a) = c·(a×b); swapping any two flips the sign.
- The dot and cross may be exchanged: a·(b×c) = (a×b)·c.
- **Test:** a·(b×c) = 0  ⇔  a, b, c are **coplanar** (linearly dependent).

## 4. Vector triple product  ("BAC–CAB")
$$\mathbf a\times(\mathbf b\times\mathbf c)=\mathbf b(\mathbf a\cdot\mathbf c)-\mathbf c(\mathbf a\cdot\mathbf b).$$
Lies in the plane of **b**, **c**. Note (a×b)×c = b(a·c) − a(b·c) is *different* —
the cross product is not associative, so parentheses matter.

## 5. Identities worth knowing (all checked in the tests / demo)
- **Lagrange:**  |a×b|² = |a|²|b|² − (a·b)².
- **Jacobi:**  a×(b×c) + b×(c×a) + c×(a×b) = 0.
- **Binet–Cauchy:**  (a×b)·(c×d) = (a·c)(b·d) − (a·d)(b·c).
- ε–δ identity:  εᵢⱼₖ εᵢₗₘ = δⱼₗδₖₘ − δⱼₘδₖₗ  (the engine behind BAC–CAB & Lagrange).

## 6. Vectors that are functions  → why this module returns functions
When the components depend on a parameter, **a**(t) = (a₀(t), a₁(t), a₂(t)), the
products are taken pointwise, and they obey product rules just like scalars:
$$\frac{d}{dt}(\mathbf a\cdot\mathbf b)=\mathbf a'\cdot\mathbf b+\mathbf a\cdot\mathbf b',
\qquad
\frac{d}{dt}(\mathbf a\times\mathbf b)=\mathbf a'\times\mathbf b+\mathbf a\times\mathbf b'.$$
(Order is preserved in the cross-product rule because a×b ≠ b×a.)

This is exactly why the code *lifts* each operation to accept callables: given a
trajectory **r**(t) and velocity **v**(t)=**r**′(t),

- `dot(r, v)`  → ½ d/dt|r|²  (rate of change of distance-squared),
- `cross(r, v)` → the specific angular momentum **r**×**v** as a function of t,
- `norm(v)`    → the speed |v(t)|.

These become the building blocks of `~CM-01` (kinematics) and `~CM-09` (angular
momentum & torque, **N** = **r**×**F**, d**L**/dt = **N**).
