# MA-17 — Differential Geometry (notes)

Citation key (full details + PDF pages in `refs.md`): **W** = Warner,
*Foundations of Differentiable Manifolds and Lie Groups*; **dR** = de Rham,
*Differentiable Manifolds*; **B** = Boas 3e. Pages are the *printed* book pages.
This is an **[adv]** module; the curvature half is the math of `~RE-09…RE-13`.

## 1. Manifolds and forms (the setting)
A **differentiable manifold** is a space that looks locally like Rⁿ, glued by
smooth coordinate changes [dR §1 p.3; W §1.14 p.13 for tangent vectors]. On it live
**differential p-forms** — antisymmetric, the things you integrate over
p-dimensional regions [W §2 *Tensors and Differential Forms* p.56; dR §4 p.15].
A 0-form is a function; a 1-form is "∑ aᵢ dxⁱ"; the **wedge** ∧ is the antisymmetric
product (dx∧dy = −dy∧dx).

## 2. The exterior derivative and d² = 0
The **exterior derivative** d maps p-forms to (p+1)-forms [W p.65; dR §4 p.17], and
its defining property is that it is **nilpotent**:
$$\boxed{\,d^2=0\,}.$$
In R³ this single statement contains all of vector calculus (`~MA-02`):
- d on a **0-form** f = **grad** f,
- d on a **1-form** = **curl**,
- d on a **2-form** = **div**.
So d²=0 reads **curl(grad f)=0** and **div(curl V)=0** — the two "automatically
zero" identities, now one principle. Code: `gradient`, `curl`, `divergence`; the
test checks d²=0 at sample points. (The converse — when a closed form dω=0 is exact
ω=dα — is the **Poincaré lemma**, the seed of de Rham cohomology, `~MA-22`.)

## 3. The metric, connection, and Christoffel symbols
To differentiate *tensors* on a curved space you need a **connection**: the metric
g (from `~MA-16`) supplies the unique torsion-free metric-compatible one, the
**Levi-Civita connection**, with **Christoffel symbols**
$$\Gamma^k_{ij}=\tfrac12\,g^{kl}\big(\partial_i g_{jl}+\partial_j g_{il}-\partial_l g_{ij}\big).$$
These are *not* tensor components (they vanish in a locally-flat frame); they encode
how the basis vectors twist from point to point. Code: `christoffel` (built from a
callable metric by finite differences); the test matches the sphere's analytic
Γᶿ_φφ=−sinθcosθ and Γᶲ_θφ=cotθ.

## 4. Curvature
The **Riemann tensor** measures the failure of second covariant derivatives to
commute — equivalently, the rotation a vector picks up on a tiny closed loop:
$$R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}
+\Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma}-\Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}.$$
Contracting gives the **Ricci tensor** R_{σν}=Rᵖ_{σρν} and the **scalar curvature**
R=gˢᵛR_{σν}; in 2-D the **Gaussian curvature** is K=R/2. Code: `riemann`, `ricci`,
`ricci_scalar`, `gaussian_curvature_2d`.

## 5. Theorema Egregium (the showcase)
Gauss's "remarkable theorem": curvature is **intrinsic** — computable from the
metric (distances within the surface) alone, with no reference to how the surface
sits in space. The code demonstrates it numerically:
- **round 2-sphere** of radius a, g=diag(a², a²sin²θ): K = **1/a²** everywhere
  (the test confirms 1, 0.25, 4 for a=1, 2, 0.5);
- **flat plane in polar coordinates**, g=diag(1, r²): K = **0**, even though the
  metric has a position-dependent r² — curvy *coordinates* are not curvature.
This is exactly why gravity is geometry (`~RE-10`): tidal forces are the Riemann
tensor, and "flat vs curved spacetime" is a coordinate-independent fact.

## Where this goes
- `~RE-09`: covariant derivatives, parallel transport, and the geodesic equation
  ẍᵏ+Γᵏ_ij ẋⁱẋʲ=0 are §3 in spacetime.
- `~RE-11`/`~RE-13`: the Riemann/Ricci tensors of §4 are the left side of Einstein's
  equation G_{μν}=8πT_{μν} — curvature sourced by energy.
- `~MA-22`: d²=0 (§2) and the Poincaré lemma open de Rham cohomology, a topological
  invariant built from forms.
