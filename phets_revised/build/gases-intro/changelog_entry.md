## 2026-09-21 — gases-intro: PhET's two intro screens, plus the P–V plane and the four gas laws measured off the simulation

### Added

`docs/phets_revised/gases-intro.html` (197 KB, 3424 lines), a clean-room remake
of PhET Interactive Simulations' **Gases Intro** 1.1.7 (CC-BY 4.0; new code, no
PhET code or assets). Built on the finished `gas-properties` remake: the
event-driven hard-disk engine (`build/gas-properties/p2_engine.js`, documented
in its `ENGINE.md`), the shared house layer, the drawing helpers and the
container/plot layer are taken **unchanged** by `make_shared.py`, which asserts
every block it slices.

**Four views.** `the box` is PhET's Intro screen, `the laws` its Laws screen,
`P against V` is the Laws screen's own gas on the pressure–volume plane, and
`the four laws` measures Boyle, Charles, Gay-Lussac and Avogadro by running the
simulation.

**What is exact.**

- PhET's Gases Intro is its Ideal screen twice over, and the minified original
  says so outright: `class wb extends vb{ … hasHoldConstantFeature:!1 }` is
  registered as `IntroScreen` and `class Sb extends vb{ …
  hasHoldConstantFeature:!0 }` as `LawsScreen`, both extending `IdealScreen`.
  The two screens therefore differ in exactly one thing — the Hold Constant
  panel — and the UI drive asserts that the Intro view hides it and the Laws
  view shows it.
- PhET's constants, read out of `docs/phets/gases-intro_en.html`: BOLTZMANN
  8316 AMU pm² ps⁻² K⁻¹ (+1.849e-4 against CODATA k_B/u = 8314.4626), KG_PER_AMU
  1.66e-27, ATM_PER_KPA 0.00986923, the box (8750 × 4000 pm, 5–15 nm wide), the
  masses and radii, the lid, the limits, the counter periods. Every one pinned
  absolutely.
- The 2-D Maxwell–Boltzmann one-sided flux ⟨vₓ⁺⟩ = √(kT₂/2πm), by scipy
  quadrature, and the identity ⟨vₓ⁺⟩ = ⟨v⟩/π exactly.
- The hard-disk contact measure M = 2πσab − 4σ²(a+b) + 2σ³ **term by term**:
  the edge integral ∫₀^σ 2 arccos(x/σ) dx = 2σ, and the corner term, which is
  where the +2σ³ comes from — the two edge arcs overlap exactly on the quarter
  disc x² + y² < σ², and that overlap integrates to σ²/2 per corner
  (analytically π²/16 + 1/4 twice, minus π²/8). Cross-checked against an
  8-million-sample Monte Carlo of the whole measure.
- PhET's heater as a rate: v → v(1 + a/800) per 60-fps frame, so 300 K → 1000 K
  takes 20.0788 ps at full heat — computed in closed form and frame by frame.

**The one falsifiable number on these screens** is the Collision Counter.
Nothing in PhET *defines* how often the disks strike the walls; kinetic theory
says the rate is 2 n Z ⟨v⟩/π (a + b) with a = W − 2r, b = H − 2r and n = N/ab.
For 100 heavy disks at 300 K in the 10 nm box that is **6.4234/ps** with Z = 1
and **7.2178/ps** with the hard-disk Z. `derive.py` gets that three independent
ways (the flux form, the per-particle free-flight form |vₓ|/a, and a
free-flight simulation of 4000 disks), and `selfTest` measures it off the
engine:

- collisions **off**, 200 disks, 60 ps: the measured count equals the
  closed-form free-flight count particle by particle, **exactly** (`eq`, not
  `close`), and the rate formula reproduces that realisation's mean;
- collisions **on**, 120 disks, 120 ps (~1000 hits, 3 % Poisson): the measured
  rate matches theory-with-Z within 3.5 σ and sits more than 2 σ **above** the
  Z = 1 value, so the measurement can tell the two apart.

`the four laws` runs a real sweep: it engages PhET's hold, steps the controlled
variable to five targets, settles 2 ps, then counts wall hits for the window.
The sim says plainly on the canvas and in the equation bar that the *law* line
is exact by construction (PhET defines P = NkT/V), so what the sweep tests is
the **controller** — and that the invariant holds to about 1e-9, which is PhET
rounding the held-pressure width to five decimals. The hit-rate panel beside it
is the half that could come out wrong.

