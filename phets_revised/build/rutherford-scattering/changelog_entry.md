## 2026-09-22 — rutherford-scattering: PhET's Rutherford Scattering remade, with the closed form beside every trajectory

### Added
`docs/phets_revised/rutherford-scattering.html` (215 KB, 4 078 lines) — a
clean-room remake of PhET Interactive Simulations' **Rutherford Scattering**
(University of Colorado Boulder, CC-BY 4.0), built against its minified build
**1.1.29** in `docs/phets/`. New code; no PhET code or assets. Both of PhET's
screens (Rutherford Atom, Plum Pudding Atom) and both of the Rutherford
screen's scenes (the zoomed-out atomic view and the zoomed-in nuclear view),
its gun, its Energy / Protons / Neutrons sliders, its Traces checkbox and its
legend.

Six views: **the nucleus** (PhET's nuclear-scale scene), **the foil** (its
atomic-scale scene, five atoms), **plum pudding** (its second screen, with the
number that killed the model on a logarithmic axis beside it), **the
hyperbola** (the closed form with an RK4 integration of Newton's equations laid
over it), **the cross section** (1/sin⁴(θ/2) three independent ways) and
**gold, for real** (PhET's scaled numbers against the real ones).

**What is exact.** The whole Coulomb problem. Every drawn particle is on the
exact hyperbola `r(φ) = b²/[b sinφ + (D/2)(cosφ − 1)]` at every step — only its
timing along the conic is integrated (RK4 on `dφ/dt = v∞ b/r²`, fourth order,
measured: 1.65e-4 → 6.6e-7 → 2.6e-9 for 15 / 60 / 240 steps). From it:
`tan(θ/2) = D/2b`, `r_min = D/2 + √(D²/4 + b²)`, the asymptote offsets, the
eccentricity `1/sin(θ/2)`, and `dσ/dΩ = (D/4)²/sin⁴(θ/2)` obtained as the
Jacobian `(b/sinθ)|db/dθ|` rather than quoted. Checked against `scipy`
independently: the deflection integral `θ = π − 2b∫dr/(r²√(1 − U/E − b²/r²))`
reproduces `2 atan(D/2b)` to 2e-11; `solve_ivp` on the equations of motion
conserves energy to 8e-13 and angular momentum to 2e-13 and reaches the same
deflection, with a residual of **1.505/r_final²** — a truncation whose rate is
measured at three distances, not waved at. The head-on case `b = 0` is exact
too (`r_min = D`, `θ = π`), and the radial motion has the closed parametric
solution `r = (D/2)(cosh η + 1)`, `t = (D/2)(sinh η + η)`, which satisfies
`v² = 1 − D/r` identically. The seeded beam is a `mulberry32` reproduced bit
for bit in Python — the JS and Python samples are the *same* sample, so the
binned cross section is asserted against derive.py's counts exactly and against
the exact solid-angle average to **the model's own 1/√N**, a tolerance taken
from the sampling law and not chosen.

Thomson's atom is a uniform ball of `+Ze` of radius `R` with the electron
charge on its surface, so the atom is neutral outside and the field inside is
the ball's alone: `θ(b) = D b √(R² − b²)/R³`, `θ_max = D/2R` at `b = R/√2`,
`⟨θ²⟩ = D²/6R²`. The impulse form is checked against the full deflection
integral and its error is shown to be a real O(θ) departure (0.082 % → 0.041 %
→ 0.020 % as D halves), not zero. Electrons are not deflectors: a free electron
can turn an alpha by at most `asin(m_e/m_α) = 1.371e-4 rad`.

**PhET's values, read out of the minified original** and labelled PhET's
throughout: `RSConstants` (energy 50–100 default 80, protons 20–100 default 79,
neutrons 20–150 default 118, traces off, `SPACE_NODE_WIDTH` 510),
`RSBaseModel` (bounds ±127.5), `RutherfordAtomSpace` (five atoms of width 30 at
±n/2, ±n and −n/2 with n = 127.5), `RutherfordNucleusSpace` (one atom whose box
is the whole bounds), `RutherfordAtom.moveParticle`
(`D = (L/8)(protons/79)(80/energy)²`), `Gun.step` (one particle every
`width/energy/20` s, a uniformly random x, nudged away from any atom centre it
comes within 4 % of the bounds width of), and both scale captions
(6.0×10⁻¹⁰ m atomic, 1.5×10⁻¹³ m nuclear). The element names on the proton
slider are PhET's own SHRED strings, emitted from `inventory.json` by
`gen_elements.py` — not one was typed. Writing PhET's D as `2α/s₀²` makes the
Coulomb strength `α = 400 L (Z/79)` independent of the gun setting, as it must
be, and both spellings are asserted equal over the whole slider space.

**The scale distortions are printed on the canvas**, as the house rule
requires: PhET's two captions are 4000× apart while its two scenes are only
8.5× apart geometrically, and a real gold atom is **20 623** nuclear diameters
across; at PhET's own nuclear-scale caption a real gold nucleus would be 9.3 %
of the frame and D 19.7 %, against the drawn 12.5 %.

Verification: `derive.py` (scipy.constants CODATA 2022, `quad`, `solve_ivp`,
`brentq`, `minimize_scalar`, a bit-for-bit Python `mulberry32`) prints 401
reference values into `refvals.txt`, which `make_refs.py` emits into
`p7_refs.js`; **973 selfTest assertions, 0 failed**; **234 UI-drive assertions,
0 failed**; **104 mutants, 104 caught, 0 survived**; the layout audit is clean
at 1400×820, 820×520 and 560×380 over 28 captured configurations.

### Fixed (during the build)
- **`asin(C/R)` is the wrong way to invert a conic, and it fails silently at
  small b.** Solving `b sinφ + (D/2) cosφ = b²/r + D/2` as `R sin(φ + θ/2) = C`
  is algebraically right and numerically useless: at b = 1e-6 and D = 31.875,
  `C` and `R` agree to fifteen digits, the arcsine has no correct digits left,
  and `phiAtRadius` returned **φ = 0 for every radius** — which made the b = 0
  button produce NaN in the readout. In the half-angle variable `t = tan(φ/2)`
  the same equation is the plain quadratic `(D + q)t² − 2bt + q = 0` with
  `q = b²/r`, which returns 8.4e-9 and 1.2e-7, the right answers.
- **The velocity angle needed the conic's derivative, and the derivative has a
  closed form the radius cancels out of.** `atan2(dX/dφ, dY/dφ)` built from
  `r(φ)` and `r′(φ)` is NaN at φ = 0, where the radius is infinite — and φ = 0
  is exactly where every incoming particle is. Differentiating properly, the
  `b²/den²` factor cancels and the whole thing collapses to
  `χ(φ) = atan2((D/2)(1 − cosφ), b − (D/2) sinφ)`, with the versine written as
  `2sin²(φ/2)` (Known-bad, brachistochrone). It has no singularity anywhere,
  `χ(0) = 0` and `χ(φ_∞) = θ` exactly, and selfTest checks it against the
  brute-force derivative.
- **The plum pudding was ATTRACTIVE.** `puddingKick` rotated the velocity with
  the counter-clockwise matrix and a sign taken from the side, which pushed
  *both* sides of the beam inward. No bound on the deflection SIZE could see
  it, because the size is the same either way, and the first three rounds of
  tests were all bounds. Found by the assertion written to close a mutation
  survivor: `p(x>0).vx > 0 && p(x<0).vx < 0`.
- **A formula written out twice is a mutant waiting to survive.**
  `puddingKick` re-derived `θ(b) = (D/R)(b/R)√(1 − (b/R)²)` instead of calling
  `thomsonTheta`, and a mutant that dropped the square root survived a
  102-mutant sweep. It now calls the pinned function with `D_model = (D/R)·R`,
  which is the same number by construction. (Known-bad: the drum's group
  velocity, written out three times.)
- **A release test built from the current velocity lets a particle leave and
  re-enter the same atom on alternate ticks.** Once a particle is on its orbit
  its velocity has turned, so the box test has to use the frame the orbit was
  SET UP in, not a fresh one; and a particle released at the boundary must not
  be re-captured by the atom it just left.
- **`Math.floor(dtWall/DT_TICK)` throws the leftover away, and a browser frame
  is 16.6 ms against a 16.67 ms tick** — so the floor is zero on most frames
  and the sim crawls or stops outright. The leftover accumulates now, capped at
  0.2 s and at six ticks a frame so the loop always terminates.
- **Nothing in the orbit views was clipped to its box.** The hyperbola view
  drew its whole family from ±3 Rw and the lines ran across the caption and off
  the stage; the live views drew particles thrown back down the beam line over
  the gun and the census strip. Everything is clipped in DATA space now
  (a `ctx.clip()` would fix the browser and not the display-list audit, which
  records `clip()` as a no-op — Known-bad).
- **A canvas gradient records as an object, not a colour string.** The plum
  pudding's ball was filled with a `createLinearGradient`; the display-list
  audit cannot read it and `raster.py` paints an unparseable colour magenta, so
  the whole atom came out solid magenta. A flat premixed fill is what the
  capture can see — and the same objection applies to the browser's audit
  trail, not just the rasteriser's.
- **The family of orbits ran up the +x side only**, so three quarters of the
  frame was empty and the picture read as a spray out of the nucleus rather
  than a beam passing it — the same failure as drawing each conic in its own
  frame (Known-bad, `differential_scattering.html`). Both sides now.
- **`sigf()` was drawing `3.7x10^-14` on the canvas.** The shared formatter's
  exponent used a literal caret; canvas has no markup. Digit superscripts are
  safe in the rasteriser's font (letter ones are not), so it builds one.
- **A tick that lands exactly on the bottom-left corner of a plot box grazes
  the leftmost x-tick label by 7×1 px** — which `tools/audit.py`'s half-pixel
  rule reports and the eye reads as smear. `ticksNoFloor()` drops the edge
  tick; dropping it is cheaper than moving either label.
- **The stacked cross-section panels needed 64 px between them, not 30**: the
  upper panel's x-axis title ends 33 px below its frame and the lower panel's
  title starts 24 px above its own. And at a stacked width the two rotated
  y-axis titles overlapped each other, so they shorten.
- **A gold-ruler label that only dodges what it collides with still runs off
  the canvas** — "PhET's atomic-scale caption" ended at x = 597 on a 560 px
  stage. `sideLabel()` picks the side with room inside the panel first. Ten
  labels also need ten rows: with four they landed on each other and half of
  them were dropped.
- **The launch of a head-on orbit was checked against the wrong quantity.**
  derive.py's first `b = 0` integration started at `v = −1` from `r = 400`
  instead of `v = −√(1 − D/r₀)` and turned at 2.9777 for D = 3 — an 0.74 %
  "error" that was the right answer to the wrong question (that orbit really
  does have E = 0.50375 and turns at (D/2)/E). Same file, same day: the elapsed
  time along a conic was integrated from φ = 1e-12, where the integrand goes as
  1/φ² and the integral diverges, so the "RK4 error" it reported was entirely
  the lower limit.
- **Twelve mutation survivors, each a real gap.** The Poisson sigma (the bin
  test recomputed `3/√n` locally instead of reading the model's own — Known-bad:
  assert off a BUILT model); PhET's 4 % nudge window (doubling it leaves the
  smallest reachable |x| unchanged, so only the DENSITY it doubles can see it);
  `dφ/dt` and the speed law (every earlier assertion measured a *direction*,
  which the timing and the speed cannot change — now pinned against derive's
  quadrature of the elapsed time, and by the energy of every particle the
  engine is carrying); the orbit frame's j component (identically zero in the
  nuclear scene, so no straight-up launch could see it — now checked in a frame
  rotated by 0.7 rad); the beam's uniform x (nothing asserted it was symmetric
  or as wide as the box); the five atoms' positions; `DT_TICK`; and the
  Thomson kick's D, its charge and its direction.

