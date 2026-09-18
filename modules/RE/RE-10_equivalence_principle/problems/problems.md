# RE-10 — Problems

Work them by hand, then check with `code/equivalence_principle.py`. Sources in
`../refs.md`. SI units throughout (`c, g, G` explicit — see the module note).

### P1. The Pound–Rebka shift  *(Zee §V.2, p.280/PDF 303)*
A 14.4 keV γ-ray climbs the `h = 22.5 m` Jefferson tower. Using only the
equivalence principle, predict the fractional frequency shift `Δf/f = −gh/c²` and
its sign. Why is the result negative ("red")?
*Answer:* `−9.80665·22.5/(2.998×10⁸)² = −2.45×10⁻¹⁵`; negative because the photon
climbs *out*, spending energy against the (effective) field.
*Check:* `pound_rebka()` → `2.455e-15`; `redshift_uniform_field(9.80665, 22.5)` →
`-2.455e-15`.

**Solution.** By the equivalence principle the climbing photon is equivalent to one received by an observer accelerating upward at $g$; in the flight time $t=h/c$ the receiver gains speed $v=gt=gh/c$ away from the source, so the first-order Doppler shift is
$$\frac{\Delta f}{f}=-\frac{v}{c}=-\frac{gh}{c^2}.$$
With $g=9.80665\ \text{m/s}^2$ and $h=22.5\ \text{m}$, $\Delta f/f=-9.80665\cdot22.5/(2.998\times10^8)^2=-2.45\times10^{-15}$. It is negative - a redshift - because the photon climbs *out*, spending energy against the effective field and dropping in frequency. This matches `pound_rebka()` $=2.455\times10^{-15}$ (magnitude) and `redshift_uniform_field(9.80665, 22.5)` $=-2.455\times10^{-15}$.

### P2. The equivalence, made numerical  *(Zee §V.2; the central claim)*
A rocket accelerates at `a = g`. Show that the floor→ceiling redshift over height
`h` equals the redshift of a photon rising `h` in a uniform field `g` — i.e. no
experiment in the sealed cabin distinguishes the two.
*Check:* for any `a, h`, `accelerated_frame_redshift(a, h)` ==
`redshift_uniform_field(a, h)` (`test_equivalence_accelerated_equals_field`).

**Solution.** In the rocket, light emitted at the floor reaches the ceiling height $h$ after $t=h/c$; in that interval the ceiling has gained speed $v=at=ah/c$ away from the emission event, so the Doppler shift is $\Delta f/f=-v/c=-ah/c^2$ - this is `accelerated_frame_redshift(a,h)`. A photon rising $h$ in a uniform field $g$ climbs a potential $\Delta\Phi=gh$, giving $\Delta f/f=-\Delta\Phi/c^2=-gh/c^2$ - this is `redshift_uniform_field(g,h)`. Setting $g=a$,
$$\left.\frac{\Delta f}{f}\right|_{\text{rocket}}=-\frac{ah}{c^2}=-\frac{gh}{c^2}=\left.\frac{\Delta f}{f}\right|_{\text{field}}.$$
The two are numerically identical for *every* $a,h$, so no measurement of the photon shift inside the sealed cabin can distinguish acceleration $a$ from a field $g=a$ - the equivalence principle. Confirmed by `accelerated_frame_redshift(a, h)` $==$ `redshift_uniform_field(a, h)` (`test_equivalence_accelerated_equals_field`).

### P3. Redshift **is** time dilation  *(notes §3; conceptual)*
A clock sits at potential `Φ_lower`, another at `Φ_upper > Φ_lower`. Show that the
fractional rate by which the lower clock falls behind equals the redshift of a
photon sent from the lower to the upper clock.
*Answer:* both equal `−(Φ_upper−Φ_lower)/c²`.
*Check:* `grav_time_dilation(Φ_lo, Φ_up) − 1` == `grav_redshift(Φ_up − Φ_lo)`
(`test_redshift_timedilation_consistency`). Apply it to GPS: ground clocks run slow,
so the satellite clock gains time.

