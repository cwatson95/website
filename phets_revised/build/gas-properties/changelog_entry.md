## 2026-09-18 — gas-properties: PhET's four screens on an exact event-driven hard-disk engine, and where the gauge's pressure and the Maxwell–Boltzmann law come from
### Added
- `gas-properties.html` (216 KB), a remake of PhET's Gas Properties 1.1.10 in six views: *the gas
  law*, *the moving wall*, *the energy*, *diffusion*, *the pressure* and *equilibrium*. The credit
  line is in the header and on the page, the site nav is absolute, and nothing touches the network.
- *The gas law* is PhET's Ideal screen, with every control PhET's has:
  - the pump, heavy or light, where a full stroke adds 50, as in PhET;
  - the particle counts (0–1000 each);
  - the heater, which springs back to zero when released;
  - the left-wall grip: the sim pauses while it is dragged and the disks are spread over the new
    width;
  - the lid knob, PhET's blow-off rule (above 20,000 kPa unless the gap is ≥ 1500 pm), return lid
    and erase;
  - Hold Constant (Nothing, V, T, P↕V, P↕T), with PhET's enabling rules and all six of its Oops
    cases;
  - the thermometer (K/°C), the gauge (atm/kPa, with PhET's 0.75-ps refresh and optional noise
    law), the stopwatch, the collision counter (5/10/20 ps) and the width ruler.

  House additions: P and T traces over time, and the readout prints the invariant the chosen hold
  keeps (P/T, PV, V/T, NT).
- *The moving wall* is PhET's Explore screen. The wall does work elastically (v′ = 2u − v) at no
  more than a speed limit (PhET's 800 m/s by default, adjustable from 10 to 800). The view shows the
  wall's velocity arrow, T against the width set against the hard-disk adiabat and the point law,
  T over the adiabat (the irreversibility), and the wall speed as a Mach number.
- *The energy* is PhET's Energy screen: the 1-ps histograms (19 bins of 170 m/s and of 1.33 zJ)
  for heavy, light and all particles, the zoom levels, the average speeds, the injection
  temperature (match the container, or set 50–1000 K) and the collisions switch. The exact 2-D
  Maxwell–Boltzmann counts are drawn over the bars.
- *Diffusion* is PhET's Diffusion screen:
  - two species in a 16 × 8.75 nm box, each with its number, mass, radius and starting
    temperature on PhET's grids;
  - PhET's quirks kept: a new mass or temperature resets every particle of that species to
    √(3kT/m), and putting the divider back restarts both sides;
  - the centres of mass, the 300-frame flow rates, the scale, and normal or slow time;
  - a house trace of the centres of mass.
- *The pressure* (house view) sets the momentum the walls actually receive against PhET's gauge.
  It breaks the ratio into (3/2) · W/(W−2r) · Z and plots Z against the area fraction beside the
  exact hard-disk B₂ and B₃.
- *Equilibrium* (house view) starts from one speed, from hot heavy and cold light disks, or from
  the pump. It shows the log energy histogram against e^(−E/kT₂), Boltzmann's H with its sampling
  floor, and equipartition.
- The gas engine is its own part, `build/gas-properties/p2_engine.js`, documented in `ENGINE.md`
  (API and invariants) for the `gases-intro` and `diffusion` jobs. It uses PhET's units (pm, ps,
  AMU) and PhET's frame (origin at the box's bottom-right corner).