### Known-bad candidates
- **A conic inverted through an arcsine loses every digit at small impact
  parameter, and it fails by returning zero rather than by throwing.**
  `b sinφ + (D/2) cosφ = C` written as `R sin(φ + δ) = C` has `C/R → 1` as
  `b → 0`; at b = 1e-6 and D = 31.875 it returned φ = 0 for every radius, which
  propagated NaN into the readout of the one case the view has a button for.
  The half-angle substitution `t = tan(φ/2)` turns the same equation into a
  quadratic with no cancellation. Generally: before inverting a trigonometric
  sum, check what its amplitude and its right-hand side do in the limit the UI
  can reach.
- **A deflection with the right magnitude and the wrong sign is invisible to
  every bound you will think to write.** The plum-pudding kick pulled both
  sides of the beam inward for three rounds of testing, because every assertion
  was of the form `|θ| < x` or `|θ| > y`. Any scattering angle needs one
  assertion about which WAY it goes, on both sides of the axis.
- **A canvas gradient is invisible to the display-list audit and reads as the
  rasteriser's error colour.** `createLinearGradient` records as an object, not
  a colour string; `tools/raster.py` paints an unparseable colour magenta, so a
  gradient-filled shape comes out as a solid magenta blob that looks
  deliberate. Premix the colour and fill flat, or the capture is not showing
  you what the sim draws.
