# RE-04 — Time Dilation, Length Contraction & Simultaneity (notes)

Conventions: `c = 1`, event `x = (ct, x, y, z)`, η = diag(−1,+1,+1,+1),
`β = v/c`, `γ = 1/√(1−β²)`. Frame **S′** moves at `+β x̂` relative to S, so the
boost (RE-03) is
$$ct' = \gamma(ct-\beta x),\qquad x' = \gamma(x-\beta ct),\qquad y'=y,\ z'=z,$$
with inverse obtained by `β → −β`. Everything below is this one map applied to a
*pair of events*; the only subtlety is **which two events you choose**.

## 1. Proper time and time dilation
The **proper time** `τ` of a clock is the time it reads along its own worldline —
the time between two events that happen at the *same place in the clock's frame*
(`Δx' = 0`). Put the two ticks at `(ct',x') = (0,0)` and `(Δτ,0)` and carry them to
S with the inverse boost `ct = γ(ct' + βx')`:
$$\boxed{\ \Delta t = \gamma\,\Delta\tau\ }\qquad(\Delta t \ge \Delta\tau).$$
A moving clock's ticks are spread out in coordinate time by γ: **moving clocks run
slow** (Griffiths §12.1.2, "Time Dilation"). Read the other way, a clock that
moves for coordinate time `Δt` logs only `Δτ = Δt/γ` of proper time
(`proper_time`). The effect is **reciprocal** — each inertial observer finds the
*other's* clock slow — and there is no contradiction, because the two judgements
compare *different pairs of events* (this is the seed of the twin "paradox," §6).
For small β, `γ ≈ 1 + ½β²`, so `Δt − Δτ = O(β²)` and Newton is recovered.

## 2. Length contraction and how it is *measured*
The **rest (proper) length** `L₀` of a rod is its length in its own frame. To
measure a *moving* rod you must mark **both ends at the same instant of your
frame** (`Δt = 0`) — otherwise the rod moves between the markings and the answer
is meaningless. Take the ends' worldlines `x' = 0` and `x' = L₀`; demand `ct = 0`
in S and solve `x' = γ(x − βct)` for the S-positions: `x = 0` and `x = L₀/γ`. Hence
$$\boxed{\ L = \dfrac{L_0}{\gamma}\ }\qquad(L \le L_0).$$
The moving rod is **shorter** by 1/γ (Griffiths §12.1.2, "Lorentz Contraction").
Only the dimension **along the motion** contracts; **transverse** lengths are
unchanged (a transverse boost mixes no `t`, and a symmetry argument — two identical
rings threaded as they pass would jam if either shrank — forbids transverse
change). Length contraction is *the same γ* as time dilation: indeed
`L · Δt = L₀ · Δτ` for unit proper quantities, the cleanest statement that the two
are one effect. Like dilation it is reciprocal, and for the *same operational
reason* — the two observers mark the ends at instants they each call "simultaneous,"
and they disagree about that (§3).

## 3. The relativity of simultaneity (leading clocks lag)
Take two clocks at rest in S′, a rest-distance `L₀` apart, **synchronised in S′**
(both read `t' = 0`). What do they read at one instant of S? Their reading *is*
`t'`, and from `t' = γ(t − βx)` evaluated at fixed `t`,
$$\Delta t' = -\gamma\beta\,\Delta x = -\beta L_0$$
(using `Δx = L₀/γ`, the contracted S-separation). The clock in front — the
**leading** clock, in the direction of motion — reads `βL₀` *less*:
$$\boxed{\ \text{leading clocks lag by } \beta L_0\ }$$
(`leading_clocks_lag`). Simultaneity is **frame-dependent**: "now" is a different
slice of spacetime for S and S′. This `βx` cross-term is the part of the boost with
no Newtonian counterpart, and it is the true engine of special relativity — §§5–6
are all simultaneity in disguise.

## 4. One boost, three readings
Sections 1–3 are the **same** transformation, distinguished only by which
coordinate is held fixed across the two events:

| hold fixed | events | result | name |
|---|---|---|---|
| `Δx' = 0` (one clock) | two ticks | `Δt = γΔτ` | time dilation |
| `Δt = 0` (one instant) | two rod-ends | `L = L₀/γ` | length contraction |
| `Δt = 0` (one instant) | two synced clocks | `Δt' = −βL₀` | simultaneity |

So time dilation and length contraction share γ, and contraction and simultaneity
share the `Δt = 0` slice that the two frames disagree about. `boosted_axes` (§7)
draws all three at once.

## 5. Muon decay — the canonical confirmation
Cosmic-ray muons are created high in the atmosphere with mean rest-frame lifetime
`τ₀ ≈ 2.2 μs`. Travelling a height `d` at speed β, Newton predicts a survival
fraction `exp(−d/(βτ₀))` — for `d ≈ 33` light-μs (~10 km) at `β = 0.98` that is
`~2×10⁻⁷`, essentially **none** should reach the ground. Relativity time-dilates
the muon's clock to lab-lifetime `γτ₀`, giving
$$\frac{N}{N_0}\Big|_{\text{rel}}=\exp\!\Big(\!-\frac{d}{\gamma\beta\tau_0}\Big)\;>\;\exp\!\Big(\!-\frac{d}{\beta\tau_0}\Big)\Big|_{\text{naive}},$$
about `5%` — and `~5%` is what is observed (Rossi–Hall 1941; Griffiths Ex. 12.1).
`muon_fraction` returns the pair `(relativistic, naive)`; the ratio is `~10⁵`. In
the **muon's** frame nothing is dilated — instead the atmosphere is *length-
contracted* to `d/γ`, and the same `5%` survive. The two descriptions are §§1–2 of
one boost.

## 6. The "paradoxes" resolved
**Pole-in-barn (barn-and-ladder).** A pole of rest length `L₀` runs at β through a
barn of length `L_barn < L₀`. In the **barn** frame the pole is contracted to
`L₀/γ`; if `L₀/γ ≤ L_barn` it momentarily fits, and **both doors shut
simultaneously** with the pole inside. In the **pole** frame the *barn* is
contracted to `L_barn/γ < L₀`, so the pole never fits — and indeed the two
door-shuts are **not simultaneous** (`door_gap_pole = γβL_barn`): the far door
shuts and reopens to let the front out *before* the near door shuts behind the
back. No contradiction: the frames agree on every local event and disagree only on
*simultaneity* (Griffiths Ex. 12.3; `pole_in_barn`).

**Twin paradox.** One twin flies out at β and back; the other stays home. The
traveller returns **younger**, ageing `T_home/γ` against the home twin's `T_home`
(`twin_ages`). The naive "but each sees the other's clock slow, so it's symmetric"
fails because the situation is **not** symmetric: only the traveller **changes
inertial frame** at the turnaround. At that instant her line of simultaneity swings
across the home twin's worldline, and the home twin "ages suddenly" by exactly the
`βL₀`-type simultaneity jump — accounting for the whole difference (Griffiths
Ex. 12.2 / Prob. 12.16). The asymmetry, and the age gap, vanish only as `β → 0`.

## 7. Minkowski spacetime diagrams
Draw `ct` vertical, `x` horizontal; a particle traces a **worldline**, light moves
on the `±45°` lines `ct = ±x`. The axes of S′ are drawn *in* S's diagram:
- the **ct′-axis** is the worldline of `x' = 0`, the line `x = βct` — direction
  `(ct,x) = (1,β)`, **slope `1/β`**;
- the **x′-axis** is the locus S′ calls simultaneous, `ct' = 0` ⟹ `ct = βx` —
  direction `(β,1)`, **slope `β`**.

Both axes **scissor toward the light line** `ct = x` through the *same* angle
`arctan β` (their slopes `1/β` and `β` are reciprocals, i.e. mirror images about the
light line). `boosted_axes` returns the two directions. The picture makes the trunk
visual: time dilation is the differing tick-spacing along the two time axes, length
contraction the differing rod-projection along the two space axes, and simultaneity
the tilt of the x′-axis off the x-axis — the three effects of §4 in one figure
(Zee §III.4). The hyperbola `s² = ηₘₙxᵐxⁿ = const` calibrates both sets of axes and
is the bridge to RE-05.