- **Exact:**
  - Every collision inside a substep happens at its exact contact time, in time order. For two
    disks that is the earlier root of |dp + t dv|² = σ², in the cancellation-free form
    c/(−b + √(b² − ac)); for a moving wall it is linear. `derive.py` checks both in exact rational
    arithmetic.
  - Over 5000 random collisions with masses from 1 to 40, momentum is conserved to 3.4e-16 and
    energy to 1.5e-15.
  - Four brute-force event-driven runs in `derive.py` (O(N²), no grid, no substeps) are matched
    to 7e-8, 1.6e-7, 7e-7 and 7e-10 pm, with identical event counts. That includes a moving wall
    whose work, 23,040,000 AMU pm²/ps², matches to the last digit. A fifth run (R5) puts three
    stale predictions inside one substep: a pair event stale in its partner, one stale in its
    owner, and a wall event whose disk was struck first. It matches to 2e-11 pm, and the engine
    reports exactly three skipped events.
  - The energy ledger closes to 1e-15. The virial ledger, Δ(Σ m r·v) = ∫2KE dt + Σ r·J (walls)
    + Σ σ|J| (pairs) + heater + escapes, closes to about 1e-15 of its terms.
  - The injection is bit-exact against a mulberry32 and Box–Muller twin.
  - PhET's constants are pinned absolutely.
- **Statistics, with tolerances from the exact sampling law** (a closed box of hard disks has no
  potential energy, so the energy shares are Dirichlet(1,…,1), whatever the masses):
  - ⟨E²⟩/⟨E⟩² = 1.958 against 2N/(N+1) = 1.967 ± 0.038;
  - the mean √share is within 0.4 sd;
  - χ² = 13.0 against its exact-ensemble 99.99 % point of 35.8;
  - equipartition from a 6:1 split: D = 0.008 ± 0.040;
  - Z − 1 = 0.1102 against B₂+B₃ theory 0.11024 (B₂ alone, 0.1018, is excluded);
  - wall hits carry 1.481 × the mean energy against 2-D effusion's 3/2;
  - a slow push (20 m/s) ends at T·w/T₀w₀ = 1.0694 against the hard-disk adiabat's 1.0691
    (the point law gives 1.0111).
- **Verification:**
  - selfTest: 834 passed, 0 failed under osascript, in 13 s.
  - UI drive: 165 passed, 0 failed. Each of the three canvas drags moves the drawing through
    the frame loop from a proven-idle baseline.
  - Mutation sweep, on a copy inside `_out/sweep/`: 80 mutants (69 physics, 11 UI), 78 caught.
    The two survivors are equivalent and say so in their labels: `b >= 0 → b > 0` in the contact
    test (b = 0 leaves d = −ac ≤ 0, so the root is `Infinity` or `NaN` and no event is pushed
    either way), and halving the substep count (a speed knob: the event order inside a substep is
    exact for any h, and the grid's cells grow with h).
  - Audit: 0 layout problems at 1400×820, 1100×700 and 560×380.
  - Every view's PNG was looked at.
- **Sources:**
  - PhET's constants, read from `docs/phets/gas-properties_en.html`: BOLTZMANN 8316,
    KG_PER_AMU 1.66e-27, ATM_PER_KPA 0.00986923, the box 5–15 × 8.75 × 4 nm, the lid insets, the
    limits, the time transform, the histogram bins and the diffusion grids.
  - PhET's `doc/model.md` (raw.githubusercontent.com/phetsims/gas-properties/main/doc/model.md), fetched with curl on 2026-09-18 and followed; not copied into the build.
  - CODATA k_B/u, for the comparison only.
### Fixed (during the build)
- **The suite hung, drawing a flat curve.** The two species' mean-energy ratios were both 1 to the
  last bit, so the auto-ranged axis spanned about 2e-16 of its endpoints. The shared `ticksFor`
  steps `t += step`, and at that span t never advances, so the loop spun for ever. `niceRange()`
  now widens any sub-rounding span before ticks are asked for, and selfTest draws a series flat to
  the last bit.
- **Every plot threw.** `plotSeries` was defined without the short-title parameter its callers
  passed, so the series array landed in the options slot.
- **The wall-pressure plot showed 1 ps of a 5-ps run.** Passing `x0` skipped measuring the data,
  and the far end fell back to 1.
- **"Push slowly and T·V = const" was the point-particle law, and it was false for these disks.**
  A 20-m/s push of 100 heavy disks measured 1.07, not 1.011. The cause is finite size: Z > 1 and
  the excluded strip W − 2r. The quasi-static hard-disk adiabat, ln T₁/T₀ = ∫Z dW/(W − 2r), gives
  1.0691, which the engine reproduces, and the page now claims that. The same probe showed PhET's
  800 m/s limit is Mach 1.55 in the heavy gas, a shock that heats the gas to about 3× the adiabat.
- **Evaporation was predicted at 3/2 kT₂ and measured 1.95.** 3/2 is effusion, which needs a hole
  much smaller than the mean free path. The lid's widest gap is about twenty mean free paths, so
  the gas leaves as a jet carrying its enthalpy, 2kT₂. The test now brackets the escapees between
  the two limits, and pins the exact 3/2 on the wall hits of a closed box.
- **An Oops cleared itself.** Erasing while T was held raised PhET's Oops, and the button's
  after-action refresh cleared it the same instant. Controls now clear the *previous* Oops before
  they act.
- **The pressure view's Z marker used the wall-side Z.** That estimate carries the finite-run
  boundary term Δ(Σ m r·v)/2Et, about ±0.2 at 5 ps. The marker now uses the collision-side Z,
  which converges far faster, and a collisions-off gas sits on Z = 1.
- **A guessed 25 % tolerance on the collisions-off pressure** was replaced by a closed form. With
  collisions off, every bounce is periodic, so each wall's momentum is Σ 2m|vₓ| × (a closed-form
  hit count), and it matches to 2.6e-16.
