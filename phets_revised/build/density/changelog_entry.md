## 2026-09-22 — density: PhET's Intro, Compare and Mystery screens, with Archimedes' principle solved rather than approximated

### Added
- `docs/phets_revised/density.html` (169 KB, 2942 lines), a clean-room remake of
  PhET Interactive Simulations' **Density** (build 1.2.10). Five views: **the
  pool** (PhET's Intro screen), **the sets** (Compare), **the mystery**
  (Mystery), **mass and volume** and **the waterline**. No PhET code or assets;
  the house scaffold, 2-D layer and world helpers are extracted from
  `build_lagr/p1_head.html`, `build_lagr/p1_utils.js` and
  `build_buoy/p4_views.js` by `make_head.py`, and `fluidRect()`/`forceArrow()`
  come from the house's own `buoyancy.html`, which wrote them for this job.
- **Archimedes exactly, not approximately.** The free surface solves
  `G(y) = A_pool (y + H) − (every solid below y) = V_fluid` by bisection on a
  function proved non-decreasing (swept over 4001 levels), and the level taken
  is the **smallest** root, so a body spanning the pool's cross-section puts
  the surplus fluid above itself instead of inside itself. A floating cube's
  draft is `d = s ρ_b/ρ_f` and its submerged fraction `ρ_b/ρ_f` exactly, pinned
  against `scipy.brentq` on the force balance at 1.4e-17. A floating body
  raises the level by its own **mass**/(ρ_f A) and a sunk one by its own
  **volume**/A — two different laws, both asserted off the solver as well as
  from the closed form.
- **The upthrust computed twice.** The hydrostatic pressure integrated over the
  cube's six faces (bottom minus top, sides cancelling to exactly zero, one
  side face pinned to 59.0782 N from a 4000-strip integral) and round the
  polygon cross-section edge by edge with the linear-load closed form; the two
  agree with `ρ_f g V_sub` to 3e-16 relative, and the per-edge form agrees with
  a 2000-point perimeter sum to 1e-6.
- **The three awkward cases asserted, not assumed.** A block denser than the
  fluid (rests, `N = (ρ_b − ρ_f) g V`, submerged fraction exactly 1); one
  exactly at neutral buoyancy (fraction exactly 1, N = 0, a spring scale reads
  zero, and the hand force is unchanged at two different depths, so no depth is
  preferred); and one **wider than the pool's free surface** — a 216 L cube
  whose 0.36 m² footprint equals the pool's — where the fluid stands entirely
  above it at `−H + s + V_f/A`, and its floating counterpart rides on all of
  the fluid at `−H + V_f/A`.
- **PhET's measured data, with provenance.** Every material density is read out
  of PhET's own build and marked as PhET's; beside it is the handbook value
  from Wikipedia's "Densities of various materials" (fetched 2026-09-21), with
  **"no row"** said plainly for the six materials that table does not carry
  (brick, pyrite, apple, human, gasoline, honey). The four numbers that are
  teaching choices rather than measurements are named on screen: styrofoam 150
  against 75, concrete 3150 against 2400, PVC 1440 against 1175, and glass,
  which is simply aluminium's 2700 reused. Gravity is PhET's 9.8, not 9.80665,
  and the file says so.
- **The Mystery screen's claim is checked.** That the printed numbers identify
  the material is asserted rather than assumed: all fifteen blocks of PhET's
  three fixed sets are named correctly from mass and displaced volume rounded
  to the two decimals the sim shows, with a worst reading error of 0.17 % and a
  smallest gap to the runner-up of 3.30 %; and all 130 material × whole-litre
  combinations of the shuffled set, plus 1000 blocks over 200 seeds, come out
  right. PhET's set 2 A is built at 11340 where its own table says lead is
  11342 — a 0.018 % mismatch that is pinned rather than smoothed over.
- **The floating trap, made a control.** A floating block displaces its own
  *weight*, not its own volume, so left alone every floater measures as water
  whatever it is made of. "Hold them under" switches between the two, and the
  wrong answer is drawn (the floaters pile onto the water line on the density
  axis) rather than described.
- Verification: `selfTest` **872 passed, 0 failed**; UI drive
  (`ui_drive_density.js`) **179 passed, 0 failed**; mutation sweep **72 caught,
  0 survived, 0 skipped** over 63 physics and 9 UI mutants; `audit.py` clean at
  1400×820 and 820×520; 28 + 5 PNGs rasterised and looked at.
  `derive.py` (scipy) is the Python twin and `refvals.txt` its printed output.

