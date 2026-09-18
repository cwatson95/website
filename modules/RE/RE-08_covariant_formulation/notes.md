# RE-08 — Covariant Formulation of Special Relativity (notes)

Conventions: `c = 1`, event `x^μ = (ct, x, y, z)`, η = diag(−1,+1,+1,+1), Greek
indices 0..3, Einstein summation (a repeated upper+lower pair is summed). A boost
Λ is an RE-03 Lorentz transformation (`Λᵀ η Λ = η`).

## 1. A tensor is what transforms like a tensor
The defining idea (Zee §I.4): a 4-tensor is an object carrying a **definite
Lorentz transformation law**, fixed by its rank and by which indices are up/down.

- **Scalar** (rank 0): `s → s`. Frame-independent (e.g. `s²`, rest mass, proper time).
- **Contravariant** `V^μ` (index up): transforms like the coordinate displacement,
  $$V'^\mu = \Lambda^\mu{}_\nu\,V^\nu \qquad(\texttt{transform\_vector}).$$
- **Covariant** `V_μ` (index down): transforms with the **inverse-transpose**,
  $$V'_\mu = (\Lambda^{-1})^\nu{}_\mu\,V_\nu \qquad(\texttt{transform\_covector}).$$
- **Rank-2** `T^{μν}`: one factor of Λ per index (Griffiths Eq. 12.115),
  $$T'^{\mu\nu} = \Lambda^\mu{}_\alpha\,\Lambda^\nu{}_\beta\,T^{\alpha\beta}
    \qquad(\texttt{transform\_tensor2}).$$

The pay-off — **manifest covariance**: if `A^μ = B^μ` in one frame, then in any
other `A'^μ = Λ^μ_ν A^ν = Λ^μ_ν B^ν = B'^μ`; the equality is preserved because both
sides carry the same index and so transform identically. *A tensor equation true
in one inertial frame is true in all of them.* Building physics from tensors is
therefore the way to guarantee it respects relativity.

## 2. Raising and lowering: contra ↔ covariant with η
The metric is the dictionary between the two index positions (MA-16):
$$V_\mu = \eta_{\mu\nu}V^\nu\ (\texttt{lower}),\qquad
  V^\mu = \eta^{\mu\nu}V_\nu\ (\texttt{raise\_}),\qquad \eta^{\mu\nu}=\eta_{\mu\nu}.$$
With mostly-plus η this just flips the sign of the time component:
`V_μ = (−V⁰, V¹, V², V³)`. Lowering then raising is the identity because
`η^{μα}η_{αν} = δ^μ_ν`. That the *covariant* `V_μ` really does transform by the
inverse-transpose law is forced by consistency: lowering and boosting commute
(`test_lowered_vector_transforms_covariantly`).