`selfTest` **659 passed, 0 failed** (14 s); UI drive **149 passed, 0 failed**;
mutation sweep **75 mutants (64 physics, 11 UI), 75 caught, 0 survivors** — the
first pass left 17 alive and every one of them is written up below
(`_out/mutation_log.txt`, then `mutation_log_fix.txt`, `mutation_log_fix2.txt`
and `mutation_log_final.txt`, the last of which is the sweep of the file that
ships). `derive.py` writes `refvals.txt` and `p7a_refs.js`, so no pinned value
is retyped.

### Fixed (during the build)

- **A contact-measure "cross-check" that double-subtracted the corners.** The
  first quadrature subtracted each edge's removed arc independently, which
  over-counts on the quarter disc where two of them overlap, and it disagreed
  with the closed form by 2.5e-4 — looking exactly like a wrong closed form.
  Root cause: the four removed arcs are not disjoint. Replaced by a term-by-term
  check (edge integral, corner overlap integral, then the sum) plus a
  whole-measure Monte Carlo, which agree to 1.5e-12 and 9.5e-5 respectively.
- **The theory kept its Z with collisions switched off.** `hitRateTheory(g,true)`
  applied the hard-disk Z whatever `g.collisions` said, so the "with Z" curve
  would have claimed a crowding correction that is not there. Root cause: Z *is*
  the pair collisions; the flag has to reach the theory. Fixed, and both
  branches are now asserted (`useZ && g.collisions !== false`), with a mutant
  that removes the guard.
- **The Avogadro sweep measured a clump, not a gas, and read 38 % low.**
  Stepping N with PhET's pump puts every new disk at one point (−r, H/5), and
  fifty of them take tens of picoseconds to spread across a 10 nm box; the
  wall-hit rate measured 2 ps later is the rate of a clump near the entry
  point. Root cause: a *measurement* sweep needs a homogeneous gas, which the
  pump does not give. The sweep now changes the count with `gasFill` (uniform,
  non-overlapping) and says so in the code and the captions; the pump is still
  PhET's, on the screens where PhET uses it. A mutant restores the pump.
- **The Avogadro sweep ran to an area fraction where B₃ is not enough.** Its
  top target was 2.5 × the starting count (η = 0.14), where the truncated
  virial series under-predicts Z by more than the counting error. Capped at
  2 × (η = 0.112) and stated.
- **The Charles targets could round past the container's end.** PhET's
  hold-pressure controller solves w = NkT/(P H D) and rounds it to five
  decimals; a target that asks for exactly 15000 pm can round to 15000.00001
  and raise "Volume would be too large". The targets are now clamped a hair
  inside, and the derivation records that at P = 1183.248 kPa and N = 100 the
  container's 5–15 nm range is exactly 150–450 K.
- **The energy-ledger assertion normalised by a field that does not exist.**
  `gasLedger()` returns `{E, pred, resid}`; the test divided by `led.scale`,
  which is `undefined`, so `(led.scale||1)` made it an *absolute* 1e-12 bound on
  a residual of order 1e-7 on an energy of 1.5e9 — i.e. 1.6e-16 relative, which
  is rounding. It passed in one sim by luck and failed in the other. Now
  normalised by `led.E` in both.

**Seven drawing defects the PNGs caught and the audit could not.** The layout
audit compares text boxes with text boxes, so a curve running through a label,
a key covering the start of a trace, and a degenerate axis are all invisible to
it. Rasterising every view and looking at it found:

1. The hit-rate panel's three labels were struck through by the bars and lines
   they annotated. Every in-plot key now paints a patch of the canvas ground
   first (`keyAt`), the way `plotNote` already did.
2. **A hold makes two of P, V, T proportional, so they are drawn as the same
   line and one disappears under the other** — Charles's law and Gay-Lussac's
   law made invisible by being exactly true. Each series now has its own dash
   as well as its own colour, and the panel names the coincidence: "P and T
   move together: that IS Gay-Lussac's law".
3. Keys sat on the first 200 px of the very curves they described (the P–V
   key, both sweep keys). `keyText` now takes a corner, chosen per plot — and
   for the sweeps per *law*, since Boyle and Avogadro decay away from the top
   right while Charles and Gay-Lussac rise away from the top left.
