# RE-14 — Schwarzschild solution & black holes (notes)

Conventions: geometrized units `G = c = 1` (a mass `M` is a length;
`M_⊙ = GM_⊙/c² = 1.477 km`), coordinates `(t, r, θ, φ)`, metric mostly-plus
`diag(−,+,+,+)`. The metric and its curvature invariants are RE-11's, imported
here. Write `f(r) = 1 − 2M/r` (the `lapse`).

## 1. The metric: unique static, spherically symmetric vacuum (Birkhoff)
Solving the vacuum equations `R_{μν}=0` (RE-13) for the most general static,
spherically symmetric line element forces
$$\boxed{\,ds^2 = -\Big(1-\tfrac{2M}{r}\Big)dt^2 + \Big(1-\tfrac{2M}{r}\Big)^{-1}dr^2 + r^2\,d\Omega^2\,}$$
with the single integration constant fixed by the Newtonian limit `g_{tt}→−(1+2Φ)`,
`Φ=−M/r`, to be the mass `M`. **Birkhoff's theorem** strengthens "static" to a
*derived* property: *any* spherically symmetric vacuum region is a piece of this
metric — so a pulsating or collapsing star radiates **no** monopole gravitational
waves, and the exterior is static even while the interior heaves. RE-11 verifies
the exterior is **Ricci-flat** (`test_schwarzschild_is_vacuum_solution`:
`ricci(schwarzschild_metric(1), …) ≈ 0` for `r>2M`), so all Ricci-based scalars
vanish and the curvature is *pure Weyl*. The two special radii where the metric
misbehaves, `r=2M` (`f=0`) and `r=0`, are dissected in §2.

## 2. Two singularities — coordinate vs physical
At `r=2M` the lapse `f→0` (so `g_{tt}→0`) and `g_{rr}=1/f→∞`: the metric
components blow up. At `r=0` they also blow up. These are completely different
animals, and the **coordinate-invariant** Kretschmann scalar (RE-11) tells them
apart:
$$K = R_{μνρσ}R^{μνρσ} = \frac{48\,M^2}{r^6}\qquad(\texttt{kretschmann\_formula}).$$
- **`r=2M`: a coordinate singularity.** `K(2M)=48M²/(2M)^6 = 3/(4M^4)` is
  *finite* — spacetime is perfectly regular; only the `(t,r)` chart fails (like the
  pole of a Mercator map). A freely falling observer notices nothing special as
  they cross (Kruskal/Eddington–Finkelstein coordinates make this manifest, cpope
  §10). This `r=2M` is the **event horizon** `r_S = 2M` (`horizon_radius`): a
  one-way causal boundary, not a place of infinite tidal force.
- **`r=0`: a true curvature singularity.** `K→∞`; tidal forces diverge; no
  coordinate change removes it. This is where geodesics end.

`test_kretschmann_matches_formula_and_horizon_is_finite` reproduces `48M²/r⁶` from
RE-11's Riemann tensor (to `~10⁻⁶`) and checks finiteness at `2M` against
divergence at small `r`. Inside the horizon (`r<2M`) `f<0`: `g_{tt}>0` and
`g_{rr}<0`, so `t` becomes spacelike and `r` timelike — the decrease of `r` toward
`0` becomes as inexorable as the forward march of time (`test_horizon_is_coordinate_singularity`).

## 3. Gravitational redshift (exact, then the weak field)
A static observer at `r` has 4-velocity `u^μ = (f^{-1/2},0,0,0)` and ticks at
proper rate `dτ = \sqrt{f}\,dt`: **clocks deeper in the well run slow**. A photon's
energy `E=-p_t` is conserved along `∂_t`, so the frequency a static observer
measures, `ω = -p_μu^μ = E/\sqrt{f(r)}`, gives the exact shift between emitter and
observer:
$$1+z = \frac{\omega_\text{emit}}{\omega_\text{obs}}=\sqrt{\frac{1-2M/r_\text{obs}}{1-2M/r_\text{emit}}}\qquad(\texttt{gravitational\_redshift\_factor}).$$
Two limits (`test_redshift_weak_field_limit`, `test_redshift_diverges_at_horizon`):
- **Weak field**, `r≫M`: `z ≈ M/r_\text{emit} - M/r_\text{obs} = ΔΦ/c²` — exactly
  RE-10's equivalence-principle result `gh/c²` (Pound–Rebka up the Harvard tower;
  the `~38 μs/day` GPS clock correction). The geometry has *reproduced* the EP
  prediction it was built to honour.
- **Horizon**: as `r_\text{emit}→2M`, `z→∞`. Light from just above the horizon is
  infinitely redshifted; to a distant observer an infalling emitter freezes,
  reddens, and fades — the horizon is where the redshift diverges.

## 4. Orbits from one effective potential — the GR term
In the equatorial plane the conserved energy `E=f\,\dot t` and angular momentum
`L=r²\dot φ` (per unit mass) reduce the geodesic to a 1-D problem,
$$\dot r^{\,2} = E^2 - V(r),\qquad
  \boxed{\,V(r) = \Big(1-\tfrac{2M}{r}\Big)\Big(1+\tfrac{L^2}{r^2}\Big)\,}\quad(\texttt{effective\_potential}).$$
