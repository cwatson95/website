# RE-03 — Lorentz Transformations (notes)

Conventions: `c = 1`, event `x = (ct, x, y, z)`, η = diag(−1,+1,+1,+1),
`β = v/c`, `γ = 1/√(1−β²)`. Frame **S′** moves at velocity `+β x̂` relative to S.

## 1. From the postulates to the boost
The two postulates of `RE-02` are (i) the laws of physics are the same in every
inertial frame and (ii) the speed of light `c` is the same in every inertial
frame. Homogeneity of spacetime forces the map S → S′ to be **linear**, and (in
the standard configuration, motion along x, axes aligned) to leave `y, z`
untouched. So in the `(ct, x)` plane,
$$\begin{pmatrix}ct'\\x'\end{pmatrix}=\begin{pmatrix}A&B\\D&E\end{pmatrix}\begin{pmatrix}ct\\x\end{pmatrix}.$$

Three conditions pin the four entries:
- The origin of S′ (`x' = 0`) moves as `x = βct` in S ⇒ `D = −Eβ`.
- A light pulse `x = ct` must map to `x' = ct'` (postulate ii) ⇒ the form is
  symmetric, `A = E`, `B = D`.
- The transformation and its inverse (swap S↔S′, β→−β) must be consistent ⇒
  `A = γ`.

The result is the **Lorentz boost** (Griffiths Eq. 12.18):
$$ct' = \gamma(ct-\beta x),\qquad x' = \gamma(x-\beta ct),\qquad y'=y,\ z'=z,$$
$$\Lambda(\beta)=\begin{pmatrix}\gamma&-\gamma\beta&0&0\\-\gamma\beta&\gamma&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}.$$
As `c→∞` (β = v/c → 0, γ → 1) this collapses to the **Galilean** transformation
`x' = x − vt`, `t' = t` — the `~CM-03` limit (Griffiths Prob. 12.18).

## 2. The defining property
A boost is exactly the linear map that preserves the metric:
$$\boxed{\ \Lambda^{\mathsf T}\,\eta\,\Lambda=\eta\ }$$
Equivalently it preserves the interval `s² = ηₘₙ xᵐxⁿ` of *every* event, and in
particular keeps the light cone `s²=0` fixed — that **is** the constancy of `c`.
The full set of such Λ (boosts in any direction + spatial rotations) is the
**Lorentz group** O(1,3). `preserves_eta` tests the boxed identity directly.

## 3. Rapidity: a boost is a hyperbolic rotation
Write `γ = cosh φ`, `γβ = sinh φ`, consistent because `cosh²−sinh² = 1` matches
`γ²(1−β²) = 1`. Then
$$\phi=\operatorname{artanh}\beta,\qquad
\Lambda(\phi)=\begin{pmatrix}\cosh\phi&-\sinh\phi\\-\sinh\phi&\cosh\phi\end{pmatrix}.$$
This is a rotation through an **imaginary angle**: compared with an ordinary
rotation `R(θ) = [[cosθ,−sinθ],[sinθ,cosθ]]`, send `θ → iφ` and the cosh/sinh
appear (Griffiths Prob. 12.19). Two consequences are immediate:
- **Boosts along one axis form a one-parameter group** `≅ (ℝ, +)`: composing two
  collinear boosts adds the rapidities, `Λ(φ₁)Λ(φ₂) = Λ(φ₁+φ₂)`.
- `c` corresponds to `φ → ∞`: no finite rapidity, hence no boost, reaches it.

## 4. Velocity addition = rapidity addition
Collinear boosts compose, so velocities combine by
$$w=\frac{u+v}{1+uv}\quad(c=1),\qquad\text{equivalently}\quad
\operatorname{artanh}w=\operatorname{artanh}u+\operatorname{artanh}v .$$
(`velocity_add`; Griffiths Ex. 12.6.) Because `tanh` saturates at 1: if `|u|,|v|<1`
then `|w|<1`, and `v=1` gives `w=1` — light stays at light speed in every frame.
For small speeds `w ≈ u+v` (Galilean). The **non-collinear** case has no such tidy
scalar form; the clean way is to carry the object's 4-velocity between frames,
$$\mathbf v_{S}= \text{3-vel}\big(\Lambda(-\mathbf u)\,U'(\mathbf v')\big),
\qquad U=\gamma_v(1,\mathbf v),$$
which is what `velocity_add_3d` does. (Composing two **non-parallel** boosts is
*not* a pure boost — it is a boost times a rotation, the **Thomas–Wigner**
rotation; here we only verify the product is still a Lorentz transformation.)

## 5. Structure of the Lorentz group
From `ΛᵀηΛ = η`: taking determinants gives `(det Λ)² = 1 ⇒ det Λ = ±1`, and the
00-component obeys `(Λ⁰₀)² ≥ 1 ⇒ Λ⁰₀ ≥ 1` or `≤ −1`. This splits O(1,3) into four
pieces by the signs of `det Λ` and `Λ⁰₀`:
- **proper** (`det = +1`) vs improper (parity flip `P`, `det = −1`);
- **orthochronous** (`Λ⁰₀ ≥ 1`, preserves time direction) vs not (time reversal `T`).

Boosts and rotations live in the identity component `SO⁺(1,3)` (proper +
orthochronous); `is_proper` and `is_orthochronous` detect the others. `P` and `T`
are still metric-preserving Lorentz transformations — that is why the test builds
them explicitly and checks `preserves_eta(P)` while `not is_proper(P)`.

## 6. The interval and 4-velocity (handed to RE-05)
The invariant `dot4(a,b) = −a⁰b⁰ + 𝐚·𝐛` and `interval2(x) = dot4(x,x)` are the
seeds of `RE-05` (Minkowski space). One object built here recurs everywhere: the
**4-velocity** `U = dx/dτ = γ(1, 𝐯)`, a unit timelike vector `U·U = −1`, whose
invariance under boosts (`test_four_velocity_normalisation`) is the backbone of
relativistic dynamics in `RE-06`.