- **The house `sigf()` writes its exponent with a literal caret**, which is
  fine in the readout's HTML and draws `3.7x10^-14` on the canvas. The copy in
  `build/rutherford-scattering/p1_utils.js` builds a digit superscript instead;
  the other sims in the collection still have the caret.
- **`Math.floor(dtWall/dt)` in a frame loop is a sim that does not run.** A
  browser frame is 16.6 ms and a 60 Hz tick is 16.67 ms, so the floor is zero
  on most frames. Accumulate the remainder (capped, and with a bounded number
  of catch-up ticks).
- **A timing law and a speed law leave no trace in any angle.** Every geometric
  assertion about a trajectory — the deflection, the closest approach, the
  asymptotes — is invariant to how fast the particle moves along it. Pin the
  elapsed time against a quadrature and the energy against its own definition,
  or `dφ/dt = L/mr²` and `v = v∞√(1 − D/r)` can be anything.
- **A frame whose second basis vector is (0,1) hides every mutation of its own
  j component.** In a scene where everything is launched straight up, `p.jx` is
  identically zero and a sign error in `pos = a + i·X + j·Y` changes nothing.
  Test placement in a deliberately rotated frame.
- **PhET's `atan2(X0, −Y0)` and its entry quadratic are safe only because its
  tracking region is a SQUARE rotated to the particle's direction.** On a
  bounding circle the discriminant `X0² − 2D(Y0 + r0)` goes negative for a
  grazing entry once `2D > R`, which the proton and energy sliders reach; on
  the square it stays positive over the whole slider space. The sim counts
  clamps and selfTest asserts the count is zero.
