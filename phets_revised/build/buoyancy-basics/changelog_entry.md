## 2026-09-22 — buoyancy-basics: PhET's Explore and Compare screens on density.html's engine, with the upthrust taken from the pressure on the faces

### Added
- `docs/phets_revised/buoyancy-basics.html` (160 KB, 2821 lines), a clean-room
  remake of PhET Interactive Simulations' **Buoyancy: Basics** (build 1.2.11)
  and the companion of `density.html`. Five views: **the pool** (PhET's Explore
  screen), **the sets** (Compare), **the faces**, **the scale** and **float or
  sink**. No PhET code or assets.
- **One engine, two sims.** `p2_physics.js` is byte-identical to
  `build/density/p2_physics.js` apart from its banner, and both files are pinned
  against the same `build/density/derive.py` and the same `refvals.txt`. What
  this sim adds is what PhET's Buoyancy adds: six fluids instead of water alone
  (gasoline 680, oil 920, water 1000, seawater 1029, honey 1440, mercury 13593
  — PhET's values), a scale on the ground and a scale in the pool, and the three
  forces drawn as arrows.
- **The two scales, and what they mean together.** The ground scale reads
  `ρ_b g V`, the pool scale reads `W − ρ_f g V_sub`, and the difference between
  them is asserted to be exactly the weight of the fluid the block pushed aside
  (118.44 N against 132.30 N for PhET's aluminium block). The pool scale is
  PhET's own 0.15 × 0.06 × 0.2 m box, displacing 1.8 L of fluid itself, and its
  height runs PhET's 0 to 1 — at 0 it stands on the floor and at 1 its top is
  level with the ground, both pinned. Raised, it holds a floating block *above*
  its own waterline, so the block rests on it and the reading is real: that is
  asserted rather than treated as a bug.
- **The faces view derives the upthrust instead of asserting it.** The
  hydrostatic pressure is drawn to scale on all six faces, the four sides cancel
  in pairs to exactly zero, and `(p_bot − p_top) A = ρ_f g (y_t − y_b) A =
  ρ_f g V` is checked three ways — the face integral, the per-edge polygon
  closed form and a 2000-point perimeter sum — with the residual printed in the
  readout. The net force is asserted **unchanged** when the block is taken twice
  as deep, while the pressure on its bottom face doubles.
- **The scale view draws the whole descent.** 241 solved points: the reading
  falls in a straight line while the block enters, then goes exactly flat at
  `(ρ_b − ρ_f) g V` once the top face is under — every one of the fully
  submerged points pinned to 49.000 N for a 5 L brick — and reaches zero with
  the string slack for anything that floats. The entering leg carries the real
  tilt, because the fluid rises to meet the block as it goes in.
- **Float or sink** is all 27 materials against all 6 fluids at once, ordered by
  density, with every cell's fraction checked against `min(1, ρ_b/ρ_f)` computed
  a second way. 23 of the 27 float in mercury (all but mercury itself, tantalum
  and gold and platinum); only styrofoam and wood float in gasoline.
- Provenance as in `density.html`: PhET's value beside the handbook value from
  Wikipedia's "Densities of various materials" (fetched 2026-09-21), with "no
  row" said for the six materials that table does not carry; gravity PhET's 9.8;
  PhET's "vacuum assumption" (air buoyancy ignored) stated, and the 0.06 % it
  costs a 5 L block quoted in the readout.
- Verification: `selfTest` **708 passed, 0 failed**; UI drive
  (`ui_drive_buoyancy-basics.js`) **189 passed, 0 failed**; mutation sweep
  **76 caught, 0 survived, 0 skipped** over 66 physics and 10 UI mutants;
  `audit.py` clean at 1400×820 and 820×520; 28 + 5 PNGs rasterised and looked at.

### Fixed (during the build)
- **The same registry gaps as `density.html`**, since the file carries the same
  helpers: block tags and scale readings drawn with a raw `fillText` were
  invisible to `lab()`'s dodging, `axes()` draws its tick labels, axis names and
  title outside any registry, the caption band was not reserved, and the
  right-column panels were painted after the stage. Fixed the same way —
  `labFixed()`, `axesReg()`, the caption rectangle pushed in `layout()`, panels
  drawn first, and each block's own rectangle registered.
- **The "ground scale" label collided with the block standing on it.** The name
  was placed above the platform, which is exactly where a block on the pan goes.
  It now moves under the scale when the scale is occupied.
- **Two axis ticks that will not fit.** "1000" and "1440" collided on the
  fluid-density strip at 900×600 and below; the strip now drops to two ticks
  under 300 px of panel.
- **Twenty-seven row names in 250 px.** The float-or-sink grid stacked its
  labels at 620×420. They are now thinned by *measured* spacing with the picked
  row drawn first so it is never the one dropped, and the canvas prints how many
  of the 27 are named.
- **Labels dodged into the block they were describing.** "fully submerged" and
  "the bottom is pressed hardest" were placed just outside the block's faces,
  which is where the pressure arrows are, so `lab()` moved them inside it. They
  are now placed beyond the arrow tips.
- **An axis fixed at 60 cm for a block 8 cm down.** The pressure-against-depth
  panel had a floor of 0.6 m whatever the block's depth, so at shallow settings
  both markers clustered in the top centimetre of the plot. It now fits the
  depth the block is at.
- **A caption that was wrong about its own picture, and a fix that silently
  did not apply.** "everything on the list floats in mercury except tantalum
  and platinum" — gold (19320) does not float in it either, nor does mercury
  itself. The first correction was written as a Python string replace whose
  pattern did not match the file (the source carries the literal glyph rho,
  not a \u escape) and it was not asserted, so it reported success and changed
  nothing; the PNG pass caught that the old text was still on the canvas.
  Corrected, and the claim is now pinned: the test computes which materials do
  not float in mercury and asserts the caption names each of them and none of
  the ones that do.
- **A 99.9 % cell printed as "100%"**, which reads as fully submerged in a grid
  whose whole point is the difference between floating and not. Cells above
  99.5 % now carry a decimal.
- **A caption naming a panel the view does not draw.** The sets caption
  described "the bars beside the pool"; the panel beside the pool is the
  mass–volume plane.
- **A marker silently clamped to the axis floor.** Wood's 400 kg/m³ line on the
  fluid-density strip was drawn hard against the left edge, where it reads as
  the axis. The floor is now 300 and a marker that still clamps says "(off the
  axis)".
- **Two test-side errors of my own.** Two assertions read `b.m` off
  `compareBlocks()`, which returns volume and density and no mass, so both
  compared "—,—"; and the mercury assertion in the scale view pinned the
  *held* block's submerged fraction (1, because it is being held on the floor)
  where it meant the free-floating one (0.1986).
- **A mutation sweep that could not see what only the UI exercises.** The
  mass/volume coupling, the two scales and the lowering curve were all reached
  only through the panel, so physics-only mutants on them survived. Each got its
  own `selfTest` coverage off the model — including the pool scale's support,
  which a mutant had quietly moved back to the pool floor.
- **An equivalent mutant, explained rather than patched.** "the ground scale
  reads `A.W − A.F_b`" cannot change anything, because a block on the ground
  scale is out of the pool and its buoyancy is exactly zero; it was replaced by
  a mutant that is not equivalent (reading the contact force instead).

### Known-bad candidates
- **A scale raised above a floating block's waterline makes the block REST on
  it, and the reading is not zero.** It looks like a bug (wood "pressing" on a
  scale) and is the physics: the scale holds the block higher than it would
  float, so it is only partly submerged and the scale takes `W − F_b`. Assert
  it, do not silence it.
- **A mutation sweep that runs only `selfTest` is blind to everything only the
  UI reaches.** Mass/volume coupling, a scale's support, a lowering curve — if
  the model's own tests never call them, physics mutants on them survive while
  the UI drive would have caught them. Either mark such mutants `u`, or (better)
  give the model its own assertions, because a model quantity that only the
  panel exercises is in the wrong layer.
- **A cell that rounds to 100 % in a table about floating.** 99.9 % under and
  fully submerged are the two states the table exists to distinguish; a
  zero-decimal formatter erases the distinction exactly where it matters.
- **A caption that counts.** "everything except tantalum and platinum" was
  wrong by two entries, and no assertion could see it because it was prose.
  Any caption that states a count should have that count asserted — the fix
  here was to make the test name the exceptions, not just the number.
- **A scripted edit that does not match reports success and changes nothing.**
  A `str.replace()` with no `assert s.count(old)==1` beside it is a silent
  no-op when the pattern is wrong — here the patch was written with `\u03c1`
  where the file carries the glyph rho — and the build then goes on believing
  the fix landed. Every scripted patch in these two builds asserts its pattern
  matched exactly once; the one that did not was the one that failed, and only
  the PNG pass caught it, because prose is invisible to every other check.
- **A marker clamped to an axis edge reads as the axis.** If a reference line
  can fall outside the range, either widen the range or say on the canvas that
  it has been clamped.
