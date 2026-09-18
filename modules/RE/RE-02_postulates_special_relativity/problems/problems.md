# RE-02 — Problems

Work them by hand, then check with `code/postulates.py`. Sources in `../refs.md`.

### P1. The radar method places an event  *(Griffiths 4e, Prob. 12.5, p.510)*
You sit at the origin with a single clock. You send a radar pulse at clock-time
`t_send = 2` and receive its echo at `t_echo = 8`. Assign the reflection event a
time and a distance using only this clock. Then show that if the reflector is a
probe moving at constant `β`, the echo time is the send time stretched by exactly
`k²`.
*Answer:* `(t, x) = (5, 3)`, so `x/t = 0.6`; `k² = t_echo/t_send = 4 ⇒ k = 2 ⇒
β = (4−1)/(4+1) = 0.6`.
*Check:* `radar_coordinates(2, 8) → (5.0, 3.0)`; `bondi_k(0.6)**2 → 4.0`;
`beta_from_k(2.0) → 0.6`.

**Solution.** Light goes out and back at the same speed, so the reflection sits at the
temporal midpoint of emission and reception, a distance equal to half the round-trip
light time:
$$t=\tfrac12(t_\text{send}+t_\text{echo})=\tfrac12(2+8)=5,\qquad x=\tfrac12(t_\text{echo}-t_\text{send})=\tfrac12(8-2)=3,$$
so `radar_coordinates(2, 8)`$=(5,3)$ and $x/t=0.6$. For a probe at constant $\beta$ each
leg is Doppler-stretched by one Bondi factor $k$, hence $t_\text{echo}/t_\text{send}=k^2$.
With $\beta=0.6$, $k=\sqrt{1.6/0.4}=2$, so $k^2=4$ (`bondi_k(0.6)**2`) — the echo at
$8=4\cdot2$ — and $\beta=(k^2-1)/(k^2+1)=3/5=0.6$ (`beta_from_k(2.0)`).

### P2. Leading clocks lag  *(Griffiths 4e, §12.1.2, p.509)*
Two clocks a rest-distance `L = 3` (light-seconds) apart along the line of motion
are synchronized **in their own frame**. They fly past you at `β = 0.8`. Are they
synchronized for you? Which reads ahead, and by how much?
*Answer:* No. The front ("leading") clock lags the rear one by `βL = 0.8·3 = 2.4`
s; equivalently the rear (trailing) clock reads ahead by 2.4 s.
*Check:* `leading_clocks_lag(0.8, 3.0) → 2.4`; reversing the motion,
`leading_clocks_lag(-0.8, 3.0) → -2.4`.

**Solution.** "Synchronized in their own frame" means the two zero-settings are
simultaneous there, $\Delta t'=0$ at rest-separation $\Delta x'=L$. A clock fixed in that
frame reads, in the lab, $t'=\gamma(t-\beta x)$, so at one lab instant two clocks differ in
reading by $\Delta t'=-\gamma\beta\,\Delta x_\text{lab}$. The lab sees their separation
contracted, $\Delta x_\text{lab}=L/\gamma$, giving
$$\Delta t_\text{offset}=\gamma\beta\,(L/\gamma)=\beta L=0.8\cdot3=2.4,$$
with the front (larger $x$) clock reading *behind* — "leading clocks lag." So
`leading_clocks_lag(0.8, 3.0)`$=2.4$; reversing the motion swaps which clock leads,
`leading_clocks_lag(-0.8, 3.0)`$=-2.4$.

### P3. The freight-car simultaneity split  *(Griffiths 4e, §12.1.2(i), p.509)*
Two events are simultaneous in frame S (`Δt = 0`) and separated by `Δx = 2`. In a
frame S′ moving at `β = 0.6`, are they still simultaneous? Which happens first?
*Answer:* `Δt′ = γ(Δt − βΔx) = γ(−βΔx) = −1.25·0.6·2 = −1.5 ≠ 0`. Not
simultaneous; the event at the **larger** `x` occurs **earlier** in S′ (negative
`Δt′`).
*Check:* `simultaneity_breakdown(0.6, 0.0, 2.0) → -1.5`; and it vanishes only in
the trivial cases `simultaneity_breakdown(0.0, 0.0, 2.0) → 0` and
`simultaneity_breakdown(0.6, 0.0, 0.0) → 0`.

**Solution.** The time row of the boost gives $\Delta t'=\gamma(\Delta t-\beta\,\Delta x)$.
Simultaneous in S means $\Delta t=0$, so with $\gamma=1/\sqrt{1-0.6^2}=1/0.8=1.25$,
$$\Delta t'=-\gamma\beta\,\Delta x=-(1.25)(0.6)(2)=-1.5\neq0.$$
They are *not* simultaneous in S′. Taking $\Delta x=x_2-x_1=2>0$, the negative
$\Delta t'=t'_2-t'_1$ means the event at the **larger** $x$ happens **earlier** in S′.
This is `simultaneity_breakdown(0.6, 0.0, 2.0)`$=-1.5$, which collapses to $0$ only in the
trivial cases $\beta=0$ or $\Delta x=0$.

### P4. Time dilation **derived** from the light clock  *(Griffiths 4e, §12.1.2(ii), p.510)*
A transverse light clock has mirror gap `D = 1`. For `β = 0.6`, set up the
right-triangle path of one half-tick (legs `D` and `βτ`, hypotenuse the light
path `τ`), solve for `τ`, and read off the dilation factor `τ/D`. You must get
`γ` **without** assuming it.
*Answer:* `(1−β²)τ² = D² ⇒ τ = D/√(1−0.36) = 1.25 ⇒ γ = 1.25`.
*Check:* `light_clock_gamma(0.6) → 1.25`, equal to `1/(1-0.6**2)**0.5`, and
independent of the gap: `light_clock_gamma(0.6, 3.7)` is the same 1.25.

