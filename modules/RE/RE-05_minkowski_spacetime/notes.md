# RE-05 — Minkowski Spacetime (notes)

Conventions: `c = 1`, event `x^μ = (ct, x, y, z)`, η = diag(−1,+1,+1,+1).
Greek indices run 0..3; the spatial part is written **x**.

## 1. The metric and the interval
RE-03 found that every Lorentz transformation preserves
$$s^2 = \eta_{\mu\nu}\,x^\mu x^\nu = -(ct)^2 + x^2 + y^2 + z^2 .$$
Promote this from a fact about transformations to a **geometry**: spacetime is ℝ⁴
equipped with the bilinear form η. The "length-squared" of a 4-vector and the
"angle" between two are given by the **Minkowski inner product**
`u·v = η_{μν}u^μv^ν` (`mdot`, delegated to `MA-16.inner`). The single minus sign
is the whole of special relativity; everything else is linear algebra you already
did in `MA-04`/`MA-16` with a positive-definite metric.

## 2. The light cone and the causal trichotomy
The sign of `x·x` is Lorentz-invariant, so it partitions the vectors at each
event into three frame-independent classes:
- **timelike** `s² < 0` — connectible by a sub-light worldline; inside the cone;
- **null / lightlike** `s² = 0` — the cone itself; the path of light;
- **spacelike** `s² > 0` — outside the cone; no causal contact.

For two events, `causal_relation(A,B)` asks where `B−A` lies. If timelike or null
with `Δt>0`, `B` is in `A`'s **future** (A can influence B); `Δt<0` is the
**past**; spacelike is **elsewhere**. The crucial theorem: a boost can never flip
the time-order of timelike-separated events (their `Δt` keeps its sign — proven in
`test_causal_order…`), so **cause precedes effect in every frame**. Spacelike
"order," by contrast, *is* frame-dependent — which is exactly why no signal may
travel spacelike.

## 3. Proper time — and why the inertial twin ages most
Along a timelike worldline parameterised by `λ`, the **proper time** is the
Minkowski arc length
$$\tau = \int \sqrt{-\eta_{\mu\nu}\,\frac{dx^\mu}{d\lambda}\frac{dx^\nu}{d\lambda}}\;d\lambda ,$$
the time a clock carried along that worldline actually reads (`proper_time`). The
minus sign reverses the usual triangle inequality: of all worldlines between two
timelike-separated events, the **straight (inertial) one has the longest proper
time**. Concretely, from `A=(0,0,0,0)` to `B=(10,0,0,0)`:
- inertial: `τ = √(10² ) = 10`;
- out-and-back through `x=4`: `τ = 2√(5²−4²) = 2·3 = 6`.

The travelling twin returns younger. There is no paradox: the two worldlines are
geometrically different (one is straight, one is bent), and the bent one is
*shorter* in proper time. The asymmetry is the turnaround, not anything about who
"really" moved.

## 4. Index raising and lowering with η
A contravariant vector `v^μ` has a covariant partner `v_μ = η_{μν}v^ν` (`lower`),
which here just flips the sign of the time component: `v_μ = (−v^0, v^1, v^2, v^3)`.
Raising with `η^{μν} = η_{μν}` undoes it (`raise_`). The inner product can then be
written as a plain contraction `u·v = u^μ v_μ` — the form that generalises
unchanged to curved spacetime in `RE-09`, where η becomes a position-dependent
`g_{μν}(x)`.

## 5. The standard 4-vectors and their invariants
Differentiating the worldline by **proper time** (an invariant) produces 4-vectors:
- **4-velocity** `U^μ = dx^μ/dτ = γ(1, 𝐯)`, a unit timelike vector `U·U = −1`.
- **4-momentum** `p^μ = mU^μ = (E, 𝐩)` with `E = γm`, `𝐩 = γm𝐯`. Its invariant is
  the **mass shell**
  $$p\cdot p = -m^2 \quad\Longleftrightarrow\quad E^2 = \mathbf p^2 + m^2 ,$$
  the relativistic energy–momentum relation (`invariant_mass` returns `√(−p·p)`,
  the **same number in every frame** — `test_invariant_mass_is_frame_independent`).
  Massless particles (`m=0`) ride the light cone: `p·p = 0`, `E = |𝐩|`.

These invariants are what make relativistic dynamics (`RE-06`) and relativistic
quantum mechanics (`~QM-22`, where `p·p = −m²` becomes the Klein–Gordon operator)
frame-independent statements.
