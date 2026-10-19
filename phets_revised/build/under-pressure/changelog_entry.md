## 2026-09-23 — under-pressure: PhET's four pools, with the hydrostatic law and the unit definitions taken exactly

### Added
- **`docs/phets_revised/under-pressure.html`** — a clean-room remake of PhET
  Interactive Simulations' *Under Pressure* (build 1.1.36, the
  FLUID_PRESSURE_AND_FLOW repo), in the house six-view form. PhET's single
  screen carries four scenes and those are the first four views; the last two
  are analysis. New code; no PhET code or assets.
  - **the pool** — PhET's square pool at true proportion (3.7 × 3 m, and 2 m
    out of the page, so 22 200 L full), a faucet and a drain, two draggable
    gauges, the fluid-density and gravity sliders with PhET's named ticks, the
    atmosphere switch, the grid and the ruler, and the three unit chips. Beside
    it the same law as a line: intercept p_atm, slope ρg, both gauges on it.
  - **the shapes** — PhET's trapezoid pool. Two chambers tapering in opposite
    directions, joined along the floor: a gauge in each at the same depth reads
    the same number with 1.35× (at half fill) to 2.83× (at 0.5 m) as much fluid
    standing over one as the other. The side panel shows why the level is so
    well behaved — the two widths are equal and opposite linear functions of
    height and **sum to a constant 3.85 m**.
  - **the press** — PhET's chamber pool: a 1.00 m² piston and a 4.60 m² one,
    Pascal's principle solved rather than scripted, with displacement against
    load drawn as two straight lines whose slopes are in the ratio of the areas.
  - **the mystery** — PhET's mystery pool, with what each of the three
    candidates would read at every depth, and the inversion that names the
    answer.
  - **the paradox** — four vessels, one base, one depth, 3.1 to 8.4 m³ of
    fluid, one base force; with the difference tracked into the slanted walls
    by an integral that never uses the force balance.
  - **the column** — the whole sim as one straight line, and the same pressure
    on all three of PhET's scales at once.
- **What is exact.** The hydrostatic law p = p_atm(y_surface) + ρgh with no
  approximation, asserted against `build/under-pressure/derive.py` for every
  fluid tick × gravity tick × depth {0, 1.5, 3} m with the atmosphere on and
  off, at the surface and at the floor, and swept over 11 466 points of the two
  continuous sliders (all finite, none negative, max 363 522.2142857142 Pa).
  A second, independent route — integrating dp/dy = −ρg in 4000 slabs — agrees
  to 5e-13 relative.
- **The unit conversions are the definitions, not rounded factors.** 1 atm =
  101 325 Pa exactly; 1 psi = (0.45359237 kg × 9.80665 m/s²)/(0.0254 m)² =
  6894.7572931683608 Pa; 1 ft = 0.3048 m. So 1 atm = 14.69594877551345 psi and
  every round trip over 0–4 MPa is exact to **1.434e-16**. PhET 1.1.36 stores
  9.8692e-6 atm/Pa and 1.4504e-4 psi/Pa; the panel prints how far those are
  from the definitions (3.31e-6 atm, 2.29e-4 psi at one atmosphere).
- **The trapezoid's volume-to-level map is exact**, where PhET's is a linear
  stand-in: the cross-section is 5.145 m wide through the floor channel and
  3.85 m above it, so the level is piecewise linear with one kink, inverted
  exactly (round trip 1e-12) and cross-checked against `scipy.integrate.quad`.
- **Pascal is derived, not asserted.** Matching the pressure at one point by
  the two routes (down from the loaded surface, down from the free one) gives
  Δp = (ρg + λ)Δh with λ the air's own lapse, and because Δp = Mg/A₁ and λ both
  carry g, **g cancels**: Δh = M/(A₁(ρ + λ/g_earth)) with the atmosphere on and
  the classical M/(ρA₁) exactly with it off. The air simply subtracts its own
  1.2482993197278909 kg/m³. selfTest asserts both closed forms and asserts that
  a gauge reads the same pressure whichever surface you come down from, to
  1e-9 Pa, at every mass × fluid × atmosphere setting.