### Fixed (during the build)
- **A block tag drawn with a raw `fillText` is invisible to the label
  registry.** The waterline caption ("water 102.0 L") landed on block A's "A" at
  900×600 and below. Root cause: `lab()` dodges only what is in `LABELS`, and
  the tags were painted straight to the canvas. Added `labFixed()`, which paints
  unconditionally *and* registers, and put every must-draw label through it.
- **`axes()` draws its tick labels, axis names and title outside any
  registry**, so dodging labels landed on them — "0.0" on "gasoline" in the
  waterline view, "400" on a note in the mystery view. The house `axesR`
  registers only the title; added `axesReg()`, which registers the tick labels,
  both axis names and the title.
- **The caption is painted last but occupies its band from the moment the
  layout is known.** At 620×420 a force label ("hand 29.4 N") was dodged down
  onto the prose. `layout()` now pushes the caption rectangle into `LABELS`
  before it returns.
- **Panels drawn after the stage cannot be dodged.** The right-column plots were
  painted after the pool, so stage labels had no way to avoid their axes. The
  three pool views now draw the right column first.
- **A wide stage drawing an equal-aspect square picture wastes two thirds of
  its width.** The pool was rendering about 350 px across in a 1244 px stage,
  and 0.30 m of empty sky above the pool took another 38 % of the height. Root
  cause: a pool is a *shape*, so its two axes must share a scale (the house
  rule), and a one-box layout then fits it by the smaller dimension. Added
  `splitMain()` — pool on the left, analysis panels down the right — and cut
  the world's top to `POOL_YTOP = 0.22`, with the drag clamped by
  `holdCeiling(s)` so a lifted block's top stays inside it.
- **Force arrows and their labels were painted over the block they belong to.**
  Arrows now run from the block's centre to its edges with labels beside it, and
  the block's own rectangle is registered, because with two blocks 26 px apart
  there is no room for a label between them.
- **A drawing scale computed at the call site cannot be pinned.** A mutant that
  handed each block its own weight as the arrow reference survived the sweep:
  `selfTest` was asserting `forceLengths()` while the draw call passed its own
  `Fref`. Root cause: the quantity was in the wrong layer. `forceScale()` now
  returns `{len, Fref}` together and the sweep catches every mutation of either.
- **A clamp enforcing a property the solve already guarantees is dead code.**
  `N = Math.max(0, W − F_b)` was unreachable: a block only ever rests when the
  upthrust cannot lift it, so `W − F_b ≥ 0` there by construction. Mutation
  testing correctly reported it as an equivalent mutant. The clamp is deleted
  and the property is swept instead — 84 configurations, minimum N exactly 0.
- **`cubeBelow` saturated at `s³`, not at `V`.** `s = V^(1/3)` is inexact in
  binary, so a fully submerged block reported a submerged fraction of
  1.0000000000000004. It now returns `V` exactly, and a test asserts that
  `s*s*s !== V`, which is why it has to.
- **A continuity assertion that asserted the wrong thing.** "G is continuous
  across the float/rest switch" was written as `ΔG = 2εA` and failed on correct
  code: G is continuous but its *slope* jumps there, from `A − s²` below to `A`
  above. Replaced by the true statements — the displaced volume is continuous
  (the gap across ±ε is exactly `s²ε`, and grows 100× when the probe does), and
  the two one-sided slopes are each pinned.
- **The mystery screen's scale was drawn buried.** Its platform was placed from
  −SCALE_H to 0, i.e. below ground level, so the block being weighed appeared to
  stand on the earth. The platform now stands *on* the ground with the block on
  its pan.
- **A horizontal log axis in a tall, narrow column.** The mystery density table
  was drawn across the bottom; after the layout change its column is 400 px wide
  and 600 tall, so the axis is now vertical, with the table's thirteen materials
  naming its left and the five readings pointing at its right.
- **Four anonymous dashed rays.** The mass–volume plane drew a handbook ray for
  every Intro material, unlabelled, so wood's 700 sat above wood's 400 with no
  way to tell which was which. Only the picked material now gets its handbook
  ray, labelled, and a material with no handbook row says so on the canvas.