Expanding,
$$V = \underbrace{1 - \tfrac{2M}{r} + \tfrac{L^2}{r^2}}_{\text{Newton + centrifugal}} \;\underbrace{-\,\tfrac{2ML^2}{r^3}}_{\text{purely GR}}.$$
The last term — absent from the Kepler problem of ~CM-11
(`test_effective_potential_has_the_relativistic_term`) — is the whole story.
Circular orbits are extrema, `V'(r)=0 ⇒ Mr^2 - L^2 r + 3ML^2 = 0`, with roots
$$r_\pm = \frac{L^2 \pm \sqrt{L^4 - 12M^2L^2}}{2M}\qquad(\texttt{circular\_orbit\_radius}).$$
- **ISCO `r=6M`.** Real roots require `L ≥ 2\sqrt3\,M`; at equality the stable
  minimum (`r_+`) and unstable maximum (`r_-`) **merge at `r=6M`** — the
  **innermost stable circular orbit** (`isco`). Inside it the `−2ML²/r³` term wins
  and *no* stable circular orbit exists; matter spirals in. Equivalently `r=6M`
  minimises `L^2(r)=Mr^2/(r-3M)` over circular orbits — how `isco_from_potential`
  locates it numerically (→ `6.000M`). The ISCO sets the inner edge of accretion
  discs and the radiative efficiency of black holes (Zee §VII.1, Eq. 8).
- **Photon sphere `r=3M`.** For light, `V_\gamma(r)=(1-2M/r)L^2/r^2`
  (`effective_potential_massless`) has a single **maximum at `r=3M`**, independent
  of `L` (`photon_sphere_from_potential` → `3.000M`). There light can orbit on an
  *unstable* circular null geodesic — the photon sphere — which is what gives a
  black hole its sharp "shadow." `3M < 6M`, both outside `2M`
  (`test_characteristic_radii`, `test_photon_sphere_is_maximum_of_massless_potential`).

## 5. The four classic tests
With the potential in hand, the solar-system tests are short computations
(Zee §VI.3; cpope §6.3):

1. **Perihelion precession.** A bound orbit is no longer closed: per revolution the
   perihelion advances by
   $$Δφ = \frac{6πM}{a(1-e^2)}\qquad(\texttt{perihelion\_precession}),$$
   the leading effect of the `−2ML²/r³` term. For **Mercury**
   (`a, e, M=M_⊙`) this is `≈ 43''` per century — the anomaly Einstein found
   "beside myself with joyous excitement" (`test_mercury_perihelion_precession`
   recovers `42.98''/cy` from real orbital elements). Set `M→0` and it vanishes:
   Newtonian ellipses don't precess (`test_newtonian_orbit_does_not_precess`).
2. **Deflection of light.** A ray with impact parameter `b` bends by
   $$Δφ = \frac{4M}{b}\qquad(\texttt{light\_deflection}).$$
   Grazing the **Sun** (`b=R_⊙`) this is `1.75''` (`8.49×10⁻⁶` rad), Eddington's
   1919 eclipse result (`test_solar_light_deflection`). It is **exactly twice** the
   `0.87''` the equivalence principle alone gives (RE-10): half from gravitational
   time dilation, half from the spatial curvature `g_{rr}=1/f` that the EP cannot
   see.
3. **Shapiro time delay.** A radar signal passing the Sun is *retarded*,
   $$Δt = 2M\,\ln\!\frac{(r_1+\sqrt{r_1^2-b^2})(r_2+\sqrt{r_2^2-b^2})}{b^2}\quad(\texttt{shapiro\_delay}),$$
   `~200 μs` round trip for an Earth–Venus echo grazing the Sun (Zee §VI.3 App. 2;
   `test_shapiro_delay_…`). It probes the same `g_{tt},g_{rr}` as the deflection.
4. **Gravitational redshift** — §3, the first test historically reachable in the
   lab (Pound–Rebka) and the one your phone's GPS corrects for daily.

## 6. Falling in — finite proper time, infinite coordinate time
For a radially infalling observer released from rest at `r_0`, the proper time to
reach the horizon (and on to `r=0`) is **finite** — they cross `r=2M` without
incident and hit the singularity in proper time `~ πM(r_0/2M)^{3/2}`. But the
*coordinate* time diverges:
$$\frac{dt}{dr} = -\frac{1}{f}\sqrt{\dots}\ \xrightarrow{r\to 2M}\ \infty,\qquad
  t \sim -2M\ln(r-2M)\to\infty .$$
So a distant bookkeeper using Schwarzschild `t` never sees the infall complete —
the image asymptotes to the horizon, redshifting to black (§3). Both statements are
true at once because `t` is a bad coordinate at `r=2M` (§2); the infaller's clock
is the physical one (cpope §10.2). This split — *you* fall in fine, *they* watch you
freeze forever — is the defining strangeness of a horizon, the global cousin of
RE-10's Rindler acceleration horizon, and the gateway to Hawking radiation (QF-05).