- **At 560×380 the long caption squeezed the box** until the thermometer and gauge hung off the
  canvas and the dial covered the thermometer's label. The audit could not see this, because the
  covered text was still on the canvas. A scene with gauges now needs 330 px above its caption or
  takes the short one, and the instruments keep 170 px.
- **A narrow stage printed a caption describing plots it had dropped.** There is now a third,
  no-plots caption for that case.
- **The captions ran into the page's `#hint` line.** The hint is HTML (`bottom: 11px`, 11px
  type) over the canvas's bottom-left corner, so neither the capture nor the audit can see it,
  and every caption ended 23 px above the canvas bottom — inside it. Captions now reserve
  `HINT_H = 18` px (the fix the wave-on-a-string build found), and the layout sweep asserts that
  no canvas text reaches within 27 px of the bottom in the left 340 px, at four sizes.
- **The gas law's lone trace marker contradicted the readout.** The trace is seeded at t = 0, and
  an edit made while paused (a resize, the pump, erase) moves the state it describes: after
  halving the width the marker still read 11.6 atm beside a readout of 23.6. The seed is now
  re-taken while the trace is a single point and no time has passed.
- **A dashed reference line struck through an empty plot's note.** The diffusion view's
  centre-of-mass plot draws its zero line through the middle, where "run the clock to trace the
  centres of mass" sits. The audit could not see it: both were on the canvas. Notes are now
  drawn on a patch of the canvas ground.
- **Smaller defects in the pictures:**
  - the default gas-law view's plot row was blank at t = 0;
  - the centre-of-mass markers touched the plot title;
  - a narrow heater's label overflowed it;
  - the Energy screen's default zoom was 0–200, where PhET's is 0–100;
  - the gas law's "PV/NkT" row was 1 by construction, and is replaced by the hold's own invariant.
- **The first suite took 87 s.** Every configuration was rebuilt once per canvas size, and one of
  them held 1800 disks injected at a point. Configurations are now built once per size sweep, and
  sections throw at their boundary after a failure, with the 12-s statistics last, so a caught
  mutant costs seconds.
- **Defects in `derive.py`:**
  - numpy 2's repr leaked `np.float64(...)` into the generated JS;
  - the Dirichlet moments from gammaln were good only to 3e-14, and are now exact rationals;
  - the first moving-wall reference never hit the wall, so it pinned no work.