- **The paradox is computed twice.** The weight is the exact integral of a
  piecewise-linear width profile; the vertical pressure on the walls is the
  separate integral ∫p(y)w′(y)D dy done term by term; the identity
  F_wall,z = W − F_base is then a *check*, not a definition (worst residual
  6.5e-11 N). F_base/W = 1, 0.5714285714285714, 1.5483870967741937,
  0.67377877596855684, independent of the fluid and the gravity (asserted).
- **The memo key is complete, and that is now a stated property.** Every view
  caches its model under a key built from the state it reads; selfTest changes
  each of **51 (view, input) pairs** with no `clearAll()` in between and
  asserts the key notices, and separately asserts the memo really does cache.
  That makes the two surviving UI mutants equivalent *by construction* rather
  than by luck.
- **Verification.** `selfTest` **785 passed, 0 failed** under `osascript` and
  under `jsc`; the UI drive `build/under-pressure/ui_drive_under-pressure.js`
  **324 passed, 0 failed**; `tools/audit.py` reports **0 layout problems** on
  both the 1400 × 820 capture (29 configurations) and the 820 × 520 one; every
  view's PNG was rasterised and looked at. `mutants.json` carries **81 mutants
  (66 physics, 15 UI)**, each pattern checked unique in the shipped file by
  `gen_mutants.py`. A confidence run in `_out/quickcheck.py` (not the
  definitive sweep — the orchestrator runs that) has **66/66 physics caught**
  and **13/15 UI caught**, the two survivors explained below.

### Fixed (during the build)
- **PhET's own trapezoid pool has a 7 cm gap in it, and its own
  `isPointInsidePool` agrees.** Its `bottomChamber` runs to x = 6.0 while the
  right chamber's foot is at x = 6.07, leaving a wedge that closes only at
  y = −2.8286; 5948 sampled points inside that wedge are reported as *outside*
  the pool, so a gauge dropped there reads air rather than fluid
  (`build/under-pressure/_out/gap.py` is the evidence). Root cause: the channel
  and the chamber borders were authored from different constants and never
  reconciled. This file runs the channel to x = 6.2 and asserts connectivity at
  41 heights of the band — and asserts that PhET's 6.0 really does leave the
  gap, so the fix cannot be quietly undone.
- **The drawn trapezoid held 3.2 % more fluid than the model said.** Symptom:
  `polyAreaW(fluidPolys) × DEPTH_OUT` was 12.202 m³ against a model volume of
  11.822. Root cause: the fluid was drawn as three polygons — two chamber
  trapezia running the full height plus the floor channel — which **overlap**
  inside the channel band, and the cavity outline was three overlapping
  rectangles whose strokes cut through both chambers. Rebuilt as
  non-overlapping pieces (one sliding band below the channel top, two chamber
  trapezia above it) and one U-shaped cavity outline; selfTest now asserts the
  drawn area *is* the model volume at 3 %, 50 % and 100 % full, and that the
  chamber pool holds the same fluid loaded and unloaded.
- **A gauge in the air above the ground read "no reading".** PhET's
  `getPressureAtCoords` returns the air pressure for any y > 0 and so does
  physics; `probeFlat` tested "is it inside the pool?" first and reported
  everything outside as unreadable. Root cause: one predicate doing two jobs.
  Split into three cases — air above the ground, solid ground, pool cavity —
  in both `probeFlat` and `chamberPressure`, with the readout now saying
  "buried in the ground" only where that is true. Six assertions added.
- **Pascal's Δh = M/(ρA₁) is not the equilibrium when the air has weight.**
  Symptom: a gauge at y = −2.5 in the chamber read 4894 Pa differently
  depending on which surface it was reached from — in a *connected* fluid, so
  one of them had to be wrong. Root cause: Δh was taken as Δp/(ρg) while the
  two free surfaces sit at different heights and PhET's air pressure lapses
  with height, so the air column between them carries part of the load. The
  exact solve (above) drops the residual to 0 and gives a closed form in which
  g still cancels.
- **The house legend takes `[colour, text]` arrays, not `{c, t}` objects.**
  Four panels passed objects, so `legendBox` drew the literal string
  `undefined` three or four times per panel — and the *physics* suite could not
  see it, because nothing there inspects canvas text. Found by the text audit
  in the layout sweep.