**Solution.** An ideal clock at potential $\Phi$ ticks at proper rate $d\tau/dt\approx1+\Phi/c^2$ (weak field). The fractional amount by which the lower clock falls behind the upper one is then
$$\frac{d\tau_{\text{lower}}}{d\tau_{\text{upper}}}-1\approx\Big(1+\frac{\Phi_{\text{lower}}}{c^2}\Big)-\Big(1+\frac{\Phi_{\text{upper}}}{c^2}\Big)=-\frac{\Phi_{\text{upper}}-\Phi_{\text{lower}}}{c^2}.$$
A photon sent from the lower to the upper clock climbs $\Delta\Phi=\Phi_{\text{upper}}-\Phi_{\text{lower}}>0$, so its redshift is $\Delta f/f=-\Delta\Phi/c^2$ - the same number. Redshift and time dilation are one phenomenon: the light looks reddened only because the deeper clock genuinely runs slow. Confirmed: `grav_time_dilation(phi_lo, phi_up) - 1` $==$ `grav_redshift(phi_up - phi_lo)`. For GPS the ground clock (lower $\Phi$) runs slow, so the orbiting clock gains time.

### P4. Bending light, and the missing factor of two  *(Zee §V.2, p.280; notes §4)*
Light crosses an elevator of width `L` accelerating at `g`. Find the transverse
drop and deflection angle. Then explain why this EP estimate is only **half** the
measured deflection of starlight grazing the Sun.
*Answer:* `drop = ½g(L/c)²`, `θ = gL/c²`; the EP fixes only the *time* part of the
metric, and the equal *space*-curvature contribution (RE-11) doubles it
(0.87″ → 1.75″).
*Check:* `light_deflection_elevator(g, L)` → `(drop, angle)` with `drop = ½·L·angle`.

**Solution.** A ray crossing the width $L$ takes $t=L/c$; in that time the floor accelerates up by the transverse drop, and the exit angle is the transverse speed over $c$:
$$\text{drop}=\tfrac12 g\,t^2=\tfrac12 g\Big(\frac{L}{c}\Big)^2,\qquad \theta\approx\frac{g\,t}{c}=\frac{gL}{c^2},$$
so $\text{drop}=\tfrac12 L\theta$. By the equivalence principle light must bend the same way in a real field $g$. But this argument curves only the *time* part of the metric; the equal contribution from *spatial* curvature (RE-11), invisible to the EP, doubles the result - turning Einstein's 1911 figure $0.87''$ into the measured $1.75''$ for starlight grazing the Sun. Confirmed: `light_deflection_elevator(g, L)` returns `(drop, angle)` with $\text{drop}=\tfrac12 L\cdot\text{angle}$ (demo: $5.46\times10^{-15}\ \text{m}$ and $1.09\times10^{-15}\ \text{rad}$).

### P5. The 1-g horizon  *(notes §5; seeds RE-14, QF-05)*
An observer holds constant proper acceleration `a`. How far behind them is the
Rindler horizon? Evaluate for `a = g` and convert to light-years. What happens as
`a → 0`?
*Answer:* `d = c²/a`; for `a = g`, `d = 9.17×10¹⁵ m ≈ 0.97 ly`; `d → ∞` as `a → 0`
(an inertial observer has no horizon).
*Check:* `rindler_horizon(9.80665)` → `9.165e15`; `rindler_horizon(0.0)` → `inf`;
`rindler_horizon(a)*a == c²`.