## 3. Lorentz invariants from full contraction
Tie off **every** index (each upper with a lower) and the result is a Lorentz
scalar — nothing left to transform:
- `V^μ V_μ = η_{μν}V^μV^ν = V·V` — the squared norm (RE-05's interval / mass shell).
- `V^μ W_μ` — invariant precisely **because** covectors carry the inverse-transpose
  law: `V'^μ W'_μ = Λ^μ_ν V^ν (Λ⁻¹)^ρ_μ W_ρ = δ^ρ_ν V^ν W_ρ = V^ν W_ν`
  (`test_contra_co_contraction_is_invariant`).
- the **trace** `T^μ_μ = η_{μν}T^{μν} = −T^{00}+T^{11}+T^{22}+T^{33}` (`trace`) — note
  the metric, not the bare diagonal sum, supplies the minus sign.
- the **double contraction** `S_{μν}T^{μν}` (`double_contract`), e.g. `F_{μν}F^{μν}`
  in EM-18.

All are unchanged by any boost (`test_trace_is_invariant`).

## 4. The 4-gradient is covariant; the d'Alembertian is a scalar
Differentiating a scalar field by the **contravariant** coordinates produces a
**covariant** object — the index comes out *down*:
$$\partial_\mu \equiv \frac{\partial}{\partial x^\mu}
  = \Big(\frac{\partial}{\partial (ct)},\ \nabla\Big),\qquad
  \partial^\mu = \eta^{\mu\nu}\partial_\nu = \Big(-\frac{\partial}{\partial(ct)},\ \nabla\Big).$$
(The minus on `∂^0` is the giveaway that `∂_μ` is naturally covariant.) A clean
check: for `f = x·x`, `∂_μ f = 2x_μ` — the lowered position
(`test_four_gradient_is_two_x_lower`). Contracting the gradient with itself gives
the **d'Alembertian**, a Lorentz scalar operator (Griffiths Eq. 12.138):
$$\Box \equiv \partial^\mu\partial_\mu = \eta^{\mu\nu}\partial_\mu\partial_\nu
  = -\frac{\partial^2}{\partial(x^0)^2} + \nabla^2 .$$
Because it is built from the invariant η, `□` has the *same form in every frame*;
`□f` is frame-independent (`test_dalembertian_is_a_lorentz_scalar`). It governs
wave propagation: a null plane wave `cos(k_μx^μ)` with `k·k = 0` satisfies
`□f = −(k·k)\,f = 0` (`test_null_plane_wave_solves_wave_equation`), and in EM-18
the covariant Maxwell equations collapse to `□A^μ = −μ₀ J^μ` in Lorenz gauge.
Quick closed values used in the tests: `□(x^0)² = −2`, `□(x^i)² = +2`, and
`□(x·x) = 2η^{μν}η_{μν} = 2·4 = 8`.

## 5. Manifestly covariant physics — the standard 4-vectors
Differentiating a worldline by the **invariant** proper time τ promotes 3-vectors
to 4-vectors with definite transformation laws (RE-05 → RE-06):
- **4-velocity** `U^μ = dx^μ/dτ = γ(1,𝐯)`, unit timelike `U·U = −1`.
- **4-acceleration** `A^μ = dU^μ/dτ`; differentiating `U·U=−1` gives the identity
  `U·A = 0` (4-acceleration is always Minkowski-orthogonal to 4-velocity).
- **4-momentum** `p^μ = mU^μ = (E,𝐩)`, invariant `p·p = −m²` (the mass shell).
- **4-force** `K^μ = dp^μ/dτ`, and the **4-current** `J^μ = (cρ, 𝐉)` whose
  continuity equation is the manifestly covariant `∂_μ J^μ = 0`.

Each is a tensor equation, so each holds in every frame at once — that is the
whole reason for the formalism.

## 6. The invariant tensors η, δ, ε
Some tensors have the *same components in every frame*:
- **η** (as `η^{μν}`): `Λ^μ_α Λ^ν_β η^{αβ} = η^{μν}` is just the Lorentz condition
  `ΛηΛᵀ = η` rewritten (`test_eta_is_an_invariant_tensor`). The metric is the
  fixed background of SR.
- **Kronecker δ** (mixed `δ^μ_ν`): `Λ^μ_α (Λ⁻¹)^β_ν δ^α_β = (ΛΛ⁻¹)^μ_ν = δ^μ_ν`
  (`test_kronecker_delta_is_invariant`).
- **Levi-Civita ε^{μνρσ}** (MA-16): invariant up to `det Λ` — `ε'^{μνρσ} =
  (det Λ)\,ε^{μνρσ}`, so it is a true invariant **tensor** only for *proper*
  Lorentz transformations (`det Λ = +1`); under a parity flip it picks up the sign
  (it is a pseudotensor / tensor density). It builds the dual `*F^{μν} =
  ½ε^{μνρσ}F_{ρσ}` in EM-18.

Symmetry type is itself a Lorentz-invariant label: a boost maps symmetric →
symmetric and antisymmetric → antisymmetric (Griffiths Prob. 12.50,
`test_symmetry_type_preserved_by_boost`). Hence the split
`T^{μν} = T^{(μν)} + T^{[μν]}` is frame-independent, and contracting the two parts
vanishes, `S_{μν}A^{μν} = 0` (`test_double_contract_sym_with_antisym_vanishes`).

## 7. Where this goes
This is the exact machinery the rest of the program runs on. **EM-18** packages
`(E,B)` into the antisymmetric field tensor `F^{μν} = ∂^μA^ν − ∂^νA^μ` and writes
all of electrodynamics as two tensor equations (`∂_μF^{μν} = μ₀J^ν`,
`∂_{[λ}F_{μν]} = 0`) — manifestly Lorentz-covariant. **RE-09** keeps every law
above but lets the metric vary, `η_{μν} → g_{μν}(x)`, replacing `∂_μ` with the
covariant derivative `∇_μ`; the index bookkeeping is unchanged, which is why a
firm grip on it here is the prerequisite for curved spacetime. (EM-18 is a
downstream application of this module, not a prerequisite for it.)
