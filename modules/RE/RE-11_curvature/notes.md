# RE-11 — Curvature (notes)

Conventions: metric `g_{μν}(x)`, connection `Γ` the Levi-Civita connection of
RE-09, Riemann `R^ρ_{σμν} = ∂_μΓ^ρ_{νσ} − ∂_νΓ^ρ_{μσ} + Γ^ρ_{μλ}Γ^λ_{νσ} − Γ^ρ_{νλ}Γ^λ_{μσ}`
(MA-17's convention, returned as `R[ρ][σ][μ][ν]`). Geometrized units `G = c = 1`.

## 1. Why a *tensor* measures curvature
The connection coefficients `Γ` are not tensors (RE-09 §7): at any point you can
choose locally-inertial coordinates with `Γ = 0` there. So `Γ` cannot be the
gravitational field. The combination that **does** transform as a tensor is the
**commutator of covariant derivatives** on a vector,
$$[\nabla_\mu, \nabla_\nu]\,V^\rho = R^\rho{}_{\sigma\mu\nu}\,V^\sigma ,$$
which involves *derivatives* of `Γ`. `R = 0` everywhere ⟺ parallel transport is
path-independent ⟺ spacetime is flat. Curvature is the failure of second
covariant derivatives to commute — equivalently (RE-09 §5) the holonomy per unit
area of parallel transport around a closed loop.

## 2. Symmetries and the count of independent components
Lowering the first index, `R_{ρσμν} = g_{ρλ}R^λ_{σμν}`, the Riemann tensor obeys
- **antisymmetry** in each pair: `R_{ρσμν} = −R_{σρμν} = −R_{ρσνμ}`;
- **pair symmetry**: `R_{ρσμν} = R_{μνρσ}`;
- **first Bianchi**: `R_{ρ[σμν]} = 0` (cyclic sum on the last three).

These cut the `n⁴` components to `n²(n²−1)/12` independent ones: **1** in 2-D (the
Gaussian curvature `K`, with `R = 2K`), **6** in 3-D (Ricci determines Riemann
completely), and **20** in 4-D (Ricci is only 10 of them — the other 10, the
**Weyl tensor**, are the free gravitational field that propagates as waves,
RE-16). `test_riemann_antisymmetry` checks the last-pair antisymmetry numerically.

## 3. Ricci, scalar, and the Einstein tensor
Contracting Riemann gives the lower-rank curvatures:
$$R_{\sigma\nu} = R^\rho{}_{\sigma\rho\nu}\ \text{(Ricci)},\qquad
  R = g^{\sigma\nu}R_{\sigma\nu}\ \text{(scalar)},$$
and the **Einstein tensor**
$$\boxed{\,G_{\mu\nu} = R_{\mu\nu} - \tfrac12 R\,g_{\mu\nu}\,}$$
(`einstein_tensor`). In `n` dimensions its trace is `g^{μν}G_{μν} = (1−n/2)R`
(`test_einstein_trace_identity`: 0 in 2-D, `−R/2` in 3-D, `−R` in 4-D). `G_{μν}`
is singled out among combinations of Ricci and `g` by the **contracted Bianchi
identity**
$$\nabla_\mu G^{\mu\nu} = 0 ,$$
an *automatic* divergence-free-ness. That is exactly the property a source needs:
setting `G_{μν} ∝ T_{μν}` then forces `∇_μ T^{μν}=0`, local energy–momentum
conservation, *for free* — the structural reason the Einstein equations of RE-13
take this form.

## 4. Geodesic deviation — curvature you can feel
Take a one-parameter family of geodesics with tangent `u^a` and connecting vector
`ξ^a` (the separation to a neighbour). Their relative acceleration is
$$\frac{D^2\xi^a}{d\tau^2} = -R^a{}_{bcd}\,u^b\,\xi^c\,u^d$$
(`geodesic_deviation`). In flat space the right side vanishes — free particles
stay in formation. Near a mass it does not: this is the **tidal field**, and the
equation says tidal forces *are* the Riemann tensor — the precise, frame-
independent content of RE-10 §6 ("what free fall cannot remove"). Positive
curvature **focuses**: on the unit 2-sphere two meridians, parallel at the
equator, accelerate toward each other (`A·ξ < 0`, and `A^θ = −sin²θ` exactly for a
`φ`-geodesic separated in `θ`). The focusing of geodesics by the Ricci tensor
(via `R_{μν}u^μu^ν ≥ 0` for ordinary matter) is the engine of the singularity
theorems.

## 5. Curvature invariants and singularities
Tensor components are coordinate-dependent, so "the curvature blows up" must be
phrased with **scalars**. The simplest is the **Kretschmann scalar**
$$K = R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}\qquad(\texttt{kretschmann}).$$
For Schwarzschild (a *vacuum* solution: `R_{μν}=0`, `R=0`, `G_{μν}=0`, so Ricci-
based scalars are all zero) the Kretschmann scalar is
$$K = \frac{48\,M^2}{r^6}.$$
It is **finite at the horizon** `r = 2M` — the singularity there is only in the
coordinates (Schwarzschild's `t,r` break down, not spacetime) — and **diverges at
`r = 0`**, the genuine physical singularity. This single invariant decides
"coordinate vs real," and `test_schwarzschild_kretschmann…` reproduces `48M²/r⁶`
to ~1%. That `R_{μν}=0` but `R_{μνρσ}≠0` is the statement that **vacuum gravity is
pure Weyl curvature** — there is a field in empty space, which is why RE-16's
gravitational waves can travel through it.

## 6. Constant-curvature (maximally symmetric) spaces
When curvature is the same in every direction at every point,
$$R_{\rho\sigma\mu\nu} = \frac{R}{n(n-1)}\,(g_{\rho\mu}g_{\sigma\nu} - g_{\rho\nu}g_{\sigma\mu}),$$
with `R` constant. The unit `n`-sphere realises this with `R = n(n−1)/a²` (the
code checks `R = 2/a²` on `S²` and `R = 6/a²` on `S³`). These three geometries —
positive (sphere), zero (flat), negative (hyperbolic) curvature — are exactly the
spatial slices of the FLRW cosmologies in RE-15, so the curvature algebra here is
reused there with `k = +1, 0, −1`.