4. The held-invariant axis auto-ranged onto a residual that is pure rounding,
   so all four ticks printed as "-0.0000". Below a thousandth of a ppm the axis
   is now fixed there and the key states the actual figure ("flat to 6.7e-10
   ppm — the controller is exact to rounding").
5. The hottest isotherm only clips the top-right corner of the P–V box, and the
   label search ran left to right and gave up, so it was drawn unlabelled. It
   now falls back to the entry point and hangs the label leftwards — and the
   mutant that removes the leftward hang survived the first sweep, because at
   the DEFAULT axis the label fits whichever way it hangs. Pinning it needed a
   state where it does not: cooled to 290 K the isotherm enters 0.1 nm³ from
   the right edge, and a rightward label runs off the plot. **A fallback has to
   be tested at the state that triggers it, not at the state you happen to be
   looking at.**
6. An empty P–V box auto-ranged to a 0.01 atm axis, which means nothing. It now
   falls back to the scale the default gas would set and says "there is no gas
   in the box yet".
7. The lone trace marker survived an erase and contradicted the readout beside
   it (12 atm on the plot, "—" in the panel). Re-seeded on draw, and pinned —
   the same fix the gas-properties remake needed.

One more, not a defect but a silence: after pumping, the measured wall-hit rate
can be tens of sigma below kinetic theory, because PhET's pump puts every
particle at one point and the theory assumes a uniform gas. The panel now says
how many sigma apart they are and that the gas may not be uniform yet, instead
of leaving the reader to conclude the theory is wrong.

**The mutation sweep, and the seventeen holes it found.** The first pass caught
54 of 71 and left 17 alive. Every survivor was a missing assertion, and the list
is worth reading as a list, because the *kinds* repeat:

- **Nothing pinned PhET's pump.** The π/2 fan, the √(3kT/m) speed and the
  restored Gaussian mean all mutated freely. Now: 1000 injections span the fan
  to FAN/1000 and are centred on π; with collisions off every speed is exactly
  √(3kT/m); with collisions on 200 injected at 437 K leave T at exactly 437
  while the individual speeds are visibly spread.
- **Dead code in the shared engine.** `hdZ1` is not called by this sim (`hdZ`
  computes the same thing by summing over pairs), so mutating it changed
  nothing. Rather than delete a function the engine owns, the test now asserts
  the two agree at N = 2, 50, 100, 400 — the identity, not a retyped formula.
- **The overlap branch of the contact quadratic had no boundary test.**
  `c < 0` → `c < −1` lets a pair overlapping by 0.002 pm collide, which no
  bulk statistic sees. Pinned at the join, the way the diffraction sim's
  small-argument series had to be.
- **PhET's five-decimal rounding of the held-pressure width was invisible**
  because every sweep target is a round number. Asserted on a width that is
  not: 137 disks going 317 K → 200 K ask for 6309.148… pm, and V/T can only
  hold to 8e-10 if the rounding really is at the fifth decimal.
- **The hold-T restore after a *partial* removal was untested** — the only
  removal any test did was "erase everything", which takes the empty-box Oops
  branch instead.
- **The Ideal wall's redistribution was untested**, in the model *and* in the
  pointer handler. Without it a narrowing leaves disks outside their own box;
  `gasWidthTo` moves the wall and nothing puts them back.
- **The lid's blow-off gap and the gauge's 0.75-ps refresh** had no test at all.
- **Two sweep knobs were self-consistent and therefore invisible**: the settle
  (now asserted to be exactly long enough for the overlaps a halving resize
  creates to separate) and the counting window (now asserted to equal what the
  slider says).
- **The P–V isotherm was computed inside the draw call**, so a mutant that drew
  it at 2T could only be caught by looking at the picture. Lifted into
  `pvIsotherm()` — the Known-bad rule that "if a mutant can only be caught by
  looking at the picture, the quantity is in the wrong layer".
- **A pointer-DOWN that repaints nothing** was invisible because the harness's
  recorder does not capture colours, and the grab's only effect is that the grip
  turns magenta. Assert that a frame was *drawn* from a proven-quiet loop, not
  that the geometry moved.

Two of the seventeen survived a second time, and both for the same reason —
**the test was written in terms of the thing it was meant to pin**:

- the lid-gap test set its gaps as `LID_WIDE ± 200`, so mutating `LID_WIDE`
  moved the test with it. Absolute gaps (1700 pm and 1200 pm) now.
- the Avogadro-clump test called `sweepSetCount` directly, while the mutant
  changes the *call site* inside `sweepApply`. The test now drives the real
  sweep.

And the third, the Charles clamp, survived because nothing asserted what the
guard guards; it now asserts that the extreme targets ask for a width strictly
inside the container (and only just). **73 caught, 0 survivors.**

### Known-bad candidates

- **A sweep that changes the particle count with the pump is measuring a clump
  for the first tens of picoseconds.** PhET's `addParticles` puts every new
  particle at one point; the gas needs roughly W²/(π²D) to homogenise (≈ 36 ps
  for 200 heavy disks in the 10 nm box, longer when it is cold). Any
  measurement taken over a settle shorter than that is of the injection, not of
  the gas — it read 38 % low here. Use a uniform fill for measurements and keep
  the pump for the screens that are about the pump.
- **A "cross-check" of a closed form by re-integrating its terms independently
  can be wrong in exactly the place the closed form is right.** Removed arcs,
  excluded areas and shadowed regions overlap near corners; subtracting them
  one at a time over-counts. Check term by term against the *derivation's own*
  decomposition, or Monte-Carlo the whole thing, and say which you did.
- **A flag that switches the physics must reach the theory curve as well as the
  model.** Switching particle collisions off makes the gas ideal, so a theory
  curve that keeps its compressibility factor is drawing a correction that the
  simulation no longer has. Assert both branches.
- **`gasLedger()` has no `scale` field.** `{E, pred, resid}` only. An assertion
  written as `1e-12*(led.scale||1)` is an absolute bound of 1e-12 on a quantity
  of order 1e9, i.e. 1e-21 relative — unreachable, and it passes only when the
  residual happens to be tiny in absolute terms. Normalise by `led.E`.
- **A test whose own SETUP is written in terms of the constant it is meant to
  pin cannot see that constant change.** The lid test built its gaps as
  `LID_WIDE + 200` and `LID_WIDE − 300`, so doubling `LID_WIDE` moved the gaps
  with it and every assertion still held. Two of seventeen survivors were this,
  and it is invisible on reading — the test looks careful. Write the setup in
  absolute numbers and pin the constant separately.
- **A test that exercises the HELPER does not test the CALL SITE.** The
  Avogadro-clump assertion called `sweepSetCount` directly while the mutant
  swapped the call inside `sweepApply` for PhET's pump; the helper was perfect
  and the sweep was wrong. When the defect you are guarding against is "somebody
  calls the other function", the test has to go through the caller.
- **A defensive clamp with nothing asserting what it guards is indistinguishable
  from dead code.** The Charles targets are held a hair inside the container so
  the controller's `toFixed(5)` cannot round past the end; removing the clamp
  changed no outcome at any reachable setting. Either assert the property the
  clamp provides (here: the extreme targets ask for a width strictly inside the
  range, and only just) or delete it.
- **A pointer-DOWN must repaint, and the display-list harness cannot see why.**
  Grabbing a handle changes only its colour, and the recorder captures geometry,
  not styles — so "the picture changed" is the wrong assertion. Assert that a
  frame was *emitted at all* from a proven-quiet loop.
- **A law that is exactly true draws two curves on top of each other, and the
  law disappears.** Hold V and P/T is constant, so the normalised P and T
  traces are the same line; hold P and so are T and V. Whichever is drawn
  second hides the first, and the screen that exists to show the law shows one
  curve. Give every series its own DASH as well as its own colour, and say on
  the canvas that they coincide — the coincidence is the result.
- **An auto-ranged axis on a residual that is pure rounding prints every tick
  as "-0.0000".** The house `tickFmt` caps at four decimals, so an axis a
  billionth of a ppm wide has four identical labels and tells the reader
  nothing. Fix the axis at a readable floor and print the real figure in the
  key. (Related to the existing Known-bad about `ticksFor` spinning on a span
  below its endpoints' rounding — `niceRange` stops the hang, not the
  meaninglessness.)
- **A fallback branch must be tested at the state that triggers it.** The
  P–V isotherm label falls back to hanging leftwards when its curve enters near
  the right edge; at the default axis it fits either way, so the mutant that
  removed the fallback survived a 75-mutant sweep with the drawing asserted and
  the label present. The assertion only bites at 290 K, where the isotherm
  enters a tenth of a nm³ from the edge. Same shape as the Known-bad about
  series branches that no test argument reaches — but for *layout*, where the
  triggering state is a range of the axis rather than a range of the argument.
- **The layout audit cannot see a line crossing a label, a key covering the
  start of a trace, or an axis whose ticks are all the same.** All three shipped
  past a clean audit here and were found only by rasterising every view and
  looking at it. The audit is necessary and it is not sufficient; the brief's
  "then actually look at the PNGs" is load-bearing.
