# RE-02 — Postulates of Special Relativity (notes)

Conventions: `c = 1`, event `x = (ct, x, y, z)`, η = diag(−1,+1,+1,+1),
`β = v/c`, `γ = 1/√(1−β²)`. Frame **S′** moves at velocity `+β x̂` relative to S.
History (ether, Michelson–Morley) belongs to `RE-01`; here we take the
experimental verdict as given and extract its consequences.

## 1. The two postulates
Einstein (1905) keeps **one** principle from Galileo and adds **one** fact from
Maxwell (Griffiths §12.1.1, the two postulates stated on p.506):

1. **Principle of relativity.** The laws of physics are identical in every
   inertial frame. No experiment singles out a state of absolute rest.
2. **Universal speed of light.** The speed of light in vacuum, `c`, is the same
   for all inertial observers, *independent of the motion of source or observer*.

Postulate 1 is old (a billiard game plays the same on a smoothly moving train).
Postulate 2 is the radical one: speed is distance/time, so if everyone measures
the *same* `c` for a light beam they cannot agree about distance and time. The
price of keeping both postulates is **absolute simultaneity** — and that is the
whole of special relativity.

## 2. Why Galileo and Maxwell collide
Maxwell's equations fix the speed of an electromagnetic wave at
`c = 1/√(ε₀μ₀)` — a constant built from lab constants, with **no reference to any
frame**. Under a Galilean boost `x' = x − vt`, `t' = t`, velocities add:
`u' = u − v`. A pulse at `c` in S would travel at `c − v` in S′, so Maxwell's `c`
would hold *in only one frame* — reviving the ether and breaking postulate 1 for
electrodynamics. Zee §III.1 ("Galileo versus Maxwell") frames the dilemma
exactly this way. The Michelson–Morley null result (details in `RE-01`) says the
ether frame is undetectable. Two escapes:
- keep Galilean kinematics, patch Maxwell → killed by experiment;
- **keep Maxwell (constant `c`), fix the kinematics** → Einstein's choice, which
  forces the Lorentz transformation of `RE-03`. As `c → ∞` the conflict
  evaporates and Galileo returns (the `~CM-03` limit).

## 3. Einstein clock synchronization & the operational meaning of "constant c"
"The speed of light is constant" is empty until you say how distant clocks are
set. Einstein's **operational** definition uses light itself. To synchronize a
clock at B with one at A, send a pulse from A at time `t₁`, reflect it at B, and
read its return at A as `t₂`. *Define* B's clock so that the reflection happened at
$$t_B=\tfrac12(t_1+t_2),\qquad \text{distance } AB=\tfrac12 c\,(t_2-t_1).$$
This is the **midpoint / two-way** convention: it *assigns* equal out-and-back
light times, making the **two-way** speed of light `c` true by construction
(Griffiths §12.1.2, p.509–510). The non-trivial physical content of postulate 2
is then that the **one-way** speed also comes out `c` for *every* inertial
observer who synchronizes this way — and different observers, using the *same*
rule, end up with **different** synchronizations. That clash is §4.

## 4. The relativity of simultaneity (the immediate consequence)
Griffiths' freight car (§12.1.2, p.509): a bulb at the centre of a moving car
flashes. On the train the light hits the front and back walls **simultaneously**
(equal distances, speed `c`). On the ground the car moves into the forward beam
and away from the rear beam, so — *still using `c` both ways*, by postulate 2 —
the light reaches the **back first**. The two events are simultaneous in one frame
and not the other. Quantitatively, two events with separation `(Δt, Δx)` in S have
$$\boxed{\ \Delta t' = \gamma\,(\Delta t - \beta\,\Delta x)\ }$$
in S′ (`simultaneity_breakdown`; this is the time row of the `RE-03` boost). If
they are simultaneous in S (`Δt = 0`) then `Δt' = −γβΔx`, nonzero whenever `β≠0`
**and** `Δx≠0`. Equivalently, two clocks a rest-distance `L` apart and
synchronized **in their own frame** are seen, in a frame where they move at `β`,
to be offset by
$$\Delta t_\text{offset}=\beta L\qquad(=vL/c^2\text{ with units}),$$
the **leading clock lagging** (`leading_clocks_lag`). "Leading clocks lag" is the
slogan worth memorizing. (The two formulas reconcile via length contraction:
the rest separation `L` appears as `L/γ` in S, and `γβ·(L/γ)=βL`.)

## 5. The Bondi k-calculus (radar method)
You can build all of kinematics from a single clock and light echoes, never
assuming the Lorentz transformation. An observer assigns to a distant event the
**radar coordinates**
$$t=\tfrac12(t_\text{send}+t_\text{echo}),\qquad x=\tfrac12(t_\text{echo}-t_\text{send})$$
(`radar_coordinates`) — exactly the synchronization rule of §3. Now let A flash
signals at proper-time spacing `T`; an observer B receding at `β` receives them
spaced by `kT`, where the **Bondi factor**
$$\boxed{\ k=\sqrt{\dfrac{1+\beta}{1-\beta}}\ }$$
(`bondi_k`). `k` is purely the relativistic **Doppler** factor (`~RE-07`), and it
is its own inverse under `β→−β`: `k(β)k(−β)=1`. Two clean consequences:
- **Velocity from k:** `β = (k²−1)/(k²+1)` (`beta_from_k`).
- **Radar echoes stretch by `k²`.** A pulse A sends at `t₁`, reflected off B's
  worldline (speed `β`) and received at `t₂`, satisfies `t₂/t₁ = k²` — one factor
  of `k` outbound, one inbound. Feeding `t₁, k²t₁` into `radar_coordinates`
  reproduces `x/t = β`, tying the radar method, the Doppler factor, and velocity
  into one identity. (This is the slick, transformation-free route to time
  dilation `t_B = t₁ k /γ`-style results, expanded in `~RE-04`.)

## 6. The transverse light clock — time dilation **follows** from constant `c`
Take two mirrors a distance `D` apart, **perpendicular** to the motion; light
bouncing between them is a clock (one tick = round trip). In the clock's rest
frame a half-tick is `τ₀ = D` (`c=1`). In a frame where the clock glides at `β`,
during a half-tick `τ` the far mirror advances to `βτ`, and the light — *still at
speed `c=1`, because that is postulate 2* — must travel the **hypotenuse**:
$$\tau^2=D^2+(\beta\tau)^2\ \Longrightarrow\ (1-\beta^2)\,\tau^2=D^2\ \Longrightarrow\ \frac{\tau}{D}=\frac{1}{\sqrt{1-\beta^2}}=\gamma.$$
So the moving tick is `γ` times longer (`light_clock_gamma` builds this triangle
and solves for the ratio; it is `γ`, **not assumed**, and independent of `D`).
The lesson the module is built to deliver: **time dilation is a theorem**, the
shortest possible consequence of "the speed of light is the same for everyone."
`RE-04` makes dilation, length contraction, and the twin paradox quantitative;
`RE-03` packages all of this — boost, simultaneity, dilation — into the single
matrix Λ(β) with `ΛᵀηΛ = η`.