**Solution.** An observer with constant proper acceleration $a$ traces the hyperbola $x^2-(ct)^2=(c^2/a)^2$. A light pulse starting a distance $d$ directly behind can keep pace only out to the break-even separation
$$d=\frac{c^2}{a}.$$
For $a=g=9.80665\ \text{m/s}^2$, $d=(2.998\times10^8)^2/9.80665=9.17\times10^{15}\ \text{m}$, and dividing by $9.461\times10^{15}\ \text{m}$ per light-year gives $0.97$ light-years. As $a\to0$, $d\to\infty$ - an inertial observer accelerates not at all and has no horizon. Confirmed: `rindler_horizon(9.80665)` $=9.165\times10^{15}$, `rindler_horizon(0.0)` $=$ `inf`, and `rindler_horizon(a)*a` $=c^2$.

### P6. What free fall cannot remove  *(C. Pope notes, PDF 10; notes §6)*
Two test masses hang `dr` apart, one directly above the other, and are released to
fall toward a mass `M` at distance `r`. Free fall cancels the local `GM/r²` for
*each* mass — yet they don't stay a fixed distance apart. Find their relative
("tidal") acceleration and show it survives the free-fall transformation.
*Answer:* `a_tidal = 2GM·dr/r³` (a radial stretch); it `→0` as `dr→0` but is nonzero
for any finite `dr` and depends on no choice of frame — it is curvature.
*Check:* `tidal_acceleration(M, r, dr)` scales as `1/r³` and `∝ dr`;
`tidal_acceleration(M, r, 0) == 0` while the local field `GM/r²` it removes is
millions of times larger (`test_tidal_curvature_is_irreducible`).

**Solution.** The local field at radius $r$ is $g(r)=GM/r^2$, stronger on the near mass than the far one. After free fall cancels the common $GM/r^2$, the residual *relative* acceleration is the field gradient times the separation:
$$a_{\text{tidal}}=\Big|\frac{d}{dr}\frac{GM}{r^2}\Big|\,dr=\frac{2GM}{r^3}\,dr,$$
a stretch along $r$. It $\to0$ as $dr\to0$ (so a single point can be made locally inertial) but is nonzero for any finite $dr$, scales as $1/r^3$, and depends on no choice of frame - it is curvature (geodesic deviation, RE-11). For Earth, two masses $1\ \text{m}$ apart give $a_{\text{tidal}}\approx3.1\times10^{-6}\ \text{m/s}^2$, while the local $GM/r^2\approx9.8\ \text{m/s}^2$ that free fall removes is millions of times larger. Confirmed: `tidal_acceleration(M, r, dr)` scales as $1/r^3$ and $\propto dr$, with `tidal_acceleration(M, r, 0)` $=0$.

### P7. The universality of free fall  *(Will Ch. 2, Eötvös ratio, p.25/PDF 42)*
Two bodies fall with accelerations `a₁, a₂`. Define the Eötvös ratio and state what
the weak EP requires of it. If a torsion balance bounds `η < 10⁻¹³`, what does that
say about composition-dependent forces?
*Answer:* `η = 2|a₁−a₂|/(a₁+a₂)`; the WEP demands `η = 0` for all material pairs;
`η < 10⁻¹³` means any "fifth force" coupling to composition is excluded at that
level (Will Table 2.2, PDF 44).
*Check:* `eotvos_parameter(a, a)` → `0.0`; `eotvos_parameter(1.0, 1.0+1e-13)` →
`1.0e-13`.

**Solution.** The Eotvos ratio compares the fall rates of two bodies,
$$\eta=\frac{2\,|a_1-a_2|}{a_1+a_2}.$$
If gravitational and inertial mass coincide then $a=(m_{\text{grav}}/m_{\text{inert}})\,g$ is identical for every body, so the weak equivalence principle demands $\eta=0$ for *all* material pairs. A torsion-balance bound $\eta<10^{-13}$ therefore says any composition-dependent "fifth force" must be weaker than gravity by at least that factor - excluded at the $10^{-13}$ level (Will Table 2.2). Confirmed: `eotvos_parameter(a, a)` $=0.0$ and `eotvos_parameter(1.0, 1.0+1e-13)` $\approx1.0\times10^{-13}$.
