# RE-01 — Problems

Work them by hand, then check with `code/galilean.py`. Sources in `../refs.md`.

### P1. Velocities that exceed light  *(conceptual; Zee III.1)*
Two particles approach each other, each at `0.7c` in the lab. What does Galilean
addition predict for their closing speed, and why is it unphysical?
*Answer:* Galilean: `1.4c` (faster than light!); the relativistic rule gives
`(0.7+0.7)/(1+0.49) = 0.94c`.
*Check:* `galilean_velocity_add(0.7,0.7)=1.4` vs `relativistic_velocity_add(0.7c,0.7c,c)/c ≈ 0.9396`.

**Solution.** Galilean addition just sums collinear speeds, so the rule assigns one
particle a speed $0.7c+0.7c=1.4c$ in the other's rest frame — a material body faster
than light, which no inertial observer can measure (it would outrun a light signal).
The correct composition law caps it:
$$w=\frac{u+v}{1+uv/c^2}=\frac{0.7c+0.7c}{1+(0.7)(0.7)}=\frac{1.4c}{1.49}=0.9396\,c<c.$$
(The lab *closing rate* of the gap may legitimately read $1.4c$ — that is a coordinate
rate, not anyone's velocity.) So `galilean_velocity_add(0.7,0.7)`$=1.4$ overshoots $c$,
while `relativistic_velocity_add(0.7c,0.7c,c)/c`$=0.9396$ stays sub-luminal.

### P2. The c→∞ limit  *(Griffiths 4e, Prob. 12.18a, p.527)*
Show that Einstein's velocity-addition rule `(u+v)/(1+uv/c²)` becomes the Galilean
`u+v` as `c→∞`, and estimate the fractional error at everyday speeds (`u=v=30 m/s`).
*Answer:* error `≈ uv(u+v)/c² ≈ 6×10⁻¹⁵ m/s` — utterly negligible.
*Check:* `galilean_limit_error(30, 30, c)` and watch it fall as `1/c²`.

**Solution.** Expand Einstein's rule for $uv/c^2\ll1$:
$$w=\frac{u+v}{1+uv/c^2}=(u+v)\Big(1-\frac{uv}{c^2}+\cdots\Big)=(u+v)-\frac{uv(u+v)}{c^2}+\cdots,$$
so $w\to u+v$ as $c\to\infty$ and the leading defect is $uv(u+v)/c^2\propto1/c^2$. At
$u=v=30$ m/s this is $\tfrac{30\cdot30\cdot60}{c^2}\approx6\times10^{-13}$ m/s on a
$60$ m/s sum (a fractional $uv/c^2\sim10^{-14}$) — utterly negligible.
`galilean_limit_error(30,30,c)` returns exactly this $6.0\times10^{-13}$, and because
the error $\propto1/c^2$ each tenfold increase in $c$ shrinks it about a hundredfold —
Galilean addition is the low-speed limit.

### P3. Why Newton never noticed  *(notes §1–2)*
Show that a Galilean boost leaves acceleration unchanged (`a'=a`) so `F=ma` is
invariant, but that the same boost gives a frame-dependent light speed `c±v`.
*Check:* `galilean_invariant_acceleration(9.81, V)` for any `V`; contrast
`light_speed_galilean(30e3, c) ≠ c`.

**Solution.** Under a constant-velocity boost $\mathbf v'=\mathbf v-\mathbf V$ with
$\mathbf V$ fixed, differentiate once more (and $t'=t$):
$$\mathbf a'=\frac{d\mathbf v'}{dt}=\frac{d\mathbf v}{dt}-\frac{d\mathbf V}{dt}=\mathbf a,$$
since $d\mathbf V/dt=0$. With $m$ unchanged, $\mathbf F=m\mathbf a$ keeps its form —
Newton is Galilean-invariant for any boost, so `galilean_invariant_acceleration(9.81, V)`$=9.81$.
But the same rule applied to light gives a frame-dependent speed $c\pm V$: met head-on,
$c+v=$ `light_speed_galilean(30e3, c)`$=299\,822\,458$ m/s $\neq c$. Newton survives the
boost; Maxwell's fixed $c$ does not — the contradiction that forces new kinematics.

### P4. The Michelson–Morley shift  *(Griffiths 4e §12.1.1, p.502)*
For arm length `L=11 m`, wavelength `λ=500 nm`, and Earth's orbital speed
`v=30 km/s`, compute the fringe shift expected on a 90° rotation.
*Answer:* `ΔN = (2L/λ)(v/c)² ≈ 0.44` fringe — easily visible, yet not seen.
*Check:* `michelson_morley_shift(30e3, 11.0, 500e-9) ≈ 0.44`; verify it scales as `(v/c)²`.

**Solution.** Riding the ether wind the two arms have unequal round-trip times, differing
to leading order by $\Delta t\approx(L/c)(v/c)^2$. A $90^\circ$ rotation swaps the fast and
slow arms, doubling the optical path difference to $2c\,\Delta t$, so the fringe count
shifts by
$$\Delta N=\frac{2c\,\Delta t}{\lambda}=\frac{2L}{\lambda}\Big(\frac{v}{c}\Big)^2.$$
With $L=11$ m, $\lambda=500$ nm and $v/c\approx1.0\times10^{-4}$: $\tfrac{2L}{\lambda}=4.4\times10^{7}$
and $(v/c)^2=1.0\times10^{-8}$, giving $\Delta N\approx0.44$ — matching
`michelson_morley_shift(30e3, 11.0, 500e-9)`$=0.44$. The $(v/c)^2$ scaling means doubling
$v$ quadruples the shift; yet the observed shift was $\sim0$.

### P5. Second-order smallness  *(notes §3)*
The ether-wind time difference is `Δt ≈ (L/c)(v/c)²`. Evaluate it for the numbers
above and confirm the fringe shift equals `2cΔt/λ`.
*Check:* `ether_wind_dt(30e3, 11.0) ≈ 3.7×10⁻¹⁶ s`, and
`2·c·ether_wind_dt(...)/λ` reproduces `michelson_morley_shift(...)`.

**Solution.** Expand the exact arm times $t_\parallel=\tfrac{2L/c}{1-\beta^2}$,
$t_\perp=\tfrac{2L/c}{\sqrt{1-\beta^2}}$ with $\beta=v/c$:
$$\Delta t=t_\parallel-t_\perp=\frac{2L}{c}\Big[(1+\beta^2+\cdots)-(1+\tfrac12\beta^2+\cdots)\Big]=\frac{L}{c}\,\beta^2+O(\beta^4).$$
For $L=11$ m and $\beta\approx1.0\times10^{-4}$, $\Delta t\approx(11/c)(1.0\times10^{-8})\approx3.7\times10^{-16}$ s,
i.e. `ether_wind_dt(30e3, 11.0)`$=3.67\times10^{-16}$. The $90^\circ$ rotation turns this
into a fringe shift $2c\,\Delta t/\lambda=0.44$, reproducing `michelson_morley_shift(...)`
and confirming $\Delta N=2c\,\Delta t/\lambda$.

### P6. The bridge to RE-03  *(conceptual)*
Argue that if `c` is the same in every frame (RE-02), the linear coordinate map
that keeps the light cone fixed cannot be Galilean — it must mix space and time.
That map is the Lorentz transformation (RE-03), of which the Galilean one here is
the `c→∞` corner.
*Answer:* No — keeping the light cone $x=\pm ct$ fixed in every frame forces the map to
mix $t$ and $x$ (you cannot hold $t'=t$); that mixing is the Lorentz transformation, with
Galilean as its $c\to\infty$ corner.

**Solution.** Homogeneity of spacetime makes the frame-to-frame map linear. If $c$ is the
same in every frame (RE-02), the two light worldlines $x=ct$ and $x=-ct$ must each map
onto themselves. A Galilean boost keeps $t'=t$ and shears only space, sending $x=ct$ to
$x'=(c-V)t$ — a *different* slope, so it tilts the light cone and fails. The only linear
maps that pin both null lines while leaving $-(ct)^2+x^2$ invariant are the hyperbolic
rotations
$$ct'=\gamma(ct-\beta x),\qquad x'=\gamma(x-\beta ct),$$
which necessarily transform time as well as space. That is the Lorentz transformation
(RE-03); letting $c\to\infty$ ($\beta\to0,\ \gamma\to1$) kills the $\beta x$ term and
returns the Galilean map — exactly the limit `galilean_limit_error`$\to0$ measured in P2.