- **Twenty-five labels stacked on a fifth of an axis.** In mercury every
  material's density ratio is below 0.4, so the waterline view's names piled up.
  Labels are now thinned by measured spacing, every material is still a dot, and
  the canvas prints how many of how many are named.
- **The draft panel drew a fraction it was not printing.** A resting block was
  placed on the tank floor at `−0.95 s`, which is shallower than the block is
  tall, so its top stood *above* the surface: the panel showed a neutrally
  buoyant block half out of the water under a readout saying 100 % under, and
  the dimension line measured that false draft ("15.62 cm of 17.10 cm"). Root
  cause: the tank depth had been chosen for a floating block and never checked
  against a resting one; the same constant then cut the top off a barely-wetted
  floater (styrofoam in gasoline floats with 78 % of its side in the air, against
  0.55 s of sky). The geometry is lifted out of the draw call into
  `draftGeom(M, h)` and asserted both ways — the drawn draft equals the model's
  submerged fraction over six material/fluid cases at three panel heights, and
  the old 0.95 s tank is re-run and shown to still get it wrong by 0.41.
- **A caption that named a panel the view no longer draws.** The sets caption
  still said "the panel below" after the plot moved to the right.
- **Prose claims that no assertion could see.** The mass-volume caption and its
  info paragraph state a count ("six materials have no handbook row") and name
  four of PhET's teaching choices; nothing checked that the prose and the data
  agreed. `selfTest` now pins the count against the table and asserts the
  paragraph names styrofoam, concrete, PVC and glass.
- **Two chip rows with the same seven labels.** The UI harness found the block-A
  material chip by label and arity and drove **block B**, because a label-only
  walk takes the last match. Chip rows are now addressed by group and row index.
- **A test that re-derived what it was testing.** The UI drive checked the
  lifted-block clamp against `holdCeiling()`, the same function the sim uses, so
  a mutant on it was invisible; pinned against an absolute 0.037 m instead.

### Known-bad candidates
- **A label painted with a raw `fillText` is invisible to the dodging
  registry, and so is everything `axes()` draws.** `lab()` avoids only what is
  in `LABELS`; `axesR` registers the plot title and nothing else. Tick labels,
  axis names, block tags, scale readings and the caption band all have to be
  registered explicitly, and the must-draw ones have to be registered *first* —
  which also means panels must be drawn before the stage whose labels should
  dodge them. Four separate collisions in one build came from this one gap.
- **A wide stage drawing an equal-aspect picture wastes most of its width, and
  empty sky above the subject wastes the rest.** A pool must be drawn at equal
  aspect because it is a shape, so a single full-width box fits it by height and
  leaves two thirds of the width empty. Split the stage (subject left, analysis
  panels right) and cut the world to what is actually drawn — then clamp any
  drag so the subject cannot leave the world it was cut to.
- **A tank sized for a floating body is too shallow for a resting one.** A block
  placed on the floor of a tank less than one block deep pokes out of the
  surface, and every quantity read off that drawing — the draft dimension, the
  submerged wash — then contradicts the readout beside it. The same constant is
  wrong at the other end for a body that barely dips in (78 % of a styrofoam
  cube is above the surface in gasoline). Size the drawn tank from the block,
  and assert that the DRAWN fraction equals the model's over both regimes.
- **A drawing scale computed at the call site cannot be mutation-tested.** If a
  view computes its own reference value and passes it to a helper, a mutant on
  the call site changes only pixels and survives. Return the scale and its
  reference together from one function, and assert the lengths off that.
- **A clamp that enforces what the solve already guarantees is dead code, and
  the sweep will say so.** `max(0, W − F_b)` on a contact force is unreachable
  because a block only rests when the upthrust cannot lift it. Delete it and
  sweep the property instead; a surviving mutant on a guard is usually telling
  you the guard is unreachable, not that the test is weak.
- **Saturating a submerged volume at `s³` instead of `V`.** `s = V^(1/3)` is
  inexact, so "fully submerged" prints 1.0000000000000004 and every `=== 1`
  assertion has to be loosened. Saturate at the quantity you were given.
- **"Continuous" and "smooth" are different claims.** The displaced volume is
  continuous across the float/rest switch; the free-surface function's slope is
  not (it jumps from `A − s²` to `A`). Asserting the second as though it were
  the first fails on correct code.
- **A UI harness that finds a chip by label and arity still finds the wrong
  one** when two groups carry the same list. Address chip rows by group and row
  index, not by what is written on them.
