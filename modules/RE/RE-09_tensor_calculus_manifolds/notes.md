# RE-09 — Tensor Calculus on Manifolds (notes)

Conventions: indices run `0..n−1`; the metric is a position-dependent matrix
`g_{μν}(x)` with inverse `g^{μν}` (`g^{μλ}g_{λν}=δ^μ_ν`); `∂_i ≡ ∂/∂x^i`. We work
with general Riemannian metrics from `MA-17` (the round 2-sphere, the flat plane in
polar coordinates) and the flat Lorentzian `η = diag(−1,+1,+1,+1)`. The geometric
machinery is the same in both signatures.

## 1. From flat-space tensors to a curved manifold
In `RE-08`/`MA-16` the metric was a single constant matrix and "the inner product
of two vectors" was one global operation. On a curved manifold a vector lives in
the **tangent space** at a point, and the inner product
$$\langle u, v\rangle_x = g_{\mu\nu}(x)\,u^\mu v^\nu$$
is a *different* bilinear form at every point — the metric is now a **field**
`g_{μν}(x)`. (`MA-17`'s `sphere_metric` returns exactly such a callable
`x ↦ g`.) Tensors are objects whose components transform with the appropriate
powers of the Jacobian `∂x'^μ/∂x^ν` under a change of coordinates; a *tensor
equation* is then true in every coordinate system, which is the whole point of the
formalism (Zee §V.5). The new difficulty is **differentiating** such fields.

## 2. Why `∂_i V^k` is not a tensor
Write a vector field as `V = V^k(x)\,e_k`, where `e_k = ∂/∂x^k` is the coordinate
basis. Differentiating,
$$\partial_i V = (\partial_i V^k)\,e_k + V^k\,(\partial_i e_k),$$
and on a curved manifold (or merely in curvilinear coordinates) **the basis
vectors themselves vary from point to point**, so the second term does not vanish.
The naive `∂_i V^k` therefore captures only part of the change; under a coordinate
change it picks up an inhomogeneous piece `∝ ∂²x'/∂x∂x` and **fails to transform
as a tensor** (Zee §V.6: "as the vector varies from a given point to a neighbouring
point, the coordinate axes that define its components also change"). We need a
derivative that subtracts off the basis drift.

## 3. The Levi-Civita connection (Christoffel symbols)
Encode the basis drift in the **connection coefficients** `Γ^k_{ij}` via
`∂_i e_j = Γ^k_{ij} e_k`. Demanding two natural conditions fixes them **uniquely**:
- **torsion-free** (symmetric): `Γ^k_{ij} = Γ^k_{ji}`;
- **metric-compatible**: `∇g = 0` (lengths and angles are preserved by transport).

The unique solution is the **Levi-Civita connection** (`christoffel`, re-exported
from `MA-17`, derived in cpope §4.4):
$$\boxed{\;\Gamma^k_{ij} = \tfrac12\,g^{kl}\bigl(\partial_i g_{jl} + \partial_j g_{il} - \partial_l g_{ij}\bigr)\;}$$
Built from first derivatives of the metric, it is *determined by the geometry
alone*. On the unit sphere `g = diag(1, sin²θ)` it gives the closed forms
$$\Gamma^\theta_{\phi\phi} = -\sin\theta\cos\theta,\qquad \Gamma^\phi_{\theta\phi}=\Gamma^\phi_{\phi\theta} = \cot\theta,$$
with all other components zero (`test_sphere_christoffels_match_closed_form`).

## 4. The covariant derivative
Adding the connection correction to the partial derivative yields the **covariant
derivative**, which *does* transform as a tensor. For a contravariant vector and a
covariant vector (1-form) the corrections carry opposite signs:
$$\nabla_i V^k = \partial_i V^k + \Gamma^k_{ij} V^j,\qquad
  \nabla_i W_k = \partial_i W_k - \Gamma^j_{ik} W_j .$$
(`covariant_derivative_vector`, `covariant_derivative_covector`.) The opposite
sign is forced: `W_k V^k` is a scalar, so `∇_i(W_k V^k) = ∂_i(W_k V^k)` must hold,
and the two `Γ`-terms have to cancel (Zee §V.6). The defining property
**`∇_i g_{jk} = ∂_i g_{jk} − Γ^l_{ij}g_{lk} − Γ^l_{ik}g_{jl} = 0`**
(`metric_compatibility`, numerically `≈ 0` on both the sphere and the plane-polar
metric) is what lets `∇` commute with raising/lowering indices. On flat `η` every
`Γ = 0`, so `∇_i` collapses back to `∂_i` (`test_flat_…`): special relativity is
this formalism with the curvature switched off.

## 5. Parallel transport and holonomy
A vector is **parallel-transported** along a curve when its covariant derivative
along the curve vanishes, `dx^i \nabla_i V^k = 0`, i.e. each step drags it by
$$\delta V^k = -\,\Gamma^k_{ij}(x)\,V^j\,dx^i$$
(`parallel_transport`, cpope §4.6, Eq. 4.99). This is the curved-space notion of
"keeping a vector pointing the same way." The signature of curvature: transporting
a vector **around a closed loop does not return the original vector** — it comes
back rotated. The rotation angle (the *holonomy*) equals the integral of the
Gaussian curvature over the enclosed region (Gauss–Bonnet),
$$\Delta\alpha = \iint_{\Omega} K\,dA \;\;\xrightarrow{\text{unit sphere, }K=1}\;\; \text{Area}(\Omega).$$
Numerically, transporting a vector round a small lat–long rectangle on the unit
sphere rotates it by an angle equal (to `<0.1%`) to the enclosed area
`(\cosθ_0 − \cos(θ_0{+}Δθ))Δφ` (`test_holonomy_equals_enclosed_area`). The angle's
**sign tracks the loop's orientation** (reversing the loop negates it — verified in
`test_holonomy_sign_flips_…`); its magnitude is the coordinate-independent
curvature content, and a zero-area (out-and-back) path produces no holonomy.
Curvature **is** holonomy-per-unit-area — the bridge to `RE-11`
(`ΔV^μ = −½R^μ_{νρσ}V^ν ΔA^{ρσ}`, cpope Eq. 4.117).

