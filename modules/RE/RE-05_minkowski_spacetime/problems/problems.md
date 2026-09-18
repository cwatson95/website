# RE-05 — Problems

Work them by hand, then check with `code/minkowski.py`. Sources in `../refs.md`.

### P1. Classify the separations  *(Griffiths 4e, Prob. 12.20, p.529)*
For events A = (0,0,0,0) and B = (ct, x, 0, 0), decide timelike/null/spacelike for
(a) ct=5, x=3; (b) ct=3, x=5; (c) ct=4, x=4.
*Answers:* (a) timelike (s²=−16), (b) spacelike (s²=+16), (c) null.
*Check:* `classify([5,3,0,0])`, `classify([3,5,0,0])`, `classify([4,4,0,0])`.

**Solution.** With $A$ at the origin, $B-A=(ct,x,0,0)$ and the invariant interval is
$$s^2=\eta_{\mu\nu}\,\Delta x^\mu\Delta x^\nu=-(ct)^2+x^2 .$$
(a) $s^2=-5^2+3^2=-16<0$ — time wins, **timelike**: a sub-light worldline links the
events. (b) $s^2=-3^2+5^2=+16>0$ — space wins, **spacelike**: no causal contact.
(c) $s^2=-4^2+4^2=0$ — **null**, joined only by light. Because $s^2$ is
Lorentz-invariant these labels hold in every frame, matching `classify([5,3,0,0])`→`timelike`,
`classify([3,5,0,0])`→`spacelike`, `classify([4,4,0,0])`→`null`.