**Solution.** In one half-tick of lab-duration $\tau$ the clock slides horizontally by
$\beta\tau$, while the light still covers a path of length $\tau$ (speed $c=1$, postulate 2)
along the hypotenuse over the transverse gap $D$:
$$\tau^2=D^2+(\beta\tau)^2\ \Longrightarrow\ (1-\beta^2)\tau^2=D^2\ \Longrightarrow\ \frac{\tau}{D}=\frac{1}{\sqrt{1-\beta^2}}.$$
At $\beta=0.6$ this is $1/\sqrt{1-0.36}=1/0.8=1.25$, so the dilation factor is $\gamma=1.25$ —
read off the triangle, never assumed. The ratio $\tau/D$ contains no $D$, so it is
gap-independent: `light_clock_gamma(0.6)`$=1.25=1/(1-0.6^2)^{0.5}$, and
`light_clock_gamma(0.6, 3.7)` gives the same $1.25$.

### P5. The Galilean limit — Galileo vs Maxwell  *(Griffiths 4e, Prob. 12.3, p.508; Zee III.1)*
Maxwell builds a fixed `c` into electromagnetism; Galilean velocity addition would
make `c` frame-dependent. Show that the *relativistic* machinery nonetheless
reduces to Newton as `β → 0`: the Doppler factor `k → 1`, the dilation `γ → 1`,
and the simultaneity offset `→ 0` (absolute time returns). What is the fractional
error in `γ` at `β = 10⁻³`?
*Answer:* `γ − 1 ≈ ½β² = 5×10⁻⁷` and `k ≈ 1 + β`. **Time dilation and length
contraction are second order** (`β²` — which is why Michelson–Morley needed such
care), but the **relativity of simultaneity is first order**: the `−βΔx` term in
`Δt′ = γ(Δt − βΔx)` is `O(β)`. All of it vanishes as `β → 0`, returning Newton's
absolute time.
*Check:* `light_clock_gamma(1e-3) → 1.0000005` (so `γ−1 ≈ 5×10⁻⁷`);
`bondi_k(1e-3) → 1.0010005…`; the simultaneity term survives at first order —
`simultaneity_breakdown(1e-3, 2.0, 3.0) → 1.99700…`, deviating from `Δt = 2` by
exactly `βΔx = 0.003`. Kill the separation and time becomes absolute:
`simultaneity_breakdown(1e-3, 2.0, 0.0) → 2.000001 ≈ Δt` (only the `O(β²)` dilation left).

**Solution.** For small $\beta$, $\gamma=(1-\beta^2)^{-1/2}=1+\tfrac12\beta^2+\cdots$ and
$k=\sqrt{\tfrac{1+\beta}{1-\beta}}=1+\beta+\cdots$, while the simultaneity offset
$-\gamma\beta\,\Delta x=O(\beta)$. So dilation and contraction are **second order** in
$\beta$, but the relativity of simultaneity is **first order**. At $\beta=10^{-3}$,
$$\gamma-1\approx\tfrac12\beta^2=5\times10^{-7},$$
i.e. `light_clock_gamma(1e-3)`$=1.0000005$ and `bondi_k(1e-3)`$=1.0010005$. The first-order
term survives: `simultaneity_breakdown(1e-3, 2.0, 3.0)`$=1.99700$, short of $\Delta t=2$ by
exactly $\beta\,\Delta x=0.003$. Kill the separation and absolute time returns,
`simultaneity_breakdown(1e-3, 2.0, 0.0)`$=2.000001\approx\Delta t$ (only the $O(\beta^2)$
dilation remaining).

### P6. Seen vs observed  *(Griffiths 4e, Prob. 12.6, p.510; conceptual)*
A star moving at `v` at angle `θ` to the line of sight can *appear* to cross the
sky faster than light. Explain why this is not a violation: the *raw reception
time* (what you **see**) is not the event's coordinate time (what you **observe**)
— they differ by the light-travel time, which is exactly what Einstein
synchronization / the radar method removes.
*Check (the principle):* `radar_coordinates(t_send, t_echo)` returns the
**observed** `(t, x)` after subtracting light travel; the bare `t_echo` is only
what the clock **sees**. Place an event at `(t, x) = (5, 3)` via `t_send = t − x`,
`t_echo = t + x`: you *see* the echo at `t_echo = 8`, but *observe* the event at
`t = 5`. This separation of "seen" from "observed" is the whole point of §12.1.2.

**Solution.** What you *see* is the photon's arrival time; what you *observe* (assign as the
event's coordinate time) is that arrival minus the light-travel delay. For a source
approaching at angle $\theta$, photons emitted later leave from nearer points, so their
arrivals bunch up and the *apparent* transverse speed $\dfrac{v\sin\theta}{1-\beta\cos\theta}$
can exceed $c$ — but only the raw reception rate is superluminal, not the source. Einstein
synchronization removes exactly this delay through the radar assignment
$$t=\tfrac12(t_\text{send}+t_\text{echo}),\qquad x=\tfrac12(t_\text{echo}-t_\text{send}).$$
Placing an event at $(t,x)=(5,3)$ via $t_\text{send}=t-x=2$, $t_\text{echo}=t+x=8$: you
*see* the echo at $t_\text{echo}=8$ but *observe* the event at `radar_coordinates(2, 8)`$=(5,3)$ —
the seen/observed split of §12.1.2, with no real faster-than-light motion.