- **`legendAuto` records its box in `LEGEND_RECTS`, which `lab()` never
  consults**, so a note placed in "the empty corner" landed on the legend.
  Added `legendReg()`, which registers the returned box in `LABELS`.
- **The word "undefined" in ordinary prose trips the panels-clean scan.** Two
  strings ("undefined at the surface", "undefined at h = 0") were reworded
  rather than excepted — the pulsar Known-bad says the check should stay blunt.
- **A picture contradicting its own caption: the "flask" was not a flask.** The
  profile is a narrow cylinder stepping out to a wide one, i.e. the neck is at
  the *bottom*. Renamed "stepped" everywhere (JS, derive.py, the tests, the
  capture list) rather than redrawing it.
- **The mystery panel drew its three candidates on top of each other.** A few
  kPa of separation on an axis running from zero is invisible, which is exactly
  the thing that view exists to show. The axis is now fitted to the fan, with
  "the axis starts at … not at zero" printed on the canvas (the house rule for
  any scale distortion).
- **The column view's title named three fluids when one was drawn.** It now
  names the slider's fluid when the three-fluid checkbox is off.
- **The weight arrow in the paradox ran out through the base** at shallow
  depths (it was anchored at the fluid surface and scaled by the largest weight
  in the row), and at full depth the two arrows crossed. Anchored at the top of
  the vessel, with a horizontal offset clamped to the *narrowest* of the two
  heights the arrows are drawn at, so the tapered vessel's arrow stays inside
  its own wall.
- Layout, all found by the audit or by looking: the chamber world gave away a
  third of its height to empty sky (ymax 1.35 → 0.62); the grid's labels sat on
  the ruler's (moved to the right edge); the gauge boxes stacked on each other
  when two gauges were at the same height (they now dodge through eight
  candidate positions); the gauge's probe dot was not in the label registry;
  the column's three unit scales interleaved on a short stage (one scale is
  drawn there instead, and says so) and their names sat on their own first tick
  (a 54 px gutter); a marker callout in the last third of a plot landed under
  the floating readout (it flips); the "slope ρg" note was quoted in kPa/m on
  an axis drawn in atm.
- **The gauge's own reading — the number the whole sim exists to print — was
  pinned by nothing.** A mutant that reversed the probe's depth
  (`pressureAt(ySurf-y…)` → `pressureAt(y-ySurf…)`) survived: every assertion
  on the gauges compared A against B, and both flipped together, while every
  absolute pressure pin went through `pressureAt` directly rather than through
  the probe. Root cause: the same quantity reached by two code paths, only one
  of which was pinned. Now the default gauge reading is asserted absolutely in
  all three units (110163.35 Pa = 110.16335 kPa = 1.0872277325 atm =
  15.977843065 psi), at the surface, in honey on Jupiter and with the
  atmosphere off.
- **`G_MARS` survived a sweep.** The hydrostatic table passes the literal
  `3.71`, the slider sweep only asserts finiteness, and Δh in the press is
  independent of g — so nothing anywhere would have moved if Mars's gravity
  were wrong. Root cause: a constant used only as a range endpoint. All six of
  PhET's named values are now pinned absolutely *and* reached through
  `G_TICKS`/`G_RANGE`/`RHO_RANGE`, which is how the UI gets to them.
- **Pressing a draggable marker dead on its centre makes the grab radius
  untestable.** `dx*dx+dy*dy <= 26*26` mutated to `<= 0` survived, because the
  harness pressed at exactly the marker's mapped position and `0 <= 0` holds.
  Every drag now presses 8 px off-centre, and a press 40 px away is asserted
  to grab nothing.
- **Two guards on one path, again.** The pointermove handler's `dirty = true`
  and its `S.pointer(...)` return value both survived, because `pointerdown`
  had already set the flag. The drag tests now press, drain the flag, prove
  the loop idle, and only then fire the move.
- **The drag clamp was never exercised.** Every test drag stayed inside the
  world, so deleting the clamp changed nothing. A drag 4000 px off the stage
  now has to land exactly on the world's left edge and floor.
- **A stale audit read as a pass.** After one edit the capture aborted (the
  self-test failed inside `cap_run.js`) and `audit.py` silently re-read the
  *previous* `display_narrow.json`, reporting the identical collision after a
  change that provably removed it. Exactly the Known-bad; the tell is that the
  audit output does not move at all. The capture's exit code is checked now.