### P2. Cause precedes effect  *(conceptual; Zee III.3)*
Show that if B is in A's future light cone, no Lorentz boost can make `Δt' < 0`.
Then show that for a *spacelike* separation a boost CAN reverse the time order.
*Check:* `test_causal_order_is_frame_invariant_for_timelike` does exactly this with
random boosts.

**Solution.** A boost along $x$ transforms the time gap as $\Delta t'=\gamma(\Delta t-\beta\,\Delta x)$
with $|\beta|<1$. If $B$ is in $A$'s future the separation is timelike with $\Delta t>0$
and $|\Delta x|<\Delta t$, so
$$\Delta t'=\gamma(\Delta t-\beta\,\Delta x)\ \ge\ \gamma\big(\Delta t-|\beta|\,|\Delta x|\big)\ >\ \gamma\big(\Delta t-|\Delta x|\big)\ >\ 0 .$$
Thus $\Delta t'>0$ in **every** frame — cause precedes effect, always (the null boundary
$|\Delta x|=\Delta t$ gives $\Delta t'=\gamma\Delta t(1\mp\beta)>0$ too). For a **spacelike**
pair $|\Delta x|>|\Delta t|$, so any boost with $\Delta t/\Delta x<\beta<1$ makes
$\Delta t-\beta\,\Delta x<0$ and reverses the order — exactly why no signal may travel
spacelike. `test_causal_order_is_frame_invariant_for_timelike` shows both: the timelike $B$
keeps ${B'}^0>0$ under random boosts, while a spacelike event's $\Delta t$ flips.

### P3. The invariant of the 4-velocity  *(Griffiths 4e, Prob. 12.26, p.535)*
Compute `U·U` for `U = γ(1, 𝐯)`. Show it equals `−1` (i.e. `−c²` with units),
independent of **v**.
*Check:* `mdot(four_velocity([0.6,0.2,0.0]), four_velocity([0.6,0.2,0.0]))` → −1.

**Solution.** With $U^\mu=\gamma(1,\mathbf v)$ and $\eta=\mathrm{diag}(-1,+1,+1,+1)$,
$$U\cdot U=-\gamma^2(1)^2+\gamma^2|\mathbf v|^2=-\gamma^2\big(1-|\mathbf v|^2\big).$$
But $\gamma=1/\sqrt{1-|\mathbf v|^2}$ gives $\gamma^2(1-|\mathbf v|^2)=1$ identically, so
$U\cdot U=-1$ (i.e. $-c^2$ in units with $c$) for **any** $\mathbf v$. The 4-velocity is a
unit timelike vector by construction — differentiating $x^\mu$ by the invariant $\tau$
guarantees it. For $\mathbf v=(0.6,0.2,0)$ ($\gamma\approx1.291$) this is
`mdot(four_velocity([0.6,0.2,0.0]), four_velocity([0.6,0.2,0.0]))`→$-1$, independent of speed.

### P4. The mass shell  *(Griffiths 4e, §12.2.2, p.535)*
A particle has mass m=2 and speed 0.6c along x. Find E and **p**, and verify
`E² − |𝐩|² = m²`.
*Answer:* γ=1.25, E=2.5, p_x=1.5; `2.5² − 1.5² = 6.25 − 2.25 = 4 = 2²`.
*Check:* `four_momentum(2.0, [0.6,0,0])` → `[2.5, 1.5, 0, 0]`; `invariant_mass` → 2.0.

**Solution.** At $\beta=0.6$, $\gamma=1/\sqrt{1-0.36}=1/0.8=1.25$. The 4-momentum is
$p^\mu=mU^\mu=(\gamma m,\ \gamma m\mathbf v)$, so
$$E=\gamma m=1.25\cdot2=2.5,\qquad p_x=\gamma m v=1.25\cdot2\cdot0.6=1.5 .$$
The mass shell then follows from $U\cdot U=-1$ (P3): $p\cdot p=m^2(U\cdot U)=-m^2$, i.e.
$$E^2-|\mathbf p|^2=2.5^2-1.5^2=6.25-2.25=4=2^2=m^2 .$$
So $\sqrt{-p\cdot p}=2$ in every frame, reproducing
`four_momentum(2.0, [0.6,0,0])`→`[2.5, 1.5, 0, 0]` and `invariant_mass`→`2.0`.

### P5. The twin paradox is a triangle inequality  *(Zee III.3; conceptual)*
Twin A stays at rest from `(0,0,0,0)` to `(10,0,0,0)`. Twin B flies out to
`(5, x, 0, 0)` and back. Show B's proper time `2√(25 − x²)` is always less than
A's `10`, and find the `x` that makes B return at half A's age.
*Answer:* `2√(25−x²) = 5 ⇒ x = √(75)/2 ≈ 4.33` (β = x/5 ≈ 0.866, γ = 2).
*Check:* `proper_time([[0,0,0,0],[5,4.33,0,0],[10,0,0,0]])` ≈ 5.0.

**Solution.** Each leg of B's trip spans coordinate time $\Delta t=5$ and displacement
$\Delta x=x$, so its proper time is the Minkowski arc length
$\sqrt{(\Delta t)^2-(\Delta x)^2}=\sqrt{25-x^2}$. The two symmetric legs give
$$\tau_B=2\sqrt{25-x^2}\ \le\ 2\sqrt{25}=10=\tau_A ,$$
with equality only at $x=0$: the **bent** worldline is always shorter (the reversed triangle
inequality), so the travelling twin returns younger. Setting $\tau_B=\tfrac12\tau_A=5$ gives
$\sqrt{25-x^2}=2.5\Rightarrow x^2=18.75\Rightarrow x=\sqrt{75}/2\approx4.33$ (so
$\beta=x/5\approx0.866$, $\gamma=2$). Then
`proper_time([[0,0,0,0],[5,4.33,0,0],[10,0,0,0]])`$\approx5.0$, half of A's $10$.

### P6. Maximal aging  *(conceptual; bridge to RE-12)*
Argue from the reversed triangle inequality that a free (inertial) particle
follows the worldline of **maximal proper time** between two events. This
"principle of maximal aging" is the seed of the geodesic principle in `RE-12`.
*Check:* any bent worldline you feed `proper_time` returns less than the straight one.

**Solution.** Take any timelike worldline from $A$ to $B$ and insert an intermediate event
$C$ off the straight line. The reversed triangle inequality (P5), applied leg by leg, gives
$$\tau_{A\to C}+\tau_{C\to B}\ \le\ \tau_{A\to B},$$
with equality only when $C$ lies on the straight worldline — every kink (an acceleration)
strictly *shortens* the elapsed proper time. Iterating over all detours, the **inertial**
path is the unique maximum of $\tau=\int d\tau$. This is the principle of *maximal aging*:
a free particle extremizes its proper time, the seed of the geodesic principle in `RE-12`.
Concretely, any bent worldline handed to `proper_time` returns less than the straight
$A\to B$ value of $10$.
