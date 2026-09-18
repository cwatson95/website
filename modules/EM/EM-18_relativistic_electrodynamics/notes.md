# EM-18 — Relativistic Electrodynamics (notes)

Special relativity is not a correction bolted onto electrodynamics — it is *built
into* it. Maxwell's equations already single out one speed c = 1/√(μ₀ε₀) for every
observer, and once that is accepted, **E** and **B** can no longer be separate,
frame-independent fields. This module packs them into the **field tensor** F^{μν},
shows how a boost rotates one into the other, and writes all four Maxwell equations
as a single covariant line.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e.
Page numbers are the *printed* book pages. The boost is along +**x̂** at speed
v = βc, with Lorentz factor γ = 1/√(1−β²) (`gamma`); c = `C` is built from `EPS0`
(`~EM-01`) and `MU0` (`~EM-08`).

## 1. Magnetism as a relativistic phenomenon
Griffiths' set-up (Gr §12.3.1, p.550): a wire, electrically neutral in the lab,
carries a steady current, and a point charge q drifts parallel to it. In the lab
the charge feels a purely **magnetic** force q**v**×**B**. Now ride along with the
charge. In *its* frame the charge is at rest, so it can feel no magnetic force at
all — yet whether it deflects cannot depend on who is watching. The resolution:
length contraction acts *differently* on the wire's positive and negative lattices
once they move at different speeds, so the wire is **charged** in the moving frame,
and the deflection is now blamed on a purely **electric** force. Same physics, two
names:
$$\text{magnetism} \;=\; \text{electrostatics} \;+\; \text{special relativity}.$$
Magnetism is simply what an electric field *looks like* to a moving observer; the
two are inseparable, which is the whole reason a single tensor must carry both.

## 2. How the fields transform under a boost
Boost from frame S to S′ moving at v = βc along +**x̂**. The components **along**
the boost are unchanged; the **transverse** components mix (Gr §12.3.2,
Eqs. 12.108–12.109, p.553):
$$
\begin{aligned}
E'_x &= E_x, & B'_x &= B_x,\\
E'_y &= \gamma\!\left(E_y - vB_z\right), & B'_y &= \gamma\!\left(B_y + \tfrac{v}{c^2}E_z\right),\\
E'_z &= \gamma\!\left(E_z + vB_y\right), & B'_z &= \gamma\!\left(B_z - \tfrac{v}{c^2}E_y\right).
\end{aligned}
$$
Code: `boost_fields(E, B, beta)`. Two limits are worth keeping. If **B** = 0 in S,
then S′ sees **B′** = −(1/c²)**v**×**E′** ≠ 0 — a pure **E** field *generates* a
**B** field (the demo: a transverse 1000 V/m field, boosted to 0.6c, sprouts
B′_z ≈ −2.5 μT). If v ≪ c then γ → 1 and **E′**_⊥ ≈ (**E** + **v**×**B**)_⊥, the
elementary "motional" combination. The inverse boost is the same map with β → −β
(`boost_fields(…, −beta)`), and it returns the original fields exactly.

## 3. The field tensor F^{μν}
The transformation law in §2 is *exactly* how the components of an antisymmetric
rank-2 tensor transform. Order the coordinates (ct, x, y, z) and define
(Gr §12.3.3, Eq. 12.118, p.562):
$$
F^{\mu\nu}=\begin{pmatrix}
0 & E_x/c & E_y/c & E_z/c\\
-E_x/c & 0 & B_z & -B_y\\
-E_y/c & -B_z & 0 & B_x\\
-E_z/c & B_y & -B_x & 0
\end{pmatrix},
\qquad F^{0i}=\frac{E_i}{c},\quad F^{ij}=-\varepsilon_{ijk}B_k .
$$
It is **antisymmetric**, F^{μν} = −F^{νμ}, so its diagonal vanishes and only six of
the sixteen entries are independent — precisely the three components of **E** and
the three of **B**. Code: `field_tensor(E, B)` builds it, `is_antisymmetric`
verifies the symmetry, and `fields_from_tensor` reads the fields back off the
entries (B_x = F^{yz}, B_y = F^{zx}, B_z = F^{xy}). Boosting the *fields* by §2 and
boosting the *tensor* by $F'^{\mu\nu}=\Lambda^{\mu}{}_{\alpha}\,\Lambda^{\nu}{}_{\beta}\,F^{\alpha\beta}$
are the same operation — that equivalence is the content of §12.3.3.

## 4. Electrodynamics in tensor notation
Collect the sources into the four-current J^ν = (cρ, **J**). The two
*inhomogeneous* Maxwell equations — Gauss's law and the Ampère–Maxwell law —
become one covariant equation (Gr §12.3.4, Eqs. 12.127–12.128, p.565):
$$\partial_\mu F^{\mu\nu}=\mu_0 J^{\nu}.$$
The ν = 0 component is ∇·**E** = ρ/ε₀; the three spatial components are
∇×**B** = μ₀**J** + μ₀ε₀ ∂**E**/∂t. The two *homogeneous* equations (∇·**B** = 0
and Faraday's law) say the **dual** tensor is divergence-free, ∂_μ G^{μν} = 0
(§12.3.4). Charge conservation comes for free: ∂_ν J^ν = (1/μ₀)∂_ν∂_μ F^{μν} = 0,
because a symmetric pair of derivatives contracts to zero against the antisymmetric
F. Four vector equations, one tensor line — the form that carries straight into
`~RE-08` and `~QF-03`.

## 5. The invariants E·B and B²−E²/c²
Boosts shuffle **E** and **B** between frames, but two scalars are pinned.
Contracting the tensor with itself, and with its dual G^{μν} = ½ε^{μναβ}F_{αβ},
gives (Gr §12.3.3, Prob. 12.47, p.562):
$$F_{\mu\nu}F^{\mu\nu}=2\!\left(B^2-\frac{E^2}{c^2}\right),
\qquad F_{\mu\nu}G^{\mu\nu}\;\propto\;\mathbf E\cdot\mathbf B .$$
So **E·B** and **B²−E²/c²** take the *same value in every inertial frame* (Griffiths
writes the second invariant as E²−c²B²; the two differ only by the constant factor
−c²). Code: `field_invariants(E, B)` returns the pair, and
`test_invariants_preserved_under_boost` confirms they survive boosts up to 0.99c.
Three consequences that need no calculation: if **E** ⊥ **B** in one frame
(E·B = 0) they are perpendicular in *all* frames; if E = cB in one frame (a light
wave — both invariants zero) it holds in all frames, so no observer can call a
light wave purely electric or purely magnetic; and you can never boost away a field
for which E·B ≠ 0.

## Where this goes
- `~RE-08` re-derives F^{μν} and ∂_μF^{μν} = μ₀J^ν from the relativity side, as
  index gymnastics on 4-vectors — the same objects, the covariant viewpoint.
- `~MA-16` is the tensor algebra (covariant vs contravariant indices, the metric
  η_{μν} that lowers F^{μν} → F_{μν}) used silently throughout this module.
- `~QF-03` promotes F^{μν} to the **field strength** of the U(1) gauge potential
  A^μ (the `~EM-09` four-potential): F_{μν} = ∂_μA_ν − ∂_νA_μ, and the Maxwell
  Lagrangian −¼F_{μν}F^{μν} is the seed of QED.
- Tensors as the network backbone: `~MA-16`/`~MA-17` → `~CM-13` (inertia tensor) →
  **EM-18** (field tensor) → `~RE-09`…`~RE-13` (curvature & the Einstein equations)
  — `KEY BRIDGE B5`.