## 6. The geodesic equation
A **geodesic** is a curve that parallel-transports its own tangent `\dot x` — the
straightest possible path. Setting `\dot x^i\nabla_i \dot x^k = 0` gives
$$\ddot x^k + \Gamma^k_{ij}\,\dot x^i\dot x^j = 0,$$
so the covariant acceleration `\ddot x^k = -\Gamma^k_{ij}\dot x^i\dot x^j`
(`geodesic_acceleration`) vanishes. On the sphere the **equator** (`θ=π/2`, `φ`
varying) is a great circle and has zero geodesic acceleration, while a **circle of
latitude** `θ=const≠π/2` does not: `\ddot x^\theta = \sin\theta\cos\theta\,\dot\phi^2 \neq 0`
(`test_geodesic_great_circle_vs_latitude`) — you must steer to hold a latitude, the
defining feature of a non-geodesic. This is the seed of `RE-12` (free fall and the
bending of light follow geodesics).

## 7. Christoffels are not tensors — the equivalence principle
Because of the inhomogeneous `∂²x'/∂x∂x` term in their transformation law, the
`Γ^k_{ij}` are **not** tensor components: a quantity that is nonzero in one
coordinate system can be made to **vanish at any chosen point** by passing to
**locally inertial / geodesic-normal coordinates** there (cpope §4.7 Taylor-expands
`Γ(x)` to construct them). What cannot be removed is the *derivative* of `Γ` — the
Riemann tensor (`RE-11`). That a freely-falling observer can always choose
coordinates in which `Γ = 0` at their location — gravity locally transformed away —
is precisely the mathematical face of the **equivalence principle** (`RE-10`):
gravitation is not a force field on a fixed background but the curvature of
spacetime, felt through the connection.