### Mutants that survive, and why they are equivalent
- **`a slider marks the frame dirty`** — the slider, checkbox and chip handlers
  all call `refresh()`, which calls `S.draw()` unconditionally, so the
  frame-loop `dirty` flag is redundant on the control path and deleting it
  changes nothing visible. It is load-bearing only on the pointer path, which
  has its own proven-idle test (and whose mutant is caught).
- **`a tab change clears the memo`** — each view memoises under a key built
  from every input it reads, so a stale entry can never be returned; selfTest
  proves this over 51 (view, input) pairs with no `clearAll()` in between.
  `clearAll()` is therefore redundant everywhere it appears. It is kept because
  it is the family idiom and costs nothing, and the redundancy is now a stated,
  asserted property rather than an accident.

### Known-bad candidates
- **The house legend helpers take POSITIONAL pairs, `[colour, text]`.**
  `legendBox`/`legendAuto` read `it[0]` and `it[1]`; an object `{c, t}` yields
  `undefined` from `plain(it[1])` and draws that word, silently, once per entry.
  No physics assertion can see it — only a canvas-text audit can. Check the
  helper's signature before passing it anything.
- **`legendAuto`'s box is NOT in the `LABELS` registry.** It records into
  `LEGEND_RECTS`, which only the polyline-crossing check reads, so every later
  `lab()` is free to land on top of it. Wrap it (`legendReg`) or push the
  returned box yourself.
- **Drawing one region as several overlapping polygons makes "the drawn area
  is the model volume" fail by the overlap**, and the overlap is invisible at
  a glance because the fills are translucent and identically coloured. Build
  fluid/cavity geometry as a partition, not a union, whenever a test multiplies
  its area by anything.
- **A vessel whose free surfaces sit at different heights has an air column
  between them, and that column has weight.** Any two-surface hydrostatic
  balance (a manometer, a hydraulic press, a U-tube) written as Δp = ρgΔh is
  wrong by λ/(ρg) ≈ 0.12 % in water as soon as the model's atmosphere varies
  with height. The tell is a pressure that depends on which surface you came
  down from. Solve Δp = (ρg + λ)Δh, and note that g cancels out of Δh either
  way.
- **"Is it inside the container?" is not the same question as "is there
  anything here to measure?"** A probe above the ground is in the air and reads
  the atmosphere; only a probe inside solid matter reads nothing. Collapsing
  the two into one `inside()` test silently turns the whole sky into a dead
  zone.
- **An axis from zero hides any effect that rides on a large offset.** Three
  fluids differing by 4 kPa on top of 101 kPa are one line at that scale. Fit
  the axis to the structure and print the fact that it is not zero-based —
  which is the same house rule as printing any other scale distortion.
- **Check the exit code of the display-list capture before believing the
  audit.** `cap_run.js` contains the sim's own `selfTest`, so a failing suite
  aborts the capture *before* it writes the JSON, and the next `audit.py` reads
  the previous run's file and reports the previous run's problems. The tell is
  an audit whose output does not change at all after an edit that provably
  changed the drawing.
- **PhET's trapezoid pool (build 1.1.36) is not watertight.** Its bottom
  chamber ends at x = 6.0 and its right chamber's foot is at x = 6.07. Anyone
  porting that geometry gets a 7 cm dead wedge at the floor. Do not "restore"
  the 6.0.
- **A pair of readings that must agree pins neither of them.** "Gauge A equals
  gauge B" survives any error that moves both — here, reversing the sign of the
  probe's depth. Whenever a view's headline number is reached by a second code
  path (a probe, a picker, a formatter), pin that path against an absolute
  value, not only against its twin.
- **A constant that is only ever a RANGE ENDPOINT is invisible.** `G_MARS`
  appears in a slider range, a tick list and a sweep that checks only
  finiteness; every physics assertion passed the literal 3.71 instead. Pin such
  constants absolutely *and* evaluate something through the range object, or a
  wrong value ships.
- **Pressing a draggable marker at exactly its own centre makes its grab
  radius untestable** — `dx² + dy² <= 0` is true there, so the threshold can be
  mutated to zero and every drag test still passes. Press off-centre, and
  assert separately that a press outside the radius grabs nothing.