- **The first full mutation sweep left seven survivors.** Two are equivalent (see Verification).
  The other five were holes in the tests:
  - *Deleting the stamp check survived.* No test put a stale prediction inside a substep. Stale
    events only arise when a disk is struck by a third party before its predicted event, and
    none of the parity runs did that. R5 now does, in three ways.
  - *The lid's whole-disk escape rule survived being cut to the centre.* The rule was written
    twice, once in the opening prediction and once in the re-prediction, and every test reached
    only the first copy. The two routines are now one, `gasPredict(…, half)`, and a disk whose
    centre is in the gap but whose edge is under the lid must bounce.
  - *Shrinking the grid cell from σ + 2v_b·h to σ + 0.2v_b·h survived.* No test had fast pairs
    across a cell boundary. Now 20 head-on pairs at 3000 m/s, stepped across the cells, must
    all bounce in one frame.
  - *The overlap test survived c < −1 in place of c < 0.* Only deep overlaps were tested. A
    hair's overlap (c = −0.5 pm²) is now asserted.
  - *Deleting the Ideal wall's pause survived.* The pause is guarded twice, in the frame loop
    and in the model step, so each copy covered for the other. Each now has its own test: a
    grip held still costs no frames, and the step key does not step.
- **A mutant added after that sweep, re-predicting pairs only with higher indices, survived
  too.** No test checked that the disks never overlap. When a collision is missed, the two disks
  slide into each other and PhET's overlap rule lets them pass through. The energy and the
  statistics do not notice. selfTest now checks every pair of 400 disks (area fraction 0.22)
  every frame for 4 ps, through 1828 collisions. The closest approach is 1.25e-3 pm outside
  contact, and the mutant makes 602 overlaps.
### Known-bad candidates
- **The shared `ticksFor` spins for ever when an axis span is below the rounding of its
  endpoints.** `t += step` does not advance. Guard every auto-ranged axis, as `niceRange()` in
  `build/gas-properties/p4_views.js` does, or carry the guard into the shared layer.
- **PhET's T = (2/3)⟨KE⟩/k in a 2-D box means the walls feel 3/2 of the gauge,** and more through
  W/(W − 2r) and Z. Never compare a measured wall pressure with NkT/V without those factors.
- **PhET's moving wall (v′ = u − v) is not elastic** and does half the work. Its 800 m/s limit is
  supersonic in the heavy gas at 300 K, so a quasi-static (adiabatic) push needs about 20 m/s.
- **The energy per escaping particle depends on the Knudsen number:** 3/2 kT₂ for a hole much
  smaller than the mean free path (effusion), 2kT₂ for a jet. Say which regime a lid is in.
- **A time-averaged wall pressure carries a 1/t boundary term** (Δ(Σ m r·v)/2Et). The
  collisional virial converges far faster. Use it for a live estimate.
- **Hard disks are stiffer than points, even dilute:** 6.9 % above T·w = const (1.1 % from the excluded strip W − 2r, the rest from Z) at an area
  fraction of 0.05–0.07.
- **In an event-driven engine with a grid built at the substep's start, search neighbours from the
  cell a particle was registered in, not the one it has moved to.** Two disks that can still touch
  started within one cell width of each other.
- **A rule written twice hides from a mutation sweep.** The event engine's escape rule lived in
  both its opening prediction and its re-prediction. The tests reached one copy, so a mutant of
  the other survived. Keep one routine per rule, or test every copy.
- **PhET's overlap rule hides a missed collision.** The two disks pass through each other, energy
  is conserved, and the statistics barely move. Assert that disks started apart never overlap.
- **An event-driven engine needs a stale-event test.** Parity runs can pass with the stamp check
  deleted, because a stale event needs a third party to strike a disk before its predicted
  event. R5 in `build/gas-properties/derive.py` is a template.
- **Kill only your own processes, by full path.** A `ps | grep _mutant.js | kill` during this
  build killed osascript processes of other agents' concurrent mutation sweeps; every agent's
  scratch file has that name. Their `mutate.py` then logs the killed mutant as "caught".
